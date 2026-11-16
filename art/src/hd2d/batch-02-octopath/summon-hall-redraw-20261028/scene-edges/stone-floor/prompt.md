# Triệu Linh Điện — seamless stone floor

Redraw the Summoning Hall floor as a genuine seamless 512×512 overhead gameplay floor tile; the supplied hall reference provides warm pale-stone identity and the existing rejected floor is content context only, never a style anchor. Irregular large and medium limestone slabs with narrow deep warm-gray mortar, subtle carved edge bevels and a few hairline mineral veins; maintain even detail density to within 8 pixels of all four boundaries and exact matching continuation across opposite edges. Keep all four corner base colors identical. No frame, border, central medallion, rugs, props, objects, shadows, perspective, gradient, vignette, noise or dither. Octopath-like HD-2D pixel-art texture, 2–4 tones per material, 33–48 colors after finish, hue-matched dark-brown outlines only where slab joints require them, restrained warm upper-left light and cool stone shadows.

Route: built-in Codex ImageGen (`host_image`). Planned palette quantization plus four-edge seam inspection; candidate replacement for the rejected `hall-floor-stone` only.

References, attached in this order (repository-relative; SHA-256 recorded):
- Content/material: `.ai/design/map-checklists/refs/summoning_hall_main_hall.jpg` — `06a047e1dc00a1e8465ede65197abf5f66358311929e47ef1d76e1afe5165aff`
- Rejected floor for content identity only: `apps/game-web/art-src/hd2d/batch-02-octopath/hall-floor-stone/final.png` — `ef1a3edea0bc8778d42bb8c64e7bb3cf51c78e4a06971500efd36851bb5ba142`
- Approved same-kit material anchor: `apps/game-web/art-src/hd2d/batch-02-octopath/hall-floor-wood/final.png` — `cb9d0ec9c9971ce4d4b6dbdc0576fc2ec64ce4b6f4460697207a408531efff97`
- DocDangNu outline/shading anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- DaoThienDuong outline/shading anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`
