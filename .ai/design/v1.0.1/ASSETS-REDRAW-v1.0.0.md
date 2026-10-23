# Danh sách asset cần vẽ lại từ v1.0.0 (gửi ChatGPT)

> Trạng thái từng mục (đã vẽ / đã duyệt) nằm ở `CHECKLIST-REDRAW-CODEX.md`. File này giữ quy cách và prompt mẫu.

Gộp từ `GPT-REMAINING.md` (mục 1–17) và phần mới sau đợt rà chuyển động. Quy tắc gửi: **từng ảnh một kèm prompt, không gửi zip**; tên file đặt đúng như cột "Lưu thành".

## Quy ước chung (dán đầu mỗi prompt)

- Khung **192×192 px**, người cao ~168 px, **chân ở (96,184)**, nền **ma-gen-ta #FF00FF**, alpha nhị phân (không bóng mờ), ≤64 màu.
- Pixel-art nhìn chéo kiểu Octopath, ánh sáng từ **trên-trái**, viền tối 1 px, không khử răng cưa.
- Dải khung là **một hàng ngang**, các khung đều nhau; mọi khung cùng chiều cao thân và **cùng điểm chân** (không để thân nhảy lên xuống giữa các khung, trừ nhịp nảy của bước chân).
- **Chu kỳ đi 8 khung**: 2 khung chạm đất, 2 khung nhấc chân, đổi chân ở giữa chu kỳ; khung đầu và khung cuối nối liền được (vòng lặp). Code đã dựng nhịp theo quãng đường (mỗi ô ≈ 4 khung), nên 8 khung = đúng 1 chu kỳ hai bước mỗi 2 ô.
- Nhân vật **nhìn sang phải** với dải ngang (code tự lật khi đi trái).

## P0 — gây cảm giác "lướt/không mượt" (làm trước)

| # | Asset | Số khung | Lưu thành | Ghi chú |
|---|---|---|---|---|
| 1 | Nam chính đi **ngang** (vẽ lại) | 8 | `player-male.run.png` | Dải cũ 6 khung, nhịp chân hơi cứng. Đổi chân rõ, tay vung ngược chân. |
| 2 | Nữ chính đi **ngang** (vẽ lại) | 8 | `player-female.run.png` | Như trên; áo/tóc có nhịp bay nhẹ trễ sau thân. |
| 3 | Nam chính đi **xuống** (vẽ lại, đều hàng) | 8 | `player-male.run-down.png` | Dải cũ có hàng 2 thấp hơn hàng 1, sinh ra nhảy. Nhìn thẳng về camera. |
| 4 | Nữ chính đi **xuống** (mới) | 8 | `player-female.run-down.png` | Hiện chưa có → đi dọc đang dùng hình đi ngang nên nhìn như trượt ngang. |
| 5 | Nam chính đi **lên** (mới) | 8 | `player-male.run-up.png` | Nhìn từ sau lưng. |
| 6 | Nữ chính đi **lên** (mới) | 8 | `player-female.run-up.png` | Nhìn từ sau lưng. |
| 7 | **Người đi đường** ×6 (đi ngang): baker, elder, boy, girl, guard, traveller | 8 | `walker-<tên>.run.png` | Hiện chỉ **2 khung** → bước cứng, trượt. Đây là nguyên nhân chính NPC "lướt". |
| 8 | Người đi đường ×6 đi **xuống** và **lên** | 8 | `walker-<tên>.run-down.png`, `walker-<tên>.run-up.png` | Thiếu → đi dọc thành trượt ngang. Nếu hạn chế lượt vẽ: làm tối thiểu cho baker, boy, girl trước. |

Prompt mẫu (mục 1, đổi hướng/giới tính cho các mục còn lại):

> Pixel art game sprite sheet, one horizontal strip of 8 frames, each frame 192×192 px, magenta #FF00FF background, binary alpha, ≤64 colors, 1px dark outline, light from top-left, Octopath Traveler isometric-3/4 view. A young adventurer (male: dark-blue hair, brown coat with gold trim, boots) **walking to the right**, a looping 8-frame walk cycle: frame 1 contact, 2 passing, 3 high point, 4 contact on the other foot, repeating on the opposite leg for frames 5–8. Arms swing opposite to the legs. Body height ~168 px, **feet anchored at (96,184) in every frame**, identical outfit and proportions to the idle strip I attached. Output 1536×192.

## P1 — sảnh, nhân vật, hội thoại

| # | Asset | Lưu thành | Ghi chú |
|---|---|---|---|
| 9 | **Chờ 4 khung** cho 7 NPC nộp tạm: Mira, bia_skill, bia_free, trụ đá, kỹ năng, sàn giao dịch, kho | `npc-<id>.idle.png` (4 khung, 768×192) | Mira là NPC đầu tiên người chơi gặp, ưu tiên số 1. Thở nhẹ, đổi trọng tâm, cầm trượng đung đưa. |
| 10 | **Chân dung bán thân NPC** 256×256 cho 19 NPC | `portrait-<id>.png` | Ưu tiên: Mira, Lio, Rowan, Tamo, Mero, Karn, Tessa, Selka. |
| 11 | **Ảnh chọn starter** lớn 3 linh thú (Tiên Chưởng, Sa Hạt, Xích Ưng) | `starter-<id>.png` | Cho thẻ xác nhận chọn bệ. |
| 12 | **Chân dung chọn nhân vật** nam/nữ, bán thân 256×256, nền ma-gen-ta | `slot-male.png`, `slot-female.png` | Mới: màn "Chọn nhân vật" (3 ô) và bước chọn Nam/Nữ hiện dùng khung chờ cắt từ dải idle, hơi nhỏ. |
| 13 | **Hiệu ứng triệu hồi**: cột sáng + vòng sáng từ vòng triệu hồi (6 khung, 192×384, nền ma-gen-ta, cộng sáng) | `fx-summon.png` | Mới: lúc nhân vật hiện ra giữa vòng. Hiện đang dùng ống sáng vẽ bằng code (tạm). |

## P2 — trận đấu và HUD

| # | Asset | Lưu thành |
|---|---|---|
| 14 | Nền trận 5 ảnh 1920×1080 (forest, deep_forest, gate, city, hall); prompt có sẵn trong `battle-bg/PROMPTS.md` | `apps/client/public/battle/battle-bg-<key>.png` |
| 15 | Hiệu ứng kỹ năng theo hệ (lửa, nước, cây, đất, thú, côn trùng), 6 khung/hiệu ứng | `fx-<hệ>.png` |
| 16 | Khung thanh chỉ số có nhãn (HP/MP/EXP), tách nhãn khỏi thanh | `bar-frame-*.png` |
| 17 | Vòng cảnh báo quái trên map: vòng rune đỏ cam 4 khung, nhìn từ trên xuống | `foe-ring.png` |
| 18 | Dải trang trí thanh dưới (thanh đá hoa văn giữa) | `ui-bottombar.png` |
| 19 | Khung bản đồ nhỏ, khung Mục tiêu, hộp chat cùng ngôn ngữ khung vàng | `ui-*` |

## P3 — cảnh

| # | Asset |
|---|---|
| 20 | Bóng tiếp xúc: tròn nhỏ/lớn, chữ nhật, dài theo tán, cùng hướng sáng |
| 21 | Thảm/gạch/bệ Hoàng Môn và Quảng Trường: viền thảm tua, bậc đá, mép gạch vỡ vào đá cuội, 2–3 biến thể đá cuội, bệ giếng tròn có bóng |
| 22 | Mảnh nối mặt tiền nhà (ngõ, ống máng, cột) |
| 23 | Biến thể mảnh chuyển đường đất để phá nhịp lặp (DEBT D10) |

## Cách nạp sau khi có ảnh

1. Đặt file vào `apps/client/public/hd2d/` (nhân vật/NPC) hoặc thư mục ghi ở bảng.
2. Cập nhật `assets.json`: `run_frames`, `run_down_frames`, `run_up_frames`, `idle_frames` đúng số khung. **Chỉ dùng `sync_client_assets.py --merge`**, không chạy bản đầy đủ.
3. Code **không cần sửa**: nhịp bước đã bám theo quãng đường, dải dọc tự dùng khi có. Với người đi đường, khi có dải dọc cần thêm `run_down_frames`/`run_up_frames` vào mục asset của họ.
