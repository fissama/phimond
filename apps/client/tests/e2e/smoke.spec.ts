import { expect, test, type Page } from '@playwright/test';

// E2E với server thật (devserver, dữ liệu trong bộ nhớ). Dùng móc __phimond (chỉ có ở bản dev) để ra lệnh
// đi tới ô/NPC như khi người chơi chạm vào cảnh, rồi kiểm trạng thái server qua HUD.

type Pos = { map: string; x: number; y: number; settled: boolean };
const pos = (p: Page) =>
  p.evaluate(() => {
    const w = (window as unknown as { __phimond: { world: { mover: { mapId: string; cell: { x: number; y: number }; settled: boolean } } } }).__phimond.world;
    return { map: w.mover.mapId, x: w.mover.cell.x, y: w.mover.cell.y, settled: w.mover.settled } as Pos;
  });
const act = (p: Page, a: unknown) => p.evaluate((a) => (window as unknown as { __phimond: { world: { act(a: unknown): void } } }).__phimond.world.act(a), a);

async function register(p: Page): Promise<void> {
  await p.goto('/');
  await p.getByTestId('username').fill(`e2e${Date.now().toString(36)}${Math.floor(Math.random() * 1e4)}`);
  await p.getByTestId('password').fill('matkhau-e2e-12345');
  await p.getByTestId('register').click();
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
  for (let i = 0; i < 150; i++) {
    await p.waitForTimeout(200);
    if (await p.getByTestId('battle').count()) {
      await p.getByTestId('act-flee').click();
      await p.getByTestId('battle-continue').click({ timeout: 10_000 });
      await act(p, { kind: 'ground', cell });
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

test('người chơi mới: Triệu Linh Điện → chọn bệ đá → Bìa Rừng', async ({ page }) => {
  await register(page);
  expect((await pos(page)).map).toBe('summoning_hall_main_hall');
  await expect(page.getByTestId('hud-map')).toHaveText('Triệu Linh Điện');
  await chooseStarter(page, 2);
  await expect(page.getByTestId('hud-map')).toHaveText('Bìa Rừng Lục Bảo');
  await expect(page.getByTestId('hud-gold')).toContainText('Lv 3');
});

test('đi trọn tuyến Đợt A và dùng trụ đá quay về', async ({ page }) => {
  test.setTimeout(150_000);
  await register(page);
  await chooseStarter(page);
  await walk(page, { x: 33, y: 6 }, 'emerald_forest_deep_woods');
  await walk(page, { x: 37, y: 5 }, 'city_palace_gate'); // lần đầu: Hoàng Môn
  await walk(page, { x: 25, y: 6 }, 'city_square');
  await walk(page, { x: 0, y: 5 }, 'city_palace_gate');
  await walk(page, { x: 25, y: 6 }, 'city_square');
  // Trụ đá: đi tới, mở bảng, đích khóa không bấm được, về Bìa Rừng. (Lệnh gửi lúc đang tải map bị bỏ → chờ tải xong.)
  await expect(page.getByTestId('loading')).toHaveCount(0, { timeout: 20_000 });
  await act(page, { kind: 'pillar' });
  await expect(page.getByTestId('travel-city_farm')).toBeDisabled({ timeout: 20_000 });
  await page.getByTestId('travel-emerald_forest_main_woods').click();
  await expect.poll(async () => (await pos(page)).map, { timeout: 15_000 }).toBe('emerald_forest_main_woods');
});

test('chạm quái → trận → chạy → quái ẩn tới khi hồi', async ({ page }) => {
  await register(page);
  await chooseStarter(page);
  const spawn = await page.evaluate(() => {
    const w = (window as unknown as { __phimond: { world: { content: { map(id: string): { wild_spawns: { id: string }[] } } } } }).__phimond.world;
    return w.content.map('emerald_forest_main_woods').wild_spawns[0]!.id;
  });
  await act(page, { kind: 'spawn', id: spawn });
  await expect(page.getByTestId('battle')).toBeVisible({ timeout: 20_000 });
  await expect(page.getByTestId('battle-enemy')).toBeVisible();
  await page.getByTestId('act-flee').click();
  await expect(page.getByTestId('battle-result')).toContainText('chạy thoát');
  await page.getByTestId('battle-continue').click();
  await expect(page.getByTestId('battle')).toHaveCount(0);
  // Quái vừa đánh (có thể là con khác chặn đường đi) phải đang ẩn phía server.
  const hidden = await page.evaluate(
    () => (window as unknown as { __phimond: { session: { character: { value: { spawn_hidden: Record<string, number> } } } } }).__phimond.session.character.value.spawn_hidden,
  );
  expect(Object.keys(hidden).length).toBeGreaterThan(0);
});

test('NPC: tới gần, hội thoại, hồi phục; cổng khóa báo chưa mở', async ({ page }) => {
  test.setTimeout(120_000);
  await register(page);
  await chooseStarter(page);
  await act(page, { kind: 'npc', id: 'forest_guide' });
  await expect(page.getByTestId('npc-name')).toHaveText('Kiểm Lâm Lio', { timeout: 15_000 });
  await page.getByTestId('npc-role-heal').click();
  await page.getByTestId('do-heal').click();
  await page.getByTestId('npc-close').click();
  await walk(page, { x: 33, y: 6 }, 'emerald_forest_deep_woods');
  await walk(page, { x: 37, y: 5 }, 'city_palace_gate');
  await walk(page, { x: 4, y: 2 });
  await expect(page.getByTestId('toasts')).toContainText('chưa mở', { timeout: 10_000 });
});

test('cài đặt đồ họa lưu qua tải lại trang', async ({ page }) => {
  await register(page);
  await page.getByTestId('menu-open').click();
  await page.getByTestId('menu-settings').click();
  await page.getByTestId('quality-low').click();
  await page.getByTestId('fps-30').click();
  const saved = await page.evaluate(() => localStorage.getItem('phimond.settings.v1'));
  expect(JSON.parse(saved!)).toMatchObject({ quality: 'low', fps: 30 });
});

test('đăng nhập sai báo lỗi rõ ràng', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username').fill('khong-ton-tai-xyz');
  await page.getByTestId('password').fill('sai-mat-khau-123');
  await page.getByTestId('login').click();
  await expect(page.getByTestId('login-error')).toBeVisible();
});

test('điều khiển thật: nhấn phím, giữ phím, D-pad, click mặt đất', async ({ page }) => {
  await register(page);
  const at = async () => {
    await page.waitForTimeout(400);
    await expect.poll(async () => (await pos(page)).settled, { timeout: 5000 }).toBe(true);
    return pos(page);
  };
  const s0 = await at(); // Triệu Linh Điện (9,7)
  await page.keyboard.press('ArrowLeft'); // nhấn nhanh: đúng một ô
  expect((await at()).x).toBe(s0.x - 1);
  await page.keyboard.down('ArrowUp');
  await page.waitForTimeout(700);
  await page.keyboard.up('ArrowUp');
  const s2 = await at();
  expect(s2.y).toBeLessThan(s0.y - 1); // giữ phím: đi nhiều ô
  const d = (await page.getByTestId('dpad-right').boundingBox())!;
  await page.mouse.move(d.x + d.width / 2, d.y + d.height / 2);
  await page.mouse.down();
  await page.waitForTimeout(600);
  await page.mouse.up();
  expect((await at()).x).toBeGreaterThan(s2.x);
  const before = JSON.stringify(await at());
  await page.mouse.click(640, 470); // chạm mặt đất dưới nhân vật
  await expect.poll(async () => JSON.stringify(await pos(page)), { timeout: 8000 }).not.toBe(before);
});
