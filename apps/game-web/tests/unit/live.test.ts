// Test trực tiếp với server Go thật (devserver trong bộ nhớ). Bỏ qua nếu chưa chạy server.
import { describe, expect, it, beforeAll } from 'vitest';
import { BrowserTransport } from '../../src/net/transport.ts';
import { Session } from '../../src/net/session.ts';

const API = process.env.GAME_API_URL ?? 'http://127.0.0.1:8090';
let up = false;
beforeAll(async () => {
  try {
    up = (await fetch(`${API}/healthz`)).ok;
  } catch {
    up = false;
  }
});

const rand = () => Math.random().toString(36).slice(2, 10);

describe.skipIf(process.env.SKIP_LIVE === '1')('session với server thật', () => {
  it('đăng ký, tải catalog, kết nối WS, đi một bước, nhận revision tăng', async () => {
    if (!up) return expect.soft(up, 'server không chạy, bỏ qua').toBe(false);
    const s = new Session(new BrowserTransport(API));
    await s.authenticate('register', `t_${rand()}`, `Pw-${rand()}-xyz`);
    const cat = await s.loadContent();
    expect(Object.keys(cat.maps)).toContain('severa');
    await s.connect();
    expect(s.status.value).toBe('online');
    const first = s.character.value!;
    expect(first.map_id).toBe('severa');
    const r = await s.send('world.move', { direction: 'right' });
    expect(r.ok).toBe(true);
    if (r.ok) {
      expect(r.batch.revision).toBeGreaterThan(s.revision - 1);
      expect(r.batch.character.x).toBe(first.x + 1);
    }
    expect(s.busy.value).toBe(false);
    await s.logout();
  });

  it('từ chối intent thứ hai khi đang chờ và dịch lỗi sang tiếng Việt', async () => {
    if (!up) return;
    const s = new Session(new BrowserTransport(API));
    await s.authenticate('register', `t_${rand()}`, `Pw-${rand()}-xyz`);
    await s.connect();
    const a = s.send('world.move', { direction: 'right' });
    const b = await s.send('world.move', { direction: 'right' });
    expect(b).toEqual({ ok: false, message: 'busy' });
    await a;
    const bad = await s.send('npc.interact', { npc_id: 'trainer' });
    // Trainer ở x=6 trên severa; người chơi bắt đầu x=6 (+1 sau bước đi) nên vẫn đủ gần.
    expect(bad.ok).toBe(true);
    const far = await s.send('shop.buy', { item_id: 'potion', quantity: 99 });
    expect(far.ok).toBe(false);
    if (!far.ok) expect(far.message).toBe('Không đủ vàng.');
    s.disconnect();
  });

  it('đăng nhập sai trả thông điệp thân thiện', async () => {
    if (!up) return;
    const s = new Session(new BrowserTransport(API));
    await expect(s.authenticate('login', 'khong_ton_tai', 'sai-mat-khau-12345')).rejects.toThrow('Tên đăng nhập hoặc mật khẩu không đúng.');
  });

  it('nối lại không phát lại sự kiện cũ', async () => {
    if (!up) return;
    const s = new Session(new BrowserTransport(API));
    await s.authenticate('register', `t_${rand()}`, `Pw-${rand()}-xyz`);
    await s.connect();
    await s.send('npc.interact', { npc_id: 'trainer' });
    const seen: number[] = [];
    s.onBatch((b) => seen.push(b.events.length));
    await s.connect();
    expect(seen[0]).toBe(0);
  });
});
