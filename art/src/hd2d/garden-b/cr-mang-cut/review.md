# cr-mang-cut — self review

face_row_1: eyes=91,126; mouth=96,135; blink=frame3
face_row_2: eyes=89,79; mouth=96,91; blink=frame3
face_row_3: eyes=84,60; mouth=96,74; blink=frame3
face_row_4: eyes=83,75; mouth=96,88; blink=frame3
face_row_5: eyes=91,138; mouth=96,145; blink=none

The mangosteen queen has a pale face framed by a green calyx crown, a deep-violet fruit body, and visible cream-white fruit segments. Rows 1–3 each blink in frame 3. Plant f4 repeats the small sprout silhouette. Harvest waves before fading to sparse pale flecks.

Measured selected raw-01: all gates pass after these face annotations. 60 colors; heights 57 / 94 / 126–127 px; max width 111 px; plant/sprout IoU .9577; minimum loop IoU .8792. Viewed the generated sheet and packed atlas; contours are hard stepped with no baked shadow/glow. Palette is at the 60-color limit.


## Continuation audit — 2026-11-12

Selected packed source is `raw-06.png`; final SHA256 `b8a729c724b279d01cf4e15afa647902538e0bb84bf4482975ef717712307b65`. Mechanical gates: 10/10. Latest independent visual audit: FAIL. Manual dark 4x review shows violet/magenta contour despite all mechanical gates passing.

Status: `blocked_imagegen_limit` after 8 outputs. No further pixel modifications were made.


## Edge defringe — 2026-11-12

Repacked from `raw-06.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6784 before, 5200 in final quantized atlas; 3195 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
