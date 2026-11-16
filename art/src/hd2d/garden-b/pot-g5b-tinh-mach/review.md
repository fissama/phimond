# Visual review — pot-g5b-tinh-mach

## Face notes

## Current task gate record

Opened current final: purple stone and gold veins read; body stability and wet-darkening gates fail.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | pot pivot compared with (96,175), ±1 px |
| f | PASS | N/A for pot |
| g | FAIL | min adjacent body IoU=0.4441; joins={'water4_to_wet1': 0.9553816046966732, 'upgrade4_to_idle1': 0.9452597026452983, 'clear4_to_idle1': 0.9204211325049796}; soil darkening=6.97%; measured connected bbox sizes range 118–120w × 118–120h px (water/plant effects may be connected) |
| h | PASS | N/A for pot |
| i | PASS | N/A for pot (no face) |
| j | PASS | loop min IoU=0.0000 |

**Overall: FAIL (9/10 script checks).** `approved:false`; not a Claude approval.

## Latest repair round — 8 ImageGen outputs

Opened latest packed atlas. The purple stone bowl and gold vein read clearly; however the bowl remains too tall and narrow, and the wet soil only appears modestly darker in the measured mouth ellipse.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; binary alpha; hidden RGB=0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | no opaque pixel outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | N/A for pot |
| g | FAIL | minimum adjacent body IoU=0.9499 (<0.95); joins min=0.9495 (≥0.93); soil darkening=6.84% (<15%). Body bbox [33,57,158,175] =126×119 px, outside requested 130–158×70–100 px. |
| h | PASS | N/A for pot |
| i | PASS | N/A, pot has no face |
| j | PASS | loop minimum IoU=0.9499 |

**Overall: FAIL (9/10 mechanical checks); size gate also fails.** Eight new ImageGen outputs were used; no threshold changed. Raw-11 SHA256: `930f6cc41a2d076b4d7c899cf5ff17b9bf21ab24745e29ac0a50a95d00fabc43`.

## Repack and review — 2026-11-13

Selected `raw-13.png`; 10/10 mechanical gates pass. Purple-hued opaque edge pixels: 20237 before, 16475 after. all gates pass; body IoU .9536; join min .9436; wet darkening 46.40%; edge 20237→16475. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.
