// Kiểm tra M0: /healthz, đăng ký tài khoản dùng một lần, WS auth.session. Không in token.
import { AuthResponse, ServerMessage } from '@phimond/protocol';
import { API_BASE, WS_URL } from '../net/config.ts';

export async function runSmoke(log: (line: string) => void): Promise<void> {
  const health = await fetch(`${API_BASE}/healthz`).then((r) => r.json());
  log(`healthz: ${JSON.stringify(health)}`);
  const name = `web_${Math.random().toString(36).slice(2, 10)}`;
  const reg = await fetch(`${API_BASE}/api/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: name, password: `Pw-${crypto.randomUUID()}` }),
  });
  if (!reg.ok) throw new Error(`register ${reg.status}`);
  const auth = AuthResponse.parse(await reg.json());
  log(`register: ok (${name})`);
  await new Promise<void>((resolve, reject) => {
    const ws = new WebSocket(WS_URL);
    const timer = setTimeout(() => reject(new Error('ws timeout')), 10000);
    ws.onopen = () => ws.send(JSON.stringify({ op: 'auth.session', request_id: `smoke-${Date.now()}`, data: { token: auth.token } }));
    ws.onmessage = (ev) => {
      clearTimeout(timer);
      const msg = ServerMessage.parse(JSON.parse(String(ev.data)));
      log(msg.op === 'state' ? `ws auth: ok, revision ${msg.data.character.revision}, map ${msg.data.character.map_id}` : `ws error: ${msg.data.message}`);
      ws.close();
      resolve();
    };
    ws.onerror = () => reject(new Error('ws error'));
  });
}
