import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { Session, RESPONSE_TIMEOUT_MS, type Batch } from '../../src/net/session.ts';
import type { HttpResult, SocketLike, Wire } from '../../src/net/transport.ts';

class FakeSocket implements SocketLike {
  readyState = 0;
  onopen: (() => void) | null = null;
  onmessage: ((d: string) => void) | null = null;
  onclose: (() => void) | null = null;
  onerror: (() => void) | null = null;
  sent: { op: string; request_id: string; data: unknown }[] = [];
  closed = false;
  send(d: string) {
    this.sent.push(JSON.parse(d));
  }
  close() {
    this.closed = true;
    this.readyState = 3;
  }
  open() {
    this.readyState = 1;
    this.onopen?.();
  }
  reply(msg: unknown) {
    this.onmessage?.(JSON.stringify(msg));
  }
  last() {
    return this.sent[this.sent.length - 1]!;
  }
}

const char = (rev: number, x = 0) => ({
  id: 'c1', name: 'An', level: 1, map_id: 'm', x, y: 0, revision: rev, pets: [], inventory: {}, recipes: [], quests: {},
});
const state = (id: string, rev: number, x = 0, events: unknown[] = []) => ({
  op: 'state', request_id: id, sequence: rev, data: { character: char(rev, x), events },
});
const ev = (seq: number) => ({ seq, type: 'damage', actor_id: 'a', target_id: 'b', amount: 1, message: 'hit' });

class FakeWire implements Wire {
  sockets: FakeSocket[] = [];
  async request(_m: 'GET' | 'POST', path: string): Promise<HttpResult> {
    if (path === '/api/content') return { status: 200, json: { species: {}, skills: {}, maps: {}, npcs: {} } };
    if (path === '/api/logout') return { status: 200, json: { ok: true } };
    if (path === '/api/login') return { status: 200, json: { token: 'tok', character_id: 'c1' } };
    return { status: 401, json: { message: 'sai mật khẩu' } };
  }
  openSocket() {
    const s = new FakeSocket();
    this.sockets.push(s);
    return s;
  }
}

async function online(): Promise<{ s: Session; w: FakeWire; sock: FakeSocket }> {
  const w = new FakeWire();
  const s = new Session(w);
  const p = s.login('an', 'pw');
  await vi.waitFor(() => expect(w.sockets.length).toBe(1));
  const sock = w.sockets[0]!;
  sock.open();
  const auth = sock.last();
  expect(auth.op).toBe('auth.session');
  expect(auth.data).toEqual({ token: 'tok' });
  sock.reply(state(auth.request_id, 5, 0, [ev(1)]));
  await p;
  return { s, w, sock };
}

describe('Session', () => {
  beforeEach(() => vi.useFakeTimers({ shouldAdvanceTime: true }));
  afterEach(() => vi.useRealTimers());

  it('xác thực bằng khung đầu tiên và không phát lại sự kiện cũ', async () => {
    const batches: Batch[] = [];
    const w = new FakeWire();
    const s = new Session(w);
    s.onBatch((b) => batches.push(b));
    const p = s.login('an', 'pw');
    await vi.waitFor(() => expect(w.sockets.length).toBe(1));
    const sock = w.sockets[0]!;
    sock.open();
    sock.reply(state(sock.last().request_id, 5, 0, [ev(1)]));
    await p;
    expect(s.status.value).toBe('online');
    expect(s.character.value?.revision).toBe(5);
    expect(batches).toHaveLength(1);
    expect(batches[0]!.events).toEqual([]);
  });

  it('báo lỗi đăng nhập bằng thông điệp server', async () => {
    const s = new Session(new FakeWire());
    await expect(s.login('an', 'pw', true)).rejects.toThrow('sai mật khẩu');
  });

  it('cho nhiều intent chờ cùng lúc và khớp phản hồi theo request_id', async () => {
    const { s, sock } = await online();
    const a = s.send('world.move', { direction: 'right' });
    const b = s.send('world.move', { direction: 'right' });
    expect(s.inFlight.value).toBe(2);
    const [ida, idb] = [sock.sent[1]!.request_id, sock.sent[2]!.request_id];
    expect(ida).not.toBe(idb);
    sock.reply(state(idb, 7, 2));
    sock.reply(state(ida, 6, 1)); // đến trễ, cũ hơn
    await expect(a).resolves.toMatchObject({ ok: true });
    await expect(b).resolves.toMatchObject({ ok: true, revision: 7 });
    expect(s.character.value?.x).toBe(2); // bản cũ không ghi đè bản mới
    expect(s.inFlight.value).toBe(0);
  });

  it('phát sự kiện đúng một lần cho mỗi revision', async () => {
    const { s, sock } = await online();
    const batches: Batch[] = [];
    s.onBatch((b) => batches.push(b));
    const p = s.send('world.encounter', {});
    const id = sock.last().request_id;
    sock.reply(state(id, 6, 0, [ev(1)]));
    sock.reply(state(id, 6, 0, [ev(1)])); // trùng
    await p;
    expect(batches).toHaveLength(1);
    expect(batches[0]!.events).toHaveLength(1);
  });

  it('trả từ chối của server cho đúng intent', async () => {
    const { s, sock } = await online();
    const p = s.send('world.move', { direction: 'left' });
    sock.reply({ op: 'error', request_id: sock.last().request_id, data: { message: 'use a portal at the map edge' } });
    await expect(p).resolves.toEqual({ ok: false, reason: 'rejected', message: 'use a portal at the map edge' });
    expect(s.status.value).toBe('online');
  });

  it('quá hạn phản hồi thì đóng kết nối, không gửi lại', async () => {
    const { s, sock } = await online();
    const p = s.send('world.move', { direction: 'up' });
    const before = sock.sent.length;
    vi.advanceTimersByTime(RESPONSE_TIMEOUT_MS + 1);
    await expect(p).resolves.toMatchObject({ ok: false, reason: 'timeout' });
    expect(s.status.value).toBe('offline');
    expect(sock.closed).toBe(true);
    expect(sock.sent.length).toBe(before);
  });

  it('mất kết nối thì báo lỗi mọi intent đang chờ; gửi khi offline bị từ chối ngay', async () => {
    const { s, sock } = await online();
    const p = s.send('world.move', { direction: 'up' });
    sock.readyState = 3;
    sock.onclose?.();
    await expect(p).resolves.toMatchObject({ ok: false });
    expect(s.status.value).toBe('offline');
    await expect(s.send('world.move', { direction: 'up' })).resolves.toMatchObject({ ok: false, reason: 'offline' });
  });

  it('kết nối lại giữ revision và không phát lại sự kiện', async () => {
    const { s, w, sock } = await online();
    const batches: Batch[] = [];
    s.onBatch((b) => batches.push(b));
    sock.readyState = 3;
    sock.onclose?.();
    const p = s.connect();
    const sock2 = w.sockets[1]!;
    sock2.open();
    sock2.reply(state(sock2.last().request_id, 9, 3, [ev(1)]));
    await p;
    expect(s.character.value?.x).toBe(3);
    expect(batches.every((b) => b.events.length === 0)).toBe(true);
  });
});
