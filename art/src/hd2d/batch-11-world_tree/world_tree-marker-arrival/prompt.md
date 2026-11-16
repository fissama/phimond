# World Tree arrival marker — four frame leaf rune

Route: built-in Codex image_gen; model not exposed. Generated 2026-11-05.

## Prompt used

A four-frame 2x2 game VFX atlas, transparent background, for a small flat overhead arrival marker on the ground in Phimond's World Tree map. Every equal square cell contains the SAME small circular ground glyph, viewed perfectly from above: a thin broken ring of tiny emerald leaf-shaped runes and muted golden dots, like a magical floor decal. It must be flat on the ground and occupy only about 45% of each cell; it is NOT a portal, NOT an arch, NOT a gate, NOT a standing object. Four consecutive looping phases, arranged clockwise: top-left sparkle at 12 o'clock, top-right at 3, bottom-right at 6, bottom-left at 9; ring geometry, size, center and colors identical in every frame, only one tiny gold sparkle moves. Crisp pixel-art clusters, dark hue-shifted outlines, high-quality Octopath HD-2D game FX. Palette forest green, emerald and restrained gold. Each cell independent with generous padding. Actual transparent background; no checkerboard, no text, no beams, no shadows, no floor surface, no props, no larger than the ring. References: map only for palette, existing teal arrival marker only for small flat size/function, firefly for sparkle style, pet sprites for outline weight.

## Ordered references and SHA256

1. `.ai/design/map-checklists/refs/world_tree_gate.jpg` — `c196f4f16f3e679ebca69562144d6f0ee60f955792eb435ba69cf30d81107a03`
2. `apps/game-web/art-src/hd2d/batch-11-ghost_castle/ghost_castle-marker-arrival/final.png` — `27843890174bb2b176928ae77ac914edb47a901dc201d3d87e32a923415b73a6`
3. `apps/game-web/art-src/hd2d/batch-01-octopath/firefly/final.png` — `44fea9f36370f69387c35062e00bf93eb5b30d6065d48dc05a4ef340cc4730ee`
4. `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
5. `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Raw SHA256: `5f191084b3c98226fe01f520ca12ac3e69099c754562644cc4e26978237ddeaf`; final SHA256: `5a6612452240fd8de17582ca49ac9971dbd7e606d79b90915215f59348fbc7ae`. Finish: split raw 2×2 in clockwise frame order, resize each cell with LANCZOS to 92×92 then center on 128×128 frame, binary alpha threshold 128, shared no-dither 40-color palette.
