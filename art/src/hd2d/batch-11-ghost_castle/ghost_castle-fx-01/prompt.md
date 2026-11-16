# Ghost Castle — candle flame FX, four-frame loop

Route: built-in Codex `image_gen`; generated 2026-11-04. Raw source `raw-01.png`, SHA-256 `6641c3b534cfaa2f906326e3206d9a27f86f3c874ce256d6b5bfb875d0397bbb`.

## Ordered references and hashes

- Content/map screenshot: `.ai/design/map-checklists/refs/ghost_castle_gate.jpg` — `e1b28852ec2cc652ee9c224f73680e7448f892cb348d0201dbb1fea8eedc8caa`
- Flame scale and palette context (content reference only): `apps/game-web/art-src/hd2d/batch-11-ghost_castle/ghost_castle-prop-06/final.png` — `45136966ea2d1659ffd22e8f325faaf97a8670ede3618b55403e4caa4b174a17`
- Approved batch-01 pixel cluster/style anchor: `apps/game-web/art-src/hd2d/batch-01-octopath/firefly/final.png` — `44fea9f36370f69387c35062e00bf93eb5b30d6065d48dc05a4ef340cc4730ee`
- Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

## Prompt

Generate one game-ready 4-frame looping animation sheet for the candle flames used on the attached Ghost Castle silver candelabrum. The candelabrum image is a CONTENT reference only for flame scale, candle location and muted palette; the batch-01 firefly and two pet atlases are STYLE anchors for crisp clustered pixels and outline/shading only.

Canvas 1536x1024, exact 2 columns × 2 rows, four equal 768×512 cells, one isolated flame in each cell. Order top-left to bottom-right: frame 1 upright narrow flame; frame 2 bends gently left; frame 3 briefly broadens with one small side lick; frame 4 bends gently right, shaped to loop back to frame 1. Keep identical baseline at the lower center of every cell, same flame height and width envelope, no drift. Flame alone: no candle, wick, holder, smoke, sparks, ring, text or other subject.

Visual: restrained haunted candle flame, pale warm ivory core with a muted desaturated teal edge/accent, dark blue-slate outline in tiny portions only. 33–48 colors, 2–4 shade steps, crisp HD-2D pixel clusters, no smooth gradients, no blur, no bloom, no external halo; glow must not be baked into the pixels. Flat exact #FF00FF background only. Keep each flame fully inside its cell with large margins, no cross-cell overlap, no magenta/pink colors on the artwork.

## Visual sheet review

All four frames are separate; baseline and center registration appear consistent; the silhouette varies through narrow, right/left lean and a brief side lick. The top-left and bottom-right silhouettes are close; frame-level QA and 4× dark/checker inspection remain pending before asset completion.
