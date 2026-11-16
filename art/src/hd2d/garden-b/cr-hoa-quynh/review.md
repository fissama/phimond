# cr-hoa-quynh — self review

Selected candidate: raw-07.png (ImageGen attempt 7/8). Raw-01 through raw-07 are preserved.

## Face notes (cell-local coordinates)

face_row_1: eyes=92,128; mouth=96,136; blink=frame3
face_row_2: eyes=91,100; mouth=96,109; blink=frame3
face_row_3: eyes=84,75; mouth=96,85; blink=frame3
face_row_4: eyes=84,93; mouth=96,104; blink=none
face_row_5: eyes=92,130; mouth=96,139; blink=none

## Measured gates

- a–e: PASS; 768x960 RGBA, binary alpha, hidden RGB zero; 20/20 unique non-empty frames; all pixels within [16,175]; 56 colors; pivots within ±1.
- f: PASS; stage heights 70/70/70/70, 100/100/100/100, 150/150/150/149 px; max body width 123 px.
- g: N/A (crop).
- h: PASS; plant f4 vs sprout f1 IoU 0.9443.
- i: PASS after face annotation; visible blink at frame 3 in each looping row 1–3.
- j: PASS; minimum loop IoU 0.9488.

## Visual review

10/10 mechanical gates; h=.9483, min loop IoU=.9681. Manual dark 4x shows visible violet/magenta contour fringe.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6392 before, 3394 in final quantized atlas; 4957 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
