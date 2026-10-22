# Đơn 10 vòng 3 — gói gọi ChatGPT web (dáng tư thế, vẽ bằng image gen)

**Vì sao có vòng 3:** ở vòng 2, ChatGPT dùng Python ghép ảnh (dịch/lật ảnh tham chiếu) và trả về zip, nên không có khung động thật. Vòng 3 chỉ xin **3–4 tư thế đứng cạnh nhau** (dễ cho GPT hơn lưới 8 khung), engine tự ghép thành chuyển động.

**Cách dùng:** mỗi thư mục = một lần gọi, **mỗi lần một chat mới**. Kéo ảnh trong thư mục vào, dán `prompt.txt`. Kết quả phải là **ảnh hiện ngay trong chat** (do image gen vẽ). Nếu GPT bắt đầu viết code hoặc đưa file zip: bấm dừng và nhắn *"Do not use code. Use image generation to paint it."* Tải ảnh về, đặt tên theo thư mục, gửi lại cho Claude.

Phần engine tự làm (không cần vẽ): thở/nhún khi đứng, bướm vỗ cánh (bóp ngang), chó thở, quạ, dây cờ lay, biển treo đung đưa (xoay quanh móc), đèn nhấp nháy.

Thứ tự: 01 → 02–07 → 08–11.

## 01-4R-decal — 4R — Decal mặt đất

Ảnh đính kèm: `REF-1-nen-da-trong-game.png`, `REF-2-ban-cu-SAI.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

SHEET 4R — Ground overlay decals for a pixel-art town square. REF-1 is the cream cobblestone floor already in the game. REF-2 is a WRONG earlier attempt: it painted whole patches of stones that look like raised mounds.
Draw ONLY the added detail that will lie on top of the existing floor — no paving stones, cobbles, grout or ground texture around or under it. Seen straight from above, completely flat.
Canvas 1536×1024, grid 3 columns × 2 rows, one decal centred in each cell, each within ~320×320 px, painted pixel art with shading (not thin vector lines).
1) Cracks: dark-brown branching cracks with tiny chipped edges and 4–5 small loose stone chips.
2) Square dark-iron drain grate (~110×110 px) with bevelled rim, highlights and dark gaps between bars.
3) Rain puddle: irregular blob of blue-grey water, darker rim pixels, a reflected sky highlight and two light streaks; no stones.
4) Fallen petals and small leaves: white and pale-yellow petals, green leaves only — no pink, purple or magenta.
5) Chalk hopscotch: slightly smudged pale-white chalk squares and one circle; nothing written inside.
6) Two parallel wagon-wheel ruts: worn darker sand-brown stripes with small pebbles, running diagonally.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 02-A1-di-bo-boy — A1 — Dáng đi: boy

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A1 — WALKING POSES for the townsperson in REF. The character is now turned to face RIGHT, seen from the side in 3/4 view (we see the right side of the body, walking toward the right edge of the image).
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Standing still, facing right, arms relaxed.
2) Mid-stride: LEFT leg forward, right leg back, right arm forward, left arm back.
3) Mid-stride: RIGHT leg forward, left leg back, left arm forward, right arm back.
Walking style: light bouncy steps, the toy sword held low in the hand nearest the viewer.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 03-A2-di-bo-girl — A2 — Dáng đi: girl

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A2 — WALKING POSES for the townsperson in REF. The character is now turned to face RIGHT, seen from the side in 3/4 view (we see the right side of the body, walking toward the right edge of the image).
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Standing still, facing right, arms relaxed.
2) Mid-stride: LEFT leg forward, right leg back, right arm forward, left arm back.
3) Mid-stride: RIGHT leg forward, left leg back, left arm forward, right arm back.
Walking style: small steps, still holding the apple with both hands.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 04-A3-di-bo-elder — A3 — Dáng đi: elder

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A3 — WALKING POSES for the townsperson in REF. The character is now turned to face RIGHT, seen from the side in 3/4 view (we see the right side of the body, walking toward the right edge of the image).
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Standing still, facing right, arms relaxed.
2) Mid-stride: LEFT leg forward, right leg back, right arm forward, left arm back.
3) Mid-stride: RIGHT leg forward, left leg back, left arm forward, right arm back.
Walking style: slow steps with a slight stoop, the cane planted forward.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 05-A4-di-bo-baker — A4 — Dáng đi: baker

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A4 — WALKING POSES for the townsperson in REF. The character is now turned to face RIGHT, seen from the side in 3/4 view (we see the right side of the body, walking toward the right edge of the image).
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Standing still, facing right, arms relaxed.
2) Mid-stride: LEFT leg forward, right leg back, right arm forward, left arm back.
3) Mid-stride: RIGHT leg forward, left leg back, left arm forward, right arm back.
Walking style: the basket stays on her arm, skirt hem swings with the step.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 06-A5-di-bo-guard — A5 — Dáng đi: guard

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A5 — WALKING POSES for the townsperson in REF. The character is now turned to face RIGHT, seen from the side in 3/4 view (we see the right side of the body, walking toward the right edge of the image).
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Standing still, facing right, arms relaxed.
2) Mid-stride: LEFT leg forward, right leg back, right arm forward, left arm back.
3) Mid-stride: RIGHT leg forward, left leg back, left arm forward, right arm back.
Walking style: firm steps, the spear held upright.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 07-A6-di-bo-traveller — A6 — Dáng đi: traveller

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A6 — WALKING POSES for the townsperson in REF. The character is now turned to face RIGHT, seen from the side in 3/4 view (we see the right side of the body, walking toward the right edge of the image).
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Standing still, facing right, arms relaxed.
2) Mid-stride: LEFT leg forward, right leg back, right arm forward, left arm back.
3) Mid-stride: RIGHT leg forward, left leg back, left arm forward, right arm back.
Walking style: heavy steps under the big backpack, the staff planted forward.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 08-A7-bo-cau — A7 — Bồ câu

Ảnh đính kèm: `REF-1.png`, `REF-2.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A7 — POSES of ONE grey pigeon (same bird design as REF-1 and REF-2), side view facing LEFT.
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 4 poses:
1) Standing, head up.
2) Head down, beak touching the ground (pecking).
3) Flying, both wings raised high above the body.
4) Flying, both wings swept down below the body.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 09-A8-meo — A8 — Mèo vẫy đuôi

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

A8 — POSES of the orange tabby cat in REF, sitting exactly as in REF.
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses (only the tail and one ear change):
1) Tail curled to the LEFT around the paws.
2) Tail raised straight up with the tip curled, left ear turned sideways.
3) Tail curled to the RIGHT.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 10-P1-co-cot — P1 — Cờ cột phấp phới

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

P1 — POSES of the flagpole in REF. The pole, base and gold finial are identical in every pose; ONLY the blue pennant changes.
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Pennant hanging with a gentle S-curve.
2) Pennant blown to the right, a wave ripple in its middle.
3) Pennant blown further, its forked tip lifted and twisted.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```

## 11-P2-bon-nuoc — P2 — Nước bồn sư tử

Ảnh đính kèm: `REF.png`.

```text
IMPORTANT: paint this with the IMAGE GENERATION tool and show the image in the chat. Do NOT use Python, code, scripts or a zip file. Do NOT copy, shift, flip or paste the reference — every pose must be freshly painted with the body really in a different position.

P2 — POSES of the lion wall fountain in REF. All stone is identical in every pose; ONLY the water changes.
LAYOUT: canvas 1536×1024. Draw the poses side by side in ONE horizontal row, evenly spaced, left to right in the order listed, all at the SAME size as each other, feet/base all on the same horizontal baseline. At least 64 px of magenta between poses. Keep the exact same design, face, costume, colours and proportions as REF.
Draw 3 poses:
1) Water stream from the lion's mouth straight, small splash in the basin, ripples near the centre.
2) Stream slightly wavier, splash droplets higher, ripples spread wider with a sparkle on the left.
3) Stream with a bulge halfway, droplets falling, ripples near the basin rim with a sparkle on the right.

STYLE: crisp HD-2D pixel art exactly like the attached reference (Octopath Traveler look), chunky pixel clusters with 2–4 tone shading, dark same-hue outlines, warm light from upper-left. No cast shadow on the ground, no text, letters, numbers or watermark.
BACKGROUND: one flat pure magenta #FF00FF colour, no gradient, no grid lines, no labels, no frames. Hard pixel edges, no pink fringe.
```
