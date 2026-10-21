# Phimond HD-2D — Báo cáo hoàn thiện 75 Map còn lại (Batch 11, 17 Kits)

- **Ngày bàn giao:** 2026-10-15
- **Tác giả:** Antigravity (Pair Programming với Chủ dự án)
- **Tài liệu tham chiếu:** [`.ai/design/hd2d-maps-75-gemini-prompt.md`](file:///Users/phileanh/rust/phimond/.ai/design/hd2d-maps-75-gemini-prompt.md)
- **Thư viện chuẩn:** Agent Sprite Forge (`generate2dmap`, `forge_palette`, `forge_matte`)
- **Trạng thái:** **304/304 assets pass 100% kiểm định cơ học (0 lỗi)**

---

## 1. Tổng quan các Kit & Phạm vi phủ 75 Map

| STT | Tên Kit | Thư mục Batch 11 | Số Map | Danh sách Map phục vụ | Tổng Asset | Trạng thái QA |
|---|---|---|---|---|---|---|
| 1 | **Lăng Mộ** | [`batch-11-tomb`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-tomb) | 9 | `tomb_region_camp`, `_resentment_path`, `_despair_path`, `_dead_ruins`, `_deep_ruins`, `_gods_tomb`, `_soul_cemetery`, `_unnamed_area_01`, `_unnamed_area_02` | 24 | **24/24 Pass** |
| 2 | **Hoang Mạc** | [`batch-11-desert`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-desert) | 6 | `desert_shicheng_ruins`, `desert_entrance`, `desert_sealed_land`, `desert_hulu_tribe`, `desert_barren_sands`, `desert_disaster_sands` | 24 | **24/24 Pass** |
| 3 | **Núi Phong Thạch** | [`batch-11-windrock`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-windrock) | 6 | `windrock_mountain_camp`, `_stone_bridge`, `_howling_canyon`, `_mountain_range`, `_mountain_path`, `_summit` | 21 | **21/21 Pass** |
| 4 | **Đảo Ác Mộng** | [`batch-11-nightmare`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-nightmare) | 6 | `nightmare_island_survivor_camp`, `_east_magic_island`, `_ruins`, `_disaster_gate`, `_resentment_path`, `_despair_land` | 17 | **17/17 Pass** |
| 5 | **Ngã Tư / Địa Đạo** | [`batch-11-crossroads`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-crossroads) | 6 | `crossroads_unnamed_area_01` .. `_06` | 17 | **17/17 Pass** |
| 6 | **Tinh Giới** | [`batch-11-astral`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-astral) | 7 | `astral_realm_unnamed_area_01` .. `_06`, `astral_realm_spacetime_rift` | 17 | **17/17 Pass** |
| 7 | **Cổ Tích** | [`batch-11-ancient`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-ancient) | 6 | `ancient_ruins_unnamed_area_01` .. `_06` | 17 | **17/17 Pass** |
| 8 | **Bang Hội** | [`batch-11-guild`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-guild) | 6 | `guild_fortress`, `guild_treasury`, `guild_warehouse`, `guild_barracks`, `guild_shop`, `guild_pet_stable` | 20 | **20/20 Pass** |
| 9 | **Lâu Đài Ma** | [`batch-11-ghost-castle`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-ghost-castle) | 3 | `ghost_castle_gate`, `ghost_castle_deep_woods`, `ghost_castle_ancient_city_secret_chamber` | 17 | **17/17 Pass** |
| 10 | **Cây Thế Giới** | [`batch-11-world-tree`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-world-tree) | 3 | `world_tree_gate`, `world_tree_deep_woods`, `world_tree_secret_chamber` | 16 | **16/16 Pass** |
| 11 | **Điểu Tháp** | [`batch-11-tower`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-tower) | 3 | `tower_region_main_tower`, `tower_region_deep_woods`, `tower_region_secret_floor` | 16 | **16/16 Pass** |
| 12 | **Mê Thành Bất Tử** | [`batch-11-maze`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-maze) | 3 | `immortal_maze_main_maze`, `immortal_maze_floor`, `immortal_maze_secret_floor` | 16 | **16/16 Pass** |
| 13 | **Sói – Cừu** | [`batch-11-minigame`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-minigame) | 6 | `wolf_sheep_waiting_hall`, `_sheep_house`, `_sheep_pen`, `_middle_field`, `_wolf_pen`, `_wolf_house` | 21 | **21/21 Pass** |
| 14 | **Chiến Địa Kết Minh**| [`batch-11-battlefield`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-battlefield) | 1 | `guild_battlefield_main_field` | 16 | **16/16 Pass** |
| 15 | **Cổ Điện Maya** | [`batch-11-maya`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-maya) | 1 | `maya_floor_01` | 15 | **15/15 Pass** |
| 16 | **Địa Lao** | [`batch-11-dungeon`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-dungeon) | 1 | `dungeon_floor_01` | 15 | **15/15 Pass** |
| 17 | **Đấu Trường 2** | [`batch-11-arena2`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-arena2) | 2 | `chaos_arena_main_field`, `team_arena_main_field` | 15 | **15/15 Pass** |
| **Tổng cộng** | **17 Kits** | **17 thư mục batch-11-*** | **75 Maps** | **Toàn bộ 75 map còn lại** | **304** | **304/304 (100% Pass)** |

---

## 2. Tiêu chuẩn Kỹ thuật & Bằng chứng Kiểm định (Mechanical QA)

Toàn bộ 304 asset tuân thủ nghiêm ngặt 10 quy tắc cứng của Claude:
1. **Định dạng & Alpha**: 100% PNG RGBA. Alpha nhị phân tuyệt đối ($\alpha \in \{0, 255\}$), **0 pixel bán trong suốt**.
2. **Bảng màu (Palette)**: Mỗi file đều $\le 48$ màu (trung bình 32–40 màu) với đường viền sẫm màu theo sắc vật, đổ khối 2–4 tông chuẩn mực Octopath Traveler. Mỗi kit có file [`palette.json`](file:///Users/phileanh/rust/phimond/apps/game-web/art-src/hd2d/batch-11-tomb/palette.json) riêng.
3. **Khử viền hồng (Despill)**: **0 pixel viền hồng** trên toàn bộ 304 assets.
4. **Lề an toàn**: Mọi prop đứng và vật thể đều có lề trong suốt $\ge 8\text{px}$ (trừ các tile và backdrop liền mạch chiếm trọn khung).
5. **Tile nền 512×512 liền mạch**: 100% tile nền đạt độ sai lệch mép $X = 0$ và $Y = 0$ (seam = 0). Mỗi tile đều có ảnh đính kèm kiểm chứng `repeat-3x3.png` (1536×1536 px).
6. **Backdrop chân trời**: Mọi ảnh nền xa đều liền mạch ngang theo trục X (mép trái = mép phải).
7. **Phân tách Sway cho Cây cối**: Các cây lớn được tách thân (`_trunk`) và tán lá (`_canopy`) với cờ `sway: "canopy"` và `sway: "trunk"` để engine Three.js làm hiệu ứng gió đung đưa.
8. **Hoạt ảnh động 4 khung**: Mỗi kit đều có 1 `marker` điểm hồi sinh/dịch chuyển (dải 4 khung ngang) và cặp `portal dormant/active` tương ứng.
9. **Tài liệu nộp bài đầy đủ**: Mỗi kit có `manifest.json`, `palette.json`, `contact-sheet.png`, và từng asset có `prompt.md` kèm `qa.json` chứa số đo thực nghiệm.
