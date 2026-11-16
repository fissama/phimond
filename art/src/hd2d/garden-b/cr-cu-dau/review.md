# Visual review — cr-cu-dau

Image reviewed: final.png (20-frame 4×5 atlas).

## Face notes (cell-local pixel coordinates)
face_row_1: eyes=94,145; mouth=96,154; blink=frame3
face_row_2: eyes=96,143; mouth=96,153; blink=frame3
face_row_3: eyes=96,137; mouth=96,151; blink=frame3
face_row_4: eyes=96,145; mouth=96,154; blink=none
face_row_5: eyes=96,145; mouth=96,154; blink=none

## Visual inspection
Reviewed the packed atlas directly: character identity is readable at atlas scale, face remains present through all stages, looping rows include a visible closed-eye frame, and harvest / plant rows remain distinct. Measurements are recorded in qa.json; this note records visual presence, not Claude approval.

## Latest gate results (measure_atlas.py)

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | see qa.json |
| b | PASS | see qa.json |
| c | PASS | see qa.json |
| d | PASS | see qa.json |
| e | PASS | see qa.json |
| f | PASS | heights {'1': [71, 70, 70, 71], '2': [101, 104, 103, 102], '3': [124, 123, 124, 124]}; max width 128 px |
| g | PASS | see qa.json |
| h | PASS | plant/sprout IoU 0.9136 |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.8547 |

Overall: PASS (10/10). This is mechanical QA, not Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 10033 before, 4364 in final quantized atlas; 7375 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
