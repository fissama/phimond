# P01 — Kế hoạch v1.1.0 (Đợt B1: Thành) — 2026-11-06

Trạng thái: **ĐÃ DỰNG xong 6/6 map (2026-11-06), chờ review thiết bị thật + chạy test Go/CI.** Bối cảnh: [`P01-scope.md`](P01-scope.md) §8 (đóng P01 ở v1.1.0).

## 1. Phát hiện chính: không cần cơ chế "map riêng theo người chơi"

Server hiện **không có presence** (không có danh sách người chơi cùng map, không broadcast vị trí; `live`/`sessions` chỉ giữ từng nhân vật; quái vốn đã "riêng từng người"). Vì vậy mọi map đều đang là không gian một người. Điền Trang và Phòng thú cưng "riêng từng người" **tự đúng**, không cần instance.
- Bản kế hoạch cũ coi đây là việc server lớn nhất; thực tế **không phải**, bỏ khỏi v1.1.0.
- Điều kiện giữ: hợp đồng P12 (farm private/account-owned, khách chỉ xem) sẽ được kiểm lại khi P06 thêm presence. Ghi vào P06, không làm bây giờ.
- Save người chơi hiện có không bị ảnh hưởng: map mới chỉ thêm vào `data/maps`; `normalizeLocation` đã xử lý map không tồn tại; `Visited` và quest `reach_map` đã chạy theo id map.

## 2. Đồ thị cổng (từ `portal-graph.json` P12, đối chiếu runtime)

| Từ | Tới | Hiện tại |
|---|---|---|
| city_palace_gate | city_market, city_royal_palace | cổng `locked` |
| city_square | city_market | cổng `locked` |
| city_square (trụ) | city_farm | `locked` |
| city_market | city_square, city_palace_gate | chưa có map |
| city_royal_palace | city_palace_gate, city_activity_hall | chưa có map |
| city_activity_hall | city_royal_palace | chưa có map |
| city_deathmatch_arena | city_square (cửa) | vào bằng NPC `sq_arena` (N01) |
| city_farm | city_square (cửa), city_pet_room (cửa) | chưa có map |
| city_pet_room | city_farm | chưa có map |

Điểm đến "cần đặt" ở Quảng Trường (arrival từ arena, từ farm) phải chọn toạ độ khi dựng.

## 3. Thứ tự dựng (mỗi map một commit, test tới đâu chạy tới đó)

1. **Thương Phố** (`city_market`) — kéo theo mở khoá hai cổng từ Hoàng Môn và Quảng Trường; NPC `mk_general`, `mk_trader`; kit market-*, awning-*, city-*.
2. **Vương Cung** (`city_royal_palace`) — NPC `pal_healer`; kit palace-*, `royal-carpet-runner`.
3. **Vạn Sự Hội Sảnh** (`city_activity_hall`) — NPC `act_events`; kit hall-*.
4. **Điền Trang Lục Dã** (`city_farm`) — mở trụ Quảng Trường; NPC `ranch_keeper`; farm-*, `farm-tilled-*`, `farm-hills-far`.
5. **Phòng thú cưng** (`city_pet_room`) — NPC `pet_master`, `pet_shop`; pet-nest-*, `pet-feed-bowl-*`.
6. **Huyết Chiến Đài** (`city_deathmatch_arena`) — NPC `arena_master`; chỉ cảnh + lối vào (nợ N01).

Mỗi map cần: hàm dựng trong `tools/p01/build_maps.py` (sinh JSON ở `data/maps/p01`), NPC trong `data/npcs/npcs.json`, mục trong `apps/client/public/hd2d/assets.json` + file ảnh (cài từ `art-src/.../p01-v1.1.0-b1`), kiểm tra `content` validate và e2e đi tới map.

## 4. Chức năng NPC ở 1.1.0 (đề xuất, cần owner chốt)

| NPC | Có sẵn ở server | Đề xuất 1.1.0 |
|---|---|---|
| mk_general, pet_shop | shop.buy (5 vật phẩm hiện có) | **Mở shop** với catalog hiện tại; thêm hàng mới chờ P19 |
| mk_trader | — | Hội thoại, "chưa mở" cho hàng luân phiên |
| pal_healer | heal | **Mở hồi máu** (có sẵn `pet_heal`) |
| ranch_keeper | — (kho pet) | Hội thoại, "chưa mở" (gửi/rút pet cần thiết kế kho, P03) |
| pet_master | — | Hội thoại, "chưa mở" (giám định/lai tạo P03/P16) |
| act_events | — | Hội thoại, "chưa mở" |
| arena_master | heal | Hồi máu + "chưa mở" cho đấu trường (N01) |

## 5. Rủi ro và việc cần kiểm

- Engine client chưa chắc hỗ trợ theme `farm`, `arena`, `interior` (hiện mới có `city`, `forest`, `hall`): cần đọc `render/engine.ts`, `world/` theo map trước khi dựng map 4–6.
- Content validator yêu cầu mọi NPC thuộc đúng map; thêm 8 NPC phải khớp.
- `build_maps.py` đã có kiểm tra bố cục; mở rộng cho 6 map mới, không sửa 5 map cũ (id/toạ độ đã có người chơi đứng).
- Go server vẫn không build được trong môi trường này; kiểm thử server dựa vào máy owner/CI.
- Hiệu năng: thêm ~60 ảnh; tải theo map nếu cần (liên quan v1.1.1).

## 6. Quyết định cần owner

1. Đồng ý bỏ cơ chế instance (mục 1)?
2. Bảng chức năng NPC mục 4 có ổn không?
3. Kích thước map B1 theo gốc APK rồi phóng ~20–30% như Đợt A, hay làm gọn hơn?


## 7. Kết quả dựng (2026-11-06)

- 6 map: `city_market` 30×12, `city_royal_palace` 26×13, `city_activity_hall` 20×11 (theme hall), `city_farm` 34×14 (theme forest + nền `farm-hills-far`), `city_pet_room` 20×11 (theme mới `room`), `city_deathmatch_arena` 30×13 (theme mới `arena`, `min_level` 10).
- Cổng mở: Hoàng Môn ↔ Thương Phố ↔ Quảng Trường, Hoàng Môn ↔ Vương Cung ↔ Hội Sảnh, trụ Quảng Trường → Điền Trang ↔ Phòng thú cưng, cổng `square_to_arena` (ô trên NPC `sq_arena`, cần cấp 10). Chưa có cổng từ Điền Trang tới trụ Hải Tặc Hào (tàu chưa có).
- NPC: 8 NPC mới. Chức năng: shop (`mk_general`, `pet_shop`), hồi máu (`pal_healer`, `arena_master`), còn lại hội thoại "chưa mở" (`mk_trader`, `ranch_keeper`, `pet_master`, `act_events`).
- Lỗi phát hiện khi chụp ảnh: map thành không có danh sách người đi đường làm hiện ô xanh (sprite thiếu). Đã sửa ở `ambient.ts`.
- Kiểm tra: `build_maps.py --check`, `tsc`, unit client, e2e chromium (xem log), ảnh chụp từng map. **Chưa chạy được test Go** (không có toolchain Go ở môi trường làm việc): cần `go test ./...` ở máy có Go hoặc CI.
- Còn lại cho P01 exit review: chơi thử trên iPhone/Safari, kiểm tay 6 map, ảnh cối xay quay (rotor) và nền xa Điền Trang chưa dùng (rừng viền che nền).
- Phiên bản: CI tự tăng minor khi có commit `feat(...)` kể từ tag `v1.0.0`, nên push các commit này lên main sẽ ra **v1.1.0**.

## 8. Hoàn thiện trước phát hành (2026-11-10)

- **Art bổ sung (đơn GPT 12):** 39 asset đã nghiệm thu và cài; 4 map dựng lại bố cục (Điền Trang có ruộng/hàng rào/cổng/giếng; Phòng thú cưng có sàn ván nhỏ/thảm/lồng/thú ngủ; Huyết Chiến Đài sàn cát/cổng sắt/đài trọng tài/lồng lửa; Vương Cung sàn cẩm thạch/cửa sổ kính/cờ/tượng vàng). Chưa dùng: `palace-throne-dais`, `farm-soil-edge-01/02`.
- **Sửa hình:** bỏ vũng nước/nắp cống/vết nứt lạc chỗ ở Thương Phố và Vương Cung; dời dây cờ và Nhà Buôn Lữ Hành ở Thương Phố; dời cột đấu trường khỏi giá vũ khí; viền sàn ngoài map của đấu trường/phòng không còn ám xanh.
- **Máy chủ:** ping WebSocket 25 giây/lần (ingress không cắt kết nối khi đứng yên; quy tắc AFK 10 phút không gửi lệnh vẫn giữ). Bộ tách migration bỏ qua chú thích/chuỗi có `;` — DB mới tinh chạy được migration 003 (DB production đã áp dụng 003, không bị ảnh hưởng vì checksum file không đổi).
- **Kiểm tra đã chạy:** `go test ./... -race` (chạy bằng Go 1.24 cục bộ; CI dùng Go 1.25), `go vet`, `build_maps.py --check` (11 map), `tsc`, 27 unit test client, `vite build`, e2e chromium: 14/15 qua ở lượt chạy đủ bộ, test còn lại (cửa hàng Thương Phố + Ngự Y) sửa bước chờ tải rồi chạy riêng qua.
- **Chưa kiểm được ở môi trường làm việc:** Safari/iPhone thật; MySQL thật (test `fault_mysql` tự bỏ qua khi không có DB); kết nối qua ingress thật ≥3 phút (ping đã có test đơn vị).
- **Nợ ghi nhận:** rìa rừng Điền Trang che hàng dưới nên ruộng chỉ 1 hàng; nhà rơm ở Điền Trang mờ đi khi nhân vật đứng gần (cơ chế che khuất chung); NPC chưa có hoạt ảnh đứng yên; chức năng guild/kho/thư/giám định "chưa mở"; Huyết Chiến Đài chỉ có cảnh (N01).
