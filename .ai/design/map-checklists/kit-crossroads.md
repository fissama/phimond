# Kit `crossroads` — Ngã Tư / Địa Đạo

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Hang địa đạo xanh lam đêm, rêu biếc, thủy quang, san hô tím. Một chuỗi phòng cùng nền, đổi sắc nhẹ theo phòng.
- Thư mục asset: `apps/game-web/art-src/hd2d/batch-11-crossroads/`
- Số map: 6

## 1. Danh sách asset cần vẽ (kit chưa có asset)

Nguồn: Phần C `hd2d-maps-75-gemini-prompt.md`. Yêu cầu gốc: tile đá hang ẩm, đường mòn đá cuội, rêu biếc, mặt nước nông (viền bọt 4 khung), đáy hang; prop: măng đá ×4, thạch nhũ treo ×3, san hô tím ×3, nấm phát quang ×3, ván cầu đá, cột đá chống hầm, đèn hang, cổng hầm; backdrop xa: vách hang sâu, ánh sáng cửa hang.

| Vẽ | Duyệt | id (số thứ tự; đặt tên tiếng Anh vào manifest `name`) | loại | mô tả + prompt đi kèm |
|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads-floor-01` | floor | đá hang ẩm — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-floor-02` | floor | đường mòn đá cuội — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-floor-03` | floor | rêu biếc — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-floor-04` | floor | mặt nước nông (viền bọt 4 khung) — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-floor-05` | floor | đáy hang — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-01` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-02` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-03` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-04` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-05` | prop | thạch nhũ treo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-06` | prop | thạch nhũ treo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-07` | prop | thạch nhũ treo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-08` | prop | san hô tím — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-09` | prop | san hô tím — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-10` | prop | san hô tím — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-11` | prop | nấm phát quang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-12` | prop | nấm phát quang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-13` | prop | nấm phát quang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-14` | prop | ván cầu đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-15` | prop | cột đá chống hầm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-16` | prop | đèn hang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-prop-17` | prop | cổng hầm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-backdrop-far-01` | backdrop_far | vách hang sâu — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-backdrop-far-02` | backdrop_far | ánh sáng cửa hang — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `crossroads-floor-extra-01` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `crossroads-floor-extra-02` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `crossroads-floor-extra-03` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `crossroads-edge-01` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `crossroads-edge-02` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `crossroads-edge-03` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `crossroads-decal-01` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-02` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-03` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-04` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-05` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-06` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-07` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-08` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-09` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-10` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-11` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-decal-12` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `crossroads-shadow-01` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `crossroads-shadow-02` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `crossroads-shadow-03` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `crossroads-shadow-04` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `crossroads-backdrop-far` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `crossroads-backdrop-mid` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `crossroads-backdrop-near` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `crossroads-portal-dormant` | portal | cổng nhìn thẳng mặt trước, đúng tông kit |
| ⬜ | ⬜ | `crossroads-portal-active` | portal | cùng mask với dormant |
| ⬜ | ⬜ | `crossroads-marker-arrival` | marker | vòng sáng 4 khung |
| ⬜ | ⬜ | `crossroads-fx-01` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `crossroads-fx-02` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `crossroads-fx-03` | fx | hạt/tia sáng sprite sheet theo chủ đề |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Ngã Tư / Địa Đạo (crossroads). Style: Hang địa đạo xanh lam đêm, rêu biếc, thủy quang, san hô tím. Một chuỗi phòng cùng nền, đổi sắc nhẹ theo phòng.. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong apps/game-web/art-src/hd2d/batch-11-crossroads/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-crossroads` = 0 lỗi, contact-sheet mới hơn manifest.
```

## 3. Từng map

### `crossroads_unnamed_area_01` — Cổng Địa Đạo Lam Dạ

![crossroads_unnamed_area_01](refs/crossroads_unnamed_area_01.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_01.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_01.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_01.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_01.md)
- Cổng: 3 · vùng quái: không · spawn: 0 · NPC: cross_elric, cross_fara · ghi chú: nối Quảng trường; hub 02 + 05
- neo `P:crossroads_portal_003` (door) Cửa → Hốc San Hô Tím: px [1025, 713]
- neo `P:crossroads_portal_006` (door) Cửa → Hành Lang Rêu Biếc: px [2130, 494]
- neo `P:crossroads_portal_010` (door) Cửa → Quảng Trường Thạch Trụ: px [114, 518]
- neo `AT:square:crossroads_unnamed_area_01` (arrival) Đến từ trụ Quảng Trường: px [214, 508]
- neo `cross_elric` (npc) : px CẦN ĐẶT
- neo `cross_fara` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): cross_elric, cross_fara

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads_unnamed_area_01-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `crossroads_unnamed_area_01-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_01 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_01.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `crossroads_unnamed_area_02` — Hành Lang Rêu Biếc

![crossroads_unnamed_area_02](refs/crossroads_unnamed_area_02.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_02.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_02.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_02.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_02.md)
- Cổng: 2 · vùng quái: có · spawn: 12 · NPC: — · ghi chú: chuỗi 01→02→03→04→06
- neo `P:crossroads_portal_004` (door) Cửa → Cổng Địa Đạo Lam Dạ: px [118, 489]
- neo `P:crossroads_portal_007` (door) Cửa → Đoạn Thủy Quang: px [2130, 509]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads_unnamed_area_02-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `crossroads_unnamed_area_02-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_02 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_02.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `crossroads_unnamed_area_03` — Đoạn Thủy Quang

![crossroads_unnamed_area_03](refs/crossroads_unnamed_area_03.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_03.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_03.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_03.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_03.md)
- Cổng: 2 · vùng quái: có · spawn: 12 · NPC: cross_gwen
- neo `P:crossroads_portal_005` (door) Cửa → Hành Lang Rêu Biếc: px [118, 519]
- neo `P:crossroads_portal_011` (door) Cửa → Ngã Ba Đêm Xanh: px [2078, 489]
- neo `cross_gwen` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): cross_gwen

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads_unnamed_area_03-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `crossroads_unnamed_area_03-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_03 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_03.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `crossroads_unnamed_area_04` — Ngã Ba Đêm Xanh

![crossroads_unnamed_area_04](refs/crossroads_unnamed_area_04.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_04.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_04.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_04.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_04.md)
- Cổng: 2 · vùng quái: có · spawn: 10 · NPC: cross_hale
- neo `P:crossroads_portal_001` (door) Cửa → Đoạn Thủy Quang: px [172, 505]
- neo `P:crossroads_portal_008` (door) Cửa → Đáy Địa Đạo: px [752, 745]
- neo `cross_hale` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): cross_hale

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads_unnamed_area_04-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `crossroads_unnamed_area_04-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_04 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_04.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `crossroads_unnamed_area_05` — Hốc San Hô Tím

![crossroads_unnamed_area_05](refs/crossroads_unnamed_area_05.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_05.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_05.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_05.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_05.md)
- Cổng: 1 · vùng quái: có · spawn: 10 · NPC: cross_ines · ghi chú: cụt, nhánh từ 01
- neo `P:crossroads_portal_009` (door) Cửa → Cổng Địa Đạo Lam Dạ: px [1930, 389]
- neo `cross_ines` (npc) : px CẦN ĐẶT
- NPC cần sprite (batch-05; kiểm trùng): cross_ines

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads_unnamed_area_05-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `crossroads_unnamed_area_05-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_05 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_05.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `crossroads_unnamed_area_06` — Đáy Địa Đạo

![crossroads_unnamed_area_06](refs/crossroads_unnamed_area_06.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_06.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_06.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_06.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_06.md)
- Cổng: 1 · vùng quái: có · spawn: 10 · NPC: — · ghi chú: cuối chuỗi
- neo `P:crossroads_portal_002` (door) Cửa → Ngã Ba Đêm Xanh: px [268, 393]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `crossroads_unnamed_area_06-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `crossroads_unnamed_area_06-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_06 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_06.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```
