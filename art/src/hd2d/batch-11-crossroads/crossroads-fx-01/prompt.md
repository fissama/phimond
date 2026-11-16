# crossroads-fx-01

Route: built-in image_gen. Model not exposed.

Use case: pixel VFX sprite sheet for Phimond's blue night cave map. Create one exact 1536x1024 sheet with strict 4 columns x 4 rows; each cell is 384x256. Rows are FOUR different tiny looping effects, each row animates left-to-right across its four cells with a stable center pivot and matching scale. Row 1: three small bioluminescent teal water motes orbiting subtly. Row 2: a pair of pale-cyan cave bubbles that swell and pop gently, no bubble trail. Row 3: a restrained violet coral sparkle, one compact diamond glint with tiny adjacent pixels. Row 4: a short curved turquoise mineral shimmer, only a few hard-edged pixels, no long beam. Keep each effect centered within the middle 35% of its cell, with generous clear magenta around every cell and no pixels crossing grid boundaries. Reference 1 sets cave palette only. References 2 and 3 define approved pixel-VFX finish and small sprite scale. References 4 and 5 define pixel edge weight only. Pixel-art clusters with 2-4 tones per material, 33-48 total visible colors, crisp colored outlines, no pure black, no smooth gradients, no bloom, no haze, no ground shadow. Background must be perfectly flat RGB #FF00FF for chroma-key removal, absolutely no color spill or checkerboard. No text, labels, lines, or watermark.

Actual attachments (ordered):
1. .ai/design/map-checklists/refs/crossroads_unnamed_area_01.jpg — SHA256 7f6522193f17a5514164c1975e2073275cf9bc0471d2b5bf03fe50778369187a
2. apps/game-web/art-src/hd2d/batch-01-octopath/fx/extracted/f01/prop.png — SHA256 60dbfe30bd6d01c6f3003fdb5f0dbb79c3386539e79fc69c28913ddbd110cd23
3. apps/game-web/art-src/hd2d/batch-01-octopath/fx/extracted/f09/prop.png — SHA256 a5a89e0b8f04403c161463eeb79ba34c2cdc2b251cdd77b53e814daa05303642
4. apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png — SHA256 fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da
5. apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png — SHA256 043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3

Raw: raw-01.png; SHA256 6eb168cec8810e2d97ed87c0412c2aea8b44634ba96e25401638d21eb7481fc7; source box [0, 0, 1536, 1024]; sheet extraction polygon None; translation-only source registration None. Final [1536, 1024]. Non-dithered 48color finish, native1:1 pixel copy and transparent padding; NO resampling. No content drawn with code.

Native scale: {"desired_world_size_before_drawing": [12, 8], "height_relative_to_player": null, "source_footprint_px": [1263, 851], "resampling": "NONE; source pixels copied1:1, transparent padding only"}

Finish details: {"visible_colors": 48, "palette_source": null, "palette_include": null, "palette_exclude": null, "palette_remap": null, "base_palette_filter": null, "native_alpha": false, "key_threshold": 100, "key_edge_threshold": 150, "despill_radius": 2, "documented_exception": null, "job_palette_note": null}

Edit attempt 02 (`jobs/fx-01/raw-02.png`) tried to strengthen the violet in row 3. It changed all rows and introduced broad baked cyan/violet halos; rejected. The original raw-01 and packaged final remain selected.
