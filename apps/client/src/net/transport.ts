// Lớp truyền tải: tách fetch/WebSocket khỏi Session để unit test bằng socket giả.

export interface HttpResult {
  status: number;
  json: unknown;
}

/** Tập con của WebSocket mà Session dùng. readyState: 0 connecting, 1 open, 2 closing, 3 closed. */
export interface SocketLike {
  readonly readyState: number;
  onopen: (() => void) | null;
  onmessage: ((data: string) => void) | null;
  onclose: (() => void) | null;
  onerror: (() => void) | null;
  send(data: string): void;
  close(): void;
}

export interface Wire {
  request(method: 'GET' | 'POST', path: string, body?: unknown, token?: string): Promise<HttpResult>;
  openSocket(): SocketLike;
}

/** apiBase rỗng = cùng origin (dev qua proxy Vite, production cùng host). */
export function apiBaseFromEnv(): string {
  const v = (import.meta.env.VITE_GAME_API_URL as string | undefined) ?? '';
  return v.replace(/\/$/, '');
}

export class BrowserWire implements Wire {
  constructor(private readonly apiBase: string) {}

  async request(method: 'GET' | 'POST', path: string, body?: unknown, token?: string): Promise<HttpResult> {
    const headers: Record<string, string> = {};
    if (body !== undefined) headers['Content-Type'] = 'application/json';
    // Token chỉ đi qua header, không bao giờ nằm trong URL (protocol README).
    if (token) headers.Authorization = `Bearer ${token}`;
    const res = await fetch(this.apiBase + path, {
      method,
      headers,
      body: body === undefined ? null : JSON.stringify(body),
    });
    let json: unknown = null;
    try {
      json = await res.json();
    } catch {
      json = null;
    }
    return { status: res.status, json };
  }

  openSocket(): SocketLike {
    const base = this.apiBase || location.origin;
    const ws = new WebSocket(base.replace(/^https:/, 'wss:').replace(/^http:/, 'ws:') + '/ws');
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
