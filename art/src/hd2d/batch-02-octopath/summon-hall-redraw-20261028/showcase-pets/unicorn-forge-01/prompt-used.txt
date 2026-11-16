# Triệu Linh Điện — three guardian showcase sprites

Route: built-in Codex ImageGen, 2026-10-28. `raw-01.png` is preserved byte-identically (2172×724; SHA256 `d5eb25515a42ce851ae07e1e4735f1765d2594c47bd359e312ce5ac79a04b0ae`). The 3 equal source cells are 724×724.

Prompt: Create a three-character showcase sprite sheet for the three established 5★ guardians displayed above the summoning hall's three starter pedestals. Layout: exactly 3 equal square cells in one horizontal row, transparent-friendly pure #FF00FF background, one full-body creature per cell. Cell 1: Linh Tiên Hoa Hương, the same pink blossom-winged plant fairy from reference 1, clearly recognizable with layered green-to-indigo leaf dress, large pink flower petals/wings and warm green-eyed face. Cell 2: Kim Kỳ Lân (also called Thú Vàng Một Sừng in legacy data), the same elegant ivory/gold unicorn from reference 2, with exactly one horn, golden flame-like mane and tail, four clear legs, no wings or armor. Cell 3: Độc Hạt Vương (legacy roster name Đại Vương Bọ Cạp), the same purple-bodied scorpion king from reference 3, with two large red pincers, multiple articulated legs and one arched segmented red tail with a glowing amber stinger. Preserve the established species identity and silhouette from each attached reference; do not blend their traits. These are dignified, calm idle showcase poses, facing slightly toward the viewer, hovering/standing without a base; no attack, no motion trails, no extra creatures. Give each generous clear space, no overlap. Pixel art consistent with approved Phimond HD-2D sprites: chunky readable clusters, crisp pixel edges, warm upper-left light, dark same-hue outline, 2–4 tones per material, around 40 colors, no smooth gradients, no bloom/glow, no background, no pedestal, no shadow, no text or labels.

References and SHA256 (identity refs first, followed by outline/shading refs):

- `apps/client/public/pets/species_0144.webp` — `ef685e9c868e5d287c783e018af029a973f2f3f4514fab4fdab8a895f376bdd2`
- `apps/client/public/pets/species_0149.webp` — `c00ede4e39b226232d8783db55d9ecce747a46af62d1aa94f895503ab7ffac90`
- `apps/client/public/pets/species_0151.webp` — `2715dc960e0b352603b73c18659b9442e7a94be559e98f6a76b54f265c23c176`
- `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`
- `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` — `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`

Processing: Sprite Forge `generate2dsprite.py process`, target asset, mode sheet, 1×3, 192px output cells, magenta chroma key, soft matte/despill, then shared 48-colour palette and binary-alpha finish. Intended for pedestal display only; no combat or gameplay change. Owner approval pending.
