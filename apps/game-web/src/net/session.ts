import { signal, type ReadonlySignal } from '@preact/signals';
import {
  AuthResponse,
  Catalog,
  Character,
  ServerMessage,
  type BattleEvent,
  type IntentMap,
  type IntentOp,
} from '@phimond/protocol';
import { localizeCatalog } from '../i18n';
import { eventMessage, friendlyError, httpFailureText } from './text.ts';
import type { SocketLike, WireTransport } from './transport.ts';

export type ConnectionStatus = 'idle' | 'connecting' | 'online' | 'offline';

export interface Batch {
  revision: number;
  character: Character;
  events: BattleEvent[];
  presentation: { battle_id?: string; completed_battle?: unknown } | undefined;
  requestId: string;
}

export type SendResult = { ok: true; batch: Batch } | { ok: false; message: string };

export const RESPONSE_TIMEOUT_MS = 15000;

export class FriendlyError extends Error {}

interface Pending {
  resolve: (r: SendResult) => void;
  timer: ReturnType<typeof setTimeout>;
}

/**
 * Phiên chơi: giữ token trong bộ nhớ, một kết nối WS, một intent chờ tại một thời điểm.
 * Quy tắc (port từ PhimondClient.gd, packages/protocol/README.md):
 *  - Không tự gửi lại intent chưa rõ kết quả; quá 15 giây thì ngắt và yêu cầu kết nối lại.
 *  - Sự kiện chỉ phát một lần cho mỗi revision; snapshot cũ hơn revision hiện tại bị bỏ.
 *  - Khi vừa nối lại (resuming) không phát lại sự kiện đã lưu.
 */
export class Session {
  token = '';
  revision = -1;
  lastEventRevision = -1;

  private readonly _status = signal<ConnectionStatus>('idle');
  private readonly _busy = signal(false);
  private readonly _character = signal<Character | null>(null);
  private readonly _catalog = signal<Catalog | null>(null);
  private readonly _lastError = signal('');

  readonly status: ReadonlySignal<ConnectionStatus> = this._status;
  readonly busy: ReadonlySignal<boolean> = this._busy;
  readonly character: ReadonlySignal<Character | null> = this._character;
  readonly catalog: ReadonlySignal<Catalog | null> = this._catalog;
  readonly lastError: ReadonlySignal<string> = this._lastError;

  private socket: SocketLike | null = null;
  private pending = new Map<string, Pending>();
  private counter = 0;
  private readonly prefix = `${Date.now().toString(36)}-${Math.floor(Math.random() * 1e9).toString(36)}`;
  private connectTimer: ReturnType<typeof setTimeout> | null = null;
  private authRequestId = '';
  private resuming = true;
  private connectWaiter: { resolve: () => void; reject: (e: Error) => void } | null = null;
  private readonly batchListeners = new Set<(b: Batch) => void>();
  private readonly logListeners = new Set<(text: string) => void>();
  private readonly statusListeners = new Set<(s: ConnectionStatus) => void>();

  constructor(readonly wire: WireTransport) {}

  onBatch(fn: (b: Batch) => void): () => void {
    this.batchListeners.add(fn);
    return () => this.batchListeners.delete(fn);
  }
  onLog(fn: (text: string) => void): () => void {
    this.logListeners.add(fn);
    return () => this.logListeners.delete(fn);
  }
  onStatus(fn: (s: ConnectionStatus) => void): () => void {
    this.statusListeners.add(fn);
    return () => this.statusListeners.delete(fn);
  }
  private log(text: string): void {
    this._lastError.value = text;
    for (const fn of this.logListeners) fn(text);
  }
  private setStatus(s: ConnectionStatus): void {
    if (this._status.value === s) return;
    this._status.value = s;
    for (const fn of this.statusListeners) fn(s);
  }

  // ---------- HTTP ----------

  async authenticate(kind: 'register' | 'login', username: string, password: string): Promise<void> {
    let res;
    try {
      res = await this.wire.request('POST', `/api/${kind}`, { username, password });
    } catch {
      throw new FriendlyError(httpFailureText(0, false));
    }
    if (res.status < 200 || res.status >= 300) throw new FriendlyError(httpFailureText(res.status, false, kind));
    const parsed = AuthResponse.safeParse(res.json);
    if (!parsed.success) throw new FriendlyError('Máy chủ chưa cấp phiên đăng nhập. Vui lòng thử lại.');
    if (this.token !== parsed.data.token) {
      this.revision = -1;
      this.lastEventRevision = -1;
    }
    this.token = parsed.data.token;
  }

  async loadContent(): Promise<Catalog> {
    let res;
    try {
      res = await this.wire.request('GET', '/api/content');
    } catch {
      throw new FriendlyError(httpFailureText(0, false));
    }
    const parsed = Catalog.safeParse(res.json);
    if (res.status !== 200 || !parsed.success) throw new FriendlyError('Phản hồi máy chủ không hợp lệ. Vui lòng thử lại.');
    const cat = await localizeCatalog(parsed.data);
    this._catalog.value = cat;
    return cat;
  }

  async fetchLineage(petId: string): Promise<unknown> {
    const res = await this.wire.request('GET', `/api/lineage/${encodeURIComponent(petId)}`, undefined, this.token);
    if (res.status !== 200) throw new FriendlyError('Không tải được phả hệ.');
    return res.json;
  }

  async logout(): Promise<void> {
    const token = this.token;
    this.disconnect(false);
    this.token = '';
    this.revision = -1;
    this.lastEventRevision = -1;
    this._character.value = null;
    if (token) {
      try {
        await this.wire.request('POST', '/api/logout', undefined, token);
      } catch {
        /* đã xóa token cục bộ */
      }
    }
  }

  // ---------- WebSocket ----------

  connect(): Promise<void> {
    this.closeSocket();
    this.clearPending();
    this.resuming = true;
    this.setStatus('connecting');
    this.log('Đang kết nối máy chủ…');
    return new Promise<void>((resolve, reject) => {
      this.connectWaiter = { resolve, reject };
      let socket: SocketLike;
      try {
        socket = this.wire.openSocket();
      } catch {
        this.fail('Không thể kết nối máy chủ. Vui lòng kết nối lại.');
        return;
      }
      this.socket = socket;
      this.connectTimer = setTimeout(() => this.fail('Kết nối quá lâu. Vui lòng kết nối lại.'), RESPONSE_TIMEOUT_MS);
      socket.onopen = () => {
        this.authRequestId = this.newId();
        socket.send(JSON.stringify({ op: 'auth.session', request_id: this.authRequestId, data: { token: this.token } }));
      };
      socket.onmessage = (data) => this.onMessage(data);
      socket.onclose = () => {
        if (this.socket === socket) this.fail('Mất kết nối máy chủ. Vui lòng kết nối lại.');
      };
      socket.onerror = () => {
        /* onclose sẽ xử lý */
      };
    });
  }

  disconnect(announce = true): void {
    this.closeSocket();
    this.clearPending();
    if (this._status.value !== 'idle') this.setStatus('offline');
    if (announce) this.log('Đã ngắt kết nối.');
  }

  private closeSocket(): void {
    if (this.connectTimer) clearTimeout(this.connectTimer);
    this.connectTimer = null;
    const s = this.socket;
    this.socket = null;
    if (s) {
      s.onopen = s.onmessage = s.onclose = s.onerror = null;
      try {
        s.close();
      } catch {
        /* bỏ qua */
      }
    }
  }

  private fail(message: string): void {
    this.closeSocket();
    this.clearPending();
    this.setStatus('offline');
    this.log(message);
    const w = this.connectWaiter;
    this.connectWaiter = null;
    w?.reject(new FriendlyError(message));
  }

  private clearPending(): void {
    for (const p of this.pending.values()) {
      clearTimeout(p.timer);
      p.resolve({ ok: false, message: 'Mất kết nối trước khi nhận kết quả.' });
    }
    this.pending.clear();
    this._busy.value = false;
  }

  private newId(): string {
    this.counter += 1;
    return `${this.prefix}-${this.counter}`;
  }

  private onMessage(raw: string): void {
    let parsedJson: unknown;
    try {
      parsedJson = JSON.parse(raw);
    } catch {
      return;
    }
    const msg = ServerMessage.safeParse(parsedJson);
    if (!msg.success) {
      // Gói hỏng: không mở khóa input; để timeout/đồng bộ lại xử lý.
      return;
    }
    const m = msg.data;
    if (m.op === 'error') {
      const text = friendlyError(m.data.message);
      this.finishPending(m.request_id, { ok: false, message: text });
      if (!m.request_id) this.clearPending();
      this.log(text);
      return;
    }
    const seq = m.sequence;
    if (seq < this.revision) {
      this.finishPending(m.request_id, { ok: false, message: 'Trạng thái cũ bị bỏ qua.' });
      return;
    }
    const wasResuming = this.resuming;
    if (this.resuming) {
      this.resuming = false;
      if (this.connectTimer) clearTimeout(this.connectTimer);
      this.connectTimer = null;
      this.setStatus('online');
      this.log('Đã kết nối máy chủ.');
      const w = this.connectWaiter;
      this.connectWaiter = null;
      w?.resolve();
    }
    this.revision = seq;
    this._character.value = m.data.character;
    let events: BattleEvent[] = [];
    let presentation: Batch['presentation'];
    if (!wasResuming && seq > this.lastEventRevision) {
      events = m.data.events;
      presentation = m.data.presentation;
    }
    const batch: Batch = { revision: seq, character: m.data.character, events, presentation, requestId: m.request_id };
    this.finishPending(m.request_id, { ok: true, batch });
    for (const fn of this.batchListeners) fn(batch);
    if (seq <= this.lastEventRevision) return;
    this.lastEventRevision = seq;
    for (const ev of events) {
      const text = eventMessage(ev);
      if (text) this.log(text);
    }
  }

  private finishPending(requestId: string, result: SendResult): void {
    const p = this.pending.get(requestId);
    if (!p) return;
    clearTimeout(p.timer);
    this.pending.delete(requestId);
    this._busy.value = this.pending.size > 0;
    p.resolve(result);
  }

  // ---------- Intent ----------

  isOnline(): boolean {
    return this._status.value === 'online' && this.socket?.readyState === 1;
  }

  send<K extends IntentOp>(op: K, data: IntentMap[K]): Promise<SendResult> {
    if (!this.isOnline()) {
      this.log('Chưa kết nối máy chủ. Vui lòng kết nối lại.');
      return Promise.resolve({ ok: false, message: 'offline' });
    }
    if (this.pending.size > 0) {
      this.log('Đang chờ kết quả thao tác trước…');
      return Promise.resolve({ ok: false, message: 'busy' });
    }
    const requestId = this.newId();
    return new Promise<SendResult>((resolve) => {
      const timer = setTimeout(() => {
        // Có thể mất ack: yêu cầu snapshot mới, không bao giờ tự phát lại intent.
        this.fail('Chưa nhận được kết quả. Hãy kết nối lại để cập nhật trạng thái.');
      }, RESPONSE_TIMEOUT_MS);
      this.pending.set(requestId, { resolve, timer });
      this._busy.value = true;
      try {
        this.socket?.send(JSON.stringify({ op, request_id: requestId, data }));
      } catch {
        this.fail('Không thể gửi yêu cầu. Vui lòng kết nối lại.');
      }
    });
  }
}
