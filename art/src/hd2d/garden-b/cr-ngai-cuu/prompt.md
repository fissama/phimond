# Prompt & provenance — cr-ngai-cuu

- Source tool: built-in Codex `image_gen` only; 8 outputs retained as `raw-01.png` through `raw-08.png`.
- Selected sheet: `raw-08.png`; SHA-256 `1acb962eaf8f5f2c9cb675e868fa1067905c4e097b5478af0dea05185bc559ce`.
- Final atlas: `final.png`; SHA-256 `d646705c07781a4b5d84ca4bb9bb4e8a404f4e11e78db092422e98ca7200e372`. Packed with `tools/pack_atlas.py`; nearest-neighbor common scale 0.696463; no pixel edits.
- Sprout reference attached: `reference-sprout-f1.png`; SHA-256 `ba6f9bf23a9123a8790ceedcdacb358a9bf7d9a9ced212b3dc69f9be62427402`.
- Other references attached:
  - `cr-bac-ha/final.png`: `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
  - `cr-moc-nhi/final.png`: `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`
  - `DocDangNu/sprites.png`: `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Brief: 4×5 sprite atlas with 192px cells and magenta key; a gentle sleepy silver-gray woolly lamb formed from lobed mugwort leaves. Rows are sprout, grow, ripe, harvest, plant. The plant begins as seed in soil and frame 4 matches sprout frame 1. Each looping row blinks. Ripe is curled asleep; harvest waves and ends in sparse rays. Intended sizes after packing: 45–75 / 85–112 / 120–150px, width ≤140px. Pixel style uses stepped clusters, matching dark outlines, no blur, glow, baked shadow, text or fog.

All 8 image_gen outputs are preserved. Full request wording is recorded in generation history and constrained by the brief above. Result passes mechanical gates a–j; visual style remains blocked because violet/magenta contour pixels persisted after attempt 8.
