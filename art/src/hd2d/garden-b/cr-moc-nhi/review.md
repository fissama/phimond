# Visual review — cr-moc-nhi

Inspected `review-4x-checker.png`, `review-4x-dark.png`, and all five row previews. The shy mushroom-rabbit silhouette, face, cap texture, and friendly harvest rays are readable. The ripe row has a strong happy pose, but sprout/grow/ripe are oversized; the lower roots wander horizontally; plant frame 4 is a much smaller character rather than a close return to sprout frame 1. The first looping row stays sleepy with closed eyes throughout, so it has no clear blink. Visual review: **FAIL**.

Face notes below are approximate cell-local positions from the 4× previews, not machine-detected measurements.
face_row_1: eyes=96,136; mouth=96,147; blink=frame3
face_row_2: eyes=96,102; mouth=96,120; blink=frame3
face_row_3: eyes=96,69; mouth=96,88; blink=frame3
face_row_4: eyes=96,79; mouth=96,96; blink=none
face_row_5: eyes=96,138; mouth=96,149; blink=none

Mechanical review (`qa.json`): a,b,g PASS; c,d,e,f,h,i FAIL. Safe-area violations 6; invariant body colors 0; root-center spread 11.39 px; heights sprout 94–99 px, grow 129–138 px, ripe 155–164 px, max width 159 px; plant4→sprout1 difference 28.71%; harvest4 coverage 1.50%.


## Pipeline v3 round 1 — raw-10 pack

Inspected current `review-4x-checker.png`, `review-4x-dark.png`, `review-pivot-grid.png`, and row previews/GIFs. The design remains the same shy mushroom-rabbit. Row 1 now clearly blinks in frame 3; row 2 blinks in frame 3; row 3 blinks in frame 3. Harvest frame 4 retains a small mushroom creature and visible rays, so it is not near-empty. Plant row frame 4 is still visibly smaller and includes extra soil/mushroom clusters compared with sprout frame 1.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | all pivots within ±1 after pack correction |
| f | FAIL | grow 112–114 px (limit 85–112); max width 141 px (limit 140); sprout 64–66, ripe 149–150 |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.2847 (≥0.80) |
| i | PASS | blink frames: row1 f3, row2 f3, row3 f3; face positions above |
| j | PASS | minimum loop body IoU 0.8741 (≥0.85) |


## Pipeline v3 final — raw-12, independently remeasured 2026-11-10

Opened the current 4× checker and dark previews, pivot grid, and all five row strips. The shy mushroom-rabbit identity, wavy wood-ear ears, cream face, blush, leaf arms, and root feet remain consistent. Sprout is sleepy; grow is curious with a blink; ripe is happy and proud with a blink; harvest f4 still has a recognizable face/body and sparse rays; plant f4 returns closely to sprout f1. Visual review: **PASS for handoff; Claude review pending**.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 65/64–65 / 92–93 / 147–150 px; max width 139 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 mask IoU 0.9030 |
| i | PASS | blink row1 f3, row2 f3, row3 f3; positions above |
| j | PASS | minimum loop body IoU 0.8593 |


## Edge defringe — 2026-11-12

Repacked from `raw-12.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 8359 before, 3912 in final quantized atlas; 7208 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
