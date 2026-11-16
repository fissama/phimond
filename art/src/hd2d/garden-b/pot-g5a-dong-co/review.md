# Visual review — pot-g5a-dong-co

## Face notes

## Current task gate record

Opened latest packed final: the patinated green-bronze body and drum motif read clearly; soil is visibly darker in the wet row. Body remains steady across frames.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | pot pivot compared with (96,175), ±1 px |
| f | PASS | N/A for pot |
| g | PASS | min adjacent body IoU=0.9529; joins={'water4_to_wet1': 0.9860, 'upgrade4_to_idle1': 0.9838, 'clear4_to_idle1': 0.9679}; soil darkening=15.15%; body bbox 157×99 px |
| h | PASS | N/A for pot |
| i | PASS | N/A for pot (no face) |
| j | PASS | loop min IoU=0.0000 |

**Overall: PASS (10/10 script checks).** `approved:false`; pending Claude review. Soil darkening and adjacent body IoU are close to the minimum thresholds. Raw-02 SHA256: `cf2aa8b47262f0fc33c37eccfc393dcc1a4d1cbd7de4d231dafdbf6c2dc87aa2`.


## Edge defringe — 2026-11-12

Repacked from `raw-02.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7131 before, 730 in final quantized atlas; 6558 pixels replaced. Mechanical gates: 9/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
