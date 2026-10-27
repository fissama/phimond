# Kit `ghost_castle` — Lâu Đài Ma

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Đá cẩm thạch đen nứt, rèm nhung rách, nến bạc, rừng U Lâm xanh bích.
- Thư mục asset: `apps/game-web/art-src/hd2d/batch-11-ghost_castle/`
- Số map: 3

## 1. Danh sách asset cần vẽ (kit chưa có asset)

Nguồn: Phần C `hd2d-maps-75-gemini-prompt.md`. Yêu cầu gốc: tile sàn cẩm thạch đen, thảm rách, cỏ khô nghĩa địa; prop: cổng lâu đài sắt, tường lâu đài, tháp canh nhỏ, rèm rách ×2, chân nến bạc (lửa 4 khung), tranh chân dung (không mặt nhận diện), tủ sách mục, cây khô ×3, đèn ma; backdrop xa: lâu đài trên đồi + trăng.

| Vẽ | Duyệt | id (số thứ tự; đặt tên tiếng Anh vào manifest `name`) | loại | mô tả + prompt đi kèm |
|---|---|---|---|---|
| ⬜ | ⬜ | `ghost_castle-floor-01` | floor | sàn cẩm thạch đen — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-floor-02` | floor | thảm rách — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-floor-03` | floor | cỏ khô nghĩa địa — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-01` | prop | cổng lâu đài sắt — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-02` | prop | tường lâu đài — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-03` | prop | tháp canh nhỏ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-04` | prop | rèm rách — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-05` | prop | rèm rách — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-06` | prop | chân nến bạc (lửa 4 khung) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-07` | prop | tranh chân dung (không mặt nhận diện) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-08` | prop | tủ sách mục — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-09` | prop | cây khô — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-10` | prop | cây khô — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-11` | prop | cây khô — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-prop-12` | prop | đèn ma — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-backdrop-far-01` | backdrop_far | lâu đài trên đồi + trăng — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Lâu Đài Ma, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `ghost_castle-floor-extra-01` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `ghost_castle-floor-extra-02` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `ghost_castle-floor-extra-03` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `ghost_castle-floor-extra-04` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `ghost_castle-floor-extra-05` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `ghost_castle-edge-01` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `ghost_castle-edge-02` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `ghost_castle-edge-03` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `ghost_castle-decal-01` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-02` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-03` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-04` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-05` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-06` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-07` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-08` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-09` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-10` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-11` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-decal-12` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `ghost_castle-shadow-01` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `ghost_castle-shadow-02` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `ghost_castle-shadow-03` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `ghost_castle-shadow-04` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `ghost_castle-backdrop-far` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `ghost_castle-backdrop-mid` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `ghost_castle-backdrop-near` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `ghost_castle-portal-dormant` | portal | cổng nhìn thẳng mặt trước, đúng tông kit |
| ⬜ | ⬜ | `ghost_castle-portal-active` | portal | cùng mask với dormant |
| ⬜ | ⬜ | `ghost_castle-marker-arrival` | marker | vòng sáng 4 khung |
| ⬜ | ⬜ | `ghost_castle-fx-01` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `ghost_castle-fx-02` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `ghost_castle-fx-03` | fx | hạt/tia sáng sprite sheet theo chủ đề |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Lâu Đài Ma (ghost_castle). Style: Đá cẩm thạch đen nứt, rèm nhung rách, nến bạc, rừng U Lâm xanh bích.. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong apps/game-web/art-src/hd2d/batch-11-ghost_castle/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-ghost_castle` = 0 lỗi, contact-sheet mới hơn manifest.
```

## 3. Từng map

### `ghost_castle_gate` — Cổng U Lâu

![ghost_castle_gate](refs/ghost_castle_gate.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/ghost_castle_gate.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/ghost_castle_gate.png`, 2241×831 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/LauDaiMa.unity`, 17 sprite ghép; brief: [../map-briefs/kit_ghost_castle/ghost_castle_gate.md](../map-briefs/kit_ghost_castle/ghost_castle_gate.md)
- Cổng: 2 · vùng quái: không · spawn: 0 · NPC: ghost_tove, ghost_una
- neo `P:ghost_castle_portal_004` (door) Cửa → U Linh Cổ Thành: px [1648, 411]
- neo `P:ghost_castle_portal_005` (door) Cửa → Hải Tặc Hào: px [113, 549]
- neo `AT:ship:ghost_castle_gate` (arrival) Đến từ trụ Hải Tặc Hào: px [212, 536]
- neo `ghost_tove` (npc) : px CẦN ĐẶT
- neo `ghost_una` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): ghost_tove, ghost_una

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `ghost_castle_gate-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `ghost_castle_gate-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map ghost_castle_gate (), kit ghost_castle.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/ghost_castle_gate.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `ghost_castle_deep_woods` — U Linh Cổ Thành

![ghost_castle_deep_woods](refs/ghost_castle_deep_woods.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/ghost_castle_deep_woods.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/ghost_castle_deep_woods.png`, 2509×826 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/LauDaiMa.unity`, 21 sprite ghép; brief: [../map-briefs/kit_ghost_castle/ghost_castle_deep_woods.md](../map-briefs/kit_ghost_castle/ghost_castle_deep_woods.md)
- Cổng: 2 · vùng quái: có · spawn: 25 · NPC: — · ghi chú: tên nguồn trùng với 2 map khác
- neo `P:ghost_castle_portal_001` (door) Cửa → Cổng U Lâu: px [103, 599]
- neo `P:ghost_castle_portal_002` (door) Cửa → Cổng U Lâu: px [2374, 563]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `ghost_castle_deep_woods-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `ghost_castle_deep_woods-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map ghost_castle_deep_woods (), kit ghost_castle.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/ghost_castle_deep_woods.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `ghost_castle_ancient_city_secret_chamber` — Mật Thất Cổ Thành

![ghost_castle_ancient_city_secret_chamber](refs/ghost_castle_ancient_city_secret_chamber.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/ghost_castle_ancient_city_secret_chamber.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/ghost_castle_ancient_city_secret_chamber.png`, 2509×826 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/LauDaiMa.unity`, 20 sprite ghép; brief: [../map-briefs/kit_ghost_castle/ghost_castle_ancient_city_secret_chamber.md](../map-briefs/kit_ghost_castle/ghost_castle_ancient_city_secret_chamber.md)
- Cổng: 1 · vùng quái: có · spawn: 20 · NPC: —
- neo `P:ghost_castle_portal_003` (door) Cửa → Cổng U Lâu: px [115, 519]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `ghost_castle_ancient_city_secret_chamber-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `ghost_castle_ancient_city_secret_chamber-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map ghost_castle_ancient_city_secret_chamber (), kit ghost_castle.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/ghost_castle_ancient_city_secret_chamber.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```
