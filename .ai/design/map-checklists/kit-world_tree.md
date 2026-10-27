# Kit `world_tree` — Cây Thế Giới

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim.
- Thư mục asset: `apps/game-web/art-src/hd2d/batch-11-world_tree/`
- Số map: 3

## 1. Danh sách asset cần vẽ (kit chưa có asset)

Nguồn: Phần C `hd2d-maps-75-gemini-prompt.md`. Yêu cầu gốc: tile vỏ cây/cành lát, rêu, lá rụng; prop: rễ khổng lồ ×3, lá khổng lồ ×3 (sway), nấm khổng lồ, quả thần phát sáng (4 khung), cổng tán cây, bậc thang cành, dây leo, đom đóm (4 khung); backdrop xa: thân cây vươn tới trời, tán lá.

| Vẽ | Duyệt | id (số thứ tự; đặt tên tiếng Anh vào manifest `name`) | loại | mô tả + prompt đi kèm |
|---|---|---|---|---|
| ⬜ | ⬜ | `world_tree-floor-01` | floor | vỏ cây/cành lát — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-floor-02` | floor | rêu — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-floor-03` | floor | lá rụng — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-01` | prop | rễ khổng lồ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-02` | prop | rễ khổng lồ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-03` | prop | rễ khổng lồ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-04` | prop | lá khổng lồ (sway) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-05` | prop | lá khổng lồ (sway) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-06` | prop | lá khổng lồ (sway) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-07` | prop | nấm khổng lồ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-08` | prop | quả thần phát sáng (4 khung) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-09` | prop | cổng tán cây — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-10` | prop | bậc thang cành — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-11` | prop | dây leo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-prop-12` | prop | đom đóm (4 khung) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-backdrop-far-01` | backdrop_far | thân cây vươn tới trời — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-backdrop-far-02` | backdrop_far | tán lá — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Cây Thế Giới, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `world_tree-floor-extra-01` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `world_tree-floor-extra-02` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `world_tree-floor-extra-03` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `world_tree-floor-extra-04` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `world_tree-floor-extra-05` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `world_tree-edge-01` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `world_tree-edge-02` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `world_tree-edge-03` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `world_tree-decal-01` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-02` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-03` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-04` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-05` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-06` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-07` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-08` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-09` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-10` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-11` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-decal-12` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `world_tree-shadow-01` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `world_tree-shadow-02` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `world_tree-shadow-03` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `world_tree-shadow-04` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `world_tree-backdrop-far` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `world_tree-backdrop-mid` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `world_tree-backdrop-near` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `world_tree-portal-dormant` | portal | cổng nhìn thẳng mặt trước, đúng tông kit |
| ⬜ | ⬜ | `world_tree-portal-active` | portal | cùng mask với dormant |
| ⬜ | ⬜ | `world_tree-marker-arrival` | marker | vòng sáng 4 khung |
| ⬜ | ⬜ | `world_tree-fx-01` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `world_tree-fx-02` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `world_tree-fx-03` | fx | hạt/tia sáng sprite sheet theo chủ đề |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Cây Thế Giới (world_tree). Style: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim.. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong apps/game-web/art-src/hd2d/batch-11-world_tree/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-world_tree` = 0 lỗi, contact-sheet mới hơn manifest.
```

## 3. Từng map

### `world_tree_gate` — Thế Thụ Môn

![world_tree_gate](refs/world_tree_gate.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/world_tree_gate.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/world_tree_gate.png`, 2476×860 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/CayTheGioi.unity`, 42 sprite ghép; brief: [../map-briefs/kit_world_tree/world_tree_gate.md](../map-briefs/kit_world_tree/world_tree_gate.md)
- Cổng: 2 · vùng quái: không · spawn: 0 · NPC: tree_vik, tree_willa
- neo `P:world_tree_portal_004` (door) Cửa → Thế Thụ Thâm Lâm: px [1766, 448]
- neo `P:world_tree_portal_005` (door) Cửa → Hải Tặc Hào: px [116, 547]
- neo `A:world_tree_portal_001` (arrival) Điểm đến từ Mật Thất Thế Thụ: px [1238, 760]
- neo `AT:ship:world_tree_gate` (arrival) Đến từ trụ Hải Tặc Hào: px [215, 537]
- neo `tree_vik` (npc) : px CẦN ĐẶT
- neo `tree_willa` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): tree_vik, tree_willa

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `world_tree_gate-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `world_tree_gate-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map world_tree_gate (), kit world_tree.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/world_tree_gate.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `world_tree_deep_woods` — Thế Thụ Thâm Lâm

![world_tree_deep_woods](refs/world_tree_deep_woods.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/world_tree_deep_woods.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/world_tree_deep_woods.png`, 2586×946 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/CayTheGioi.unity`, 37 sprite ghép; brief: [../map-briefs/kit_world_tree/world_tree_deep_woods.md](../map-briefs/kit_world_tree/world_tree_deep_woods.md)
- Cổng: 2 · vùng quái: có · spawn: 17 · NPC: — · ghi chú: tên nguồn trùng
- neo `P:world_tree_portal_002` (door) Cửa → Thế Thụ Môn: px [180, 549]
- neo `P:world_tree_portal_003` (door) Cửa → Thế Thụ Môn: px [2253, 539]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `world_tree_deep_woods-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `world_tree_deep_woods-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map world_tree_deep_woods (), kit world_tree.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/world_tree_deep_woods.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `world_tree_secret_chamber` — Mật Thất Thế Thụ

![world_tree_secret_chamber](refs/world_tree_secret_chamber.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/world_tree_secret_chamber.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/world_tree_secret_chamber.png`, 2586×950 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/CayTheGioi.unity`, 40 sprite ghép; brief: [../map-briefs/kit_world_tree/world_tree_secret_chamber.md](../map-briefs/kit_world_tree/world_tree_secret_chamber.md)
- Cổng: 1 · vùng quái: có · spawn: 17 · NPC: —
- neo `P:world_tree_portal_001` (door) Cửa → Thế Thụ Môn: px [191, 587]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `world_tree_secret_chamber-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `world_tree_secret_chamber-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map world_tree_secret_chamber (), kit world_tree.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```
