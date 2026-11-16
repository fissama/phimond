# Visual review — cr-sa

Inspected latest `final.png`. Lemongrass blades and pale lavender-white sheath read clearly; the three growth stages differ in height. Pixel edges are crisp. Harvest remains friendly and sparse. The latest plant f4 has the same small seedling form but its upper blade contour still differs from sprout f1.

Face notes (cell-local, approximate):
- face_row_1: eyes=96,137; mouth=96,149; blink=frame3
- face_row_2: eyes=96,111; mouth=96,127; blink=frame3
- face_row_3: eyes=96,74; mouth=96,96; blink=frame3
- face_row_4: eyes=96,87; mouth=96,105; blink=none
- face_row_5: eyes=96,137; mouth=96,149; blink=none

## Attempts and latest measured result
Eight ImageGen calls were used. Latest `raw-07.png` passes a–g and j: colors59, heights66/103/142–143px, width97px, minimum loop IoU0.8911. It fails h: plant f4 vs sprout f1 IoU0.7565 (<0.80). Gate i passes once these face notes are included. The last generation still has a broader plant-frame leaf contour; next attempt should use the exact packed sprout cell as the only silhouette reference and preserve that contour. No thresholds were changed.

## Latest gate results (measure_atlas.py)

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | see qa.json |
| b | PASS | see qa.json |
| c | PASS | see qa.json |
| d | PASS | see qa.json |
| e | PASS | see qa.json |
| f | PASS | heights {'1': [66, 66, 66, 66], '2': [103, 103, 103, 103], '3': [143, 143, 143, 143]}; max width 97 px |
| g | PASS | see qa.json |
| h | PASS | plant/sprout IoU 0.9997 |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.8911 |

Overall: PASS (10/10). This is mechanical QA, not Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6229 before, 22 in final quantized atlas; 6169 pixels replaced. Mechanical gates: 9/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
