# Review — cr-dua

## Face notes
face_row_1: eyes = 88,145; mouth = 96,157; blink = frame3
face_row_2: eyes = 88,125; mouth = 96,140; blink = frame3
face_row_3: eyes = 88,95; mouth = 96,110; blink = frame3
face_row_4: eyes = 88,95; mouth = 96,110; blink = none
face_row_5: eyes = 88,145; mouth = 96,157; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 |
| raw-02.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | FAIL | 60 colors; heights 88–95/111–119/145–150; width126; h=.9500; j=.8094 |
| raw-03.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 |
| raw-04.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 |
| raw-05.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 60 colors; heights 59–60/97–98/150; width139; h=.8007; j=.9500 |
| raw-06.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 59 colors; heights 57–60/96–97/149–150; width137; h=.8021; j=.8676 |
| raw-07.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 60 colors; heights 58–60/95–97/150; width138; h=.8307; j=.8766 |
| raw-08.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: key failure, row3 frame1 largest component 47,052 px |

Selected raw-07. Opened its 4× dark preview: silhouette and animation read clearly, but magenta/purple fringe remains visible along the body, leaves and feet. This is a visual style blocker after eight outputs; do not clean by code. Mechanical result is 10/10.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7449 before, 0 in final quantized atlas; 7158 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
