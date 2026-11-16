# Visual review — cr-chom-chom

Inspected the packed atlas and source sheet. The round red rambutan body, cream face, green tipped hairs and seedling arc are readable; sprout/grow/ripe silhouettes visibly grow, harvest keeps the character through the farewell frames, and the last plant frame returns to a small character. However, the plant f4 contour does not match sprout f1 closely enough (measured IoU .5159). The generated character also shows thin pink/magenta contour pixels at 4x against dark background; style visual review fails.

Visual review: **FAIL**; gate h and contour color remain blockers.

Approximate cell-local face positions from enlarged atlas:
face_row_1: eyes=96,142; mouth=96,154; blink=frame3
face_row_2: eyes=96,116; mouth=96,133; blink=frame3
face_row_3: eyes=96,86; mouth=96,107; blink=frame3
face_row_4: eyes=96,102; mouth=96,122; blink=none
face_row_5: eyes=96,143; mouth=96,155; blink=none

## Attempt log

1. `sprout-reference.png`: standalone seedling reference generated; retained. (counts as ImageGen output)
2. `raw-01.png`: first atlas. f failed: sprout=98, grow=130, ripe=150 px; h=.7220; i annotations absent.
3. `raw-02.png`: resized sprout/grow succeeded; f passes; h=.5272; loop=.9537; i annotations absent.
4. `raw-03.png`: h=.5062; loop=.9476; f passes.
5. `raw-04.png`: h=.5003; loop=.9105; f passes.
6. `raw-05.png`: h=.5069; loop=.9588; f passes.
7. `raw-06.png`: h=.4980; loop=.9049; f passes.
8. `raw-07.png`: h=.5159; loop=.9552; f passes. Selected latest candidate; eight outputs exhausted.

## Selected candidate measurements — raw-07

| Gate | Result | Measurement |
|---|---|---|
| a | PASS | 768×960 RGBA; alpha 0/255; hidden RGB 0 |
| b | PASS | 20/20 nonempty and unique |
| c | PASS | 0 alpha pixels outside [16,175] |
| d | PASS | 60 colors |
| e | PASS | pivots within ±1 of (96,168) |
| f | PASS | heights sprout 57–58, grow 103–104, ripe 150 px; max width 134 px |
| g | N/A | Crop |
| h | FAIL | plant f4 vs sprout f1 mask IoU=.5159 (≥.80) |
| i | PASS | blink row1/2/3 frame3; face notes recorded above |
| j | PASS | min loop-body IoU=.9552 (≥.85) |

Overall mechanical result: 9/10. Blocked after 8 ImageGen outputs on h; visual style also fails due pink/magenta outline pixels. Criteria unchanged.


## Plant f4 repair — 2026-11-12

Used 4 new ImageGen output(s) where applicable. Selected `raw-09.png` and repacked with `pack_atlas.py` plus edge defringe. Plant-to-sprout IoU: 0.6271735926908341; gates passed 9/10; purple-hued edge count 8108→3717. Reference: `reference-sprout-f1.png` SHA-256 `1496d07bfe5de5ec1b392c58ecae985d0901c271fff30d5d68f6eb734472a3fe`.

## Repack and review — 2026-11-13

Selected `raw-09.png`; 9/10 mechanical gates pass. Purple-hued opaque edge pixels: 8108 before, 3717 after. h=.6272; edge 8108→3717. See the refreshed `review-4x-dark.png` and `qa.json`; any remaining edge color or failed gate keeps the asset blocked.

## Targeted repair 2026-11-16
raw-13, 1/6 attempts: a–j pass, h=.8811, j=.9577, 60 colors, ripe 150 px, width 131. Viewed 4x dark: no distinct isolated magenta fringe observed; row 1–3 blink at frame 3; plant begins with a seed. Harvest f4 still shows the full character with sparkle, noted for Claude.
