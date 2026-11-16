# Visual review — cr-nam-rom

Inspected `final.png` at native atlas view. The mushroom-cap farmer reads clearly; sprout, juvenile and ripe forms grow in three distinct sizes. Pixel clusters are crisp and the cream/straw/gray-brown palette is coherent. The ripe action varies the arm and face; cap remains stable. Harvest ends as a friendly sparse effect.

Face notes (cell-local, approximate):
- face_row_1: eyes=96,137; mouth=96,147; blink=frame3
- face_row_2: eyes=96,111; mouth=96,126; blink=frame3
- face_row_3: eyes=96,72; mouth=96,91; blink=frame3
- face_row_4: eyes=96,83; mouth=96,98; blink=none
- face_row_5: eyes=96,137; mouth=96,147; blink=none

## Latest gate measurements
The first selected sheet `raw-03.png` measured f=FAIL only on grow height (115 px) and i was pending visual notes. Redraw `raw-04.png` corrected grow height. Latest result is recorded in `qa.json`; rerun confirms all a–j pass.


## Edge defringe — 2026-11-12

Repacked from `raw-04.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5505 before, 0 in final quantized atlas; 5244 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
