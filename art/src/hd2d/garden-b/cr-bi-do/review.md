# Visual review — cr-bi-do

Visual inspection: opened the 4×5 final atlas. Character faces are visible at native scale and each repeating growth row includes a closed-eye blink.

## Face notes
face_row_1: eyes = 96,148; mouth = 96,158; blink = frame3
face_row_2: eyes = 96,134; mouth = 96,146; blink = frame3
face_row_3: eyes = 96,116; mouth = 96,130; blink = frame3
face_row_4: eyes = 96,112; mouth = 96,126; blink = none
face_row_5: eyes = 96,148; mouth = 96,158; blink = frame3

## Current task gate record

Opened packed atlas: face is readable; blink is visible in frame 3 of rows 1–3; harvest ends in sparse motes.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | crop pivots compared with (96,168), ±1 px |
| f | PASS | heights sprout/grow/ripe=[62, 62, 62, 62]/[100, 100, 100, 100]/[132, 132, 132, 132]; max width=114 px |
| g | PASS | N/A for crop |
| h | PASS | plant/sprout IoU=0.8839 |
| i | PASS | face rows=[1, 2, 3, 4, 5], blink rows=[1, 2, 3] |
| j | PASS | loop min IoU=0.8946 |

**Overall: PASS (10/10 script checks).** `approved:false`; not a Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7023 before, 1630 in final quantized atlas; 6558 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
