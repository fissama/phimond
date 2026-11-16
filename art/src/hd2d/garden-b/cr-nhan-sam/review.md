# cr-nhan-sam — self review

Selected source: `raw-07.png` (ImageGen output 8/8). Raw outputs `raw-01.png` through `raw-07.png` and `sprout-reference.png` are retained.

## Face notes (cell-local pixel coordinates)

face_row_1: eyes=89,126; mouth=96,132; blink=frame3
face_row_2: eyes=90,84; mouth=96,92; blink=frame3
face_row_3: eyes=83,67; mouth=96,76; blink=frame3
face_row_4: eyes=83,85; mouth=96,93; blink=frame3
face_row_5: eyes=92,140; mouth=96,146; blink=none

Eyes and mouths are small, readable facial features on the ginseng child. Rows 1–3 visibly close both eyes in frame 3. Plant frame 4 repeats the small berry-capped sprout silhouette with a closed-eye smile.

## Measured gates

Latest `measure_atlas.py` result for selected raw-07: a–h and j pass; i is pending remeasurement after these face annotations. Measurements: 58 colors; heights sprout 71/71/71/71, grow 95/95/95/95, ripe 142/141/140/141 px; max width 121 px; plant f4 vs sprout f1 IoU 0.9186; minimum loop IoU 0.9321. No pixels outside safe area; 20/20 distinct populated frames.

## Visual review

Viewed `final.png` at atlas scale. Character silhouettes are centered and bottom anchored; the ripe row reads substantially larger than sprout and grow. The harvest row transitions to sparse friendly flecks. No baked shadow or glow is visible. The raw has a clean magenta key background; packing removes that key. Overall sprite contour remains slightly warm/red at some edges, but no opaque magenta fringe is apparent in the packed view.


## Continuation audit — 2026-11-12

Selected packed source is `raw-07.png`; final SHA256 `8201a77aa17bf9ea97c609042dc4f37bce0189ac2e106504f451b818fd1bc393`. Mechanical gates: 10/10. Latest independent visual audit: FAIL. Manual dark 4x review shows violet/magenta contour despite all mechanical gates passing.

Status: `blocked_imagegen_limit` after 8 outputs. No further pixel modifications were made.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5423 before, 0 in final quantized atlas; 5013 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
