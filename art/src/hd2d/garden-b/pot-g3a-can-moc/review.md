# Review — pot-g3a-can-moc

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
| g | PASS | min body IoU 0.9504; transitions {'water4_to_wet1': 0.9534335727109515, 'upgrade4_to_idle1': 0.9806356077001936, 'clear4_to_idle1': 0.9697211155378486}; soil darkening 41.97% |
| h | PASS | see qa.json |
| i | PASS | see qa.json |
| j | PASS | min loop body IoU 0.0000 |

Overall: PASS (10/10). This is mechanical QA, not Claude approval.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6576 before, 1413 in final quantized atlas; 6431 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
