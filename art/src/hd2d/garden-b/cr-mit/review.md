# Review — cr-mit

## Face notes
face_row_1: eyes = 90,145; mouth = 96,156; blink = frame3
face_row_2: eyes = 90,124; mouth = 96,139; blink = frame3
face_row_3: eyes = 90,96; mouth = 96,112; blink = frame3
face_row_4: eyes = 90,96; mouth = 96,112; blink = none
face_row_5: eyes = 90,145; mouth = 96,156; blink = none

## Measurement rounds

| Source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | FAIL | 60 colors; heights 85–90/114–119/143–150; width140; h=.9284; j=.7643 |
| raw-02.png | FAIL | — | — | — | — | — | — | — | — | — | Pack failed: no common scale s≥0.6 |
| raw-03.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | PASS | PASS | 59 colors; sprout=81–83 (>75); heights grow 93–96, ripe 120–121; width144; h=.9624; loop=.9325 |
| raw-04.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | PASS | PASS | 59 colors; height limits fit, width144 (>140); h=.6516; loop=.8818 |
| raw-05.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | 59 colors; heights 68/98/132; width139; h=.6857; loop=.9668 |
| raw-06.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | 60 colors; heights 68/98/130–131; width138; h=.6919; loop=.9719 |
| raw-07.png | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | FAIL | PASS | PASS | Growth reversed: heights 153/144/117; h=.2368; loop=.9618 |
| raw-08.png | PASS | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | PASS | PASS | 58 colors; heights 69/98/131; width138; h=.6837; loop=.9414 |

Selected raw-06 as best measured candidate. Opened its 4× dark preview: pangolin is readable, but vivid magenta/purple pixels fringe the outline around spikes, face, body and feet; this fails the clean contour style. Gate h also fails at .6919 (<.80). Eight outputs exhausted; no code cleanup or gate changes.


## Plant f4 repair — 2026-11-12

Used 4 new ImageGen output(s) where applicable. Selected `raw-10.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.6799312208302628; gates passed 9/10; purple-hued edge count 7108→2711. Reference: `reference-sprout-f1.png` SHA-256 `ba3a8c9d2a091324ea15817b50eef89186cad6381c2b7bc177e2e3d52660f352`.

## Repack and review — 2026-11-13

Selected `raw-10.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 7108 before, 2711 after. h=.6799; edge 7108→2711. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.

## Targeted repair 2026-11-16
Four outputs raw-13–16. Selected raw-16: a–j script 10/10, h=.9260, j=.9646, 56 colors, width 138. Inspected 4x dark: row 1 has no visible blink, row 5 begins with mature plant, violating visual contract despite annotated i passing. Blocked; fixing those rows exceeds authorized plant f4-only scope.

## Current repair round — 2026-11-16 (plant row only)
Selected `raw-22.png` after six new ImageGen outputs (`raw-17..22`); all raw sheets retained. The plant row now reads seed in soil → cracked seed → small sprout → sprout matching the crop character; h=0.9014. Re-measure: a–e, g–j pass; f fails because sprout row height is 76 px (>75) and maximum body width is 151 px (>140); grow=107 px and ripe=142 px. The requested edit scope did not include the crop rows that produce the f failure, so the atlas remains blocked. The 4× preview also makes the sprout-row blink difficult to distinguish; QA records row-1 frame 3, but this is a visual-review note, not a measured gate failure.
