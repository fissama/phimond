# Triệu Linh Điện — rising spirit motes loop

Route: built-in Codex ImageGen, 2026-10-28. Raw `raw-01.png`: 1254×1254, SHA256 `ae8aa90aa6bc7292fd23f405e676b25434a6d675810b1ac1e4e614436dd23ab8`.

Prompt: A four-frame loop of small magical spirit motes rising above a summoning pedestal in the Phimond hall. Exactly 2×2 square-cell sprite sheet, reading order. Each frame contains the same cluster of 7–9 tiny floating light motes, in pale warm gold and cool blue-white, following a gentle upward spiral; shift their positions and sizes slightly from frame to frame, with frame 4 returning close to frame 1 for a calm seamless loop. Keep each frame's cluster compact, center stable, dots discrete and readable, no long trails. HD-2D Octopath-like pixel art, chunky hard-edged clusters, warm gold light against cool blue accents, dark same-hue outlines where needed, no airbrush, no smooth gradient, no blur, no bloom or glow halo. Pure flat #FF00FF background; no pedestal, floor, shadow, rune circle, text or scenery. Keep every mote at least 16% inside each cell edge; no magenta in the art.

References and SHA256:
- Content: `.ai/design/map-checklists/refs/summoning_hall_main_hall.jpg` — `06a047e1dc00a1e8465ede65197abf5f66358311929e47ef1d76e1afe5165aff`
- Approved FX style: `apps/game-web/art-src/hd2d/batch-02-octopath/hall-candle/final.png` — `36d63108b0c6c78fcd0b04bed4aef272bd28240c1bef26e20f035c166d07de0d`
- Approved FX style: `apps/game-web/art-src/hd2d/batch-02-octopath/fountain-water/final.png` — `582193177b79beb975ae024be8f20aef907e8ef8de5a16097451bc85ed27d342`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: Sprite Forge `generate2dsprite.py process`, target asset, mode fx, 2×2, magenta chroma key, 192 px cells, strict structural QC; then palette build/apply. Approval false until owner review.
