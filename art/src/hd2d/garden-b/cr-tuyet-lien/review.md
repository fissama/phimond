# cr-tuyet-lien — self review

Selected candidate: raw-08.png (ImageGen output 8/8).

## Face notes (cell-local coordinates)
face_row_1: eyes=91,136; mouth=96,145; blink=frame3
face_row_2: eyes=91,116; mouth=96,128; blink=frame3
face_row_3: eyes=90,100; mouth=96,114; blink=frame3
face_row_4: eyes=90,99; mouth=96,114; blink=frame2
face_row_5: eyes=91,136; mouth=96,145; blink=frame4

## Visual review
The snow-fox / lotus silhouette is readable and loop poses are stable. Harvest frame 4 retains a small character while snow motes remain sparse. Opened the dark 4x preview; violet/purple contour fringe is visible around the white-blue sprites. This violates the no-magenta visual requirement after 8 outputs, so the asset remains blocked.

## Gate record
Selected raw-08.png. Mechanical gates a–j pass after annotations; see qa.json for measured results. Visual palette inspection fails due contour fringe.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7149 before, 2189 in final quantized atlas; 5764 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
