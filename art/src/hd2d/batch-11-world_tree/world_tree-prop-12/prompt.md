# world_tree-prop-12 — four-frame firefly

Route: built-in Codex image_gen; model not exposed. Generated 2026-11-05.

## Prompt used

A perfectly aligned 2x2 animation sprite sheet on transparent background for a 2D HD-2D pixel RPG. In EACH of the four equal quadrants, draw EXACTLY ONE identical firefly sprite: a tiny dark forest-green beetle body, two small pale green wings, two antennae, one golden glowing abdomen. Keep the sprite same size, orientation, and position in all four cells. Only change abdomen brightness subtly: dim, medium, bright, medium. Do not draw groups, duplicates, extra insects, tails, particle effects, stars, lines, labels, dividers, or background. Each sprite centered inside its own quadrant with large transparent margin. Crisp pixel clusters, limited coherent green and gold palette, dark same-hue outline. Transparent alpha everywhere outside the four individual fireflies.

## Ordered references and SHA256

1. `.ai/design/map-checklists/refs/world_tree_deep_woods.jpg` — `471eac275c1feccaab31d6d70d6d26e43c93995f4ec9036cf1af539cb4b5cee0`
2. `apps/game-web/art-src/hd2d/batch-01-octopath/tree-large-03-canopy/final.png` — `aed538f11738feeffbc67043106d610745f316712ae370e0196d24500705a161`

## Finish

First take rejected because cell counts differed (single fly in top cells, clusters in bottom cells); retained as raw-01. Selected raw-02 retained byte-identically at 1269×1240. Alpha threshold 160, quadrant crops, nearest fit to 112×96 and centering in 128×128; shared no-dither palette and binary alpha; arranged horizontal four-frame atlas 512×128. Visible colors: 39; frame boxes `[[8, 16, 120, 112], [8, 15, 120, 112], [8, 16, 120, 112], [8, 15, 120, 112]]`. Final viewed 4× checker/dark. Raw SHA256 `67efe124145a26ade2f93dc12c940cfe5ad0cf2c09a79b1cb101d9cdca84d000`; final SHA256 `8d87e207b3eae6f4ede19f812552c8c690a419779fb26a5ee8e01b7c18e1cbc4`.
