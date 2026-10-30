# Prompt gộp v2: hoàn thiện màn đăng nhập HD-2D (copy khối bên dưới vào ChatGPT)

Đính kèm trước khi gửi:
- `hall-city-backdrop.png` (kinh thành hiện tại, tông màu và kiểu vẽ cần giữ)
- `stage-floor.png`, `stage-dais-large.png` (sân khấu đã duyệt, để khớp tông)
- `stage-species_0052.png`, `stage-species_0107.png`, `stage-species_0088.png`, `stage-species_0150.png`, `stage-species_0153.png`, `stage-species_0155.png` (6 thú mới, bản đứng)
- `showcase-unicorn.png`, `showcase-scorpion.png`, `showcase-flower.png` (3 thú cũ)
- `chat-tab-selected.png`, `chat-tab-normal.png`, `slot-rare.png`, `slot-common.png`, `slot-legendary.png`, `dialogue-panel.png`

```
You are producing game art for an HD-2D game in the style of Octopath Traveler (a login screen with a dusk city, a stone terrace and guardian beasts). Work through the jobs IN ORDER. One PNG per reply, wait for me to say "next". Every PNG exactly the size stated.

GLOBAL RULES: crisp pixel art with painterly shading, no anti-aliasing, no blur, no film grain, no dither noise, no watermark, no text. Light from the TOP-LEFT (low warm sun). Max 48 colours per image. Binary alpha. Background is one flat magenta #FF00FF (hard edge, no pink fringe, no magenta pixels left inside enclosed gaps, none inside the art) unless the job says opaque. Warm dusk palette: sandstone, cream, terracotta, muted gold, dusty teal shadows; nothing more saturated than the attached hall-city-backdrop.png except the creatures.

JOB 1 - login-sky.png, 1024x512, OPAQUE, tileable horizontally (left and right 16 px columns continue seamlessly). A calm sunset sky: deep blue-violet at the top, through dusty rose, to warm apricot and pale gold at the bottom edge (the bottom 96 px must be a smooth flat-ish pale gold band so a city can sit on top of it). A few tiny stars in the top third. No clouds, no sun disc (the sun glow is added in code). Use clean dithering-free colour steps (about 10 bands).

JOB 2 - login-clouds.png, 1024x256, magenta background, tileable horizontally. A single band of 5-7 stylised pixel-art cloud clusters with warm-lit undersides (apricot) and cream tops, in different sizes, separated by magenta gaps. Left and right 24 px columns must be empty so it tiles. No outline darker than dusty violet.

JOB 3 - login-city-far.png, 2432x420, magenta background (sky is NOT drawn), tileable horizontally. The same city as hall-city-backdrop.png (terracotta roofs, sandstone towers, a grand palace in the centre) but: hazier and slightly desaturated (aerial perspective), roofs/towers only above a flat sandstone city wall at the bottom, and a SOFT lighter haze already painted into the lowest 60 px. Left and right 32 px columns identical so it tiles. Faint mountains are drawn behind the roofs (greyed lavender).

JOB 4 - login-city-near.png, 2432x300, magenta background, tileable horizontally. A closer, darker, lower layer of rooftops and chimneys (terracotta and teal-green roofs, a few chimneys with thin smoke curls) in front of the far city. Warm rim light on the left faces. Left and right 32 px columns identical.

JOB 5 - login-frame.png, 512x640, magenta background, 9-slice friendly. An ornate login window frame: double gold border (dark outer, bright inner), carved corner ornaments about 56 px, plain tileable edges between corners, a small crest/diamond at the centre of the top edge. The INTERIOR is flat magenta (it becomes transparent; the game fills it with frosted glass). Match the colours of dialogue-panel.png. Outer silhouette is a slightly rounded rectangle.

JOB 6 - beast idle strips. For EACH of the nine beasts attached, draw a 4-frame idle loop in one horizontal strip of four equal cells (strip = 4 x cell width), the SAME creature, outline weight, palette and facing as the attached image, feet staying on the same line in every cell, nothing cropped, 4 px margin. Cell sizes: the six stage-species creatures 256x256 (strip 1024x256); the three showcase creatures 192x192 (strip 768x192). The motion must be clearly visible at game size: frame 1 neutral, frame 2 inhale (body or chest up 3 px, wings/ears/mane lifted 4-6 px), frame 3 peak (wings/mane/tail 6-8 px from neutral), frame 4 returns halfway; tails, manes, flames, feathers and antler glow lag behind the body by one frame. Do one creature per reply in this order: unicorn, scorpion, flower fairy, species_0052 dragon, species_0107 golden roc, species_0088 flame wolf, species_0150 bird of paradise, species_0153 moon deer, species_0155 nebula dragon. File names: idle-<name>.png.

JOB 7 - chat-tab-selected.png, 160x44, magenta background. Same dark navy-teal tab as chat-tab-normal.png but the SELECTED state: bright gold outline 2 px (clearly brighter than the normal tab), a thin light-gold highlight line along the inside of the top edge, and the bottom edge OPEN (no border, the navy fill runs off the bottom) so it joins the chat frame.

JOB 8 - item slot frames, 96x96 each, magenta interior and background, same geometry and corner shapes as slot-common.png: (a) slot-uncommon.png green-silver border (emerald accents), (b) slot-epic.png violet border with purple gems at the corners. Only border colour and corner gem colour differ. Also redraw slot-rare.png at 96x96 in the same family (blue border, sapphire corner gems), matching the attached slot-rare.png colours.

Start with JOB 1.
```

Ghi chú (không dán):
- Job 1–4 là bộ nền mới thay `hall-city-backdrop` (trời xanh bão hoà hiện lệch tông): khi có đủ mình ghép lại thành cảnh ba lớp thị sai, mây trôi và ánh nắng.
- Job 6 là thứ đem lại chuyển động thật cho thú; nếu quá tốn lượt, ưu tiên 6 thú mới trước.
- Job 5 cho phép hộp đăng nhập kiểu kính mờ (Octopath) thay khối navy phẳng.
