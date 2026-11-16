# Visual review — cr-khoai-mon

Opened raw-02 sheet and confirmed baby taro-elephant identity, tiny face, leaf ears, distinct growth silhouettes, and frame-3 blink in repeating rows 1–3. Harvest is a friendly wave and fade.

## Face notes
face_row_1: eyes = 96,148; mouth = 96,159; blink = frame3
face_row_2: eyes = 96,133; mouth = 96,148; blink = frame3
face_row_3: eyes = 96,112; mouth = 96,128; blink = frame3
face_row_4: eyes = 96,112; mouth = 96,128; blink = none
face_row_5: eyes = 96,148; mouth = 96,159; blink = frame3

## Current task gate record

Opened latest packed final: taro-elephant identity reads clearly; ripe is visibly taller than grow; seedling matches sprout f1; loop frames are stable and include blinks.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | crop pivots compared with (96,168), ±1 px |
| f | PASS | heights sprout=[67,67,67,67], grow=[100,101,100,100], ripe=[130,130,130,130] px; max width=131 px |
| g | PASS | N/A for crop |
| h | PASS | plant/sprout IoU=0.9336 |
| i | PASS | face rows=[1, 2, 3, 4, 5], blink rows=[1, 2, 3] |
| j | PASS | loop minimum IoU=0.8661 |

**Overall: PASS (10/10 script checks).** `approved:false`; pending Claude review.

**Packing note:** raw-02 through raw-04 did not pack within safe bounds. New ImageGen sheets raw-05 and raw-06 were created; the common scale and zero clipping are recorded in qa.json. Raw-06 SHA256: `e05bad957390bb5179d32410eb6613e6e1fd1b5fe07aa6688cef6087bcfc7714`.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 11340 before, 9433 in final quantized atlas; 5429 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
