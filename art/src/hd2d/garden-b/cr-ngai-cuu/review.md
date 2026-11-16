# Visual review — cr-ngai-cuu

## Manual inspection

Opened `review-4x-checker.png`, `review-4x-dark.png`, `review-pivot-grid.png`, and all five current row previews/GIFs. Creature silhouette and faces read as a silver-gray mugwort lamb; sprout/grow/ripe stages are clearly distinct, harvest waves and ends with sparse rays, plant begins at seed and returns to a sprout. The fixed pivots align. However, opaque violet/magenta fringe pixels remain on sprite contours, visible against both dark and checker backgrounds. This violates the no-magenta style requirement; visual review is **FAIL**, so the asset is blocked despite passing mechanical gates.

Face notes are approximate cell-local positions from the opened row previews:
face_row_1: eyes=96,137; mouth=96,147; blink=frame1
face_row_2: eyes=96,105; mouth=96,120; blink=frame3
face_row_3: eyes=96,69; mouth=96,93; blink=frame2
face_row_4: eyes=96,94; mouth=96,108; blink=none
face_row_5: eyes=96,137; mouth=96,147; blink=none

## Attempts and gate records

| Source | Outcome |
|---|---|
| raw-01 | Pack failed at common scale 0.6 due to detached row 4 frame 2 pixels outside safe bounds. |
| raw-02 | Packed; max width 147 px, above 140. |
| raw-03 | 9/10; sprout 78–79 px, grow 117 px, max width 107; stages 1–2 exceeded limits. |
| raw-04 | 9/10; heights 64/117/142 px; h IoU 0.7785. |
| raw-05 | 9/10; heights 63/98/141 px; h IoU 0.7845. |
| raw-06 | 9/10; heights 63/97–98/141 px; h IoU 0.7983. |
| raw-07 | 10/10; 63/97/139 px, width 107 px, h 0.8175, loop min 0.9426. Purple-like opaque pixels: 16603. |
| raw-08 (selected) | 10/10; 65/100/142 px, width 115 px, h 0.8082, loop min 0.9307. Purple-like opaque pixels: 4856. Visual style still fails; 8 attempts exhausted. |

Current `qa.json` contains the unchanged mechanical measurements from `measure_atlas.py` plus the separate visual-review failure. No approval is assigned.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5734 before, 0 in final quantized atlas; 5607 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
