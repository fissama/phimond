# Visual review — cr-huong-duong

Inspected `final.png`. The sunflower lion cub reads as a distinct golden flower character with round cream face and green leaves. Stage sizes visibly progress; pixel clusters are crisp. Row 3 face looks upward; harvest fades to sparse rays.

Face notes (cell-local, approximate):
- face_row_1: eyes=96,137; mouth=96,148; blink=frame2
- face_row_2: eyes=96,110; mouth=96,128; blink=frame3
- face_row_3: eyes=96,76; mouth=96,96; blink=frame2
- face_row_4: eyes=96,88; mouth=96,105; blink=none
- face_row_5: eyes=96,137; mouth=96,148; blink=none

Latest mechanical measurements are in `qa.json`; first raw sheet f failed height/width slightly; selected redraw `raw-04.png` corrected f.


## Edge defringe — 2026-11-12

Repacked from `raw-04.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5730 before, 0 in final quantized atlas; 5677 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
