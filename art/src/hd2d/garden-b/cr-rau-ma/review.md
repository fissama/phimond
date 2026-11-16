# Visual review — cr-rau-ma

Rau Má is a calm sleepy frog spirit with two round centella leaves as side ears, cool greens, cream face/belly, and a low leaf base. Packed character is legible at 4× and distinct from the approved mint cat and mushroom rabbit. I inspected `final.png` visually.

Approximate face positions (cell-local):
- face_row_1: eyes=96,133; mouth=96,143; blink=frame4
- face_row_2: eyes=96,124; mouth=96,141; blink=frame3
- face_row_3: eyes=96,87; mouth=96,108; blink=frame2
- face_row_4: eyes=96,100; mouth=96,118; blink=none
- face_row_5: eyes=96,133; mouth=96,143; blink=none

## Pipeline rounds

| Round/source | a | b | c | d | e | f | g | h | i | j | Measurements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 raw-02 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | FAIL | Heights 81 / 99 / 112–113; width 135; h 0.8756; loop min 0.8498. |
| 2 raw-03 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | FAIL | Heights 77–78 / 100 / 126–128; width 139; h 0.8870; loop min 0.8496. |
| 3 raw-04 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | Heights 74 / 100 / 126–127; width 139; h 0.8365; loop min 0.8612. |
| 4 raw-06 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | Selected. Heights 74 / 100 / 125–127; width 139; h 0.9575; loop min 0.8536. |

## Visual observations

Ripe uses a meditation pose and tiny water breath bubbles. Harvest is gentle and ends in sparse pixels. The selected plant f4 was a single-frame ImageGen sprite using the packed sprout f1 as its primary reference; the other 19 packed frames were retained in the assembled source for the unchanged packer. No baked glow or shadow.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 8074 before, 4481 in final quantized atlas; 4569 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
