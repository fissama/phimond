# Ghost Castle — edge 01, cemetery earth to marble

Route: built-in Codex image_gen, 2026-11-04. Selected generation: raw-03, 2172×724 RGB.

Exact prompt:

> Generate a horizontally repeatable 4:1 landscape terrain edge texture for an HD-2D pixel game, intended to crop/resize to 512x128. Think of it as a looped strip: the exact visual pattern at the far left edge MUST continue at the far right edge, including matching colors and rock/soil forms. Make the composition periodic with three broad repeating clusters across the width, and place the same half-cluster at both ends so horizontal joins are seamless. Along the vertical direction, transition from dark charcoal graveyard earth with sparse dry roots at the top, through an irregular rubble boundary, into blue-black cracked marble with muted teal veins at the bottom. Straight top-down terrain texture, no perspective. The band is full-bleed; no frame or seam line. Painted pixel clusters like the approved Octopath tile references, restrained 33-48 colors, clear grouped shade ramps, dark hue-matched outlines. No text, props, fog, glow, shadows or gradients. Source image is only for Ghost Castle palette/content. Approved batch-01 edges/contact sheet establish finish and edge type. Pet sprites only establish shading and outline.

## Ordered references and SHA256

1. `.ai/design/map-checklists/refs/ghost_castle_gate.jpg` — `e1b28852ec2cc652ee9c224f73680e7448f892cb348d0201dbb1fea8eedc8caa`
2. `apps/game-web/art-src/hd2d/batch-01-octopath/edge-grass-dirt/final.png` — `cea364b6f8306a6a2db0561b36b846d0e1252cf9b9c75f383a8f97a86a2c417d`
3. `apps/game-web/art-src/hd2d/batch-01-octopath/edge-grass-roots/final.png` — `7bf3e3700ef71963c08b435e2bc1a717799e46acef74ca018b27122d4541aab8`
4. `apps/game-web/art-src/hd2d/batch-01-octopath/contact-sheet.png` — `4347e8dafc3491cb1516c88379effbf92c32b2ac1b17a0776469eedb7fa94a05`
5. `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` — `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

## Finish

`raw-01.png` is the exact generated image. The crop was `[0,90,2172,633]`, then resized to 512×128 with Lanczos and snapped to a 40-color palette. No image content was drawn in code. Raw SHA256: `ecca2953f49e816fa5e6169612efb639f6e4ec76c2ec5592bbb30bbe1070d15b`. Final SHA256: `56e01308af9369f1f7d649f573345dedd7bf55c1708b04d07635d09c538d3a81`.

Earlier rejected generations are retained under `jobs/edge-01-20261104/`: attempt 01 has incompatible soil/stone endpoints; attempt 02 seam ratio was 1.7866 (>1.25). Selected attempt 03 seam report is 0.807923 (continuous).
