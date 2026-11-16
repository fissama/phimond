# Các map đang chờ hoàn thiện — snapshot hàng đợi 2026-10-24, cập nhật 2026-10-29

Phần bảng hàng đợi gốc gồm 14 kit / 54 map; forest/city/beach/ship dùng các batch cũ, không suy ra thiếu asset chỉ vì không có batch-11 tương ứng. Đồng bộ Claude ngày 29/10: desert (98), windrock (32 tại lúc review), nightmare (67), crossroads (59), tomb (11). Cập nhật Codex ngày 30/10: desert 98, windrock 82, nightmare 67, crossroads 62, tomb 76; art gate batch-11 quét 411 asset, 0 lỗi/0 cảnh báo. Không kit nào được duyệt. Claude xem floor/prop của 4 kit nhưng chưa xem backdrop; kết luận backdrop trong báo cáo theo log Codex. Số lượng art không đồng nghĩa map đã dựng.

Review focus hiện tại: **nightmare, crossroads, windrock và tomb**. Mỗi phiên chỉ làm một kit theo Master v2; không có tác vụ nền tự chạy. Mục tiêu full map cần cả asset, landmark riêng, dựng cảnh và kiểm collision/portal ở bước được owner giao; art worker hiện chỉ tạo asset nháp.

## Tình trạng 5 kit đã review (2026-10-29)

| Kit | Map | Asset | Việc còn lại |
|---|---:|---:|---|
| desert | 6 | 98 | Dùng dựng thử; chưa duyệt. Backdrop chưa được Claude xem; boulder/backdrop-far còn vấn đề theo log. |
| windrock | 6 | 82 | Cập nhật 30/10: checklist candidate đủ asset dùng chung, gồm edge-01..03; landmark map tái dùng prop có đối chiếu. Chờ Claude/owner review. Bảng 74 dòng là inventory Gemini cũ. |
| nightmare | 6 | 67 | Edge-02/03 và far-01/02 có candidate mới, gate sạch; backdrop chưa Claude xem. Landmark-02 rows cần đối chiếu ảnh nguồn; repeat sàn lộ chu kỳ. |
| crossroads | 6 | 62 | Edge-01..03 và backdrop-far-01/02 có; gate sạch. Claude chưa xem backdrop; floor repeat lộ chu kỳ; map chưa dựng. |
| tomb | 9 | 76 | Candidate GPT redraw đầy đủ checklist, gate sạch; chưa owner duyệt, backdrop repeat và map compositions chờ review. |

| Kit | Map | Tên | Trạng thái |
|---|---|---|---|
| nightmare | `nightmare_island_survivor_camp` | Trại Tàn Sinh | Kit có 67 asset nhưng còn edge/backdrop; map chưa dựng |
| nightmare | `nightmare_island_east_magic_island` | Đông Đảo Huyền Thuật | Kit có 67 asset nhưng còn edge/backdrop; map chưa dựng |
| nightmare | `nightmare_island_ruins` | Phế Tích Cổ Thành | Kit có 67 asset nhưng còn edge/backdrop; map chưa dựng |
| nightmare | `nightmare_island_disaster_gate` | Cổng Tai Kiếp | Kit có 67 asset nhưng còn edge/backdrop; map chưa dựng |
| nightmare | `nightmare_island_resentment_path` | Oán Linh Hải Đạo | Kit có 67 asset nhưng còn edge/backdrop; map chưa dựng |
| nightmare | `nightmare_island_despair_land` | Tuyệt Vọng Hải Địa | Kit có 67 asset nhưng còn edge/backdrop; map chưa dựng |
| crossroads | `crossroads_unnamed_area_01` | Cổng Địa Đạo Lam Dạ | Kit có 59 asset; còn edge/backdrop và cần redraft floor repeat; map chưa dựng |
| crossroads | `crossroads_unnamed_area_02` | Hành Lang Rêu Biếc | Kit có 59 asset; còn edge/backdrop và cần redraft floor repeat; map chưa dựng |
| crossroads | `crossroads_unnamed_area_03` | Đoạn Thủy Quang | Kit có 59 asset; còn edge/backdrop và cần redraft floor repeat; map chưa dựng |
| crossroads | `crossroads_unnamed_area_04` | Ngã Ba Đêm Xanh | Kit có 59 asset; còn edge/backdrop và cần redraft floor repeat; map chưa dựng |
| crossroads | `crossroads_unnamed_area_05` | Hốc San Hô Tím | Kit có 59 asset; còn edge/backdrop và cần redraft floor repeat; map chưa dựng |
| crossroads | `crossroads_unnamed_area_06` | Đáy Địa Đạo | Kit có 59 asset; còn edge/backdrop và cần redraft floor repeat; map chưa dựng |
| astral | `astral_realm_unnamed_area_01` | Tử Vân Lâm | Chưa bắt đầu |
| astral | `astral_realm_spacetime_rift` | Thời Không Liệt Khích | Chưa bắt đầu |
| astral | `astral_realm_unnamed_area_02` | Lối Mây Tím | Chưa bắt đầu |
| astral | `astral_realm_unnamed_area_03` | Bờ Hồ Vân Ảnh | Chưa bắt đầu |
| astral | `astral_realm_unnamed_area_04` | Hốc Cổ Thụ | Chưa bắt đầu |
| astral | `astral_realm_unnamed_area_05` | Rừng Hoàng Hôn | Chưa bắt đầu |
| astral | `astral_realm_unnamed_area_06` | Tận Cùng Thời Không | Chưa bắt đầu |
| ancient | `ancient_ruins_unnamed_area_01` | Tiền Sảnh Ngọc Lục | Chưa bắt đầu |
| ancient | `ancient_ruins_unnamed_area_02` | Phòng Tượng Cổ | Chưa bắt đầu |
| ancient | `ancient_ruins_unnamed_area_03` | Phòng Tinh Thạch | Chưa bắt đầu |
| ancient | `ancient_ruins_unnamed_area_04` | Hành Lang Thạch Vệ | Chưa bắt đầu |
| ancient | `ancient_ruins_unnamed_area_05` | Thâm Sảnh Ngọc Lục | Chưa bắt đầu |
| ancient | `ancient_ruins_unnamed_area_06` | Tận Điện Cổ Tích | Chưa bắt đầu |
| ghost_castle | `ghost_castle_gate` | Cổng U Lâu | Chưa bắt đầu |
| ghost_castle | `ghost_castle_deep_woods` | U Linh Cổ Thành | Chưa bắt đầu |
| ghost_castle | `ghost_castle_ancient_city_secret_chamber` | Mật Thất Cổ Thành | Chưa bắt đầu |
| world_tree | `world_tree_gate` | Thế Thụ Môn | Chưa bắt đầu |
| world_tree | `world_tree_deep_woods` | Thế Thụ Thâm Lâm | Chưa bắt đầu |
| world_tree | `world_tree_secret_chamber` | Mật Thất Thế Thụ | Chưa bắt đầu |
| tower | `tower_region_main_tower` | Điểu Tháp | Chưa bắt đầu |
| tower | `tower_region_deep_woods` | Vân Tiêu Thiên Tầng | Chưa bắt đầu |
| tower | `tower_region_secret_floor` | Điểu Tháp Mật Tầng | Chưa bắt đầu |
| maze | `immortal_maze_main_maze` | Trường Sinh Mê Thành | Chưa bắt đầu |
| maze | `immortal_maze_floor` | Bất Tử Mê Tầng | Chưa bắt đầu |
| maze | `immortal_maze_secret_floor` | Bất Tử Mật Tầng | Chưa bắt đầu |
| guild | `guild_fortress` | Thành Lũy Bang Hội | Chưa bắt đầu |
| guild | `guild_treasury` | Ngân Khố Bang | Chưa bắt đầu |
| guild | `guild_warehouse` | Kho Vật Tư Bang | Chưa bắt đầu |
| guild | `guild_barracks` | Doanh Trại Bang | Chưa bắt đầu |
| guild | `guild_shop` | Quầy Hàng Bang | Chưa bắt đầu |
| guild | `guild_pet_stable` | Chuồng Linh Thú | Chưa bắt đầu |
| battlefield | `guild_battlefield_main_field` | Chiến Địa Kết Minh | Chưa bắt đầu |
| maya | `maya_floor_01` | Cổ Điện Tế Lễ · Tầng I | Chưa bắt đầu |
| dungeon | `dungeon_floor_01` | Địa Lao · Tầng I | Chưa bắt đầu |
| arena2 | `chaos_arena_main_field` | Đấu Trường Hỗn Mang | Chưa bắt đầu |
| arena2 | `team_arena_main_field` | Đấu Trường Tổ Đội | Chưa bắt đầu |
| minigame | `wolf_sheep_waiting_hall` | Sảnh Đối Quyết Lang Dương | Chưa bắt đầu |
| minigame | `wolf_sheep_sheep_house` | Dương Xá | Chưa bắt đầu |
| minigame | `wolf_sheep_sheep_pen` | Dương Lan | Chưa bắt đầu |
| minigame | `wolf_sheep_middle_field` | Bãi Tranh Đoạt | Chưa bắt đầu |
| minigame | `wolf_sheep_wolf_pen` | Lang Huyệt | Chưa bắt đầu |
| minigame | `wolf_sheep_wolf_house` | Lang Sào | Chưa bắt đầu |

Quy trình và phong cách: [README](README.md), [Master v2](../gpt-redo/00-master-v2.md). Chỉ cập nhật ✅ Vẽ khi final đã được xem 4×; Duyệt do Claude/owner.
