import { expect, test } from '@playwright/test';

// S0: đăng ký → vào world → đi một bước → server xác nhận → đăng xuất.
test('đăng ký, vào world, đi một bước được server xác nhận', async ({ page }) => {
  const user = `e2e${Date.now().toString(36)}${Math.floor(Math.random() * 1e4)}`;
  await page.goto('/');
  await page.getByTestId('username').fill(user);
  await page.getByTestId('password').fill('matkhau-e2e-1');
  await page.getByTestId('register').click();
  await expect(page.getByTestId('hud-status')).toHaveText('Trực tuyến', { timeout: 15_000 });
  await expect(page.locator('[data-testid="world-canvas"]')).toBeVisible();

  const pos = page.getByTestId('hud-pos');
  const before = await pos.textContent();
  const x0 = Number(/x (\d+)/.exec(before ?? '')?.[1]);
  await page.keyboard.press('ArrowRight');
  await expect(pos).toHaveText(new RegExp(`x ${x0 + 1} `));

  await page.getByTestId('logout').click();
  await expect(page.getByTestId('username')).toBeVisible();
});

test('đăng nhập sai báo lỗi rõ ràng', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('username').fill('khong-ton-tai-xyz');
  await page.getByTestId('password').fill('sai');
  await page.getByTestId('login').click();
  await expect(page.getByTestId('login-error')).toBeVisible();
});
