# Review — pot-g1b-thung-tre

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
| g | PASS | min body IoU 0.9532; transitions {'water4_to_wet1': 0.9764465313541351, 'upgrade4_to_idle1': 0.9913502755664422, 'clear4_to_idle1': 0.9708263326714526}; soil darkening 18.33% |
| h | PASS | see qa.json |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.0000 |

Overall: PASS (10/10). This is mechanical QA, not Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-04.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6466 before, 1785 in final quantized atlas; 5634 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
