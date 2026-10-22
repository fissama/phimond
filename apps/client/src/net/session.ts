import { signal, type ReadonlySignal } from '@preact/signals';
import {
  AuthResponse,
  Catalog,
  ServerMessage,
  type BattleEvent,
  type Character,
  type IntentMap,
  type IntentOp,
} from '@phimond/protocol';
import type { SocketLike, Wire } from './transport.ts';

export type ConnectionStatus = 'idle' | 'connecting' | 'online' | 'offline';

/** Một lô trạng thái đã được server xác nhận (một revision). */
export interface Batch {
  revision: number;
  character: Character;
  events: BattleEvent[];
  presentation: Record<string, unknown> | undefined;
  requestId: string;
}

export type SendResult =
  | { ok: true; revision: number; character: Character }
  | { ok: false; message: string; reason: 'rejected' | 'offline' | 'timeout' };

export const RESPONSE_TIMEOUT_MS = 15_000;
export const CONNECT_TIMEOUT_MS = 10_000;

interface Pending {
  op: IntentOp;
  resolve: (r: SendResult) => void;
  timer: ReturnType<typeof setTimeout>;
}

/**
 * Phiên chơi trên một WebSocket.
 *
 * Quy tắc (packages/protocol/README.md):
 * - Khung đầu tiên là auth.session; token chỉ ở đó hoặc header HTTP.
 * - Mỗi intent một request_id duy nhất. Không tự gửi lại intent chưa rõ kết quả.
 * - Cho phép nhiều intent đang chờ cùng lúc (P01 §9 D1: di chuyển pipeline). Giới hạn do lớp gọi quyết định.
 * - Trạng thái chỉ áp dụng khi sequence (revision) mới hơn; sự kiện phát đúng một lần mỗi revision,
 *   không phát lại khi vừa xác thực lại (resuming).
 * - Quá RESPONSE_TIMEOUT_MS không có phản hồi: kết nối coi như hỏng, đóng và báo lỗi mọi intent đang chờ.
 */
export class Session {
  private token = '';
  private revision = -1;
  private lastEventRevision = -1;
  private socket: SocketLike | null = null;
  private readonly pending = new Map<string, Pending>();
  private counter = 0;
  private readonly prefix = `${Date.now().toString(36)}-${Math.floor(Math.random() * 1e9).toString(36)}`;
  private readonly batchListeners = new Set<(b: Batch) => void>();

  private readonly _status = signal<ConnectionStatus>('idle');
  private readonly _character = signal<Character | null>(null);
  private readonly _catalog = signal<Catalog | null>(null);
  private readonly _inFlight = signal(0);
  private readonly _lastError = signal('');

  readonly status: ReadonlySignal<ConnectionStatus> = this._status;
  readonly character: ReadonlySignal<Character | null> = this._character;
  readonly catalog: ReadonlySignal<Catalog | null> = this._catalog;
  readonly inFlight: ReadonlySignal<number> = this._inFlight;
  readonly lastError: ReadonlySignal<string> = this._lastError;

  constructor(private readonly wire: Wire) {}

  get loggedIn(): boolean {
    return this.token !== '';
  }

  onBatch(fn: (b: Batch) => void): () => void {
    this.batchListeners.add(fn);
    return () => this.batchListeners.delete(fn);
  }

  /** Đăng nhập hoặc đăng ký, nạp catalog rồi mở WebSocket. */
  async login(username: string, password: string, register = false): Promise<void> {
    const res = await this.wire
      .request('POST', register ? '/api/register' : '/api/login', { username, password })
      .catch(() => ({ status: 0, json: null }));
    if (res.status !== 200) throw new Error(errorText(res.json, res.status));
    const auth = AuthResponse.parse(res.json);
    this.token = auth.token;
    const cat = await this.wire.request('GET', '/api/content');
    if (cat.status !== 200) throw new Error(errorText(cat.json, cat.status));
    this._catalog.value = Catalog.parse(cat.json);
    await this.connect();
  }

  /** Mở (hoặc mở lại) WebSocket và xác thực. Không phát lại sự kiện cũ. */
  connect(): Promise<void> {
    if (!this.token) return Promise.reject(new Error('Chưa đăng nhập'));
    this.dropSocket();
    this._status.value = 'connecting';
    const sock = this.wire.openSocket();
    this.socket = sock;
    const authId = this.nextId();
    return new Promise<void>((resolve, reject) => {
      let settled = false;
      const timer = setTimeout(() => finish(new Error('Không kết nối được máy chủ')), CONNECT_TIMEOUT_MS);
      const finish = (err?: Error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        if (err) {
          this.dropSocket();
          this._status.value = 'offline';
          this._lastError.value = err.message;
          reject(err);
        } else {
          this._status.value = 'online';
          resolve();
        }
      };
      sock.onopen = () => sock.send(JSON.stringify({ op: 'auth.session', request_id: authId, data: { token: this.token } }));
      sock.onmessage = (raw) => {
        if (!settled) {
          const msg = parse(raw);
          if (msg?.request_id !== authId) return;
          if (msg.op === 'error') return finish(new Error(msg.data.message));
          // Xác thực lại: nhận trạng thái mới nhất nhưng không phát lại sự kiện đã lưu.
          this.applyState(msg.sequence, msg.data.character, [], undefined, authId, true);
          return finish();
        }
        this.handle(raw);
      };
      sock.onclose = () => {
        if (sock !== this.socket) return;
        if (!settled) return finish(new Error('Mất kết nối khi xác thực'));
        this.lostConnection('Mất kết nối máy chủ');
      };
      sock.onerror = () => undefined; // onclose luôn theo sau
    });
  }

  /** Gửi một intent. Trả về khi server xác nhận/từ chối, hoặc khi kết nối hỏng. */
  send<K extends IntentOp>(op: K, data: IntentMap[K]): Promise<SendResult> {
    const sock = this.socket;
    if (!sock || sock.readyState !== 1 || this._status.value !== 'online') {
      return Promise.resolve({ ok: false, message: 'Chưa kết nối máy chủ', reason: 'offline' });
    }
    const id = this.nextId();
    return new Promise<SendResult>((resolve) => {
      const timer = setTimeout(() => {
        // Không biết server đã áp dụng hay chưa: không gửi lại, coi kết nối là hỏng.
        this.lostConnection('Máy chủ không phản hồi');
      }, RESPONSE_TIMEOUT_MS);
      this.pending.set(id, { op, resolve, timer });
      this._inFlight.value = this.pending.size;
      sock.send(JSON.stringify({ op, request_id: id, data }));
    });
  }

  async logout(): Promise<void> {
    const token = this.token;
    this.token = '';
    this.dropSocket();
    this.failAll('Đã đăng xuất', 'offline');
    this._status.value = 'idle';
    this._character.value = null;
    this.revision = -1;
    this.lastEventRevision = -1;
    if (token) await this.wire.request('POST', '/api/logout', undefined, token).catch(() => undefined);
  }

  private handle(raw: string): void {
    const msg = parse(raw);
    if (!msg) return;
    const p = msg.request_id ? this.pending.get(msg.request_id) : undefined;
    if (msg.op === 'error') {
      if (p) this.settle(msg.request_id, { ok: false, message: msg.data.message, reason: 'rejected' });
      else this._lastError.value = msg.data.message;
      return;
    }
    this.applyState(msg.sequence, msg.data.character, msg.data.events, msg.data.presentation, msg.request_id, false);
    if (p) this.settle(msg.request_id, { ok: true, revision: this.revision, character: this._character.value! });
  }

  private applyState(
    sequence: number,
    character: Character,
    events: BattleEvent[],
    presentation: Record<string, unknown> | undefined,
    requestId: string,
    resuming: boolean,
  ): void {
    // Bản cũ hơn (đến trễ, trùng request) không được ghi đè trạng thái mới hơn.
    if (sequence < this.revision) return;
    const fresh = sequence > this.revision;
    this.revision = sequence;
    this._character.value = character;
    if (!fresh) return;
    const emit = !resuming && sequence > this.lastEventRevision;
    if (resuming || emit) this.lastEventRevision = sequence;
    const batch: Batch = { revision: sequence, character, events: emit ? events : [], presentation, requestId };
    for (const fn of this.batchListeners) fn(batch);
  }

  private settle(id: string, r: SendResult): void {
    const p = this.pending.get(id);
    if (!p) return;
    clearTimeout(p.timer);
    this.pending.delete(id);
    this._inFlight.value = this.pending.size;
    p.resolve(r);
  }

  private failAll(message: string, reason: 'offline' | 'timeout'): void {
    for (const id of [...this.pending.keys()]) this.settle(id, { ok: false, message, reason });
  }

  private lostConnection(message: string): void {
    this.dropSocket();
    this._status.value = 'offline';
    this._lastError.value = message;
    this.failAll(message, 'timeout');
  }

  private dropSocket(): void {
    const s = this.socket;
    this.socket = null;
    if (!s) return;
    s.onopen = s.onmessage = s.onclose = s.onerror = null;
    try {
      s.close();
    } catch {
      /* đã đóng */
    }
  }

  private nextId(): string {
    this.counter += 1;
    return `${this.prefix}-${this.counter}`;
  }
}

function parse(raw: string): ServerMessage | null {
  try {
    const r = ServerMessage.safeParse(JSON.parse(raw));
    return r.success ? r.data : null;
  } catch {
    return null;
  }
}

/** Dịch thông báo lỗi tiếng Anh thường gặp của server (đăng nhập, giới hạn tần suất). */
const SERVER_TEXT: [RegExp, string][] = [
  [/Unable to sign in\/register/i, 'Không đăng nhập/đăng ký được. Tên tài khoản 3–24 ký tự (không trùng), mật khẩu 10–72 ký tự.'],
  [/too many/i, 'Thao tác quá nhanh, thử lại sau ít giây.'],
  [/unauthori[sz]ed|invalid session/i, 'Phiên đăng nhập đã hết hạn, hãy đăng nhập lại.'],
];

function errorText(json: unknown, status: number): string {
  // Server trả {"message": "..."} khi lỗi (transport.fail).
  if (json && typeof json === 'object' && 'message' in json && typeof (json as { message: unknown }).message === 'string') {
    const m = (json as { message: string }).message;
    return SERVER_TEXT.find(([re]) => re.test(m))?.[1] ?? m;
  }
  if (status === 0 || status >= 500) return 'Máy chủ không phản hồi, thử lại sau.';
  return `Lỗi máy chủ (${status})`;
}
