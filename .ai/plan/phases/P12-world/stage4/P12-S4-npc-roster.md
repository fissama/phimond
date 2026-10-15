# P12 Stage 4 — Roster NPC đề xuất (nháp, chờ owner duyệt)

106 NPC + 1 hòm thư (vật thể) trong 75 map (17 map phạm vi + 58 map của 11 vùng mở rộng 2026-10-15): 40 gắn vào vị trí NPC gốc APK 3.2 (44 slot, chỉ 17 map đầu), 67 MỚI (cần đặt vị trí khi vẽ HD-2D). Sinh bằng `gen_npc_roster.py`; tên không dùng tên NPC trong APK.

**Lưu ý:** tên object trong APK (`thaythuoc`, `TTTD`, `guild`…) là tên prefab, chưa đủ tin cậy để suy vai trò; vai trò ở đây là **thiết kế đề xuất**, chỉ dùng vị trí gốc làm sườn. Tọa độ APK chỉ là bản phác, bản vẽ HD-2D sẽ đặt lại.

Hạng: **main** = chuỗi nhiệm vụ chính (P04 onboarding; P17 viết truyện sau), **free** = NPC tự do/nhiệm vụ phụ (P18), **service** = dịch vụ.

## Ma trận phủ theo map

| Map | main | free | heal | learn | shop | khác |
|---|---|---|---|---|---|---|
| `summoning_hall_main_hall` | — | 1 | — | — | — | events |
| `emerald_forest_main_woods` | 1 | 1 | 1 | 1 | 1 | — |
| `emerald_forest_deep_woods` | — | 2 | — | — | — | — |
| `city_palace_gate` | 1 | — | — | — | — | guild |
| `city_square` | 1 | 2 | 1 | 2 | — | arena, exchange, mailbox, quest_board, teleport, warehouse |
| `city_market` | — | 1 | — | — | 3 | — |
| `city_royal_palace` | 1 | — | 1 | — | — | guild, story |
| `city_activity_hall` | — | 1 | — | — | — | events, reward |
| `city_pet_room` | 2 | — | 1 | — | 1 | appraise, bless, breed, hatch, recipe, strengthen |
| `city_farm` | — | — | — | — | — | storage |
| `city_deathmatch_arena` | 1 | 1 | 1 | — | — | arena |
| `treasure_beach_fishermen_beach` | 1 | 1 | 1 | 1 | 1 | — |
| `treasure_beach_east_beach` | — | 2 | — | — | — | — |
| `treasure_beach_west_beach` | — | 2 | — | — | — | — |
| `treasure_beach_deep_sea` | — | 1 | — | — | — | — |
| `treasure_beach_prosperity_island` | — | 1 | — | — | — | — |
| `middle_corridor_main_hall` | 1 | 1 | 1 | 1 | 1 | smith, story, teleport |
| `desert_shicheng_ruins` | 1 | 1 | 1 | 1 | 1 | — |
| `desert_entrance` | — | 1 | — | — | — | — |
| `desert_sealed_land` | — | — | — | — | — | — |
| `desert_hulu_tribe` | — | 1 | — | — | — | — |
| `desert_barren_sands` | — | 1 | — | — | — | — |
| `desert_disaster_sands` | — | — | — | — | — | — |
| `windrock_mountain_camp` | 1 | 1 | 1 | 1 | 1 | — |
| `windrock_mountain_stone_bridge` | — | 1 | — | — | — | — |
| `windrock_mountain_howling_canyon` | — | — | — | — | — | — |
| `windrock_mountain_mountain_range` | — | 1 | — | — | — | — |
| `windrock_mountain_mountain_path` | — | 1 | — | — | — | — |
| `windrock_mountain_summit` | — | 1 | — | — | — | — |
| `nightmare_island_survivor_camp` | 1 | 1 | 1 | 1 | 1 | — |
| `nightmare_island_east_magic_island` | — | 1 | — | — | — | — |
| `nightmare_island_ruins` | — | 1 | — | — | — | — |
| `nightmare_island_disaster_gate` | — | — | — | — | — | — |
| `nightmare_island_resentment_path` | — | 1 | — | — | — | — |
| `nightmare_island_despair_land` | — | 1 | — | — | — | — |
| `tomb_region_camp` | 1 | 1 | 1 | 1 | 1 | — |
| `tomb_region_resentment_path` | — | 1 | — | — | — | — |
| `tomb_region_despair_path` | — | — | — | — | — | — |
| `tomb_region_dead_ruins` | — | — | — | — | — | — |
| `tomb_region_deep_ruins` | — | — | — | — | — | — |
| `tomb_region_gods_tomb` | — | 1 | — | — | — | — |
| `tomb_region_soul_cemetery` | — | 2 | — | — | — | — |
| `tomb_region_unnamed_area_01` | — | — | — | — | — | — |
| `tomb_region_unnamed_area_02` | — | — | — | — | — | — |
| `crossroads_unnamed_area_01` | 1 | — | 1 | 1 | 1 | — |
| `crossroads_unnamed_area_02` | — | — | — | — | — | — |
| `crossroads_unnamed_area_03` | — | 1 | — | — | — | — |
| `crossroads_unnamed_area_04` | — | 1 | — | — | — | — |
| `crossroads_unnamed_area_05` | — | 1 | — | — | — | — |
| `crossroads_unnamed_area_06` | — | — | — | — | — | — |
| `astral_realm_unnamed_area_01` | 1 | — | 1 | 1 | 1 | — |
| `astral_realm_spacetime_rift` | — | — | — | — | — | — |
| `astral_realm_unnamed_area_02` | — | 1 | — | — | — | — |
| `astral_realm_unnamed_area_03` | — | — | — | — | — | — |
| `astral_realm_unnamed_area_04` | — | — | — | — | — | — |
| `astral_realm_unnamed_area_05` | — | 1 | — | — | — | — |
| `astral_realm_unnamed_area_06` | — | — | — | — | — | — |
| `ancient_ruins_unnamed_area_01` | 1 | — | 1 | 1 | 1 | — |
| `ancient_ruins_unnamed_area_02` | — | 1 | — | — | — | — |
| `ancient_ruins_unnamed_area_03` | — | — | — | — | — | — |
| `ancient_ruins_unnamed_area_04` | — | 1 | — | — | — | — |
| `ancient_ruins_unnamed_area_05` | — | 1 | — | — | — | — |
| `ancient_ruins_unnamed_area_06` | — | — | — | — | — | — |
| `ghost_castle_gate` | 1 | — | 1 | 1 | 1 | — |
| `ghost_castle_deep_woods` | — | — | — | — | — | — |
| `ghost_castle_ancient_city_secret_chamber` | — | — | — | — | — | — |
| `world_tree_gate` | 1 | — | 1 | 1 | 1 | — |
| `world_tree_deep_woods` | — | — | — | — | — | — |
| `world_tree_secret_chamber` | — | — | — | — | — | — |
| `tower_region_main_tower` | 1 | — | 1 | 1 | 1 | — |
| `tower_region_deep_woods` | — | 1 | — | — | — | — |
| `tower_region_secret_floor` | — | — | — | — | — | — |
| `immortal_maze_main_maze` | 1 | — | 1 | 1 | 1 | — |
| `immortal_maze_floor` | — | 1 | — | — | — | — |
| `immortal_maze_secret_floor` | — | — | — | — | — | — |

## summoning_hall_main_hall (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Triệu Linh Sư Mira** (`summoner_mira`) | free | events, free | -5.32, 0.36 | Npc | Map sự kiện (owner 2026-10-15): NPC đánh dấu phụ / sự kiện hằng ngày. Hướng dẫn chọn bệ nhận pet 1★ chuyển cho phase quest quyết. Nguồn có 4 biến thể ẩn cùng vị trí. |

## emerald_forest_main_woods (4)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Kiểm Lâm Lio** (`forest_guide`) | main | quest, heal | 4.78, 1.59 | Lisa | NPC runtime sẵn có (`forest_guide`). Chuỗi P04: di chuyển, nói chuyện, chiến đấu, bắt pet. Gần điểm xuất hiện. |
| **Tiểu Thương Wen** (`bia_shop`) | service | shop | 15.13, 1.46 | Shop | Tạp hóa cơ bản (thuốc, bẫy). |
| **Thợ Săn Rowan** (`bia_skill`) | service | learn | 11.95, 1.39 | Skill | Dạy kỹ năng bậc 1 (Lv1–10). |
| **Người Hái Nấm Tuli** (`bia_free`) | free | free | 8.39, 1.36 | Npc | Nhiệm vụ phụ nhẹ (thu thập). |

## emerald_forest_deep_woods (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Gác Rừng Mero** (`sau_guard`) | free | free | 45.18, 1.41 | Vesa | Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15), không hồi máu/cửa hàng. Bước đi Hoàng Môn lần đầu do phase quest đặt NPC. |
| **Cụ Rêu Tamo** (`sau_free`) | free | free | MỚI: chưa đặt | — | MỚI. Cụ già giữ rừng, truyện nền. |

## city_palace_gate (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thị Vệ Trưởng Karn** (`gate_captain`) | main | quest | MỚI: chưa đặt | — | MỚI. Tiếp nhận người chơi lần đầu tới Hoàng Môn theo nhiệm vụ, chỉ đường về Quảng Trường. |
| **Sứ Giả Bang Hội Ryo** (`gate_guild`) | service | guild | 30.91, -0.16 | guild (1) | Tư vấn/dẫn vào khu bang hội. |

## city_square (10)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Huấn Luyện Viên Elin** (`trainer_elin`) | main | quest, learn | 0.12, 0.6 | thaythuoc | NPC runtime sẵn có (`trainer`). Trung tâm chuỗi P04 tại thành. Runtime hiện còn shop+heal; thiết kế chuyển sang Thương Phố/Selka. |
| **Y Sư Selka** (`sq_healer`) | service | heal | -11.23, 0.32 | thaythuoc (3) | Hồi máu/MP cho pet toàn đội. |
| **Sư Phụ Kỹ Năng Doran** (`sq_skill`) | service | learn | -9.51, 0.04 | thaythuoc (5) | Dạy kỹ năng bậc 2 (Lv10–40). Phân trường phái theo race: P13 quyết. |
| **Người Kể Chuyện Hanae** (`sq_free`) | free | free | -8.23, -2.79 | thaythuoc (2) | Truyện nền thành phố, nhiệm vụ phụ. |
| **Trụ Sư Orsa** (`sq_pillar`) | service | teleport | 6.28, -1.66 | TTTD | Vận hành trụ đá (U1). Menu chỉ hiện vùng đủ cấp. Tên nguồn TTTD + gợi ý loading "Thủy tinh dịch chuyển phía Đông Quảng Trường" cho thấy đây rất có thể là trụ gốc. |
| **Đài Sứ Rena** (`sq_arena`) | service | arena | -2.44, -2.09 | TTTD (2) | Đăng ký Huyết Chiến Đài theo bậc. |
| **Quản Sự Nhiệm Vụ Tessa** (`sq_board`) | free | free, quest_board | -6.12, -0.06 | TTTD (3) | Bảng nhiệm vụ phụ/hằng ngày (P08/P18). |
| **Chủ Sàn Giao Dịch Ketra** (`sq_exchange`) | service | exchange | MỚI: chưa đặt | — | MỚI (owner 2026-10-15). Sàn giao dịch giữa người chơi. |
| **Thủ Kho Odan** (`sq_warehouse`) | service | warehouse | MỚI: chưa đặt | — | MỚI (owner 2026-10-15). Quản lý kho đồ (vật phẩm); kho pet vẫn ở Điền Trang. |
| **Hòm Thư Thạch Trụ** (`sq_mailbox`) | service | mailbox | MỚI: chưa đặt | — | MỚI. Vật thể tương tác (không phải NPC) đặt cạnh Thủ Kho Odan; thư và đính kèm. |

## city_market (3)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Chủ Tạp Hóa Bao** (`mk_general`) | service | shop | 65.31, 0.05 | Npc (1) | Vật phẩm tiêu hao, thức ăn pet. |
| **Thợ Rèn Gorun** (`mk_smith`) | service | shop | 68.39, 0.05 | Npc (2) | Trang bị (hook cho P14). |
| **Nhà Buôn Lữ Hành Zhen** (`mk_trader`) | free | free, shop | 80.49, 0.28 | Npc (3) | Hàng luân phiên/nhiệm vụ phụ. |

## city_royal_palace (3)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Đại Thần Cố Vấn Ezra** (`pal_advisor`) | main | story, quest | 35.45, 17.8 | TTTD (1) | Hook cốt truyện chính cho P17 (chưa viết tuyến). |
| **Quan Bang Hội Lorne** (`pal_guild`) | service | guild | 40.51, 17.44 | guild | Lập/gia nhập bang hội. |
| **Ngự Y Hoàng Cung Mina** (`pal_healer`) | service | heal | 43.75, 17.56 | thaythuoc (4) | Hồi máu + giải trạng thái. |

## city_activity_hall (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Sứ Quản Hoạt Động Thalia** (`act_events`) | free | events, free | -0.53, 16.07 | guild (2) | Cổng vào hoạt động: Sói–Cừu, đấu trường PK/đội, chiến bang. |
| **Nhân Viên Phần Thưởng Fia** (`act_reward`) | service | reward | MỚI: chưa đặt | — | MỚI. Nhận thưởng hoạt động/hằng ngày (P08). |

## city_pet_room (6)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Lão Sư Thuần Linh Haru** (`pet_master`) | main | appraise, quest | -5.63, -14.05 | Ong Poke | Bước giám định trong chuỗi P04 (Phòng thú cưng: giám định, cường hóa, lai tạo, ấp, cửa hàng pet). |
| **Chủ Tiệm Linh Thú Pomi** (`pet_shop`) | service | shop | -2.34, -14.03 | Shop | Đồ cho pet (thức ăn, huấn luyện). |
| **Thợ Cải Hoán Zeno** (`pet_enhance`) | service | strengthen | 0.82, -14.06 | LamMoi | Cường hóa/làm mới pet. |
| **Tế Ti Ban Phúc Sana** (`pet_bless`) | service | heal, bless | 3.61, -14.06 | ChucPhuc | Hồi pet + ban phúc (buff ngắn). |
| **Thuật Sư Hợp Linh Vaen** (`pet_fusion`) | main | breed, recipe, quest | MỚI: chưa đặt | — | MỚI. Tổng hợp pet → trứng, học công thức (thay phần breed/recipe của Oren). Bước "tổng hợp → trứng" của chuỗi P04. |
| **Ấp Sư Nimu** (`pet_hatch`) | service | hatch | MỚI: chưa đặt | — | MỚI. Ấp trứng/nở. P16 có thể dời việc ấp ra nông trại riêng sau. |

## city_farm (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Quản Trang Oren** (`ranch_keeper`) | service | storage | -3.51, -25.71 | QuanLy | NPC runtime sẵn có (`ranch_keeper`). Owner 2026-10-15: NPC duy nhất ngoài nông trại, chỉ gửi/rút pet. Runtime hiện còn appraise, breed, strengthen, recipe, heal, quest: chuyển sang Phòng thú cưng khi migrate (chưa đổi runtime). |

## city_deathmatch_arena (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Đài Chủ Vale** (`arena_master`) | main | arena, heal | 39.65, 39.66 | thaythuoc (1) | NPC runtime sẵn có (`arena_master`). Cổng đấu trường trong chuỗi P04. |
| **Cựu Đấu Sĩ Garm** (`arena_free`) | free | free | MỚI: chưa đặt | — | MỚI. Truyện nền đấu trường. |

## treasure_beach_fishermen_beach (4)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Hoa Tiêu Nia** (`beach_guide`) | main | quest, heal | -0.02, 1.82 | Walter (1) | NPC runtime sẵn có (`beach_guide`). Dẫn vào vùng bãi biển. |
| **Ngư Thương Coda** (`fish_shop`) | service | shop | 4.94, 1.66 | Shop | Mồi, đồ biển. |
| **Sư Phụ Hải Kỹ Marin** (`fish_skill`) | service | learn | -2.95, 1.91 | Skill | Kỹ năng bậc 2 theo vùng biển. |
| **Lão Ngư Dân Bako** (`fish_free`) | free | free | 2.7, 1.8 | Gustin | Nhiệm vụ phụ ngư nghiệp. |

## treasure_beach_east_beach (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Trạm Trưởng Rinka** (`east_camp`) | free | free | 40.18, 1.94 | Saja | Bãi quái: chỉ nhiệm vụ phụ (không hồi máu). Gần điểm xuất hiện từ trụ. |
| **Người Nhặt Vỏ Sò Pua** (`east_free`) | free | free | MỚI: chưa đặt | — | MỚI. Gần điểm xuất hiện. |

## treasure_beach_west_beach (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Y Sư Lữ Hành Kuri** (`west_healer`) | free | free | -27.06, 1.47 | Ithaqua | Bãi quái: đổi từ hồi máu sang nhiệm vụ phụ (hái thảo dược); hồi máu chỉ ở map an toàn. |
| **Họa Sĩ Bãi Cát Sen** (`west_free`) | free | free | MỚI: chưa đặt | — | MỚI. Truyện nền. |

## treasure_beach_deep_sea (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thợ Lặn Maro** (`deep_diver`) | free | free | -9.92, -13.68 | Walter | Bãi quái: chỉ nhiệm vụ phụ. |

## treasure_beach_prosperity_island (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thuyền Trưởng Đảo Fenn** (`isl_captain`) | free | free | MỚI: chưa đặt | — | MỚI. Bãi quái: chỉ nhiệm vụ phụ; bỏ hồi máu và cửa hàng. |

## middle_corridor_main_hall (7)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thuyền Trưởng Dorn** (`ship_captain`) | main | story, quest | -0.23, -1.96 | Logan | Hook cốt truyện chính Lv40+ (P17). |
| **Hoa Tiêu Trụ Kael** (`ship_pillar`) | service | teleport | 3.05, 1.87 | TTTD | Trụ trên tàu: 6 vùng cao, Điền Trang, Quảng Trường (U5). |
| **Y Sư Thuyền Lilo** (`ship_healer`) | service | heal | 0.71, 1.81 | Npc | Hồi máu. |
| **Sư Phụ Hải Chiến Zephyr** (`ship_skill`) | service | learn | -5.15, 1.67 | npc (1) | Kỹ năng bậc 3 (Lv40+). |
| **Quản Kho Thuyền Moto** (`ship_shop`) | service | shop | -2.39, 1.81 | Npc (1) | Đồ Lv40+. |
| **Thợ Rèn Tàu Harlo** (`ship_smith`) | service | smith | MỚI: chưa đặt | — | MỚI (owner 2026-10-15). Rèn trang bị Lv40+ (hook cho P14). |
| **Lữ Khách Tàu Yuma** (`ship_free`) | free | free | -4.21, -1.96 | npc | Nhiệm vụ phụ vùng cao. |

## desert_shicheng_ruins (4)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Trạm Trưởng Sa Thạch Aven** (`desert_aven`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Thương Nhân Sa Mạc Brisa** (`desert_brisa`) | service | shop | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng của vùng. |
| **Sư Phụ Hoang Sa Calder** (`desert_calder`) | service | learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Dạy kỹ năng; bậc do P13 quyết. |
| **Lữ Khách Cát Vàng Dalia** (`desert_dalia`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Nhiệm vụ phụ nhẹ, truyện nền. |

## desert_entrance (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Tìm Nước Edda** (`desert_edda`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## desert_sealed_land (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## desert_hulu_tribe (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Tìm Nước Fenwick** (`desert_fenwick`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## desert_barren_sands (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Tìm Nước Galen** (`desert_galen`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## desert_disaster_sands (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## windrock_mountain_camp (4)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Trại Trưởng Phong Thạch Hesper** (`wind_hesper`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Thợ Đồ Sơn Cước Iris** (`wind_iris`) | service | shop | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng của vùng. |
| **Sư Phụ Đá Gió Jorin** (`wind_jorin`) | service | learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Dạy kỹ năng; bậc do P13 quyết. |
| **Người Chăn Dê Núi Kestra** (`wind_kestra`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Nhiệm vụ phụ nhẹ, truyện nền. |

## windrock_mountain_stone_bridge (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thợ Săn Núi Loren** (`wind_loren`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## windrock_mountain_howling_canyon (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## windrock_mountain_mountain_range (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thợ Săn Núi Mirel** (`wind_mirel`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## windrock_mountain_mountain_path (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thợ Săn Núi Nolan** (`wind_nolan`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## windrock_mountain_summit (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thợ Săn Núi Orla** (`wind_orla`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## nightmare_island_survivor_camp (3)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Đội Trưởng Tàn Sinh Pavel** (`night_pavel`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Map hỗn hợp (NPC và quái trộn, owner 2026-10-15): được phép hồi máu. Hook chuỗi chính. |
| **Tiểu Thương Sống Sót Quinn** (`night_quinn`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Map hỗn hợp: cửa hàng + dạy kỹ năng (bậc do P13). |
| **Người Kể Chuyện Đảo Rhea** (`night_rhea`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Nhiệm vụ phụ, truyện nền. |

## nightmare_island_east_magic_island (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Sống Sót Soren** (`night_soren`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## nightmare_island_ruins (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Sống Sót Talia** (`night_talia`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## nightmare_island_disaster_gate (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## nightmare_island_resentment_path (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Sống Sót Ulric** (`night_ulric`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## nightmare_island_despair_land (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Sống Sót Vesna** (`night_vesna`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## tomb_region_camp (4)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Quản Trạm Canh Lăng Wren** (`tomb_wren`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Người Bán Hương Nến Xan** (`tomb_xan`) | service | shop | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng của vùng. |
| **Sư Phụ Linh Lăng Yara** (`tomb_yara`) | service | learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Dạy kỹ năng; bậc do P13 quyết. |
| **Người Giữ Mộ Zora** (`tomb_zora`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Nhiệm vụ phụ nhẹ, truyện nền. |

## tomb_region_resentment_path (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Thắp Đèn Mộ Alder** (`tomb_alder`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## tomb_region_despair_path (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## tomb_region_dead_ruins (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## tomb_region_deep_ruins (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## tomb_region_gods_tomb (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Thắp Đèn Mộ Bram** (`tomb_bram`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## tomb_region_soul_cemetery (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Thắp Đèn Mộ Cora** (`tomb_cora`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |
| **Người Thắp Đèn Mộ Dov** (`tomb_dov`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## tomb_region_unnamed_area_01 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## tomb_region_unnamed_area_02 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## crossroads_unnamed_area_01 (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Trưởng Cổng Địa Đạo Elric** (`cross_elric`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Thợ Đèn Địa Đạo Fara** (`cross_fara`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## crossroads_unnamed_area_02 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## crossroads_unnamed_area_03 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Dò Đường Gwen** (`cross_gwen`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## crossroads_unnamed_area_04 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Dò Đường Hale** (`cross_hale`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## crossroads_unnamed_area_05 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Dò Đường Ines** (`cross_ines`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## crossroads_unnamed_area_06 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## astral_realm_unnamed_area_01 (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Tiên Sứ Tử Vân Joss** (`astral_joss`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Hiền Giả Vân Ảnh Kira** (`astral_kira`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## astral_realm_spacetime_rift (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## astral_realm_unnamed_area_02 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Kẻ Ngắm Mây Lars** (`astral_lars`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## astral_realm_unnamed_area_03 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## astral_realm_unnamed_area_04 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## astral_realm_unnamed_area_05 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Kẻ Ngắm Mây Mara** (`astral_mara`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## astral_realm_unnamed_area_06 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## ancient_ruins_unnamed_area_01 (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thủ Hộ Tiền Sảnh Neth** (`ancient_neth`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Học Giả Ngọc Lục Olin** (`ancient_olin`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## ancient_ruins_unnamed_area_02 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Khảo Cổ Perrin** (`ancient_perrin`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## ancient_ruins_unnamed_area_03 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## ancient_ruins_unnamed_area_04 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Khảo Cổ Rue** (`ancient_rue`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## ancient_ruins_unnamed_area_05 (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Khảo Cổ Sable** (`ancient_sable`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## ancient_ruins_unnamed_area_06 (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## ghost_castle_gate (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Quản Cổng U Lâu Tove** (`ghost_tove`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Du Hồn Thương Nhân Una** (`ghost_una`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## ghost_castle_deep_woods (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## ghost_castle_ancient_city_secret_chamber (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## world_tree_gate (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Hộ Vệ Thế Thụ Vik** (`tree_vik`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Dược Sư Lá Xanh Willa** (`tree_willa`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## world_tree_deep_woods (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## world_tree_secret_chamber (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## tower_region_main_tower (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Điểu Sứ Yves** (`tower_yves`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Tăng Nhân Điểu Tháp Zane** (`tower_zane`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## tower_region_deep_woods (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Người Quan Sát Chim Aria** (`tower_aria`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## tower_region_secret_floor (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## immortal_maze_main_maze (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Dẫn Lộ Mê Thành Bex** (`maze_bex`) | main | quest, heal | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Trưởng hub: nhiệm vụ vùng (hook chuỗi chính) + hồi máu. |
| **Thương Nhân Mê Cung Cleo** (`maze_cleo`) | service | shop, learn | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Cửa hàng + dạy kỹ năng (bậc do P13). |

## immortal_maze_floor (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Kẻ Lạc Lối Dune** (`maze_dune`) | free | free | MỚI: chưa đặt | — | MỚI (vị trí chưa trích từ APK). Bãi quái: chỉ nhiệm vụ phụ (owner 2026-10-15). |

## immortal_maze_secret_floor (0)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|

## Phạm vi roster

Tài liệu này **chỉ soạn NPC** (tên, hạng, vai trò dịch vụ, vị trí sườn). Hạng `main` chỉ đánh dấu NPC dự kiến tham gia tuyến chính; **chuỗi nhiệm vụ chính, thứ tự và nội dung do phase quest quyết (P04/P17)**, không quyết ở P12. Runtime hiện có 4 nhiệm vụ và 5 NPC, roster này không đổi runtime.

## Quyết định owner
- Kỹ năng: mỗi điểm dạy là một thầy chung cho mọi race; bậc kỹ năng từng thầy do P13 quyết.
- Nông trại và Phòng thú cưng là map riêng của từng người chơi (không dùng chung). Nông trại chỉ có Oren (gửi/rút pet); giám định, cường hóa, lai tạo, ấp và dịch vụ pet khác ở Phòng thú cưng, ấp trứng cũng ở đó.

