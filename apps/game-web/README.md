# Phimond game web (Three.js)

Client game web thay Godot (ADR-0001). Vite + TypeScript strict + Preact signals + Three.js r170. Server Go giữ nguyên giao thức (xem `packages/protocol/README.md`).

- Kế hoạch: `.ai/plan/phases/P01-world/P01-threejs-migration-plan.md`
- Bảng parity: [PARITY.md](PARITY.md)
- Kiểu + schema giao thức: `packages/protocol-ts`

## Chạy

```sh
cd apps/game-web
npm ci            # trên máy của bạn (node_modules không dùng chung giữa hệ điều hành)
npm run dev       # http://127.0.0.1:5173
```

Cần một server game để đăng nhập. Hai cách:

1. **Server Go thật hoặc devserver** (bộ nhớ, không cần MySQL):

   ```sh
   cd apps/game-server
   GAME_CORS_ORIGINS=http://127.0.0.1:5173,http://localhost:5173 \
   GAME_ALLOWED_ORIGINS=127.0.0.1:5173,localhost:5173 \
   go run ./cmd/devserver            # 127.0.0.1:8090
   ```

   Đổi địa chỉ server bằng `VITE_GAME_API_URL`. Thử trên iPhone cùng Wi-Fi: chạy `npm run dev -- --host 0.0.0.0`, đặt `VITE_GAME_API_URL=http://<ip-máy>:8090`, thêm origin tương ứng vào hai biến CORS ở trên.

2. **Engine Go chạy ngay trong trình duyệt (wasm)** — không cần server, dùng cho bản thử/demo:

   ```sh
   tools/build-wasm-demo.sh          # tạo public/engine/engine.wasm
   npm run dev                       # mở http://127.0.0.1:5173/?local=1
   ```

   Đây là đúng engine và catalog của server (`character.Engine`), chỉ khác kho dữ liệu trong RAM: tắt trang là mất tài khoản.

Tham số URL: `?q=low|medium|high` (chất lượng đồ họa, mặc định tự chọn + tự hạ khi chậm), `?bench=1` (đo hiệu năng thực tế ~40 s rồi hiện kết quả, đọc thêm ở `window.__bench`), `?local=1` (wasm). F3 hoặc Cài đặt → "Hiện thống kê hiệu năng" bật lớp số liệu.

## Kiểm tra

```sh
npm run typecheck && npm test            # unit + controller với server thật (SKIP_LIVE=1 để bỏ qua)
CHROME=/đường/dẫn/chrome npm run test:e2e # Playwright: luồng chơi, menu, bố cục nhiều màn hình, axe, ngân sách hiệu năng
npm run build                            # dist/ (base tương đối, đặt được ở thư mục con)
```

Hiệu năng trên sandbox dùng SwiftShader nên chỉ đo "proxy" (bản vẽ, tam giác, texture, heap, long task); FPS thật phải đo trên thiết bị bằng `?bench=1`.

## HUD / menu (sprite APK 3.2)
HUD và mọi menu dùng sprite gốc trích từ APK (`public/assets/ui/*`, nguồn + SHA trong `hud.json`), bố cục theo canvas 960×640 của bản tham chiếu Godot (`classic_hud.gd`, `reference_menus.gd`): dải điều khiển dưới 186/640 (dpad · chat · Chọn/Trở về), khung `panel_menu` 9-slice (34/34/34/112) nền #073054, hàng/tab/slot/thanh HP-MP-XP từ sprite. Hệ số `--k` = cao/640 (0.72–1.6), `--t` (≥0.98) cho vùng chạm. Phần “hiện đại hơn”: hiệu ứng nhấn/mở menu, glow, safe-area, chữ có viền, thanh chạy mượt, màn Cường hóa có thước 0–10 lần.
