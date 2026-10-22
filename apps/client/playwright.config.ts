import { defineConfig, devices } from '@playwright/test';

// E2E chạy với server game thật nhưng kho dữ liệu trong bộ nhớ (cmd/devserver) để không đụng DB dev.
// Cổng riêng (8098/5188) để không đụng server/Vite đang mở tay.
const SERVER_PORT = 8098;
const WEB_PORT = 5188;
// PHIMOND_DEVSERVER_BIN: dùng binary devserver đã build sẵn thay cho `go run` (môi trường không tải được toolchain Go).
const DEVSERVER = process.env.PHIMOND_DEVSERVER_BIN ?? 'go run ./cmd/devserver';

export default defineConfig({
  testDir: 'tests/e2e',
  timeout: 60_000,
  retries: 0,
  reporter: [['list']],
  use: { baseURL: `http://127.0.0.1:${WEB_PORT}`, trace: 'retain-on-failure' },
  // webkit/iphone cần `npx playwright install webkit` trên máy dev.
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'iphone', use: { ...devices['iPhone 15 Pro Max'] } },
  ],
  webServer: [
    {
      command: DEVSERVER,
      cwd: '../game-server',
      env: { GAME_ADDR: `127.0.0.1:${SERVER_PORT}`, GAME_DATA_DIR: '../../data' },
      url: `http://127.0.0.1:${SERVER_PORT}/healthz`,
      timeout: 120_000,
      reuseExistingServer: false,
    },
    {
      command: `npx vite --port ${WEB_PORT}`,
      env: { GAME_SERVER: `http://127.0.0.1:${SERVER_PORT}` },
      url: `http://127.0.0.1:${WEB_PORT}`,
      timeout: 60_000,
      reuseExistingServer: false,
    },
  ],
});
