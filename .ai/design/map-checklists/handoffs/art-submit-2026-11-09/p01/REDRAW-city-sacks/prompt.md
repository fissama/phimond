# REDRAW-city-sacks

Built-in image_gen, one generated raw frame, source preserved as `raw-01.png`.

Prompt: Compact pair of tied burlap market sacks, one squat tan and one smaller muted olive-brown, coarse woven cloth indicated with broad pixel clusters, folded necks tied with dark cord. No crates or spilled goods. Whole silhouette about 0.8 world units wide and under 0.65 units tall; upper-left light, dark warm-brown outlines, 2–4 firm tones, crisp HD-2D pixel-art, transparent background with ≥12% margin. Avoid ground shadow, glow, text, watermark, magenta/pink/violet, white fringe, smooth gradient.

References: map content/palette then style anchor.
- `.ai/design/map-checklists/refs/city_market.jpg` SHA256 `91b5e2aea26c8caba904c53c96a0e3f995da3a40952a2f10e2fa87e7f486a9f5`
- `art/src/hd2d/batch-01-octopath/bush-01/final.png` SHA256 `15573d1325946dd41c0faa0ef7ea8bc4c7f7a7910ea85a93de16766a4f4f1830`

Pipeline: alpha threshold >240 to exclude low-alpha glow; crop alpha bbox; nearest resize to 94×76; place on 112×96 canvas; 40-color quantize; binary alpha threshold 127. Pivot between sacks at base (0.5, 0.91).
