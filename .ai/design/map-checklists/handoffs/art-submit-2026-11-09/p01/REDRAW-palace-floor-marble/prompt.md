# REDRAW-palace-floor-marble

Built-in image_gen; raws `raw-01.png` through `raw-03.png`.

Prompt: top-down opaque matte palace marble floor, dark slate blue-gray palette from palace map; subtle irregular mineral clouds/veins; no carpet, walls, objects, grout grid, repeated swirls, shadows/glow/text/magenta. Crisp stepped pixel clusters, low contrast, all four edges seamless.

References:
- `.ai/design/map-checklists/refs/city_royal_palace.jpg` SHA256 `4824318a48f0ad36193b7aa73689f7929175b3468a02695f6cd554b3cabbd524`
- `art/src/hd2d/batch-02-octopath/hall-floor-stone/final.png` SHA256 `ef1a3edea0bc8778d42bb8c64e7bb3cf51c78e4a06971500efd36851bb5ba142`

Pipeline: crop 512×512 from raw (attempt crop search), nearest at source resolution, quantize to 40 colors.
