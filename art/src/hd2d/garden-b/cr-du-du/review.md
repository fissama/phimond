# Review — cr-du-du

## ImageGen attempt 1 / raw-01

Visual inspection of packed `final.png`: the giraffe/papaya identity reads clearly; the sprite is compact and the magenta key is clean. Harvest frames wave and finish as sparse motes. Plant f4 matches sprout f1 silhouette closely.

Measured: a–h pass. Sizes sprout 62/62/59/62 px, grow 109/110/110/110 px, ripe 137/137/137/136 px; maximum width 114 px; plant f4 vs sprout f1 IoU 0.9287. Gate i failed because face annotations were absent from this review. Gate j failed at min loop body IoU 0.7895. Regenerate with smaller motion confined inside the silhouette.

Face notes (packed atlas cell coordinates; eyes and mouth positions are approximate centers):
face_row_1: eyes=96,140; mouth=96,150; blink=frame1
face_row_2: eyes=96,112; mouth=96,125; blink=frame3
face_row_3: eyes=96,79; mouth=96,94; blink=frame2
face_row_4: eyes=96,75; mouth=96,90; blink=none
face_row_5: eyes=96,145; mouth=96,155; blink=none

## Gate history

| Attempt | a | b | c | d | e | f | g | h | i | j | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 62/109/137, width 114 | N/A | PASS 0.9287 | FAIL annotations absent | FAIL 0.7895 | 8/10 |
| raw-02 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 60/110/136, width 112 | N/A | PASS after face notes | FAIL 0.8065 | 9/10 |
| raw-03 | PASS | PASS | PASS | PASS 58 colors | PASS | FAIL grow 113, width 111 | N/A | PASS | FAIL 0.8080 | 8/10 |
| raw-04 | PASS | PASS | PASS | PASS 60 colors | PASS | FAIL grow 120, width 121 | N/A | PASS 0.8511 | PASS 0.9269 | 9/10 |
| raw-05 | PASS | PASS | PASS | PASS 59 colors | PASS | FAIL grow 118, width 120 | N/A | PASS 0.8348 | PASS 0.9271 | 9/10 |
| raw-06 | PASS | PASS | PASS | PASS 58 colors | PASS | PASS heights 60/86–87/145, width 107 | N/A | PASS 0.8324 | PASS 0.9531 | 10/10 mechanical |
| raw-07 | PASS | PASS | PASS | PASS 58 colors | PASS | FAIL grow 84, width 102 | N/A | PASS 0.8339 | PASS 0.9608 | 9/10 |

## Final visual check and disposition

Opened `review-pivot-grid.png` and `review-4x-dark.png` from the selected raw-06 candidate. The giraffe reads clearly at 4×, but thin purple/magenta contour fringe remains visibly attached around outlines and soil. A read-only HSV scan of non-keyed raw-06 pixels (hue 0.77–0.94, saturation ≥0.30, value ≥0.15) found 7,871 purple-like pixels. All 8 ImageGen calls for this item are used. This does not meet the no-magenta visual constraint, so the asset is recorded as blocked despite raw-06 passing the mechanical a–j checks. No pixel edits were made.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5835 before, 1201 in final quantized atlas; 5424 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
