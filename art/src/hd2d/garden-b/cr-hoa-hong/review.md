# Visual review — cr-hoa-hong

Opened `review-4x-checker.png` and `preview-row-5.png`. The princess-gai identity, readable face, and seed-to-sprout plant progression are clear. Plant frame 4 now matches sprout frame 1 in silhouette and scale, with a waking expression.

## Face notes
face_row_1: eyes=96,150; mouth=96,159; blink=frame3
face_row_2: eyes=96,133; mouth=96,145; blink=frame3
face_row_3: eyes=96,105; mouth=96,119; blink=frame3
face_row_4: eyes=96,108; mouth=96,121; blink=frame3
face_row_5: eyes=96,148; mouth=96,159; blink=frame2

## Latest repair — 2026-11-11

Plant row 5 was regenerated as seed → sprout; f4 used the current sprout-f1 image as direct ImageGen reference. The first packed pass measured h=0.6619 because plant f4 bbox was 61×55 px vs sprout f1 49×45 px. After reducing only plant f4, final source `raw-10.png` passes all gates.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | pivots within ±1 px |
| f | PASS | sprout 45–46; grow 102; ripe 149–150 px; max width 119 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 mask IoU 0.8823 |
| i | PASS | blink rows 1–3, frame 3 |
| j | PASS | min loop body IoU 0.9216 |

**Overall: PASS 10/10.** Candidate is `ready_for_claude_review`, `approved:false`.


## Edge defringe — 2026-11-12

Repacked from `raw-10.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5778 before, 3184 in final quantized atlas; 5064 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
