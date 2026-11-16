# tomb-decal-bone-fragments — image_gen prompt

One isolated top-down ground decal for the Tomb HD-2D map: bone fragments, irregular stepped footprint, grouped pixel clusters, 2–4 tones per material, muted Tomb palette. Transparent background, no glow, halo, shadow, magenta, pink, text, rectangular or elliptical shape.

Route: built-in image_gen (`host_image`). References and SHA256:
- `.ai/design/map-checklists/refs/tomb_region_dead_ruins.jpg` — `63ecc574df1e80e09a7aed253b5c01a2ec0f3e351651a313036d574ca6c46861`
- `apps/game-web/art-src/hd2d/batch-01-octopath/mud-patch/final.png` — `b0759f3111b274228356d66fb95cce948d0ef805e6c53b1e6e96bccfdbe6bcdf`
- `apps/game-web/art-src/hd2d/batch-01-octopath/dirt-floor-01/final.png` — `bd4ba8187917b9023a9f9c9bd7ddc8ad43cb269724cbe02c1137f299ea03dff3`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- Raw sheet `raw-01.png` — `d32e2c8cad7835f3faa4fde3a5d0c94c240309c4ebd68f96a2dd7ddf4c46f7f9`

Finish: extracted a 512×512 cell from transparent 3×2 sheet; alpha floor 250 removed generated halo; crop, nearest-neighbor resize, 8px transparent padding and reduce to 48 colors. No drawing or mirroring.
