# Triệu Linh Điện — summoning circle loop

Route: built-in Codex ImageGen, 2026-10-28. Raw `raw-01.png`: 1774×887, SHA256 `b640b2a79db10637ca197ecbbcd2b208aaa472ae8f3389e5c1832e6b40220bcd`.

Prompt: A four-frame looping magic effect sprite sheet for the floor of the Phimond summoning hall. Layout exactly 2×2 equal square cells, read left-to-right then next row. Each cell contains one matching circular ritual sigil viewed directly from above: elegant pale-gold and cool blue-gray stone-light rune ring, three concentric segmented rings, small clear glyph marks and a few discrete star motes. Across frames, the ring gently pulses: frame 1 quiet dim ring; frame 2 small outer runes brighten and several motes lift; frame 3 full but restrained illumination; frame 4 motes drift to new positions and the light eases back to frame 1. Keep the outer silhouette size and center fixed for seamless looping. Visual direction: Octopath-like HD-2D pixel art, high-detail but chunky readable clusters, crisp pixel edges, warm golden highlights balanced by cool blue-gray; no smooth gradients, no bloom, no blur. Transparent-friendly completely flat pure #FF00FF background. No floor texture, perspective, shadows, labels, words, cell lines or other objects. Keep the ring fully inside each cell with 12% margin; background key color must not appear in the effect.

References and SHA256:
- Content: `.ai/design/map-checklists/refs/summoning_hall_main_hall.jpg` — `06a047e1dc00a1e8465ede65197abf5f66358311929e47ef1d76e1afe5165aff`
- Approved style: `apps/game-web/art-src/hd2d/batch-02-octopath/summon-floor-emblem/final.png` — `260e4ae7fe783a7beae457bab12e431c72e561d9f6100d142c4362c9a05bb5e1`
- Approved FX style: `apps/game-web/art-src/hd2d/batch-02-octopath/fountain-water/final.png` — `582193177b79beb975ae024be8f20aef907e8ef8de5a16097451bc85ed27d342`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: Sprite Forge `generate2dsprite.py process`, target asset, mode fx, 2×2, magenta chroma key, 192 px cells, strict structural QC; then palette build/apply. Approval false until owner review.
