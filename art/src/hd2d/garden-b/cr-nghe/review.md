# Visual review — cr-nghe

Inspected the current 4× checker, dark background, pivot grid, and all five row strips. The subject reads as a turmeric tiger cub with the intended orange/cream palette, and rows1–3 show expressive faces and blinks. The plant sequence starts with a root in soil, but its f4 does not sufficiently match the sprout silhouette. Harvest frame3 includes loose leaves. Opaque purple/magenta fringe is prominent around silhouettes on dark and checker backgrounds, contrary to the style brief. Visual review: FAIL.

Face notes approximate from the opened row previews:
face_row_1: eyes=96,138; mouth=96,149; blink=frame1
face_row_2: eyes=96,104; mouth=96,119; blink=frame3
face_row_3: eyes=96,73; mouth=96,91; blink=frame2
face_row_4: eyes=96,89; mouth=96,104; blink=none
face_row_5: eyes=96,140; mouth=96,150; blink=none

## Attempts and selected gate record

One standalone sprout reference plus eight full-sheet ImageGen outputs were produced (9 total, recorded as an accidental overrun of the 8-output cap); all raw files remain. Best measured full atlas was raw-05 and is selected for audit. Attempts that addressed plant f4 did not raise the h measurement above threshold.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 |
| f | PASS | heights 74–75 / 109 / 150 px; width 121 px |
| g | N/A | crop |
| h | FAIL | plant f4 vs sprout f1 IoU 0.7640 (≥0.80) |
| i | PASS | face notes rows1–5; blinks rows1 f1, 2 f3, 3 f2 |
| j | PASS | minimum loop IoU 0.9383 (≥0.85) |

Read-only style scan: 17,634 opaque purple-like pixels in the selected atlas. No waiver or threshold changed. Status: blocked; not approved.


## Plant f4 repair — 2026-11-12

Used 4 new ImageGen output(s) where applicable. Selected `raw-05.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.7639719261762412; gates passed 9/10; purple-hued edge count 6681→0. Reference: `reference-sprout-f1.png` SHA-256 `e8f915bdb4ee42d0ef5b7240b33aebc7942d14e3a7f6f16915e5181573181056`.

## Repack and review — 2026-11-13

Selected `raw-05.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 6681 before, 0 after. h=.7640; edge 6681→0. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.

## Targeted plant f4 repair — 2026-11-16

Used six new ImageGen outputs and retained all raws. Latest candidate `raw-18.png`: 9/10; h=0.5673 fails .80; j=0.9192 passes; all other measured gates pass. Blocked after 6/6 attempts.

## Current repair round — 2026-11-16 (plant f4 only)
Selected `raw-29.png` from six new ImageGen outputs (`raw-25..30`; `raw-30` did not pack). Repacked and remeasured with the Claude thresholds in `measure_atlas.py`. Gate h is 0.6717 (<0.75); a–g, i, j pass; 59 colors, stage heights 73/72–74/147–148 px, width 118 px, loop IoU 0.9127. Six attempts exhausted. 4× dark review shows no detached magenta fringe. Status remains blocked on h.
