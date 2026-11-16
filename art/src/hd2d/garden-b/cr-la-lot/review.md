# Visual review — cr-la-lot

Opened the raw-04 sheet and confirmed the shy leaf-cloak design, visible cream face, row 1–3 blink poses at frame 3, harvest fade, and compact sprout. Rows 1–3 use restrained pose changes to preserve loop silhouettes.

## Face notes
face_row_1: eyes = 96,145; mouth = 96,156; blink = frame3
face_row_2: eyes = 96,137; mouth = 96,150; blink = frame3
face_row_3: eyes = 96,111; mouth = 96,127; blink = frame3
face_row_4: eyes = 96,112; mouth = 96,127; blink = none
face_row_5: eyes = 96,145; mouth = 96,156; blink = frame2

## Current task gate record

Opened packed atlas: leaf-cloak silhouette and cream face read clearly; row 1–3 frame 3 are closed-eye blinks; plant resembles sprout.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | crop pivots compared with (96,168), ±1 px |
| f | PASS | heights sprout/grow/ripe=[71, 72, 71, 72]/[100, 101, 100, 100]/[149, 150, 149, 149]; max width=113 px |
| g | PASS | N/A for crop |
| h | PASS | plant/sprout IoU=0.8541 |
| i | PASS | face rows=[1, 2, 3, 4, 5], blink rows=[1, 2, 3] |
| j | PASS | loop min IoU=0.9221 |

**Overall: PASS (10/10 script checks).** `approved:false`; not a Claude approval.


## C04 height margin

The strict measured gate f permits up to 150 px. The C04 prompt additionally asks for ripe <=148 px to leave margin. Current ripe heights are [149, 150, 149, 149] px, so this task-specific margin is **FAIL**; keep blocked pending redraw.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6042 before, 0 in final quantized atlas; 5924 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
