# Review — cr-hoa-dao

## Face notes
face_row_1: eyes = 90,144; mouth = 96,155; blink = frame3
face_row_2: eyes = 90,122; mouth = 96,137; blink = frame3
face_row_3: eyes = 90,94; mouth = 96,110; blink = frame3
face_row_4: eyes = 90,94; mouth = 96,110; blink = none
face_row_5: eyes = 90,144; mouth = 96,155; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 |
| raw-02.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 |
| raw-03.png | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | FAIL | PASS | FAIL | 60 colors; pivot x=97.26; heights 67–71/89–99/123–129; width116; h=.4434; j=.7624 |
| raw-04.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | 60 colors; heights 68–72/88–97/121–128; width114; h=.5076; j=.7870 |
| raw-05.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | 60 colors; heights 70–73/90–99/122–129; width115; h=.9185; j=.7996 |
| raw-06.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | PASS | FAIL | 59 colors; ripe f4=119; h=.4046; j=.8128 |
| raw-07.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | 58 colors; heights 70–71/90–93/122–127; width114; h=.9061; j=.8163 |
| raw-08.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | 59 colors; heights 70–71/91–92/121–125; width113; h=.4185; j=.8410 |

Selected raw-07 as the best candidate: nine gates pass; loop IoU is .8163 (<.85). Opened the 4× dark preview: the fawn and peach blossoms read cleanly, outlines are dark warm brown, and no obvious separate magenta fringe dominates. Eight outputs exhausted; blocker is j. No code pixel edits or gate changes.

## Repack and review — 2026-11-13

Selected `raw-12.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 8464 before, 3747 after. loop min .8707 passes; sprout 76 px fails f; edge 8464→3747. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.


## Targeted sprout repair — 2026-11-16

| Raw | a | b | c | d | e | f | g | h | i | j | Measurements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-13 | P | P | P | P | P | F | P | F | P | P | sprout 59–62; ripe min 119; h=.7658; 58 colors; j=.8518 |
| raw-14 | P | P | P | P | P | P | P | F | P | P | sprout 67; ripe 121–124; h=.7940; 59 colors; j=.8618 |
| raw-15 | P | P | P | P | P | P | P | F | P | P | sprout 65–66; ripe 120–124; h=.7596; 59 colors; j=.8614 |
| raw-16 | P | P | P | P | P | P | P | P | P | P | sprout 69–70; grow 96–97; ripe 122–125; width 117; 59 colors; h=.8361; j=.8707 |

Opened `review-4x-dark.png`: fawn sprites and warm outlines read clearly; no distinct detached magenta fringe is visible. Current candidate passes all 10 mechanical gates.
