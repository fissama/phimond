# P12 Stage 4 — Registry map canonical (đề xuất, chờ owner duyệt)

92 map APK 3.2; 75 map trong phạm vi roster. Sinh bằng `gen_map_registry.py` từ `apk-extract/map-scan.json`.
Loại map là suy luận: có trigger quái hoặc điểm spawn → bãi quái; không quái mà có NPC → hub an toàn; instance/riêng/chung theo bang là **đề xuất**, APK chưa có bằng chứng. Cấp quái ngoài 17 map là dải vùng (APK), chưa chia từng map.

| Map | Nhóm | Loại | Cấp | Spawn APK → đề xuất | Slot NPC | Cửa | Hồi sinh về | Phạm vi |
|---|---|---|---|---|---|---|---|---|
| **Triệu Linh Điện** (`summoning_hall_main_hall`) | Khởi đầu | dùng một lần | — | 0 | 4 | 1 | Bìa Rừng Lục Bảo | có |
| **Quảng Trường Thạch Trụ** (`city_square`) | Thành phố | hub an toàn | — | 0 | 7 | 2 | Quảng Trường Thạch Trụ | có |
| **Hoàng Môn** (`city_palace_gate`) | Thành phố | hub an toàn | — | 0 | 1 | 3 | Quảng Trường Thạch Trụ | có |
| **Điền Trang Lục Dã** (`city_farm`) | Thành phố | riêng từng người chơi | — | 0 | 2 | 2 | Quảng Trường Thạch Trụ | có |
| **Phòng thú cưng** (`city_pet_room`) | Thành phố | riêng từng người chơi | — | 0 | 4 | 1 | Quảng Trường Thạch Trụ | có |
| **Thương Phố** (`city_market`) | Thành phố | hub an toàn | — | 0 | 3 | 2 | Quảng Trường Thạch Trụ | có |
| **Vương Cung** (`city_royal_palace`) | Thành phố | hub an toàn | — | 0 | 3 | 2 | Quảng Trường Thạch Trụ | có |
| **Vạn Sự Hội Sảnh** (`city_activity_hall`) | Thành phố | hub an toàn | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | có |
| **Huyết Chiến Đài** (`city_deathmatch_arena`) | Thành phố | instance | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | có |
| **Bìa Rừng Lục Bảo** (`emerald_forest_main_woods`) | Emerald | hỗn hợp (NPC và quái) | 1–5 | 0 → 4 | 4 | 1 | Bìa Rừng Lục Bảo | có |
| **Rừng Sâu Lục Bảo** (`emerald_forest_deep_woods`) | Emerald | bãi quái | 5–10 | 6 → 8 | 1 | 2 | Bìa Rừng Lục Bảo | có |
| **Bến Ngư Châu** (`treasure_beach_fishermen_beach`) | Bãi biển | hub an toàn | — | 0 | 4 | 3 | Bến Ngư Châu | có |
| **Bờ Đông Ngọc Bích** (`treasure_beach_east_beach`) | Bãi biển | bãi quái | 10–12 | 15 → 12 | 1 | 2 | Bến Ngư Châu | có |
| **Vực Hải Lam** (`treasure_beach_deep_sea`) | Bãi biển | bãi quái | 13–14 | 10 | 1 | 1 | Bến Ngư Châu | có |
| **Bờ Tây Hoàng Sa** (`treasure_beach_west_beach`) | Bãi biển | bãi quái | 12–13 | 10 | 1 | 2 | Bến Ngư Châu | có |
| **Đảo Phú Quý** (`treasure_beach_prosperity_island`) | Bãi biển | bãi quái | 14–15 | 10 | 0 | 1 | Bến Ngư Châu | có |
| **Sa Thạch Cổ Thành** (`desert_shicheng_ruins`) | Sa Mạc | hub an toàn | — | 0 | 4 | 3 | Sa Thạch Cổ Thành | có |
| **Cửa Ngõ Hoàng Mạc** (`desert_entrance`) | Sa Mạc | bãi quái | 15–20 | 12 | 1 | 2 | Sa Thạch Cổ Thành | có |
| **Phong Ấn Cổ Địa** (`desert_sealed_land`) | Sa Mạc | bãi quái | 15–20 | 12 | 0 | 1 | Sa Thạch Cổ Thành | có |
| **Bộ Lạc Hồ Lô** (`desert_hulu_tribe`) | Sa Mạc | bãi quái | 15–20 | 10 | 1 | 3 | Sa Thạch Cổ Thành | có |
| **Hoang Sa Vô Tận** (`desert_barren_sands`) | Sa Mạc | bãi quái | 15–20 | 12 | 1 | 1 | Sa Thạch Cổ Thành | có |
| **Tai Ương Sa Mạc** (`desert_disaster_sands`) | Sa Mạc | bãi quái | 15–20 | 10 | 0 | 1 | Sa Thạch Cổ Thành | có |
| **Trại Phong Thạch** (`windrock_mountain_camp`) | Mỏm Đá Gió | hub an toàn | — | 0 | 4 | 3 | Trại Phong Thạch | có |
| **Cầu Thiên Thạch** (`windrock_mountain_stone_bridge`) | Mỏm Đá Gió | bãi quái | 20–25 | 12 | 1 | 2 | Trại Phong Thạch | có |
| **Hẻm Gió Gào** (`windrock_mountain_howling_canyon`) | Mỏm Đá Gió | bãi quái | 20–25 | 12 | 0 | 1 | Trại Phong Thạch | có |
| **Dãy Phong Lĩnh** (`windrock_mountain_mountain_range`) | Mỏm Đá Gió | bãi quái | 20–25 | 12 | 1 | 2 | Trại Phong Thạch | có |
| **Sơn Đạo Phong Vân** (`windrock_mountain_mountain_path`) | Mỏm Đá Gió | bãi quái | 20–25 | 12 | 1 | 2 | Trại Phong Thạch | có |
| **Đỉnh Thiên Phong** (`windrock_mountain_summit`) | Mỏm Đá Gió | bãi quái | 20–25 | 10 | 1 | 1 | Trại Phong Thạch | có |
| **Trại Tàn Sinh** (`nightmare_island_survivor_camp`) | Đảo Ác Mộng | hỗn hợp (NPC và quái) | 25–30 | 5 | 3 | 4 | Trại Tàn Sinh | có |
| **Đông Đảo Huyền Thuật** (`nightmare_island_east_magic_island`) | Đảo Ác Mộng | bãi quái | 25–30 | 12 | 1 | 2 | Trại Tàn Sinh | có |
| **Phế Tích Cổ Thành** (`nightmare_island_ruins`) | Đảo Ác Mộng | bãi quái | 25–30 | 10 | 1 | 1 | Trại Tàn Sinh | có |
| **Cổng Tai Kiếp** (`nightmare_island_disaster_gate`) | Đảo Ác Mộng | bãi quái | 25–30 | 10 | 0 | 1 | Trại Tàn Sinh | có |
| **Oán Linh Hải Đạo** (`nightmare_island_resentment_path`) | Đảo Ác Mộng | bãi quái | 25–30 | 12 | 1 | 2 | Trại Tàn Sinh | có |
| **Tuyệt Vọng Hải Địa** (`nightmare_island_despair_land`) | Đảo Ác Mộng | bãi quái | 25–30 | 12 | 1 | 1 | Trại Tàn Sinh | có |
| **Trạm Canh Lăng** (`tomb_region_camp`) | Lăng Mộ | hub an toàn | — | 0 | 4 | 3 | Trạm Canh Lăng | có |
| **Oán Linh Cổ Đạo** (`tomb_region_resentment_path`) | Lăng Mộ | bãi quái | 30–35 | 15 → 14 | 1 | 2 | Trạm Canh Lăng | có |
| **Tuyệt Vọng Chi Địa** (`tomb_region_despair_path`) | Lăng Mộ | bãi quái | 30–35 | 15 → 14 | 0 | 2 | Trạm Canh Lăng | có |
| **Tàn Tích Tịch Diệt** (`tomb_region_dead_ruins`) | Lăng Mộ | bãi quái | 30–35 | 0 → 12 | 0 | 2 | Trạm Canh Lăng | có |
| **Thâm Cung Tịch Diệt** (`tomb_region_deep_ruins`) | Lăng Mộ | bãi quái | 30–35 | 0 → 12 | 0 | 1 | Trạm Canh Lăng | có |
| **Thần Lăng Vĩnh Miên** (`tomb_region_gods_tomb`) | Lăng Mộ | bãi quái | 30–35 | 0 → 14 | 1 | 1 | Trạm Canh Lăng | có |
| **Bãi Vãng Sinh** (`tomb_region_soul_cemetery`) | Lăng Mộ | bãi quái | 30–35 | 6 → 10 | 2 | 4 | Trạm Canh Lăng | có |
| **Cồn Úa Vàng** (`tomb_region_unnamed_area_01`) | Lăng Mộ | bãi quái | 30–35 | 0 → 10 | 0 | 1 | Trạm Canh Lăng | có |
| **Bãi Gai Khô** (`tomb_region_unnamed_area_02`) | Lăng Mộ | bãi quái | 30–35 | 0 → 10 | 0 | 1 | Trạm Canh Lăng | có |
| **Cổng Địa Đạo Lam Dạ** (`crossroads_unnamed_area_01`) | Giao Điểm | hub an toàn | — | 0 | 2 | 3 | Cổng Địa Đạo Lam Dạ | có |
| **Hành Lang Rêu Biếc** (`crossroads_unnamed_area_02`) | Giao Điểm | bãi quái | 35–40 | 12 | 0 | 2 | Cổng Địa Đạo Lam Dạ | có |
| **Đoạn Thủy Quang** (`crossroads_unnamed_area_03`) | Giao Điểm | bãi quái | 35–40 | 12 | 1 | 2 | Cổng Địa Đạo Lam Dạ | có |
| **Ngã Ba Đêm Xanh** (`crossroads_unnamed_area_04`) | Giao Điểm | bãi quái | 35–40 | 10 | 1 | 2 | Cổng Địa Đạo Lam Dạ | có |
| **Hốc San Hô Tím** (`crossroads_unnamed_area_05`) | Giao Điểm | bãi quái | 35–40 | 10 | 1 | 1 | Cổng Địa Đạo Lam Dạ | có |
| **Đáy Địa Đạo** (`crossroads_unnamed_area_06`) | Giao Điểm | bãi quái | 35–40 | 10 | 0 | 1 | Cổng Địa Đạo Lam Dạ | có |
| **Hải Tặc Hào** (`middle_corridor_main_hall`) | Hải Tặc Hào | hub an toàn | — | 0 | 6 | 0 | Hải Tặc Hào | có |
| **Tử Vân Lâm** (`astral_realm_unnamed_area_01`) | Tinh Không | hub an toàn | — | 0 | 2 | 4 | Tử Vân Lâm | có |
| **Thời Không Liệt Khích** (`astral_realm_spacetime_rift`) | Tinh Không | trung chuyển | — | 0 | 0 | 2 | Tử Vân Lâm | có |
| **Lối Mây Tím** (`astral_realm_unnamed_area_02`) | Tinh Không | bãi quái | 41–44 | 10 | 1 | 2 | Tử Vân Lâm | có |
| **Bờ Hồ Vân Ảnh** (`astral_realm_unnamed_area_03`) | Tinh Không | bãi quái | 45–48 | 10 | 0 | 1 | Tử Vân Lâm | có |
| **Hốc Cổ Thụ** (`astral_realm_unnamed_area_04`) | Tinh Không | bãi quái | 49–52 | 12 | 0 | 1 | Tử Vân Lâm | có |
| **Rừng Hoàng Hôn** (`astral_realm_unnamed_area_05`) | Tinh Không | bãi quái | 53–56 | 10 → 12 | 1 | 2 | Tử Vân Lâm | có |
| **Tận Cùng Thời Không** (`astral_realm_unnamed_area_06`) | Tinh Không | bãi quái | 57–60 | 12 | 0 | 1 | Tử Vân Lâm | có |
| **Tiền Sảnh Ngọc Lục** (`ancient_ruins_unnamed_area_01`) | Di Tích Cổ | hub an toàn | — | 0 | 2 | 4 | Tiền Sảnh Ngọc Lục | có |
| **Phòng Tượng Cổ** (`ancient_ruins_unnamed_area_02`) | Di Tích Cổ | bãi quái | 41–44 | 0 → 10 | 1 | 1 | Tiền Sảnh Ngọc Lục | có |
| **Phòng Tinh Thạch** (`ancient_ruins_unnamed_area_03`) | Di Tích Cổ | bãi quái | 45–48 | 0 → 10 | 0 | 1 | Tiền Sảnh Ngọc Lục | có |
| **Hành Lang Thạch Vệ** (`ancient_ruins_unnamed_area_04`) | Di Tích Cổ | bãi quái | 49–52 | 0 → 12 | 1 | 2 | Tiền Sảnh Ngọc Lục | có |
| **Thâm Sảnh Ngọc Lục** (`ancient_ruins_unnamed_area_05`) | Di Tích Cổ | bãi quái | 53–56 | 0 → 12 | 1 | 2 | Tiền Sảnh Ngọc Lục | có |
| **Tận Điện Cổ Tích** (`ancient_ruins_unnamed_area_06`) | Di Tích Cổ | bãi quái | 57–60 | 0 → 12 | 0 | 1 | Tiền Sảnh Ngọc Lục | có |
| **Cổng U Lâu** (`ghost_castle_gate`) | Lâu Đài Ma | hub an toàn | — | 0 | 2 | 2 | Cổng U Lâu | có |
| **U Linh Cổ Thành** (`ghost_castle_deep_woods`) | Lâu Đài Ma | bãi quái | Tầng 1–60 = Lv61–120 | 25 | 0 | 2 | Cổng U Lâu | có |
| **Mật Thất Cổ Thành** (`ghost_castle_ancient_city_secret_chamber`) | Lâu Đài Ma | bãi quái | Lv190–200 | 20 | 0 | 1 | Cổng U Lâu | có |
| **Thế Thụ Môn** (`world_tree_gate`) | Cây Thế Giới | hub an toàn | — | 0 | 2 | 2 | Thế Thụ Môn | có |
| **Thế Thụ Thâm Lâm** (`world_tree_deep_woods`) | Cây Thế Giới | bãi quái | Tầng 1–60 = Lv61–120 | 17 | 0 | 2 | Thế Thụ Môn | có |
| **Mật Thất Thế Thụ** (`world_tree_secret_chamber`) | Cây Thế Giới | bãi quái | Lv190–200 | 17 | 0 | 1 | Thế Thụ Môn | có |
| **Điểu Tháp** (`tower_region_main_tower`) | Tháp Chim | hub an toàn | — | 0 | 2 | 2 | Điểu Tháp | có |
| **Vân Tiêu Thiên Tầng** (`tower_region_deep_woods`) | Tháp Chim | bãi quái | Tầng 1–40 = Lv121–160 | 17 | 1 | 2 | Điểu Tháp | có |
| **Điểu Tháp Mật Tầng** (`tower_region_secret_floor`) | Tháp Chim | bãi quái | Lv122–160 (theo tầng chẵn đã vào) | 17 | 0 | 1 | Điểu Tháp | có |
| **Trường Sinh Mê Thành** (`immortal_maze_main_maze`) | Mê Thành | hub an toàn | — | 0 | 2 | 2 | Trường Sinh Mê Thành | có |
| **Bất Tử Mê Tầng** (`immortal_maze_floor`) | Mê Thành | bãi quái | Tầng 1–40 = Lv161–200 | 30 | 1 | 2 | Trường Sinh Mê Thành | có |
| **Bất Tử Mật Tầng** (`immortal_maze_secret_floor`) | Mê Thành | bãi quái | Lv162–200 (theo tầng chẵn đã vào) | 30 | 0 | 1 | Trường Sinh Mê Thành | có |
| **Thành Lũy Bang Hội** (`guild_fortress`) | Bang hội | chung theo bang | — | 0 | 1 | 6 | Quảng Trường Thạch Trụ | không |
| **Ngân Khố Bang** (`guild_treasury`) | Bang hội | chung theo bang | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
| **Kho Vật Tư Bang** (`guild_warehouse`) | Bang hội | chung theo bang | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
| **Doanh Trại Bang** (`guild_barracks`) | Bang hội | chung theo bang | — | 0 | 0 | 1 | Quảng Trường Thạch Trụ | không |
| **Quầy Hàng Bang** (`guild_shop`) | Bang hội | chung theo bang | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
| **Chuồng Linh Thú** (`guild_pet_stable`) | Bang hội | chung theo bang | — | 0 | 0 | 1 | Quảng Trường Thạch Trụ | không |
| **Chiến Địa Kết Minh** (`guild_battlefield_main_field`) | Bang hội | chung theo bang | — | 0 | 0 | 1 | Quảng Trường Thạch Trụ | không |
| **Cổ Điện Tế Lễ · Tầng I** (`maya_floor_01`) | Hoạt động / hầm ngục | instance | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
| **Địa Lao · Tầng I** (`dungeon_floor_01`) | Hoạt động / hầm ngục | instance | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
| **Đấu Trường Hỗn Mang** (`chaos_arena_main_field`) | Hoạt động / hầm ngục | instance | — | 0 | 0 | 1 | Quảng Trường Thạch Trụ | không |
| **Đấu Trường Tổ Đội** (`team_arena_main_field`) | Hoạt động / hầm ngục | instance | — | 0 | 0 | 1 | Quảng Trường Thạch Trụ | không |
| **Sảnh Đối Quyết Lang Dương** (`wolf_sheep_waiting_hall`) | Sói–Cừu | trung chuyển | — | 0 | 0 | 1 | Quảng Trường Thạch Trụ | không |
| **Dương Xá** (`wolf_sheep_sheep_house`) | Sói–Cừu | instance | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
| **Dương Lan** (`wolf_sheep_sheep_pen`) | Sói–Cừu | instance | — | 0 | 0 | 2 | Quảng Trường Thạch Trụ | không |
| **Bãi Tranh Đoạt** (`wolf_sheep_middle_field`) | Sói–Cừu | instance | — | 0 | 1 | 2 | Quảng Trường Thạch Trụ | không |
| **Lang Huyệt** (`wolf_sheep_wolf_pen`) | Sói–Cừu | instance | — | 0 | 0 | 2 | Quảng Trường Thạch Trụ | không |
| **Lang Sào** (`wolf_sheep_wolf_house`) | Sói–Cừu | instance | — | 0 | 1 | 1 | Quảng Trường Thạch Trụ | không |
