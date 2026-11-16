# tomb-decal-slate-chips — image_gen prompt

Use case: stylized-concept; isolated top-down ground decal for the Tomb HD-2D map.
Primary content: slate chips, broad irregular ground-plane footprint, stepped pixel silhouette, grouped 2–4 tone materials. Muted tomb blue-gray/earth/moss/ochre palette as appropriate. Transparent background, crisp edge, no glow, halo, cast shadow, fog, pink, magenta, text, rectangles or ellipse.

Route: built-in image_gen (`host_image`). References and SHA256:
- `.ai/design/map-checklists/refs/tomb_region_deep_ruins.jpg` — `8b8e6bb377e5af52213504db25fdb4d4f38e64d90411716472d3a5df41ebb721`
- `apps/game-web/art-src/hd2d/batch-01-octopath/mud-patch/final.png` — `b0759f3111b274228356d66fb95cce948d0ef805e6c53b1e6e96bccfdbe6bcdf`
- `apps/game-web/art-src/hd2d/batch-01-octopath/dirt-floor-01/final.png` — `bd4ba8187917b9023a9f9c9bd7ddc8ad43cb269724cbe02c1137f299ea03dff3`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- Raw sheet `raw-01.png` — `2378c1e6783bcaabf55080c19f577272b7cbdeec3409724130693c7889afe4da`

Finish: extracted exact 512×512 cell from transparent 3×2 sheet; alpha floor 250 to remove faint generated halo; crop to visible pixels, nearest-neighbor reduce to fit 400px, add 8px transparent padding, reduce palette to 48 colors. No drawing or mirroring.
