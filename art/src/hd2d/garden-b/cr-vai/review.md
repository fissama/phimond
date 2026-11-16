# cr-vai — self review

Selected candidate: raw-01.png (ImageGen attempt 1/8).

## Face notes (cell-local coordinates)

face_row_1: eyes=91,133; mouth=96,140; blink=frame3
face_row_2: eyes=90,110; mouth=96,119; blink=frame3
face_row_3: eyes=82,82; mouth=96,95; blink=frame2
face_row_4: eyes=84,103; mouth=96,114; blink=none
face_row_5: eyes=91,132; mouth=96,140; blink=none

## Visual review

9/10 gates. Gate f fails: sprout 79–80 px (limit 45–75), grow 116–119 px (limit 85–112); ripe 148–150 px, width 139 px, h=.9290, min loop IoU=.9405. Manual dark preview shows magenta/pink contour fringe.

## Repack and review — 2026-11-13

Selected `raw-10.png`; 10/10 mechanical gates pass. Purple-hued opaque edge pixels: 5558 before, 0 after. all gates pass; heights 74–75/108/147–150; width 137; edge 5558→0. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.
