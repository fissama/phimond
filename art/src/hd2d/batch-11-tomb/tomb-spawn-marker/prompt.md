# Tomb spawn marker — image_gen prompt

Route: built-in image_gen (`host_image`).

Generated 4-frame top-down stone arrival sigil in 2x2 layout, frames: dim -> runes ignite -> satellites orbit -> dim. Transparent background.

Refs (SHA256):
- `.ai/design/map-checklists/refs/tomb_region_deep_ruins.jpg` — `8b8e6bb377e5af52213504db25fdb4d4f38e64d90411716472d3a5df41ebb721`
- `apps/game-web/art-src/hd2d/batch-01-octopath/contact-sheet.png` — `4347e8dafc3491cb1516c88379effbf92c32b2ac1b17a0776469eedb7fa94a05`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
- raw `raw-01.png` — `5d831064d7424d26d5b06f2b47d34ae077a131696611adf9f47e47fe020a79e1`

Post-processing: crop via agent-sprite-forge `extract_prop_pack.py` native alpha; center-resize to 192px frames, threshold alpha to binary at 120, reduce RGB palette to 48 colors, assemble four frames left-to-right. No pixels drawn or mirrored.
