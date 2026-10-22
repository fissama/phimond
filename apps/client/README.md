# apps/client — client Phimond v1 (P01)

Client web mới viết từ đầu cho v1.0.0: Three.js 0.170 + Vite 7 + TypeScript strict + Preact/signals.
Server Go (`apps/game-server`) là nguồn luật chơi; client chỉ hiển thị và gửi intent.
Kế hoạch: [`.ai/plan/phases/P01-world/P01-implement-plan.md`](../../.ai/plan/phases/P01-world/P01-implement-plan.md).
`apps/game-web` chỉ là bản thử Three.js để tham khảo hành vi, không import code từ đó.

## Chạy dev

Cần Node 22+ và Go 1.25.

```sh
# 1. Server. Chọn một:
#    a) server thật với MySQL dev: xem AGENTS.md (cổng 8090)
#    b) server luật thật, dữ liệu trong bộ nhớ (không cần DB, mất dữ liệu khi tắt):
cd apps/game-server && GAME_ADDR=127.0.0.1:8090 GAME_DATA_DIR=../../data go run ./cmd/devserver

# 2. Client (terminal khác)
cd apps/client
npm install
npm run dev            # http://127.0.0.1:5180
```

Vite chuyển `/api`, `/healthz`, `/ws` sang server (mặc định `http://127.0.0.1:8090`, đổi bằng `GAME_SERVER=http://host:port npm run dev`). Trình duyệt luôn gọi cùng origin nên không cần cấu hình CORS.

Mở trên iPhone cùng mạng Wi-Fi: `npx vite --host 0.0.0.0`, rồi vào `http://<IP máy Mac>:5180`.

Bản build gọi server qua `VITE_GAME_API_URL` (bỏ trống = cùng origin).

## Kiểm tra

```sh
npm run typecheck      # tsc strict
npm test               # vitest: unit test (tests/unit)
npm run build          # build production vào dist/
npm run check          # cả ba lệnh trên

# E2E: Playwright tự bật devserver (cổng 8098) + Vite (5188), không đụng server đang mở tay.
npx playwright install chromium webkit      # lần đầu
npm run e2e                                  # chromium + webkit + iPhone giả lập
npm run e2e -- --project=chromium            # một trình duyệt
PHIMOND_DEVSERVER_BIN=/đường/dẫn/devserver npm run e2e   # dùng binary devserver build sẵn
```

## Cấu trúc

| Thư mục | Vai trò |
|---|---|
| `src/net` | Phiên WebSocket: xác thực khung đầu, request_id, nhiều intent chờ cùng lúc (pipeline di chuyển), khử lặp theo revision, quá hạn → đóng kết nối, không tự gửi lại |
| `src/state` | Trạng thái dùng chung (signals) |
| `src/world` | Hệ tọa độ chung (ADR-P01-01), lưới đi, tìm đường, dự đoán vị trí |
| `src/render` | Renderer Three.js, camera, cảnh, sprite, cache tài nguyên, giới hạn FPS |
| `src/input` | Bàn phím, D-pad, chạm/click-to-move |
| `src/ui` | HUD, menu, cài đặt, hội thoại, trận đấu |
| `src/bench` | Chế độ đo hiệu năng `?bench=` (S6) |
| `tests/unit`, `tests/e2e` | vitest, Playwright |

## Trạng thái

- **S0 (xong):** khung dự án, đăng nhập/đăng ký, kết nối WS, đi từng ô bằng phím trên lưới tạm, unit test phiên, e2e đăng ký → đi → đăng xuất.
- Tiếp theo: S1 (server world 2D, 5 map Đợt A).
