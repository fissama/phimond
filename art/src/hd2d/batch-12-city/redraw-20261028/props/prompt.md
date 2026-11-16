# Royal capital plaza prop sheet — raw 01

Route: built-in Codex ImageGen, 2026-10-28. Raw: `raw-01.png`, 1536×1024, SHA256 `a674f0e54ddc71ab1ff9866fe97ca7a4271074b64fb6037325472b39cf5c6475`.

Prompt: Create a 3-column × 2-row sheet of SIX separate new prop sprites for the royal capital plaza. Use the attached city-square image as content context; use the approved city statue and carved pillar only as pixel-art style references; use the two pet sprites only as outline and shading anchors. Include, in reading order: (1) a freestanding carved stone city-map kiosk with blank, unlettered inset panels; (2) a small bronze handbell on an ornate low stone plinth; (3) a brass market balance scale with empty pans; (4) an open wooden lute case with a few coins and a folded music sheet with no writing; (5) a pair of linked queue stanchions with crimson rope and gold finials; (6) a compact square stone flower planter with warm orange and cream blossoms. Make each object clearly different and useful as an environment prop; do not repeat existing city assets such as fountain, streetlamp, vendor cart, bench, tree, topiary, flowerbox or sign. Each prop shown once, no variants, no mirrored duplicates. HD-2D Octopath-like pixel art, chunky crisp clusters, warm upper-left light, dark same-hue outlines, 2–4 tones per material, 33–48 colors per object. One isolated object centered in each equal square cell with at least 8 px safe space, on perfectly flat pure #FF00FF magenta background. No cast shadows, labels, readable text, gradients, glow, scene, floor or cell borders.

Attached references and SHA256:

- Content: `.ai/design/map-checklists/refs/city_square.jpg` — `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- Approved style: `apps/game-web/art-src/hd2d/batch-02-octopath/city-statue/final.png` — `08f3e6e6e486638546ce9e7f87a173354a5660a674dbb597544d7a012cfb82a1`
- Approved style: `apps/game-web/art-src/hd2d/batch-02-octopath/city-carved-pillar/final.png` — `a86272e9062c92fde05450db8da9b1379b7f0d792b7ed56946a8baeb2f3e88c8`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: Sprite Forge `generate2dsprite.py process`, target asset, mode sheet, 2×3, magenta chroma key, 192 px cells, strict structural QC. This is interpreted new content, not recovered source art. Review the output against the prompt: the generator substituted an ornate bell standard for the requested small handbell. Approval=false pending owner review.
