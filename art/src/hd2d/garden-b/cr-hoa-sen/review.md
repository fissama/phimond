# Review — cr-hoa-sen

## Face notes
Eyes and small mouth are centered in the lotus face; row 1 blinks in frame 3, row 2 in frame 3, row 3 in frame 3.
face_row_1: eyes = 92,140; mouth = 96,151; blink = frame3
face_row_2: eyes = 92,120; mouth = 96,133; blink = frame3
face_row_3: eyes = 92,100; mouth = 96,113; blink = frame3
face_row_4: eyes = 92,99; mouth = 96,113; blink = none
face_row_5: eyes = 92,140; mouth = 96,151; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-02.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-03.png | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | FAIL | heights 71–90/92–115/118–120; width=131; h=0.8338; loop min=0.5896 |
| raw-04.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-05.png | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | h=0.5993; heights 64/89/123; width=112; loop min=0.9582 |
| raw-06.png | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | PASS | sprout=79 px (>75); heights grow 104, ripe 150; h=0.9267; loop min=0.9721 |
| raw-07.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-08.png | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | 60 colors; heights 64–65/86/128; width=126; h=0.9279; loop min=0.9544 |

Visual review: opened `review-4x-dark.png` for raw-08. Lotus character and animation remain readable, but red-violet fringe is visible around the sprite contours. After eight outputs, this remains a visual style blocker. No pixel edits were made.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 4542 before, 1 in final quantized atlas; 4537 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
