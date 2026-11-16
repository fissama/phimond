# Review — cr-hau-dau-co

## Face notes
Opened raw-03 source sheet: faces are forward in all looping rows. Face positions below are approximate cell-local coordinates.
face_row_1: eyes = 88,143; mouth = 96,153; blink = frame3
face_row_2: eyes = 88,113; mouth = 96,128; blink = frame2
face_row_3: eyes = 86,80; mouth = 96,101; blink = frame3
face_row_4: eyes = 86,81; mouth = 96,103; blink = none
face_row_5: eyes = 88,143; mouth = 96,153; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS* | FAIL | f grow frame4=114 px; j min loop=0.6175; row1 frames1-2 face not visible |
| raw-02.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-03.png | PASS | PASS | PASS | PASS | FAIL | FAIL | N/A | PASS | PASS | PASS | e plant row frame1 pivot x=86.89/y=135; f width=152; h=0.9235; loop=0.9238 |
| raw-04.png | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | 59 colors; heights 65–70/89–94/125–129; width=102; h=0.9259; loop=0.8992 |
| raw-05.png | PASS | PASS | PASS | PASS | FAIL | FAIL | N/A | PASS | PASS | PASS | plant f1 pivot x=125.5/y=103; ripe width=155; h=0.9606; loop=0.9200 |
| raw-06.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-07.png | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | FAIL | PASS | PASS | sprout=88 px, grow frame3=113 px; h=0.7811; loop=0.9645 |
| raw-08.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |

Final visual review: opened `review-4x-dark.png` generated from best mechanical candidate raw-04. Character identity, face, and stage progression read clearly, but a visible pink/violet contour fringe remains. This blocks visual approval after eight ImageGen outputs. No pixel edits were made.


## Edge defringe — 2026-11-12

Repacked from `raw-04.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5053 before, 0 in final quantized atlas; 5027 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
