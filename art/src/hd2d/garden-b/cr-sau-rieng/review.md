# Review — cr-sau-rieng

The selected packed candidate is sourced from `raw-08.png` after 8 ImageGen outputs. Mechanical gates a–j pass (58 colors; sprout/grow/ripe heights 73/101/139 px; width 139 px; plant IoU .9333; loop min IoU .9455).

## Visual review

Opened the 4× dark preview and `raw-08.png`. A vivid violet/magenta contour fringe remains. More seriously, the character reads as a bright flower-headed warrior carrying a sword and shield; it does not read as a durian fruit with spiked armor and cream segments. This is a visual identity failure, so the candidate is blocked despite all 10 mechanical checks passing. The 8-output allowance was already used; any next round should begin with a prompt that explicitly prohibits flower petals, sword, and shield and depicts the durian spiked husk with cream interior.

The previous text in this file claiming the selected source was raw-01 and visual review was pending did not match the current QA source and preview. This note records the inspected current artifact.


## Edge defringe — 2026-11-12

Repacked from `raw-08.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 4823 before, 0 in final quantized atlas; 4813 pixels replaced. Mechanical gates: 9/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.


## Face annotations for redesigned atlas
face_row_1: eyes=91,145; mouth=96,156; blink=frame3
face_row_2: eyes=91,121; mouth=96,136; blink=frame3
face_row_3: eyes=91,93; mouth=96,111; blink=frame3
face_row_4: eyes=91,94; mouth=96,111; blink=none
face_row_5: eyes=91,145; mouth=96,156; blink=none


## Identity redesign measurement — 2026-11-16

| Raw | a | b | c | d | e | f | g | h | i | j | Measurements / observation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-09 | P | P | P | P | P | P | P | P | F | P | colors 60; heights 68/99/129; width 125; h=.9336; j=.9471; face notes not added at measure |
| raw-10 | P | P | P | P | P | P | P | P | P | P | colors 60; heights 66/95–96/125–126; width 129; h=.9574; j=.9208 |

Reviewed dark 4× image: mature stages read as durian fruit with green-yellow triangular husk spikes around a cream flesh opening; no flower petals, sword or shield. Face is legible with stern brows and blush. Harvest frame 4 reduces to sparse motes. Rows 1–3 blink in frame 3. Face positions (cell-local) are recorded above; row 5 face is visible in frame 4. No distinct detached magenta fringe observed.
