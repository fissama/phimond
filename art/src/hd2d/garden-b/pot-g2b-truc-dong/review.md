# Review — pot-g2b-truc-dong

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
| g | FAIL | min body IoU 0.6318; transitions {'water4_to_wet1': 0.9865150713907985, 'upgrade4_to_idle1': 0.8121116120385037, 'clear4_to_idle1': 0.9431625602920088}; soil darkening 20.48% |
| h | PASS | see qa.json |
| i | PASS | see qa.json |
| j | FAIL | min loop body IoU 0.0000 |

Overall: FAIL (8/10). This is mechanical QA, not Claude approval.

## Current task gate record

Opened current final: bamboo bundle and layered mouths read; current design is low/wide, though measured wet darkening still misses gate g.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | opaque bounds checked against [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | pot pivot compared with (96,175), ±1 px |
| f | PASS | N/A for pot |
| g | FAIL | min adjacent body IoU=0.9055; joins={'water4_to_wet1': 0.9832933439971563, 'upgrade4_to_idle1': 0.9495495495495495, 'clear4_to_idle1': 0.9540722596448254}; soil darkening=4.54%; measured connected bbox sizes range 149–151w × 91–106h px (water/plant effects may be connected) |
| h | PASS | N/A for pot |
| i | PASS | N/A for pot (no face) |
| j | PASS | loop min IoU=0.0000 |

**Overall: FAIL (9/10 script checks).** `approved:false`; not a Claude approval.

**Task-specific size gate:** current final connected body bbox includes animation protrusions; core bamboo pot is visibly 149–151 px wide and around 91–97 px tall in most frames, but some attached effects/upgrade leaves extend the measured connected height to 106 px. User gate g still fails on soil and body IoU.

## Latest repair round — 8 ImageGen outputs

Opened the latest packed atlas. The muted bamboo bundle and repeated no-face pot silhouettes are readable; however the image still shows little soil value change in the measured mouth region.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; binary alpha; hidden RGB=0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | no opaque pixel outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | N/A for pot |
| g | FAIL | minimum adjacent body IoU=0.9451 (<0.95); joins min=0.9748 (≥0.93); soil darkening=2.78% (<15%). Latest packed bbox [18,67,172,175] = 155×109 px, outside requested height range and width upper limit. |
| h | PASS | N/A for pot |
| i | PASS | N/A, pot has no face |
| j | PASS | loop min IoU=0.9870 |

**Overall: FAIL (9/10 mechanical checks); task-specific size and wet-soil requirements also fail.** Eight new ImageGen outputs were used in this repair round. No threshold changed. See qa.json for every measured value. Raw-29 SHA256: `a023eb7543dce6855888b3980476f606f12d49e1f11c970ea346769e09ec3ff1`.

## Repack and review — 2026-11-13

Selected `raw-29.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 7752 before, 2866 after. body IoU .9451; wet darkening 2.80%; edge 7752→2866. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.


## Targeted repair round — 2026-11-16 (6 new ImageGen attempts)

| Raw | Pack | a | b | c | d | e | g | j | Main measurement |
|---|---|---|---|---|---|---|---|---|---|
| raw-34 | PASS | P | P | P | P | P | F | P | min body IoU .9460; wet darkening 1.76% |
| raw-35 | PASS, selected | P | P | P | P | P | F | P | min body IoU .9465; wet darkening 16.15%; joins ≥.9813 |
| raw-36 | PASS | P | P | P | P | P | F | P | min body IoU .9447; wet darkening 2.10% |
| raw-37 | FAIL | — | — | — | — | — | — | — | no common scale s≥.6 fits safe bounds |
| raw-38 | PASS | P | P | P | P | P | F | P | min body IoU .9458; wet darkening 15.66% |
| raw-39 | PASS | P | P | P | P | P | F | P | min body IoU .9392; wet darkening .81% |

Selected raw-35 as the best candidate and repacked it for the current `final.png`. Dark 4× preview inspected: the wet soil is visibly darker than idle, the bamboo bundle remains legible, and no distinct detached magenta fringe is visible. The remaining gate g failure is min adjacent body IoU .9465 (<.95); the minimum occurs in water row 3, frames 1→2 (exact QA value .9465099965; .9458 was measured on a different candidate). Wet darkening is 16.15% (≥15%); transition joins all pass (minimum .9814 ≥.93). Six new outputs are exhausted; do not claim full pass.

## Current repair round — 2026-11-16 (palette + upgrade; six outputs)
Selected `raw-44.png` from six new ImageGen outputs (`raw-42..47`); retained all raws and used the approved pack/defringe/measure pipeline. The 4× dark preview shows a muted olive bamboo bundle, brown ties, clear nodes and an upgrade row with shoots. Mechanical gate g still fails: min adjacent body IoU=0.9371 (<0.94), wet soil darkening=3.95% (<15%); transition IoUs are 0.9734 / 0.9529 / 0.9725 and pass. Other a–f,h–j pass; 60 colors. Six attempts exhausted; blocked.
