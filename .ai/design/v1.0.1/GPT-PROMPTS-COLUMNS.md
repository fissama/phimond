# Prompt vẽ lại cột / trụ — 2026-10-30

Hiện trạng (xem `columns-current-sheet.png`): `hall-column` (224×560) là cái xấu nhất — bị cắt mất mép trái, có vệt thừa ở góc trên-trái, bề mặt lốm đốm dither nên khi phóng to trong Sảnh nhìn như bị bể. `palace-column`, `palace-marble-pillar` sạch hơn nên dùng làm ảnh tham chiếu phong cách. `arena-column` và `city-carved-pillar` ổn nhưng hơi thô, vẽ lại sau.

Quy tắc chung (dán đầu mọi prompt): *Pixel art for an HD-2D game in the style of Octopath Traveler, crisp pixels, painterly shading, light from the TOP-LEFT, no anti-aliasing, no blur, no watermark, max 48 colors, binary alpha. Background is a single flat magenta #FF00FF (no soft edge, no pink/lilac fringe pixels, none inside the artwork). Output PNG exactly the size stated, one asset per image.*

Tiêu chí duyệt chung: cột đối xứng trái–phải, **không bị cắt mép nào**, chừa 4 px lề magenta mỗi bên, đáy chạm cách mép dưới 8 px (chân cột đặt tại giữa đáy), bề mặt thân cột là mảng màu sạch có đường rãnh rõ, không dither lốm đốm.

## C1. `hall-column.png` (224×560) — ưu tiên số 1
Đính kèm: `palace-column.png` (phong cách vàng–ngà), `palace-marble-pillar.png`, `hall-column.png` (bản hiện tại, chỉ để giữ tỉ lệ và vị trí, KHÔNG sao chép lỗi).
> Tall fluted marble column for the main hall of a summoning palace, 224×560. Same cream-ivory stone with warm gold trim as the first two attachments. Structure from top to bottom: square abacus slab, gold-banded echinus with a row of rounded gold beads, a straight shaft with 7 clearly visible vertical flutes (light on the left flutes, shadow on the right), a thick gold ring near the base, a round torus, then an octagonal plinth. Perfectly symmetric, fully inside the canvas with a 4 px magenta margin on the left and right, nothing cropped. The shaft is clean flat colour bands with sharp flute lines, NOT speckled or noisy. Light from the TOP-LEFT. No ground shadow, no floor, no background objects.

## C2. `palace-column.png` (178×416)
Đính kèm: `palace-column.png`, `palace-marble-pillar.png`.
> Same column as the first attachment (Corinthian-style capital with gold leaf ornament, cream shaft with a gold scroll motif, grey-green stone base), redrawn at 178×416 with cleaner outlines and no speckle noise, identical composition and proportions, symmetric, 4 px margin, light from top-left.

## C3. `arena-column.png` (148×366)
Đính kèm: `arena-column.png`, `palace-column.png`.
> Same gold spiral-ribbon column as the first attachment (gold capital with leaf pattern, red base trim, ribbon winding around a gold shaft), redrawn at 148×366: the ribbon must wind consistently in one direction with even spacing, edges crisp, red trim only at base and capital rim, symmetric silhouette, light from top-left.

## C4. `city-carved-pillar.png` (110×266)
Đính kèm: `city-carved-pillar.png`, `palace-marble-pillar.png`.
> Same short carved stone pillar as the first attachment (ball finial, stepped cap, carved leaf panel, stepped base), redrawn at 110×266 in the same cream-gold palette as the second attachment, crisp panel carving, symmetric, light from top-left.

Gợi ý quy trình: gửi C1 trước; nếu thân cột vẫn lốm đốm, thêm câu "Use at most 6 flat tones for the shaft; do not add noise or film grain". Mỗi ảnh một lượt riêng, gửi lại file kết quả để mình duyệt và lắp (kích thước/pivot giữ nguyên nên không cần sửa code).
