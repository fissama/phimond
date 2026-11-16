# Triệu Linh Điện — modular foreground threshold edge

Create one full-width transparent-key foreground edge layer for the lower edge of the 19-tile Summoning Hall. A low pale-marble threshold with one broad step and narrow warm-gold inlay. Keep all art low along the bottom edge so it does not cover actors or the playfield. At the exact center make a completely empty 3-tile-wide opening for the existing exit; terminate each side of the step with a clean squared carved stone end block. Extend the rest of the low border to both outer map edges. No tall railing, extra wall, columns, characters, creatures, text or shadow. Pixel-art HD-2D with warm cream limestone and restrained gold, 2–4 tones per material, 33–48 colors after finish, hue-matched dark outlines, clustered edges, no gradients, bloom, dithering or fog. Flat pure #FF00FF outside the edge. Source is a 3:1 sheet; crop to the visible border and conform to a single 2432×280 full-map strip. This is a fixed composition, not a repeat tile.

Route: built-in Codex ImageGen (`host_image`) plus a localized edit that opened the center exit gap. The resulting full-width layer was cropped, keyed and conformed with `extract_terrain_tiles.py`, then quantized with the shared stone palette. Fixed full-width candidate; not a repeating tile.

Generation passes: `raw-01.png` SHA-256 `a4dda6c3f949c284f0e4e1a0e452db4c07b677d387692fa00f1a4b91777d97dd`; `raw-02.png` SHA-256 `43e452157164707dbc66ac13e05eee42c5028ddb9ac19ecea9fbd9023dc88c80`; final gap edit `raw-03.png` SHA-256 `f6454b9079c9b3517ea70c30b2c40ed988242a6ab153415540e01f3250e7777a`.

References, attached in this order (repository-relative; SHA-256 recorded):
- Content/composition: `.ai/design/map-checklists/refs/summoning_hall_main_hall.jpg` — `06a047e1dc00a1e8465ede65197abf5f66358311929e47ef1d76e1afe5165aff`
- Approved hall wall stone material/style: `apps/game-web/art-src/hd2d/batch-02-octopath/hall-wall-stone/final.png` — `f8f8f83e54e71f536417d1523febe6768b9ae45c1e5b643bb02bddcf8ed9b15b`
- Approved stone-step form anchor: `apps/game-web/art-src/hd2d/batch-02-octopath/stone-steps/final.png` — `59f7f8fbd3040bced9e5c5264543db4af3c09d94511a043bc13c673029116c67`
- DocDangNu outline/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- DaoThienDuong outline/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
