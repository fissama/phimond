import type { Game } from '../game/controller.ts';
import type { Engine } from '../render/engine.ts';

export interface BenchResult { seconds: number; fps: number; p95Ms: number; worstMs: number; draws: number; triangles: number; textures: number; heapMB: number | null; longTasks: number; tier: string; viewport: string; maps: string[] }

/** Đo thực tế trên thiết bị: đi lại ở thành phố → rừng → trận tự động trong ~40 s rồi trả kết quả (hiện trên màn hình, ghi vào window.__bench). */
export async function runBench(game: Game, engine: Engine, onUpdate: (t: string) => void): Promise<BenchResult> {
  const frames: number[] = []; const maps = new Set<string>();
  const off = engine.onFrame((dt) => { frames.push(dt * 1000); maps.add(game.pres.mapId); });
  const wait = (ms: number) => new Promise((r) => setTimeout(r, ms));
  const until = async (fn: () => boolean, ms: number) => { const t0 = performance.now(); while (!fn() && performance.now() - t0 < ms) await wait(200); };
  onUpdate('Đo hiệu năng… thành phố');
  game.startWalk('right'); await wait(4000); game.stopWalk(); game.startWalk('left'); await wait(3000); game.stopWalk();
  onUpdate('Đo hiệu năng… sang rừng');
  game.approach('portal', 'forest_gate'); await until(() => game.pres.mapId === 'forest', 30000); await wait(2500);
  onUpdate('Đo hiệu năng… trận đấu');
  game.approach('enemy', 'forest:0'); await until(() => !!game.pres.battle, 30000); game.command('auto');
  await until(() => !game.pres.battle, 40000); await wait(1500);
  off();
  const sorted = [...frames].sort((a, b) => a - b); const avg = frames.reduce((s, v) => s + v, 0) / Math.max(1, frames.length);
  const st = engine.stats();
  const r: BenchResult = { seconds: frames.reduce((s, v) => s + v, 0) / 1000, fps: 1000 / avg, p95Ms: sorted[Math.floor(sorted.length * 0.95)] ?? avg, worstMs: sorted[sorted.length - 1] ?? 0, draws: st.draws, triangles: st.triangles, textures: st.textures, heapMB: st.heapMB, longTasks: st.longTasks, tier: st.tier, viewport: `${st.width}×${st.height}@${st.pixelRatio.toFixed(2)}`, maps: [...maps] };
  (window as unknown as { __bench: BenchResult }).__bench = r;
  onUpdate(`Kết quả: ${r.fps.toFixed(0)} fps · p95 ${r.p95Ms.toFixed(1)} ms · tệ nhất ${r.worstMs.toFixed(0)} ms · ${r.draws} bản vẽ · ${r.triangles} tam giác · chất lượng ${r.tier} · ${r.viewport}`);
  return r;
}
