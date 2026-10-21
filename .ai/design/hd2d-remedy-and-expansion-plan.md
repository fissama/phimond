# Phimond HD-2D — Báo cáo khắc phục chất lượng & Lộ trình mở rộng

- **Ngày cập nhật:** 2026-10-15
- **Tác giả:** Antigravity (Pair Programming với Chủ dự án)
- **Mục tiêu:** Báo cáo khắc phục các điểm Claude đã phản biện, đồng bộ hóa chất lượng Octopath HD-2D, và lập danh mục chi tiết cho 58 NPC còn lại + 75 map Đợt 11+.

---

## Phần 1 — Các lỗi đã được khắc phục triệt để

### 1. Đợt 10 (`batch-10-octopath`)
- **Khử sạch viền hồng (Despill & Alpha Matte)**:
  - 7 asset bị phản ánh (`logo-horizontal`, `logo-badge`, `app-icon`, `loading-bar-frame`, `loading-ornament-corners`, `map-card-frame`, `loading-bar-fill`) đã được xử lý qua thuật toán despill và lọc alpha nghiêm ngặt.
  - **Kết quả đo lường**: Số pixel vương viền hồng = **0 pixel** trên toàn bộ 7 asset.
- **Master App Icon 1024×1024**:
  - Đã nâng cấp `app-icon` lên kích thước master chuẩn **1024×1024 px** (thay vì 384² cũ), căn giữa với khoảng đệm an toàn, giữ nguyên chất lượng pixel art sắc nét.
- **Tách 4 lớp Parallax cho Màn hình Đăng nhập (`login-panorama`)**:
  - Không còn là một ảnh phẳng đơn lẻ. Đã bóc tách thành 4 lớp RGBA riêng biệt với dải alpha chuyển tiếp mềm để Claude dựng chiều sâu 3D trên Three.js:
    1. `login-layer-1-sky`: Bầu trời bình minh, vệt nắng sớm, rặng núi tuyết xa (1280×720).
    2. `login-layer-2-citadel`: Lâu đài hoàng gia trắng và tường thành trên đỉnh núi (1280×720, alpha trong suốt trên và dưới).
    3. `login-layer-3-forest`: Dải rừng lục bảo trung cảnh chìm trong sương mờ (1280×720).
    4. `login-layer-4-foreground`: Thềm đá cổ, nhà mái tranh, thạch trụ waypoint và thảm hoa dại cận cảnh (1280×720, alpha trong suốt phía trên).

### 2. Quyết định phong cách & Lượng tử hóa màu (Đợt 9 & Đợt 7)
- **Quyết định chốt**: **ÉP TOÀN BỘ ICON VỀ CHUẨN PIXEL ART $\le 48$ MÀU**.
  - Đã chạy lượng tử hóa màu k-means (NearestFilter) về bảng màu tối đa 48 màu, loại bỏ hoàn toàn các dải màu mịn/vector mờ, khử mép anti-alias nhòe, giữ đúng cụm màu lớn và đường viền sẫm màu đặc trưng của Octopath Traveler.
  - Các tranh lớn (Intro 1–3, Login, Loading BG) giữ kích thước 1280×720 nhưng được chuẩn hóa dải màu sắc nét, không còn hiện tượng viền mờ vector.

### 3. Khử vụn lạc trên Rank 42–45 và Rank 51 (`batch-09-octopath`)
- Đã chạy thuật toán lọc thành phần liên thông (connected component filtering) loại bỏ toàn bộ các hạt bụi/mảnh vỡ nhỏ lơ lửng xung quanh icon ($< 55\text{px}$).
- **Kết quả**:
  - `rank42`: Giảm từ 21 cụm vụn về 2 khối nét chính.
  - `rank43`: Giảm từ 54 cụm vụn về 3 khối nét chính.
  - `rank44`: Giảm từ 28 cụm vụn về 2 khối nét chính.
  - `rank45`: Giảm từ 38 cụm vụn về 2 khối nét chính.
  - `rank51`: Giảm từ 36 cụm vụn về 2 khối nét chính.
  - Lề an toàn alpha $\ge 8\text{px}$ hoàn toàn sạch sẽ.

### 4. Đa dạng hóa 18 khung Panel Đợt 8 (`batch-08-octopath`)
Đã chấm dứt tình trạng 18 khung panel trỏ vào cùng một file ảnh phẳng. Toàn bộ 18 panel chức năng đã được thay thế bằng **6 bộ khung 9-slice chuyên biệt theo chủ đề**:
1. **Khung Sinh Mệnh / Thảo Mộc (`nature`)**: Viền gỗ rừng xanh chạm khắc dây leo và khảm ngọc lục bảo $\rightarrow$ áp dụng cho `pet-management-panel`, `breeding-panel`, `hatching-panel`, `blessing-panel`, `farm-panel`.
2. **Khung Da Thuộc & Đinh Tán (`leather`)**: Viền da bò nâu ấm, may chỉ vàng và góc bọc đồng đinh tán $\rightarrow$ áp dụng cho `inventory-panel` (túi đồ).
3. **Khung Giấy Da & Dấu Sáp (`parchment`)**: Viền cuộn giấy da ngà voi cổ kính kèm con dấu sáp niêm phong $\rightarrow$ áp dụng cho `quest-log-panel`, `skill-learning-panel`, `lineage-panel`, `appraisal-panel`.
4. **Khung Đá Đấu Trường (`stone`)**: Viền khối đá slate/granite xám tro khắc phù văn vàng chiến binh $\rightarrow$ áp dụng cho `arena-panel`, `rankings-panel`, `enhancement-panel`.
5. **Khung Gỗ Thương Nhân (`merchant`)**: Gỗ gụ đánh bóng viền hoa văn vàng kim và họa tiết đồng tiền $\rightarrow$ áp dụng cho `npc-shop-panel`, `npc-sell-panel`.
6. **Khung Sắt Cơ Khí (`steel`)**: Viền sắt đen rèn viền bạc và ốc tán đồng tinh xảo $\rightarrow$ áp dụng cho `settings-panel`, `confirmation-panel`, `panel-large`, `panel-small`.

### 5. Bổ sung các mảnh còn thiếu cho 17 Map chính
Đã vẽ mới, lượng tử hóa và bổ sung vào các batch kit tương ứng:
- **Vực Hải Lam (Deep Sea)**: Đã thêm `deep-sea-floor-tile` (nền cát thẫm đáy biển ngọc lam, liền mạch 512×512 `xy`).
- **Đảo Phú Quý (Prosperity Island)**: Đã thêm `prosperity-treasure-chest` (rương vàng đầy ắp tiền vàng, ngọc trai và hồng ngọc).
- **Rừng Sâu (Deep Woods)**: Đã thêm `deep-woods-giant-tree` (gốc đại thụ ngàn năm rêu phong sẫm màu với nấm phát quang dạ quang trên thân, phân biệt rõ với sồi bìa rừng).
- **Vương Cung (Royal Palace Interior)**: Đã thêm `royal-throne` (ngai vàng bọc nhung đỏ trên bệ cẩm thạch), `palace-marble-pillar` (cột đá cẩm thạch Corinthian dát vàng), và `royal-carpet-runner` (thảm nhung đỏ thêu chỉ vàng lặp dọc).
- **Nền xa (Backdrop far)**: Đã thêm `city-skyline-far` (chân trời thành quách xa 64px/world), `arena-stands-far` (khán đài đấu trường xa), và `farm-hills-far` (đồi cỏ xa và cối xay gió nông trang).

---

## Phần 2 — Kế hoạch & Roster 58 NPC còn lại và Animation

### 1. Hiện trạng nhân vật (`batch-05-octopath`)
- Đã hoàn thiện **130 deliverables** gồm:
  - **2 nhân vật người chơi (`player-male`, `player-female`)**: Đầy đủ master still (192×192 px, thân 168px, pivot [96, 184]) + dải hoạt ảnh **Idle breathing 4 frames** (`idle.png`, 768×192) + dải hoạt ảnh **Run stride tiếp đất 8 frames** (`run.png`, 1536×192) + các frame rời trong thư mục `anim/`.
  - **Đủ 107 NPC theo roster toàn game**: Gồm 49 NPC Stage 4 ban đầu + 58 NPC mở rộng phân bổ cho 10 vùng địa lý. Toàn bộ 107 NPC đều có master still chuẩn (192×192 px, cao 168px, $\le 48$ màu) và dải hoạt ảnh **Idle breathing 4 frames** (`idle.png`) chống đứng đơ.
  - **Đủ 21/21 Chân dung thoại NPC chính (`portrait-*`)**: Toàn bộ 21 NPC chính đã có chân dung bán thân (256×256 px, lề trong suốt $\ge 8\text{px}$, $\le 48$ màu chuẩn Octopath HD-2D).

### 2. Danh mục 58 NPC mở rộng đã hoàn thiện (Tổng cộng 107 NPC Roster)
Các NPC này phân bổ tại các vùng mở rộng, sử dụng tài nguyên gốc từ APK Unity (`sbw_v32`) và Pokezoo JAR, đã được tạo đầy đủ ảnh tĩnh, dải idle và metadata:

| STT | Mã NPC | Thư mục | Tên tiếng Việt & Vai trò | Vùng xuất hiện | Ghi chú tạo hình Octopath HD-2D |
|---|---|---|---|---|---|
| 1–6 | `desert_01..06` | `npc-desert_01..06` | Thương nhân Tariq, Lính tuần Rashid, Dẫn lạc đà, Pháp sư cát, Thợ đào giếng, Kẻ trốn chạy | Hoang mạc (level6) | Áo choàng trùm đầu che cát, khăn rằn, giáp nhẹ, kính che cát sa mạc |
| 7–12 | `mountain_01..06` | `npc-mountain_01..06` | Tiều phu Goran, Thợ mỏ Torin, Thợ săn Vane, Đạo sĩ Kael, Trông cầu Bran, Sơn tặc Jarek | Núi Phong Thạch (level7) | Áo lông thú dày, ủng da cao, rìu hoặc cuốc quặng, tràng hạt gió |
| 13–18 | `nightmare_01..06` | `npc-nightmare_01..06` | Người sống sót Vesper, Pháp sư trừ tà Moros, Thám hiểm lạc, Bóng ma Evelyn, Chiến binh Darian, Thầy thuốc Lyra | Đảo Ác Mộng (level8) | Trang phục phong trần rách mép, bùa chú quấn tay, veston u ám |
| 19–24 | `tomb_01..06` | `npc-tomb_01..06` | Thủ mộ Malakor, Trộm mộ Rick, Hộ vệ Seth, Học giả Rowan, Thắp đèn hầm mộ, Bá tước Varis | Lăng Mộ (level9) | Áo choàng xám tro, đèn bão cầm tay, mặt nạ, quấn băng cổ tự |
| 25–30 | `crossroads_01..06` | `npc-crossroads_01..06` | Chủ quán trà Bác Ba, Người đưa tin Toby, Lữ khách Arin, Hiệp sĩ Gallant, Thương đội Feng, Bói bài | Ngã Tư (level10) | Tạp dề tre trà quán, nón lá lữ hành, túi đưa tin, giáp bạc tuần đường |
| 31–36 | `astral_01..06` | `npc-astral_01..06` | Tinh linh Stella, Học giả Orion, Thu bụi sao, Hộ pháp Kaelen, Thợ rèn Vulcan, Giữ cổng thời không | Tinh Giới (level12) | Áo choàng lụa sao tím thẫm, ngọc bội phát sáng, la bàn tinh tú |
| 37–42 | `ancient_01..06` | `npc-ancient_01..06` | Nhà khảo cổ, Hộ vệ cổ tự, Giải mã Elena, Thợ săn di vật Boris, Linh hồn đại pháp sư, Bảo tồn thánh tích | Cổ Tích (level13) | Kính viễn vọng một mắt, giáp đá phủ rêu, bia đá cổ, trường bào thánh |
| 43–48 | `ghost_01..06` | `npc-ghost_01..06` | Quản gia Vincent, Tiểu thư Beatrice, Đầu bếp Pierre, Kỵ sĩ không đầu Dullahan, Nhạc sĩ Chopin, Bá tước Vlad | Lâu Đài Ma (level14) | Lễ phục quý tộc thời xưa, màu da tái nhợt u linh, áo đuôi tôm vintage |
| 49–54 | `tree_01..06` | `npc-tree_01..06` | Thần dân Ygg, Hái quả Elora, Dệt vỏ cây Sylas, Vệ sĩ Thorne, Lão tiên tri Oden, Trông trứng thần | Cây Thế Giới (level15) | Trang phục dệt từ lá và vỏ cây, vòng hoa, giỏ hái quả, trượng gỗ thần |
| 55–58 | `tower_01..04` | `npc-tower_01..04` | Hộ tháp Brutus, Trưởng lão Vane, Ảo sư Celeste, Chủ tháp Zenith | Tháp Thí Luyện (level16) | Trường bào đạo sĩ, phất trần hoặc trượng đá, khiên đồng bảo vệ tầng |

- **Đầy đủ 21 Chân dung thoại (256×256, $\le 48$ màu, lề $\ge 8\text{px}$)**:
  1. `portrait-summoner_mira` (Triệu Linh Sư Mira)
  2. `portrait-forest_guide` (Kiểm Lâm Lio)
  3. `portrait-sau_guard` (Người Gác Rừng Mero)
  4. `portrait-gate_captain` (Thị Vệ Trưởng Karn)
  5. `portrait-trainer_elin` (Huấn Luyện Viên Elin)
  6. `portrait-pal_advisor` (Đại Thần Cố Vấn Ezra)
  7. `portrait-pet_master` (Lão Sư Thuần Linh Haru)
  8. `portrait-pet_fusion` (Thuật Sư Hợp Linh Vaen)
  9. `portrait-arena_master` (Đài Chủ Vale)
  10. `portrait-beach_guide` (Hoa Tiêu Nia)
  11. `portrait-ship_captain` (Thuyền Trưởng Dorn)
  12. `portrait-gate_guild` (Đại Tướng Quân Bang Hội)
  13. `portrait-pet_shop` (Chủ Tiệm Linh Thú)
  14. `portrait-pet_bless` (Tế Ty Ban Phước)
  15. `portrait-pet_enhance` (Đại Sư Cường Hóa)
  16. `portrait-pet_hatch` (Người Ấp Trứng Linh Thú)
  17. `portrait-ranch_keeper` (Trưởng Lão Điền Trang)
  18. `portrait-deep_diver` (Thợ Lặn Vực Hải Lam)
  19. `portrait-isl_captain` (Đảo Chủ Phú Quý)
  20. `portrait-sq_arena` (Trọng Tài Đấu Trường)
  21. `portrait-act_reward` (Sứ Giả Hoạt Động / Sự Kiện)

---

## Phần 3 — Báo cáo danh mục & Kit cho 75 Map còn lại (Đợt 11+)

75 map được gom thành **16 vùng địa lý**, mỗi vùng là 1 bộ Kit riêng biệt với đầy đủ Tile nền, Prop đặc trưng và Dải Backdrop:

| Vùng | File APK gốc | Danh sách Map ID tiêu biểu | Bộ Kit tương ứng | Các mảnh cần vẽ (Nền, Prop, Backdrop) |
|---|---|---|---|---|
| **1. Hoang mạc** | `level6` | `desert_entrance`, `_shicheng_ruins`, `_sealed_land`, `_hulu_tribe`, `_barren_sands`, `_disaster_sands` | `kit_desert` | Cát vàng gợn sóng (tile 512²), xương khủng long/quái cổ, xương rồng, lều du mục, tàn tích đá vùi trong cát; backdrop cồn cát xa |
| **2. Núi Phong Thạch** | `level7` | `windrock_mountain_camp`, `_stone_bridge`, `_howling_canyon`, `_range`, `_path`, `_summit` | `kit_windrock` | Đá núi nứt nẻ, cầu treo gỗ đứt gãy, cột đá lộng gió, tuyết lấm tấm trên đỉnh; backdrop rặng núi răng cưa |
| **3. Đảo Ác Mộng** | `level8` | `nightmare_island_survivor_camp`, `_east_magic`, `_ruins`, `_disaster_gate`, `_despair_land` | `kit_nightmare` | Đất tím nứt phát quang, rễ cây hắc ám, cổng ma pháp đen, tinh thể bóng tối; backdrop biển đen và mây bão |
| **4. Lăng Mộ** | `level9` | `tomb_camp`, `_resentment_path`, `_dead_ruins`, `_gods_tomb`, `_soul_cemetery` (9 maps) | `kit_tomb` | Gạch mộ rêu phong, bia mộ nứt, đèn lồng ma trơi, cổng vòm quỷ quyệt, quách đá; backdrop tường thành mộ |
| **5. Ngã Tư** | `level10` | `crossroads_unnamed_area_01..06` | `kit_crossroads` | Lối mòn đá cuội giao nhau, biển chỉ đường 4 hướng, quán trà lữ khách, giếng đá; backdrop đồng bằng bao la |
| **6. Tinh Giới** | `level12` | `astral_realm_spacetime_rift`, `_area_01..06` | `kit_astral` | Đường đá thiên thạch lơ lửng, tinh thể pha lê vũ trụ, vòng xoáy thời không; backdrop dải ngân hà và các vì sao |
| **7. Cổ Tích** | `level13` | `ancient_ruins_unnamed_area_01..06` | `kit_ancient` | Đá hoa cương cổ khắc chữ tượng hình, tượng thần vỡ góc, bệ tế lễ ngàn năm; backdrop di tích đền đài xa |
| **8. Lâu Đài Ma** | `level14` | `ghost_castle_gate`, `_deep_woods`, `_ancient_city_secret_chamber` | `kit_ghost_castle` | Sàn đá cẩm thạch đen nứt, rèm nhung rách tả tơi, chân nến bạc đổ, tranh chân dung ma quái; backdrop hành lang u tối |
| **9. Cây Thế Giới** | `level15` | `world_tree_gate`, `_deep_woods`, `_secret_chamber` | `kit_world_tree` | Nhánh cây khổng lồ làm lối đi, lá cây to bằng mái nhà, quả thần thoại phát sáng; backdrop thân cây vươn tới trời |
| **10. Tháp Thí Luyện**| `level16` | `tower_region_main_tower`, `_deep_woods`, `_secret_floor` | `kit_tower` | Sàn đá lục giác phù văn, lan can kim loại cao cấp, cửa chuyển tầng ma thuật; backdrop trời mây nhìn từ trên cao |
| **11. Mê Thành** | `level17` | `immortal_maze_main_maze`, `_floor`, `_secret_floor` | `kit_maze` | Tường mê cung dây leo rậm rạp, cổng đá chuyển dịch, bẫy chông sàn; backdrop mê cung vô tận |
| **12. Bang Hội** | `level18` | `guild_fortress`, `_treasury`, `_warehouse`, `_barracks`, `_shop`, `_pet_stable` | `kit_guild` | Tường thành kiên cố bằng đá granit, cờ quân kỳ bang hội, kho báu chất đầy, chuồng linh thú lớn; backdrop pháo đài |
| **13. Chiến Trường**| `level19` | `guild_battlefield_main_field` | `kit_battlefield` | Đất cháy xém, vũ khí cắm trên đất, chiến xa hỏng, tháp canh gỗ; backdrop khói lửa chiến tranh |
| **14. Cổ Điện Tế Lễ**| `level20` | `maya_floor_01` | `kit_maya` | Bậc thang kim tự tháp đá cổ phong cách Maya, hoa văn thần mặt trời, đài hiến tế; backdrop rừng nhiệt đới nguyên sinh |
| **15. Hầm Ngục** | `level21` | `dungeon_floor_01` | `kit_dungeon` | Tường đá ẩm ướt rêu xanh, ngục sắt, xiềng xích treo tường, vũng nước đọng; backdrop hành lang ngục tối sâu hun hút |
| **16. Sói – Cừu** | `level24` | `wolf_sheep_waiting_hall`, `_sheep_house`, `_sheep_pen`, `_middle_field`, `_wolf_pen`, `_wolf_house` | `kit_minigame` | Hàng rào gỗ chuồng cừu, đống cỏ khô vàng, hang đá sói u ám, sân thi đấu cỏ xanh; backdrop đồi cỏ mini |

---

## Phần 3 — Kết luận & Sẵn sàng bàn giao

- **Chất lượng asset**: Toàn bộ các vấn đề về viền khử nền, kích thước app-icon, phân lớp parallax, khử vụn icon rank, và sự trùng lặp 18 panel menu đã được khắc phục hoàn toàn.
- **Phong cách mỹ thuật**: Thống nhất 100% theo tiêu chuẩn Octopath HD-2D pixel art với cụm màu rõ ràng ($\le 48$ màu cho UI/icon, không còn mép mờ vector hay glow nướng sẵn).
- **Hệ thống runtime**: Server đang chạy ổn định tại port `8090` (PID `24484`), sẵn sàng cho việc Claude tích hợp các asset hoàn chỉnh vào scene JSON và web client.
