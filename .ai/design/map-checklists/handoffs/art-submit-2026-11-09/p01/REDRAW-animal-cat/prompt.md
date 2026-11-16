# REDRAW-animal-cat

Built-in image_gen; raw source saved as `raw-01.png`.

Prompt: one compact alert street cat sitting with curled tail beside forepaws, side three-quarter view, upright ears, whiskers and eyes. Muted gray-brown tabby fur with cream chest/muzzle, dark warm-brown outlines, upper-left warm light. Approx 0.58×0.75 world units. No ground/shadow. Crisp stepped pixels, 2–4 tones, transparent margin. Avoid glow, text, watermark, magenta/neon, smooth gradients, extra animals/background.

References (content/palette, style only):
- `.ai/design/map-checklists/refs/city_market.jpg` SHA256 `91b5e2aea26c8caba904c53c96a0e3f995da3a40952a2f10e2fa87e7f486a9f5`
- `art/src/hd2d/batch-09-octopath/race_bird/final.png` SHA256 `debbe2ea4fa5f0e081ba7db95cd9282b1beb754c878e037e5000830fd1dbff86`

Pipeline: alpha>240 bbox crop, nearest resize within 74×96, 8px canvas margin, binary alpha threshold 127, 40-color quantize.
