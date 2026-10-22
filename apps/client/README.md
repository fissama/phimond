# apps/client — client Phimond v1 (P01 v1.0.0)

Client web mới viết từ đầu cho v1.0.0: Three.js 0.170 + Vite 7 + TypeScript strict + Preact/signals.
Server Go (`apps/game-server`) là nguồn luật chơi; client chỉ hiển thị và gửi intent.
Kế hoạch: [`P01-implement-plan.md`](../../.ai/plan/phases/P01-world/P01-implement-plan.md) · tọa độ/map: [ADR-P01-01](../../.ai/plan/phases/P01-world/adr/ADR-P01-01-map-format.md).
`apps/game-web` chỉ là bản thử Three.js để tham khảo hành vi, không import code từ đó.

## Chạy để thử tay (manual test)

Cần Node 22+ và Go 1.25.

```sh
# 1) Server — chọn một:
#   a) Không cần DB (dữ liệu trong bộ nhớ, mất khi tắt) — nhanh nhất để thử:
cd apps/game-server && GAME_ADDR=127.0.0.1:8090 GAME_DATA_DIR=../../data go run ./cmd/devserver
#   b) Server thật với MySQL dev: lệnh trong AGENTS.md (cổng 8090).
#      Dữ liệu dev cũ (map cũ) không cần xóa để chạy: nhân vật cũ tự được đưa về Quảng Trường.
#      Muốn chơi lại sạch (D3): sh tools/p01/reset_dev_db.sh  rồi  sh tools/p01/reset_dev_db.sh --yes

# 2) Client (terminal khác)
cd apps/client
npm install
npm run dev                       # mở http://127.0.0.1:5180
```

Thử trên iPhone cùng Wi-Fi: `npm run dev -- --host 0.0.0.0`, rồi mở `http://<IP máy Mac>:5180` bằng Safari.
Server khác cổng: `GAME_SERVER=http://127.0.0.1:8095 npm run dev`. Vite chuyển `/api`, `/healthz`, `/ws` sang server nên không cần CORS.

### Điều khiển

| Việc | Bàn phím | Cảm ứng / chuột |
|---|---|---|
| Đi | Mũi tên / WASD (giữ để đi liên tục) | D-pad trái dưới, hoặc chạm vào ô đất để đi tới |
| Nói chuyện / chọn bệ / trụ | Enter, Space, E (đứng kề) | Chạm vào NPC/bệ/trụ (tự đi tới rồi mở) · nút **Chọn** |
| Đóng / mở menu | Esc, M | Nút **Trở về**, nút Menu |
| Gặp quái | Đi tới đứng kề quái | Chạm vào quái |
| Qua cổng | Đi vào vùng cổng ở mép map | Chạm vào lối ra |

### Tuyến Đợt A (v1.0.0)

Triệu Linh Điện (chọn 1 trong 3 bệ → nhận pet → sang Bìa Rừng, một chiều) → Bìa Rừng Lục Bảo (NPC, 4 điểm quái) ↔ Rừng Sâu Lục Bảo (8 điểm quái) → lần đầu Hoàng Môn, các lần sau thẳng Quảng Trường · Hoàng Môn ↔ Quảng Trường Thạch Trụ · Trụ đá Quảng Trường → Bìa Rừng. Lối sang Thương Phố, Vương Cung và đích trụ Điền Trang/Bờ Đông hiện nhưng khóa ("chưa mở").

### Cài đặt đồ họa (Menu → Cài đặt)

Thấp / Trung bình / Cao và giới hạn 30 / 60 FPS riêng, lưu trong trình duyệt. Thấp: độ phân giải 0,75×, không bóng, 35% trang trí, tắt hiệu ứng phụ, sàn không tính ánh sáng. Cao: bóng đổ thật theo hình sprite. Quái/NPC/thông tin trận giống nhau ở mọi mức.

## Kiểm tra tự động

```sh
npm run typecheck      # tsc strict
npm test               # vitest: phiên WS, lưới/A*/bộ điều khiển di chuyển
npm run build          # build production vào dist/
npm run check          # cả ba lệnh trên

npx playwright install chromium webkit   # lần đầu
npm run e2e                              # tự bật devserver (8098) + Vite (5188): chromium + webkit + iPhone giả lập
npm run e2e -- --project=chromium        # một trình duyệt
```

E2E đi thật: đăng ký → bệ đá → Bìa Rừng → Rừng Sâu → Hoàng Môn → Quảng Trường → trụ đá; chạm quái → trận → chạy → quái ẩn; NPC hồi phục; cổng khóa; lưu cài đặt.
Bản dev có móc `window.__phimond` (world, session) cho E2E/gỡ lỗi; bản build chỉ có khi mở với `?debug`.

## Art

Ảnh nằm trong `public/hd2d` (kit HD-2D đã duyệt) và `public/pets` (atlas linh thú P10), sinh bằng:

```sh
python3 tools/p01/sync_client_assets.py     # chạy từ gốc repo, cần Pillow + numpy
```

Asset chặn 1.0.0 chưa duyệt (sàn thành, nền xa thành, 7 NPC mới, hòm thư) đang dùng **bản tạm** cắt từ ảnh owner nộp (`_intake/`), đánh dấu `provisional` trong `public/hd2d/assets.json`. Nhân vật chính dùng dải idle/run cũ (một hướng) tới khi cắt xong bộ 3 hướng của đơn 09. Duyệt art xong thì chạy lại script.

## Cấu trúc

| Thư mục | Vai trò |
|---|---|
| `src/net` | Phiên WebSocket: xác thực khung đầu, request_id, nhiều move chờ cùng lúc (D1), khử lặp revision, quá hạn → đóng không gửi lại, tự kết nối lại |
| `src/world` | Tọa độ (ADR-P01-01), lưới đi (cùng RLE với server), A*, `Mover` (đi mượt, pipeline, đối soát với server) |
| `src/game` | `GameWorld`: nhận trạng thái server, tự qua cổng/chạm quái khi đứng đúng chỗ, tương tác NPC/bệ/trụ, chuyển map; `content`: tên tiếng Việt, văn bản sự kiện |
| `src/render` | Renderer, camera HD-2D, dựng cảnh từ `layout` của map + kit, sprite người/NPC/linh thú, cache texture có giới hạn, chọn bằng chạm |
| `src/ui` | HUD gốc, menu, cài đặt, hội thoại NPC (hồi phục/cửa hàng/học kỹ năng/nhiệm vụ), bệ đá, trụ, trận đấu |
| `src/state` | Signals dùng chung: phiên, cài đặt, lớp phủ, log, thông báo |
| `tests/unit`, `tests/e2e` | vitest, Playwright |

## Giới hạn đã biết (theo plan, làm ở bước sau)

- Benchmark (`?bench=`), đo frame/bộ nhớ trên thiết bị thật và QA thủ công: S6/S7 (owner yêu cầu sau).
- Quái dùng 14 loài cũ hiển thị bằng atlas P10 (nợ N02); chức năng NPC chưa có ở server báo "chưa mở" (N04); Huyết Chiến Đài chưa mở (N01).
- Nhân vật chính một hướng; NPC idle tĩnh với 7 NPC mới (chặng 6 chưa có).
- Kênh chat Thế giới/Khu vực/Đội/Riêng chỉ là khung; log hiện thông báo hệ thống và đổi map.
