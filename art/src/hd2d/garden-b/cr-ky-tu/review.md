# Visual and face review — cr-ky-tu best candidate raw-03

Opened the packed atlas and 4× previews. The curved pale-green branch and red-orange goji-birds read clearly; each ripe berry-bird has a small face. Stage progression and sparse harvest motes are visible. Contours retain slight pink/violet fringe at 4×. Face positions (approximate, cell-local):
face_row_1: eyes=96,142; mouth=96,151; blink=frame1
face_row_2: eyes=96,119; mouth=96,132; blink=frame3
face_row_3: eyes=96,85; mouth=96,104; blink=frame2
face_row_4: eyes=96,83; mouth=96,100; blink=none
face_row_5: eyes=96,143; mouth=96,152; blink=none

## Repack and review — 2026-11-13

Selected `raw-03.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 7441 before, 1853 after. width 144 px fails f; edge 7441→1853. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.


## Targeted width repair — 2026-11-16

| Raw | a | b | c | d | e | f | g | h | i | j | Measurements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-13 | P | P | P | P | P | F | P | P | P | P | max width 120; ripe 118–119; h=.8379; j=.9006; common scale .6231 |
| raw-14 | P | P | P | P | P | P | P | P | P | P | max width 128; ripe 120–121; h=.8336; j=.8614; 60 colors |

Opened `review-4x-dark.png`: berry-birds and pale-green branch read clearly; outlines look dark brown and no separate magenta fringe is apparent. All ten mechanical gates pass.
