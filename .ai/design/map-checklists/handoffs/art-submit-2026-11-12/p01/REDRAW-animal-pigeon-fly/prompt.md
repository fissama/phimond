# REDRAW-animal-pigeon-fly

Built-in image_gen; original raw preserved as `raw-01.png`.

Prompt: one small natural city pigeon in a direct side view mid-flight, body tilted slightly up, raised asymmetric flapping wings, fanned tail, tucked feet, short beak/dark eye. Blue-gray/slate feathers, muted rose feet/beak. Silhouette about 0.47×0.55 world units, transparent margin ≥16%, crisp stepped pixels and warm upper-left light. Avoid shadow, glow, text, watermark, magenta, smooth gradients, extra birds/background.

References (city palette/content, style only):
- `.ai/design/map-checklists/refs/city_square.jpg` SHA256 `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- `art/src/hd2d/batch-09-octopath/race_bird/final.png` SHA256 `debbe2ea4fa5f0e081ba7db95cd9282b1beb754c878e037e5000830fd1dbff86`

Pipeline: crop alpha>240 bbox, nearest resize to fit 60×70, place with 8px margin, binary alpha threshold 127, 40-color quantize.
