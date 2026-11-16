# Phimond

Game web HD-2D (phong cách Octopath) dựng lại vòng chơi nuôi thú và dung hợp nhiều đời của 《靈獸世界 Online》. Đang chơi được tại <https://play.philand.io.vn> (bản `v1.1.0`: 11 map từ Triệu Linh Điện tới Vương Cung, Điền Trang, Phòng thú cưng). Đây chưa phải bản sao đầy đủ hay đã được chứng nhận 100%; luật gốc, phần dựng lại có chủ ý và khoảng trống nằm ở [research](docs/research/fidelity.md) và [trạng thái](docs/STATUS.md).

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `apps/client` | Client web: Vite + TypeScript + Three.js + Preact. Đây là client duy nhất của game. |
| `apps/game-server` | Server Go: luật chơi, map, NPC, trận đấu, MySQL, REST + WebSocket. |
| `apps/web` | Trang đồng hành (Next.js): bách khoa, công thức, nhật ký pet. |
| `data` | Catalog chạy thật (loài, kỹ năng, vật phẩm, map `data/maps/p01`, NPC). Thiết kế 160 loài/97 kỹ năng nằm ở `.ai/plan/phases/`. |
| `migrations` | Schema MySQL có version. |
| `packages` | Hợp đồng giao thức (`protocol`, `protocol-ts`). |
| `deploy` | Docker + manifest triển khai homelab (k3s); xem [docs/DEPLOY-HOMELAB.md](docs/DEPLOY-HOMELAB.md). |
| `art` | Kho art nguồn (GPT/Codex): ảnh final, manifest, prompt, 160 atlas pet đã duyệt. Ảnh trung gian nằm trên đĩa, git bỏ qua. |
| `tools` | Công cụ dựng map, cài art, kiểm tra nội dung và art. |
| `docs` | Kiến trúc, DB, gameplay, nghiên cứu, báo cáo. |
| `.ai` | Master plan, spec từng phase, đơn đặt art, review. |

Chi tiết, chính sách art và bản đồ đường dẫn cũ → mới: [docs/REPO-LAYOUT.md](docs/REPO-LAYOUT.md).

## Chạy local

1. Tạo `.env` từ `.env.example`. Dùng **một database MySQL riêng** (`phimond_reconstruction`), không dùng database khác.
2. Migrate: `./tools/server.sh -migrate`.
3. Chạy server: `./tools/server.sh` (mặc định `http://127.0.0.1:8090`).
4. Chạy client: `cd apps/client && npm ci && npm run dev` rồi mở `http://localhost:5180`. Hướng dẫn thêm (thử trên iPhone cùng Wi-Fi, e2e): [apps/client/README.md](apps/client/README.md).
5. Trang đồng hành (tùy chọn): `cd apps/web && npm ci && npm run dev` (cổng 3100).

Cần Go 1.25+, Node 20.9+, MySQL 8+. Thông tin đăng nhập chỉ nằm trong `.env` (đã bị git bỏ qua).

## Kiểm tra

```sh
sh tools/check.sh          # go test -race, go vet, map, client typecheck/unit/build, web, cổng art
cd apps/client && npm run e2e   # Playwright, cần server chạy
python3 tools/p01/build_maps.py --check   # kiểm tra 11 map
```

## Phát hành

Push lên `main` chạy `.github/workflows/release-main.yml`: kiểm tra → tính version từ commit (`feat` tăng minor, `fix` tăng patch) → build 2 image → gắn tag → cập nhật manifest ở repo hạ tầng. Thay đổi chỉ ở tài liệu, `.ai`, `art`, `tools`... được bỏ qua (không ra bản mới vì mỗi lần rollout ngắt người chơi).

Lịch sử: client Godot và client thử `apps/game-web` đã bị xóa; xem lại bằng tag `archive/game-client-final` và `archive/game-web-final`.
