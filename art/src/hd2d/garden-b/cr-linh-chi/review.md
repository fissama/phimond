# Visual review — cr-linh-chi

Inspected `review-4x-dark.png`, `review-4x-checker.png`, `review-pivot-grid.png`, and row strips/GIFs. The tortoise/reishi identity is readable, and the stage sequence is visibly distinct. The dark preview reveals magenta/purple fringe around most character outlines, which violates the no-magenta style rule. Harvest frame 4 retains warm motes but no character.

Visual review: **FAIL** (visible magenta/purple outline fringe).

Face notes below are approximate cell-local coordinates from the enlarged atlas.
face_row_1: eyes=96,143; mouth=96,155; blink=frame3
face_row_2: eyes=96,117; mouth=96,137; blink=frame3
face_row_3: eyes=96,86; mouth=96,108; blink=frame3
face_row_4: eyes=96,105; mouth=96,120; blink=none
face_row_5: eyes=96,143; mouth=96,155; blink=none

## ImageGen attempts and measurements

| Attempt | Source | Result |
|---:|---|---|
| 1 | raw-01 | 9/10; f failed (sprout 72–78 px; ripe 123–132 px; width 142 px); h=.6597; loop min=.8588. |
| 2 | raw-02 | Pack failed: no common scale s≥0.6 fit all frames. |
| 3 | raw-03 | 9/10; f failed (ripe 114 px, width 145 px); h=.9573; loop min=.8619. Selected as highest gate count. |
| 4 | raw-04 | 8/10; h=.7351, loop min=.8045; f passes. |
| 5 | raw-05 | 8/10; h=.6974, loop min=.7580; f passes. |
| 6 | raw-06 | 8/10; h=.7261, loop min=.6921; f passes. |
| 7 | raw-07 | 8/10; h=.7162, loop min=.7421; f passes. |
| 8 | raw-08 | 8/10; h=.7303, loop min=.8363; f passes. |

## Selected candidate measurement — raw-03

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | No alpha outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | All pivots within ±1 |
| f | FAIL | Heights sprout 58–59, grow 88, ripe 114 px; max width 145 px (ripe needs 120–150 high, width ≤140) |
| g | N/A | Crop |
| h | PASS | IoU 0.9573 (≥0.80) |
| i | PASS | Blink rows 1–3 at frame3; face notes present |
| j | PASS | Minimum loop IoU 0.8619 (≥0.85) |

Overall: 9/10 mechanical gates pass. **Blocked after all 8 ImageGen outputs** by gate f and visual contour fringe. No criteria were relaxed.

SHA-256 final: `35ba934e565dd72150bbda604a1478336da645641f19e3d1435a60c20402e5f8`; selected raw: `2b0d76441fee95c0f66f0c1a1ccda8bf56b9b9db1ef78c155a0c86da2af78f30`.

## Repack and review — 2026-11-13

Selected `raw-10.png`; 10/10 mechanical gates pass. Purple-hued opaque edge pixels: 6576 before, 4545 after. all gates pass; ripe 140; width 98; edge 6576→4545. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.
