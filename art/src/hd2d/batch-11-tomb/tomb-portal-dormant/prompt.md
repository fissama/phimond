# tomb-portal-dormant — redraw 02

Route: built-in image_gen (`host_image`), model not exposed.

Prompt: Front-facing freestanding tomb portal, dormant state. Keep same dark blue-gray mossy carved stone frame, lintel, straight-on camera and three shallow approach steps as its paired state. Deep black inactive doorway. Centered transparent canvas, ≥8px margin, crisp chunky HD-2D pixel clusters, 33–48 colors, no blur, no external glow, no ground shadow, no text.

Actual attached references and SHA256:
- `.ai/design/map-checklists/refs/tomb_region_dead_ruins.jpg` — `63ecc574df1e80e09a7aed253b5c01a2ec0f3e351651a313036d574ca6c46861`
- `apps/game-web/art-src/hd2d/batch-01-octopath/contact-sheet.png` — `4347e8dafc3491cb1516c88379effbf92c32b2ac1b17a0776469eedb7fa94a05`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- composition reference for paired state: the other generated portal image; SHA256 `e8ab1ec6ec0bd69c3db5f3a4458136bdec818a77a33f1300bde4d65059cc5459`
- prior pilot kept as `raw-01.png`; redraw `raw-02.png` — `7fb390007b339d6a12afdcb68be814fbdb523aca9072ce6be24c0e37c56d1776`

Finish: alpha threshold 128, normalize art crop to common 208×217 canvas and apply shared intersection mask, transparent 8px border, nondithered 48-color reduction. The shared alpha silhouette prevents frame mask mismatch; no artwork was drawn or mirrored by code.
