# cr-thanh-long — self review

face_row_1: eyes=91,127; mouth=96,134; blink=frame3
face_row_2: eyes=88,82; mouth=96,91; blink=frame3
face_row_3: eyes=77,62; mouth=96,75; blink=frame3
face_row_4: eyes=78,81; mouth=96,91; blink=frame3
face_row_5: eyes=89,139; mouth=96,146; blink=none

The face is centered in the cream face area; row 3 is visibly closed-eye in frame 3. The harvest row reads as a friendly wave followed by sparse flecks. The four crop stages are clearly size-separated and plant f4 repeats sprout f1's body silhouette.

Measured first pack: a–h and j pass; i awaits this annotation. Colors 59; heights 64–66 / 94–95 / 131 px; max width 124 px; plant/sprout IoU .9256; loop minimum .9185. Viewed the generated sheet and packed atlas. Pixel contours are hard stepped; packed atlas has no visible shadow/glow. The raw source contains some accent marks in cells as motion lines, which are intentional animation cues.


Latest source raw-02 was opened at 4× on dark background. Outline is darker and less purple than raw-01, but slight violet fringe remains around some pink fruit edges. Continue color-contour correction if further ImageGen outputs are available.


## Continuation audit — 2026-11-12

Selected packed source is `raw-07.png`; final SHA256 `167c2b3256b541acb09fa44b4b0729b55b6841c2fbdc911de4db7840d194721f`. Mechanical gates: 9/10. Latest independent visual audit: FAIL. Manual dark 4x review shows violet/magenta contour; additionally gate h fails at IoU=.7011.

Status: `blocked_imagegen_limit` after 8 outputs. No further pixel modifications were made.


## Plant f4 repair — 2026-11-12

Used 1 new ImageGen output(s) where applicable. Selected `raw-09.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.980309423347398; gates passed 10/10; purple-hued edge count 6809→612. Reference: `reference-sprout-f1.png` SHA-256 `29279fcb3b637bcd747b422f6b4b554ed2503554ab0d7ae4ea92faa18b2d62ed`.

## Repack and review — 2026-11-13

Selected `raw-09.png`; 10/10 mechanical gates pass. Purple-hued opaque edge pixels: 6809 before, 612 after. h=.9803; edge 6809→612. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.
