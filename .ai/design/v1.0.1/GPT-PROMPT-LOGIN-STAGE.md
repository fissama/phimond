# Prompt gộp: sân khấu màn đăng nhập + thêm linh thú 5 sao

Hiện chỉ có 3 linh thú 5★ có ảnh (Kim Kỳ Lân, Linh Tiên Hoa Hương, Độc Hạt Vương). Code đã dàn theo danh sách `BEASTS` (thêm thú = thêm một dòng + ảnh), nên khi có ảnh mới mình chỉ lắp vào, bố cục tự dàn.

Bố cục mục tiêu (rộng 1600, nhìn ngang): hàng sau 3 thú nhỏ đứng trên bệ cao, hàng trước 4 thú lớn đứng trên thềm; chừa trống chính giữa (hộp đăng nhập che) nên thú dồn về hai bên: trái 2 trước + 1 sau, phải 2 trước + 1 sau.

Đính kèm: `showcase-unicorn.png`, `showcase-scorpion.png`, `showcase-flower.png` (cỡ và phong cách thú), `hall-city-backdrop.png` (tông màu thành phố), `hall-column.png`.

```
Game art for an HD-2D game in the style of Octopath Traveler, used on the login screen behind a city skyline at dusk. Work through the jobs IN ORDER, one PNG per reply, and wait for me to say "next".

GLOBAL RULES: crisp pixel art with painterly shading, no anti-aliasing, no blur, no film grain, no dither noise, no watermark, no text. Light from the TOP-LEFT. Max 48 colours per image. Binary alpha. Background is one flat magenta #FF00FF (hard edge, no pink fringe, none inside the art) unless the job says opaque. Exact sizes. Palette: warm sandstone, cream, terracotta and muted gold matching hall-city-backdrop.png; nothing more saturated than that reference except the creatures.

JOB 1 - stage-floor.png, 512x240, opaque, TILEABLE horizontally (left and right 16 px columns must continue into each other with no seam). A wide stone terrace seen from slightly above, front-on. Top 16 px: the back edge, a low carved parapet ledge with a bright top highlight (this is the line creatures stand behind). Below it: flagstone paving in perspective (stones get larger and darker toward the bottom), fine cracks, a few moss tufts, soft ambient occlusion along the parapet. Bottom 24 px: a darker front lip that fades toward black. Max 6 tones per material, large flat stone faces.

JOB 2 - stage-balustrade.png, 256x96, magenta background, TILEABLE horizontally. A short balustrade with turned stone balusters and a flat cap rail in the same sandstone, to sit along the back edge of the terrace. Light from the top-left.

JOB 3 - stage-dais-large.png, 320x120, magenta background. A low round stone dais seen from slightly above, two steps, a gold inlay ring on the top face, worn edges. The top face is an ellipse about 280x56 px so a large creature can stand on it. Light from the top-left.

JOB 4 - stage-dais-small.png, 200x90, magenta background. Same design, smaller (top face ellipse about 170x36 px), for the back row.

JOB 5 - stage-props.png, 640x200, magenta background, ONE sheet with four separate props spaced 40 px apart, bottoms aligned at y=192: (a) a bronze brazier on a tall tripod with a small calm flame (flame drawn as a separate lighter shape so it can be animated), (b) a stone lantern post, (c) a terracotta planter with trimmed shrubs and a few small flowers, (d) a short banner pole with a cream-and-gold banner. Each about 120-160 px tall.

JOB 6 - stage-light.png, 512x512, magenta background replaced by TRANSPARENCY is impossible, so draw it on pure black #000000 instead: a soft warm sunset light shaft coming from the top-left, additive-glow style, smooth gradient allowed here (this is the only image where smooth gradients are allowed).

JOB 7..12 - six new five-star creatures, one per job, matching the size, outline weight and rendering style of the attached showcase-*.png (about 200-230 px wide, three-quarter view facing slightly right, a clean silhouette, no ground shadow, no base, full body inside the canvas with 4 px margin, canvas 256x256, feet or lowest point at y=248 and centred):
 7: Thai Co Thanh Long (an ancient holy dragon, ivory and teal scales, long body coiled upright, gold horns)
 8: Kim Si Dai Bang (a giant golden roc with wings half-raised, crimson crest)
 9: Xich Viem Lang (a crimson flame wolf, mane of fire, mid-stride pose)
 10: Thien Duong Dieu (a bird-of-paradise, long trailing tail feathers in rose and turquoise)
 11: Nguyet Dai Loc (a moon-deer, pale blue fur, antlers carrying a glowing crescent)
 12: Tinh Van Long (a nebula dragon, deep violet body with star-speckled wings)
For each creature ALSO provide a second image of the same creature, same canvas, in a slightly different breathing pose (chest/wings/mane shifted by 2-4 px) so I can alternate the two for a light idle animation; keep every other pixel identical.

Start with JOB 1.
```

Ghi chú:
- Chốt thú nào lên màn đăng nhập tuỳ anh; mình đề xuất 4–6 con để không lộn xộn (hàng trước 3–4, hàng sau 2–3).
- Job 6 ánh sáng vẽ nền đen để mình tự trộn kiểu cộng sáng (không cần alpha).
- Các thú mới nên được đưa vào `data/pets` cho đúng loài; trước mắt chỉ dùng làm hình trang trí đăng nhập.
