# Checklist asset theo map — Phimond HD-2D (cho Codex)

Sinh bởi `tools/build-web-assets/gen_map_asset_checklists.py` (chạy lại để cập nhật trạng thái). 92 map / 21 kit.

## Nghiệm thu Claude 2026-11-09 (cập nhật tay; giữ nguyên lịch sử bên dưới)

Báo cáo: [REVIEW-CLAUDE-20261109-HANDOFF.md](REVIEW-CLAUDE-20261109-HANDOFF.md) · [ASSET-VERDICTS](ASSET-VERDICTS-20261109.csv) · [MAP-COVERAGE](MAP-COVERAGE-20261109.csv) · [ROADMAP](ROADMAP-ART-92MAPS-20261109.md) · [TASKS](ROADMAP-ART-TASKS-20261109.csv).
Kết luận: **0/92 map asset-ready, 0/92 có scene proof; 23 map/8 kit chưa có art; chưa đạt 100% art plan.** Cột "Duyệt" trong bảng cũ bên dưới là cờ manifest cũ, không phải verdict hiện hành. Bảng dưới đếm verdict V1 (primary + slot), chưa 4×:

| Kit | Map | DUYỆT | SỬA | VẼ_LẠI | THIẾU slot | Trạng thái map |
|---|---:|---:|---:|---:|---:|---|
| ancient | 6 | 48 | 4 | 3 | 0 | chưa đủ |
| arena2 | 2 | 0 | 0 | 0 | 44 | CHƯA CÓ ART |
| astral | 7 | 56 | 0 | 3 | 0 | chưa đủ |
| battlefield | 1 | 0 | 0 | 0 | 50 | CHƯA CÓ ART |
| beach | 5 | 0 | 0 | 0 | 0 | chưa đủ |
| city | 9 | 0 | 0 | 0 | 0 | chưa đủ |
| crossroads | 6 | 46 | 4 | 12 | 0 | chưa đủ |
| desert | 6 | 93 | 0 | 5 | 6 | chưa đủ |
| dungeon | 1 | 0 | 0 | 0 | 47 | CHƯA CÓ ART |
| forest | 2 | 0 | 0 | 0 | 2 | chưa đủ |
| ghost_castle | 3 | 44 | 0 | 6 | 0 | chưa đủ |
| guild | 6 | 0 | 0 | 0 | 59 | CHƯA CÓ ART |
| maya | 1 | 0 | 0 | 0 | 49 | CHƯA CÓ ART |
| maze | 3 | 0 | 0 | 0 | 50 | CHƯA CÓ ART |
| minigame | 6 | 0 | 0 | 0 | 58 | CHƯA CÓ ART |
| nightmare | 6 | 47 | 0 | 20 | 0 | chưa đủ |
| ship | 1 | 0 | 0 | 0 | 1 | chưa đủ |
| tomb | 9 | 59 | 0 | 17 | 0 | chưa đủ |
| tower | 3 | 0 | 0 | 0 | 50 | CHƯA CÓ ART |
| windrock | 6 | 70 | 0 | 12 | 0 | chưa đủ |
| world_tree | 3 | 47 | 0 | 4 | 1 | chưa đủ |

## Cách dùng với Codex

1. **Cài agent-sprite-forge** (bắt buộc): https://github.com/0x0funky/agent-sprite-forge — Codex: `git clone https://github.com/0x0funky/agent-sprite-forge.git && cd agent-sprite-forge && python -m pip install -r requirements.txt && python tools/install_skills.py --apply --host codex`, rồi mở phiên Codex mới. Bản đã dùng cho batch-00: commit `5324342fdfab72430f4e9604f3fe427009f8596d` (skills ở `~/.codex/skills/`). Cần Python ≥3.10, numpy/Pillow/scipy, ffmpeg ≥5.1.
2. Kiểm route ảnh: `python "<generate2dmedia>/scripts/route_media.py" resolve --kind image` phải ra route image_gen/Codex đã đăng nhập; `forge_doctor.py` báo cấu hình. Nếu route rơi về `codeart2d` → DỪNG và báo (codeart2d chỉ là phương án cuối, bị cấm ở đây).
3. Skills: `generate2dmap` (tile, prop kit, tách/kiểm seam), `generate2dsprite` (prop, icon, FX, đóng gói khung + pixel finish `finish_frames.py`), `generate2dmedia` (định tuyến). Mỗi asset: raw-01 giữ nguyên → cắt/khử nền/finish bằng script forge → `final.png`.
4. Làm theo thứ tự ở bảng trạng thái. Mỗi kit: đọc `kit-<tên>.md`, rà bảng, vẽ theo sheet 6 vật, cập nhật cột Vẽ, chạy `python3 tools/hd2d_audit/art_gate.py batch-11-<kit>`.
5. Luật chung: `.ai/design/gpt-redo/00-master-v2.md` (style DNA, lỗi đã bị trả, tỉ lệ: người chơi = 1.31 đơn vị, bảng cỡ ở `tools/hd2d_audit/size_check.py`). Ảnh gốc từng map nằm ngay trong kit file (đính kèm vào image_gen là bắt buộc).
6. KHÔNG: codeart2d, API trả phí, vẽ bằng code, lật gương, đổi màu để thành asset mới, commit, sửa runtime/gate/waivers. CHỈ Claude/owner đánh "Duyệt".

> Cập nhật tay 29/10/2026 theo [REVIEW-20261029.md](REVIEW-20261029.md). KHÔNG chạy lại generator (ghi đè chỉnh tay).
> Cập nhật Codex 04/11/2026: art gate batch-11 quét 494 asset, 0 lỗi/0 cảnh báo. Tomb vẫn có 76 candidate, 0 owner duyệt; crypt mossstone và near backdrop chưa đạt repeat review, mid/far/near cần composite map review. Không thay manifest Tomb ở checkpoint này.

> Cập nhật Codex 30/10: Windrock có 82 draft, 0 duyệt; Lăng Mộ có 76, Ngã Tư/Địa Đạo có 62. Art gate mới nhất quét 411 asset trong 5 kit batch-11, 0 lỗi/0 cảnh báo. Edge-01..03 của Windrock và Ngã Tư đã có; landmark từng map được ánh xạ tới prop dùng chung khi nguồn không chứng minh landmark độc nhất. Chưa có kit nào được Claude/owner duyệt.
> Phạm vi review được Claude làm rõ 29/10: xem sheet floor/prop của 4 kit; chưa xem sheet backdrop. Mọi kết luận backdrop ở bảng tiến độ là theo log/QA của Codex, chưa phải Claude review bằng mắt. 3×3 repeat hiện đã mở để kiểm lưới; chưa thay cho dựng thử hoàn chỉnh trong từng map. Không kit nào được duyệt.

## Trạng thái chung (v1.0.0: đang hoàn thiện Rừng, Hoàng Cung, Sa Mạc)

| Kit | Map | Asset có | Duyệt | Việc |
|---|---|---|---|---|
| [forest](kit-forest.md) Rừng Lục Bảo | 2 | 62 | 61 | ĐANG HOÀN THIỆN (v1.0.0) |
| [city](kit-city.md) Thành phố, Hoàng Cung, nội thất, trang trại, đấu trường | 9 | 143 | 89 | ĐANG HOÀN THIỆN Hoàng Cung/thành (v1.0.0); phòng còn lại rà lại |
| [beach](kit-beach.md) Bãi biển châu báu | 5 | 61 | 57 | rà lại cho v1.0.x |
| [ship](kit-ship.md) Tàu cướp biển | 1 | 21 | 21 | rà lại |
| [desert](kit-desert.md) Hoang mạc | 6 | 98 | 0 | GPT vẽ lại, gate pass; dùng dựng thử, chưa duyệt (review 29/10) |
| [windrock](kit-windrock.md) Núi Phong Thạch | 6 | 82 | 0 | Đủ asset dùng chung theo mức tối thiểu; edge 3 mới qua gate, landmark 6 map tái dùng prop riêng; mọi asset chờ Claude/owner review |
| [nightmare](kit-nightmare.md) Đảo Ác Mộng | 6 | 67 | 0 | Edge-02/03 và far-01/02 có candidate mới, gate sạch; floor cadence và landmark-02 cần chốt; backdrops chờ Claude xem |
| [tomb](kit-tomb.md) Lăng Mộ | 9 | 76 | 0 | Candidate kit đầy đủ theo checklist; gate sạch, contact sheet mới; 18 map rows dùng chung 2 foliage props; backdrop repeat và scene composition còn owner review |
| [crossroads](kit-crossroads.md) Ngã Tư / Địa Đạo | 6 | 62 | 0 | Candidate kit đủ edge/backdrop-far, gate sạch; floors 01–03 lộ chu kỳ cụm đá trong repeat 3×3; backdrop chưa được Claude xem; map compositions chưa dựng |
| [astral](kit-astral.md) Tinh Giới | 7 | 59 | 0 | Asset kit hoàn tất, gồm 6 tree sway-split parts và 14 landmark rows map vào candidate dùng chung; 0 duyệt |
| [ancient](kit-ancient.md) Cổ Tích | 6 | 55 | 0 | Checklist vẽ đủ; 0 duyệt; cần Claude/owner review và composite map-scale backdrop |
| [ghost_castle](kit-ghost_castle.md) Lâu Đài Ma | 3 | 50 | 0 | ĐANG VẼ; 50 candidate, 0 owner duyệt. Landmark bình đồng dùng chung đã thêm; floor-extra-05 vẫn chưa đạt viền phẳng; backdrop/layout composition còn mở |
| [world_tree](kit-world_tree.md) Cây Thế Giới | 3 | 51 | 0 | ĐANG VẼ; 51 candidates, 0 owner duyệt. Edge-03 còn thiếu; edge-01/02, các floor-extra và backdrop đã có candidate nhưng còn review repeat/map-scale. Có QA composition cho 3 map; rà lại style/scale các prop và owner review trước khi đóng kit. |
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

> Cập nhật 2026-11-04: Cổ Tích có thêm 6 candidate decal ground; prompt/raw/hash/review lưu trong `batch-11-ancient/jobs/`. Chưa được owner duyệt.

> Cập nhật 2026-11-04: Cổ Tích có thêm 4 contact shadow và 2 floor variant; manifest có 42 candidate. Art gate quét 512 asset ở 7 kit batch-11, 0 lỗi/0 cảnh báo; đây là gate cơ học, chưa phải duyệt hình hay đóng kit.


> Cập nhật Codex 2026-11-04: Cổ Tích có 55 candidate; toàn bộ dòng checklist vẽ đã được hoàn thành/ánh xạ dùng lại. Art gate quét 525 asset trên 7 kit batch-11, 0 lỗi/0 cảnh báo. Chưa được owner duyệt; backdrop cần composite map-scale. Codex chuyển sang kit Lâu Đài Ma theo thứ tự.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma có 12 prop + 1 FX candidate (lửa nến 4 khung), 0 owner duyệt. Mỗi asset có raw/prompt/hash/final/review/QA; prop dùng palette 40 màu, FX dùng palette chung 40 màu, alpha nhị phân; 4× dark/checker đã xem. Art gate batch-11 quét 538 asset, 0 lỗi/0 cảnh báo. `sheet_qc` của FX có WARN `torso_drift` 2.39 (ngưỡng 2.0), do detector áp phép đo thân cây lên flame nghiêng; đã ghi trong review. Đây là candidate, kit chưa hoàn tất.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma có thêm 6 decal candidate; từng final được xem ở 4× trên nền tối/caro, 48 màu, art gate sạch. Tổng 19 candidate, 0 owner duyệt. Hai atlas sàn bị strict seam QC bác bỏ; lượt thứ hai có 7 seam lỗi, max ratio 2.77 (ngưỡng 1.25), nên không phát hành floor. Art gate quét 544 asset trong 8 kit batch-11, 0 lỗi/0 cảnh báo; QC atlas sàn là lỗi riêng của job thử và không phải asset đã phát hành.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma có thêm 4 shadow candidate; cả bốn được xem 4× trên nền tối/caro, 48 màu và alpha mềm có ghi ngoại lệ trong review. Tổng 23 candidate, 0 owner duyệt. Dải edge study không đạt lặp ngang (RGB edge delta trung bình 32.1–37.0), chưa đưa vào manifest.

> Cập nhật Codex 2026-11-04: Thêm cặp portal dormant/active, 48 màu, binary alpha, đã xem 4×; mask final khớp tuyệt đối sau khi căn alpha (XOR 0 pixel). Tổng 25 candidate, 0 owner duyệt; kit vẫn đang làm.

> Cập nhật Codex 2026-11-04: Thêm marker đến map 4 khung (48 màu dùng chung, alpha nhị phân), sheet spill/frame QC và xử lý strict đều pass, đã xem 4×. Lượt QC mặc định trước đó có WARN `safe_frame` do margin nguồn 7.0–7.6% thấp hơn mặc định 15%; không cắt biên/không spill; chạy strict lại ở 6% pass, frame đầu ra 128×128 còn lề tối thiểu 11px. Tổng 26 candidate, 0 owner duyệt.


> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm FX-02 (rune + wisps) và FX-03 (bụi rune/tia sáng), mỗi asset 4 khung, palette 40 màu, alpha nhị phân, đã xem 4× tối/caro. Tổng 28 candidate, 0 owner duyệt. Spill có WARN `safe_frame` ở 3 ô FX-02; không cắt/spill. Character-specific frame QC báo FAIL `identity_head_ratio` và WARN `torso_drift` cho cả hai FX; số đo được lưu, không áp dụng cho VFX. Art gate chạy sau khi manifest/contact sheet cập nhật.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma có 29 candidate, thêm `ghost_castle-floor-01` sàn cẩm thạch đen 512×512, 40 màu. Terrain QC pass (contrast 0.0414; wrap x 0.9097/y 0.7603; không warning), mosaic 3×3 đã xem và không thấy grid rõ. `seamless_verified=false` theo giới hạn công cụ; chưa owner duyệt.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma hiện có 30 candidate, 0 owner duyệt. Bổ sung floor-02 thảm nhung đỏ rượu, palette 40 màu; contrast 0.0459, wrap x 1.2199/y 0.8818, QC pass; mosaic 3×3 đã xem. Họa tiết mòn lặp khá rõ, cần bố trí map để tránh lặp thẳng hàng.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm floor-03 đất nghĩa địa/cỏ khô, 40 màu, QC seamless pass và mosaic 3×3 đã xem. Họa tiết cỏ lặp thấy rõ nên cần phá cụm bằng variants/decal khi lát map. Tổng 31 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm floor-extra-01 đá lát than; palette 40 màu, terrain QC pass, mosaic 3×3 đã xem. Họa tiết lát lặp rõ nhưng mạch nối liền; dùng như alternate thưa. Tổng 32 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm floor-extra-02 đá cuội ẩm/rêu thưa; 40 màu, QC terrain pass, mosaic 3×3 đã xem. Tổng 33 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm floor-extra-03 đất tro/mảnh slate thưa; 40 màu, terrain QC pass và mosaic 3×3 đã xem. Cụm rubble lặp rõ nên cần xen kẽ texture khác. Tổng 34 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm floor-extra-04 phiến obsidian chéo; 40 màu, QC pass, mosaic 3×3 đã xem. Motif chéo lặp rõ nên dùng xen kẽ. Tổng 35 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm `ghost_castle-floor-extra-05`, khảm đá cẩm thạch bát giác 512×512, 40 màu; terrain QC pass (contrast 0.055168, seam x 0.095335/y 1.0, không cảnh báo), mosaic 3×3 và ảnh chi tiết 4× đã xem. Motif lặp đều. QA phát hiện outer8_uniform=false so với rule mép tile; giữ candidate để theo dõi, chưa compliant hoàn toàn và chưa owner duyệt. Manifest/contact sheet cập nhật; art gate 561 asset, 0 lỗi/0 cảnh báo.

> Cập nhật Codex 2026-11-04: Lâu Đài Ma thêm `ghost_castle-edge-01`, dải đất nghĩa trang → đá cẩm thạch nứt 512×128/40 màu; seam ngang 0.807923, repeat 3×/chi tiết 4× đã xem. Hai lượt trước bị loại do đầu dải không tương thích/seam 1.7866. Motif cụm đá lặp rõ nên cần xen kẽ. Kit 37 candidate, 0 owner duyệt; art gate 562 asset, 0 lỗi/0 cảnh báo.

> Cập nhật Codex 2026-11-05: Lâu Đài Ma thêm landmark `ghost_castle_gate-landmark-01`, huy hiệu gargoyle có cánh diễn giải từ ảnh cổng (không tuyên bố trích xuất sprite gốc), 447×219, 40 màu nhìn thấy, alpha nhị phân, lề 8 px. Đã xem chi tiết 4× trên nền tối/caro và contact sheet; manifest có 43 candidate, 0 owner duyệt. Art gate quét 568 asset trong 8 kit batch-11, 0 lỗi/0 cảnh báo. Kit vẫn mở: decal-07, edge-02/03, ba backdrop, floor-extra-05 cần redraw, landmark/composite của hai map còn lại và owner review.

> Cập nhật Codex 2026-11-05: Lâu Đài Ma thêm decal-07 (bồ hóng/tro xám) bản redraw trung tính, 939×639, 40 màu, alpha nhị phân, lề 9 px; final đã xem 4× trên nền caro/tối. Các lần sinh trước bị loại do sắc lavender và sai tỉ lệ được giữ trong jobs, không vào manifest. Manifest có 44 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: Lâu Đài Ma thêm edge-02 512×128 (thảm rách → marble), seam ratio 0.710037, 3× repeat đã xem. Manifest khai `tileable: x` như edge-01; lỗi bbox-edge cũ do metadata thiếu, không sửa gate/waiver. Còn junction dọc nhẹ để kiểm trong composition. Tổng 45 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: Ghost Castle edge-03 hoàn thành candidate đất nghĩa địa/cobble → thảm rách 512×128, 40 màu; seam ratio 1.000/1.25, repeat 3× và chi tiết 4× đã xem. Mật độ họa tiết lặp nhìn thấy; cần map composition để tránh kéo dải quá dài. Tổng 46 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: Ghost Castle thêm backdrop-far-01 1280×384, 40 màu, 64 px/unit, ngang lặp. Seam mean 2.03 so với ngưỡng 14; repeat 3× không lộ mối nối. Castle/trăng lặp theo mỗi tile, cần kiểm khoảng lặp trong composition. 47 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: Ghost Castle thêm backdrop-mid-01 (twisted yews + tường marble), 1280×384/40 màu, alpha nhị phân, seam mean 6.61 < 14; repeat 3× không lộ mối nối. Far-mid preview cho thấy lớp giữa che lâu đài xa ở alignment mặc định; cần map-scale composition/parallax review. Tổng 48 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: Ghost Castle backdrop-near-01 hoàn thành 1280×384/40 màu, alpha nhị phân, seam mean 12.81 < 14; repeat 3× đã xem. Ghép far/mid/near cho thấy lớp giữa che castle xa ở alignment mặc định; composition cần chỉnh offset. Tổng 49 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `world_tree-prop-06`, lá paddle khổng lồ 512×304/39 màu, alpha nhị phân, lề 8 px, `sway:true`; final đã xem 4×. Manifest/contact sheet có 6 candidate, 0 owner duyệt. Floor-01 chưa compliant; kit còn nhiều asset và landmark/composition.

> Cập nhật Codex 2026-11-06: World Tree có 51 candidate, 0 owner duyệt. `floor-extra-05` là candidate phụ. Edge-01 có candidate tạm (40 màu, seam 10.586/3.734); edge-02 có candidate tạm từ attempt 03 crop 02 (37 màu, seam 17.768/17.630, limit tương đối 28.208). Cả hai còn cadence hiển thị trong repeat, cần ghép map-scale và Claude review. Edge-01 attempts 12–21 khác và edge-02 attempts 01–03 khác chưa đạt; crop đầu attempt 17 đã rút sau `SEAM_X 17.6/4.3`. Edge-03 attempts 01–03 chưa đạt. Backdrop far-01/02 đã có candidate, chờ composite map-scale/owner review.

> Cập nhật Codex 2026-11-05: World Tree thêm nấm tán vàng khổng lồ `prop-07`, 512×480/38 màu, binary alpha, lề ngang 8 px; final đã xem 4×. Lượt đầu viền đỏ và lượt edit nền trắng bị loại, không đăng ký. Manifest hiện 7 candidate; 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `prop-08` quả thần pulse 4 khung, atlas 512×128, frame 128×128, palette 40 màu, alpha nhị phân; registration ổn định, đã xem 4×. Tổng 8 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `prop-09` cổng vòm cành sống 512×384/35 màu; lỗ giữa trong suốt, binary alpha, 8px lề; xem 4×. Candidate thứ 9, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `prop-10` bậc cành sáu cấp 512×384/29 màu, binary alpha, đã xem 4×. Tổng 10 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `prop-11` dây leo treo 256×512/36 màu, binary alpha, `sway:true`, xem 4×. Tổng 11 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `prop-12` đom đóm 4 frame, atlas 512×128, 128×128/frame, 39 màu, binary alpha; frame alignment lệch ≤1px, xem 4×. Candidate thứ 12, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-01` cụm lá rụng/vụn vỏ, 384×256/39 màu, binary alpha, xem 4×. Tổng 13 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-02` cụm rêu và đầu rễ cuộn, 384×256/34 màu, binary alpha, xem 4×. Tổng 14 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-03` mảnh vỏ và hạt hổ phách, 384×256/35 màu, binary alpha, xem 4×. Tổng 15 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `shadow-01`, bóng canopy 512×256/40 RGB, alpha mềm có chủ đích; xem 4×. Tổng 16 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-04` vòng tăng trưởng vỏ đứt đoạn, 384×384/38 màu, binary alpha, xem 4×. Tổng 17 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-05` vệt nhựa hổ phách/vụn vỏ, 384×256/40 màu, binary alpha, xem 4×. Tổng 18 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `shadow-02`, bóng rễ chéo 512×256/40 RGB, alpha mềm; cần kiểm tra tương phản khi đặt dưới nền bark. Tổng 19 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-06` mảng vỏ có rãnh rễ/rêu, 384×256/36 màu, binary alpha, đã xem 4×. Tổng 20 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-07` dăm vỏ xoắn/rêu/vỏ hạt rỗng, 384×256/39 màu, binary alpha, xem 4×. Tổng 21 candidate, 0 owner duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `world_tree-decal-08`, nhựa cây hổ phách/dăm vỏ/rêu, 384×256/40 màu, alpha nhị phân, lề 8 px; final xem 4× và ghép trên floor-01. Màu hổ phách nổi mạnh, chờ owner đánh giá cách dùng. Manifest: 26 candidates, 0 duyệt. Hai thử tile mới của floor-02/03 bị loại do cadence/lưới lặp; shadow-04 bị loại vì nặng màu trong composition.

> Bổ sung thử nghiệm World Tree 2026-11-05: `edge-01` attempt 01 loại do hoa hồng ngoài palette/tỉ lệ 3:1; attempt 02 loại vì motif rễ-bụi lặp dày, seam 16px=14.732. Cả hai raw/prompt/review nằm trong jobs; edge-01 vẫn chưa có candidate.

> Cập nhật Codex 2026-11-05: World Tree thêm cặp `portal-dormant`/`portal-active`, mỗi 512×384/40 màu, alpha nhị phân; lối giữa trong suốt, active dùng mask dormant y hệt (IoU 1.0). Đã xem 4× caro/tối; rune active sáng, chờ owner xem map-scale. Manifest: 28 candidates, 0 duyệt.

> Cập nhật Codex 2026-11-05: World Tree có candidate `floor-02` rêu xanh ngọc 512×512/40 màu, seam X=4.323/Y=5.340, mosaic 3×3 không lộ lưới. Outer8 chưa phẳng, cadence hơi đều; chưa owner duyệt. Manifest 29 candidate.

> Cập nhật Codex 2026-11-05: thêm `world_tree-floor-03`, nền olive với mảnh lá/vỏ vụn nhỏ, 512×512/40 màu, seam X=2.781/Y=3.122, corr với floor-02=0.111; 3×3 không lộ lưới. Lá vụn nhẹ, outer8 không phẳng; chờ owner review. World Tree: 30 candidate, 0 duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `decal-11`, vỏ hạt thần nứt đôi với hạt vàng rơi, 384×256/40 màu, alpha nhị phân, lề 8px; final xem 4× caro/tối. Ba study `floor-extra-01` bị loại vì palette cát, cadence sọc hoặc lưới mảng vỏ; giữ dưới `jobs/`. Manifest/contact sheet hiện 31 candidate, 0 duyệt. Art gate: 606 asset/9 kit, 0 lỗi/0 cảnh báo; chưa phải duyệt hình.

> Cập nhật Codex 2026-11-05: World Tree thêm marker đến 4 khung `world_tree-marker-arrival`, vòng rune lá phẳng và sparkle chạy vòng, atlas 512×128/40 màu, alpha nhị phân; 4× caro/tối đã xem. Lượt đầu bị loại vì giống portal đứng, lưu trong jobs. Manifest/contact sheet 32 candidates, 0 duyệt.

> Cập nhật Codex 2026-11-05: World Tree thêm `shadow-04`, bóng tán dappled 512×256/40 màu, alpha mềm; alpha≤32 spill đã loại theo cùng ngưỡng shadow-01. Đã xem 4× caro/tối; bóng diffuse nên owner cần kiểm tra tương phản trên map. Candidate chưa duyệt. Manifest: 33 asset.

> Cập nhật Codex 2026-11-05: thêm `world_tree-decal-12`, cụm mầm cây non ba nhánh, 384×256/40 màu, alpha nhị phân, lề 8px; đã xem 4× caro/tối. Manifest 34 candidate, 0 duyệt.

> Cập nhật Codex 2026-11-05: thêm far backdrop-01 thân cây xa và skyline tán, 1280×384/40 màu, seam X=9.817; tile mosaic 3×1 không lộ join nhưng cadence thân cây lặp thấy rõ. Candidate chờ map-scale review. World Tree: 35 asset.

> Cập nhật Codex 2026-11-05: thêm far backdrop-02 skyline tán xa 1280×384/40 màu, seam X=2.518; tile mosaic 3×1 không lộ join, cadence mảng tán lặp. World Tree: 36 candidates.

> Cập nhật Codex 2026-11-05: thêm backdrop-mid thân cây/cành ngang, 1280×384/40 màu, alpha nhị phân, seam X=9.516, 3×1 không lộ join; cadence thân cây rõ và cần offset/map-scale. World Tree: 37 candidate.

> Cập nhật Codex 2026-11-05: thêm near backdrop thân cây đóng khung hai mép, 1280×384/40 màu, alpha nhị phân, seam X=5.378, repeat 3×1 không lộ join; motif lặp cần offset. World Tree: 38 candidate.
