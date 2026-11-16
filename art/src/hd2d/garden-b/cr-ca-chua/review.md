# Visual review — cr-ca-chua

Cà Chua is a cheerful red tomato spirit with a five-point green calyx hat, round cheeks and a friendly face. I inspected the packed atlas; the fruit silhouette reads clearly and is distinct from earlier plants. Harvest frame 4 has a dithered fade and should be checked for sparsity during review.

Approximate face positions (cell-local):
- face_row_1: eyes=96,137; mouth=96,148; blink=frame1
- face_row_2: eyes=96,127; mouth=96,144; blink=frame4
- face_row_3: eyes=96,96; mouth=96,117; blink=frame2
- face_row_4: eyes=96,101; mouth=96,119; blink=none
- face_row_5: eyes=96,137; mouth=96,148; blink=none

## Pipeline rounds

| Round/source | a | b | c | d | e | f | g | h | i | j | Measurements |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 raw-02 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | FAIL | Heights 97 / 125 / 145–147; width 129; h 0.9012; loop min 0.8326. |
| 2 raw-03 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | PASS | PASS | PASS | Heights 79–80 / 111–112 / 132–134; width 112; h 0.8983; loop min 0.9354. |
| 3 raw-04 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 73 / 111–112 / 132–133; width 112; h 0.7918; loop min 0.9217. |
| 4 raw-06 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | Selected. Heights 73 / 111–112 / 132–133; width 112; h 0.9612; loop min 0.9217. |

## Visual observations

Ripe poses suggest rolling via leaf-arm and facial movement while keeping a round tomato body. Harvest is friendly; frame 4 is a compact dithered dissolve, though visually denser than a few sparse rays. The selected plant f4 was generated from the packed sprout f1 reference, then inserted in the raw atlas and repacked. No pain or scary expression; no baked glow or shadow.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5845 before, 0 in final quantized atlas; 5630 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
