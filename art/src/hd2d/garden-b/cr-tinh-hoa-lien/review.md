# Visual review — cr-tinh-hoa-lien

Selected `raw-08.png` after 8 ImageGen outputs. Inspected refreshed 4× dark preview, checker preview, pivot grid, and row previews. Crystal-lotus princess silhouette is consistent, friendly, and readable; all three loop rows visibly blink. **Visual FAIL:** violet/magenta contour fringe remains visible around petals and face against the dark background after the final generation. Keep blocked for ImageGen limit; do not claim ready.

Face notes are approximate cell-local positions from the preview:
face_row_1: eyes=96,139; mouth=96,151; blink=frame3
face_row_2: eyes=96,104; mouth=96,120; blink=frame3
face_row_3: eyes=96,70; mouth=96,89; blink=frame3
face_row_4: eyes=96,82; mouth=96,100; blink=none
face_row_5: eyes=96,142; mouth=96,153; blink=none

## Final measurement

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 opaque pixels outside [16,175] |
| d | PASS | 56 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 72 / 106–107 / 137 px; max body width 121 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU 0.8818 |
| i | PASS | blink row1 f3, row2 f3, row3 f3; face positions above |
| j | PASS | minimum loop body IoU 0.9571 |

`qa.json` contains the raw measurements and pack provenance. Visual gate remains failed due to the visible fringe.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6814 before, 2086 in final quantized atlas; 5269 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
