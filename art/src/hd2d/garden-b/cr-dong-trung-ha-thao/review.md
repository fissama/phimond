# cr-dong-trung-ha-thao — self review

Selected candidate: `raw-08.png` (ImageGen attempt 8/8). All raw outputs `raw-01.png` through `raw-08.png` are retained.

## Face notes (cell-local coordinates)

face_row_1: eyes=92,132; mouth=96,139; blink=frame3
face_row_2: eyes=91,115; mouth=96,123; blink=frame3
face_row_3: eyes=86,86; mouth=96,98; blink=frame3
face_row_4: eyes=86,100; mouth=96,112; blink=none
face_row_5: eyes=92,136; mouth=96,145; blink=none

## Measured gates

- a PASS: 768x960 RGBA; alpha `[0,255]`; hidden RGB count 0.
- b PASS: 20/20 nonempty and unique.
- c PASS: no opaque pixels outside `[16,175]`.
- d PASS: 54 visible colors (≤60).
- e PASS: all 20 pivots within ±1.
- f PASS: sprout `[54,60,55,55]`, grow `[93,93,93,93]`, ripe `[150,150,145,150]`; max width 81 px.
- g N/A for crop.
- h PASS: plant f4 vs sprout f1 IoU `0.8607`.
- i PASS: rows 1–3 blink at frame 3; face annotations present for all rows.
- j PASS: minimum loop IoU `0.8675`.

## Visual review

Opened `review-4x-dark.png` after export. The character is readable and compact, with clear growth progression and warm cream/orange materials. However, the contour has distinct violet/magenta pixels against the dark background. This violates the style rule; do not treat this asset as ready despite the 10/10 mechanical result.

## Attempts

Eight ImageGen outputs were used. Attempts 1–3 were rejected for visual contour fringe; attempts 4–5 had packing/size issues; attempt 6 failed loop IoU (`0.8321`); attempt 7 fixed the grow loop but retained the fringe; attempt 8 passes mechanics but still retains the fringe.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 3727 before, 0 in final quantized atlas; 3684 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
