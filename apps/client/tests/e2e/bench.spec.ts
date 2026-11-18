import { expect, test, type Page } from '@playwright/test';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

// AD0 — bench vòng map (nợ P01 N08). Chỉ chạy khi PHIMOND_BENCH=1:
//   PHIMOND_BENCH=1 PHIMOND_BENCH_LOOPS=5 PHIMOND_BENCH_QUALITY=low npx playwright test bench --project=chromium
// Mỗi lần tới map mới: chờ tải xong + 1,5 s rồi ghi số đo `window.__phimondBench()` vào JSON (PHIMOND_BENCH_OUT).
// Ý chính: sau nhiều vòng đi lại cùng các map, số texture GPU và bộ nhớ cache phải phẳng (không rò).

test.skip(!process.env.PHIMOND_BENCH, 'bench chỉ chạy khi đặt PHIMOND_BENCH=1');

type Pos = { map: string; x: number; y: number; settled: boolean };
const pos = (p: Page) =>
  p.evaluate(() => {
    const w = (window as unknown as { __phimond: { world: { mover: { mapId: string; cell: { x: number; y: number }; settled: boolean } } } }).__phimond.world;
    return { map: w.mover.mapId, x: w.mover.cell.x, y: w.mover.cell.y, settled: w.mover.settled } as Pos;
  });
const act = (p: Page, a: unknown) => p.evaluate((a) => (window as unknown as { __phimond: { world: { act(a: unknown): void } } }).__phimond.world.act(a), a);

async function register(p: Page): Promise<void> {
  // Máy chạy test không có GPU (SwiftShader): hậu kỳ HD-2D làm khung hình rất thấp nên thời gian đi bộ lệch.
  // Mặc định mức Thấp cho test, trừ khi test tự đặt cài đặt (chỉ ghi khi chưa có).
  await p.addInitScript((quality) => {
    if (!localStorage.getItem('phimond.settings.v1')) localStorage.setItem('phimond.settings.v1', JSON.stringify({ quality, fps: 60, dpad: true, hud: 'full', time: 'day' }));
  }, process.env.PHIMOND_BENCH_QUALITY ?? 'low');
  await p.goto(process.env.PHIMOND_E2E_DIST ? '/?debug&bench=1' : '/?bench=1');
  await p.getByTestId('username').fill(`e2e${Date.now().toString(36)}${Math.floor(Math.random() * 1e4)}`);
  await p.getByTestId('password').fill('matkhau-e2e-12345');
  await p.getByTestId('register').click();
  await p.getByTestId('terms').check();
  await p.getByTestId('register-submit').click();
  await createCharacter(p, 'Tester', 'male');
}

/** Đăng ký xong: màn chọn nhân vật → ô 1 → tạo nhân vật → vào thế giới. */
async function createCharacter(p: Page, name: string, gender: 'male' | 'female', slot = 1): Promise<void> {
  await p.getByTestId(`slot-${slot}`).click({ timeout: 20_000 });
  await p.getByTestId(`gender-${gender}`).click({ timeout: 20_000 });
  await p.getByTestId('char-name').fill(name);
  await p.getByTestId('char-create').click();
  await expect(p.getByTestId('hud-status')).toHaveText('Trực tuyến', { timeout: 20_000 });
  await expect(p.getByTestId('loading')).toHaveCount(0, { timeout: 20_000 });
}

async function chooseStarter(p: Page, index = 1): Promise<void> {
  await act(p, { kind: 'pedestal', index });
  await p.getByTestId('starter-confirm').click({ timeout: 15_000 });
  await expect.poll(async () => (await pos(p)).map, { timeout: 15_000 }).toBe('emerald_forest_main_woods');
}

/** Đi tới ô (hoặc tới khi sang map khác). Gặp quái dọc đường thì chạy trốn rồi đi tiếp. */
async function walk(p: Page, cell: { x: number; y: number }, untilMap?: string): Promise<void> {
  await expect(p.getByTestId('loading')).toHaveCount(0, { timeout: 20_000 });
  await act(p, { kind: 'ground', cell });
  let last = '';
  let still = 0;
  // Dưới tải song song (SwiftShader không GPU) mỗi chặng có thể chậm gấp đôi: cho tới ~60 s mỗi chặng.
  for (let i = 0; i < 300; i++) {
    await p.waitForTimeout(200);
    if (await p.getByTestId('battle').count()) {
      // Cảnh trận tự đóng sau kết quả; chỉ bấm Chạy khi còn trong lượt (nút còn hiện).
      if (await p.getByTestId('act-flee').count()) await p.getByTestId('act-flee').click().catch(() => undefined);
      await expect(p.getByTestId('battle')).toHaveCount(0, { timeout: 15_000 });
      await act(p, { kind: 'ground', cell });
      continue;
    }
    const s = await pos(p);
    if (untilMap ? s.map === untilMap && s.settled : s.x === cell.x && s.y === cell.y && s.settled) return;
    // Đứng yên quá lâu (lệnh bị bỏ khi đang tải map / bị cắt bởi trận): ra lệnh lại.
    const k = JSON.stringify(s);
    still = k === last ? still + 1 : 0;
    last = k;
    if (still >= 5 && s.settled) {
      still = 0;
      await act(p, { kind: 'ground', cell });
    }
  }
  throw new Error(`không tới được ${JSON.stringify(cell)} / ${untilMap}: ${JSON.stringify(await pos(p))}`);
}


type Sample = { loop: number; map: string; t: number } & Record<string, unknown>;

async function sample(p: Page, loop: number, t0: number): Promise<Sample> {
  await expect(p.getByTestId('loading')).toHaveCount(0, { timeout: 30_000 });
  await p.waitForTimeout(1500);
  const b = await p.evaluate(() => (window as unknown as { __phimondBench(): unknown }).__phimondBench());
  // AD1: ảnh/âm thanh/json tải theo tên gốc (chưa băm) = không được cache dài. Bản build phải bằng 0.
  const unhashed = await p.evaluate(() =>
    performance
      .getEntriesByType('resource')
      .map((r) => new URL(r.name).pathname)
      .filter((u) => /\.(png|webp|jpe?g|ogg|mp3|wav|json)$/i.test(u) && !/\.[0-9a-f]{10}\.[a-z0-9]+$/i.test(u) && !u.startsWith('/api')),
  );
  return { loop, map: (await pos(p)).map, t: Math.round((Date.now() - t0) / 1000), unhashed: unhashed.length, unhashedSample: unhashed.slice(0, 5), ...(b as Record<string, unknown>) };
}

test('bench: Bìa Rừng → Rừng Sâu → Hoàng Môn → Quảng Trường, rồi lặp Quảng Trường → Hoàng Môn → Thương Phố → Quảng Trường', async ({ page }) => {
  const loops = Number(process.env.PHIMOND_BENCH_LOOPS ?? 5);
  test.setTimeout(240_000 + loops * 120_000);
  const t0 = Date.now();
  const out: Sample[] = [];
  await register(page);
  out.push(await sample(page, 0, t0));
  // Rừng có quái: đi liền một mạch (đứng chờ đo dễ bị chạm quái), chỉ đo khi tới thành phố.
  await chooseStarter(page);
  await walk(page, { x: 33, y: 6 }, 'emerald_forest_deep_woods');
  await walk(page, { x: 37, y: 5 }, 'city_palace_gate');
  await walk(page, { x: 0, y: 6 }, 'city_square');
  out.push(await sample(page, 0, t0));
  // Vòng thành phố (không có quái nên ổn định): mỗi vòng đi qua 3 map rồi về lại Quảng Trường.
  for (let i = 1; i <= loops; i++) {
    await walk(page, { x: 31, y: 5 }, 'city_palace_gate');
    out.push(await sample(page, i, t0));
    await walk(page, { x: 25, y: 6 }, 'city_market');
    out.push(await sample(page, i, t0));
    await walk(page, { x: 29, y: 6 }, 'city_square');
    out.push(await sample(page, i, t0));
  }
  const file = process.env.PHIMOND_BENCH_OUT ?? 'test-results/bench.json';
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify({ quality: process.env.PHIMOND_BENCH_QUALITY ?? 'low', loops, samples: out }, null, 2));
  console.log(`bench → ${file}`);
  // Không rò: số texture GPU ở Quảng Trường vòng cuối không vượt vòng 1 quá 10% (+3).
  const at = (loop: number) => out.find((s) => s.loop === loop && s.map === 'city_square')!.gpuTextures as number;
  if (process.env.PHIMOND_BENCH_ASSERT) expect(at(loops)).toBeLessThanOrEqual(Math.ceil(at(1) * 1.1) + 3);
});
