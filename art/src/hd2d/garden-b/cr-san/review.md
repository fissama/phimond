# Review — cr-san

## Face notes
face_row_1: eyes = 88,143; mouth = 96,153; blink = frame3
face_row_2: eyes = 88,119; mouth = 96,132; blink = frame2
face_row_3: eyes = 88,83; mouth = 96,99; blink = frame3
face_row_4: eyes = 88,78; mouth = 96,98; blink = none
face_row_5: eyes = 88,141; mouth = 96,151; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-02.png | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | h=0.6916; heights 64/104/147–148 px; width=121 px; min loop IoU=0.9529 |
| raw-03.png | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | FAIL | FAIL | PASS | heights 102–105/118–121/133–134 px; h=0.7145; min loop IoU=0.9004 |
| raw-04.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-05.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-06.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-07.png | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | 56 colors; heights 72/97–98/143 px; width=136 px; h=0.9343; min loop IoU=0.9510 |
| raw-08.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |

Visual review: opened `review-4x-dark.png` generated from raw-07. Cassava puppy identity, root tail, leaf cap, faces, and harvest fade are readable. A visible pink/violet fringe persists on the sprite contours after eight ImageGen outputs. No pixel cleanup was applied. Best mechanical candidate raw-07 passes a–j, but visual style remains blocked.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5976 before, 0 in final quantized atlas; 5928 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
