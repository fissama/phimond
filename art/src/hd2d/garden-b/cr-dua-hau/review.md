# Visual review — cr-dua-hau

Visual inspection: opened the 4×5 final atlas. Character faces are visible at native scale and each repeating growth row includes a closed-eye blink.

## Face notes
face_row_1: eyes = 96,148; mouth = 96,158; blink = frame3
face_row_2: eyes = 96,130; mouth = 96,145; blink = frame3
face_row_3: eyes = 96,112; mouth = 96,130; blink = frame3
face_row_4: eyes = 96,115; mouth = 96,129; blink = frame2
face_row_5: eyes = 96,148; mouth = 96,159; blink = frame2

## Current task gate record — plant-row redraw (8 ImageGen outputs)

Opened the latest packed atlas. The seed-to-seedling sequence is visible and the character remains readable. Bottom-right plant f4 is visibly larger than sprout f1, matching the measured h failure. ImageGen regenerated the full sheet despite repeated row-5-only instructions; no code compositing or pixel patching was used.

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha=[0, 255]; hidden RGB=0 |
| b | PASS | 20/20 nonempty; 20/20 unique |
| c | PASS | 0 opaque pixels outside [16,175] |
| d | PASS | 60 visible colors |
| e | PASS | crop pivots compared with (96,168), ±1 px |
| f | PASS | sprout=[65,66], grow=[106,107], ripe=[140,141] px; max body width=136 px |
| g | PASS | N/A for crop |
| h | FAIL | plant f4 vs sprout f1 IoU=0.5710 (required ≥0.80) |
| i | PASS | face rows=[1, 2, 3, 4, 5], blink rows=[1, 2, 3] |
| j | FAIL | loop minimum IoU=0.8458 (required ≥0.85) |

**Overall: FAIL (8/10 script checks).** Eight new built-in ImageGen outputs were used for this task; the per-asset allowance is exhausted. No threshold was changed. `approved:false`.

## Plant-row task review — 2026-11-10

The plant row now starts with a seed in soil and progresses to a sprout. The final frame still misses the silhouette IoU gate. Attempts raw-02 through raw-09 were packed and measured; the final raw-09 result is retained in qa.json. The original request was to change only row 5, but ImageGen re-rendered rows 1–4 on each call, causing width and loop measurements to vary. Current final SHA256: `ed70ec92b194dc57b3482094b9aa2c03c63c6158f76520fec0b6292e64517b14`; raw-09 SHA256: `d70232cf09c3457439daab95d00f69b82c04a5222baf5d1fdff708500f9bde65`.


## Plant f4 repair — 2026-11-12

Used 4 new ImageGen output(s) where applicable. Selected `raw-09.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.5709541062801933; gates passed 8/10; purple-hued edge count 8020→4642. Reference: `reference-sprout-f1.png` SHA-256 `83dd38c22a1c3d9d5f97e5e6f9a595a10444f4364d2d568f8ed3d04da7e9e762`.

## Repack and review — 2026-11-13

Selected `raw-09.png`; 8/10 mechanical gates pass. Purple-hued opaque edge pixels: 8020 before, 4642 after. h=.5710; j=.8458; edge 8020→4642. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.

## Retry status — 2026-11-13

Latest candidate `raw-13.png`: 9/10 mechanical gates; h IoU=.7891 fails the .80 threshold; j=.8524 passes. Gates a–g and i pass. Dark preview refreshed from this candidate. Three of six new ImageGen outputs were used. ImageGen returned HTTP 429; pause and resume after 2026-11-13 11:50:38 +07.

## Targeted plant f4 repair — 2026-11-13

Used all six new ImageGen outputs (`raw-11.png`–`raw-16.png`), retaining every source. Latest packed candidate is raw-16: h=.5822 (<.80), j=.8690 (pass), all other measured crop gates pass. No threshold changes or pixel edits. Marked blocked after 6/6 outputs.

## Targeted plant f4 repair — 2026-11-16

Used six new ImageGen outputs and retained all raws. Latest candidate `raw-16.png`: 9/10; h=0.5822 fails .80; j=0.8690 passes; all other measured gates pass. Blocked after 6/6 attempts.
