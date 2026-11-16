# REDRAW-astral-floor-extra-03

Raw generations: `raw-01.png` through `raw-03.png`; candidate is the best seam attempt (attempt 2). Sources: CSV prompt, astral maps and dirt-floor anchors. Processing: nearest resize 512x512 and 40-color median-cut quantization without dithering. All iterations are fresh imagegen outputs or a targeted edit.

Attempt metrics are recorded in `qa.json`. No attempt met wrap x/y <=1.25 (best wrap x=1.409), so this is `FAILED_AFTER_3_TRIES`; a Claude reviewer can judge visual continuity separately. `repeat-3x3.png` shows the best attempt. Art gate not run because candidate is handoff-only and pre-acceptance manifest registration is forbidden.
