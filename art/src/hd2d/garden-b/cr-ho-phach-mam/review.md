# cr-ho-phach-mam — self review

Selected candidate: raw-03.png (ImageGen output 3/8). Earlier outputs raw-01 and raw-02 were retained; pack rejected them because no common scale >=0.6 fit all content within the safe bounds. raw-03 packs at common scale 0.615898.

## Face notes (cell-local coordinates)

face_row_1: eyes=90,136; mouth=96,143; blink=frame2
face_row_2: eyes=90,120; mouth=96,128; blink=frame2
face_row_3: eyes=84,126; mouth=96,137; blink=frame2
face_row_4: eyes=88,122; mouth=96,132; blink=none
face_row_5: eyes=90,137; mouth=96,144; blink=none

## Visual review

Best measured candidate raw-05: 9/10 gates. Gate h fails, plant f4 vs sprout f1 IoU=.5906 (<.80); other gates pass (59 colors; heights 71/73, 105–110, 149–150; width 133; min loop IoU=.8809). Raw-08 cannot be packed: common scale >=.6 cannot fit content. Manual dark 4x shows magenta contour fringe.


## Plant f4 repair — 2026-11-12

Used 4 new ImageGen output(s) where applicable. Selected `raw-10.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.6041313918049441; gates passed 9/10; purple-hued edge count 6533→0. Reference: `reference-sprout-f1.png` SHA-256 `ebfdfea6e96d9131735a14bb95bb1fbc660275eefa362825f6d9ee98891900d8`.

## Repack and review — 2026-11-13

Selected `raw-10.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 6533 before, 0 after. h=.6041; edge 6533→0. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.

## Targeted repair 2026-11-16
Selected raw-16, 4/6 attempts: a–j pass, h=.9231, j=.9165, 58 colors, grow heights 109/112/112/112, ripe 150, width 132. Viewed 4x dark: no distinct magenta fringe observed.

## Current repair round — 2026-11-16 (grow/ripe pixel density)
Selected `raw-21.png` (six-or-fewer new attempts; selected after raw-20 and raw-21), packed through the existing pipeline and measured. All a–j pass: 58 colors; stage heights sprout 75, grow 106, ripe 150 px; max width 130 px; plant/sprout IoU 0.8953; minimum loop IoU 0.9547. Opened `review-4x-dark.png`: grow/ripe now read with finer, more consistent pixel clusters rather than the previous approximately 3× coarse blocks; character remains the amber-vein creature and no detached magenta fringe is apparent. Submitted `ready_for_claude_review`, `approved:false`.
