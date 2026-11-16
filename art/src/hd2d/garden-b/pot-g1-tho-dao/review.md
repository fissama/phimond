# Visual review — pot-g1-tho-dao

Inspected `review-4x-checker.png`, `review-4x-dark.png`, and all five `preview-row-N.png` images. The pot remains recognizable and has no face. Pixel edges are readable, but a bright spiky ornament on the left body reads as a baked emblem and the water/upgrade/clear sequences change or remove too much of the pot. In row 3 the water effect jumps from a droplet to a large splash, then a small splash, then bare idle; row 4/5 also fail to return to idle cleanly. Visual review: **FAIL**.

Mechanical review (`qa.json`): a,b PASS; c,d,e,g FAIL; f,h,i N/A. Body x drift 23 px; mouth dark centroid (99.64,105.53), target (96,112); maximum adjacent body-region difference 84.99%; water→wet 35.36%, upgrade→idle 40.53%, clear→idle 42.13%; wet soil luminance is 150.52 vs idle 143.37 (−4.99% darkening, direction wrong). Safe-area violations: 7 cells. Invariant body colors 0/required 33–48.


## Pipeline v3 round 2 — raw-11 pack

Inspected refreshed 4× checker/dark atlas, pivot grid and row previews. Clay is now a softer warm brown-orange and no face is present. Water/upgrade/clear joins pass by mask IoU, but the pot body changes slightly between consecutive frames. The soil in the measured mouth ellipse is not darker: the current wet row appears similar to idle at the sampled ROI.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | all pivots within ±1 |
| f | N/A | pot |
| g | FAIL | min consecutive body IoU 0.9371 (≥0.95); water/wet 0.9789, upgrade/idle 0.9708, clear/idle 0.9585 (each ≥0.93); soil idle 141.45, wet 141.87, darkening −0.30% (≥15%) |
| h | N/A | pot |
| i | N/A | pot has no face |
| j | FAIL | min loop body IoU 0.9409 (≥0.85) |


## Pipeline v3 final — raw-21, independently remeasured 2026-11-10

Opened the current 4× checker and dark previews, pivot grid, and all five row strips. The pot is a squat warm terracotta bowl with no face or plant. Wet soil is visibly darker; water, upgrade, and clear transitions return cleanly to their target rows. The clay reads slightly brighter orange than the garden-a anchor at 4×; the shape and pixel edge remain legible. Visual review: **PASS for handoff; Claude review pending**.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 59 colors |
| e | PASS | all pivots within ±1; base target (96,175) |
| f | N/A | pot |
| g | PASS | min adjacent body IoU 0.9531; joins 0.9851 / 0.9869 / 0.9884; idle soil 113.56, wet soil 93.11, darkening 18.01% |
| h | N/A | pot |
| i | N/A | pot has no face |
| j | PASS | minimum loop body IoU 0.9898 |


## Edge defringe — 2026-11-12

Repacked from `raw-21.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7358 before, 3643 in final quantized atlas; 4593 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
