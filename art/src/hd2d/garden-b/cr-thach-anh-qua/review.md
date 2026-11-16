# Visual review — cr-thach-anh-qua

Selected `raw-08.png` after 8 outputs. Inspected refreshed 4× checker and dark previews, pivot grid, and all five row previews. The quartz-owl face reads clearly, sprout/grow/ripe silhouettes are distinct, and harvest ends with sparse rays. **Visual FAIL:** persistent violet/magenta contour fringe remains visible around sprites in the dark preview, despite repeated prompts for dark-only outlines. Blocked at ImageGen limit.

Face notes (approximate cell-local coordinates from preview):
face_row_1: eyes=96,136; mouth=96,148; blink=frame3
face_row_2: eyes=96,111; mouth=96,125; blink=frame3
face_row_3: eyes=96,78; mouth=96,94; blink=frame3
face_row_4: eyes=96,84; mouth=96,101; blink=none
face_row_5: eyes=96,143; mouth=96,155; blink=none

## Final measurement

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 opaque pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 64 / 96 / 122–123 px; max width 119 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU 0.8884 |
| i | PASS | blink row1 f3, row2 f3, row3 f3 |
| j | PASS | minimum loop body IoU 0.9385 |

Mechanical measurements and packing provenance are in `qa.json`. Visual gate remains failed due to the visible fringe.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6005 before, 3805 in final quantized atlas; 3468 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.

## Visual identity check after defringe — 2026-11-13

The quartz-owl character and face remain readable, but small violet/magenta pixels still form a visible fringe on the outer sprite contours.
