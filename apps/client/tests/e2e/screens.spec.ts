import { expect, test } from '@playwright/test';
import { mkdirSync } from 'node:fs';

// AD3/AD4 — chụp 11 map ở cùng vị trí camera để so trước/sau (atlas, WebP). Chỉ chạy khi PHIMOND_SCREENS=<thư mục>:
//   npm run build && PHIMOND_E2E_DIST=1 PHIMOND_SCREENS=/tmp/screens-new npx playwright test screens --project=chromium
// So bằng mắt hoặc công cụ so ảnh; hiệu ứng động (lá, đom đóm, nước) làm lệch vài pixel giữa hai lần chụp.

test.skip(!process.env.PHIMOND_SCREENS, 'chỉ chạy khi PHIMOND_SCREENS=<thư mục>');

test('chụp 11 map', async ({ page }) => {
  test.setTimeout(300_000);
  const dir = process.env.PHIMOND_SCREENS!;
  mkdirSync(dir, { recursive: true });
  const quality = process.env.PHIMOND_SCREENS_QUALITY ?? 'medium';
  await page.setViewportSize({ width: 1280, height: 720 });
  await page.addInitScript((q) => {
    localStorage.setItem('phimond.settings.v1', JSON.stringify({ quality: q, fps: 60, dpad: false, hud: 'full', time: 'day' }));
    Math.random = (() => {
      let s = 42;
      return () => ((s = (s * 16807) % 2147483647) - 1) / 2147483646;
    })();
  }, quality);
  await page.goto(process.env.PHIMOND_E2E_DIST ? '/?debug' : '/');
  await page.getByTestId('username').fill(`scr${Date.now().toString(36)}`);
  await page.getByTestId('password').fill('matkhau-e2e-12345');
  await page.getByTestId('register').click();
  await page.getByTestId('terms').check();
  await page.getByTestId('register-submit').click();
  await page.getByTestId('slot-1').click({ timeout: 20_000 });
  await page.getByTestId('gender-male').click({ timeout: 20_000 });
  await page.getByTestId('char-name').fill('Screens');
  await page.getByTestId('char-create').click();
  await expect(page.getByTestId('loading')).toHaveCount(0, { timeout: 30_000 });
  await expect.poll(() => page.evaluate(() => !!(window as unknown as { __phimond?: unknown }).__phimond), { timeout: 30_000 }).toBe(true);
  const ids = await page.evaluate(() => Object.keys((window as unknown as { __phimond: { world: { content: { cat: { maps: object } } } } }).__phimond.world.content.cat.maps).sort());
  for (const id of ids) {
    await page.evaluate(async (mapId) => {
      type E = { loadMap(m: unknown, n: unknown, p: string): Promise<void>; placePlayer(p: { x: number; y: number }): void; setPlayer(p: { x: number; y: number }, m: boolean, f: string): void; snapCamera(): void };
      const w = (window as unknown as { __phimond: { world: { engine: E; content: { cat: { maps: Record<string, { id: string; width: number; height?: number }> }; npcsOn(id: string): unknown }; playerAsset: string } } }).__phimond.world;
      const map = w.content.cat.maps[mapId]!;
      await w.engine.loadMap(map, w.content.npcsOn(map.id), w.playerAsset);
      const pos = { x: map.width / 2, y: (map.height || map.width) / 2 };
      w.engine.placePlayer(pos);
      w.engine.setPlayer(pos, false, 'down');
      w.engine.snapCamera();
    }, id);
    await page.waitForTimeout(1500);
    await page.locator('canvas').first().screenshot({ path: `${dir}/${id}.png` });
  }
});
