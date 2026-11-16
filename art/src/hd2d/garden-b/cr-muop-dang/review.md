# Visual review — cr-muop-dang, raw-01

Opened the packed 4× dark view. The dark green ridged baby crocodile, yellow flower, sleepy/grumpy-to-friendly face, and growth progression read clearly. Harvest ends with sparse motes. A pink/magenta contour fringe is visible around the sprites; treat as visual style failure until corrected.

Face notes (approximate cell-local):
face_row_1: eyes=96,148; mouth=96,157; blink=frame3
face_row_2: eyes=96,122; mouth=96,139; blink=frame3
face_row_3: eyes=85,89; mouth=98,108; blink=frame2
face_row_4: eyes=84,92; mouth=99,107; blink=none
face_row_5: eyes=96,145; mouth=96,155; blink=none

## Final candidate review — raw-06

Opened the packed 4× dark preview and inspected the sprite shapes. The dark-green warty crocodile/gourd, cream belly, yellow blossom, facial changes, growth progression, plant return, and sparse harvest ending are readable. The atlas passes all mechanical gates. A thin pink/violet fringe remains visible around the sprite contours at 4×, despite eight ImageGen attempts, so it does not meet the no-magenta visual requirement and is blocked from handoff readiness.

Face notes (approximate cell-local positions):
face_row_1: eyes=96,145; mouth=96,155; blink=frame3
face_row_2: eyes=96,113; mouth=96,132; blink=frame3
face_row_3: eyes=86,83; mouth=96,106; blink=frame2
face_row_4: eyes=84,88; mouth=96,104; blink=none
face_row_5: eyes=96,145; mouth=96,155; blink=none

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; transparent RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 58 colors |
| e | PASS | all pivots within ±1 |
| f | PASS | 62 / 87–88 / 142 px; width 122 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU=0.9313 |
| i | PASS | blink row1 f3, row2 f3, row3 f2; face notes above |
| j | PASS | minimum loop body IoU=0.9604 |

Attempt log (all raw sheets retained): raw-01 passed a–h,j after face-note annotation; raw-02 failed f (ripe 119 px); raw-03 passed a–j; raw-04 passed a–j but drifted away from the crocodile identity; raw-05 passed a–j; raw-06 passed a–j and retained the clearest compact crop silhouette; raw-07 passed a–j; raw-08 failed j=0.8440. Pink/violet contour fringe remained visible in the selected and alternate packed previews. Status: BLOCKED after 8 outputs; no waiver or approval assigned.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 4997 before, 0 in final quantized atlas; 4976 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
