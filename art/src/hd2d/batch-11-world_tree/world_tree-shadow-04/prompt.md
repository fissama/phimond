# World Tree shadow-04 — dappled canopy cast shadow

Route: built-in Codex image_gen; model not exposed. Generated 2026-11-05.

## Prompt used

One isolated soft World Tree cast shadow for an HD-2D top-down game. Shape: broad low horizontal dappled shadow from a dense canopy, irregular dark emerald patches broken by scattered small transparent light gaps, softer faded edges, no branches or leaves drawn as objects. Keep color hue-shifted forest green, moderate value so floor texture remains readable beneath; semitransparent alpha edges with 40-color-friendly smooth clusters. Distinct from a solid oval canopy contact, diagonal root shadow, and striped branch shadow. Actual transparent background, no checkerboard, no floor, no objects or text. Compose across the center 80% of a wide landscape asset with at least 8px transparent margins. Pixel-art clustered shading in the established Octopath HD-2D style.

## Ordered refs and SHA256

1. `.ai/design/map-checklists/refs/world_tree_deep_woods.jpg` — `471eac275c1feccaab31d6d70d6d26e43c93995f4ec9036cf1af539cb4b5cee0`
2. `apps/game-web/art-src/hd2d/batch-11-world_tree/world_tree-shadow-01/final.png` — `bad3e7a76c63f39e2d1ec2311989aae3a73d14d0973870850bf97944767dd88d`
3. `apps/game-web/art-src/hd2d/batch-11-world_tree/world_tree-shadow-02/final.png` — `f35aec192a29c252d7ff3213c3a13eaba682f6119fdeb483b643a64481c887c7`
4. `apps/game-web/art-src/hd2d/batch-11-world_tree/world_tree-shadow-03/final.png` — `26267aab71bf1151e53e1224f00c0b8ff490e147c1f81c163c39abc4c145f25a`
5. `apps/game-web/art-src/hd2d/batch-01-octopath/grass-floor-01/final.png` — `792b3a1c25fb3be8671af1a4e119ef7af3bbd5a89dd22e42e14206317697524c`

Raw SHA256 `a590226c118ed71dbf2f7b5eb031ee366fd67a2c03e310289e4b3de667996611`; final SHA256 `3b5c86f8b54f7f458c6c6ab0f29520bcc74b6883484456ec4cbf279e86ae3670`. Finish: retain soft alpha, remove alpha≤32 spill as in shadow-01 pipeline, fit in 512×256 with 8px margin, premultiplied LANCZOS resize, no-dither 40-color RGB palette.
