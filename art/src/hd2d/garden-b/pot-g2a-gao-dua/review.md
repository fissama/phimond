# Review — pot-g2a-gao-dua

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
| g | PASS | min body IoU 0.9534; transitions {'water4_to_wet1': 0.984474123539232, 'upgrade4_to_idle1': 0.9839128613322161, 'clear4_to_idle1': 0.946569867036463}; soil darkening 56.29% |
| h | PASS | see qa.json |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.0000 |

Overall: PASS (10/10). This is mechanical QA, not Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-09.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 8003 before, 2211 in final quantized atlas; 6819 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
