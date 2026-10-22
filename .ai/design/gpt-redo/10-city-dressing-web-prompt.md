# Đơn 10 — Asset bổ sung cho thành phố (ChatGPT web)

- **Ngày:** 2026-10-22. **Dùng cho:** v1.0.1 (làm đầy Quảng Trường Thạch Trụ, Hoàng Môn; dùng lại cho Thương Phố/Vương Cung ở 1.1.0).
- **Bối cảnh:** sau khi thu map về dạng dải ngang và dựng lại cảnh bằng kit đã duyệt (dãy nhà liền, viền vườn, chợ, giếng, cờ), thành vẫn trống vì: (1) không có người qua lại, (2) chỉ có 4 kiểu mặt tiền nên lặp, (3) mặt đất lát đá một màu không có chi tiết, (4) thiếu đồ phố cỡ nhỏ.
- **Cách làm:** mở ChatGPT web, dán **Phần 0** một lần, rồi mỗi lần dán **một** prompt sheet kèm ảnh tham chiếu ghi trong sheet. Tải ảnh về và gửi lại trong chat với Claude; Claude cắt, khử nền, đưa về bảng màu, căn pivot và đưa vào game. ChatGPT web không cần (và không có) quyền vào repo.
- **Ảnh tham chiếu** (đính kèm khi được yêu cầu), ở `.ai/design/gpt-redo/refs-v1.0.1-city/`:
  - `approved-city-kit.png` — kit thành đã duyệt (nguồn STYLE)
  - `orig-city-square.png` — Quảng Trường bản gốc (nguồn NỘI DUNG, màu)
  - `current-city-square.png`, `current-palace-gate.png` — cảnh hiện tại (để thấy chỗ trống)

## Danh sách và ưu tiên

| # | Sheet | Asset | Ưu tiên | Lý do |
|---|---|---|---|---|
| 1 | Dân phố | 6 người qua đường không tương tác | **P1** | Hiệu quả lớn nhất: thành có người là hết trống |
| 2 | Mặt tiền bộ 2 | 6 kiểu nhà mới (quán trọ, tiệm bánh, sàn giao dịch, nhà kho, tháp chuông, nhà góc) | **P1** | Hết lặp 4 kiểu nhà |
| 3 | Đồ phố bộ 2 | 6 món (biển treo, dây cờ, đống bao tải, xe bán hàng có dù, bồn nước đá, cây cắt tỉa) | **P1** | Lấp khoảng giữa quảng trường |
| 4 | Decal mặt đất | 6 mảng phẳng (đá nứt, nắp cống, vũng nước, cánh hoa, vẽ phấn, vệt bánh xe) | **P1** | Mặt lát đá bớt đơn điệu |
| 5 | Động vật | chim bồ câu, mèo, chó, đàn bướm | P2 | Thêm sự sống |
| 6 | Mảnh nối nhà | ngõ có vòm, cột đá có ống máng, tường hộp hoa, hàng rào sắt | P2 | Nối các mặt tiền tự nhiên |
| 7 | Mái nhà lớp giữa | 1 dải mái/ống khói lặp ngang | P2 | Chiều sâu giữa mặt tiền và nền xa |
| 8 | Bộ Hoàng Môn | chòi lính, bồn cây dài, cột cờ, tường thành cao, cặp sư tử đá | P2 | Hoàng Môn trang nghiêm hơn |
| 9 | Đồ phố bộ 3 | 6 món (bảng tin, cột chỉ đường, xe hoa, ghế kèm bồn cây, thùng táo, đồng hồ phố) | P3 | Đa dạng thêm |

Sau khi có P1, Claude đặt vào Quảng Trường/Hoàng Môn và gửi ảnh chụp để duyệt.

---

## Phần 0 — Dán đầu phiên ChatGPT web

```text
You are a pixel-art asset painter for "Phimond", an HD-2D (Octopath Traveler style) fantasy town game. I will ask for one sprite SHEET at a time. Follow these rules for EVERY sheet:

STYLE (match the attached approved city kit exactly)
- Crisp pixel art, chunky readable clusters, 2–4 tone shading per material, dark SAME-HUE outlines (never pure black, never white/pink halos).
- Warm key light from upper-left-front, slightly cool shadows. NO cast shadow on the ground under objects (the engine draws shadows). NO text, letters, numbers, logos or watermarks anywhere.
- Palette family of the approved kit: cream/sand limestone, warm orange terracotta roofs, honey wood, dark iron, muted teal/green cloth, gold trim. Limited palette (about 40 colours per object), no smooth gradients, no glow, no dithering noise.
- Front-facing 3/4 view from slightly above, like the approved facades and props. Buildings and props stand upright on a flat baseline.

SCALE (important)
- 1 world unit = 128 px. A person is ~1.3 units tall (~168 px). A two-storey house front is ~4 units tall (~512 px).
- Draw every object at the size I give, or a clean integer multiple of it (2× is fine); keep all objects in one sheet at the SAME scale.

SHEET LAYOUT
- Flat pure magenta #FF00FF background, one single colour, no gradient, no texture, no vignette.
- Objects laid out in the grid I specify, each fully inside its own cell, at least 48 px of magenta between objects and from the sheet edge. Nothing touches or overlaps another object.
- No pink/magenta fringe around objects: edges are hard pixel edges.
- Do not add labels, frames, grid lines, or a title.
Reply only with the image.
```

---

## Sheet 1 — Dân phố (P1)

Đính kèm: `approved-city-kit.png` (chú ý hàng NPC dưới cùng), `orig-city-square.png`.

```text
SHEET 1 — Ambient townsfolk (non-interactive passers-by). Size 1536×1024, grid 3 columns × 2 rows, 6 full-body characters, each ~168 px tall (or 2× = ~336 px), all facing down-left in 3/4 view, standing idle, feet on a common baseline in each cell. Same art style and proportions as the approved NPC row in the attached kit (Octopath-like, slightly chibi head, detailed costume).
1) Boy ~10 years old, messy brown hair, patched tunic and shorts, holding a small wooden toy sword.
2) Girl ~8 years old, two braids, yellow dress with apron, hugging a red ball.
3) Elderly man with white beard and walking cane, brown waistcoat, flat cap.
4) Housewife carrying a wicker basket with bread and vegetables, green headscarf, long skirt.
5) Town guard on patrol: light steel helmet, blue tabard with a simple gold sun emblem (no letters), holding a spear upright.
6) Travelling merchant with a big backpack of pots and rolled cloth, wide hat, walking stick.
Each must have a different silhouette and dominant colour. No shadows, no text.
```

## Sheet 2 — Mặt tiền nhà bộ 2 (P1, 2 lần gọi)

Đính kèm: `approved-city-kit.png` (4 mặt tiền đầu hàng), `orig-city-square.png`.

```text
SHEET 2A — Town building fronts, set 2. Size 1536×1024, grid 3 columns × 1 row, 3 separate building facades. Each facade ~600–700 px wide and ~512 px tall at 1×, flat ground baseline at the bottom, the whole roof visible, transparent sky (magenta) above. Same style, materials, roof tiles and window shapes as the 4 approved facades in the attached kit, so they can stand side by side in one street.
1) Inn / tavern: two storeys, timber frame, wide double door, a blank hanging wooden sign on an iron bracket showing only a mug pictogram, small balcony with flower boxes.
2) Bakery: one-and-a-half storeys, big front window with bread loaves on display, striped cloth awning (teal and cream), a brick chimney (no smoke).
3) Exchange hall: grand stone building with columns and a pediment, double bronze doors, a carved scale pictogram above the door (no letters), blue banners.
No people, no shadows, no text.
```

```text
SHEET 2B — Town building fronts, set 2 (continued). Same size, grid and rules as Sheet 2A.
4) Warehouse: tall plain stone-and-wood building, huge barn-style wooden double doors with iron straps, a hoist beam with rope and pulley at the top, crates beside the door.
5) Bell-tower house: narrow two-storey house with a slim bell tower and terracotta spire on one side, small round window, ivy on the wall.
6) Corner house: house front with a rounded corner turret, flower boxes under every window, a small arched side passage.
No people, no shadows, no text.
```

## Sheet 3 — Đồ phố bộ 2 (P1)

Đính kèm: `approved-city-kit.png` (hàng đồ vật: đèn, ghế, thùng, giếng, chậu hoa, cờ).

```text
SHEET 3 — Street props, set 2. Size 1536×1024, grid 3 columns × 2 rows, 6 props, same scale as the approved props (a street lamp is ~266 px tall, a barrel ~160 px).
1) Hanging shop sign post: wooden post with an iron bracket and a blank wooden sign showing only a potion-bottle pictogram (~2 units tall).
2) Festival bunting: two thin wooden poles ~3.5 units apart with a string of small triangular cloth flags (teal, cream, orange) hanging between them.
3) Cluster of grain sacks and stacked wooden crates (~1.5 units wide).
4) Street vendor cart with a big round cloth parasol (teal and cream stripes) and fruit baskets (~2.5 units wide).
5) Small stone drinking basin / wall fountain with a lion-head spout, water in the basin (~1.5 units).
6) Potted topiary tree: round clipped bush on a stem in a large terracotta pot (~2 units tall).
No shadows, no text.
```

## Sheet 4 — Decal mặt đất (P1)

Đính kèm: `current-city-square.png` (để khớp màu đá lát).

```text
SHEET 4 — Flat ground decals for cream-sand cobblestone paving, seen straight from above (top-down, flat, no perspective, no height). Size 1536×1024, grid 3 columns × 2 rows, each decal ~256–384 px wide with irregular natural edges (not rectangles), colours matching the attached paving.
1) Cracked and broken paving patch with a few loose stones.
2) Square iron drain grate set into the stones.
3) Shallow rain puddle reflecting a little blue sky.
4) Scattered pink and white flower petals and two green leaves.
5) Children's chalk hopscotch drawing (only squares and a circle, no numbers or letters).
6) Wagon wheel ruts and a few pebbles.
No shadows, no text.
```

## Sheet 5 — Động vật (P2)

Đính kèm: `approved-city-kit.png`.

```text
SHEET 5 — Small town animals. Size 1536×1024, grid 3 columns × 2 rows, side/3-4 view, same pixel style.
1) Group of three grey pigeons pecking (~0.8 units wide).
2) Single pigeon taking off with wings open.
3) Orange tabby cat sitting, tail wrapped (~0.6 units tall).
4) Small brown dog lying down, relaxed (~1 unit long).
5) Pair of white-and-yellow butterflies.
6) Black crow standing.
No shadows, no text.
```

## Sheet 6 — Mảnh nối giữa các nhà (P2)

Đính kèm: `approved-city-kit.png` (mặt tiền, tường cung điện).

```text
SHEET 6 — Connector pieces that stand between building facades in a continuous street. Size 1536×1024, grid 4 columns × 1 row, each ~512 px tall at 1×, flat baseline.
1) Narrow dark alley entrance with a stone arch above (~1.5 units wide).
2) Square stone pillar with a copper drainpipe and climbing ivy (~0.8 units wide).
3) Plain wall segment with two window flower boxes (~2.5 units wide).
4) Wrought-iron garden fence with a small gate, hedge behind (~3 units wide, ~1.5 units tall, baseline aligned).
No shadows, no text.
```

## Sheet 7 — Dải mái nhà lớp giữa (P2)

Đính kèm: `approved-city-kit.png`, `current-city-square.png`.

```text
SHEET 7 — Mid-distance roofline strip seen behind the street facades: a continuous row of terracotta rooftops, chimneys, small dormers and two slim spires, slightly desaturated and lower contrast than the facades (atmospheric distance), no walls below the roofs except a thin band. Size 1536×1024: draw ONE horizontal strip ~1536 px wide and ~400 px tall centred vertically, magenta above and below. The left and right ends must continue each other so the strip can repeat horizontally without a visible seam. No shadows, no text.
```

## Sheet 8 — Bộ Hoàng Môn (P2)

Đính kèm: `approved-city-kit.png` (palace-gate, palace-tower, palace-wall-section, tượng lính), `current-palace-gate.png`.

```text
SHEET 8 — Palace gate dressing, same cream limestone and gold trim as the approved palace gate. Size 1536×1024, grid 3 columns × 2 rows.
1) Guard booth: small stone sentry box with a red conical roof (~1.5 units wide, ~2.5 tall).
2) Long stone planter with clipped hedge and white flowers (~3 units wide).
3) Tall flagpole with a long blue pennant and gold finial (~3.5 units tall).
4) Tall crenellated city wall section that can repeat horizontally (~4.5 units wide, ~3.5 tall).
5) Stone lion statue on a plinth, facing right (~1.5 units tall).
6) The same lion facing left (draw it, do not mirror-copy pixels).
No shadows, no text.
```

## Sheet 9 — Đồ phố bộ 3 (P3)

```text
SHEET 9 — Street props, set 3. Size 1536×1024, grid 3 columns × 2 rows, same scale rules as Sheet 3.
1) Town notice board with pinned blank paper notes (no writing).
2) Wooden direction signpost with three blank arrow boards.
3) Flower cart: small handcart full of potted flowers.
4) Wooden bench with stone planters at both ends.
5) Stack of apple crates with red apples.
6) Ornate street clock on a tall iron post (clock face with only tick marks, no numbers).
No shadows, no text.
```

---

## Nhận lại

- Gửi lại ảnh trong chat với Claude, ghi số sheet. Claude cắt và lưu vào `apps/game-web/art-src/hd2d/batch-12-city/<id>/` (raw giữ nguyên + final), cập nhật manifest, chạy kiểm tra, rồi đặt vào map và gửi ảnh chụp để owner duyệt.
- Nếu ChatGPT vẽ nền không phẳng, có viền hồng, hoặc nhân vật dính nhau: yêu cầu vẽ lại sheet đó, đừng chỉnh tay.
