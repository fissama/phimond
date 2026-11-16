# cr-xoai — ImageGen prompt and provenance

Prompt family: C06, mango-parrot. Selected packed candidate: `raw-03.png` (SHA-256 `b65cf23816080dc593d107e4866c0e2ec6fdc4d67533553f0bf2afe9732d50da`). It is a 4×5 bright-magenta-key pixel-art atlas with a curved golden mango body, orange beak/face, green leaf wings and tail, seedling/growing/ripe/harvest/plant rows, and small facial-animation changes. The initial two prompts followed `.ai/design/gpt-redo/20-batch-C06-prompt.md`; subsequent iterations targeted smaller cell-contained frames, warm-brown-only outlines, and no pink/violet subject pixels. All generated outputs are preserved as `raw-01.png` through `raw-08.png`.

ImageGen attempt 4 was rejected by the output moderation system and produced no image. Eight image outputs were retained. `raw-03.png` was the only later candidate that packed and passed all mechanical gates. `raw-04.png` through `raw-08.png` failed packing with: `No common scale s≥0.6 fits all frames inside safe bounds; redraw required`.

Reference assets and SHA-256:

- `cr-bac-ha/final.png`: `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`
- `cr-moc-nhi/final.png`: `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`

Character and cell order follow C06 (`cr-xoai`, Lv44): mango-parrot, fruit as body, leaf tail/wings; talkative. Ripe frames open the beak and flap. Atlas is packed by `tools/pack_atlas.py` using the common scale, nearest-neighbor placement, pivot `(96,168)`, magenta key, and shared palette limit. No pixel edits were made.
