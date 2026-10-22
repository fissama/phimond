import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

// Dev: Vite chuyển /api và /ws sang server Go (mặc định 127.0.0.1:8090) nên trình duyệt gọi cùng origin, không cần cấu hình CORS.
const target = process.env.GAME_SERVER ?? 'http://127.0.0.1:8090';

export default defineConfig({
  plugins: [preact()],
  base: './',
  resolve: { preserveSymlinks: true },
  build: { target: 'es2022', sourcemap: true, outDir: 'dist' },
  server: {
    host: '127.0.0.1',
    port: 5180,
    strictPort: true,
    proxy: {
      '/api': { target, changeOrigin: false },
      '/healthz': { target, changeOrigin: false },
      '/ws': { target: target.replace(/^http/, 'ws'), ws: true },
    },
  },
  test: { include: ['tests/unit/**/*.test.ts'], environment: 'node' },
} as Parameters<typeof defineConfig>[0]);
