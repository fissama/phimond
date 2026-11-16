# Visual review — cr-ca-phe

Selected `raw-05.png` after 8 outputs: it has the best measured gate coverage. Inspected refreshed 4× dark preview, checker preview, pivot grid, and row strips. Coffee-bean silhouette, red berry cap, green leaves, and small cup read clearly. **Visual FAIL:** a violet/magenta contour fringe remains visible around the sprite edges in the dark preview after 8 outputs. Blocked at ImageGen limit.

Face notes (approximate cell-local coordinates):
face_row_1: eyes=96,137; mouth=96,150; blink=frame3
face_row_2: eyes=96,111; mouth=96,126; blink=frame3
face_row_3: eyes=96,73; mouth=96,91; blink=frame3
face_row_4: eyes=96,86; mouth=96,102; blink=none
face_row_5: eyes=96,143; mouth=96,155; blink=none

## Final measurement

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 opaque pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 65–66 / 92 / 133 px; max width 134 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU 0.8077 |
| i | PASS | blink row1 f3, row2 f3, row3 f3 |
| j | PASS | minimum loop body IoU 0.9077 |

Mechanical measurements and pack provenance are in `qa.json`; visual gate remains failed because of the fringe.


## Edge defringe — 2026-11-12

Repacked from `raw-05.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7289 before, 3446 in final quantized atlas; 5079 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.

## Visual identity check after defringe — 2026-11-13

The coffee-fruit character and face remain readable, but small violet/magenta pixels still form a visible fringe on the outer sprite contours.
