# Visual review — pot-g4a-lam-su

## Face notes

## Current task gate record

Opened current final: blue-and-white ceramic and floral decoration read; measured result passes.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 59 visible colors |
| e | PASS | pot pivot compared with (96,175), ±1 px |
| f | PASS | N/A for pot |
| g | PASS | min adjacent body IoU=0.9510; joins={'water4_to_wet1': 0.9565178730215188, 'upgrade4_to_idle1': 0.9842718973153756, 'clear4_to_idle1': 0.9888607136388335}; soil darkening=19.40%; measured connected bbox sizes range 151–153w × 98–121h px (water/plant effects may be connected) |
| h | PASS | N/A for pot |
| i | PASS | N/A for pot (no face) |
| j | PASS | loop min IoU=0.0000 |

**Overall: PASS (10/10 script checks).** `approved:false`; not a Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-01.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6327 before, 0 in final quantized atlas; 5913 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
