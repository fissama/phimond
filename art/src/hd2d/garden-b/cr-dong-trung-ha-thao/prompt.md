# cr-dong-trung-ha-thao — generation and packing record

Built-in ImageGen; 8 outputs, all retained as `raw-01.png`–`raw-08.png`. Selected and packed source: `raw-08.png` (SHA256 `28744c68249b870d5e2fcc095d0ad987bd132c4a5273e284724f4a1a5af5abd6`). Final SHA256: `e93bde4c6f4168b2af9ba98d62f180c636ead4d8ba2d4f395879e97374ce0a67`.

Style references attached for the initial generation, in this order: garden-b/cr-bac-ha/final.png (SHA256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`), garden-b/cr-moc-nhi/final.png (SHA256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`). Later revisions used prior raw sheets as edit references.

Prompt intent: friendly sleepy pale-yellow segmented larva with short amber-orange mushroom stalk; five animation rows sprout, grow, ripe, harvest and plant; compact character; blink in rows 1–3; plant frame 4 matches sprout frame 1. Source sheet uses flat #FF00FF key background. Palette restricted to cream, amber, orange, olive and warm brown; hard pixel edges; no magenta/purple contour, text, glow or baked shadows.

Pipeline: `tools/pack_atlas.py --id cr-dong-trung-ha-thao --kind crop --raw raw-08.png`, then `tools/measure_atlas.py` and `tools/export_previews.py`. Mechanical result 10/10; manual visual contour gate fails.
