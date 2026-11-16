# Review — pot-g3b-sanh-nau

Visual inspection: opened final atlas and row previews. The material and silhouette are distinct; pot has no face and the planting mouth remains visible.

Measured gate summary (latest tools/measure_atlas.py run): see qa.json.

## Latest gate results (measure_atlas.py)

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | see qa.json |
| b | PASS | see qa.json |
| c | PASS | see qa.json |
| d | PASS | see qa.json |
| e | PASS | see qa.json |
| f | PASS | see qa.json |
| g | FAIL | min body IoU 0.9255; transitions {'water4_to_wet1': 0.9790729379686435, 'upgrade4_to_idle1': 0.9540754666308581, 'clear4_to_idle1': 0.968401863479846}; soil darkening -4.05% |
| h | PASS | see qa.json |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.0000 |

Overall: FAIL (9/10). This is mechanical QA, not Claude approval.

## Current task gate record

Opened current final: brown glazed earthenware silhouette is stable; wet soil visibly darker; mechanical result passes.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | pot pivot compared with (96,175), ±1 px |
| f | PASS | N/A for pot |
| g | PASS | min adjacent body IoU=0.9753; joins={'water4_to_wet1': 0.9915312653865092, 'upgrade4_to_idle1': 0.9921044936153621, 'clear4_to_idle1': 0.939721222191452}; soil darkening=18.10%; measured connected bbox sizes range 157–158w × 74–90h px (water/plant effects may be connected) |
| h | PASS | N/A for pot |
| i | PASS | N/A for pot (no face) |
| j | PASS | loop min IoU=0.0000 |

**Overall: PASS (10/10 script checks).** `approved:false`; not a Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-17.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 5362 before, 0 in final quantized atlas; 5303 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
