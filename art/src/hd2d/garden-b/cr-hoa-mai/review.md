# Review — cr-hoa-mai

## Face notes
face_row_1: eyes=96,139; mouth=96,149; blink=frame3
face_row_2: eyes=96,107; mouth=96,126; blink=frame3
face_row_3: eyes=96,79; mouth=96,99; blink=frame2
face_row_4: eyes=96,72; mouth=96,92; blink=none
face_row_5: eyes=96,139; mouth=96,150; blink=none

## Visual review — raw-01
Opened `review-4x-dark.png`. The golden plum blossom and branch swallow reads as a friendly flower-bird; the five-petal wings, buds, plain red envelope, and stage progression are clear. Harvest ends in sparse blossom motes. A pink/violet fringe is visible around contours and soil pixels; visual style does not yet pass.

## Final candidate review — raw-02

The packed 4× dark atlas was inspected. The flower-swallow, golden five-petal wings, branch body, green buds, red envelope and sparse harvest ending remain readable. All mechanical gates pass. A visible pink/violet fringe persists at sprite boundaries after eight ImageGen outputs, so the no-magenta visual requirement remains blocked.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 75 / 103 / 125 px; max width 135 px |
| g | N/A | crop |
| h | PASS | plant f4 vs sprout f1 IoU=0.8184 |
| i | PASS | blink row1 f3, row2 f3, row3 f2; face notes above |
| j | PASS | minimum loop body IoU=0.8937 |

Status: blocked on visible magenta contour fringe after 8 ImageGen outputs. Best measured h is only 0.0184 above threshold and sprout height is exactly at 75 px.


## Edge defringe — 2026-11-12

Repacked from `raw-02.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7471 before, 0 in final quantized atlas; 7392 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
