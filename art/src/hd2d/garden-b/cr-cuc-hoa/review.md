# Visual review — cr-cuc-hoa

Cúc Hoa is a cheerful chrysanthemum girl: layered golden petals read as curly hair around a clear face with blush, leaf arms, and root base. The silhouette is distinct from both approved pilots. I inspected `review-4x-dark.png`; the face and flower layers remain readable, the three loop rows show blinks, and harvest frame 4 resolves to sparse petal/light fragments. Pixel clusters are crisp and hard-edged.

Approximate face positions (cell-local):
- face_row_1: eyes=96,145; mouth=96,157; blink=frame3
- face_row_2: eyes=96,112; mouth=96,128; blink=frame3
- face_row_3: eyes=96,75; mouth=96,94; blink=frame2
- face_row_4: eyes=96,84; mouth=96,101; blink=none
- face_row_5: eyes=96,145; mouth=96,157; blink=none

## Packing and gate rounds

| Round/source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 raw-01 | FAIL | — | — | — | — | — | N/A | — | — | — | Pack rejected: harvest row4 frame2 reached x=14 at s=0.6. |
| 2 raw-02 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | PASS | Ripe width 144 px; other checks passed. |
| 3 raw-03 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | Selected. Sprout 73–75; grow 101; ripe 127–129; width 123; h IoU 0.9356; min loop IoU 0.9105. |

## Current visual inspection

The packed flower reads as a smiling chrysanthemum spirit at native size. Row 1 is sleepy, row 2 curious, row 3 proud and lively, harvest is friendly, and the plant ending returns to the sprout silhouette. No baked glow or shadow is visible.


## Edge defringe — 2026-11-12

Repacked from `raw-03.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7000 before, 3742 in final quantized atlas; 6124 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
