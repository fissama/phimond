import { expect, test } from '@playwright/test';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

// AD3 — ghi lại ảnh hd2d mà mỗi map dùng, để bản build gói atlas theo map (`atlas-groups.json`).
// Chỉ chạy khi PHIMOND_ATLAS_USAGE=1 (cần Vite dev, vì phải import thẳng module `src/render/assets.ts`):
//   PHIMOND_ATLAS_USAGE=1 npx playwright test atlas-usage --project=chromium
// Chạy lại khi thêm/đổi prop của map (bảng MAP_PROPS/MAP_EXTRAS/MAP_DECALS trong render/scene.ts, NPC, map mới).
// Ảnh không có trong file này vẫn chạy được (tải lẻ), chỉ là không được gói.

test.skip(!process.env.PHIMOND_ATLAS_USAGE, 'chỉ chạy khi PHIMOND_ATLAS_USAGE=1');

test('ghi ảnh hd2d theo map và preset', async ({ page }) => {
  test.setTimeout(600_000);
  await page.addInitScript(() => {
    localStorage.setItem('phimond.settings.v1', JSON.stringify({ quality: 'high', fps: 60, dpad: true, hud: 'full', time: 'day' }));
  });
  await page.goto('/');
  await page.getByTestId('username').fill(`atl${Date.now().toString(36)}`);
  await page.getByTestId('password').fill('matkhau-e2e-12345');
  await page.getByTestId('register').click();
  await page.getByTestId('terms').check();
  await page.getByTestId('register-submit').click();
  await page.getByTestId('slot-1').click({ timeout: 20_000 });
  await page.getByTestId('gender-male').click({ timeout: 20_000 });
  await page.getByTestId('char-name').fill('Atlas');
  await page.getByTestId('char-create').click();
  await expect(page.getByTestId('loading')).toHaveCount(0, { timeout: 30_000 });
  await expect.poll(() => page.evaluate(() => !!(window as unknown as { __phimond?: unknown }).__phimond), { timeout: 30_000 }).toBe(true);

  const usage = await page.evaluate(async () => {
    type W = {
      world: {
        engine: { loadMap(m: unknown, n: unknown, p: string): Promise<void>; setQuality(q: string): void };
        content: { cat: { maps: Record<string, { id: string }> }; npcsOn(id: string): unknown };
        playerAsset: string;
      };
    };
    const { world } = (window as unknown as { __phimond: W }).__phimond;
    // Đường dẫn module giống hệt đường app dùng → cùng một instance `textures`.
    const path = '/src/render/assets.ts';
    const mod = (await import(/* @vite-ignore */ path)) as { textures: { get(u: string, o?: { repeat?: boolean }): Promise<unknown> } };
    const seen = new Set<string>();
    const orig = mod.textures.get.bind(mod.textures);
    mod.textures.get = (u: string, o?: { repeat?: boolean }) => {
      const m = /\/hd2d\/([^/?#]+)\.png$/.exec(u);
      if (m && !o?.repeat) seen.add(m[1]!);
      return orig(u, o);
    };
    const maps = Object.values(world.content.cat.maps);
    // Ghi theo từng preset: preset thấp dựng ít đồ trang trí hơn, nên atlas tách ảnh "chỉ preset cao mới dùng" ra trang riêng.
    const out: Record<string, Record<string, string[]>> = {};
    for (const q of ['low', 'medium', 'high']) {
      world.engine.setQuality(q);
      for (const map of maps) {
        seen.clear();
        await world.engine.loadMap(map, world.content.npcsOn(map.id), world.playerAsset);
        (out[map.id] ??= {})[q] = [...seen].sort();
      }
    }
    mod.textures.get = orig;
    return out;
  });
  expect(Object.keys(usage).length).toBeGreaterThanOrEqual(11);
  const file = fileURLToPath(new URL('../../atlas-groups.json', import.meta.url));
  writeFileSync(file, JSON.stringify({ note: 'Sinh bởi tests/e2e/atlas-usage.spec.ts — ảnh hd2d (không lặp) mỗi map dùng theo preset', maps: usage }, null, 1) + '\n');
  console.log(`atlas-groups → ${file}: ${Object.entries(usage).map(([k, v]) => `${k}:${v.low!.length}/${v.medium!.length}/${v.high!.length}`).join(' ')}`);
});
