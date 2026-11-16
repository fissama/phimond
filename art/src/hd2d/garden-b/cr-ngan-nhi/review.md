# cr-ngan-nhi — self review

face_row_1: eyes=91,132; mouth=96,139; blink=frame3
face_row_2: eyes=88,82; mouth=96,91; blink=frame3
face_row_3: eyes=82,66; mouth=96,75; blink=frame3
face_row_4: eyes=82,74; mouth=96,87; blink=frame3
face_row_5: eyes=92,136; mouth=96,144; blink=none

The shy snow-fungus girl has a small readable face in every looping frame; row 1 frame 3 and rows 2–3 frame 3 visibly blink. Plant f4 matches the small sprout silhouette. The harvest row moves from a shy wave to a few pale flecks.

Measured selected candidate raw-05: a–h and j pass; i passes after face annotations. 59 colors; heights 50–51 / 90 / 121–122 px; max width 107 px; plant/sprout IoU .9274; minimum loop IoU .9087. Viewed the sheet and packed preview: icy white/blue palette and hard stepped edges are clear; no glow or baked shadow in the packed sprite.


## Continuation audit — 2026-11-12

Selected packed source is `raw-07.png`; final SHA256 `c7dddda064f781bad84616fa71fba9712e73af522296d9a33507871a526f8502`. Mechanical gates: 10/10. Latest independent visual audit: FAIL. Manual dark 4x review shows violet/magenta contour despite all mechanical gates passing.

Status: `blocked_imagegen_limit` after 8 outputs. No further pixel modifications were made.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 3555 before, 630 in final quantized atlas; 3536 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
