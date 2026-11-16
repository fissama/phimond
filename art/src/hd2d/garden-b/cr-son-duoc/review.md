# Visual review — cr-son-duoc

Sơn Dược is a gentle, sleepy baby snake made from a heart-leaf vine coiled around a short stake; the plump cream yam-root belly carries its face. It reads distinctly from both pilot plants. Row 3 shows the lazy head yawn and tail swish. Harvest is friendly and the final cell resolves to a few lights.

Face notes are approximate cell-local positions from the current 4× preview.
face_row_1: eyes=96,137; mouth=96,150; blink=frame3
face_row_2: eyes=96,108; mouth=96,122; blink=frame3
face_row_3: eyes=96,74; mouth=96,94; blink=frame2
face_row_4: eyes=96,79; mouth=96,96; blink=none
face_row_5: eyes=96,138; mouth=96,151; blink=none

## Pipeline v3 round 1 — raw-01

| Gate | Result | Measurement |
|---|---|---|
| pack | FAIL | No common scale s≥0.6; harvest row4 frame2 effect reached x=13 (<16) |

## Pipeline v3 round 2 — raw-02

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | FAIL | sprout 84–86 px; grow 100–101; ripe 122; max width 129 |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU 0.9209 |
| i | PASS | blink rows 1–3: frame3 / frame3 / frame3; face notes above |
| j | FAIL | minimum loop body IoU 0.8228 |

## Pipeline v3 round 3 — raw-03

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | FAIL | sprout 59–60; grow 89–90; ripe 115; max width 128 |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.7102 |
| i | PASS | blink rows 1–3 present; face notes above |
| j | PASS | minimum loop body IoU 0.8973 |

## Pipeline v3 round 4 — raw-04

| Gate | Result | Measurement |
|---|---|---|
| a–e | PASS | correct canvas/alpha; 20 unique frames; safe bounds; 60 colors; pivots ±1 |
| f | PASS | heights 57–59 / 87 / 131 px; max width 129 px |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.7461 |
| i | PASS | blink rows 1–3: frame3 / frame3 / frame2; face notes above |
| j | PASS | minimum loop body IoU 0.9194 |


## Pipeline v3 round 5 — raw-05

| Gate | Result | Measurement |
|---|---|---|
| a–e | PASS | 768×960; alpha 0/255; 20 unique; safe; 60 colors; pivots ±1 |
| f | PASS | heights 57–59 / 86–88 / 131 px; width 129 px |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.7609 |
| i | PASS | blinks documented above |
| j | PASS | min loop IoU 0.9144 |

## Pipeline v3 round 6 — raw-06

| Gate | Result | Measurement |
|---|---|---|
| a–e | PASS | 768×960; alpha 0/255; 20 unique; safe; 60 colors; pivots ±1 |
| f | PASS | heights 58–60 / 88–89 / 132–133 px; width 130 px |
| g | N/A | crop |
| h | FAIL | IoU 0.7552; sprout bbox 76×59, plant4 bbox 85×67 |
| i | PASS | blinks documented above |
| j | PASS | min loop IoU 0.9102 |

## Pipeline v3 round 7 — raw-07

| Gate | Result | Measurement |
|---|---|---|
| a–e | PASS | 768×960; alpha 0/255; 20 unique; safe; 60 colors; pivots ±1 |
| f | PASS | heights 58–60 / 88 / 132 px; width 129 px |
| g | N/A | crop |
| h | FAIL | IoU 0.7653; target ≥0.80 |
| i | PASS | blinks documented above |
| j | PASS | min loop IoU 0.9050 |

## Pipeline v3 round 8 — raw-08 (attempt limit reached)

Opened the current 4× checker and dark previews. The sleepy vine-snake, heart leaves, cream root belly, and short stake read clearly at atlas scale; loop-row blinks are visible; harvest f4 ends as sparse lights. Visual note: plant f4 is very close in overall design but remains slightly larger/wider than sprout f1.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 59–60 / 88 / 129 px; max width 127 px |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.7950 (required ≥0.80) |
| i | PASS | blink row1 f3, row2 f3, row3 f2; face notes above |
| j | PASS | minimum loop body IoU 0.9111 |

After 8 ImageGen attempts, h remains short by 0.0050 IoU. Proposed next change: redraw only plant f4 1–2 px smaller at the same pivot to match sprout f1's 76×59 bbox; retain its current sleepy pose and remove any extra opaque pixels. No threshold waiver.

## Targeted plant-frame correction (this task)

The plant f4 single-frame ImageGen source used the packed sprout f1 as its primary reference (`reference-sprout-f1.png`). The first full-atlas ImageGen output changed unrelated frames and was not selected. The selected raw sheet was assembled from the untouched packed frames plus the generated f4, then processed by the unchanged `pack_atlas.py`.

| Source | a | b | c | d | e | f | g | h | i | j | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-11 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | h IoU 0.9480; heights 60 / 88 / 128 px; width 135; loop min 0.8923. |

Face positions and blink frames are unchanged. Visual review of the corrected atlas shows the same sleepy vine-snake design; only plant f4 has the new waking/yawn expression.


## Edge defringe — 2026-11-12

Repacked from `raw-11.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6220 before, 2803 in final quantized atlas; 4441 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
