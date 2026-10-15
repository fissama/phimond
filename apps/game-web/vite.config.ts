import { defineConfig } from 'vite';
import preact from '@preact/preset-vite';

export default defineConfig({
  plugins: [preact()],
  base: './',
  resolve: { preserveSymlinks: true },
  build: { target: 'es2022', sourcemap: true },
  server: { host: '127.0.0.1', port: 5173 },
  test: { include: ['tests/unit/**/*.test.ts'], environment: 'node' },
} as Parameters<typeof defineConfig>[0]);
