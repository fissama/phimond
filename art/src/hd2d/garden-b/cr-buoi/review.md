# Review — cr-buoi

## Face notes
Eyes and mouth are centered on the pomelo face. Each looping row includes a blink.
face_row_1: eyes = 88,144; mouth = 96,155; blink = frame2
face_row_2: eyes = 88,120; mouth = 96,133; blink = frame2
face_row_3: eyes = 88,84; mouth = 96,101; blink = frame2
face_row_4: eyes = 88,84; mouth = 96,101; blink = none
face_row_5: eyes = 88,144; mouth = 96,155; blink = none

## Measurement and visual review

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed; likely key failure row 3 frame 1; component 43,682 px |
| raw-02.png | FAIL | — | — | — | — | — | — | — | — | — | No common scale s≥0.6 fits all frames |
| raw-03.png | FAIL | — | — | — | — | — | — | — | — | — | No common scale s≥0.6 fits all frames |
| raw-04.png | FAIL | — | — | — | — | — | — | — | — | — | No passing packed candidate recorded |
| raw-05–07.png | FAIL | — | — | — | — | — | — | — | — | — | No passing candidate selected; retained as raw history |
| raw-08.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 51 colors; heights 68/105–106/149–150; width 131; h=0.9254; loop min=0.9042 |

Opened `review-4x-dark.png`: the pomelo sprite is readable and compact, but bright magenta/pink pixels visibly fringe the dark outline around leaves, body and feet. This violates the clean contour/style requirement. After eight ImageGen outputs, visual review remains blocked; no code-based cleanup was performed.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 3757 before, 0 in final quantized atlas; 3755 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
