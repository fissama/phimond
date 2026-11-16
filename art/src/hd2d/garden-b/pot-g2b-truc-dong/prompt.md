# Prompt/provenance — pot-g2b-truc-dong

## Asset brief
Trúc Đồng — bó 3–4 ống tre xanh vàng nhạt, đốt rõ, miệng nhiều tầng.

## Contract
- 4×5 sheet, pure #FF00FF backing, packed by garden-b/tools/pack_atlas.py; 768×960 RGBA atlas.
- HD-2D Octopath pixel art, hard pixel clusters, same-tone outlines, no baked shadow/glow/text.
- Pot: no face; stable body; wet soil darkening >=15%; final body width 130–158 px, body height 70–100 px.

## Source provenance
- Selected packed source: `raw-29.png` (sha256 `a023eb7543dce6855888b3980476f606f12d49e1f11c970ea346769e09ec3ff1`).
- ImageGen outputs in this continuation: 8 (`raw-21.png`, `raw-22.png`, and `raw-24.png` through `raw-29.png`); all generated raw sheets were retained. `raw-23.png` is unused.
- Current final is checked in `qa.json`; review findings are in `review.md`.

## Selected repair source — 2026-11-13

Repacked from `raw-29.png` (SHA-256 `a023eb7543dce6855888b3980476f606f12d49e1f11c970ea346769e09ec3ff1`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 7752→2866. body IoU .9451; wet darkening 2.80%; edge 7752→2866.


## Wet-soil/body repair — 2026-11-16

Six new built-in ImageGen sheets retained as raw-34.png through raw-39.png. Selected raw-35 SHA-256 `709b7176ff51f286d9d725522c6a3061d7ace858897426bd7d37cd57332eb034`; the other five did not improve both gate-g soil and stable body IoU. Final prompt retained the same bamboo silhouette and asked for wet soil at least 20% darker with subtle water ripples.

### 2026-11-16 palette and upgrade redraw
Selected `raw-44.png` from six outputs `raw-42..47`. Colors and upgrade appearance improved, but g still fails at adjacent body IoU=.9371 and wet darkening=3.95%. See review.md.
