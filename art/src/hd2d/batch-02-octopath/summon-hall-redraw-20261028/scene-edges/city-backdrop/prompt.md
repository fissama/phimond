# Triệu Linh Điện — far city backdrop

Create a wide fixed far-background plate spanning the full 19-tile width of the HD-2D Summoning Hall. The hall reference shows a pale imperial city, tiled roofs and distant towers through upper colonnade openings. Keep this plate as only the distant exterior and sky; do not draw the room's columns, interior wall, floor, characters, creatures, UI or text. Arrange a distinctive central palace roof and lower city wall across the width, with varied rooflines on both sides. Cool blue sky and distant blue-gray stone, warm muted terracotta roofs and cream masonry. Octopath-like HD-2D pixel-art clusters, 2–4 tones per material, 33–48 colors after finish, hue-matched dark outlines, warm upper-left light, no fog, smooth gradients, bloom, dither or cast shadows. Full-bleed opaque scenic plate, no magenta or alpha. Target 3:1 panorama; conform to 1216×405 at 64 px/world. This is one authored full-width view and is not repeated.

Route: built-in Codex ImageGen (`host_image`) plus one localized edit (the first take's foliage foreground was replaced with city roofs/wall). Conformed with `conform_background.py`, then quantized to a shared 48-color city palette. Fixed-width candidate; not tileable.

Image provenance: first take `raw-01.png` SHA-256 `1944a4e5da6480382803dfd31e4a903079cafb15e463a03d6bed28472af12462`; edited take `raw-02.png` SHA-256 `fa1f4f042597afd0af4257b4b7a807343a45df3c7cd70f61b85d87bac53d3c6c`.

References, attached in this order (repository-relative; SHA-256 recorded):
- Content/composition: `.ai/design/map-checklists/refs/summoning_hall_main_hall.jpg` — `06a047e1dc00a1e8465ede65197abf5f66358311929e47ef1d76e1afe5165aff`
- Approved far-layer style anchor: `apps/game-web/art-src/hd2d/batch-01-octopath/forest-wall-far/final.png` — `745ebb244eb1f19c5398ac02b90a958e76ad0b719a5218d736206c2cce7bcbb2`
- Approved hall material/style anchor: `apps/game-web/art-src/hd2d/batch-02-octopath/hall-wall-stone/final.png` — `f8f8f83e54e71f536417d1523febe6768b9ae45c1e5b643bb02bddcf8ed9b15b`
- DocDangNu outline/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- DaoThienDuong outline/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
