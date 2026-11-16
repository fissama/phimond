# Roadmap art 92 map / 21 kit — Claude, 2026-11-09

Nguồn sự thật: [ROADMAP-ART-TASKS-20261109.csv](ROADMAP-ART-TASKS-20261109.csv) (672 task; mỗi task có prompt copy-paste, ảnh đính kèm, output path, spec, nghiệm thu), [ASSET-VERDICTS](ASSET-VERDICTS-20261109.csv), [MAP-COVERAGE](MAP-COVERAGE-20261109.csv), [REVIEW](REVIEW-CLAUDE-20261109-HANDOFF.md).

## 1. Yêu cầu bắt buộc vs đề xuất của reviewer

**Bắt buộc (từ owner/Master v2):** art HD-2D kiểu Octopath, giữ chủng loại vật thể/landmark/bảng màu của map gốc; 128 px = 1 đv (backdrop 64 px); 33–48 màu; alpha nhị phân, lề ≥8 px; sàn 512² seamless, viền phẳng 8 px, mỗi biến thể texture khác; không bóng/glow/chữ/magenta nướng; decal bất quy tắc; portal dormant/active cùng mask; không lật gương/đổi màu; chỉ Claude/owner duyệt; ảnh đính kèm trực tiếp vào từng request (không zip).

**Đề xuất reviewer (có thể chỉnh):** thứ tự M0→M12; gom batch nhỏ theo loại asset để một lỗi không lặp hàng chục lần; arena2/minigame vẽ sau battlefield/guild vì dùng chung ảnh; mỗi kit mới bắt đầu bằng BRIEF-<kit> (viết lại danh sách theo ảnh gốc).

## 2. Thứ tự milestone

| Milestone | Nội dung | Số task | Batch |
|---|---|---:|---|
| M0 | FIX metadata/provenance + xem lại | 58 | M0-a metadata (48); M0-b xem lại (10) |
| M1 | World Tree + Garden redraw | 10 | M1-a world_tree (5); M1-b garden (5) |
| M2 | Sửa lỗi kit đã có | 88 | M2-ancient-a floor (2); M2-ancient-b edge (1); M2-astral-a floor (2); M2-astral-b edge (1); M2-crossroads-a floor (8); M2-crossroads-e other (1); M2-crossroads-b edge (3); M2-desert-a floor (5); M2-ghost_castle-a floor (3); M2-ghost_castle-b edge (2); M2-ghost_castle-d backdrop (1); M2-nightmare-a floor (8); M2-nightmare-c decal (6); M2-nightmare-b edge (2); M2-nightmare-d backdrop (4); M2-tomb-e other (9); M2-tomb-a floor (5); M2-tomb-b edge (3); M2-windrock-a floor (9); M2-windrock-b edge (3); M2-p01-e other (6); M2-p01-d backdrop (1); M2-p01-c decal (1); M2-p01 (2) |
| M3 | Landmark thiếu của kit đã có | 9 | M3 landmark (9) |
| M4 | Kit mới: tower | 51 | M4-0 brief (1); M4-a floor+edge (11); M4-b prop (10); M4-d backdrop (4); M4-c decal+shadow (16); M4-e portal+marker+fx (6); M4-f landmark (3) |
| M5 | Kit mới: maze | 51 | M5-0 brief (1); M5-a floor+edge (11); M5-b prop (10); M5-d backdrop (4); M5-c decal+shadow (16); M5-e portal+marker+fx (6); M5-f landmark (3) |
| M6 | Kit mới: guild | 60 | M6-0 brief (1); M6-a floor+edge (11); M6-b prop (16); M6-d backdrop (4); M6-c decal+shadow (16); M6-e portal+marker+fx (6); M6-f landmark (6) |
| M7 | Kit mới: battlefield | 51 | M7-0 brief (1); M7-a floor+edge (11); M7-b prop (12); M7-d backdrop (4); M7-c decal+shadow (16); M7-e portal+marker+fx (6); M7-f landmark (1) |
| M8 | Kit mới: maya | 50 | M8-0 brief (1); M8-a floor+edge (11); M8-b prop (11); M8-d backdrop (4); M8-c decal+shadow (16); M8-e portal+marker+fx (6); M8-f landmark (1) |
| M9 | Kit mới: dungeon | 48 | M9-0 brief (1); M9-a floor+edge (11); M9-b prop (9); M9-d backdrop (4); M9-c decal+shadow (16); M9-e portal+marker+fx (6); M9-f landmark (1) |
| M10 | Kit mới: arena2 | 45 | M10-0 brief (1); M10-a floor+edge (11); M10-b prop (5); M10-d backdrop (4); M10-c decal+shadow (16); M10-e portal+marker+fx (6); M10-f landmark (2) |
| M11 | Kit mới: minigame | 59 | M11-0 brief (1); M11-a floor+edge (11); M11-b prop (15); M11-d backdrop (4); M11-c decal+shadow (16); M11-e portal+marker+fx (6); M11-f landmark (6) |
| M12 | Scene proof 92 map | 92 | M12 scene proof (92) |

Quy tắc đóng mỗi batch: gate batch-11 pass → Claude xem 4× caro/tối + lát thật (sàn 3×3 + offset, edge/backdrop 3×1) → ghi verdict vào ASSET-VERDICTS → mới mở batch kế. M12 (scene proof) chỉ sau khi kit tương ứng xong.

## 3. Batch theo milestone

M0 chạy ngay, không cần vẽ: 58 task (FIX-* đóng gói + VIEW-* xem lại).

### M1 — World Tree + Garden redraw

- **M1-a world_tree** (5): `world_tree-edge-01`, `world_tree-edge-02`, `world_tree-floor-extra-05`, `world_tree_gate-landmark-01`, `world_tree-edge-03`
- **M1-b garden** (5): `gd-trunk-seg-01`, `gd-trunk-seg-02`, `gd-pillar-vein-01`, `gd-seal-strip`, `gd-seal-strip-lit`

### M2 — Sửa lỗi kit đã có

- **M2-ancient-a floor** (2): `ancient-floor-01`, `ancient-floor-extra-02`
- **M2-ancient-b edge** (1): `ancient-edge-03`
- **M2-astral-a floor** (2): `astral-floor-extra-03`, `astral-floor-extra-05`
- **M2-astral-b edge** (1): `astral-edge-03`
- **M2-crossroads-a floor** (8): `crossroads-floor-01`, `crossroads-floor-02`, `crossroads-floor-03`, `crossroads-floor-05`, `crossroads-floor-04`, `crossroads-floor-extra-01`, `crossroads-floor-extra-02`, `crossroads-floor-extra-03`
- **M2-crossroads-e other** (1): `crossroads_unnamed_area_02-landmark-01`
- **M2-crossroads-b edge** (3): `crossroads-edge-01`, `crossroads-edge-02`, `crossroads-edge-03`
- **M2-desert-a floor** (5): `desert-sandstone-floor`, `desert-sand-cracked-01`, `desert-sand-cracked-02`, `desert-sunken-brick-floor`, `desert-limestone-grit-floor`
- **M2-ghost_castle-a floor** (3): `ghost_castle-floor-03`, `ghost_castle-floor-extra-01`, `ghost_castle-floor-extra-05`
- **M2-ghost_castle-b edge** (2): `ghost_castle-edge-02`, `ghost_castle-edge-03`
- **M2-ghost_castle-d backdrop** (1): `ghost_castle-backdrop-near-01`
- **M2-nightmare-a floor** (8): `nightmare-floor-01`, `nightmare-floor-02`, `nightmare-floor-03`, `nightmare-floor-extra-01`, `nightmare-floor-extra-02`, `nightmare-floor-extra-03`, `nightmare-floor-extra-04`, `nightmare-floor-extra-05`
- **M2-nightmare-c decal** (6): `nightmare-decal-03`, `nightmare-decal-04`, `nightmare-decal-06`, `nightmare-decal-08`, `nightmare-decal-09`, `nightmare-decal-10`
- **M2-nightmare-b edge** (2): `nightmare-edge-01`, `nightmare-edge-03`
- **M2-nightmare-d backdrop** (4): `nightmare-backdrop-far`, `nightmare-backdrop-mid`, `nightmare-backdrop-near`, `nightmare-backdrop-far-02`
- **M2-tomb-e other** (9): `tomb-lantern-post`, `tomb-spirit-brazier`, `tomb-glyph-stele`, `tomb-wall-sprit-torch`, `tomb-ancient-keys`, `tomb-dead-thorn-bush`, `tomb-dead-tree-stump`, `tomb-guardian-statue-head`, `tomb-hanging-censer`
- **M2-tomb-a floor** (5): `tomb-graveyard-dirt`, `tomb-floor-cracked-slate`, `tomb-floor-ashen-dust`, `tomb-floor-golden-sand`, `tomb-tile-edge-decal`
- **M2-tomb-b edge** (3): `tomb-edge-crypt-soil`, `tomb-edge-ruin-rubble`, `tomb-edge-desert-sand`
- **M2-windrock-a floor** (9): `windrock-rock-floor-01`, `windrock-rock-floor-02`, `windrock-gravel-floor`, `windrock-grass-snow-floor`, `windrock-snow-crust-floor`, `windrock-slate-floor`, `windrock-mountain-path-floor`, `windrock-scree-floor`, `windrock-rock-floor-03`
- **M2-windrock-b edge** (3): `windrock-edge-01`, `windrock-edge-02`, `windrock-edge-03`
- **M2-p01-e other** (6): `city-sacks`, `animal-pigeon-peck`, `animal-pigeon-fly`, `animal-cat`, `palace-flagpole`, `city-lion-fountain`
- **M2-p01-d backdrop** (1): `city-roofline-mid`
- **M2-p01-c decal** (1): `decal-drain`
- **M2-p01** (2): `pet-floor-wood-fine`, `palace-floor-marble`

### M3 — Landmark thiếu của kit đã có

- **M3 landmark** (9): `desert_shicheng_ruins-landmark-01`, `desert_entrance-landmark-01`, `desert_sealed_land-landmark-01`, `desert_hulu_tribe-landmark-01`, `desert_barren_sands-landmark-01`, `desert_disaster_sands-landmark-01`, `emerald_forest_main_woods-landmark-01`, `emerald_forest_deep_woods-landmark-01`, `middle_corridor_main_hall-landmark-01`

### M4 — Kit mới: tower

- **M4-0 brief** (1): `danh sách asset kit tower`
- **M4-a floor+edge** (11): `tower-floor-01`, `tower-floor-02`, `tower-floor-03`, `tower-floor-extra-01`, `tower-floor-extra-02`, `tower-floor-extra-03`, `tower-floor-extra-04`, `tower-floor-extra-05`, `tower-edge-01`, `tower-edge-02`, `tower-edge-03`
- **M4-b prop** (10): `tower-prop-01`, `tower-prop-02`, `tower-prop-03`, `tower-prop-04`, `tower-prop-05`, `tower-prop-06`, `tower-prop-07`, `tower-prop-08`, `tower-prop-09`, `tower-prop-10`
- **M4-d backdrop** (4): `tower-backdrop-far-01`, `tower-backdrop-far`, `tower-backdrop-mid`, `tower-backdrop-near`
- **M4-c decal+shadow** (16): `tower-decal-01`, `tower-decal-02`, `tower-decal-03`, `tower-decal-04`, `tower-decal-05`, `tower-decal-06`, `tower-decal-07`, `tower-decal-08`, `tower-decal-09`, `tower-decal-10`, `tower-decal-11`, `tower-decal-12`, `tower-shadow-01`, `tower-shadow-02`, … (+2; xem CSV)
- **M4-e portal+marker+fx** (6): `tower-portal-dormant`, `tower-portal-active`, `tower-marker-arrival`, `tower-fx-01`, `tower-fx-02`, `tower-fx-03`
- **M4-f landmark** (3): `tower_region_main_tower-landmark-01`, `tower_region_deep_woods-landmark-01`, `tower_region_secret_floor-landmark-01`

### M5 — Kit mới: maze

- **M5-0 brief** (1): `danh sách asset kit maze`
- **M5-a floor+edge** (11): `maze-floor-01`, `maze-floor-02`, `maze-floor-03`, `maze-floor-extra-01`, `maze-floor-extra-02`, `maze-floor-extra-03`, `maze-floor-extra-04`, `maze-floor-extra-05`, `maze-edge-01`, `maze-edge-02`, `maze-edge-03`
- **M5-b prop** (10): `maze-prop-01`, `maze-prop-02`, `maze-prop-03`, `maze-prop-04`, `maze-prop-05`, `maze-prop-06`, `maze-prop-07`, `maze-prop-08`, `maze-prop-09`, `maze-prop-10`
- **M5-d backdrop** (4): `maze-backdrop-far-01`, `maze-backdrop-far`, `maze-backdrop-mid`, `maze-backdrop-near`
- **M5-c decal+shadow** (16): `maze-decal-01`, `maze-decal-02`, `maze-decal-03`, `maze-decal-04`, `maze-decal-05`, `maze-decal-06`, `maze-decal-07`, `maze-decal-08`, `maze-decal-09`, `maze-decal-10`, `maze-decal-11`, `maze-decal-12`, `maze-shadow-01`, `maze-shadow-02`, … (+2; xem CSV)
- **M5-e portal+marker+fx** (6): `maze-portal-dormant`, `maze-portal-active`, `maze-marker-arrival`, `maze-fx-01`, `maze-fx-02`, `maze-fx-03`
- **M5-f landmark** (3): `immortal_maze_main_maze-landmark-01`, `immortal_maze_floor-landmark-01`, `immortal_maze_secret_floor-landmark-01`

### M6 — Kit mới: guild

- **M6-0 brief** (1): `danh sách asset kit guild`
- **M6-a floor+edge** (11): `guild-floor-01`, `guild-floor-02`, `guild-floor-03`, `guild-floor-04`, `guild-floor-extra-01`, `guild-floor-extra-02`, `guild-floor-extra-03`, `guild-floor-extra-04`, `guild-edge-01`, `guild-edge-02`, `guild-edge-03`
- **M6-b prop** (16): `guild-prop-01`, `guild-prop-02`, `guild-prop-03`, `guild-prop-04`, `guild-prop-05`, `guild-prop-06`, `guild-prop-07`, `guild-prop-08`, `guild-prop-09`, `guild-prop-10`, `guild-prop-11`, `guild-prop-12`, `guild-prop-13`, `guild-prop-14`, … (+2; xem CSV)
- **M6-d backdrop** (4): `guild-backdrop-far-01`, `guild-backdrop-far`, `guild-backdrop-mid`, `guild-backdrop-near`
- **M6-c decal+shadow** (16): `guild-decal-01`, `guild-decal-02`, `guild-decal-03`, `guild-decal-04`, `guild-decal-05`, `guild-decal-06`, `guild-decal-07`, `guild-decal-08`, `guild-decal-09`, `guild-decal-10`, `guild-decal-11`, `guild-decal-12`, `guild-shadow-01`, `guild-shadow-02`, … (+2; xem CSV)
- **M6-e portal+marker+fx** (6): `guild-portal-dormant`, `guild-portal-active`, `guild-marker-arrival`, `guild-fx-01`, `guild-fx-02`, `guild-fx-03`
- **M6-f landmark** (6): `guild_fortress-landmark-01`, `guild_treasury-landmark-01`, `guild_warehouse-landmark-01`, `guild_barracks-landmark-01`, `guild_shop-landmark-01`, `guild_pet_stable-landmark-01`

### M7 — Kit mới: battlefield

- **M7-0 brief** (1): `danh sách asset kit battlefield`
- **M7-a floor+edge** (11): `battlefield-floor-01`, `battlefield-floor-02`, `battlefield-floor-03`, `battlefield-floor-extra-01`, `battlefield-floor-extra-02`, `battlefield-floor-extra-03`, `battlefield-floor-extra-04`, `battlefield-floor-extra-05`, `battlefield-edge-01`, `battlefield-edge-02`, `battlefield-edge-03`
- **M7-b prop** (12): `battlefield-prop-01`, `battlefield-prop-02`, `battlefield-prop-03`, `battlefield-prop-04`, `battlefield-prop-05`, `battlefield-prop-06`, `battlefield-prop-07`, `battlefield-prop-08`, `battlefield-prop-09`, `battlefield-prop-10`, `battlefield-prop-11`, `battlefield-prop-12`
- **M7-d backdrop** (4): `battlefield-backdrop-far-01`, `battlefield-backdrop-far`, `battlefield-backdrop-mid`, `battlefield-backdrop-near`
- **M7-c decal+shadow** (16): `battlefield-decal-01`, `battlefield-decal-02`, `battlefield-decal-03`, `battlefield-decal-04`, `battlefield-decal-05`, `battlefield-decal-06`, `battlefield-decal-07`, `battlefield-decal-08`, `battlefield-decal-09`, `battlefield-decal-10`, `battlefield-decal-11`, `battlefield-decal-12`, `battlefield-shadow-01`, `battlefield-shadow-02`, … (+2; xem CSV)
- **M7-e portal+marker+fx** (6): `battlefield-portal-dormant`, `battlefield-portal-active`, `battlefield-marker-arrival`, `battlefield-fx-01`, `battlefield-fx-02`, `battlefield-fx-03`
- **M7-f landmark** (1): `guild_battlefield_main_field-landmark-01`

### M8 — Kit mới: maya

- **M8-0 brief** (1): `danh sách asset kit maya`
- **M8-a floor+edge** (11): `maya-floor-01`, `maya-floor-02`, `maya-floor-03`, `maya-floor-extra-01`, `maya-floor-extra-02`, `maya-floor-extra-03`, `maya-floor-extra-04`, `maya-floor-extra-05`, `maya-edge-01`, `maya-edge-02`, `maya-edge-03`
- **M8-b prop** (11): `maya-prop-01`, `maya-prop-02`, `maya-prop-03`, `maya-prop-04`, `maya-prop-05`, `maya-prop-06`, `maya-prop-07`, `maya-prop-08`, `maya-prop-09`, `maya-prop-10`, `maya-prop-11`
- **M8-d backdrop** (4): `maya-backdrop-far-01`, `maya-backdrop-far`, `maya-backdrop-mid`, `maya-backdrop-near`
- **M8-c decal+shadow** (16): `maya-decal-01`, `maya-decal-02`, `maya-decal-03`, `maya-decal-04`, `maya-decal-05`, `maya-decal-06`, `maya-decal-07`, `maya-decal-08`, `maya-decal-09`, `maya-decal-10`, `maya-decal-11`, `maya-decal-12`, `maya-shadow-01`, `maya-shadow-02`, … (+2; xem CSV)
- **M8-e portal+marker+fx** (6): `maya-portal-dormant`, `maya-portal-active`, `maya-marker-arrival`, `maya-fx-01`, `maya-fx-02`, `maya-fx-03`
- **M8-f landmark** (1): `maya_floor_01-landmark-01`

### M9 — Kit mới: dungeon

- **M9-0 brief** (1): `danh sách asset kit dungeon`
- **M9-a floor+edge** (11): `dungeon-floor-01`, `dungeon-floor-02`, `dungeon-floor-03`, `dungeon-floor-extra-01`, `dungeon-floor-extra-02`, `dungeon-floor-extra-03`, `dungeon-floor-extra-04`, `dungeon-floor-extra-05`, `dungeon-edge-01`, `dungeon-edge-02`, `dungeon-edge-03`
- **M9-b prop** (9): `dungeon-prop-01`, `dungeon-prop-02`, `dungeon-prop-03`, `dungeon-prop-04`, `dungeon-prop-05`, `dungeon-prop-06`, `dungeon-prop-07`, `dungeon-prop-08`, `dungeon-prop-09`
- **M9-d backdrop** (4): `dungeon-backdrop-far-01`, `dungeon-backdrop-far`, `dungeon-backdrop-mid`, `dungeon-backdrop-near`
- **M9-c decal+shadow** (16): `dungeon-decal-01`, `dungeon-decal-02`, `dungeon-decal-03`, `dungeon-decal-04`, `dungeon-decal-05`, `dungeon-decal-06`, `dungeon-decal-07`, `dungeon-decal-08`, `dungeon-decal-09`, `dungeon-decal-10`, `dungeon-decal-11`, `dungeon-decal-12`, `dungeon-shadow-01`, `dungeon-shadow-02`, … (+2; xem CSV)
- **M9-e portal+marker+fx** (6): `dungeon-portal-dormant`, `dungeon-portal-active`, `dungeon-marker-arrival`, `dungeon-fx-01`, `dungeon-fx-02`, `dungeon-fx-03`
- **M9-f landmark** (1): `dungeon_floor_01-landmark-01`

### M10 — Kit mới: arena2

- **M10-0 brief** (1): `danh sách asset kit arena2`
- **M10-a floor+edge** (11): `arena2-floor-01`, `arena2-floor-02`, `arena2-floor-03`, `arena2-floor-extra-01`, `arena2-floor-extra-02`, `arena2-floor-extra-03`, `arena2-floor-extra-04`, `arena2-floor-extra-05`, `arena2-edge-01`, `arena2-edge-02`, `arena2-edge-03`
- **M10-b prop** (5): `arena2-prop-01`, `arena2-prop-02`, `arena2-prop-03`, `arena2-prop-04`, `arena2-prop-05`
- **M10-d backdrop** (4): `arena2-backdrop-far-01`, `arena2-backdrop-far`, `arena2-backdrop-mid`, `arena2-backdrop-near`
- **M10-c decal+shadow** (16): `arena2-decal-01`, `arena2-decal-02`, `arena2-decal-03`, `arena2-decal-04`, `arena2-decal-05`, `arena2-decal-06`, `arena2-decal-07`, `arena2-decal-08`, `arena2-decal-09`, `arena2-decal-10`, `arena2-decal-11`, `arena2-decal-12`, `arena2-shadow-01`, `arena2-shadow-02`, … (+2; xem CSV)
- **M10-e portal+marker+fx** (6): `arena2-portal-dormant`, `arena2-portal-active`, `arena2-marker-arrival`, `arena2-fx-01`, `arena2-fx-02`, `arena2-fx-03`
- **M10-f landmark** (2): `chaos_arena_main_field-landmark-01`, `team_arena_main_field-landmark-01`

### M11 — Kit mới: minigame

- **M11-0 brief** (1): `danh sách asset kit minigame`
- **M11-a floor+edge** (11): `minigame-floor-01`, `minigame-floor-02`, `minigame-floor-03`, `minigame-floor-04`, `minigame-floor-extra-01`, `minigame-floor-extra-02`, `minigame-floor-extra-03`, `minigame-floor-extra-04`, `minigame-edge-01`, `minigame-edge-02`, `minigame-edge-03`
- **M11-b prop** (15): `minigame-prop-01`, `minigame-prop-02`, `minigame-prop-03`, `minigame-prop-04`, `minigame-prop-05`, `minigame-prop-06`, `minigame-prop-07`, `minigame-prop-08`, `minigame-prop-09`, `minigame-prop-10`, `minigame-prop-11`, `minigame-prop-12`, `minigame-prop-13`, `minigame-prop-14`, … (+1; xem CSV)
- **M11-d backdrop** (4): `minigame-backdrop-far-01`, `minigame-backdrop-far`, `minigame-backdrop-mid`, `minigame-backdrop-near`
- **M11-c decal+shadow** (16): `minigame-decal-01`, `minigame-decal-02`, `minigame-decal-03`, `minigame-decal-04`, `minigame-decal-05`, `minigame-decal-06`, `minigame-decal-07`, `minigame-decal-08`, `minigame-decal-09`, `minigame-decal-10`, `minigame-decal-11`, `minigame-decal-12`, `minigame-shadow-01`, `minigame-shadow-02`, … (+2; xem CSV)
- **M11-e portal+marker+fx** (6): `minigame-portal-dormant`, `minigame-portal-active`, `minigame-marker-arrival`, `minigame-fx-01`, `minigame-fx-02`, `minigame-fx-03`
- **M11-f landmark** (6): `wolf_sheep_waiting_hall-landmark-01`, `wolf_sheep_sheep_house-landmark-01`, `wolf_sheep_sheep_pen-landmark-01`, `wolf_sheep_middle_field-landmark-01`, `wolf_sheep_wolf_pen-landmark-01`, `wolf_sheep_wolf_house-landmark-01`


## 4. Prompt thực thi — batch vẽ đầu tiên giao Codex (M1)

**Cách giao:** với MỖI asset dưới đây, mở 1 request ChatGPT/Codex, dán prompt trong khối code và đính kèm trực tiếp các ảnh liệt kê (không zip). Lưu final theo output path. Chạy `python3 tools/hd2d_audit/art_gate.py batch-11-world_tree` rồi báo Claude xem 4× + 3×1/3×3 thật. Không commit.

### M1-a World Tree (5 asset: `world_tree-edge-01`, `world_tree-edge-02`, `world_tree-floor-extra-05`, `world_tree_gate-landmark-01`, `world_tree-edge-03`)

#### REDRAW-world_tree-edge-01 — REDRAW `world_tree-edge-01` (edge) · ưu tiên P1
- Maps: world_tree_gate;world_tree_deep_woods;world_tree_secret_chamber
- Output: `art/src/hd2d/batch-11-world_tree/world_tree-edge-01/final.png`
- Spec: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha | pivot giữa-đáy, dải đặt giữa hai tile; lặp ngang 2 đầu
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/edge-grass-dirt/final.png; art/src/hd2d/batch-02-octopath/city-garden-border/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/batch-11-world_tree/world_tree-edge-01/final.png
- Tránh: Lộ đường cắt tại mốc 512 trong 3×1 thật (wx 3.5/4.1); baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Lát 3×1 thật; kích thước đúng spec; xem hình: Lát 3×1 thật: không đường cắt ở mốc 512, không cụm lặp đều ≤1 tile, không đối xứng gương

```
Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree-edge-01` (edge) cho kit world_tree. Nội dung: dải chuyển rêu → vỏ cây 512×128/40 màu, alpha đục; art-gate seam X=10.586/limit 14. Repeat 3× không lộ mối nối lớn nhưng nhịp vỏ cây lặp và màu tối; c. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha. Pivot: pivot giữa-đáy, dải đặt giữa hai tile. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Lộ đường cắt tại mốc 512 trong 3×1 thật (wx 3.5/4.1). Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-world_tree-edge-02 — REDRAW `world_tree-edge-02` (edge) · ưu tiên P1
- Maps: world_tree_gate;world_tree_deep_woods;world_tree_secret_chamber
- Output: `art/src/hd2d/batch-11-world_tree/world_tree-edge-02/final.png`
- Spec: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha | pivot giữa-đáy, dải đặt giữa hai tile; lặp ngang 2 đầu
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/edge-grass-dirt/final.png; art/src/hd2d/batch-02-octopath/city-garden-border/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/batch-11-world_tree/world_tree-edge-02/final.png
- Tránh: Lộ đường cắt tại mốc 512 trong 3×1 thật (wx 3.5/4.1); baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Lát 3×1 thật; kích thước đúng spec; xem hình: Lát 3×1 thật: không đường cắt ở mốc 512, không cụm lặp đều ≤1 tile, không đối xứng gương

```
Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree-edge-02` (edge) cho kit world_tree. Nội dung: dải rêu emerald → lối vỏ vàng 512×128/37 màu, alpha nhị phân; art-gate seam 17.768/17.630, giới hạn tương đối 28.208. Candidate tạm; mảng bark và foli. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha. Pivot: pivot giữa-đáy, dải đặt giữa hai tile. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Lộ đường cắt tại mốc 512 trong 3×1 thật (wx 3.5/4.1). Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-world_tree-floor-extra-05 — REDRAW `world_tree-floor-extra-05` (floor) · ưu tiên P1
- Maps: world_tree_gate;world_tree_deep_woods;world_tree_secret_chamber
- Output: `art/src/hd2d/batch-11-world_tree/world_tree-floor-extra-05/final.png`
- Spec: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv) | không có pivot (tile); seamless 4 cạnh
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/dirt-floor-01/final.png; art/src/hd2d/batch-01-octopath/dirt-floor-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/batch-11-world_tree/world_tree-floor-extra-05/final.png
- Tránh: wrap x/y 2.5/3.6 cao, nghi seam; wrap x/y 2.512/3.596 >2.0; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Lát 3×3 thật + offset 256 px; kích thước đúng spec; xem hình: Lát 3×3 thật + offset 256 px: không lưới/khe chữ thập, không cụm lặp theo ô; wrap_x/y ≤1.25 theo gate

```
Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree-floor-extra-05` (floor) cho kit world_tree. Nội dung: rêu emerald sáng với phấn vàng thưa, 512×512/40 màu; nearest + no-dither finish; seam X=9.315/Y=10.120; corr cao nhất 0.861 với floor-03. Mosaic có ca. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv). Pivot: không có pivot (tile). 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: wrap x/y 2.5/3.6 cao, nghi seam; wrap x/y 2.512/3.596 >2.0. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-world_tree_gate-landmark-01 — REDRAW `world_tree_gate-landmark-01` (landmark) · ưu tiên P1
- Maps: world_tree_gate;world_tree_deep_woods;world_tree_secret_chamber
- Output: `art/src/hd2d/batch-11-world_tree/world_tree_gate-landmark-01/final.png`
- Spec: 384±64 px, binary alpha, lề ≥8 px, 33–48 màu; diễn giải HD-2D từ ảnh gốc (không trích APK) | pivot giữa-đáy; -
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/bush-01/final.png; art/src/hd2d/batch-01-octopath/bush-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/batch-11-world_tree/world_tree_gate-landmark-01/final.png
- Tránh: Hoa: art yếu/glossy so với style, manifest sha cũ sau sửa lề; cần vẽ lại + scene proof; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Đặt cạnh crop ảnh gốc ở map-scale; kích thước đúng spec; xem hình: Đặt cạnh crop ảnh gốc ở map-scale: cùng chủng loại + bảng màu; ghi crop vào review

```
Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree_gate-landmark-01` (landmark) cho kit world_tree. Nội dung: hoa vàng cam cánh nhọn xòe ngang, nụ giữa cao, cụm lá xanh; redraw 384×384/40 màu, alpha nhị phân; xem 4× caro/tối và map-scale. Candidate attempt 04,. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 384±64 px, binary alpha, lề ≥8 px, 33–48 màu; diễn giải HD-2D từ ảnh gốc (không trích APK). Pivot: pivot giữa-đáy. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Hoa: art yếu/glossy so với style, manifest sha cũ sau sửa lề; cần vẽ lại + scene proof. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### NEW-world_tree-edge-03 — NEW `world_tree-edge-03` (edge) · ưu tiên P1
- Maps: world_tree_gate;world_tree_deep_woods;world_tree_secret_chamber
- Output: `art/src/hd2d/batch-11-world_tree/world_tree-edge-03/final.png`
- Spec: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha | pivot giữa-đáy, dải đặt giữa hai tile; lặp ngang 2 đầu
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/edge-grass-dirt/final.png; art/src/hd2d/batch-02-octopath/city-garden-border/final.png
- Tránh: baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Lát 3×1 thật; kích thước đúng spec; xem hình: Lát 3×1 thật: không đường cắt ở mốc 512, không cụm lặp đều ≤1 tile, không đối xứng gương

```
Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree-edge-03` (edge) cho kit world_tree. Nội dung: dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc. Attempts 01–16 rejected; 13 soft/mottled, 14 blocky/regular, 15 too flat, 16. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha. Pivot: pivot giữa-đáy, dải đặt giữa hai tile. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```


### M1-b Garden (5 asset: `gd-trunk-seg-01`, `gd-trunk-seg-02`, `gd-pillar-vein-01`, `gd-seal-strip`, `gd-seal-strip-lit`)

Đọc thêm `art/src/hd2d/garden-a/REVIEW-CLAUDE-20261109.md` (lý do trả từng asset).

#### REDRAW-gd-trunk-seg-01 — REDRAW `gd-trunk-seg-01` (prop) · ưu tiên P0
- Maps: garden (P01)
- Output: `art/src/hd2d/batch-11-garden/gd-trunk-seg-01/final.png`
- Spec: billboard binary alpha, lề alpha ≥8 px, 33–48 màu; kích thước theo vật (128 px = 1 đv; cao ≈ cao thực × 128) | pivot giữa-đáy; (nếu cây: tách trunk/canopy + sway)
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/garden (P01).jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/bush-01/final.png; art/src/hd2d/batch-01-octopath/bush-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/garden-a/gd-trunk-seg-01/final.png
- Tránh: Trunk sai exact vertical seam; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Xem 1× và 4× nền caro/tối; kích thước đúng spec; xem hình: Xem 1× và 4× nền caro/tối: không viền sáng, không glow/bóng nướng, đọc ra vật ở game-scale

```
Vẽ asset HD-2D Octopath-Traveler pixel art `gd-trunk-seg-01` (prop) cho kit garden. Nội dung: gd-trunk-seg-01. Palette/style kit:  Kỹ thuật: billboard binary alpha, lề alpha ≥8 px, 33–48 màu; kích thước theo vật (128 px = 1 đv; cao ≈ cao thực × 128). Pivot: pivot giữa-đáy. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Trunk sai exact vertical seam. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-gd-trunk-seg-02 — REDRAW `gd-trunk-seg-02` (prop) · ưu tiên P0
- Maps: garden (P01)
- Output: `art/src/hd2d/batch-11-garden/gd-trunk-seg-02/final.png`
- Spec: billboard binary alpha, lề alpha ≥8 px, 33–48 màu; kích thước theo vật (128 px = 1 đv; cao ≈ cao thực × 128) | pivot giữa-đáy; (nếu cây: tách trunk/canopy + sway)
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/garden (P01).jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/bush-01/final.png; art/src/hd2d/batch-01-octopath/bush-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/garden-a/gd-trunk-seg-02/final.png
- Tránh: Trunk sai exact vertical seam; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Xem 1× và 4× nền caro/tối; kích thước đúng spec; xem hình: Xem 1× và 4× nền caro/tối: không viền sáng, không glow/bóng nướng, đọc ra vật ở game-scale

```
Vẽ asset HD-2D Octopath-Traveler pixel art `gd-trunk-seg-02` (prop) cho kit garden. Nội dung: gd-trunk-seg-02. Palette/style kit:  Kỹ thuật: billboard binary alpha, lề alpha ≥8 px, 33–48 màu; kích thước theo vật (128 px = 1 đv; cao ≈ cao thực × 128). Pivot: pivot giữa-đáy. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Trunk sai exact vertical seam. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-gd-pillar-vein-01 — REDRAW `gd-pillar-vein-01` (prop) · ưu tiên P0
- Maps: garden (P01)
- Output: `art/src/hd2d/batch-11-garden/gd-pillar-vein-01/final.png`
- Spec: billboard binary alpha, lề alpha ≥8 px, 33–48 màu; kích thước theo vật (128 px = 1 đv; cao ≈ cao thực × 128) | pivot giữa-đáy; (nếu cây: tách trunk/canopy + sway)
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/garden (P01).jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/bush-01/final.png; art/src/hd2d/batch-01-octopath/bush-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/garden-a/gd-pillar-vein-01/final.png
- Tránh: Chỉ 1 màu; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Xem 1× và 4× nền caro/tối; kích thước đúng spec; xem hình: Xem 1× và 4× nền caro/tối: không viền sáng, không glow/bóng nướng, đọc ra vật ở game-scale

```
Vẽ asset HD-2D Octopath-Traveler pixel art `gd-pillar-vein-01` (prop) cho kit garden. Nội dung: gd-pillar-vein-01. Palette/style kit:  Kỹ thuật: billboard binary alpha, lề alpha ≥8 px, 33–48 màu; kích thước theo vật (128 px = 1 đv; cao ≈ cao thực × 128). Pivot: pivot giữa-đáy. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Chỉ 1 màu. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-gd-seal-strip — REDRAW `gd-seal-strip` (tile) · ưu tiên P0
- Maps: garden (P01)
- Output: `art/src/hd2d/batch-11-garden/gd-seal-strip/final.png`
- Spec: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv) | không có pivot (tile); -
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/garden (P01).jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/dirt-floor-01/final.png; art/src/hd2d/batch-01-octopath/dirt-floor-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/garden-a/gd-seal-strip/final.png
- Tránh: Sai lề + QA bbox; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Lát 3×3 thật + offset 256 px; kích thước đúng spec; xem hình: Lát 3×3 thật + offset 256 px: không lưới/khe chữ thập, không cụm lặp theo ô; wrap_x/y ≤1.25 theo gate

```
Vẽ asset HD-2D Octopath-Traveler pixel art `gd-seal-strip` (tile) cho kit garden. Nội dung: gd-seal-strip. Palette/style kit:  Kỹ thuật: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv). Pivot: không có pivot (tile). 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Sai lề + QA bbox. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```

#### REDRAW-gd-seal-strip-lit — REDRAW `gd-seal-strip-lit` (tile) · ưu tiên P0
- Maps: garden (P01)
- Output: `art/src/hd2d/batch-11-garden/gd-seal-strip-lit/final.png`
- Spec: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv) | không có pivot (tile); -
- Đính kèm ảnh gốc: .ai/design/map-checklists/refs/garden (P01).jpg
- Đính kèm style anchor: art/src/hd2d/batch-01-octopath/dirt-floor-01/final.png; art/src/hd2d/batch-01-octopath/dirt-floor-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/garden-a/gd-seal-strip-lit/final.png
- Tránh: Sai lề + QA bbox; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID
- Nghiệm thu đo được: Gate hd2d_audit pass (33–48 màu, binary alpha, lề ≥8, không magenta); Lát 3×3 thật + offset 256 px; kích thước đúng spec; xem hình: Lát 3×3 thật + offset 256 px: không lưới/khe chữ thập, không cụm lặp theo ô; wrap_x/y ≤1.25 theo gate

```
Vẽ asset HD-2D Octopath-Traveler pixel art `gd-seal-strip-lit` (tile) cho kit garden. Nội dung: gd-seal-strip-lit. Palette/style kit:  Kỹ thuật: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv). Pivot: không có pivot (tile). 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Sai lề + QA bbox. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.
```


## 5. Kit chưa có asset: đối chiếu ảnh gốc ↔ plan (bắt buộc đọc trước M4–M11)

Đã cross-check bằng ảnh gốc 23 map và các gói bổ sung (`arena-*` batch-02/P01 redo C, `city-facade-guild`…): **không có asset dùng được nguyên cho 8 kit**; chỉ có nguồn tham chiếu phong cách. Khác biệt:

| Kit | Plan cũ (kit md) | Ảnh gốc thật | Hệ quả |
|---|---|---|---|
| tower (3) | tháp đá lục giác, lan can kim loại, cột tháp, chim đá | rừng xanh sáng, cổ thụ, đường cát, cầu ván gỗ + tổ chim | viết lại brief |
| maze (3) | tường dây leo rêu, cổng đá, bẫy chông | cột vòm xương, gai/móng trắng, sàn hồng-nâu, cổng sọ phát sáng | viết lại brief |
| guild (6) | granit + cờ xanh/vàng, nhà gỗ | sân đá nứt + tường thành be + trời xanh; 6 công trình riêng | giữ hướng, thêm công trình |
| battlefield (1) | đất cháy, chiến xa, tháp canh | quảng trường trắng, cột tím, đài phun nước, tượng thú | viết lại brief |
| maya (1) | kim tự tháp, rừng nhiệt đới | điện thờ lục thẫm, cột phù điêu, pha lê lục lam, ngai đá | viết lại brief |
| dungeon (1) | ngục sắt, xích, vũng nước | gạch be, đầu hươu cam, sàn vảy vàng-xanh | viết lại brief |
| arena2 (2) | tái dùng Huyết Chiến Đài + cát/khán đài đỏ-xanh | CÙNG ảnh với battlefield | gộp với battlefield |
| minigame (6) | sân cỏ cừu/sân đá sói | tường/sàn/trời giống guild; 4/6 map sân trống | gộp với guild |

Task `BRIEF-<kit>` là điều kiện của mọi task NEW trong kit. Các slot plan cũ giữ trong CSV (THIẾU) để không mất dấu; sau BRIEF được owner duyệt, asset không có trong ảnh gốc sẽ bị gạch khỏi nhu cầu (ghi trong review).

## 6. Quy trình prompt mẫu cho batch bất kỳ

Mỗi dòng task CSV cột `prompt` là prompt hoàn chỉnh; cột `reference_attach` (ảnh gốc map, đính kèm trực tiếp) và `style_anchor_attach` (batch 00–09 đã duyệt; không dùng batch-10/11 làm anchor) bắt buộc đính kèm; cột `errors_to_avoid` dán thêm vào prompt khi tạo lại lần 2. Với REDRAW, đính kèm bản cũ chỉ để tránh lỗi (ghi rõ "KHÔNG bắt chước").

## 7. Phụ lục

- Scene proof (M12): 92 task `SCENE-<map_id>`, ưu tiên cuối.
- NPC là dependency riêng (cột `npc_dependency_separate` ở MAP-COVERAGE).
- UI/actor/portrait ngoài scope 92 map: xem phụ lục REVIEW §6.
