// Lớp truyền tải trừu tượng: bản thật dùng fetch + WebSocket, bản demo chạy server Go trong trình duyệt (wasm).
export interface HttpResult {
  status: number;
  json: unknown;
}

export interface SocketLike {
  readonly readyState: number; // 0 connecting, 1 open, 2 closing, 3 closed (giống WebSocket)
  onopen: (() => void) | null;
  onmessage: ((data: string) => void) | null;
  onclose: (() => void) | null;
  onerror: (() => void) | null;
  send(data: string): void;
  close(): void;
}

export interface WireTransport {
  readonly label: string;
  request(method: 'GET' | 'POST', path: string, body?: unknown, token?: string, signal?: AbortSignal): Promise<HttpResult>;
  openSocket(): SocketLike;
}

export class BrowserTransport implements WireTransport {
  readonly label: string;
  constructor(private readonly apiBase: string) {
    this.label = apiBase;
  }

  async request(method: 'GET' | 'POST', path: string, body?: unknown, token?: string, signal?: AbortSignal): Promise<HttpResult> {
    const headers: Record<string, string> = {};
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    if (token) headers.Authorization = `Bearer ${token}`;
    const init: RequestInit = { method, headers };
    if (body !== undefined) init.body = JSON.stringify(body);
    if (signal) init.signal = signal;
    const res = await fetch(this.apiBase + path, init);
    let json: unknown = null;
    try {
      json = await res.json();
    } catch {
      json = null;
    }
    return { status: res.status, json };
  }

  openSocket(): SocketLike {
    const url = this.apiBase.replace(/^https:/, 'wss:').replace(/^http:/, 'ws:') + '/ws';
    const ws = new WebSocket(url);
    const like: SocketLike = {
      get readyState() {
        return ws.readyState;
      },
      onopen: null,
      onmessage: null,
      onclose: null,
      onerror: null,
      send: (d) => ws.send(d),
      close: () => ws.close(),
    };
    ws.onopen = () => like.onopen?.();
    ws.onmessage = (ev) => like.onmessage?.(String(ev.data));
    ws.onclose = () => like.onclose?.();
    ws.onerror = () => like.onerror?.();
    return like;
  }
}
