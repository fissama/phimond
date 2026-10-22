# Đơn 10 vòng 2 — gói gọi ChatGPT web

Mỗi thư mục = **một lần gọi**. Mở ChatGPT web (chat mới cũng được, prompt đã tự đủ luật), kéo **tất cả ảnh trong thư mục** vào, dán nội dung `prompt.txt`, gửi. Tải ảnh kết quả về, đổi tên theo tên thư mục (vd `01-4R-decal.png`) rồi gửi lại cho Claude.

Thứ tự đề nghị: 01 → 02–07 → 08–12.

Nếu GPT vẽ sai (đổi thiết kế, khung lệch chân, nền không phẳng): bảo nó *"Redraw. Keep the exact design of REF, same baseline in every cell."* trong cùng chat.

## 01-4R-decal — 4R — Decal mặt đất (vẽ lại)

Ảnh đính kèm: `REF-1-nen-da-trong-game.png`, `REF-2-ban-cu-SAI.png`. Đính kèm 2 ảnh: nền đá trong game và bản cũ (để GPT biết cái sai cần tránh).

```text
SHEET 4R — Ground overlay decals for a pixel-art town square. 
Attached REF-1 shows the cream cobblestone floor already in the game. Attached REF-2 is a previous attempt that is WRONG: it painted whole patches of stones, so each decal looked like a raised stone mound that does not match the floor. 
This time draw ONLY the added detail that lies on top of the existing floor — DO NOT draw any paving stones, cobbles, grout, dirt ground or background texture around or under it. Seen straight from above, completely flat, no height, no perspective.
Canvas 1536×1024, grid 3 columns × 2 rows (cells 512×512), one decal centred in each cell, each decal fits within ~320×320 px, at least 48 px of magenta around every decal.
1) Crack lines: thin dark-brown branching cracks plus 4–5 tiny loose stone chips.
2) Square dark-iron drain grate with a thin dark rim (~110×110 px), nothing around it.
3) Rain puddle: one flat irregular blob of muted blue-grey water with two small light-blue highlight streaks; no stones, no rim.
4) Fallen petals and leaves scattered loosely: WHITE and pale YELLOW petals and small green leaves only — absolutely no pink, rose, purple or magenta colours.
5) Chalk drawing: thin pale-white and pale-blue chalk lines forming a hopscotch of squares and one circle; nothing written inside.
6) Two long parallel wagon-wheel ruts: darker sand-brown worn stripes with a few small pebbles, running diagonally.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 02-A1-dan-pho-boy — A1 — Dân phố: boy

Ảnh đính kèm: `REF.png`. Đính kèm 1 ảnh REF.png.

```text
ANIM A1 — sprite animation sheet for the attached townsperson (REF: boy ~10 years old with a wooden toy sword).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — IDLE loop, 4 frames, same 3/4 view facing down-left as REF: standing in place, gentle breathing (shoulders and chest rise 2–3 px on frames 2 and 3), one eye blink on frame 3, the held item sways very slightly.
Row 2 — WALK loop, 4 frames, the SAME person turned to face RIGHT (side 3/4 view): frame 1 contact with left foot forward, frame 2 passing (feet together, body 3 px higher), frame 3 contact with right foot forward, frame 4 passing. Arms swing opposite to the legs. Walking style: light bouncy steps; the toy sword stays in his right hand.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 03-A2-dan-pho-girl — A2 — Dân phố: girl

Ảnh đính kèm: `REF.png`. Đính kèm 1 ảnh REF.png.

```text
ANIM A2 — sprite animation sheet for the attached townsperson (REF: little girl holding a red apple with both hands).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — IDLE loop, 4 frames, same 3/4 view facing down-left as REF: standing in place, gentle breathing (shoulders and chest rise 2–3 px on frames 2 and 3), one eye blink on frame 3, the held item sways very slightly.
Row 2 — WALK loop, 4 frames, the SAME person turned to face RIGHT (side 3/4 view): frame 1 contact with left foot forward, frame 2 passing (feet together, body 3 px higher), frame 3 contact with right foot forward, frame 4 passing. Arms swing opposite to the legs. Walking style: small quick steps; she keeps holding the apple with both hands, braids bounce 2 px.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 04-A3-dan-pho-elder — A3 — Dân phố: elder

Ảnh đính kèm: `REF.png`. Đính kèm 1 ảnh REF.png.

```text
ANIM A3 — sprite animation sheet for the attached townsperson (REF: old man with a cane).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — IDLE loop, 4 frames, same 3/4 view facing down-left as REF: standing in place, gentle breathing (shoulders and chest rise 2–3 px on frames 2 and 3), one eye blink on frame 3, the held item sways very slightly.
Row 2 — WALK loop, 4 frames, the SAME person turned to face RIGHT (side 3/4 view): frame 1 contact with left foot forward, frame 2 passing (feet together, body 3 px higher), frame 3 contact with right foot forward, frame 4 passing. Arms swing opposite to the legs. Walking style: walks slowly with a slight stoop; the cane moves forward together with the right foot.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 05-A4-dan-pho-baker — A4 — Dân phố: baker

Ảnh đính kèm: `REF.png`. Đính kèm 1 ảnh REF.png.

```text
ANIM A4 — sprite animation sheet for the attached townsperson (REF: village woman carrying a basket of bread and vegetables).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — IDLE loop, 4 frames, same 3/4 view facing down-left as REF: standing in place, gentle breathing (shoulders and chest rise 2–3 px on frames 2 and 3), one eye blink on frame 3, the held item sways very slightly.
Row 2 — WALK loop, 4 frames, the SAME person turned to face RIGHT (side 3/4 view): frame 1 contact with left foot forward, frame 2 passing (feet together, body 3 px higher), frame 3 contact with right foot forward, frame 4 passing. Arms swing opposite to the legs. Walking style: the basket stays on her arm; the skirt hem sways with each step.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 06-A5-dan-pho-guard — A5 — Dân phố: guard

Ảnh đính kèm: `REF.png`. Đính kèm 1 ảnh REF.png.

```text
ANIM A5 — sprite animation sheet for the attached townsperson (REF: city guard with a spear).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — IDLE loop, 4 frames, same 3/4 view facing down-left as REF: standing in place, gentle breathing (shoulders and chest rise 2–3 px on frames 2 and 3), one eye blink on frame 3, the held item sways very slightly.
Row 2 — WALK loop, 4 frames, the SAME person turned to face RIGHT (side 3/4 view): frame 1 contact with left foot forward, frame 2 passing (feet together, body 3 px higher), frame 3 contact with right foot forward, frame 4 passing. Arms swing opposite to the legs. Walking style: firm steps; the spear stays upright in his hand, no arm swing on the spear arm, the cape sways slightly.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 07-A6-dan-pho-traveller — A6 — Dân phố: traveller

Ảnh đính kèm: `REF.png`. Đính kèm 1 ảnh REF.png.

```text
ANIM A6 — sprite animation sheet for the attached townsperson (REF: travelling merchant with a big backpack and walking staff).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — IDLE loop, 4 frames, same 3/4 view facing down-left as REF: standing in place, gentle breathing (shoulders and chest rise 2–3 px on frames 2 and 3), one eye blink on frame 3, the held item sways very slightly.
Row 2 — WALK loop, 4 frames, the SAME person turned to face RIGHT (side 3/4 view): frame 1 contact with left foot forward, frame 2 passing (feet together, body 3 px higher), frame 3 contact with right foot forward, frame 4 passing. Arms swing opposite to the legs. Walking style: heavy steady steps; the backpack bobs 2 px, the staff moves with the right foot.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 08-A7-bo-cau — A7 — Bồ câu

Ảnh đính kèm: `REF-1.png`, `REF-2.png`. Đính kèm REF-1 và REF-2.

```text
ANIM A7 — grey town pigeon (REF-1 pecking group, REF-2 flying pigeon; use the same bird design).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — ONE pigeon PECKING loop, 4 frames, side view facing left: head up, head lowered, beak touching the ground, head up again; body and feet do not move.
Row 2 — the same pigeon FLYING loop, side view facing left, 4 frames: wings fully up, wings level, wings fully down, wings level. The body stays at the same height in every cell (no ground baseline needed).
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 09-A8-meo-cho — A8 — Mèo và chó

Ảnh đính kèm: `REF-1-meo.png`, `REF-2-cho.png`. Đính kèm 2 ảnh mèo và chó.

```text
ANIM A8 — the orange tabby cat (REF-1) and the brown dog (REF-2).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — the cat sitting exactly as REF-1, 4 frames: tail tip flicks left, centre, right, centre; one ear twitches on frame 2; one blink on frame 3.
Row 2 — the dog lying down exactly as REF-2, 4 frames: slow breathing (belly rises 2 px on frames 2 and 3), tail wags on frames 2 and 4, one ear lifts on frame 3.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 10-A9-buom-qua — A9 — Bướm và quạ

Ảnh đính kèm: `REF-1-buom.png`, `REF-2-qua.png`. Đính kèm 2 ảnh bướm và quạ.

```text
ANIM A9 — the white-and-yellow butterfly (REF-1) and the black crow (REF-2).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — ONE butterfly seen from above-front, 4 frames: wings fully open, half closed, closed (seen edge-on), half closed. The body stays at the same point in every cell (no ground baseline).
Row 2 — the crow standing exactly as REF-2, 4 frames: still, head turns to look left, small hop with feet 4 px above the baseline, landing with wings slightly open.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 11-P1-co-bay — P1 — Dây cờ và cờ cột

Ảnh đính kèm: `REF-1-day-co.png`, `REF-2-cot-co.png`. Đính kèm 2 ảnh dây cờ và cột cờ.

```text
ANIM P1 — cloth moving in a gentle breeze: the bunting string (REF-1) and the flagpole with blue pennant (REF-2).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — the bunting, 4 frames: the triangular flags flutter and the rope sags slightly differently each frame; the two wooden posts never move. (It may be scaled down to fit the cell; keep the same scale in all 4 cells.)
Row 2 — the flagpole, 4 frames: the long blue pennant waves, a ripple travelling from the pole to the tip; the pole, base and gold finial never move.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```

## 12-P2-dai-phun-bien-treo — P2 — Bồn nước và biển treo

Ảnh đính kèm: `REF-1-bon-nuoc.png`, `REF-2-bien-treo.png`. Đính kèm 2 ảnh bồn nước và biển treo.

```text
ANIM P2 — the lion wall fountain (REF-1) and the hanging shop sign (REF-2).
ANIMATION RULES
- The attached image "REF" is the finished sprite. Redraw EXACTLY that same design in every frame: same face, costume, colours, outline thickness, pixel size and proportions. Do not redesign, restyle, recolour or resize it.
- Canvas 1536×1024, grid 4 columns × 2 rows, each cell 384×512 px. Each row is one looping animation of 4 frames read left to right; frame 4 must loop smoothly back to frame 1.
- The subject is the same size in every cell, centred horizontally, feet/base on the same baseline (about 40 px above the bottom of the cell) in every cell. Only the parts I name move.
- Motion is small and natural (2–8 px), not exaggerated.

Row 1 — the fountain, 4 frames: ONLY the water changes — the stream from the lion's mouth and the ripples and sparkles in the basin shift each frame; all stone stays pixel-identical.
Row 2 — the hanging sign, 4 frames: the sign board swings gently on its chains (tilt −4°, 0°, +4°, 0°); the post and iron bracket never move.
STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky readable pixel clusters, 2–4 tone shading, dark same-hue outlines (never pure black, no white or pink halo). Warm light from upper-left. NO cast shadow on the ground, NO text, letters, numbers, logos or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no texture, no grid lines, no labels, no frame. Hard pixel edges, no pink fringe.
Reply only with the image.
```
