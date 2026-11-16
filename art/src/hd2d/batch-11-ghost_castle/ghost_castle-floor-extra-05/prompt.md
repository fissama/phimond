# Ghost Castle — octagonal marble mosaic floor

Route: built-in Codex image_gen, 2026-11-04. Output: 1254×1254 RGB. Exact prompt used:

> Create ONE square seamless top-down texture tile for the Ghost Castle HD-2D pixel RPG, viewed straight down with no perspective. A distinctive broken octagonal mosaic floor of dark blue-black marble slabs, each broad octagonal plate separated by thin desaturated teal-green grout. A few chips and hairline mineral veins only; preserve large quiet dark areas. This must read as geometric octagonal mosaic, unlike diagonal slabs, ordinary square flagstones, rubble, carpet, or soil. Make every outermost 8-pixel strip a flat solid matching base so the tile can repeat on all four sides; keep all motif detail at least 8 px from the edge. Edges must wrap seamlessly left-to-right and top-to-bottom; no border or frame. Painterly Octopath-like pixel clusters, 33–48 colors, 2–4 grouped tones per material, clusters not noise, dark same-hue outlines, warm upper-left facets and cool shadows. No props, scene, characters, text, fog, bloom, glow, cast shadows, dithering, grid lines, central medallion, vignette, gradients. Use reference 1 for Ghost Castle content and palette, reference 2 for approved Octopath tile style and density, reference 3 for approved batch style, references 4–5 only for shading/outlines.

## Ordered references and SHA256

1. `.ai/design/map-checklists/refs/ghost_castle_gate.jpg` — `e1b28852ec2cc652ee9c224f73680e7448f892cb348d0201dbb1fea8eedc8caa`
2. `apps/game-web/art-src/hd2d/batch-01-octopath/grass-floor-01/final.png` — `792b3a1c25fb3be8671af1a4e119ef7af3bbd5a89dd22e42e14206317697524c`
3. `apps/game-web/art-src/hd2d/batch-01-octopath/contact-sheet.png` — `4347e8dafc3491cb1516c88379effbf92c32b2ac1b17a0776469eedb7fa94a05`
4. `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
5. `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

## Finish

`raw-01.png` is the generated source copied byte-identically. `final.png` was resized to 512×512 with nearest sampling, then snapped to a 40-color palette with `palette_tool.py`; no painted or code-generated image content. Raw SHA256: `116d00a1725f02fc7ea127ec8b40790957dd0f114e5e853d2e5deb414d49b705`. Final SHA256: `861822a38f9431509207e6af5a4333f5b2aa8b494aabcee9289d2d7ed57f1236`.
