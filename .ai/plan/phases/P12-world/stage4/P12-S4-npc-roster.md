# P12 Stage 4 — Roster NPC đề xuất (nháp, chờ owner duyệt)

49 NPC trong 17 map: 40 gắn vào vị trí NPC gốc APK 3.2 (44 slot), 9 MỚI (cần đặt vị trí khi vẽ HD-2D). Sinh bằng `gen_npc_roster.py`; tên không dùng tên NPC trong APK.

**Lưu ý:** tên object trong APK (`thaythuoc`, `TTTD`, `guild`…) là tên prefab, chưa đủ tin cậy để suy vai trò; vai trò ở đây là **thiết kế đề xuất**, chỉ dùng vị trí gốc làm sườn. Tọa độ APK chỉ là bản phác, bản vẽ HD-2D sẽ đặt lại.

Hạng: **main** = chuỗi nhiệm vụ chính (P04 onboarding; P17 viết truyện sau), **free** = NPC tự do/nhiệm vụ phụ (P18), **service** = dịch vụ.

## Ma trận phủ theo map

| Map | main | free | heal | learn | shop | khác |
|---|---|---|---|---|---|---|
| `summoning_hall_main_hall` | 1 | — | — | — | — | guide |
| `emerald_forest_main_woods` | 1 | 1 | 1 | 1 | 1 | — |
| `emerald_forest_deep_woods` | 1 | 1 | 1 | — | — | — |
| `city_palace_gate` | 1 | — | — | — | — | guild |
| `city_square` | 1 | 2 | 1 | 2 | — | arena, quest_board, teleport |
| `city_market` | — | 1 | — | — | 3 | — |
| `city_royal_palace` | 1 | — | 1 | — | — | guild, story |
| `city_activity_hall` | — | 1 | — | — | — | events, reward |
| `city_pet_room` | 2 | — | 1 | — | 1 | appraise, bless, breed, hatch, recipe, strengthen |
| `city_farm` | — | — | — | — | — | storage |
| `city_deathmatch_arena` | 1 | 1 | 1 | — | — | arena |
| `treasure_beach_fishermen_beach` | 1 | 1 | 1 | 1 | 1 | — |
| `treasure_beach_east_beach` | — | 1 | 1 | — | — | — |
| `treasure_beach_west_beach` | — | 1 | 1 | — | — | — |
| `treasure_beach_deep_sea` | — | 1 | 1 | — | — | — |
| `treasure_beach_prosperity_island` | — | 1 | 1 | — | 1 | — |
| `middle_corridor_main_hall` | 1 | 1 | 1 | 1 | 1 | story, teleport |

## summoning_hall_main_hall (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Triệu Linh Sư Mira** (`summoner_mira`) | main | quest, guide | -5.32, 0.36 | Npc | Người hướng dẫn đứng giữa; chọn bệ → nhận pet 1★ → mở khóa trụ một chiều tới Emerald. Nguồn có 4 biến thể ẩn cùng vị trí (4 trạng thái hội thoại). |

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
| **Người Gác Rừng Mero** (`sau_guard`) | main | quest, heal | 45.18, 1.41 | Vesa | Nhận báo cáo khi qua rừng sâu; giao bước nhiệm vụ đi Hoàng Môn (lần đầu). Hồi máu tại bãi quái. |
| **Cụ Rêu Tamo** (`sau_free`) | free | free | MỚI: chưa đặt | — | MỚI. Cụ già giữ rừng, truyện nền. |

## city_palace_gate (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thị Vệ Trưởng Karn** (`gate_captain`) | main | quest | MỚI: chưa đặt | — | MỚI. Tiếp nhận người chơi lần đầu tới Hoàng Môn theo nhiệm vụ, chỉ đường về Quảng Trường. |
| **Sứ Giả Bang Hội Ryo** (`gate_guild`) | service | guild | 30.91, -0.16 | guild (1) | Tư vấn/dẫn vào khu bang hội. |

## city_square (7)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Huấn Luyện Viên Elin** (`trainer_elin`) | main | quest, learn | 0.12, 0.6 | thaythuoc | NPC runtime sẵn có (`trainer`). Trung tâm chuỗi P04 tại thành. Runtime hiện còn shop+heal; thiết kế chuyển sang Thương Phố/Selka. |
| **Y Sư Selka** (`sq_healer`) | service | heal | -11.23, 0.32 | thaythuoc (3) | Hồi máu/MP cho pet toàn đội. |
| **Sư Phụ Kỹ Năng Doran** (`sq_skill`) | service | learn | -9.51, 0.04 | thaythuoc (5) | Dạy kỹ năng bậc 2 (Lv10–40). Phân trường phái theo race: P13 quyết. |
| **Người Kể Chuyện Hanae** (`sq_free`) | free | free | -8.23, -2.79 | thaythuoc (2) | Truyện nền thành phố, nhiệm vụ phụ. |
| **Trụ Sư Orsa** (`sq_pillar`) | service | teleport | 6.28, -1.66 | TTTD | Vận hành trụ đá (U1). Menu chỉ hiện vùng đủ cấp. Tên nguồn TTTD + gợi ý loading "Thủy tinh dịch chuyển phía Đông Quảng Trường" cho thấy đây rất có thể là trụ gốc. |
| **Đài Sứ Rena** (`sq_arena`) | service | arena | -2.44, -2.09 | TTTD (2) | Đăng ký Huyết Chiến Đài theo bậc. |
| **Quản Sự Nhiệm Vụ Tessa** (`sq_board`) | free | free, quest_board | -6.12, -0.06 | TTTD (3) | Bảng nhiệm vụ phụ/hằng ngày (P08/P18). |

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
| **Trạm Trưởng Rinka** (`east_camp`) | service | heal, quest | 40.18, 1.94 | Saja | Trại nghỉ ngay bãi quái; nơi người chơi tới bằng trụ. |
| **Người Nhặt Vỏ Sò Pua** (`east_free`) | free | free | MỚI: chưa đặt | — | MỚI. Gần điểm xuất hiện. |

## treasure_beach_west_beach (2)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Y Sư Lữ Hành Kuri** (`west_healer`) | service | heal | -27.06, 1.47 | Ithaqua | Hồi máu bãi quái. |
| **Họa Sĩ Bãi Cát Sen** (`west_free`) | free | free | MỚI: chưa đặt | — | MỚI. Truyện nền. |

## treasure_beach_deep_sea (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thợ Lặn Maro** (`deep_diver`) | free | free, heal | -9.92, -13.68 | Walter | Khoang khí nghỉ + nhiệm vụ phụ. |

## treasure_beach_prosperity_island (1)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thuyền Trưởng Đảo Fenn** (`isl_captain`) | free | free, heal, shop | MỚI: chưa đặt | — | MỚI. Cuối vùng: hồi máu, đồ báu vật, hook nhiệm vụ phụ. |

## middle_corridor_main_hall (6)

| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| **Thuyền Trưởng Dorn** (`ship_captain`) | main | story, quest | -0.23, -1.96 | Logan | Hook cốt truyện chính Lv40+ (P17). |
| **Hoa Tiêu Trụ Kael** (`ship_pillar`) | service | teleport | 3.05, 1.87 | TTTD | Trụ trên tàu: 6 vùng cao, Điền Trang, Quảng Trường (U5). |
| **Y Sư Thuyền Lilo** (`ship_healer`) | service | heal | 0.71, 1.81 | Npc | Hồi máu. |
| **Sư Phụ Hải Chiến Zephyr** (`ship_skill`) | service | learn | -5.15, 1.67 | npc (1) | Kỹ năng bậc 3 (Lv40+). |
| **Quản Kho Thuyền Moto** (`ship_shop`) | service | shop | -2.39, 1.81 | Npc (1) | Đồ Lv40+. |
| **Lữ Khách Tàu Yuma** (`ship_free`) | free | free | -4.21, -1.96 | npc | Nhiệm vụ phụ vùng cao. |

## Phạm vi roster

Tài liệu này **chỉ soạn NPC** (tên, hạng, vai trò dịch vụ, vị trí sườn). Hạng `main` chỉ đánh dấu NPC dự kiến tham gia tuyến chính; **chuỗi nhiệm vụ chính, thứ tự và nội dung do phase quest quyết (P04/P17)**, không quyết ở P12. Runtime hiện có 4 nhiệm vụ và 5 NPC, roster này không đổi runtime.

## Quyết định owner
- Kỹ năng: mỗi điểm dạy là một thầy chung cho mọi race; bậc kỹ năng từng thầy do P13 quyết.
- Nông trại và Phòng thú cưng là map riêng của từng người chơi (không dùng chung). Nông trại chỉ có Oren (gửi/rút pet); giám định, cường hóa, lai tạo, ấp và dịch vụ pet khác ở Phòng thú cưng, ấp trứng cũng ở đó.

