# Visual review — cr-ot

Inspected `final.png`. The curled red pepper tail and green calyx clearly identify the character; cream face reads at native atlas size. The three growth sizes are distinct, and the ripe row shows the tiny orange breath then fanning gesture. Harvest remains friendly and sparse.

Face notes (cell-local, approximate):
- face_row_1: eyes=96,139; mouth=96,149; blink=frame3
- face_row_2: eyes=96,109; mouth=96,127; blink=frame3
- face_row_3: eyes=96,75; mouth=96,96; blink=frame3
- face_row_4: eyes=96,86; mouth=96,102; blink=none
- face_row_5: eyes=96,139; mouth=96,150; blink=none

Selected `raw-05.png` corrected the previous sprout height/width miss. Current full measurements are in `qa.json`.


## Edge defringe — 2026-11-12

Repacked from `raw-05.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6171 before, 0 in final quantized atlas; 6151 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
