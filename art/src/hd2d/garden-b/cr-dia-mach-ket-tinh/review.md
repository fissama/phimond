# Review — cr-dia-mach-ket-tinh

Selected `raw-07.png` after 8 ImageGen atlas outputs. Manually inspected the packed 4× dark and checker previews. The stone golem silhouette, gold crystals, vein lines, blink, and harvest fade read clearly. A purple/magenta contour fringe remains around sprite edges, including small detached gold effects, and is visible on the dark backing. It persisted after repeated prompts requiring black/charcoal outlines and forbidding magenta. Candidate is blocked on visual style despite all a–j measurements passing.

## Face notes (cell-local pixel coordinates)
face_row_1: eyes=86,122; mouth=96,133; blink=frame3
face_row_2: eyes=86,109; mouth=96,122; blink=frame3
face_row_3: eyes=86,88; mouth=96,102; blink=frame3
face_row_4: eyes=86,109; mouth=96,121; blink=none
face_row_5: eyes=86,128; mouth=96,139; blink=none

## Measurement rounds

| Raw | Result | Key measurements |
|---|---|---|
| raw-01 | 8/10 | 60 colors; heights 52/86/115–117; ripe below 120px; h=.9244; loop .8963. |
| raw-02 | 10/10 | 60 colors; heights 57/99/148–149; width 135; h=.9602; loop .9147. |
| raw-03 | 10/10 | 60 colors; heights 58/99/147–148; width 134; h=.9437; loop .9236. |
| raw-04 | 10/10 | 60 colors; heights 57–58/96/142–143; width 140; h=.9182; loop .9080. |
| raw-05 | 10/10 | 60 colors; heights 57/96/141; width 140; h=.9613; loop .9087. |
| raw-06 | 10/10 | 59 colors; heights 56/92–93/136; width 133; h=.9474; loop .9067. |
| raw-07 | 10/10 | 59 colors; heights 57/93/133–134; width 130; h=.9650; loop .9072. |
| raw-08 | 9/10 | 58 colors; heights 56/91–92/131–132; width 132; h=.9742; loop .8270 (<.85). |

## Visual observation

The 4× dark preview confirms the fringe remains after eight differently worded attempts, including a final prompt with a fixed charcoal/gold palette and a thick black contour. The issue is not removable through the allowed pack/measure pipeline; no alpha or pixel retouching was used.


## Edge defringe — 2026-11-12

Repacked from `raw-07.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 6244 before, 4753 in final quantized atlas; 3287 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.

## Visual identity check after defringe — 2026-11-13

The crystalline-vein character and face remain readable, but small violet/magenta pixels still form a visible fringe on the outer sprite contours.
