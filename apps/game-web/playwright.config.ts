import { defineConfig } from '@playwright/test';

// Cần server Go (devserver hoặc server thật) ở 127.0.0.1:8090 với CORS cho origin Vite. Xem README.
const exe = process.env.CHROME;
export default defineConfig({
  testDir: 'tests/e2e',
  timeout: 150_000,
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL: process.env.WEB_URL ?? 'http://127.0.0.1:5173',
    launchOptions: {
      ...(exe ? { executablePath: exe } : {}),
      args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
    },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: process.env.WEB_URL ? undefined : { command: 'npm run dev', url: 'http://127.0.0.1:5173', reuseExistingServer: true, timeout: 60_000 },
});
