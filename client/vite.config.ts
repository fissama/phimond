import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 3000,
    strictPort: false,
    proxy: {
      // Browser → ws://localhost:3000/ws → Vite → ws://localhost:3001 (Node proxy) → Godot TCP :8080.
      // The Node proxy is needed because Godot 4.7.2's WebSocketServer has a
      // Chromium handshake incompatibility.
      '/ws': {
        target: 'ws://localhost:3001',
        ws: true,
        rewriteWsOrigin: false,
      },
    },
  },
  build: {
    target: 'es2022',
    sourcemap: true,
  },
})
