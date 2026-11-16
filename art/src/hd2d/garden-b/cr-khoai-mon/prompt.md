# Prompt/provenance — cr-khoai-mon

## Asset brief
Khoai Môn — voi con củ khoai, tai lá tím, hiền và thích hứng nước.

## Contract
- 4×5 sheet, pure #FF00FF backing, packed by garden-b/tools/pack_atlas.py; 768×960 RGBA atlas.
- HD-2D Octopath pixel art, hard pixel clusters, same-tone outlines, no baked shadow/glow/text.
- Crop: visible cute face; distinct sprout/grow/ripe sizes; loop rows blink; harvest and plant are one-shot.

## Source provenance
- Selected packed source: `raw-06.png` (sha256 `e05bad957390bb5179d32410eb6613e6e1fd1b5fe07aa6688cef6087bcfc7714`).
- ImageGen outputs in this continuation: 2 (`raw-05.png`, `raw-06.png`); earlier raw-04 failed packing. Both new raw files are retained.
- Current final is checked in `qa.json`; review findings are in `review.md`.
