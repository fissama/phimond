// Luật điều khiển phía client (port từ reference_game.gd) chạy với server Go thật. Bỏ qua nếu server chưa chạy.
import { beforeAll, describe, expect, it } from 'vitest';
import { Game } from '../../src/game/controller.ts';
import { Session } from '../../src/net/session.ts';
import { BrowserTransport } from '../../src/net/transport.ts';

const API = process.env.GAME_API_URL ?? 'http://127.0.0.1:8090';
let up = false;
beforeAll(async () => { try { up = (await fetch(`${API}/healthz`)).ok; } catch { up = false; } });
const rand = () => Math.random().toString(36).slice(2, 10);
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function newGame(): Promise<Game> {
  const g = new Game(new Session(new BrowserTransport(API)));
  const err = await g.signIn('register', `t_${rand()}`, `Pw-${rand()}-xyz`);
  expect(err).toBe('');
  return g;
}
/** Chạy vòng lặp ảo: dt cố định, chờ mạng thật giữa các khung. */
async function run(g: Game, seconds: number, until?: () => boolean, dt = 1 / 30): Promise<number> {
  let t = 0;
  while (t < seconds) {
    g.pres.update(dt); g.update(dt); t += dt;
    await sleep(3);
    if (until?.()) break;
  }
  return t;
}

describe.skipIf(process.env.SKIP_LIVE === '1')('Game (controller) với server thật', () => {
  it('đi liên tục đúng nhịp 0,18 s/bước và dừng khi thả phím', async () => {
    if (!up) return;
    const g = await newGame(); const x0 = g.character.value!.x;
    g.startWalk('right');
    const t = await run(g, 1.8);
    g.stopWalk('right');
    const steps = g.character.value!.x - x0;
    expect(steps).toBeGreaterThanOrEqual(4);
    expect(steps).toBeLessThanOrEqual(Math.ceil(t / 0.18) + 1);
    const x1 = g.character.value!.x; await run(g, 0.8);
    expect(g.character.value!.x).toBe(x1);
    await g.signOut();
  }, 20000);

  it('approach cổng: tự đi tới rồi chuyển map', async () => {
    if (!up) return;
    const g = await newGame();
    g.approach('portal', 'forest_gate');
    await run(g, 25, () => g.character.value?.map_id === 'forest');
    expect(g.character.value!.map_id).toBe('forest');
    expect(g.destination).toBeNull();
    g.session.disconnect();
  }, 40000);

  it('contact quái hoang vào trận một lần; thắng xong đứng yên không bị vào trận lại (latch)', async () => {
    if (!up) return;
    const g = await newGame();
    g.approach('portal', 'forest_gate');
    await run(g, 25, () => g.character.value?.map_id === 'forest');
    g.approach('enemy', 'forest:0');
    await run(g, 25, () => !!g.character.value?.battle);
    expect(g.character.value!.battle).toBeTruthy();
    const battleId = g.character.value!.battle!.id;
    g.command('auto');
    expect(g.automatic.value).toBe(true);
    await run(g, 90, () => !g.character.value?.battle && !g.pres.battle);
    expect(g.character.value!.battle).toBeFalsy();
    expect(g.automatic.value).toBe(false);
    await run(g, 3); // vẫn đang chạm quái nhưng latch giữ nguyên
    expect(g.character.value!.battle).toBeFalsy();
    expect(battleId).toBeTruthy();
    g.session.disconnect();
  }, 160000);

  it('Trở về: đóng trang → mở/đóng lối tắt; thông điệp "Không…" hủy đường đi', async () => {
    if (!up) return;
    const g = await newGame();
    g.open('Companions'); expect(g.page.value).toBe('Companions');
    g.command('back'); expect(g.page.value).toBe('World');
    g.command('back'); expect(g.shortcuts.value).toBe(true);
    g.command('back'); expect(g.shortcuts.value).toBe(false);
    g.destination = { kind: 'portal', id: 'forest_gate', x: 43, y: 12 }; g.held = 'left';
    g.message('Không đủ vàng.');
    expect(g.destination).toBeNull(); expect(g.held).toBe('');
    g.session.disconnect();
  }, 20000);

  it('mất kết nối xóa giữ phím / đích / tự động', async () => {
    if (!up) return;
    const g = await newGame();
    g.held = 'right'; g.automatic.value = true; g.destination = { kind: 'npc', id: 'trainer', x: 6, y: 12 };
    g.session.disconnect();
    expect(g.held).toBe(''); expect(g.automatic.value).toBe(false); expect(g.destination).toBeNull();
  }, 20000);
});
