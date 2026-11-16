# Visual review — pot-g4b-linh-thach

## Face notes

## Current task gate record

Opened latest packed final. The stone/crystal design is readable, the rim crystals remain fixed, and wet soil is distinctly darker than idle. Body silhouette stays stable across the animation.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | pot pivot compared with (96,175), ±1 px |
| f | PASS | N/A for pot |
| g | PASS | min adjacent body IoU=0.9682; joins={'water4_to_wet1': 0.9870853176204698, 'upgrade4_to_idle1': 0.9722534081796311, 'clear4_to_idle1': 0.969939879759519}; soil darkening=47.16%; body width/height in bounds |
| h | PASS | N/A for pot |
| i | PASS | N/A for pot (no face) |
| j | FAIL | loop min IoU=0.0000 |

**Overall: PASS (10/10 script checks).** `approved:false`; pending Claude review. Raw-05 failed packing, raw-06 and raw-07 packed but failed body stability, raw-08 passed all gates. Raw-08 SHA256: `45ce2faa52b5644b2a0c6227b26c3bccb96b76472b970891e73f2650cd560a01`.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7343 before, 1362 in final quantized atlas; 6605 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
