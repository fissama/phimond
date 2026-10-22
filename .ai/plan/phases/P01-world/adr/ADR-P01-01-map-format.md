# ADR-P01-01 — Hệ tọa độ và định dạng map dùng chung

- **Ngày:** 2026-10-22. **Trạng thái:** chấp nhận (owner chốt D1/D2 ngày 2026-10-22). **Phase:** P01 (R01, R02, R04, R05).

## Bối cảnh

Server hiện chỉ có lưới `width×height` không va chạm; cổng và NPC chỉ xét trục X; qua cổng chỉ đặt lại X; vị trí quái sinh bằng công thức. P01 cần một mô hình X/Y duy nhất cho map, renderer, NPC, cổng, spawn (R01), va chạm theo dữ liệu (R02), tầm tương tác hai trục (R04) và vùng quái theo kế hoạch P12 (R05).

## Quyết định

### Tọa độ

- Gameplay dùng ô nguyên `(x, y)`: `x` tăng sang phải, `y` tăng xuống dưới màn hình (về phía camera). Gốc `(0,0)` ở góc trên-trái map.
- **1 ô = 1 đơn vị world = 128 px art** (nền xa 64 px/đơn vị).
- Three.js: `X = x`, `Z = y`, mặt đất `Y = 0`; tâm ô ở `(x+0.5, 0, y+0.5)`.
- Tầm tương tác dùng khoảng cách Chebyshev `max(|dx|,|dy|)`: NPC ≤ 1 (đứng kề, kể cả chéo), vùng cổng = đứng trong hình chữ nhật cổng, quái = trong vùng contact.
- Di chuyển 4 hướng, mỗi `world.move` một ô (D1).

### File map

Mỗi map một file `data/maps/p01/<map_id>.json` (ID theo P12). Server đọc phần luật; client đọc cả phần luật lẫn `scene`.

| Trường | Kiểu | Nghĩa |
|---|---|---|
| `id`, `name` | string | ID P12, tên hiển thị |
| `kind` | `transit_once`·`field`·`mixed`·`safe_hub` | Theo P12 registry |
| `width`, `height` | int | Kích thước lưới (ô) |
| `walk` | string | Lưới đi: các hàng từ `y=0`, nối bằng `/`; mỗi hàng là chuỗi run-length `<số><ký tự>` với `.` = đi được, `#` = chặn. Ví dụ `3#4.3#` = 3 chặn, 4 đi được, 3 chặn. Tổng mỗi hàng phải bằng `width` |
| `spawn_default` | `{x,y}` | Điểm đặt khi vào map không qua cổng (đăng nhập, hồi sinh) |
| `respawn_to` | map id | Map hồi sinh/thoát kẹt (P12) |
| `portals[]` | `{id, rect:[x,y,w,h], to, arrive:{x,y,face}, locked?, requires?}` | Vùng cổng hình chữ nhật. `locked` = hiện nhưng chưa mở. `requires` = điều kiện (cờ nhiệm vụ, cấp) |
| `pillar` | `{npc, dest:[{map, arrive, locked?, min_level?}]}` | Trụ đá dịch chuyển (chỉ Quảng Trường ở 1.0.0) |
| `npcs[]` | `{id, x, y, face}` | Vị trí NPC (ID theo roster P12) |
| `spawn_zones[]` | `{id, rect, species[], max_alive, respawn_s}` | Vùng quái theo `P12-S4-spawn-plan.json` |
| `scene` | string | Đường dẫn file cảnh của client (kit HD-2D, ánh sáng, camera). Server bỏ qua |

### Luật kiểm hợp lệ (server từ chối khởi động nếu sai)

1. Mỗi hàng `walk` đủ `width` ô; có đúng `height` hàng.
2. `spawn_default`, mọi `arrive`, mọi NPC (ô đứng) và ít nhất một ô trong mỗi vùng quái đều nằm trên ô đi được.
3. `arrive` không nằm trong bất kỳ vùng cổng nào của map đích, và cách vùng cổng ≥ 1 ô (không kích hoạt lại cổng).
4. Từ `spawn_default`, BFS 4 hướng tới được mọi vùng cổng, mọi ô kề NPC, mọi vùng quái (không có khu bị cô lập).
5. `to` của cổng và `dest` của trụ trỏ tới map tồn tại, hoặc có `locked: true`.
6. NPC thuộc roster P12 của đúng map đó.

### Protocol (cộng thêm, D2)

- `/api/content` → `maps[id]` thêm `walk`, `spawn_default`, `portals[].rect/arrive/locked/requires`, `pillar`, `spawn_zones`. Trường cũ giữ cho client cũ trong thời gian chuyển tiếp.
- `world.portal {portal_id}`: hợp lệ khi người chơi đứng trong `rect`; đặt `map_id/x/y = arrive`.
- `world.move`: từ chối khi ô đích bị chặn (`"blocked"`), không tăng revision.
- `npc.interact`: hợp lệ khi Chebyshev ≤ 1.
- Intent mới, intent trụ đá và vòng đời quái được mô tả trong `packages/protocol/README.md` khi làm S1/S4.

## Hệ quả

- Lưới đi là nguồn chuẩn duy nhất cho va chạm; cảnh HD-2D phải khớp lưới (client có lớp debug vẽ lưới đè cảnh).
- 5 map cũ bị gỡ, dữ liệu dev bị xóa (D3); test server cũ được viết lại theo map mới.
- Client tìm đường (A*) trên cùng lưới nên đường đi client đề xuất luôn hợp lệ với server, trừ khi trạng thái lệch (lúc đó server từ chối, client kéo về vị trí xác thực).
