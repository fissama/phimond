# Ghost Castle — black marble floor 01

Route: built-in Codex image_gen; generated 2026-11-04. Raw source: `raw-05.png`.

## Ordered references and hashes
- `apps/game-web/art-src/hd2d/batch-01-octopath/grass-floor-01/final.png` (style): `792b3a1c25fb3be8671af1a4e119ef7af3bbd5a89dd22e42e14206317697524c`
- `apps/game-web/art-src/hd2d/batch-01-octopath/contact-sheet.png` (style): `4347e8dafc3491cb1516c88379effbf92c32b2ac1b17a0776469eedb7fa94a05`
- `.ai/design/map-checklists/refs/ghost_castle_gate.jpg` (content/palette): `e1b28852ec2cc652ee9c224f73680e7448f892cb348d0201dbb1fea8eedc8caa`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` (style): `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` (style): `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

## Exact prompt

One square, top-down seamless texture tile for a dark haunted marble floor in a polished HD-2D pixel RPG. Treat the image as a wraparound texture: when tiled 3x3 there must be no rectangular grid, no visible tile boundary, no abrupt horizontal or vertical seam. Compose asymmetrical blue-black marble plates and sparse muted teal hairline veins so every contour that exits the left edge re-enters at the exact same y and color on the right edge, and every contour that exits the top re-enters at the same x and color on the bottom. Edge pixels must match corresponding opposite edge pixels. Do not put a frame, perimeter band, border, or grout strip at the image boundary. The image boundary should be invisible. Irregular marble fissures should cross boundaries and continue seamlessly. Medium-low contrast, but slab shapes readable. Crisp grouped pixel clusters, Octopath-like hand-painted pixel style, dark same-hue outlines, 2–4 tones per material, 33–48 colors, no dither/noise, no props, no cast shadow, no fog, no glow, no text. The attached approved game floor is only the style reference; the castle map is for dark blue-black and teal palette only; pet sheets only for shading-cluster style. Do not mimic their layout.

## Finish and validation

Generated raw is retained unmodified. Candidate resized/cropped to 512×512 with `extract_terrain_tiles.py`, then reduced to a shared 40-color palette with `palette_tool.py build/apply`. Re-validated with `extract_terrain_tiles.py --edge-policy seamless --max-seam-ratio 1.25`. Human 3×3 repeat preview required; machine `seamless_verified` remains false by the tool's contract.
