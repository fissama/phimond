# Visual review — cr-hoa-lan

Inspected packed atlas and source. Orchid/butterfly silhouette is readable, petals are cream-white with muted violet patches, the yellow center and leafy body are clear. Sprout, grow and ripe forms progress in size. Plant f4 reads as a tiny orchid bud but its mask does not match sprout f1 closely enough by measurement. The dark background preview should be checked for generated contour fringe before final review.

Visual review: **FAIL** on plant silhouette match; no approval assigned.

Approximate cell-local face positions:
face_row_1: eyes=96,144; mouth=96,155; blink=frame3
face_row_2: eyes=96,113; mouth=96,132; blink=frame3
face_row_3: eyes=96,76; mouth=96,101; blink=frame3
face_row_4: eyes=96,82; mouth=96,105; blink=none
face_row_5: eyes=96,145; mouth=96,156; blink=none

## Attempts

| Attempt | Source | Result |
|---:|---|---|
| 1 | standalone sprout reference | Reference generated and retained. |
| 2 | raw-01 | f sprout=77 px (>75); h=.2129; loop=.9184. |
| 3 | raw-02 | f sprout=80 px; h=.3736; loop=.9035. |
| 4 | raw-03 | f sprout=80 px; h=.4290; loop=.9233. |
| 5 | raw-04 | f sprout=69–70; h=.4176; loop=.9580. |
| 6 | raw-05 | f passes (69–70/104/150; width136); h=.5712; loop=.9199. |
| 7 | raw-06 | f passes (69–70/103–104/150; width135); h=.6455; loop=.9123. Best h candidate. |
| 8 | raw-07 | f passes (69–70/103/150; width134); h=.6323; loop=.9184. |

## Selected raw-06 measurements

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA, binary alpha, hidden RGB zero |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 violations outside [16,175] |
| d | PASS | 57 colors |
| e | PASS | all pivots within ±1 |
| f | PASS | heights 69–70/103–104/150 px; max width 135 px |
| g | N/A | Crop |
| h | FAIL | IoU .6455 (<.80) |
| i | PASS | blink frame3 in rows1–3; face notes recorded |
| j | PASS | loop min IoU .9123 (≥.85) |

Blocked after 8 total ImageGen outputs (one reference and seven atlas sheets) on gate h. No threshold changes.


## Plant f4 repair — 2026-11-12

Used 3 new ImageGen output(s) where applicable. Selected `raw-10.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.8077844311377246; gates passed 10/10; purple-hued edge count 10362→7631. Reference: `reference-sprout-f1.png` SHA-256 `0ff9a3bfb79dd3df9cc383031c89173f39766c969c36bd639b8aeacdd6187b31`.

## Repack and review — 2026-11-13

Selected `raw-10.png`; 10/10 mechanical gates pass. Purple-hued opaque edge pixels: 10362 before, 7631 after. h=.8078; edge 10362→7631. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.
