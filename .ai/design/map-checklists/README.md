# Checklist asset theo map — Phimond HD-2D (cho Codex)

Sinh bởi `tools/build-web-assets/gen_map_asset_checklists.py` (chạy lại để cập nhật trạng thái). 92 map / 21 kit.

## Cách dùng với Codex

1. **Cài agent-sprite-forge** (bắt buộc): https://github.com/0x0funky/agent-sprite-forge — Codex: `git clone https://github.com/0x0funky/agent-sprite-forge.git && cd agent-sprite-forge && python -m pip install -r requirements.txt && python tools/install_skills.py --apply --host codex`, rồi mở phiên Codex mới. Bản đã dùng cho batch-00: commit `5324342fdfab72430f4e9604f3fe427009f8596d` (skills ở `~/.codex/skills/`). Cần Python ≥3.10, numpy/Pillow/scipy, ffmpeg ≥5.1.
2. Kiểm route ảnh: `python "<generate2dmedia>/scripts/route_media.py" resolve --kind image` phải ra route image_gen/Codex đã đăng nhập; `forge_doctor.py` báo cấu hình. Nếu route rơi về `codeart2d` → DỪNG và báo (codeart2d chỉ là phương án cuối, bị cấm ở đây).
3. Skills: `generate2dmap` (tile, prop kit, tách/kiểm seam), `generate2dsprite` (prop, icon, FX, đóng gói khung + pixel finish `finish_frames.py`), `generate2dmedia` (định tuyến). Mỗi asset: raw-01 giữ nguyên → cắt/khử nền/finish bằng script forge → `final.png`.
4. Làm theo thứ tự ở bảng trạng thái. Mỗi kit: đọc `kit-<tên>.md`, rà bảng, vẽ theo sheet 6 vật, cập nhật cột Vẽ, chạy `python3 tools/hd2d_audit/art_gate.py batch-11-<kit>`.
5. Luật chung: `.ai/design/gpt-redo/00-master-v2.md` (style DNA, lỗi đã bị trả, tỉ lệ: người chơi = 1.31 đơn vị, bảng cỡ ở `tools/hd2d_audit/size_check.py`). Ảnh gốc từng map nằm ngay trong kit file (đính kèm vào image_gen là bắt buộc).
6. KHÔNG: codeart2d, API trả phí, vẽ bằng code, lật gương, đổi màu để thành asset mới, commit, sửa runtime/gate/waivers. CHỈ Claude/owner đánh "Duyệt".

## Trạng thái chung (v1.0.0: đang hoàn thiện Rừng, Hoàng Cung, Sa Mạc)

| Kit | Map | Asset có | Duyệt | Việc |
|---|---|---|---|---|
| [forest](kit-forest.md) Rừng Lục Bảo | 2 | 62 | 61 | ĐANG HOÀN THIỆN (v1.0.0) |
| [city](kit-city.md) Thành phố, Hoàng Cung, nội thất, trang trại, đấu trường | 9 | 143 | 89 | ĐANG HOÀN THIỆN Hoàng Cung/thành (v1.0.0); phòng còn lại rà lại |
| [beach](kit-beach.md) Bãi biển châu báu | 5 | 61 | 57 | rà lại cho v1.0.x |
| [ship](kit-ship.md) Tàu cướp biển | 1 | 21 | 21 | rà lại |
| [desert](kit-desert.md) Hoang mạc | 6 | 98 | 0 | ĐANG HOÀN THIỆN (GPT vẽ lại, nháp) |
| [windrock](kit-windrock.md) Núi Phong Thạch | 6 | 74 | 0 | VẼ LẠI (bản Gemini bị trả) |
| [nightmare](kit-nightmare.md) Đảo Ác Mộng | 6 | 12 | 0 | ĐANG VẼ: 6 prop chung + 6 landmark nháp; kit/cảnh chưa hoàn tất |
| [tomb](kit-tomb.md) Lăng Mộ | 9 | 11 | 0 | VẼ ĐỦ KIT (pilot Gemini) |
| [crossroads](kit-crossroads.md) Ngã Tư / Địa Đạo | 6 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [astral](kit-astral.md) Tinh Giới | 7 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [ancient](kit-ancient.md) Cổ Tích | 6 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [ghost_castle](kit-ghost_castle.md) Lâu Đài Ma | 3 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [world_tree](kit-world_tree.md) Cây Thế Giới | 3 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [tower](kit-tower.md) Điểu Tháp | 3 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [maze](kit-maze.md) Mê Thành Bất Tử | 3 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [guild](kit-guild.md) Bang Hội | 6 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [battlefield](kit-battlefield.md) Chiến Địa Kết Minh | 1 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [maya](kit-maya.md) Điện Thờ Maya · Tầng I | 1 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [dungeon](kit-dungeon.md) Địa Lao · Tầng I | 1 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [arena2](kit-arena2.md) Đấu Trường Hỗn Mang / Tổ Đội | 2 | 0 | 0 | CHƯA CÓ asset — vẽ mới |
| [minigame](kit-minigame.md) Sói – Cừu | 6 | 0 | 0 | CHƯA CÓ asset — vẽ mới |

## Map → file

- **forest**: [`emerald_forest_main_woods`](kit-forest.md#emerald_forest_main_woods), [`emerald_forest_deep_woods`](kit-forest.md#emerald_forest_deep_woods)
- **city**: [`city_square`](kit-city.md#city_square), [`city_market`](kit-city.md#city_market), [`city_palace_gate`](kit-city.md#city_palace_gate), [`city_royal_palace`](kit-city.md#city_royal_palace), [`city_activity_hall`](kit-city.md#city_activity_hall), [`city_pet_room`](kit-city.md#city_pet_room), [`city_farm`](kit-city.md#city_farm), [`city_deathmatch_arena`](kit-city.md#city_deathmatch_arena), [`summoning_hall_main_hall`](kit-city.md#summoning_hall_main_hall)
- **beach**: [`treasure_beach_fishermen_beach`](kit-beach.md#treasure_beach_fishermen_beach), [`treasure_beach_east_beach`](kit-beach.md#treasure_beach_east_beach), [`treasure_beach_west_beach`](kit-beach.md#treasure_beach_west_beach), [`treasure_beach_deep_sea`](kit-beach.md#treasure_beach_deep_sea), [`treasure_beach_prosperity_island`](kit-beach.md#treasure_beach_prosperity_island)
- **ship**: [`middle_corridor_main_hall`](kit-ship.md#middle_corridor_main_hall)
- **desert**: [`desert_shicheng_ruins`](kit-desert.md#desert_shicheng_ruins), [`desert_entrance`](kit-desert.md#desert_entrance), [`desert_sealed_land`](kit-desert.md#desert_sealed_land), [`desert_hulu_tribe`](kit-desert.md#desert_hulu_tribe), [`desert_barren_sands`](kit-desert.md#desert_barren_sands), [`desert_disaster_sands`](kit-desert.md#desert_disaster_sands)
- **windrock**: [`windrock_mountain_camp`](kit-windrock.md#windrock_mountain_camp), [`windrock_mountain_stone_bridge`](kit-windrock.md#windrock_mountain_stone_bridge), [`windrock_mountain_howling_canyon`](kit-windrock.md#windrock_mountain_howling_canyon), [`windrock_mountain_mountain_range`](kit-windrock.md#windrock_mountain_mountain_range), [`windrock_mountain_mountain_path`](kit-windrock.md#windrock_mountain_mountain_path), [`windrock_mountain_summit`](kit-windrock.md#windrock_mountain_summit)
- **nightmare**: [`nightmare_island_survivor_camp`](kit-nightmare.md#nightmare_island_survivor_camp), [`nightmare_island_east_magic_island`](kit-nightmare.md#nightmare_island_east_magic_island), [`nightmare_island_ruins`](kit-nightmare.md#nightmare_island_ruins), [`nightmare_island_disaster_gate`](kit-nightmare.md#nightmare_island_disaster_gate), [`nightmare_island_resentment_path`](kit-nightmare.md#nightmare_island_resentment_path), [`nightmare_island_despair_land`](kit-nightmare.md#nightmare_island_despair_land)
- **tomb**: [`tomb_region_camp`](kit-tomb.md#tomb_region_camp), [`tomb_region_resentment_path`](kit-tomb.md#tomb_region_resentment_path), [`tomb_region_despair_path`](kit-tomb.md#tomb_region_despair_path), [`tomb_region_dead_ruins`](kit-tomb.md#tomb_region_dead_ruins), [`tomb_region_deep_ruins`](kit-tomb.md#tomb_region_deep_ruins), [`tomb_region_gods_tomb`](kit-tomb.md#tomb_region_gods_tomb), [`tomb_region_soul_cemetery`](kit-tomb.md#tomb_region_soul_cemetery), [`tomb_region_unnamed_area_01`](kit-tomb.md#tomb_region_unnamed_area_01), [`tomb_region_unnamed_area_02`](kit-tomb.md#tomb_region_unnamed_area_02)
- **crossroads**: [`crossroads_unnamed_area_01`](kit-crossroads.md#crossroads_unnamed_area_01), [`crossroads_unnamed_area_02`](kit-crossroads.md#crossroads_unnamed_area_02), [`crossroads_unnamed_area_03`](kit-crossroads.md#crossroads_unnamed_area_03), [`crossroads_unnamed_area_04`](kit-crossroads.md#crossroads_unnamed_area_04), [`crossroads_unnamed_area_05`](kit-crossroads.md#crossroads_unnamed_area_05), [`crossroads_unnamed_area_06`](kit-crossroads.md#crossroads_unnamed_area_06)
- **astral**: [`astral_realm_unnamed_area_01`](kit-astral.md#astral_realm_unnamed_area_01), [`astral_realm_spacetime_rift`](kit-astral.md#astral_realm_spacetime_rift), [`astral_realm_unnamed_area_02`](kit-astral.md#astral_realm_unnamed_area_02), [`astral_realm_unnamed_area_03`](kit-astral.md#astral_realm_unnamed_area_03), [`astral_realm_unnamed_area_04`](kit-astral.md#astral_realm_unnamed_area_04), [`astral_realm_unnamed_area_05`](kit-astral.md#astral_realm_unnamed_area_05), [`astral_realm_unnamed_area_06`](kit-astral.md#astral_realm_unnamed_area_06)
- **ancient**: [`ancient_ruins_unnamed_area_01`](kit-ancient.md#ancient_ruins_unnamed_area_01), [`ancient_ruins_unnamed_area_02`](kit-ancient.md#ancient_ruins_unnamed_area_02), [`ancient_ruins_unnamed_area_03`](kit-ancient.md#ancient_ruins_unnamed_area_03), [`ancient_ruins_unnamed_area_04`](kit-ancient.md#ancient_ruins_unnamed_area_04), [`ancient_ruins_unnamed_area_05`](kit-ancient.md#ancient_ruins_unnamed_area_05), [`ancient_ruins_unnamed_area_06`](kit-ancient.md#ancient_ruins_unnamed_area_06)
- **ghost_castle**: [`ghost_castle_gate`](kit-ghost_castle.md#ghost_castle_gate), [`ghost_castle_deep_woods`](kit-ghost_castle.md#ghost_castle_deep_woods), [`ghost_castle_ancient_city_secret_chamber`](kit-ghost_castle.md#ghost_castle_ancient_city_secret_chamber)
- **world_tree**: [`world_tree_gate`](kit-world_tree.md#world_tree_gate), [`world_tree_deep_woods`](kit-world_tree.md#world_tree_deep_woods), [`world_tree_secret_chamber`](kit-world_tree.md#world_tree_secret_chamber)
- **tower**: [`tower_region_main_tower`](kit-tower.md#tower_region_main_tower), [`tower_region_deep_woods`](kit-tower.md#tower_region_deep_woods), [`tower_region_secret_floor`](kit-tower.md#tower_region_secret_floor)
- **maze**: [`immortal_maze_main_maze`](kit-maze.md#immortal_maze_main_maze), [`immortal_maze_floor`](kit-maze.md#immortal_maze_floor), [`immortal_maze_secret_floor`](kit-maze.md#immortal_maze_secret_floor)
- **guild**: [`guild_fortress`](kit-guild.md#guild_fortress), [`guild_treasury`](kit-guild.md#guild_treasury), [`guild_warehouse`](kit-guild.md#guild_warehouse), [`guild_barracks`](kit-guild.md#guild_barracks), [`guild_shop`](kit-guild.md#guild_shop), [`guild_pet_stable`](kit-guild.md#guild_pet_stable)
- **battlefield**: [`guild_battlefield_main_field`](kit-battlefield.md#guild_battlefield_main_field)
- **maya**: [`maya_floor_01`](kit-maya.md#maya_floor_01)
- **dungeon**: [`dungeon_floor_01`](kit-dungeon.md#dungeon_floor_01)
- **arena2**: [`chaos_arena_main_field`](kit-arena2.md#chaos_arena_main_field), [`team_arena_main_field`](kit-arena2.md#team_arena_main_field)
- **minigame**: [`wolf_sheep_waiting_hall`](kit-minigame.md#wolf_sheep_waiting_hall), [`wolf_sheep_sheep_house`](kit-minigame.md#wolf_sheep_sheep_house), [`wolf_sheep_sheep_pen`](kit-minigame.md#wolf_sheep_sheep_pen), [`wolf_sheep_middle_field`](kit-minigame.md#wolf_sheep_middle_field), [`wolf_sheep_wolf_pen`](kit-minigame.md#wolf_sheep_wolf_pen), [`wolf_sheep_wolf_house`](kit-minigame.md#wolf_sheep_wolf_house)

## NPC (batch-05)

- 58 NPC đang dùng chung sprite với NPC khác (xem `.ai/design/gpt-redo/04-batch-05-npc-redo.md`). Mỗi map liệt kê NPC roster; Codex chỉ vẽ lại NPC trùng.

### Cập nhật 2026-10-24 — khởi động các kit chưa vẽ

[Hàng đợi 54 map / 14 kit](REDRAW-QUEUE-20261024.md). Đảo Ác Mộng có 12 asset đầu tiên đã tự xem4×, tất cả chờ owner/Claude duyệt; 13 kit tiếp theo vẫn chưa bắt đầu. Gói này chưa gồm nền/cổng/FX hoặc scene hoàn chỉnh.
