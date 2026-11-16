# REDRAW-city-lion-fountain

Built-in image_gen; two raws preserved as `raw-01.png` and `raw-02.png`.

Prompt: standalone winged angel fountain matching the city-square source map, despite the asset ID saying lion. Pale cream limestone angel, circular shallow turquoise-water basin, front three-quarter view; muted tan/olive-gray shadows, restrained teal. Crisp HD-2D stepped clusters, warm upper-left light, full silhouette and transparent margin. No background, ground plane, shadow, glow, text, watermark, magenta, or gradient.

Source content/palette and approved style/fountain references:
- `.ai/design/map-checklists/refs/city_square.jpg` SHA256 `995db064ece8534304239e06d3882dc472bde1b9a2198a7784d127bfaad61cf0`
- `art/src/hd2d/batch-02-octopath/city-statue/final.png` SHA256 `08f3e6e6e486638546ce9e7f87a173354a5660a674dbb597544d7a012cfb82a1`
- `art/src/hd2d/batch-02-octopath/fountain-body/final.png` SHA256 `62e3c2ccba6422e73cb1f3dc6de3ea5c2cb72ed392df1a7695be6e1359e68802`

Decision: source `city_square.jpg` visibly shows an angel fountain, so that source-of-truth subject overrides the CSV asset name `city-lion-fountain`.
Pipeline: alpha>250 bbox crop; nearest resize to fit 179×214; center on 195×230 canvas; binary alpha threshold 250; 40-color quantize.
