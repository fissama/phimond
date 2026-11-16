# Review — cr-linh-mach-mam

Final candidate selected from `raw-06.png` after 8 ImageGen outputs. `raw-06.png` is the best mechanically passing candidate. The packed 4× checker preview was opened and visually inspected. Character silhouette is clear and readable; stages progress from tiny seedling to mature stone spirit. After opening the final dark 4× preview, a conspicuous violet/magenta pixel fringe is visible on the sprite contours in rows 1–5. The 10 mechanical gates pass, but the no-magenta visual requirement fails. This remains blocked after 8 outputs; not approved.

## Face notes (cell-local coordinates)
face_row_1: eyes=90,137; mouth=96,146; blink=frame3
face_row_2: eyes=88,113; mouth=96,126; blink=frame3
face_row_3: eyes=88,81; mouth=96,96; blink=frame2
face_row_4: eyes=89,112; mouth=96,125; blink=none
face_row_5: eyes=90,137; mouth=96,146; blink=none

## Measurement rounds

| Raw | Result | Key measurements |
|---|---|---|
| raw-01 | 8/10 | 60 colors; heights sprout 70–75, grow 102–106, ripe 121–135; width 116; plant IoU .8652; loop min .7128; face notes not yet present. |
| raw-02 | 9/10 | 60 colors; heights 69–73/101–102/120–134; width 112; h=.8873; loop .7431. |
| raw-03 | 9/10 | 60 colors; heights 81/104/150; width 128; h=.9229; loop .9580; sprout too tall. |
| raw-04 | 10/10 | 60 colors; heights 61/104/150; width 128; h=.9618; loop .9645; visual contour fringe. |
| raw-05 | 9/10 | 60 colors; heights 84/106–112/136–141; width 160; h=.8734; loop .8760; sprout too tall and width too large. |
| raw-06 | 10/10 | Selected. 60 colors; heights 60/103/150; width 128; h=.9560; loop .9735; visual contour fringe. |
| raw-07 | 8/10 | 60 colors; heights 80–81/118/148; width 136; h=.7752; loop .9370. |
| raw-08 | 8/10 | 60 colors; heights 71–72/107–109/141; width 160; h=.6235; loop .9249. |

Visual check notes: row 1 reads as a sleepy stone seedling, row 2 as a curious larger sprout, row 3 as the mature guardian with an orbiting golden ring. Harvest has a wave and sparse final rays. The plant row starts as a stone seed and ends as the small sprout. Recheck the dark 4× preview for outline color after export.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 8169 before, 1343 in final quantized atlas; 7470 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
