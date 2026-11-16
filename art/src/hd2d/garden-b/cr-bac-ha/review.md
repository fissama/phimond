# Visual review — cr-bac-ha

Inspected `review-4x-checker.png`, `review-4x-dark.png`, and each of the five row previews. The mint-leaf kitten motif and face read clearly; row 1 is still too large for sprout, row 2 exceeds grow height, and row 3 exceeds ripe height. The harvest sequence is friendly and ends in sparse rays, but stages are independently redrawn and drift sideways. Visual review: **FAIL**.

Face notes below are approximate cell-local positions from the 4× previews, not machine-detected measurements.
face_row_1: eyes=96,139; mouth=96,151; blink=frame3
face_row_2: eyes=96,104; mouth=96,120; blink=frame3
face_row_3: eyes=96,70; mouth=96,89; blink=frame2
face_row_4: eyes=96,83; mouth=96,101; blink=none
face_row_5: eyes=96,142; mouth=96,153; blink=none

Mechanical review (`qa.json`): a,b,g,h PASS; c,d,e,f FAIL; i PASS from visual notes. Safe-area violations 7; invariant body colors 0; root-center spread 35.15 px; heights sprout 52–70 px, grow 115–116 px, ripe 155–164 px (max width 159 px). Harvest4 coverage 1.50%; plant4→sprout1 difference 28.71%.


## Pipeline v3 round 1 — raw-09 pack

Inspected refreshed 4× checker/dark atlas, pivot grid and every row preview/GIF. The mint-cat character remains readable; the face and blink poses are legible at preview scale. Visual review: PASS.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | all pivots within ±1 |
| f | PASS | heights 61–63 / 95 / 120–121 px; width 108 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU 0.9122 (≥0.80) |
| i | PASS | blink row1 f3, row2 f3, row3 f2; face positions above |
| j | PASS | minimum loop body IoU 0.9277 (≥0.85) |


## Pipeline v3 final — raw-09, independently remeasured 2026-11-10

Opened the current 4× checker and dark previews, pivot grid, and all five row strips. The mint-leaf kitten spirit keeps a readable face and distinct sleepy, curious, proud, friendly-harvest, and waking expressions. Rows 1–3 each show a blink; harvest ends with sparse rays. Visual review: **PASS for handoff; Claude review pending**.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 61–63 / 95 / 120–121 px; max width 108 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU 0.9117 |
| i | PASS | blink row1 f3, row2 f3, row3 f2; positions above |
| j | PASS | minimum loop body IoU 0.9277 |


## Edge defringe — 2026-11-12

Repacked from `raw-09.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7753 before, 3161 in final quantized atlas; 6598 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
