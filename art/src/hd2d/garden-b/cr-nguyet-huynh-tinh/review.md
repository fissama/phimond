# cr-nguyet-huynh-tinh — self review

Selected candidate: raw-08.png (ImageGen output 8/8).

## Face notes (cell-local coordinates)
face_row_1: eyes=91,136; mouth=96,146; blink=frame3
face_row_2: eyes=91,118; mouth=96,128; blink=frame3
face_row_3: eyes=88,105; mouth=96,115; blink=frame3
face_row_4: eyes=88,104; mouth=96,114; blink=frame2
face_row_5: eyes=91,137; mouth=96,146; blink=frame4

## Visual review
Opened `review-4x-dark.png` and `review-4x-checker.png`. Shape progression is readable; the shy face and closed-eye frames are visible, and the harvest row fades to sparse motes. A thin violet/magenta fringe remains around the sprite contours on the dark preview. This fails the no-magenta visual requirement; keep blocked despite passing mechanical gates.

## Gate record
Output 8 of 8 selected. Mechanical c, e, f, h, j pass; after face annotations are recorded, a–j are expected to pass. See `qa.json` for measurements.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5660 before, 2403 in final quantized atlas; 5300 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
