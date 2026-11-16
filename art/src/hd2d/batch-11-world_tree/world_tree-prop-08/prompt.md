# world_tree-prop-08 — four-frame sacred fruit

Route: built-in Codex image_gen; model not exposed. Generated 2026-11-05.

## Prompt used

Transparent 2x2 sprite sheet for a polished HD-2D pixel RPG. Exactly four frames, one identical floating magical World Tree fruit centered in each quadrant: pear-shaped golden amber fruit with small dark-green stem and two leaves. All four sprites same silhouette, scale and registration; only the inner amber glow shifts subtly through four brightness levels. Clear transparent gutters. Pixels are grouped and stepped, 36–42 coherent colors, crisp deep green/brown outline, forest-green and gold palette. No text, no grid lines, no border, no background, no ground, no extra particles. Keep each frame fully inside its quadrant with at least 8% transparent cell margins.

## Ordered references and SHA256

1. `.ai/design/map-checklists/refs/world_tree_gate.jpg` — `c196f4f16f3e679ebca69562144d6f0ee60f955792eb435ba69cf30d81107a03`
2. `apps/game-web/art-src/hd2d/batch-01-octopath/tree-large-02-canopy/final.png` — `0fda1f44f92d5a10b1d89f285e560a94a030172b7bed6f4228a37a34ad37b349`

## Finish

Raw source retained byte-identically at 1264×1244. Extracted four quadrant silhouettes after alpha threshold 160, centered each in 128×128, applied one shared no-dither palette and arranged as a horizontal 4-frame atlas. Final 512×128 RGBA; 40 visible RGB colors, binary alpha, frame boxes `[(25, 8, 102, 120), (25, 8, 102, 120), (25, 8, 102, 120), (25, 8, 102, 120)]`. Final viewed at 4× checker/dark. Raw SHA256 `a07b9653ac893a0ca601a93e3a2616fe9de8c78834e1d4f188089f80de449ca1`; final SHA256 `ea3f61628a4d712303433c76054795f94c16609b2512bd5a73ec7e561fc5acbc`.
