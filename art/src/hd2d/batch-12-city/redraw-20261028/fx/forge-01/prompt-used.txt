# Plaza drifting petals FX — raw 01

Route: built-in Codex ImageGen, 2026-10-28. Raw image: `raw-01.png`, 1536×1024, SHA256 `7281ee969eb065826707f0dfd50c9fb84b78483d0e92d43f72be4fccd62b29ee`.

Prompt: Make ONE four-frame looping ambient visual effect as a 2×2 sprite sheet. Subject: a small gust of cherry-blossom petals drifting and swirling gently through the stone plaza of the royal capital. Frames read left-to-right, then next row; each frame is the same small handful of distinct pale blush, warm cream and muted red petals, subtly changing orientation and spacing to make a seamless soft drifting loop. Clean crisp pixel clusters, HD-2D Octopath-like finish, dark warm outlines only where needed, warm upper-left light, 33–48 colors, no blur or glow. Keep the effect compact and centered with safe margin in every equal square cell. Background must be a perfectly flat uniform pure bright green #00FF00, with no gradients, scenery, ground plane, shadow, text or cell lines. Do not use green in the petals. No repeated identical frames.

Attached references and SHA256:

- Content: `.ai/design/map-checklists/refs/city_square.jpg` — `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- Approved FX style: `apps/game-web/art-src/hd2d/batch-02-octopath/fountain-water/final.png` — `582193177b79beb975ae024be8f20aef907e8ef8de5a16097451bc85ed27d342`
- Approved FX style: `apps/game-web/art-src/hd2d/batch-01-octopath/leaf-flutter/final.png` — `008b281e45ce1ee8ae2e322268818617f4919da0a1fb0373028cded2b43836fd`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- Line/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: Sprite Forge `generate2dsprite.py process`, target asset, mode fx, green chroma key, 2×2, 192 px cells, strict structural QC. This is an artistic addition derived from the scene reference, not a recovered original. Approval=false pending owner review.
