> Nguồn Stage 1 (ngoài repo, chỉ đọc): `~/Downloads/Phimond-P12-Review/` (inventory, `recovered-portals.json`, `portal-geometry-draft.json`, `reviews.json` = bản ghi duyệt của owner). Repo chỉ giữ tài liệu thiết kế và tóm tắt.

# Đề xuất tên map theo style JRPG (56 map chưa duyệt)

Ngày: 2026-10-14. Trạng thái: **ĐỀ XUẤT để owner debate/duyệt**. Không sửa `reviews.json`, không đổi ID code, không đổi dữ liệu runtime.
Giữ nguyên 35 map bạn đã duyệt. Cột "Tên nguồn" giữ để truy ngược; 20 map chỉ có nhãn tạm "chưa đặt tên".

## Nguyên tắc đặt tên (cần owner xác nhận)
1. Tên hiển thị tiếng Việt, 2–4 âm tiết, ưu tiên Hán-Việt gợi hình (Lâm, Cung, Lũy, Tịch Diệt…) theo giọng localization JRPG.
2. Mỗi tên là **duy nhất trong toàn thế giới** (tránh trùng như "Rừng sâu Bích Ba" ×3, "Con đường phẫn uất" ×2).
3. Chỉ dựa vào hình ảnh, nhãn nguồn và vị trí trong sơ đồ nối. **Không bịa lore**.
4. Các phòng gần như giống hệt nhau dùng tên họ + số La Mã hoặc vai trò (Cửa, Ngách, Tận Cùng), không đặt 6 tên thơ riêng cho 6 ảnh giống nhau.

## Phát hiện từ sơ đồ nối 3.2 (liên quan trực tiếp tới debate P12)
- **Hành lang tầng giữa không có portal ra nào** trong bản nháp, dù có 6 map nối vào. Cần xác minh đường quay lại.
- **Quảng trường → Rừng Bibo (Emerald) chưa có tuyến vào**: Rừng sâu nối ra Cổng Hoàng cung, nhưng Cổng Hoàng cung chỉ nối Chợ, Cung điện, Quảng trường. Rừng Bibo chỉ có đường vào từ Sảnh vẫy gọi. Đây chính là "City → Forest entry/return/recovery" trong `critical_open`.
- Giao điểm (6), Tinh Không (6), Di Tích Cổ (6) là **chuỗi hoặc cây phòng cùng một nền**, nên khả năng cao là các màn ghép của cùng một khu.
- 3 map "Rừng sâu Bích Ba" (Lâu đài ma, Cây thế giới, Tháp Chim) có cùng tên nguồn; có thể dùng lại nền Rừng sâu của Emerald. Chưa xác minh.

## Bảng đề xuất
| ID code | Tên nguồn | Tên đề xuất | Ghi chú |
|---|---|---|---|
| `tomb_region_camp` | Doanh trại lăng mộ | **Trạm Canh Lăng** | hub của vùng Lăng Mộ |
| `tomb_region_dead_ruins` | Tàn tích chết | **Tàn Tích Tịch Diệt** |  |
| `tomb_region_deep_ruins` | Sâu trong tàn tích | **Thâm Cung Tịch Diệt** | cụt, nối từ Tàn Tích Tịch Diệt |
| `tomb_region_gods_tomb` | Lăng mộ của các vị thần | **Thần Lăng Vĩnh Miên** |  |
| `tomb_region_soul_cemetery` | Nghĩa trang linh hồn | **Bãi Vãng Sinh** | hub: nối Thần Lăng + 2 khu chưa tên |
| `tomb_region_unnamed_area_01` | (chưa đặt tên) | **Cồn Úa Vàng** | cụt; sa mạc vàng, cây gai khô |
| `tomb_region_unnamed_area_02` | (chưa đặt tên) | **Bãi Gai Khô** | cụt; cùng nền với 01 |
| `crossroads_unnamed_area_01` | (chưa đặt tên) | **Cổng Địa Đạo Lam Dạ** | nối Quảng trường; hub 02 + 05 · owner chọn B (2026-10-14) |
| `crossroads_unnamed_area_02` | (chưa đặt tên) | **Hành Lang Rêu Biếc** | chuỗi 01→02→03→04→06 · owner chọn B (2026-10-14) |
| `crossroads_unnamed_area_03` | (chưa đặt tên) | **Đoạn Thủy Quang** |  · owner chọn B (2026-10-14) |
| `crossroads_unnamed_area_04` | (chưa đặt tên) | **Ngã Ba Đêm Xanh** |  · owner chọn B (2026-10-14) |
| `crossroads_unnamed_area_05` | (chưa đặt tên) | **Hốc San Hô Tím** | cụt, nhánh từ 01 · owner chọn B (2026-10-14) |
| `crossroads_unnamed_area_06` | (chưa đặt tên) | **Đáy Địa Đạo** | cuối chuỗi · owner chọn B (2026-10-14) |
| `middle_corridor_main_hall` | Hành lang tầng giữa | **Hải Tặc Hào** (Tàu cướp biển, U5 chốt 2026-10-14) | hub nối Tháp/Cây/Lâu đài/Mê Thành/Khe nứt/Di tích |
| `astral_realm_spacetime_rift` | Khe nứt không thời gian | **Thời Không Liệt Khích** | nối Hải Tặc Hào |
| `astral_realm_unnamed_area_01` | (chưa đặt tên) | **Tử Vân Lâm** | hub: 02, 04, 05 + Khe nứt · owner chọn B (2026-10-14) |
| `astral_realm_unnamed_area_02` | (chưa đặt tên) | **Lối Mây Tím** | →03 · owner chọn B (2026-10-14) |
| `astral_realm_unnamed_area_03` | (chưa đặt tên) | **Bờ Hồ Vân Ảnh** | cụt · owner chọn B (2026-10-14) |
| `astral_realm_unnamed_area_04` | (chưa đặt tên) | **Hốc Cổ Thụ** | cụt · owner chọn B (2026-10-14) |
| `astral_realm_unnamed_area_05` | (chưa đặt tên) | **Rừng Hoàng Hôn** | →06 · owner chọn B (2026-10-14) |
| `astral_realm_unnamed_area_06` | (chưa đặt tên) | **Tận Cùng Thời Không** | cụt · owner chọn B (2026-10-14) |
| `ancient_ruins_unnamed_area_01` | (chưa đặt tên) | **Tiền Sảnh Ngọc Lục** | nối Hải Tặc Hào; hub 02, 03, 04 · owner chọn B (2026-10-14) |
| `ancient_ruins_unnamed_area_02` | (chưa đặt tên) | **Phòng Tượng Cổ** | cụt · owner chọn B (2026-10-14) |
| `ancient_ruins_unnamed_area_03` | (chưa đặt tên) | **Phòng Tinh Thạch** | cụt · owner chọn B (2026-10-14) |
| `ancient_ruins_unnamed_area_04` | (chưa đặt tên) | **Hành Lang Thạch Vệ** | →05 · owner chọn B (2026-10-14) |
| `ancient_ruins_unnamed_area_05` | (chưa đặt tên) | **Thâm Sảnh Ngọc Lục** | →06 · owner chọn B (2026-10-14) |
| `ancient_ruins_unnamed_area_06` | (chưa đặt tên) | **Tận Điện Cổ Tích** | cụt · owner chọn B (2026-10-14) |
| `ghost_castle_gate` | Cổng lâu đài ma | **Cổng U Lâu** |  |
| `ghost_castle_deep_woods` | Rừng sâu Bích Ba | **U Linh Cổ Thành** | tên nguồn trùng với 2 map khác. Owner đổi 2026-10-17 (trước đó: U Lâm Bích Ba, đọc như bản đồ rừng trong khi là thành cổ) |
| `ghost_castle_ancient_city_secret_chamber` | Mật thất thành cổ | **Mật Thất Cổ Thành** |  |
| `world_tree_gate` | Cổng cây thế giới | **Thế Thụ Môn** |  |
| `world_tree_deep_woods` | Rừng sâu Bích Ba | **Thế Thụ Thâm Lâm** | tên nguồn trùng |
| `world_tree_secret_chamber` | Mật thất cây thế giới | **Mật Thất Thế Thụ** |  |
| `tower_region_main_tower` | Tháp Chim | **Điểu Tháp** | 'Tháp Chim' là đề xuất sửa chính tả trong NAMING-REVIEW |
| `tower_region_deep_woods` | Rừng sâu Bích Ba | **Vân Tiêu Thiên Tầng** | Owner yêu cầu đổi 2026-10-17 (trước đó: Điểu Tháp Thâm Lâm, vì "tháp + thâm lâm" đọc như rừng); Claude chọn tên mới, chờ owner xác nhận |
| `tower_region_secret_floor` | Bí cảnh Tháp Chim — tầng | **Điểu Tháp Mật Tầng** |  |
| `immortal_maze_main_maze` | Mê Thành Bất Tử | **Mê Thành Bất Tử** | giữ nguyên, đã hợp style |
| `immortal_maze_floor` | Tầng | **Bất Tử Mê Tầng** | tên nguồn quá chung |
| `immortal_maze_secret_floor` | Bí cảnh Mê Thành — tầng | **Bất Tử Mật Tầng** |  |
| `guild_fortress` | Pháo đài bang hội | **Thành Lũy Bang Hội** | hub dịch vụ bang |
| `guild_treasury` | Kho bạc | **Ngân Khố Bang** |  |
| `guild_warehouse` | Nhà kho | **Kho Vật Tư Bang** |  |
| `guild_barracks` | Doanh trại | **Doanh Trại Bang** |  |
| `guild_shop` | Cửa hàng | **Quầy Hàng Bang** |  |
| `guild_pet_stable` | Chuồng thú | **Chuồng Linh Thú** |  |
| `guild_battlefield_main_field` | Chiến trường bang hội | **Chiến Địa Kết Minh** |  |
| `maya_floor_01` | Maya — tầng 1 | **Điện Thờ Maya · Tầng I** | nhãn game: 'Điện thờ Maya' (Lv25–30) |
| `dungeon_floor_01` | Ngục ngầm — tầng 1 | **Địa Lao · Tầng I** |  |
| `chaos_arena_main_field` | Chiến Trường Hỗn Loạn | **Đấu Trường Hỗn Mang** |  |
| `team_arena_main_field` | Chiến trường tổ đội | **Đấu Trường Tổ Đội** |  |
| `wolf_sheep_waiting_hall` | Sảnh chờ | **Sảnh Chờ Sói–Cừu** |  |
| `wolf_sheep_sheep_house` | Nhà Cừu | **Nhà Cừu** |  |
| `wolf_sheep_sheep_pen` | Chuồng Cừu | **Chuồng Cừu** |  |
| `wolf_sheep_middle_field` | Khu vực giữa | **Bãi Tranh Đoạt** |  |
| `wolf_sheep_wolf_pen` | Chuồng Sói | **Chuồng Sói** |  |
| `wolf_sheep_wolf_house` | Nhà Sói | **Nhà Sói** |  |

## Câu hỏi để debate
1. ~~Style JRPG~~ → **Owner xác nhận đúng ý** (2026-10-14). Cột tên đọc kiểu Nhật: chưa yêu cầu.
2. ~~Phòng giống nhau~~ → **Owner đã chọn B: tên thơ riêng cho từng phòng** (2026-10-14).
3. ~~Tên đã có nghĩa sẵn~~ → **Owner cho phép đổi nếu cần để thống nhất**; chưa có đề xuất đổi ngoài bảng.
4. Minigame Sói–Cừu và khu dịch vụ bang: để tên chức năng đơn giản hay thơ hóa?
