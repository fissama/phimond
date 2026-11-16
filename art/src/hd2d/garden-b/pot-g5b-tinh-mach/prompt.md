# Prompt/provenance — pot-g5b-tinh-mach

## Asset brief
Tinh Mạch — chậu đá tím sẫm, mạch vàng và tinh thể ở miệng.

## Contract
- 4×5 sheet, pure #FF00FF backing, packed by garden-b/tools/pack_atlas.py; 768×960 RGBA atlas.
- HD-2D Octopath pixel art, hard pixel clusters, same-tone outlines, no baked shadow/glow/text.
- Pot: no face; stable body; wet soil darkening >=15%; final body width 130–158 px, body height 70–100 px.

## Source provenance
- Selected packed source: `raw-11.png` (sha256 `930f6cc41a2d076b4d7c899cf5ff17b9bf21ab24745e29ac0a50a95d00fabc43`).
- ImageGen outputs in this continuation: 8 (`raw-04.png` through `raw-11.png`); all retained. Raw-04 failed packing; raw-05 through raw-11 packed but retained one or more measured failures.
- Current final is checked in `qa.json`; review findings are in `review.md`.

## Selected repair source — 2026-11-13

Repacked from `raw-13.png` (SHA-256 `782e12d7df852dde0b4557ef31d6df07f8da47fe104b75bd314dd17632257576`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 10/10; purple edge count 20237→16475. all gates pass; body IoU .9536; join min .9436; wet darkening 46.40%; edge 20237→16475.
