# Review — cr-ho-tieu

Selected `raw-08.png` after 8 ImageGen atlas outputs. Packed and inspected at 4× on dark and checker backgrounds. Mechanically the sheet meets a–j after these face notes are recorded; visual review fails the no-magenta/style requirement: thin violet-magenta pixels remain around the subject outlines in all rows. This persisted through all 8 outputs, including a final prompt specifying olive/brown outlines and no purple/magenta. Status remains blocked; do not treat this as approved.

## Face notes
face_row_1: eyes=84,112; mouth=96,121; blink=frame3
face_row_2: eyes=84,101; mouth=96,111; blink=frame3
face_row_3: eyes=84,88; mouth=96,101; blink=frame3

## Measurement rounds

| Raw | Result | Key measurements |
|---|---|---|
| raw-01 | pack failed | Common scale ≥0.6 could not fit row 3 frame 3 pepper motes inside safe area. |
| raw-02 | 7/10 | 60 colors; sprout 76px; h=.9241; min loop IoU=.7993. |
| raw-03 | 8/10 | 60 colors; heights 70–71/101–106/150; width 120; h=.7758; loop .9177. |
| raw-04 | 8/10 | 59 colors; h=.7019; other measured gates passed. |
| raw-05 | 7/10 | 60 colors; sprout up to 83px; grow up to 114px; h=.8747; loop .8490. |
| raw-06 | 8/10 | 59 colors; h=.8178; row 1 frame 2 height 78px. |
| raw-07 | 9/10 | 58 colors; heights 73/72/73/73, 108/111/104/108, 139/138/134/138; width 127; h=.8900; loop min .8814. |
| raw-08 | 9/10 before face notes; 10/10 after | 58 colors; heights 74/74/74/74, 109/111/104/109, 139/139/135/139; width 127; h=.9246; loop min .8839. Gate i supplied by face notes above. |

## Visual observations

The character reads clearly as a friendly pepper bee, with distinct baby, growing, and ripe sizes. The sneeze/pepper cluster and plant-row awakening are legible. The 4× dark view shows a conspicuous magenta/violet contour fringe against the dark backing, so this candidate is blocked despite passing the numeric a–j checks.
face_row_4: eyes=84,111; mouth=96,120; blink=none
face_row_5: eyes=84,119; mouth=96,128; blink=none


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7786 before, 1356 in final quantized atlas; 7129 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.

## Visual identity check after defringe — 2026-11-13

The pepper-sprout character and face remain readable, but small violet/magenta pixels still form a visible fringe on the outer sprite contours.
