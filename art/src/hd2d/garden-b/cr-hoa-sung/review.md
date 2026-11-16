# Review — cr-hoa-sung

## Face notes

face_row_1: eyes=96,137; mouth=96,150; blink=frame1
face_row_2: eyes=96,112; mouth=96,126; blink=frame3
face_row_3: eyes=96,82; mouth=96,96; blink=frame2
face_row_4: eyes=96,88; mouth=96,104; blink=none
face_row_5: eyes=96,143; mouth=96,153; blink=none

## Visual review

Raw-01 sheet inspected: cute waterlily-mermaid identity and ripe singing action read clearly; the water rings are separate small effects. Pending packed-image review and a–j measurement.

## Gate history

| Source | a | b | c | d | e | f | g | h | i | j | Result |
|---|---|---|---|---|---|---|---|---|---|---|---|
| raw-01 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 62/101/130, width 125 | N/A | PASS 0.8791 | PASS | PASS 0.8561 | 10/10 |
| raw-02 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 61/99–101/129–131, width 133 | N/A | PASS 0.9321 | PASS | PASS 0.8915 | 10/10 |
| raw-03 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 62–63/101–102/130–133, width 131 | N/A | PASS 0.9462 | PASS | PASS 0.8786 | 10/10 |
| raw-04 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 63/100–103/130–134, width 133 | N/A | PASS 0.9408 | PASS | FAIL 0.8323 | 9/10 |
| raw-05 | PASS | PASS | PASS | PASS 60 colors | PASS | PASS heights 63/101–102/130–139, width 135 | N/A | PASS 0.9522 | PASS | FAIL 0.8032 | 9/10 |
| raw-06 | FAIL | — | — | — | — | — | N/A | — | — | — | PACK FAIL: no common scale s≥0.6 |
| raw-07 | FAIL | — | — | — | — | — | N/A | — | — | — | PACK FAIL: no common scale s≥0.6 |
| raw-08 | FAIL | — | — | — | — | — | N/A | — | — | — | PACK FAIL: no common scale s≥0.6 |

## Final visual review and disposition

Opened the selected candidate at 4× on checker and dark backgrounds. The character is readable and proportions/poses are sound. A thin pink-violet contour fringe remains visible around the green silhouette, outside the flower-petal fill. Read-only edge scan of raw-03 found 17,236 pixels with HSV hue 0.77–0.94, saturation ≥0.30 and value ≥0.15 among non-key boundary pixels. After all 8 atlas outputs, no candidate satisfies both visual style and measured packaging. The selected final is therefore marked blocked despite a–j passing mechanically; no pixel edits were made.


## Edge defringe — 2026-11-12

Repacked from `raw-03.png` with edge-only defringe. Purple-hued rim pixels (hue 270°–345°, saturation >0.2): 7342 before, 2256 in final quantized atlas; 6324 pixels replaced. Mechanical gates: 10/10. Dark 3× previews: `defringe-before-3x-dark.png` and `defringe-after-3x-dark.png`.
