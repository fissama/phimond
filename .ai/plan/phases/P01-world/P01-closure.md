# P01 — Đóng phase và handoff package

- **Ngày:** 2026-11-13. **Trạng thái: ĐÓNG CÓ NỢ — owner xác nhận ký 2026-11-13** (chat): phần đo hiệu năng và kiểm thử thiết bị thật chuyển thành nợ (N07–N13 trong [`P01-scope.md`](P01-scope.md) §6), không chặn đóng P01.
- **Phiên bản chốt:** tag `v1.1.0` (commit `02109580`, CI tự tạo 2026-11-10). v1.0.0 golive 2026-11-05 tại `play.philand.io.vn`; 23 commit giữa hai tag.
- **Nguồn yêu cầu:** master spec §6 P01 (R01–R10 + exit gate), [`P01-scope.md`](P01-scope.md) §8, [`P01-implement-plan.md`](P01-implement-plan.md), [`P01-B1-plan.md`](P01-B1-plan.md).
- **Lưu ý trung thực:** đóng "có nợ" khác "đạt toàn bộ gate". Master spec đòi báo cáo budget, giới hạn và thiết bị chưa đạt; mục §5 dưới đây là báo cáo đó. Không có số đo FPS/bộ nhớ nào được chứng nhận cho `apps/client`.

## 1. Đã giao

| Hạng mục | Nội dung |
|---|---|
| v1.0.0 (Đợt A) | 5 map: Triệu Linh Điện, Bìa Rừng, Rừng Sâu, Hoàng Môn, Quảng Trường; client mới `apps/client` (Three.js + Vite + Preact); luồng người chơi mới (3 bệ đá), 3 ô nhân vật/tài khoản, HUD gốc + menu, Cài đặt đồ họa, trận đấu P13, P10/P11/P13 áp vào runtime |
| v1.1.0 (Đợt B1) | 6 map: Thương Phố, Vương Cung, Vạn Sự Hội Sảnh, Điền Trang Lục Dã, Phòng thú cưng, Huyết Chiến Đài (chỉ cảnh + lối vào, nợ N01); 8 NPC mới (shop ×2, hồi máu ×2, còn lại "chưa mở"); 39 asset vẽ lại đợt GPT 12 |
| Ổn định hoá | Ping WebSocket 25 s (proxy không cắt kết nối đứng yên); bộ tách câu lệnh migration bỏ qua chú thích/chuỗi (DB mới chạy được migration 003, file 003 không đổi) |
| Triển khai | k3s namespace `phimond` trên homelab; CI `release-main` (test, semver theo commit, build image, tag, bump manifest ở repo `phimond-infra`); runbook [`docs/DEPLOY-HOMELAB.md`](../../../../docs/DEPLOY-HOMELAB.md) |
| Đồ thị cổng | Mở: Hoàng Môn ↔ Thương Phố ↔ Quảng Trường; Hoàng Môn ↔ Vương Cung ↔ Hội Sảnh; trụ Quảng Trường → Điền Trang ↔ Phòng thú; cổng đấu trường (cấp 10). Khóa có thông báo "chưa mở": Bờ Đông, Hải Tặc Hào |

## 2. Đối chiếu yêu cầu P01-R01…R10

| Yêu cầu | Kết quả | Bằng chứng | Nợ |
|---|---|---|---|
| R01 tọa độ X/Y thống nhất | Đạt | `internal/world` + `data/maps/p01/*.json`; Go test `-race`; `build_maps.py --check` (11 map: BFS, cổng, điểm đến, NPC) | — |
| R02 walkable/collision theo dữ liệu | Đạt | Lưới đi trong JSON, không suy từ ảnh | — |
| R03 phím/D-pad/click, dừng đúng | Đạt (Chromium) | Unit `world.test.ts`, e2e "điều khiển thật" | N11 (WebKit/iPhone chưa chạy) |
| R04 cổng/NPC hai trục, "chưa mở" | Đạt | Go test cổng/NPC; e2e đi hết đồ thị | — |
| R05 vòng đời quái solo | Đạt | e2e chạm → trận → chạy → quái ẩn → hồi; chọn đúng mục tiêu | N11 (reconnect giữa trận chưa có e2e riêng) |
| R06 review gameplay đầu/giữa/cuối | **Một phần** | Review rời rạc ở `.ai/design/v1.0.1/` (`REVIEW-v1.0.0-VONG-2/3`, `-TOAN-DIEN`, `review-gameplay-v1.0.0`, `review-graphics-v1.0.0`, `PLAYTEST-OCTOPATH-GAP`) và owner chơi thật v1.0.0/v1.1.0 | N10 (chưa có số đo thao tác hụt/kẹt/encounter và báo cáo cuối) |
| R07 cảnh HD-2D + camera/bóng/occlusion | Đạt trên Chromium | 11 map dựng bằng kit đã duyệt; ảnh chụp từng map | N09 (Safari thật) |
| R08 tải/giải phóng theo map, budget | **Một phần** | Tải theo map trong client theo thiết kế | **N08** (chưa có `?bench=`, không số đo, không budget) |
| R09 HUD/menu foundation | Đạt | HUD theo quyết định owner 2026-10-29, nhiều vòng review | — |
| R10 Low/Medium/High + 30/60 FPS | **Một phần** | Có chọn, lưu, fallback storage, e2e lưu qua tải lại | **N07** (chưa chứng minh Low giảm tài nguyên bằng đo) |

## 3. Exit gate master spec — đối chiếu

| Điều kiện gate | Trạng thái |
|---|---|
| Route city → forest → city → ranch bằng keyboard/D-pad/click | Đạt (Điền Trang mở từ v1.1.0) |
| Không xuyên chướng ngại/teleport; gặp đúng quái; rời trận không lặp vô hạn | Đạt (test + e2e) |
| Vị trí khi reconnect khớp state hợp lệ | Có test persistence và e2e tải lại trang; chưa có e2e reconnect giữa trận → N11 |
| Playtest góc map, đổi tỷ lệ cửa sổ, focus loss | Owner đã chơi; chưa có ca QA ghi lại → N10 |
| Cảnh HD-2D chạy trên desktop web và điện thoại iOS/Android | Chromium: có. iPhone/Safari thật cho `apps/client`: **chưa có bằng chứng** → N09. Android hoãn sang P05 (D4) |
| HUD/menu/cấu hình thao tác được; đổi preset/portal không tích lũy tài nguyên | Thao tác được. "Không tích lũy" **chưa đo** → N08 |
| Báo cáo budget, giới hạn, thiết bị chưa đạt | Đây là báo cáo; budget chưa có số → N07/N08 |

## 4. Kiểm tra đã chạy (2026-11-10, trước tag v1.1.0)

`go test ./... -race` (Go 1.24 cục bộ; CI dùng Go 1.25) · `go vet` · `python3 tools/p01/build_maps.py --check` (11 map) · `tsc` · 27 unit test client · `vite build` · e2e Chromium 14/15 ở lượt đủ bộ, test còn lại (cửa hàng Thương Phố + Ngự Y) sửa bước chờ tải rồi chạy riêng qua · test mới: ping WebSocket (`keepalive_test.go`), tách SQL (`splitsql_test.go`). CI `release-main` chạy lại test job khi push.

## 5. Báo cáo giới hạn (chưa đạt / chưa kiểm)

- Không có số đo frame time, bộ nhớ, tải lần đầu, thời gian đổi map, phiên dài cho `apps/client` (N08). Số đo duy nhất từng có là prototype P12 Stage 3: iPhone ở mức high ~60 FPS, không chuyển cho client mới.
- Chưa chứng minh Low nhẹ hơn High (N07). Chưa chạy trên iPhone 17 Pro Max Safari, macOS Safari, Chrome cho client mới (N09). Android chưa thuộc phạm vi.
- Chưa chạy WebKit/iPhone giả lập, chưa có test throttle RTT, chưa so ảnh 5 cảnh × 3 preset (N11). Chưa chạy tải server 10 CCU với profile `p01-route` (N12).
- Chưa kiểm với MySQL thật (test `fault_mysql` tự bỏ qua khi không có DB), chưa đo WS idle ≥ 3 phút qua ingress thật, chưa lập sao lưu MySQL/theo dõi log (N13).
- Cosmetic: Điền Trang chỉ 1 hàng ruộng (rìa rừng che hàng dưới), nhà rơm mờ khi đứng gần, Vương Cung sàn còn nhạt, `palace-throne-dais` và `farm-soil-edge-01/02` chưa dùng, NPC chưa có idle (N15).

## 6. Nợ chuyển giao

Danh sách đầy đủ và phase sở hữu ở [`P01-scope.md`](P01-scope.md) §6: N01–N06 cũ và **N07–N16 mới** (đo hiệu năng, thiết bị thật, QA, e2e, tải server, hạ tầng, dọn client cũ, art B1, Bãi biển). Master spec §8 có hàng D28 trỏ về các nợ đo hiệu năng và gate chuyển sang P05/P06/P09.

## 7. Handoff: những điều phase kế tiếp cần biết

**Kiểm tra nhanh**
- `sh tools/check.sh`: `go test -race`, `go vet`, `build_maps.py --check`, client `npm run check`, `check_godot.mjs`.
- Client: `cd apps/client && npm run check` (typecheck, 27 unit, vite build); `npm run e2e` (Playwright; mặc định Chromium, WebKit/iPhone cần `npx playwright install webkit`).
- Go 1.25 là bản CI; môi trường cloud chỉ có 1.24 nên cần `GOTOOLCHAIN=local` và sửa go.mod cục bộ, không commit.

**Cấu trúc**
- Map: `tools/p01/build_maps.py` sinh `data/maps/p01/*.json` (ký tự đi được `.,:=_+fgmRN`, ký tự khác chặn). Không sửa JSON tay; sửa script rồi chạy `--check`. Không đổi id hoặc tọa độ map có người chơi đứng.
- NPC: `data/npcs/npcs.json`. Validator content bắt NPC phải đứng trên ô chặn đúng quy ước.
- Client: `render/scene.ts` giữ THEMES, `floorFor`, `propsFor`, bảng `MAP_PROPS/MAP_EXTRAS/MAP_DECALS` theo map; `assets.json` là manifest ảnh (prop pivot chân, floor 512 px = 4 ô, decal pivot giữa). 128 px/ô.
- Giao thức WS: `apps/game-server/internal/transport` (có ping 25 s, AFK 10 phút không gửi lệnh).
- Phát hành: push `main`; commit `feat` tăng minor, `fix` tăng patch; push chỉ đổi `.ai`, md, `docs`, `art`, `tools`... thì CI bỏ qua (paths-ignore trong `.github/workflows/release-main.yml`).

**Quy tắc phải giữ**
- Có người chơi thật: mọi thay đổi `characters.state` cần migration và tương thích ngược; không sửa file migration đã áp dụng (checksum nằm trong DB prod).
- Asset id không được trùng id cũ (đã từng ghi đè `farm-scarecrow`).
- Điền Trang và Phòng thú "riêng từng người" hiện đúng nhờ server chưa có presence; P06 thêm presence thì phải kiểm lại hợp đồng P12.

**Đầu vào cho phase sau**
- P19: nợ N04 (NPC chưa có kho/thư/hội); `Inventory map[string]int` giữ nguyên định dạng.
- P02/P15: quái vẫn là 14 loài cũ (N02); cân bằng đầu game tạm thời đến P15.
- P05: nghiệm thu nợ N07–N11, N15; Android; HUD touch trên máy thật.
- P06: presence, tải 50 CCU (N12), kiểm hợp đồng map riêng.
- P16: Điền Trang và khu vườn ngầm (art garden đang được vẽ).

## 8. Việc còn lại trước khi "đóng sạch"

1. ~~Owner xác nhận ký đóng P01 (đóng có nợ).~~ Đã ký 2026-11-13.
2. ~~Push các commit art lên `main`.~~ Đã đổi: 7 commit art (4,5 GB) KHÔNG push, chỉ giữ ở nhánh local `backup/pre-restructure-20261113`; art nguồn nằm trong `art/`, git chỉ theo dõi ảnh final/manifest/prompt.
3. ~~Nợ N14: dọn `apps/game-web` và `apps/game-client`.~~ Xong 2026-11-16 (xem [`docs/REPO-LAYOUT.md`](../../../../docs/REPO-LAYOUT.md)).
