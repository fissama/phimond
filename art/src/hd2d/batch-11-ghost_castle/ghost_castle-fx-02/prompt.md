# Ghost Castle — FX-02 and FX-03

Route: built-in Codex image_gen; generated 2026-11-04. Source raw SHA-256: 48d12b13c6908ddf412434314f399d1709ede71d219db54ba9b41a31a8c275fe.

## Ordered references and hashes
- `.ai/design/map-checklists/refs/ghost_castle_gate.jpg` — `e1b28852ec2cc652ee9c224f73680e7448f892cb348d0201dbb1fea8eedc8caa`
- `apps/game-web/art-src/hd2d/batch-01-octopath/firefly/final.png` — `44fea9f36370f69387c35062e00bf93eb5b30d6065d48dc05a4ef340cc4730ee`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


## Prompt

Create a game-ready HD-2D pixel-painted VFX sprite sheet for the ghost castle map environment in a Pokémon-style RPG. Canvas 1024x1024, flat pure magenta #FF00FF background, exact 2 rows x 4 columns, each cell 256x512. Keep each effect centered in its own cell, clear margin from cell bounds, no element crosses cell boundaries. No text, labels, borders, shadows baked into background. Row 1: four sequential animation frames of a small floating broken black-marble rune shard with teal carved spiral and pale aqua wisps orbiting it; the stone shard stays identical size, position, silhouette, orientation and color in all four frames, only wisps move clockwise around it. Row 2: four sequential frames of ivory-gold sparkle dust and tiny broken rune motes, a sparse magical burst that gathers, brightens, disperses and returns to start. Isolated effects, crisp pixel edges, painterly HD-2D sprite finish with clustered pixels, dark colored outlines, 2–4 value steps per material, no bloom, fog, blur, gradients, or fuzzy glow. Flat magenta background only. References: ghost castle map is content/color; approved batch-01 firefly and two pet atlases are style anchors only.

## Processing

`sheet_qc.py spill` on 2x4 grid; warning `safe_frame` in cells [0,0], [0,1], [0,3] because owned art fell inside default 15% edge margin. No cross-cell components, visible overhang, sheet-edge contact, boundary band, empty cells, or specks. Visually the content remains intact with clear frame margins. `generate2dsprite.py process --target asset --mode fx --rows 2 --cols 4 --cell-size 128 --grid-rounding nearest --key magenta --key-quality soft --despill-radius 1 --strict-qc`: pass, 8 non-empty frames, no edge touch/clamping. Each row quantized independently to 40 colors with `palette_tool.py quantize-seq --loop-policy cycle --strict`; binary alpha, zero off-palette pixels. Frame QC warnings/FAILs from character anatomy detectors are not applicable to these VFX; preserve them in the study report.
