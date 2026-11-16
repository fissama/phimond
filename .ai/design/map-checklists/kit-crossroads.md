# Kit `crossroads` — Ngã Tư / Địa Đạo

> **Nghiệm thu Claude 2026-11-09** (mức V1, chưa 4×): VẼ_LẠI 12, DUYỆT 46, SỬA_ĐÓNG_GÓI_METADATA 4. Map: {'CHƯA ĐỦ': 6}. Trạng thái hiện hành ở [ASSET-VERDICTS-20261109.csv](ASSET-VERDICTS-20261109.csv) / [MAP-COVERAGE-20261109.csv](MAP-COVERAGE-20261109.csv); tick ✅/❌ bên dưới là LỊCH SỬ, không phải approval.
> VẼ_LẠI (12): `crossroads-floor-01`, `crossroads-floor-02`, `crossroads-floor-03`, `crossroads_unnamed_area_02-landmark-01`, `crossroads-floor-05`, `crossroads-floor-04`, `crossroads-floor-extra-01`, `crossroads-floor-extra-02`, `crossroads-floor-extra-03`, `crossroads-edge-01`, `crossroads-edge-02`, `crossroads-edge-03`

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Hang địa đạo xanh lam đêm, rêu biếc, thủy quang, san hô tím. Một chuỗi phòng cùng nền, đổi sắc nhẹ theo phòng.
- Thư mục asset: `art/src/hd2d/batch-11-crossroads/`
- Số map: 6

## 1. Danh sách asset cần vẽ (kit chưa có asset)

Nguồn: Phần C `hd2d-maps-75-gemini-prompt.md`. Yêu cầu gốc: tile đá hang ẩm, đường mòn đá cuội, rêu biếc, mặt nước nông (viền bọt 4 khung), đáy hang; prop: măng đá ×4, thạch nhũ treo ×3, san hô tím ×3, nấm phát quang ×3, ván cầu đá, cột đá chống hầm, đèn hang, cổng hầm; backdrop xa: vách hang sâu, ánh sáng cửa hang.

> Cập nhật 30/10: cột **Vẽ** đánh dấu final có bằng chứng QA/review; không có nghĩa là kit đã qua dựng thử hoặc được duyệt. Crop/blend thử cho `crossroads-floor-01` loại viền khung nhưng repeat 3×3 vẫn lộ chu kỳ cụm đá; giữ final hiện tại để owner đánh giá. Edge-01..03 mới đã đóng gói 512×128, alpha nhị phân, 48 màu; repeat 3× đã được nhìn. Backdrop xa 01–02 đã có preview repeat; sheet backdrop chưa được Claude xem. Art gate mới nhất quét 411 asset thuộc các batch 11: 0 lỗi, 0 cảnh báo. Mọi asset vẫn chờ owner review.

| Vẽ | Duyệt | id (số thứ tự; đặt tên tiếng Anh vào manifest `name`) | loại | mô tả + prompt đi kèm |
|---|---|---|---|---|
| ✅ | ⬜ | `crossroads-floor-01` | floor | đá hang ẩm — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-floor-02` | floor | đường mòn đá cuội — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-floor-03` | floor | rêu biếc — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-floor-04` | floor | mặt nước nông (viền bọt 4 khung) — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-floor-05` | floor | đáy hang — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-01` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-02` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-03` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-04` | prop | măng đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-05` | prop | thạch nhũ treo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-06` | prop | thạch nhũ treo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-07` | prop | thạch nhũ treo — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-08` | prop | san hô tím — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-09` | prop | san hô tím — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-10` | prop | san hô tím — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-11` | prop | nấm phát quang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-12` | prop | nấm phát quang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-13` | prop | nấm phát quang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-14` | prop | ván cầu đá — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-15` | prop | cột đá chống hầm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-16` | prop | đèn hang — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-prop-17` | prop | cổng hầm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-backdrop-far-01` | backdrop_far | vách hang sâu — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-backdrop-far-02` | backdrop_far | ánh sáng cửa hang — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Ngã Tư / Địa Đạo, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ✅ | ⬜ | `crossroads-floor-extra-01` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ✅ | ⬜ | `crossroads-floor-extra-02` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ✅ | ⬜ | `crossroads-floor-extra-03` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ✅ | ⬜ | `crossroads-edge-01` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ✅ | ⬜ | `crossroads-edge-02` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ✅ | ⬜ | `crossroads-edge-03` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ✅ | ⬜ | `crossroads-decal-01` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-02` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-03` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-04` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-05` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-06` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-07` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-08` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-09` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-10` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-11` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-decal-12` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ✅ | ⬜ | `crossroads-shadow-01` | shadow | bóng procedural alpha mềm, màu kit |
| ✅ | ⬜ | `crossroads-shadow-02` | shadow | bóng procedural alpha mềm, màu kit |
| ✅ | ⬜ | `crossroads-shadow-03` | shadow | bóng procedural alpha mềm, màu kit |
| ✅ | ⬜ | `crossroads-shadow-04` | shadow | bóng procedural alpha mềm, màu kit |
| ✅ | ⬜ | `crossroads-backdrop-far` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác; xem hai biến thể `crossroads-backdrop-far-01/02` phía trên |
| ✅ | ⬜ | `crossroads-backdrop-mid` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ✅ | ⬜ | `crossroads-backdrop-near` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ✅ | ⬜ | `crossroads-portal-dormant` | portal | cổng nhìn thẳng mặt trước, đúng tông kit |
| ✅ | ⬜ | `crossroads-portal-active` | portal | cùng mask với dormant |
| ✅ | ⬜ | `crossroads-marker-arrival` | marker | vòng sáng 4 khung |
| ✅ | ⬜ | `crossroads-fx-01` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ✅ | ⬜ | `crossroads-fx-02` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ✅ | ⬜ | `crossroads-fx-03` | fx | hạt/tia sáng sprite sheet theo chủ đề |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Ngã Tư / Địa Đạo (crossroads). Style: Hang địa đạo xanh lam đêm, rêu biếc, thủy quang, san hô tím. Một chuỗi phòng cùng nền, đổi sắc nhẹ theo phòng.. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong art/src/hd2d/batch-11-crossroads/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-crossroads` = 0 lỗi, contact-sheet mới hơn manifest.
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
| ✅ | ⬜ | `crossroads_unnamed_area_01-landmark-01` | reused prop | Cairn đá thấp bên trái; dùng `batch-01-octopath/rock-small` đã có, không vẽ trùng | [asset](../../../art/src/hd2d/batch-01-octopath/rock-small/final.png) |
| ✅ | ⬜ | `crossroads_unnamed_area_01-landmark-02` | reused prop | Chồng 3 thùng gỗ cạnh vách sau; dùng candidate Map 02 `crossroads_unnamed_area_02-landmark-01`, không vẽ trùng | [asset](../../../art/src/hd2d/batch-11-crossroads/crossroads_unnamed_area_02-landmark-01/final.png) |

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
| ✅ | ⬜ | `crossroads_unnamed_area_02-landmark-01` | landmark | Chồng 3 thùng gỗ cạnh vách sau (candidate riêng Map 02, tái dùng ở Map 01) | [asset](../../../art/src/hd2d/batch-11-crossroads/crossroads_unnamed_area_02-landmark-01/final.png) |
| — | — | `crossroads_unnamed_area_02-landmark-02` | — | Không thấy landmark độc nhất thứ hai trong ảnh gốc | — |

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

Không có landmark riêng cần vẽ thêm: ảnh chỉ dùng các cột hang/thạch nhũ, san hô và chồng thùng lặp lại đã được đại diện bởi prop dùng chung hoặc landmark Map 02.

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| — | — | `no-unique-landmark` | — | Không có landmark riêng cần vẽ; dùng props hang và thùng tái sử dụng | — |


Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_03 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_03.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: không phát hiện; giữ props dùng chung, không tạo asset trùng.
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

Không có landmark riêng cần vẽ thêm: ảnh chỉ dùng các cột hang/thạch nhũ, san hô và chồng thùng lặp lại đã được đại diện bởi prop dùng chung hoặc landmark Map 02.

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| — | — | `no-unique-landmark` | — | Không có landmark riêng cần vẽ; dùng props hang và thùng tái sử dụng | — |


Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_04 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_04.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: không phát hiện; giữ props dùng chung, không tạo asset trùng.
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

Không có landmark riêng cần vẽ thêm: ảnh chỉ dùng các cột hang/thạch nhũ, san hô và chồng thùng lặp lại đã được đại diện bởi prop dùng chung hoặc landmark Map 02.

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| — | — | `no-unique-landmark` | — | Không có landmark riêng cần vẽ; dùng props hang và thùng tái sử dụng | — |


Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_05 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_05.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: không phát hiện; giữ props dùng chung, không tạo asset trùng.
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `crossroads_unnamed_area_06` — Đáy Địa Đạo

![crossroads_unnamed_area_06](refs/crossroads_unnamed_area_06.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/crossroads_unnamed_area_06.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/crossroads_unnamed_area_06.png`, 2256×837 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/35-40/GiaoDiem.unity`, 33 sprite ghép; brief: [../map-briefs/kit_crossroads/crossroads_unnamed_area_06.md](../map-briefs/kit_crossroads/crossroads_unnamed_area_06.md)
- Cổng: 1 · vùng quái: có · spawn: 10 · NPC: — · ghi chú: cuối chuỗi
- neo `P:crossroads_portal_002` (door) Cửa → Ngã Ba Đêm Xanh: px [268, 393]

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

Không có landmark riêng cần vẽ thêm: ảnh chỉ dùng các cột hang/thạch nhũ, san hô và chồng thùng lặp lại đã được đại diện bởi prop dùng chung hoặc landmark Map 02.

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| — | — | `no-unique-landmark` | — | Không có landmark riêng cần vẽ; dùng props hang và thùng tái sử dụng | — |


Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map crossroads_unnamed_area_06 (), kit crossroads.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/crossroads_unnamed_area_06.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: không phát hiện; giữ props dùng chung, không tạo asset trùng.
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```


### 2026-11-04 — Crossroads floor-01 redraw retries 01–07

- Read the Crossroads screenshot and style tile, attached actual refs to each image_gen call, and retained all raws/prompts/candidates/QA/3×3 reviews under `batch-11-crossroads/jobs/floor-redraw-20261104/`.
- 01 removed the framed edge but kept horizontal bands (seams 3.414/6.594); 02 repeated broad horizontal stones (5.620/9.855); 03 repeated subtle striation (5.093/6.838). 04 passes numeric seams (4.686/3.948) but has broad repeated blocks and soft finish. 05/06 pass seams (3.511/4.277, 4.275/5.981) but show repeated speck/texture clusters and softness. 07 has recurring crack clusters and seam failure (6.986/8.492). All seven were visually rejected; no manifest/contact-sheet/checklist drawn status change. Existing `crossroads-floor-01` remains.
- Next strategy should move away from text-only texture retries: compare the current tile alternatives in the real map composition and use placements of existing terrain/decal variants to disrupt repeat, without editing the audit or art gate.


### Landmark reconciliation — Crossroads maps 01–06 (2026-11-04)

Opened the six source map images and reconciled generic landmark placeholders against visible content. Map 01 reuses the small cairn (`batch-01-octopath/rock-small`) and the three-crate stack from Map 02; Map 02 keeps its already-drawn crate stack. Maps 03–06 show no additional unique landmark requiring a new asset; caves, coral and crate/cairn forms are represented by shared kit props. Vẽ means an existing reusable candidate is available; Duyệt remains unchecked. Source hashes:
- `crossroads_unnamed_area_01.jpg` SHA256 `7f6522193f17a5514164c1975e2073275cf9bc0471d2b5bf03fe50778369187a`
- `crossroads_unnamed_area_02.jpg` SHA256 `e7dc8fdff2fb20caec21410c4b0953f5914b9dd6d1129823cc4bce0225c67a75`
- `crossroads_unnamed_area_03.jpg` SHA256 `16b5c6d6cf9b5e9babcecc80b9caa4edd327fa6016733aa8ea753d7f34f6e258`
- `crossroads_unnamed_area_04.jpg` SHA256 `d5179f8cf3d2a83dc5d2d978820bccca7a3838786a1d4b95d458502e633e0d60`
- `crossroads_unnamed_area_05.jpg` SHA256 `12e304608c7efbe5435500a23bc2f8a28c9cd57edc2007955f01a33418d9f357`
- `crossroads_unnamed_area_06.jpg` SHA256 `21a3fd7580077dc3507f049919f8bce09eba0cd223dbd6ad5580a68ba789d5d0`


### 2026-11-04 — Far backdrop retry attempts 12–14

- Attempts 12–14 were generated with built-in `image_gen`; each raw PNG, prompt, reference paths/hashes, crop candidate and repeat preview is retained under `art/src/hd2d/batch-11-crossroads/jobs/backdrop-far-12/` through `backdrop-far-14/`.
- Attempt 12: edge mismatch after crop (mean 3.34, max 29); repeated shelf and mineral formations; rejected.
- Attempt 13: edge match close (mean 0.61, max 3), but recognizable wall silhouettes recur at each tile; rejected.
- Attempt 14: muted, less recognizable forms and quiet lower strip; 48-color quantized preview has seam mean 1.07/max 9. Global edge-color remap collapsed the palette to 14 colors and visibly degraded it, so that processed version is rejected. No backdrop was promoted; manifest, contact sheet, and checklist draw counts are unchanged.
- Art gate after retries: 494 assets, 0 errors, 0 warnings. Mechanical gate does not resolve the repeat/style review.
