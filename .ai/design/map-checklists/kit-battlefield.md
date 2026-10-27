# Kit `battlefield` — Chiến Địa Kết Minh

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Đất cháy xém, vũ khí cắm đất, chiến xa hỏng, tháp canh gỗ; khói lửa.
- Thư mục asset: `apps/game-web/art-src/hd2d/batch-11-battlefield/`
- Số map: 1

## 1. Danh sách asset cần vẽ (kit chưa có asset)

Nguồn: Phần C `hd2d-maps-75-gemini-prompt.md`. Yêu cầu gốc: tile đất cháy, đất nứt, cỏ cháy; prop: vũ khí cắm ×4, chiến xa hỏng, tháp canh gỗ, rào chắn, cờ rách ×2 màu, hố bom, đống lửa (4 khung), xương/giáp vỡ; backdrop xa: chân trời khói lửa.

| Vẽ | Duyệt | id (số thứ tự; đặt tên tiếng Anh vào manifest `name`) | loại | mô tả + prompt đi kèm |
|---|---|---|---|---|
| ⬜ | ⬜ | `battlefield-floor-01` | floor | đất cháy — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-floor-02` | floor | đất nứt — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-floor-03` | floor | cỏ cháy — tile sàn nhìn từ trên xuống, seamless 512×512; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-01` | prop | vũ khí cắm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-02` | prop | vũ khí cắm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-03` | prop | vũ khí cắm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-04` | prop | vũ khí cắm — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-05` | prop | chiến xa hỏng — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-06` | prop | tháp canh gỗ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-07` | prop | rào chắn — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-08` | prop | cờ rách màu — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-09` | prop | cờ rách màu — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-10` | prop | hố bom — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-11` | prop | đống lửa (4 khung) — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-prop-12` | prop | xương/giáp vỡ — prop đứng billboard, pivot giữa-đáy; HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-backdrop-far-01` | backdrop_far | chân trời khói lửa — backdrop xa 1280×384 lặp ngang liền (64 px/đơn vị); HD-2D Octopath pixel art, palette Chiến Địa Kết Minh, outline tối cùng sắc, 33–48 màu, không bóng đổ/sương/chữ. |
| ⬜ | ⬜ | `battlefield-floor-extra-01` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `battlefield-floor-extra-02` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `battlefield-floor-extra-03` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `battlefield-floor-extra-04` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `battlefield-floor-extra-05` | floor | tile sàn bổ sung (đủ ≥8 biến thể khác texture), seamless 512×512 |
| ⬜ | ⬜ | `battlefield-edge-01` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `battlefield-edge-02` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `battlefield-edge-03` | edge | dải chuyển tiếp giữa 2 tile chính, 512×128 liền hai đầu, mép bất quy tắc |
| ⬜ | ⬜ | `battlefield-decal-01` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-02` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-03` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-04` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-05` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-06` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-07` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-08` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-09` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-10` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-11` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-decal-12` | decal | decal tiếp đất theo chủ đề kit (vụn, vết, xương/đá), bất quy tắc, mép mềm |
| ⬜ | ⬜ | `battlefield-shadow-01` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `battlefield-shadow-02` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `battlefield-shadow-03` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `battlefield-shadow-04` | shadow | bóng procedural alpha mềm, màu kit |
| ⬜ | ⬜ | `battlefield-backdrop-far` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `battlefield-backdrop-mid` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `battlefield-backdrop-near` | backdrop | 1280×384, lặp ngang liền, mỗi tầng một khung cảnh khác |
| ⬜ | ⬜ | `battlefield-portal-dormant` | portal | cổng nhìn thẳng mặt trước, đúng tông kit |
| ⬜ | ⬜ | `battlefield-portal-active` | portal | cùng mask với dormant |
| ⬜ | ⬜ | `battlefield-marker-arrival` | marker | vòng sáng 4 khung |
| ⬜ | ⬜ | `battlefield-fx-01` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `battlefield-fx-02` | fx | hạt/tia sáng sprite sheet theo chủ đề |
| ⬜ | ⬜ | `battlefield-fx-03` | fx | hạt/tia sáng sprite sheet theo chủ đề |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Chiến Địa Kết Minh (battlefield). Style: Đất cháy xém, vũ khí cắm đất, chiến xa hỏng, tháp canh gỗ; khói lửa.. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong apps/game-web/art-src/hd2d/batch-11-battlefield/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-battlefield` = 0 lỗi, contact-sheet mới hơn manifest.
```

## 3. Từng map

### `guild_battlefield_main_field` — Chiến Địa Kết Minh

![guild_battlefield_main_field](refs/guild_battlefield_main_field.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/guild_battlefield_main_field.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/guild_battlefield_main_field.png`, 2519×848 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/HoatDong/GuildChien.unity`, 21 sprite ghép; brief: chưa có
- Cổng: 1 · vùng quái: không · spawn: 0 · NPC: —
- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.

Asset chính: dùng bảng kit (mục 1). Landmark riêng của map (Codex xem ảnh gốc, ghi tên vật nhận diện vào bảng rồi vẽ):

| Vẽ | Duyệt | id | loại | mô tả | prompt |
|---|---|---|---|---|---|
| ⬜ | ⬜ | `guild_battlefield_main_field-landmark-01` | landmark | (vật nhận diện #1 trong ảnh gốc) | — |
| ⬜ | ⬜ | `guild_battlefield_main_field-landmark-02` | landmark | (vật nhận diện #2, nếu có) | — |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map guild_battlefield_main_field (), kit battlefield.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/guild_battlefield_main_field.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```
