# Prompt gộp: nhóm asset còn lại (chân dung NPC, thú khởi đầu, foe-ring, FX, khung N04/N08)

Đính kèm trước khi gửi:
- Chân dung: ảnh đứng của từng NPC (`npc-<id>.png`, mỗi NPC một ảnh, gửi kèm khi tới job của NPC đó), `frame-portrait.png`
- Thú khởi đầu: `showcase-flower.png`, `showcase-unicorn.png`, `showcase-scorpion.png`
- FX và khung: `fx-footstep-dust.png` (kiểu FX), `slot-selected.png`, `slot-locked.png`, `dialogue-frame.png`, `ui-bottombar.png`, `panel-large.png`

```
You are producing game art for an HD-2D game in the style of Octopath Traveler. Work through the jobs IN ORDER, one PNG per reply, and wait for me to say "next". Every PNG must be exactly the size stated.

GLOBAL RULES: crisp pixel art with painterly shading, no anti-aliasing, no blur, no film grain, no dither noise, no watermark, no text. Light from the TOP-LEFT. Max 48 colours per image. Binary alpha. Background is one flat magenta #FF00FF (hard edge, no pink fringe, no magenta pixels left inside enclosed gaps) unless the job says BLACK background. 1 px dark outline on characters. Warm dusk palette, nothing more saturated than the attached references.

JOB 1..19 - NPC bust portraits, 256x256, magenta background, one per reply: waist-up, facing slightly right (three-quarter view), looking at the viewer, head about 110 px tall, shoulders cropped by the canvas bottom edge, 8 px margin on top and sides, the same face, hair, outfit colours and props as the attached full-body sprite of that NPC, expressive and friendly, warm rim light from the top-left. Order (priority first): 1 summoner_mira (Trieu Linh Su Mira), 2 forest_guide (Kiem Lam Lio), 3 bia_skill (Tho San Rowan), 4 sau_free (Cu Reu Tamo), 5 sau_guard (Nguoi Gac Rung Mero), 6 gate_captain (Thi Ve Truong Karn), 7 sq_board (Quan Su Nhiem Vu Tessa), 8 sq_healer (Y Su Selka), then 9 bia_shop (Tieu Thuong Wen), 10 bia_free (Nguoi Hai Nam Tuli), 11 gate_guild (Su Gia Bang Hoi Ryo), 12 trainer_elin (Huan Luyen Vien Elin), 13 sq_skill (Su Phu Ky Nang Doran), 14 sq_free (Nguoi Ke Chuyen Hanae), 15 sq_pillar (Tru Su Orsa), 16 sq_arena (Dai Su Rena), 17 sq_exchange (Chu San Giao Dich Ketra), 18 sq_warehouse (Thu Kho Odan), 19 sq_mailbox (a living stone mailbox spirit, a carved face on the stone post, an envelope slot as the mouth). File names: portrait-<id>.png.

JOB 20..22 - starter creature cards, 384x384, magenta background, one per reply: the SAME creature as the attached showcase image, redrawn larger with finer detail and a dynamic pose (not a copy of the attached pose), full body inside the canvas with 8 px margin, feet or lowest point at y=372, centred. 20: Tien Chuong = the flower fairy (showcase-flower.png). 21: Sa Hat = the golden one-horned beast (showcase-unicorn.png). 22: Xich Ung = the scorpion king (showcase-scorpion.png). File names: starter-<name>.png.

JOB 23 - foe-ring.png, 768x192 (four 192x192 frames), magenta background. A warning rune circle seen from above at ground level (a flattened ellipse about 176 x 88 px, centred in each cell), red-orange with a dark outline, two concentric rings with small rune glyphs between them; the 4 frames show the glyphs rotating by a quarter step each and the inner glow pulsing (frame 1 dim, 2 brighter, 3 brightest, 4 dim). Nothing outside the ellipse.

JOB 24..29 - elemental skill effects, one strip per element, 6 frames of 192x192 in one row (1152x192), on a pure BLACK #000000 background (NOT magenta; these are blended additively), bright glowing pixel art: an effect that bursts at the centre of the cell and fades by frame 6. 24 fire (flame burst, embers), 25 water (splash ring and droplets), 26 earth (rock shards and dust ring), 27 wind (spiral gust arcs, leaf bits), 28 light (starburst and white-gold rays), 29 dark (violet swirl and shadow wisps). File names: fx-<element>.png.

JOB 30 - fx-summon.png, 1152x384 (six 192x384 frames), on BLACK, additive style: a column of golden light rising from a rune circle (frame 1 circle ignites, frames 2-4 the column rises and widens with sparkles, frames 5-6 it fades into drifting motes).

JOB 31 - slot states, 96x96 each, magenta interior and background, same geometry and corner shapes as the attached slot-selected.png: slot-empty.png (dim thin frame, interior magenta), slot-selected.png (bright gold border, bright corner pieces), slot-locked.png (darkened frame with a small gold padlock at the centre). Also slot-equipped-corner.png, 32x32: a small round gold badge with a check mark, to sit in the top-right corner of a slot.

JOB 32 - dialogue-nameplate.png, 288x56, magenta background: a name plate tab that sits on the top-left edge of the dialogue box, thin double gold border (outer dark gold, inner bright gold), dark navy-teal interior, both ends cut with a slight diagonal. Interior flat dark navy-teal (not magenta).

JOB 33 - dialogue-choice.png, 288x112 (two 288x56 states stacked): top = normal choice button (dark navy-teal, thin gold border), bottom = selected (brighter gold border, lighter interior, a small gold arrow at the left).

Start with JOB 1.
```

Ghi chú (không dán):
- Job 1–8 là chân dung ưu tiên (NPC gặp sớm nhất); 9–19 làm sau nếu hết lượt.
- Tên thú khởi đầu trong dữ liệu và ảnh trưng bày hiện không khớp hoàn toàn (Sa Hạt hiển thị kỳ lân vàng, Xích Ưng hiển thị bò cạp); prompt dùng đúng ảnh đang hiện trên bệ để thẻ chọn khớp với thứ người chơi nhìn thấy.
- FX nguyên tố và `fx-summon` vẽ trên nền đen để mình trộn cộng sáng, không cần alpha.
