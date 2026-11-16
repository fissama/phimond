# Visual review — cr-khoai-lang

Khoai Lang is a sweet-potato piglet spirit: purple tuber body, heart-shaped vine, pink pig nose, cream paws and blush. I inspected the packed atlas; the character is cute, readable and distinct from the pilots.

Approximate face positions (cell-local):
- face_row_1: eyes=96,137; mouth=96,148; blink=frame1
- face_row_2: eyes=96,127; mouth=96,145; blink=frame3
- face_row_3: eyes=96,96; mouth=96,115; blink=frame2
- face_row_4: eyes=96,100; mouth=96,118; blink=none
- face_row_5: eyes=96,137; mouth=96,148; blink=none

## Pipeline rounds

| Round/source | a | b | c | d | e | f | g | h | i | j | Measurements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 raw-02 | FAIL | — | — | — | — | — | N/A | — | — | — | Pack: no common scale ≥0.6 fits; harvest had pixels below the root pivot. |
| 2 raw-03 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | FAIL | Heights 86 / 96 / 115–116; width 142; h 0.8755; loop min 0.8436. |
| 3 raw-04 | FAIL | — | — | — | — | — | N/A | — | — | — | Pack: no common scale ≥0.6 fits; isolated/out-of-safe pixels remained. |
| 4 raw-05 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 66–68 / 94–95 / 125–126; width 135; h 0.6711; loop min 0.8649. |
| 5 raw-07 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | FAIL | Target-frame pass before final full-sheet revision: h 0.8904, loop min 0.8288. |
| 6 raw-08 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | FAIL | PASS | FAIL | Heights 65–67 / 94 / 124–125; width 141; h 0.6611; loop min 0.8275. |
| 7 raw-09 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 67–69 / 95 / 124; width 138; h 0.6849; loop min 0.8511. |
| 8 raw-10 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | Selected. Heights 67–69 / 95 / 124–125; width 138; h 0.9188; loop min 0.8511. |

## Visual observations

Ripe frames hug the tuber belly and sniff; a tiny drool accent is present. Harvest is friendly and ends with sparse rays. Plant f4 was generated from the packed sprout f1 reference and inserted into the selected raw atlas before running the unchanged packer. No baked shadow or glow.


## Edge defringe — 2026-11-12

Repacked from `raw-10.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 10113 before, 4456 in final quantized atlas; 7757 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
