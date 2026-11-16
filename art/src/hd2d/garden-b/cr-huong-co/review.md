# Visual review — cr-huong-co

Hương Cô is a gentle shiitake cook spirit: spotted warm-brown cap shaped like a chef hat, cream stem body, leafy root base, small friendly face. The silhouette is clearly mushroom-like and distinct from Mộc Nhĩ's floppy rabbit ears. I inspected `final.png`; crisp pixel clusters, no baked shadow/glow, and the pretend stirring gesture reads in ripe. Harvest frame 4 is sparse rays around a tiny remnant.

Approximate face positions (cell-local):
- face_row_1: eyes=96,142; mouth=96,151; blink=frame3
- face_row_2: eyes=96,126; mouth=96,143; blink=frame3
- face_row_3: eyes=96,89; mouth=96,110; blink=frame3
- face_row_4: eyes=96,113; mouth=96,128; blink=none
- face_row_5: eyes=96,141; mouth=96,151; blink=none

## Packing and gate rounds

| Round/source | a | b | c | d | e | f | g | h | i | j | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 raw-01 | PASS | PASS | PASS | PASS | PASS | FAIL | N/A | FAIL | PASS | PASS | Sprout 81; grow 108–109; ripe 150; width 142; h 0.7802. |
| 2 raw-02 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 73 / 109–110 / 150; width 137; h 0.6687; loop min 0.8551. |
| 3 raw-03 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | h 0.7106; other gates passed. |
| 4 raw-04 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 73–74 / 109 / 150; width 137; h 0.7102. |
| 5 raw-05 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | 60 colors; heights 73 / 109 / 150; width 137; h 0.7159. |
| 6 raw-06 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Heights 72–73 / 107–108 / 149–150; width 135; h 0.7289; loop min 0.8623. |
| 7 raw-07 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | 59 colors; heights 72–73 / 107–108 / 149–150; width 134; h 0.7369. |
| 8 raw-08 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | FAIL | PASS | PASS | Selected. 59 colors; heights 72 / 106–107 / 149–150; width 134; h 0.7158; loop min 0.8649. |

## Visual observations

The face is centered on the stem beneath the cap and remains readable at 48 px. Ripe shows a pretend stirring gesture. Character motion uses eyelids, arms, and cap gestures without changing species identity.

## Targeted plant-frame correction (this task)

Plant f4 was generated as a single frame using the packed sprout f1 from this atlas as the primary reference (`reference-sprout-f1.png`). The selected raw sheet retained the original 19 frames and inserted the generated frame at plant f4; then the unchanged packer and measurement script were run.

| Source | a | b | c | d | e | f | g | h | i | j | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-10 | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS | PASS | PASS | h IoU 0.9505; heights 73 / 107–108 / 149–150 px; width 135; loop min 0.8723. |

The corrected frame keeps the chef-cap, stem, face and root proportions; only the expression changes to a gentle waking yawn. Final 4× image inspected after repacking.


## Edge defringe — 2026-11-12

Repacked from `raw-10.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 8659 before, 7372 in final quantized atlas; 2445 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
