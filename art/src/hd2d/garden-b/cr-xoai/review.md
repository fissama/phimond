# cr-xoai review

Face notes: eyes/mouth are centered on the mango-parrot face; sleepy blink in frame 1 and frame 3 of loop rows.

face_row_1: eyes = 88,96; mouth = 96,105; blink = frame1
face_row_2: eyes = 87,94; mouth = 96,104; blink = frame3
face_row_3: eyes = 83,91; mouth = 96,102; blink = frame2
face_row_4: eyes = 84,92; mouth = 96,103; blink = frame3
face_row_5: eyes = 89,97; mouth = 96,106; blink = none

Visual check: opened `review-4x-dark.png` for raw-03. The mango-parrot silhouette, yellow fruit body, green leaf wings/tail and face remain readable, and harvest ends in sparse seed/light remnants. Visible pink/violet fringe remains around the sprite contours at 4×, so the no-magenta visual requirement fails after eight outputs. raw-04 through raw-08 were retained but each failed packing at the minimum common scale, with `No common scale s≥0.6 fits all frames inside safe bounds; redraw required`.

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-02.png | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | FAIL | FAIL | heights 62/89–91/117–120 px; h=0.9176; loop min=0.7008; no face notes at time of initial measurement |
| raw-03.png | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | 59 colors; heights 61–62/89–90/125–126 px; width 115 px; h=0.9079; blink rows 1–3; loop min=0.9125; visual magenta fringe remains |
| raw-04.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-05.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-06.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-07.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-08.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |

Status: `blocked_imagegen_limit`. raw-03 is the selected candidate for audit and its mechanical checks are 10/10, but the atlas is not visually compliant because of the contour fringe. No color or pixel cleanup was applied.


## Edge defringe — 2026-11-12

Repacked from `raw-03.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6054 before, 2596 in final quantized atlas; 5653 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
