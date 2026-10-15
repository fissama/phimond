// E2E trên game thật (Vite + server Go). Cổng chấp nhận của client web: đi/đổi map/chạm quái/trận/menu/layout/a11y.
import { expect, test, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

type G = { game: any; engine: any; stage: any; state: () => any }; // eslint-disable-line @typescript-eslint/no-explicit-any
const g = <T>(p: Page, fn: string): Promise<T> => p.evaluate(`(()=>{const w=window.__game;const game=w.game,stage=w.stage,engine=w.engine;return ${fn}})()`) as Promise<T>;
const rand = () => Math.random().toString(36).slice(2, 9);

async function enter(p: Page, quality = 'low'): Promise<void> {
  await p.goto(`/?q=${quality}`);
  const name = 'e' + rand();
  await p.fill('input[type=text]', name); await p.fill('input[type=password]', `Pw-${name}-123456`);
  await p.click('button:has-text("Đăng ký")');
  await p.waitForFunction('window.__game && window.__game.state().map', null, { timeout: 30000 });
  await p.waitForTimeout(1500);
}
async function waitFor(p: Page, expr: string, ms = 60000): Promise<void> { await p.waitForFunction(`(()=>{const w=window.__game;const game=w.game;return ${expr}})()`, null, { timeout: ms, polling: 250 }); }

test.describe('client web', () => {
  test('đăng nhập sai báo lỗi thân thiện, đăng ký vào được thế giới', async ({ page }) => {
    await page.goto('/?q=low');
    await page.fill('input[type=text]', 'khong_ton_tai'); await page.fill('input[type=password]', 'sai-mat-khau-12345');
    await page.click('button[type=submit]');
    await expect(page.getByRole('alert')).toContainText('không đúng');
    await enter(page);
    expect((await g<string>(page, 'game.pres.mapId'))).toBe('severa');
  });

  test('đi bằng phím và D-pad; thả phím thì dừng', async ({ page }) => {
    await enter(page);
    const x0 = await g<number>(page, 'game.pres.character.x');
    await page.keyboard.down('ArrowRight'); await page.waitForTimeout(1500); await page.keyboard.up('ArrowRight');
    await page.waitForTimeout(600);
    const x1 = await g<number>(page, 'game.pres.character.x');
    expect(x1).toBeGreaterThan(x0 + 1);
    await page.waitForTimeout(700);
    expect(await g<number>(page, 'game.pres.character.x')).toBe(x1);
    const pad = page.getByLabel('Phải'); const box = (await pad.boundingBox())!;
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2); await page.mouse.down(); await page.waitForTimeout(900); await page.mouse.up();
    expect(await g<number>(page, 'game.pres.character.x')).toBeGreaterThan(x1);
  });

  test('thủy tinh dịch chuyển ở Quảng Trường liệt kê vùng đủ cấp', async ({ page }) => {
    await enter(page);
    await g(page, "game.open('Teleport')");
    await expect(page.locator('button.tp')).toHaveCount(3);
  });

  test('tuyến thành → rừng → thành → nông trại; trạng thái server khớp', async ({ page }) => {
    await enter(page);
    for (const [portal, map] of [['forest_gate', 'forest'], ['city_gate', 'severa'], ['ranch_gate', 'ranch']] as const) {
      await g(page, `game.approach('portal','${portal}')`);
      await waitFor(page, `game.pres.mapId==='${map}' && !game.destination`);
    }
    expect(await g<string>(page, 'game.character.value.map_id')).toBe('ranch');
  });

  test('chạm quái → trận → tự động → thắng; không vào lại ngay (latch)', async ({ page }) => {
    test.setTimeout(300_000);
    await enter(page);
    await g(page, "game.approach('portal','forest_gate')"); await waitFor(page, "game.pres.mapId==='forest'");
    await g(page, "game.approach('enemy','forest:0')"); await waitFor(page, '!!game.pres.battle');
    await expect(page.locator('.battlebar')).toBeVisible();
    await g(page, "game.command('auto')");
    await waitFor(page, '!game.pres.battle && !game.character.value.battle', 120000);
    await page.waitForTimeout(3000);
    expect(await g<boolean>(page, '!!game.character.value.battle')).toBe(false);
  });

  test('menu: lối tắt, linh thú, túi đồ, nhiệm vụ, nông trại, cửa hàng đều mở được và Esc đóng', async ({ page }) => {
    await enter(page);
    await page.getByRole('button', { name: 'Menu', exact: true }).click();
    await expect(page.getByRole('dialog', { name: 'Lối tắt' })).toBeVisible();
    for (const [label, title] of [['Linh thú', 'Linh thú'], ['Túi đồ', 'Túi đồ'], ['Nhiệm vụ', 'Nhiệm vụ'], ['Nông trại', 'Nông trại'], ['Cửa hàng', 'Cửa hàng'], ['Hành trình', 'Hành trình'], ['Cài đặt', 'Cài đặt']] as [string, string][]) {
      if (!(await page.getByRole('dialog', { name: 'Lối tắt' }).isVisible())) await g(page, "game.open('Menu')");
      await page.getByRole('dialog', { name: 'Lối tắt' }).getByText(label, { exact: true }).click();
      await expect(page.getByRole('dialog', { name: title })).toBeVisible();
      await page.keyboard.press('Escape');
      await expect(page.getByRole('dialog', { name: title })).toBeHidden();
    }
  });

  test('NPC: chạm người hướng dẫn mở hội thoại, nhận nhiệm vụ', async ({ page }) => {
    await enter(page);
    await g(page, "game.approach('npc','trainer')"); await waitFor(page, "game.page.value==='NPC'");
    await expect(page.getByRole('dialog', { name: 'Trainer Elin' })).toBeVisible();
    await page.getByRole('button', { name: 'Nhiệm vụ' }).last().click();
    await expect(page.getByRole('dialog', { name: 'Nhiệm vụ' })).toBeVisible();
    await page.getByText('Learn from the wild').click(); await page.getByRole('button', { name: 'Nhận', exact: true }).click();
    await waitFor(page, "!!game.character.value.quests['field_training']");
  });


  test('dịch vụ NPC: mua đồ, hồi phục, học kỹ năng đều đi qua server và cập nhật giao diện', async ({ page }) => {
    await enter(page);
    await g(page, "game.approach('npc','trainer')"); await waitFor(page, "game.page.value==='NPC'");
    await page.getByRole('button', { name: 'Cửa hàng' }).click();
    const gold0 = await g<number>(page, 'game.character.value.gold');
    await page.getByRole('button', { name: /Mua 1/ }).first().click();
    await waitFor(page, `game.character.value.gold < ${gold0}`);
    await g(page, "game.open('NPC')"); await page.getByRole('button', { name: 'Hồi phục linh thú' }).click();
    await waitFor(page, "game.chat.value.some(m=>m.text.includes('hồi phục'))");
    await page.getByRole('button', { name: 'Học kỹ năng' }).click();
    const n0 = await g<number>(page, 'game.pets()[0].skills.length');
    await page.getByRole('button', { name: 'Học', exact: true }).first().click();
    await waitFor(page, `game.pets()[0].skills.length === ${n0 + 1}`);
  });

  test('mất kết nối hiện banner và nút Kết nối lại khôi phục phiên', async ({ page }) => {
    await enter(page);
    await g(page, 'game.session.disconnect()');
    await expect(page.locator('.conn')).toBeVisible();
    await page.getByRole('button', { name: 'Kết nối lại' }).click();
    await waitFor(page, "game.session.status.value==='online'");
    await expect(page.locator('.conn')).toBeHidden();
    expect(await g<string>(page, 'game.character.value.map_id')).toBe('severa');
  });

  test('chat có đủ 6 tab; tab chưa có máy chủ hiện trạng thái rỗng', async ({ page }) => {
    await enter(page);
    const tabs = page.getByRole('tab'); await expect(tabs).toHaveCount(6);
    await page.getByRole('tab', { name: 'Đội' }).click(); await expect(page.locator('.log .empty')).toBeVisible();
  });

  for (const [name, w, h, mobile] of [['iphone-ngang', 932, 430, true], ['iphone-nhỏ', 667, 375, true], ['ipad', 1024, 768, true], ['desktop', 1440, 900, false]] as const) {
    test(`bố cục ${name}: không tràn khung, mục chạm ≥ 32px, không lỗi a11y nghiêm trọng`, async ({ browser }) => {
      const ctx = await browser.newContext({ viewport: { width: w, height: h }, hasTouch: mobile, isMobile: mobile });
      const page = await ctx.newPage(); await enter(page);
      const bad = await page.evaluate(() => {
        const out: string[] = [];
        for (const el of document.querySelectorAll('#hud button, #hud [role=tab]')) {
          const r = el.getBoundingClientRect(); if (!r.width) continue;
          if (r.right > innerWidth + 1 || r.bottom > innerHeight + 1 || r.left < -1 || r.top < -1) out.push('off:' + (el.getAttribute('aria-label') ?? el.textContent));
          if (r.width < 32 || r.height < 32) out.push('small:' + (el.getAttribute('aria-label') ?? el.textContent));
        }
        return out;
      });
      expect(bad).toEqual([]);
      const axe = await new AxeBuilder({ page }).include('#hud').disableRules(['color-contrast']).analyze();
      expect(axe.violations.filter((v) => v.impact === 'critical' || v.impact === 'serious').map((v) => v.id)).toEqual([]);
      await ctx.close();
    });
  }

  test('đo hiệu năng (proxy): số bản vẽ/tam giác nằm trong ngân sách', async ({ page }) => {
    await enter(page, 'high');
    const s = await g<any>(page, 'engine.stats()'); // eslint-disable-line @typescript-eslint/no-explicit-any
    expect(s.draws).toBeLessThan(120); expect(s.triangles).toBeLessThan(5000); expect(s.textures).toBeLessThan(120);
    if (s.heapMB) expect(s.heapMB).toBeLessThan(200);
  });
});
