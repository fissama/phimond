# Kit `windrock` — Núi Phong Thạch

> **Nghiệm thu Claude 2026-11-09** (mức V1, chưa 4×): VẼ_LẠI 12, DUYỆT 70. Map: {'CHƯA ĐỦ': 6}. Trạng thái hiện hành ở [ASSET-VERDICTS-20261109.csv](ASSET-VERDICTS-20261109.csv) / [MAP-COVERAGE-20261109.csv](MAP-COVERAGE-20261109.csv); tick ✅/❌ bên dưới là LỊCH SỬ, không phải approval.
> VẼ_LẠI (12): `windrock-rock-floor-01`, `windrock-rock-floor-02`, `windrock-gravel-floor`, `windrock-grass-snow-floor`, `windrock-snow-crust-floor`, `windrock-slate-floor`, `windrock-mountain-path-floor`, `windrock-scree-floor`, `windrock-rock-floor-03`, `windrock-edge-01`, `windrock-edge-02`, `windrock-edge-03`

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Đá xám lam, cỏ núi khô, tuyết lốm đốm trên cao, gió mạnh (cờ/cỏ nghiêng). Bảng màu đá #7B8794/#566070, cỏ khô #8A8F4E, tuyết #E8EEF4.
- Thư mục asset: `art/src/hd2d/batch-11-windrock/`
- Số map: 6

## 1. Trạng thái asset hiện có

Theo manifest GPT cập nhật 30/10: tổng 82 · duyệt 0 · floor 9 · edge 3 · prop 36 · backdrop 3 · decal 16 · shadow 6 · marker 1 · FX 6 · portal 2. Asset mới đã xem final 4×; draft chờ Claude/owner review. Các landmark theo từng map vẫn cần được đối chiếu ảnh gốc ở mục 3. Danh sách 74 mục bên dưới là inventory Gemini cũ, không phản ánh manifest hiện tại; cần đối chiếu từng ID trước khi dùng làm checklist vẽ.

| Loại | Có | Cần tối thiểu | Ghi chú |
|---|---|---|---|
| floor | 9 | 8 | ✅ · có 9 tile sàn 512×512; kiểm repeat trực quan trước khi dùng |
| edge | 3 | 3 | 🟨 đủ 3 draft `windrock-edge-01..03`, 512×128, alpha nhị phân, palette ≤64 và seam qua gate; chưa được Claude/owner duyệt. Prompt, raw, repeat 3×3 và QA ở `jobs/edges-redraw-20261030/` và các thư mục asset |
| prop | 36 | 36 | 🟨 15 prop mới đã xem 4×; đủ mức tối thiểu, chờ Claude/owner review |
| decal | 16 | 12 | 🟨 16 draft đã xem 4×; đạt mức tối thiểu; 6 decal mới gồm 2 seam rêu/đá, 2 vệt chân tuyết, snow chips và stone fragments; chờ Claude/owner review |
| shadow | 6 | 4 | 🟨 Có 6 contact shadow draft, soft alpha theo ngoại lệ shadow; chờ Claude/owner review |
| backdrop | 3 | 3 | 🟨 Far/mid/near hiện có; near mới là one-shot, không tileable, chờ Claude/owner review |
| portal | 2 | 2 | 🟨 active/dormant cùng silhouette, đã xem 4×; chờ Claude/owner review |
| marker | 1 | 1 | 🟨 `windrock-spawn-marker-01` đã xem 4×; chờ Claude/owner review |
| fx | 6 | 3 | 🟨 6 draft đã xem 4×; có gust/flecks/glint/snow/sparks/dust; nhiều motif còn mềm hoặc lệch sắc ấm, chờ Claude/owner review |

### Inventory Gemini cũ (74 dòng, không dùng để theo dõi manifest GPT)

Các dấu `Vẽ`/`Duyệt` dưới đây phản ánh batch Gemini cũ; giữ lại để tra nguồn, không tính vào trạng thái hiện tại. Chỉ manifest `batch-11-windrock/manifest.json` và bảng tổng hợp phía trên phản ánh 79 asset GPT.

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-cliffs-near` | backdrop | [16.0, 6.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-horizon-gradient` | backdrop | [16.0, 2.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-peaks-mid` | backdrop | [16.0, 6.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-peaks-wall-far` | backdrop | [16.0, 6.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-chasm-ravine-01` | decal | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-chasm-ravine-02` | decal | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-alpine-moss-edge` | decal | [1.8, 3.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-ice-patch-01` | decal | [1.8, 1.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-ice-patch-02` | decal | [1.8, 1.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-rock-fissure-01` | decal | [2.0, 2.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-rock-fissure-02` | decal | [2.0, 2.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-scree-run-01` | decal | [3.5, 2.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-scree-run-02` | decal | [3.5, 2.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-snow-drift-01` | decal | [3.8, 1.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-snow-drift-02` | decal | [3.8, 1.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-decal-snow-footprints` | decal | [1.8, 3.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-tile-edge-decal` | decal | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-grass-snow-floor` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-gravel-floor` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-mountain-path-floor` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-rock-floor-01` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-rock-floor-02` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-scree-floor` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-slate-floor` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-snow-crust-floor` | floor | [4.0, 4.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-spawn-marker` | marker | [4.0, 1.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-portal-active` | portal | [3.0, 3.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-portal-dormant` | portal | [3.0, 3.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-ancient-stele` | prop | [1.5, 1.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-arch-gate` | prop | [3.8, 3.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-backpack-gear` | prop | [1.0, 1.1] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-boulder-snow-01` | prop | [1.8, 1.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-boulder-snow-02` | prop | [1.6, 1.4] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-bridge-anchor-post-left` | prop | [1.9, 2.1] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-bridge-anchor-post-right` | prop | [1.9, 2.1] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-bridge-broken` | prop | [2.2, 0.9] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-bridge-repeat` | prop | [2.5, 0.9] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-camp-tent` | prop | [2.4, 1.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-campfire-anim` | prop | [4.0, 1.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-cliff-01` | prop | [3.0, 2.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-cliff-snow-ledge` | prop | [3.0, 2.5] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-dead-wood-stump` | prop | [1.0, 1.4] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-firewood-stack` | prop | [1.2, 1.1] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-grass-snow-clump-01` | prop | [0.9, 0.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-grass-snow-clump-02` | prop | [0.9, 0.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-grass-snow-clump-03` | prop | [0.9, 0.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pebbles-scatter` | prop | [1.4, 1.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pillar-01` | prop | [1.8, 2.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pine-canopy` | prop | [2.2, 3.2] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pine-large-01-canopy` | prop | [2.3, 3.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pine-large-01-trunk` | prop | [1.3, 3.4] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pine-large-02-canopy` | prop | [2.6, 3.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pine-large-02-trunk` | prop | [1.1, 3.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-pine-trunk` | prop | [1.2, 2.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-prayer-flagpole` | prop | [1.8, 3.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shrub-snow-01` | prop | [1.0, 0.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shrub-snow-02` | prop | [1.0, 0.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shrub-snow-03` | prop | [1.0, 0.8] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shrub-snow-04` | prop | [1.0, 0.9] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-signpost-blank` | prop | [1.2, 1.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-spire-pillar-tall-01` | prop | [1.4, 3.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-spire-pillar-tall-02` | prop | [1.4, 3.0] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-stone-stairs` | prop | [2.7, 2.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-supply-crate` | prop | [1.1, 1.3] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-supply-keg` | prop | [1.0, 1.3] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-trail-cairn` | prop | [1.1, 1.7] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-wooden-barrel` | prop | [1.0, 1.2] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-wooden-fence` | prop | [2.2, 1.2] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shadow-large-oval` | shadow | [3.0, 1.4] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shadow-medium-oval` | shadow | [2.0, 1.1] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shadow-pillar-long` | shadow | [1.6, 1.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shadow-small-round` | shadow | [1.1, 0.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shadow-stairs-spread` | shadow | [3.0, 1.6] | — |
| ✅ | ❌ Gemini bị trả — vẽ lại | `windrock-shadow-tree-canopy` | shadow | [2.4, 1.2] | — |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Núi Phong Thạch (windrock). Style: Đá xám lam, cỏ núi khô, tuyết lốm đốm trên cao, gió mạnh (cờ/cỏ nghiêng). Bảng màu đá #7B8794/#566070, cỏ khô #8A8F4E, tuyết #E8EEF4.. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong art/src/hd2d/batch-11-windrock/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-windrock` = 0 lỗi, contact-sheet mới hơn manifest.
```

## 3. Từng map

### `windrock_mountain_camp` — Trại Phong Thạch

![windrock_mountain_camp](refs/windrock_mountain_camp.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/windrock_mountain_camp.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/windrock_mountain_camp.png`, 2261×825 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/20-25/MomDaGio.unity`, 21 sprite ghép; brief: [../map-briefs/kit_windrock/windrock_mountain_camp.md](../map-briefs/kit_windrock/windrock_mountain_camp.md)
- Cổng: 3 · vùng quái: không · spawn: 0 · NPC: wind_hesper, wind_iris, wind_jorin, wind_kestra
- neo `P:windrock_mountain_portal_002` (door) Cửa → Dãy Phong Lĩnh: px [643, 374]
- neo `P:windrock_mountain_portal_006` (door) Cửa → Hẻm Gió Gào: px [2143, 485]
- neo `P:windrock_mountain_portal_008` (door) Cửa → Cầu Thiên Thạch: px [111, 573]
- neo `wind_hesper` (npc) : px CẦN ĐẶT
- neo `wind_iris` (npc) : px CẦN ĐẶT
- neo `wind_jorin` (npc) : px CẦN ĐẶT
- neo `wind_kestra` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): wind_hesper, wind_iris, wind_jorin, wind_kestra

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ✅ | ⬜ | `windrock_mountain_camp-landmark-01` | prop hiện có | Nhà cửa đá ở trại (`windrock-camp-stone-door-hut`, asset dùng chung, đã vẽ) | `windrock-camp-stone-door-hut/prompt.md` |
| — | — | `windrock_mountain_camp-landmark-02` | không phát sinh | Không có landmark thứ hai tách biệt cần thêm; các vật trại còn lại là prop dùng chung | Đã đối chiếu ảnh gốc và brief |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map windrock_mountain_camp (Trại Phong Thạch), kit windrock.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/windrock_mountain_camp.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `windrock_mountain_stone_bridge` — Cầu Thiên Thạch

![windrock_mountain_stone_bridge](refs/windrock_mountain_stone_bridge.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/windrock_mountain_stone_bridge.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/windrock_mountain_stone_bridge.png`, 2248×825 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/20-25/MomDaGio.unity`, 16 sprite ghép; brief: [../map-briefs/kit_windrock/windrock_mountain_stone_bridge.md](../map-briefs/kit_windrock/windrock_mountain_stone_bridge.md)
- Cổng: 2 · vùng quái: có · spawn: 12 · NPC: wind_loren
- neo `P:windrock_mountain_portal_007` (door) Cửa → Trại Phong Thạch: px [2147, 507]
- neo `P:windrock_mountain_portal_010` (door) Cửa → Quảng Trường Thạch Trụ: px [109, 473]
- neo `AT:square:windrock_mountain_stone_bridge` (arrival) Đến từ trụ Quảng Trường: px [209, 467]
- neo `wind_loren` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): wind_loren

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ✅ | ⬜ | `windrock_mountain_stone_bridge-landmark-01` | prop hiện có | Mố cầu đá (`windrock-bridge-stone-abutment`, đã vẽ) | `windrock-bridge-stone-abutment/prompt.md` |
| — | — | `windrock_mountain_stone_bridge-landmark-02` | không phát sinh | Không thấy landmark thứ hai tách biệt trong ảnh/brief gốc | Đã đối chiếu ảnh gốc và brief |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map windrock_mountain_stone_bridge (Cầu Thiên Thạch), kit windrock.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/windrock_mountain_stone_bridge.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `windrock_mountain_howling_canyon` — Hẻm Gió Gào

![windrock_mountain_howling_canyon](refs/windrock_mountain_howling_canyon.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/windrock_mountain_howling_canyon.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/windrock_mountain_howling_canyon.png`, 2248×826 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/20-25/MomDaGio.unity`, 16 sprite ghép; brief: [../map-briefs/kit_windrock/windrock_mountain_howling_canyon.md](../map-briefs/kit_windrock/windrock_mountain_howling_canyon.md)
- Cổng: 1 · vùng quái: có · spawn: 12 · NPC: —
- neo `P:windrock_mountain_portal_005` (door) Cửa → Trại Phong Thạch: px [119, 477]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ✅ | ⬜ | `windrock_mountain_howling_canyon-landmark-01` | prop hiện có | Đá huýt gió trong hẻm (`windrock-canyon-whistling-rock`, đã vẽ) | `windrock-canyon-whistling-rock/prompt.md` |
| — | — | `windrock_mountain_howling_canyon-landmark-02` | không phát sinh | Không thấy landmark thứ hai tách biệt trong ảnh/brief gốc | Đã đối chiếu ảnh gốc và brief |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map windrock_mountain_howling_canyon (Hẻm Gió Gào), kit windrock.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/windrock_mountain_howling_canyon.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `windrock_mountain_mountain_range` — Dãy Phong Lĩnh

![windrock_mountain_mountain_range](refs/windrock_mountain_mountain_range.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/windrock_mountain_mountain_range.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/windrock_mountain_mountain_range.png`, 2262×938 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/20-25/MomDaGio.unity`, 26 sprite ghép; brief: [../map-briefs/kit_windrock/windrock_mountain_mountain_range.md](../map-briefs/kit_windrock/windrock_mountain_mountain_range.md)
- Cổng: 2 · vùng quái: có · spawn: 12 · NPC: wind_mirel
- neo `P:windrock_mountain_portal_004` (door) Cửa → Sơn Đạo Phong Vân: px [108, 525]
- neo `P:windrock_mountain_portal_009` (door) Cửa → Trại Phong Thạch: px [2158, 522]
- neo `wind_mirel` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): wind_mirel

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ✅ | ⬜ | `windrock_mountain_mountain_range-landmark-01` | prop hiện có | Sống núi răng cưa (`windrock-range-serrated-ridge`, đã vẽ) | `windrock-range-serrated-ridge/prompt.md` |
| — | — | `windrock_mountain_mountain_range-landmark-02` | không phát sinh | Không thấy landmark thứ hai tách biệt trong ảnh/brief gốc | Đã đối chiếu ảnh gốc và brief |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map windrock_mountain_mountain_range (Dãy Phong Lĩnh), kit windrock.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/windrock_mountain_mountain_range.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `windrock_mountain_mountain_path` — Sơn Đạo Phong Vân

![windrock_mountain_mountain_path](refs/windrock_mountain_mountain_path.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/windrock_mountain_mountain_path.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/windrock_mountain_mountain_path.png`, 2262×938 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/20-25/MomDaGio.unity`, 26 sprite ghép; brief: [../map-briefs/kit_windrock/windrock_mountain_mountain_path.md](../map-briefs/kit_windrock/windrock_mountain_mountain_path.md)
- Cổng: 2 · vùng quái: có · spawn: 12 · NPC: wind_nolan
- neo `P:windrock_mountain_portal_001` (door) Cửa → Đỉnh Thiên Phong: px [114, 519]
- neo `P:windrock_mountain_portal_003` (door) Cửa → Dãy Phong Lĩnh: px [2176, 510]
- neo `wind_nolan` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): wind_nolan

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ✅ | ⬜ | `windrock_mountain_mountain_path-landmark-01` | prop hiện có | Gờ đường núi uốn khúc (`windrock-path-switchback-ledge`, đã vẽ) | `windrock-path-switchback-ledge/prompt.md` |
| — | — | `windrock_mountain_mountain_path-landmark-02` | không phát sinh | Không thấy landmark thứ hai tách biệt trong ảnh/brief gốc | Đã đối chiếu ảnh gốc và brief |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map windrock_mountain_mountain_path (Sơn Đạo Phong Vân), kit windrock.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/windrock_mountain_mountain_path.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `windrock_mountain_summit` — Đỉnh Thiên Phong

![windrock_mountain_summit](refs/windrock_mountain_summit.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/windrock_mountain_summit.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/windrock_mountain_summit.png`, 2254×904 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/20-25/MomDaGio.unity`, 24 sprite ghép; brief: [../map-briefs/kit_windrock/windrock_mountain_summit.md](../map-briefs/kit_windrock/windrock_mountain_summit.md)
- Cổng: 1 · vùng quái: có · spawn: 10 · NPC: wind_orla
- neo `P:windrock_mountain_portal_011` (door) Cửa → Sơn Đạo Phong Vân: px [2138, 511]
- neo `wind_orla` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): wind_orla

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ✅ | ⬜ | `windrock_mountain_summit-landmark-01` | prop hiện có | Cairn gió trên đỉnh (`windrock-summit-wind-cairn`, đã vẽ) | `windrock-summit-wind-cairn/prompt.md` |
| — | — | `windrock_mountain_summit-landmark-02` | không phát sinh | Không thấy landmark thứ hai tách biệt trong ảnh/brief gốc | Đã đối chiếu ảnh gốc và brief |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map windrock_mountain_summit (Đỉnh Thiên Phong), kit windrock.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/windrock_mountain_summit.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```
