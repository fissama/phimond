# Danh sách sprite cần vẽ lại và prompt gửi ChatGPT (hướng HD-2D / Octopath)

Cập nhật 2026-10-29. Gửi **từng ảnh một**, đính kèm trực tiếp ảnh tham chiếu (không zip). Lưu đúng tên file ở cột "Lưu thành". Trạng thái từng mục theo dõi ở `CHECKLIST-REDRAW-CODEX.md` (mục F). Mọi ảnh tham chiếu nằm trong `apps/client/public/hd2d/` trừ khi ghi khác.

## Khối chung (dán đầu mỗi prompt)

> Pixel art game asset for an HD-2D game in the style of Octopath Traveler: detailed pixel art with crisp pixels, painterly shading, warm key light from the TOP-LEFT, cool shadows, strong value contrast (clear lights and darks, not flat), 1px dark outline on objects, no anti-aliasing, no blur, no text, no watermark. 3/4 top-down view (camera looks down about 38°). Max 48 colors, palette matching the attached reference. Scale: 1 world tile = 128 px. Background for cut-outs: flat magenta #FF00FF with binary alpha (no semi-transparent pixels, no magenta fringe). Output PNG exactly the size stated.

## Ưu tiên

Ba nhóm sau là thứ làm game giống Octopath nhất. Chúng cho engine những lớp tách nhau để làm mờ chiều sâu, đổ bóng và dựng độ cao.

| Nhóm | Mục | Vì sao |
|---|---|---|
| A. Tiền cảnh (mờ mạnh khi dựng) | S01–S06 | Octopath luôn có vật to, mờ sát camera |
| B. Hậu cảnh nhiều lớp | S07–S11 | Thành phố/rừng/cung điện có lớp xa, giữa, gần |
| C. Địa hình có độ cao | S12–S19 | Bậc, bục, vách, bờ đất: để map không còn phẳng |
| D. Còn nợ từ trước | S20–S27 | Chuyển động, sàn biến thể, bóng, khung thanh |

---

## A. Tiền cảnh

### S01 `fg-forest-branch-a.png`, `fg-forest-branch-b.png` (512×320, nền ma-gen-ta)
Đính kèm: `tree-large-01-canopy.png`, `forest-cam-bank.png`
> Foreground leafy tree branch hanging down from the top of the frame, to be drawn very close to the camera and blurred in-engine. Dark green leaves in clustered layers with a few lit edges on the top-left, a thick brown branch entering from the top-right corner, some leaves overlapping with irregular silhouette, no ground. Two variants: a = branch entering from the top-left corner, b = branch entering from the top-right. 512×320.

### S02 `fg-forest-bush-a.png`, `-b.png`, `-c.png` (384×256, nền ma-gen-ta)
Đính kèm: `bush-01.png`, `fern-01.png`
> Large foreground bush and fern clump seen from slightly above, to sit at the bottom edge of the screen very close to the camera. Chunky leaves with bright rim light on the top-left and dark undersides, silhouette wider than tall, bottom edge flat and cut straight. Three different shapes: a = round bush, b = fern fan, c = bush with a few small red berries. 384×256.

### S03 `fg-city-awning-edge.png` (768×256, nền ma-gen-ta)
Đính kèm: `awning-red.png`, `city-facade-shop.png`
> Foreground market awning edge: the front scalloped fringe of a red-and-cream striped canvas awning hanging from the top of the frame, wooden pole supports at both ends, strong shadow underneath, to be drawn very close to the camera and blurred in-engine. Top edge is flat and cut straight, scalloped fringe at the bottom, wavy cloth folds. 768×256.

### S04 `fg-city-bunting.png` (1024×160, nền ma-gen-ta, lặp ngang)
Đính kèm: `city-bunting.png`
> Festival bunting string of small triangular flags in red, blue, cream and yellow hanging in a gentle curve across the frame, with a thin dark rope on top. Seen from slightly below. Must tile horizontally: the rope height and flag pattern at the right edge match the left edge. 1024×160.

### S05 `fg-city-lantern-pair.png` (256×384, nền ma-gen-ta)
Đính kèm: `city-hanging-sign.png`, `hall-lantern.png`
> Two wrought-iron hanging street lanterns on a curved bracket entering from the top-right, warm glowing yellow glass, dark iron, a bit of cobweb detail. Drawn large for foreground use. 256×384.

### S06 `fg-hall-curtain.png` (320×512, nền ma-gen-ta)
Đính kèm: `palace-curtain.png`
> A heavy dark-red velvet curtain with gold tassel and gold rod, hanging from the top-left corner and gathered at the side, deep folds with strong lights and shadows, partly cut by the frame edge. 320×512.

## B. Hậu cảnh nhiều lớp

### S07 `city-backdrop-wide.png` (2432×486, đặc)
Đính kèm: `hall-city-backdrop.png`
> Using the attached city plate as the style reference, draw a WIDER version of the same walled sunlit city skyline, 2432×486, opaque. Flat saturated blue sky with a few small pixel clouds at the top, faint blue mountains, cream towers with orange and green roofs, a large castle with a tall central spire at the center, houses getting lower toward both sides, and at the very bottom a continuous city wall with battlements whose base is a straight horizontal line along the bottom edge. No foreground objects, no people, no sky gradient. The left and right ends do not need to tile.

### S08 `city-near-roofs.png` (2432×220, nền ma-gen-ta, lặp ngang)
Đính kèm: `hall-city-backdrop.png`, `city-roofline-mid.png`
> A thin strip of nearer rooftops and chimneys of the same city: orange and green tiled roofs, cream walls, chimneys, small towers, uneven top silhouette, flat straight bottom edge. Same palette but slightly larger in scale and a little darker and warmer so it reads as closer than the skyline behind it. The last 64 px must continue into the first 64 px with no seam.

### S09 `forest-far-layers.png` (2048×512, nền ma-gen-ta, lặp ngang)
Đính kèm: `forest-far-canopy.png`, `forest-wall-far.png`
> Distant forest in three overlapping layers in one image: the farthest layer pale blue-green and hazy (low contrast), a middle layer of mid-green tree crowns, and a nearer layer of dark green crowns with a few trunks visible. Light mist between layers (use dithering, no soft alpha). Flat bottom edge, uneven top silhouette. Tiles horizontally: the last 64 px continue into the first 64 px.

### S10 `palace-courtyard-passage.png` (384×420, nền ma-gen-ta)
Đính kèm: `palace-gate.png`
> View through the arched opening of the palace gate into the inner courtyard: stone steps rising, a bright light at the end of the passage, dark walls on both sides, a banner on the far wall. Drawn to fit behind the arch of the attached gate.

### S11 `palace-wall-fill.png` (512×320, nền ma-gen-ta, lặp ngang)
Đính kèm: `palace-wall-section.png`, `palace-crenel-wall.png`
> A long stretch of the palace outer wall with battlements and a stone ledge, same stone and color as the attached wall, no gate. Tiles horizontally with no seam.

## C. Địa hình có độ cao (mỗi ô = 128 px)

### S12 `stone-wall-face.png` (512×128, nền đặc, lặp ngang)
Đính kèm: `hall-floor-marble.png`, `city-paving-02.png`
> The vertical face of a raised stone platform seen from the front: courses of sandstone blocks, a lit top lip along the top edge (top-left light), a dark shadowed base. One tile is 128 px wide and 128 px tall; the image is 4 tiles wide and tiles horizontally.

### S13 `stone-step-face.png` (384×128, nền ma-gen-ta)
> Three-tile-wide stone staircase front: four steps, each with a lit top surface and a dark vertical riser, worn sandstone blocks, with a short stone side wall at each end. 384×128.

### S14 `stone-step-side-left.png`, `stone-step-side-right.png` (128×256, nền ma-gen-ta)
> Side view of a stone staircase going up toward the back, lit from the top-left, one tile wide, 128×256. Left version rises to the left, right version rises to the right.

### S15 `dirt-cliff-face.png` (512×128, nền đặc, lặp ngang)
Đính kèm: `path-fringe-gn.png`
> Vertical earth bank under a grassy ledge, front view: layered brown soil with roots, small stones, dark base shadow, a lit grass lip along the top. 4 tiles wide, tiles horizontally.

### S16 `grass-ledge-top.png` (512×64, nền ma-gen-ta, lặp ngang)
> The top edge of a grassy ledge seen from above: dense grass fringe overhanging the edge, a few small flowers, transparent below the edge. Tiles horizontally.

### S17 `stone-plinth-round.png`, `stone-plinth-square.png` (256×192, nền ma-gen-ta)
Đính kèm: `summon-pedestal-01.png`
> A low circular (and square) stone platform step of two tiers with a lit top surface, vertical side faces showing blocks, subtle gold trim. For NPC and monument bases. 256×192.

### S18 `wood-bridge-plank.png` (512×128, nền ma-gen-ta, lặp ngang)
> A wooden bridge deck with rope handrails along both sides, seen from the front-above, planks with nail details, dark gap under the bridge. Tiles horizontally.

### S19 `fence-stone-low.png` (512×96, nền ma-gen-ta, lặp ngang)
> A low stone balustrade with round posts at each end of a tile, lit top-left, short shadow below. Tiles horizontally.

## D. Còn nợ từ trước

### S20 `stone-floor-b.png` (512×512, đặc, lặp 2 chiều)
Đính kèm: `hall-floor-marble.png`
> Second seamless sandstone floor tile, same brick size/colors/crack thickness/lighting as the reference but a completely different arrangement of bricks and cracks. Left edge continues into the right edge and top into bottom; no darker or lighter border, no gradient or vignette.

### S21 `floor-light-1/2/3.png` (256×256, nền ma-gen-ta)
Đính kèm: `hall-stained-glass.png`, `hall-floor-marble.png`
> Flat top-down patch of colored light on a stone floor through the attached stained-glass panel, elongated slanted parallelogram, binary alpha only, soft falloff built with ordered checkerboard dithering from a bright core to sparse pixels at the edge, ≤32 colors. 1 = warm white/yellow, 2 = pink/red, 3 = blue/cyan; different pane pattern each.

### S22 `shadow-*.png` (nền ma-gen-ta, alpha nhị phân, dither)
> Ground contact shadows in dark blue-violet, cast toward the bottom-right (light from top-left), built with dithering: round small 128×64, round large 256×128, rectangle 256×96, long tree canopy shadow 384×128.

### S23 Dải chạy người chơi: `player-male.run.png`, `player-female.run.png` (1536×192, 8 khung)
Đính kèm: dải idle hiện tại của nhân vật đó (`player-male.idle.png` / `player-female.idle.png`)
> Same character, outfit and proportions as the attached idle strip, 8-frame walking cycle to the right in one horizontal row, each frame 192×192, feet at (96,184) in every frame, body height ~168 px. Frames 1 and 5 are the two contact poses with OPPOSITE legs forward; frames 3 and 7 are the passing poses; arms swing opposite to the legs. No stray pixels, same body height in every frame, frame 8 flows back into frame 1.

Làm tương tự cho `run-down` (nhìn thẳng vào camera) và `run-up` (nhìn từ sau lưng): mỗi hướng một ảnh, tổng 6 dải. Lỗi đã bị loại lần trước: chân trụ nghiêng cùng một bên ở cả hai nửa chu kỳ, điểm ảnh rác, chênh chiều cao thân.

### S24 Dải chạy người đi đường: `walker-<baker|elder|boy|girl|guard|traveller>.run.png`, `.run-down.png`, `.run-up.png` (1536×192, 8 khung)
Đính kèm: ảnh đứng của người đó và `player-male.run.png` đã được duyệt
> Same rules as S23 for this NPC. Keep the props already drawn for them (baker basket, elder staff, girl apple, guard spear, traveller staff) in all 8 frames.

### S25 Khung thanh HP/MP/EXP có nhãn tách (`bar-frame-*.png`)
Đính kèm: `ui-bottombar.png`
> Empty gold-framed status bars (HP red slot, MP blue slot, EXP green slot), no text, no fill, label plates drawn separately, same gold frame language as the attached UI. Sizes: bar 256×32, label plate 64×32.

### S26 Sửa `fx-beast`, `fx-insect`, `fx-plant`, `ui-minimap` (lô codex 2026-10-23)
> Redraw fx-beast, fx-insect, fx-plant as 6 clean frames each (frames 3–5 currently contain stray fragments). Remove the leftover magenta border inside the frame of ui-minimap.

### S27 Mảnh nối mặt tiền nhà (alley, drainpipe, pillar)
Đính kèm: `city-facade-townhouse.png`, `city-alley-arch.png`
> Connector pieces that fill the gaps between city facades: a narrow alley opening with a shadowed back wall, a drainpipe running down a wall, a carved corner pillar. Each 128×384, magenta background, same material and lighting as the attached facades.

---

## Tiêu chí duyệt chung

Kích thước đúng; ≤48 màu; alpha nhị phân; không viền ma-gen-ta; ánh sáng từ trên-trái; ảnh lặp thì ghép 3×3 không thấy đường nối; dải chuyển động thì xem ảnh động, khung 1 và 5 phải đổi chân.
