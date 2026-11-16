# Review — cr-rieng

## Face notes

face_row_1: eyes=96,143; mouth=96,153; blink=frame3
face_row_2: eyes=96,109; mouth=96,123; blink=frame3
face_row_3: eyes=96,75; mouth=96,89; blink=frame2
face_row_4: eyes=96,82; mouth=96,96; blink=none
face_row_5: eyes=96,143; mouth=96,153; blink=none

## Visual review

Raw-01 inspected: crab identity and segmented rhizome claws read clearly; tiny cute face and plant motif are visible. Pending packed review and a–j measurement.

## Gate history

| Source | a | b | c | d | e | f | g | h | i | j | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01 | pending | pending | pending | pending | pending | pending | N/A | pending | pending | pending | pending |

## Pipeline v3 attempt cap — raw-08

ImageGen outputs retained: raw-01 through raw-08 (8 total). The final packed atlas was opened at 4× on a dark background; the galangal crab identity and expressions read clearly, but a pink/magenta fringe remains around visible sprite contours. No pixel was manually edited.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 71 / 108–109 / 150 px; max width 117 px |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.7752 (required ≥0.80) |
| i | PASS | blinks row1 f3, row2 f3, row3 f2; face notes above |
| j | PASS | minimum loop body IoU 0.9603 (required ≥0.85) |

Status: **BLOCKED** after 8 ImageGen outputs. Best mechanical candidate raw-08 still misses h by 0.0248. Visual contour fringe is also unresolved. Recommendation: produce plant f4 as a single-frame edit explicitly derived from the packed sprout f1, then rebuild with the allowed pipeline after a fresh per-frame edit allowance; retain the current design and palette.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6356 before, 1446 in final quantized atlas; 5610 pixels replaced. Mechanical gates: 9/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.

## Targeted repair 2026-11-16
Five new ImageGen outputs raw-09–13. Selected raw-13: a–j pass; h=.8057, j=.9399, 59 colors, ripe 149–150 px, width 116. Viewed dark 4x: strong isolated pink fringe remains across outlines; blocked visually.
