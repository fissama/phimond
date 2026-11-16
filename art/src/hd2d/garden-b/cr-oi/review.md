# Review — cr-oi

## Face notes

face_row_1: eyes=96,143; mouth=96,153; blink=frame1
face_row_2: eyes=96,105; mouth=96,118; blink=frame3
face_row_3: eyes=96,70; mouth=96,84; blink=frame2
face_row_4: eyes=96,77; mouth=96,91; blink=none
face_row_5: eyes=96,144; mouth=96,154; blink=none

## Visual review

Raw-01 inspected: distinct round guinea-pig/guava silhouette, white blossom and green leaves; ripe chewing action reads at atlas scale. Pending packed review and a–j measurement.

## Gate history

| Source | a | b | c | d | e | f | g | h | i | j | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01 | FAIL | — | — | — | — | — | N/A | — | — | — | PACK FAIL: no common scale s≥0.6 |
| raw-02 | FAIL | — | — | — | — | — | N/A | — | — | — | PACK FAIL: no common scale s≥0.6 |
| raw-03 | PASS | PASS | PASS | PASS 58 colors | PASS | PASS 61/95/129px, width 122 | N/A | FAIL 0.7587 | PASS | PASS 0.9441 | 9/10 |
| raw-04 | PASS | PASS | PASS | PASS 58 colors | PASS | PASS 62/94–96/130–131px, width 122 | N/A | FAIL 0.7711 | PASS | PASS 0.9323 | 9/10 |
| raw-05 | PASS | PASS | PASS | PASS 59 colors | PASS | PASS 61/94–95/130px, width 122 | N/A | FAIL 0.7715 | PASS | PASS 0.9325 | 9/10 |
| raw-06 | PASS | PASS | PASS | PASS 58 colors | PASS | PASS 61/94–95/130px, width 120 | N/A | FAIL 0.7676 | PASS | PASS 0.9243 | 9/10 |
| raw-07 | PASS | PASS | PASS | PASS 57 colors | PASS | PASS 61/91–93/129–130px, width 121 | N/A | PASS 0.8934 | PASS | PASS 0.9180 | 10/10 |
| raw-08 | PASS | PASS | PASS | PASS 58 colors | PASS | PASS 61/89–92/127px, width 118 | N/A | PASS 0.9012 | PASS | PASS 0.9041 | 10/10 |

## Final visual review and disposition

Opened raw-07 packed preview at 4×. Character silhouette and cheeky guava-eating action read clearly; h and all other a–j gates pass. A visible thin pink-purple contour fringe remains on exterior edges. A non-key boundary scan using HSV hue 0.77–0.94, saturation ≥0.30, value ≥0.15 found 6,826 purple-like pixels on raw-07 versus 7,761 on raw-08, so raw-07 is the lower-fringe candidate. All 8 ImageGen calls are used. Status is blocked on the explicit no-magenta visual constraint; no pixel edits were made.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5131 before, 0 in final quantized atlas; 4979 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
