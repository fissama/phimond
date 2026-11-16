# Prompt/provenance — cr-hoa-hong

## Asset brief
Hoa Hồng — công chúa gai, váy cánh hoa đỏ, cúi chào xoay váy.

## Contract
- 4×5 sheet, pure #FF00FF backing, packed by garden-b/tools/pack_atlas.py; 768×960 RGBA atlas.
- HD-2D Octopath pixel art, hard pixel clusters, same-tone outlines, no baked shadow/glow/text.
- Crop: visible cute face; distinct sprout/grow/ripe sizes; loop rows blink; harvest and plant are one-shot.

## Source provenance
- Selected packed source: `raw-06.png` (sha256 `e951927cc3b504aa02be117eaffb75c5c09f7822a1e70c64a5edda4ba330c3d7`).
- ImageGen generations recorded this turn: 0. Exact payloads for reused raw sources from prior turns were not preserved in the repo; this file records the production brief and source hash rather than claiming a verbatim historic prompt.
- Current final is checked in `qa.json`; review findings are in `review.md`.

## Current task — plant row 5 redraw

Plant f1 must begin as a tiny seed in a small soil mound; f2 cracks/sprouts; f3 grows slightly; f4 matches the extracted sprout f1 silhouette (IoU >=0.80). Never start with a mature plant. Only row 5 may change.

ImageGen reference attached: `reference-sprout-f1.png` (cropped directly from packed sprout f1); sha256 `7050d7f2c78c612f4f76f36816311ab4a5e806027258a263d984556283b4945b`.

The built-in ImageGen edit request was rejected before output with HTTP 429 `usage_limit_reached`; no pixels or atlas rows were changed.

## 2026-11-11 row-5 repair provenance

- ImageGen calls for this repair: 4 successful outputs (plant row seed progression; background correction; f4 silhouette attempt; f4 scale correction).
- Reference: `reference-sprout-f1.png`, sha256 `e036d6064bee1bf590658750de57d83ff153ee310928c38653b33195c841123e`.
- Selected sheet: `raw-10.png`, sha256 `80c2d444554f3cb4745dcbedecbd8d393b3fc09362cc4c1b08b4c86a77c8d67b`.
- Final QA: all gates PASS; h=0.8823; min loop IoU=0.9216.
