# REDRAW-animal-pigeon-peck

Built-in image_gen; raw source saved as `raw-01.png`.

Prompt: one small natural gray pigeon in a side three-quarter view, plump low body, head dipped and short beak pecking, dark eye, folded slate-gray feather bands, small muted rose feet. No ground plane or grain. Keep realistic game scale around 0.55×0.45 world units, warm top-left light, dark slate outline, crisp pixel clusters, transparent margin ≥16%.

References (content/palette, style only):
- `.ai/design/map-checklists/refs/city_square.jpg` SHA256 `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- `art/src/hd2d/batch-09-octopath/race_bird/final.png` SHA256 `debbe2ea4fa5f0e081ba7db95cd9282b1beb754c878e037e5000830fd1dbff86`

Pipeline: alpha threshold >240 to crop object, nearest resize to fit 70×58, place with 8 px transparent margins, binary alpha threshold 127, 40-color quantize.
