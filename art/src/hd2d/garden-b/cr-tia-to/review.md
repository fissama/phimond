# Visual review — cr-tia-to

Inspected latest `final.png`. The perilla bat identity remains cute and readable; sprout, grow and ripe now have visibly different silhouettes. Harvest ends with sparse rays. The ripe leaf cape animation reads, but the mature wings remain too broad.

Face notes (cell-local, approximate):
- face_row_1: eyes=96,130; mouth=96,143; blink=frame3
- face_row_2: eyes=96,108; mouth=96,126; blink=frame3
- face_row_3: eyes=96,68; mouth=96,86; blink=frame2
- face_row_4: eyes=96,102; mouth=96,121; blink=none
- face_row_5: eyes=96,137; mouth=96,148; blink=none

## Attempts and latest measured result
Eight image_gen calls were used. Attempts were retained as `raw-10.png` through `raw-17.png` plus standalone `raw-11.png`/`raw-12.png` references; one sheet (`raw-13.png`) could not be packed at scale ≥0.6. Latest `raw-17.png` improves shape continuity and plant overlap but still fails f: sprout 94px (max75), grow 126–127px (max112), width160px (max140). Gates h=0.8369 and j=0.9056 pass; remaining a–e and i also pass. No thresholds were changed. Redraw recommendation: make sprout and grow substantially smaller relative to ripe, narrow both perilla leaves, preserve the already passing h and j geometry.

## Latest gate results (measure_atlas.py)

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | see qa.json |
| b | PASS | see qa.json |
| c | PASS | see qa.json |
| d | PASS | see qa.json |
| e | PASS | see qa.json |
| f | PASS | heights {'1': [67, 68, 67, 68], '2': [97, 98, 98, 98], '3': [137, 137, 137, 137]}; max width 117 px |
| g | PASS | see qa.json |
| h | PASS | plant/sprout IoU 0.9269 |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.9226 |

Overall: PASS (10/10). This is mechanical QA, not Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-17.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 25578 before, 25600 in final quantized atlas; 1353 pixels replaced. Mechanical gates: 9/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
