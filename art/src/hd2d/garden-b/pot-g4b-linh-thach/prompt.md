# Prompt/provenance — pot-g4b-linh-thach

## Asset brief
Linh Thạch — chậu đá xám xanh, tinh thể ngọc gắn ở viền.

## Contract
- 4×5 sheet, pure #FF00FF backing, packed by garden-b/tools/pack_atlas.py; 768×960 RGBA atlas.
- HD-2D Octopath pixel art, hard pixel clusters, same-tone outlines, no baked shadow/glow/text.
- Pot: no face; stable body; wet soil darkening >=15%; final body width 130–158 px, body height 70–100 px.

## Source provenance
- Selected packed source: `raw-08.png` (sha256 `45ce2faa52b5644b2a0c6227b26c3bccb96b76472b970891e73f2650cd560a01`).
- ImageGen outputs in this continuation: 4 (`raw-05.png` through `raw-08.png`); all retained. Raw-05 failed packing; raw-06/07 failed one or more gates; raw-08 passes.
- Current final is checked in `qa.json`; review findings are in `review.md`.
