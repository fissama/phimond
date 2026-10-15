# P12 — Checklist đóng phase (rà soát 2026-10-15)

Nguồn sự thật cho "P12 còn thiếu gì". Cập nhật mỗi khi một mục đổi trạng thái. P12 vẫn **OPEN**; owner quyết định đóng phase.

## 1. Trạng thái theo stage

| Stage | Trạng thái | Bằng chứng | Còn thiếu |
|---|---|---|---|
| 1. Nguồn / inventory | Gần xong | `~/Downloads/Phimond-P12-Review/` (92 map, 39/40 mục duyệt, nguồn chính APK 3.2) | `review_detailed_scope` vẫn `unresolved` (xem §2-A4) |
| 2. Audit Emerald + tuyến thành | **ĐÓNG** (owner duyệt 2026-10-14) | [P12-stage2-audit.md](P12-stage2-audit.md) | — |
| 3. Golden Scene / benchmark | Quyết định đã có, bằng chứng iPhone còn thiếu | `prototypes/p12-stage3/`, [ADR-0001](../../../decisions/ADR-0001-threejs-web-client.md) **Accepted**: Three.js | Số đo `?bench=1` trên iPhone 17 Pro Max Safari + macOS Safari; owner tuyên bố đóng Stage 3. Spec benchmark Godot vs Three.js đã **SUPERSEDED** |
| 4. Thiết kế chi tiết + ma trận | **ĐANG LÀM** — owner cấp quyền 2026-10-15 (chỉ tài liệu/dữ liệu thiết kế, không sửa runtime) | [stage4/P12-S4-design.md](stage4/P12-S4-design.md) (hướng dẫn chạy lại: [stage4/README.md](stage4/README.md)): portal, trụ, cấp vùng (đã duyệt), roster 49 NPC (chờ duyệt), vùng an toàn + hồi sinh (đã chốt, ngoại lệ Emerald) và điểm spawn có bản nháp; không còn câu hỏi mở về NPC/vùng an toàn; danh tính quái do P15; instance còn khung | Xem §3 |
| 5. Validation / review đóng phase | Chưa bắt đầu | — | Sau Stage 4 |

## 2. Việc chờ owner duyệt (không cần chạy gì)

| # | Mục | Đề xuất hiện tại | Nơi ghi |
|---|---|---|---|
| A1 | ~~7 tên đổi mục C + Hải Tặc Hào~~ | **ĐÃ DUYỆT 2026-10-15** | [names master §C](P12-world-names-master.md) |
| A2 | ~~3 thần thú Sảnh vẫy gọi~~ | **ĐÃ DUYỆT 2026-10-15:** Linh Tiên Hoa Hương `species_0144`, Đại Vương Bọ Cạp `species_0151`, Thú Vàng Một Sừng `species_0149` | [baseline U10](P12-emerald-baseline-package.md) |
| A3 | Câu cũ #4: tên minigame Sói–Cừu & khu dịch vụ bang | Sói–Cừu đã thơ hóa; dịch vụ bang chưa quyết | names master "Còn mở" |
| A4 | `review_detailed_scope` | **ĐÃ CHỐT trong hội thoại 2026-10-15:** City 8 map (`city_square`, `city_market`, `city_royal_palace`, `city_palace_gate`, `city_pet_room` = CanPhong / Phòng thú cưng, `city_farm`, `city_deathmatch_arena`, `city_activity_hall`) + Emerald 2 map + Bãi biển 5 map + `summoning_hall_main_hall` + `middle_corridor_main_hall` (Hải Tặc Hào). Còn lại chỉ ở global draft | Owner còn cần đánh dấu trong `reviews.json` (công cụ duyệt) |
| A5 | Gói baseline Emerald (tổng thể) | U1–U6, U8–U9 chốt; U10 chờ A2; U7 hoãn | baseline package |
| A6 | Tọa độ Sảnh vẫy gọi | Owner mô tả, hoặc agent đề xuất từ ảnh gốc ở Stage 4 | baseline U10 |

## 3. Stage 4 — sản phẩm cần có (khi được cấp quyền)

Phạm vi: City / mọi map Forest / Beach / Farm / Arena liên quan + Sảnh vẫy gọi + Hải Tặc Hào (dependency của trụ).

1. **Registry map canonical** trong repo (`data/` hoặc `.ai`): ID code, tên owner, scene/root nguồn, cấp vùng, loại (safe/field/instance), trạng thái triển khai. Global draft giữ đủ 92 map, kể cả map chưa làm.
2. **Ma trận portal/teleport:** cửa, trụ (Quảng trường → vùng Lv1–40 + Nông trại + Tàu; Tàu → 6 vùng Lv40+ + Nông trại + về thành), một chiều/hai chiều, điểm xuất hiện (≈1 đơn vị + guard chống re-trigger, R-S2-1), điều kiện mở khóa (Sảnh vẫy gọi → Emerald một chiều).
3. **Ma trận NPC/dịch vụ:** NPC nào ở map nào, dịch vụ gì (shop, kho, lai tạo…), phase sở hữu logic.
4. **Ma trận spawn/area:** vùng quái theo map (danh tính + hành vi + khu vực); số cấp/XP để P15, drop để P19/P20 (U7).
5. **Ma trận access/recovery:** chặn cấp (U4: không chặn Emerald), hồi sinh/về thành khi chết hoặc kẹt, safe arrival.
6. **Template/instance & ownership:** map dùng chung vs instance (Đấu trường, Sói–Cừu, phòng mê cung), phase sở hữu từng phần.
7. **Đối chiếu runtime:** khác biệt giữa thiết kế P12 và `data/maps/maps.json` hiện tại (5 map, 60×24) — xem §4. Việc sửa runtime thuộc P01.

## 4. Lệch giữa thiết kế P12 và runtime hiện tại (ghi nhận, chưa sửa)

| Thiết kế P12 | Runtime (`data/maps/maps.json`, `apps/game-web`) |
|---|---|
| Người chơi mới bắt đầu ở Sảnh vẫy gọi, chọn 1 trong 3 pet, rồi dịch chuyển một chiều tới Emerald | Không có Sảnh vẫy gọi; nhân vật mới vào `severa` |
| Quảng trường → vùng ngoài bằng trụ teleport | Có `pillar` trong scene + menu trụ; vẫn còn cửa `severa` x=43 → forest/ranch/arena |
| U4: không dùng `level_field_raw` làm luật chặn | `beach.min_level = 10` |
| Tên hiển thị theo names master | Đúng (i18n `vi.json`); ID nội bộ `severa/forest/beach/ranch/arena` và `name` tiếng Anh trong `maps.json` là placeholder |

## 5. Hoãn có chủ (deferred register)

| Mục | Phase nhận | Lý do |
|---|---|---|
| U7 NPC/spawn/monster số liệu | P15 (cấp, XP), P19/P20 (drop) | P12 chỉ giữ danh tính/hành vi/khu vực |
| Logic nói chuyện/nhận pet ở Sảnh vẫy gọi | P04 (UI chọn: P03/P04) | — |
| Va chạm HD-2D đầy đủ | P01 / Stage 4 | U3: dựng mới, không khôi phục gốc |
| Tin nhắn Đội/Hội/Riêng/Thế giới | phase social | server chưa có |
