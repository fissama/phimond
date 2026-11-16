# Visual review — cr-dia-hoang

Design: hardworking Rehmannia mole-root spirit, cream root body, wrinkled olive rosette, pink-purple bell flower, small pink nose. The packed sheet reads clearly at native resolution; forms and hard pixel clusters match the approved pilot style. I inspected `final.png` directly. Rows 1–3 show expression changes and small arm/leaf gestures; row 4 waves before sparse rays; plant frame 4 returns to a sprout-like silhouette.

Face notes in cell-local coordinates (approximate eye center; mouth center):
- face_row_1: eyes=96,142; mouth=96,151; blink=frame3
- face_row_2: eyes=96,128; mouth=96,143; blink=frame3
- face_row_3: eyes=96,91; mouth=96,111; blink=frame3
- face_row_4: eyes=96,105; mouth=96,123; blink=none
- face_row_5: eyes=96,142; mouth=96,151; blink=none

## Packing and gate rounds

| Round/source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 raw-01 | FAIL | — | — | — | — | — | — | — | — | — | No common scale ≥0.6 fit all pixels inside safety bounds. |
| 2 raw-02 | FAIL | — | — | — | — | — | — | — | — | — | No common scale ≥0.6 fit all pixels inside safety bounds. |
| 3 raw-03 | FAIL | — | — | — | — | — | — | — | — | — | Harvest row 4 frame 3 had effects below pivot; no safe common scale. |
| 4 raw-04 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | FAIL | FAIL | FAIL | 6/10; sprout 75–77 px, plant/sprout IoU 0.7627; face annotations absent at measurement. |
| 5 raw-05 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | FAIL | PASS | 8/10; sprout 93–96 px exceeds 75; plant/sprout IoU 0.8688; loop IoU min 0.8877. |
| 6 raw-06 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | FAIL | PASS | PASS | Heights sprout 75,77,75,75; h IoU 0.6606; loop min 0.8930. |
| 7 raw-07 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 73–75 / 98 / 134–137; width 138; h IoU 0.6539; loop min 0.8815. |
| 8 raw-08 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Selected. Heights 73–75 / 97 / 134–135; width 136; h IoU 0.6767; loop min 0.8793. |

## Current visual inspection

The eyes and tiny mouth remain readable at 48 px. Face sits on the cream root body, pink nose above the mouth. Sprout frames are visibly shorter than grow/ripe; ripe flower remains the tallest stage. Harvest has a friendly wave and sparse final pose. No scary or painful expression. The remaining failure is plant frame 4 silhouette similarity: all eight redraws remain below the 0.80 threshold, with the selected round at 0.6767. Suggested next attempt: treat sprout f1 as a near-duplicate pose for plant f4, changing only eyelids/mouth and matching the outer leaf/bell/root silhouette.
