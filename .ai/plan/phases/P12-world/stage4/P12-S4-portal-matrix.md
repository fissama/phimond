# P12 Stage 4 — Ma trận portal (sinh tự động, nguồn APK 3.2 + 8.4 trong Stage 1)

45 portal chạm phạm vi (nguồn hoặc đích). Tên VI là tên APK (`display_name_vi`), **không phải** tên owner; tên owner xem `P12-world-names-master.md`.

Cột *Đích/nguồn ngoài phạm vi* = portal đi ra/vào map ngoài 17 map, giữ để thấy dependency.


## city_square — Quảng trường thành phố

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_008` | NEXTMAP | city_palace_gate |  | 9.89, -0.95 | 27.00, 0.00, 0.00 |
| `city_portal_011` | NEXTMAP | city_market |  | -13.12, -1.23 | 82.00, -1.36, 0.00 |

## city_market — Chợ thành phố

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_001` | NEXTMAP | city_square |  | 83.95, -1.24 | -11.12, -1.00, 0.00 |
| `city_portal_009` | NEXTMAP | city_palace_gate |  | 61.12, -1.26 | 42.50, -1.36, 0.00 |

## city_royal_palace — Cung điện Hoàng gia

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_003` | NEXTMAP | city_activity_hall |  | 25.50, 15.89 | 7.00, 16.00, 0.00 |
| `city_portal_007` | NEXTMAP | city_palace_gate |  | 35.53, 14.61 | 33.00, -1.36, 0.00 |

## city_palace_gate — Cổng Hoàng cung

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_002` | NEXTMAP | city_market |  | 44.63, -1.54 | 63.13, -1.36, 0.00 |
| `city_portal_004` | NEXTMAP | city_square |  | 24.90, -1.17 | 8.55, 0.00, 0.00 |
| `city_portal_006` | NEXTMAP | city_royal_palace |  | 34.47, 0.00 | 35.00, 16.00, 0.00 |

## city_pet_room — Căn phòng poke

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_014` | NEXTMAP | city_farm |  | -0.37, -15.73 | -1.00, -26.50, 0.00 |

## city_farm — Nông trại

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_010` | NEXTMAP | city_square |  | -5.18, -27.86 | 0.00, 0.00, 0.00 |
| `city_portal_013` | NEXTMAP | city_pet_room |  | 1.33, -25.55 | -3.00, -15.00, 0.00 |

## city_deathmatch_arena — Đấu trường sinh tử

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_005` | NEXTMAP | city_square |  | 35.42, 36.98 | 0.00, 0.00, 0.00 |

## city_activity_hall — Sảnh hoạt động

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `city_portal_012` | NEXTMAP | city_royal_palace |  | 9.37, 15.96 | 27.00, 16.00, 0.00 |

## emerald_forest_main_woods — Rừng Bibo

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `emerald_forest_portal_002` | NEXTMAP | emerald_forest_deep_woods |  | 19.31, 0.42 | 37.30, 0.92, 0.00 |

## emerald_forest_deep_woods — Rừng sâu

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `emerald_forest_portal_001` | NEXTMAP | emerald_forest_main_woods |  | 35.62, 0.52 | 17.00, 1.00, 0.00 |
| `emerald_forest_portal_003` | NEXTSCENE | city_palace_gate |  | 58.40, 0.52 | 27.00, 0.00, 0.00 |

## treasure_beach_fishermen_beach — Bãi biển ngư dân

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `treasure_beach_portal_001` | NEXTMAP | treasure_beach_deep_sea |  | -0.47, -2.24 | -9.67, -12.32, 0.00 |
| `treasure_beach_portal_004` | NEXTMAP | treasure_beach_east_beach |  | 9.30, 0.42 | 21.92, 2.07, 0.00 |
| `treasure_beach_portal_006` | NEXTMAP | treasure_beach_west_beach |  | -9.77, -0.02 | -24.61, -0.10, 0.00 |

## treasure_beach_east_beach — Phía đông bãi biển

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `treasure_beach_portal_003` | NEXTMAP | treasure_beach_fishermen_beach |  | 20.80, 0.47 | 7.18, 0.68, 0.00 |
| `treasure_beach_portal_008` | NEXTSCENE | city_square |  | 42.35, 0.77 | 0.00, 0.00, 0.00 |

## treasure_beach_deep_sea — Biển sâu

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `treasure_beach_portal_002` | NEXTMAP | treasure_beach_fishermen_beach |  | -9.90, -10.80 | 0.00, 0.00, 0.00 |

## treasure_beach_west_beach — Phía tây bãi biển

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `treasure_beach_portal_005` | NEXTMAP | treasure_beach_fishermen_beach |  | -22.30, 0.00 | -7.83, 0.07, 0.00 |
| `treasure_beach_portal_009` | NEXTMAP | treasure_beach_prosperity_island |  | -26.70, -2.20 | -24.71, -12.13, 0.00 |

## treasure_beach_prosperity_island — Đảo phú quý

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `treasure_beach_portal_007` | NEXTMAP | treasure_beach_west_beach |  | -22.40, -12.30 | -25.09, -0.38, 0.00 |

## summoning_hall_main_hall — Sảnh vẫy gọi

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `summoning_hall_portal_001` | NEXTSCENE | emerald_forest_main_woods |  | 14.65, -0.34 | 0.00, 0.00, 0.00 |

## desert_entrance — Lối vào sa mạc

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `desert_portal_010` | NEXTSCENE | city_square |  | 43.08, 0.96 | 0.00, 0.00, 0.00 |

## windrock_mountain_stone_bridge — Cầu Đá trên núi

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `windrock_mountain_portal_010` | NEXTSCENE | city_square |  | -41.89, 0.54 | 0.00, 0.00, 0.00 |

## nightmare_island_east_magic_island — Phía đông Đảo Phép thuật

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `nightmare_island_portal_010` | NEXTSCENE | city_square |  | 41.86, 0.37 | 0.00, 0.00, 0.00 |

## tomb_region_resentment_path — Con đường phẫn uất

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `tomb_region_portal_016` | NEXTSCENE | city_square |  | -72.29, 0.54 | 0.00, 0.00, 0.00 |

## crossroads_unnamed_area_01 — Khu vực chưa đặt tên 01

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `crossroads_portal_010` | NEXTSCENE | city_square |  | -10.19, 0.18 | 0.00, 0.00, 0.00 |

## astral_realm_spacetime_rift — Khe nứt không thời gian

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `astral_realm_portal_013` | NEXTSCENE | middle_corridor_main_hall |  | -40.44, -0.64 | 0.00, 0.00, 0.00 |

## ancient_ruins_unnamed_area_01 — Khu vực chưa đặt tên 01

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `ancient_ruins_portal_011` | NEXTSCENE | middle_corridor_main_hall |  | -9.64, 0.10 | 0.00, 0.00, 0.00 |

## ghost_castle_gate — Cổng lâu đài ma

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `ghost_castle_portal_005` | NEXTSCENE | middle_corridor_main_hall |  | -9.97, -0.17 | 0.00, 0.00, 0.00 |

## world_tree_gate — Cổng cây thế giới

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `world_tree_portal_005` | NEXTSCENE | middle_corridor_main_hall |  | -9.97, -0.17 | 0.00, 0.00, 0.00 |

## tower_region_main_tower — Tháp Chim

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `tower_region_portal_005` | NEXTSCENE | middle_corridor_main_hall |  | -9.97, -0.17 | 0.00, 0.00, 0.00 |

## immortal_maze_main_maze — Mê Thành Bất Tử

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `immortal_maze_portal_005` | NEXTSCENE | middle_corridor_main_hall |  | -9.97, -0.17 | 0.00, 0.00, 0.00 |

## guild_fortress — Pháo đài bang hội

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `guild_portal_005` | NEXTSCENE | city_royal_palace |  | -12.31, -0.95 | 40.00, 17.00, 0.00 |

## guild_battlefield_main_field — Chiến trường bang hội

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `guild_battlefield_portal_001` | NEXTSCENE | city_square |  | 14.65, -0.34 | 0.00, 0.00, 0.00 |

## maya_floor_01 — Maya — tầng 1

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `maya_portal_001` | NEXTSCENE | city_square |  | -9.88, 0.27 | 0.00, 0.00, 0.00 |

## dungeon_floor_01 — Ngục ngầm — tầng 1

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `dungeon_portal_001` | NEXTSCENE | city_square |  | -9.88, 0.27 | 0.00, 0.00, 0.00 |

## chaos_arena_main_field — Chiến Trường Hỗn Loạn

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `chaos_arena_portal_001` | NEXTSCENE | city_square |  | 14.65, -0.34 | 0.00, 0.00, 0.00 |

## team_arena_main_field — Chiến trường tổ đội

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `team_arena_portal_001` | NEXTSCENE | city_square |  | 14.65, -0.34 | 0.00, 0.00, 0.00 |

## wolf_sheep_waiting_hall — Sảnh chờ

| Portal | Chế độ | Đích | Ngoài phạm vi? | Vị trí cửa (x,y) | Vector (điểm xuất hiện đích) |
|---|---|---|---|---|---|
| `wolf_sheep_portal_005` | NEXTSCENE | city_square |  | -12.31, -0.95 | 0.00, 0.00, 0.00 |
