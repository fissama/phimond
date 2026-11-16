# Review — cr-tam-that

## Face notes
face_row_1: eyes = 90,145; mouth = 96,155; blink = frame3
face_row_2: eyes = 90,125; mouth = 96,140; blink = frame3
face_row_3: eyes = 90,103; mouth = 96,116; blink = frame3
face_row_4: eyes = 90,105; mouth = 96,118; blink = none
face_row_5: eyes = 90,145; mouth = 96,155; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-02.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | PASS | FAIL | 56 colors; heights 66/79–82/96–99; width 115; h=.9068; loop=.8494 |
| raw-03.png | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL | 57 colors; pivot failure at harvest row4 frame3 (82.86,96); heights 70/98–99/129; width 138; h=.9133; loop=.8111 |
| raw-04.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 fits all frames |
| raw-05.png | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | FAIL | 59 colors; pivot failure harvest row4 frame3 (86.83,90); heights 68–75/92–101/134–142; width 146; h=.9042; loop=.8330 |
| raw-06.png | PASS | PASS | PASS | PASS | FAIL | FAIL | PASS | PASS | PASS | PASS | 59 colors; pivot failure harvest row4 frame3 (72.52,140); sprout=86 (>75); h=.9400; loop=.8850 |
| raw-07.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | 57 colors; heights 60–63/102/137–140; width=139; h=.7095; min loop=.8451 |
| raw-08.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | PASS | FAIL | 58 colors; heights 60–62/105/140–144; width=142; h=.6681; loop=.8131 |

Selected raw-07 because it passes eight gates, more than raw-08. Latest `final.png`, `qa.json`, and previews were regenerated from raw-07. Opened both 4× checker and dark previews: character is legible and palette coherent, but thin magenta/purple fringe is visible along multiple contours. It remains a visual blocker after all eight outputs. Gates h (IoU .7095 vs .80) and j (minimum loop IoU .8451 vs .85) also fail. No pixel cleanup or threshold changes.


## Plant f4 repair — 2026-11-12

Used 4 new ImageGen output(s) where applicable. Selected `raw-10.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.6798137496576281; gates passed 9/10; purple-hued edge count 5369→389. Reference: `reference-sprout-f1.png` SHA-256 `403de7eec1ea9c88284afd5efcfea554471f1aa3617df1cb8ab32edd658af811`.

## Repack and review — 2026-11-13

Selected `raw-10.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 5369 before, 389 after. h=.6798; j=.8593; edge 5369→389. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.

## Targeted repair 2026-11-16
Six outputs raw-13–18. Selected raw-17: a–j 10/10, h=0.9024, j=0.8525, 59 colors, max width 132; inspected dark preview and visible isolated magenta fringe remains along outlines. Blocked visually. Raw-18 h=0.9176 but j=0.8431 fails.
