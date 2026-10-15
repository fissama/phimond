import type { HttpResult, SocketLike, WireTransport } from './transport.ts';

interface Engine {
  http(method: string, path: string, body: string, token: string): { status: number; body: string };
  open(): string;
  send(conn: string, frame: string): { out: string; closed: boolean };
  close(conn: string): void;
}
declare global {
  interface Window { phimondEngine?: Engine; phimondEngineReady?: boolean }
  // eslint-disable-next-line no-var
  var Go: new () => { importObject: WebAssembly.Imports; run(i: WebAssembly.Instance): Promise<void> };
}

const base = (): string => import.meta.env.BASE_URL;
function loadScript(src: string): Promise<void> {
  return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.onload = () => res(); s.onerror = () => rej(new Error('script ' + src)); document.head.appendChild(s); });
}

/** Chạy server Go thật (engine + catalog) dưới dạng WebAssembly trong trình duyệt. Chỉ dùng cho bản demo; kho dữ liệu nằm trong RAM. */
export async function loadEngine(): Promise<Engine> {
  if (window.phimondEngine) return window.phimondEngine;
  await loadScript(`${base()}engine/wasm_exec.js`);
  const go = new Go();
  const url = `${base()}engine/engine.wasm`;
  let inst: WebAssembly.WebAssemblyInstantiatedSource;
  if (WebAssembly.instantiateStreaming) {
    try { inst = await WebAssembly.instantiateStreaming(fetch(url), go.importObject); }
    catch { inst = await WebAssembly.instantiate(await (await fetch(url)).arrayBuffer(), go.importObject); }
  } else inst = await WebAssembly.instantiate(await (await fetch(url)).arrayBuffer(), go.importObject);
  void go.run(inst.instance);
  for (let i = 0; i < 200 && !window.phimondEngineReady; i++) await new Promise((r) => setTimeout(r, 25));
  if (!window.phimondEngine) throw new Error('engine không khởi động');
  return window.phimondEngine;
}

export class LocalTransport implements WireTransport {
  readonly label = 'local-wasm';
  constructor(private readonly eng: Engine) {}

  request(method: 'GET' | 'POST', path: string, body?: unknown, token?: string): Promise<HttpResult> {
    // bất đồng bộ giả lập mạng để đảm bảo thứ tự xử lý giống bản thật
    return new Promise((resolve) => setTimeout(() => {
      const r = this.eng.http(method, path, body === undefined ? '' : JSON.stringify(body), token ?? '');
      let json: unknown = null; try { json = JSON.parse(r.body); } catch { json = null; }
      resolve({ status: r.status, json });
    }, 0));
  }

  openSocket(): SocketLike {
    const eng = this.eng; const conn = eng.open();
    let state = 0;
    const like: SocketLike = {
      get readyState() { return state; },
      onopen: null, onmessage: null, onclose: null, onerror: null,
      send: (d) => {
        if (state !== 1) return;
        setTimeout(() => {
          if (state !== 1) return;
          const r = eng.send(conn, d);
          if (r.out) like.onmessage?.(r.out);
          if (r.closed) { state = 3; like.onclose?.(); }
        }, 0);
      },
      close: () => { if (state === 3) return; state = 3; eng.close(conn); setTimeout(() => like.onclose?.(), 0); },
    };
    setTimeout(() => { state = 1; like.onopen?.(); }, 0);
    return like;
  }
}
