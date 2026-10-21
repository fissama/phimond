# Native prop scale — 2026-10-20

Player: 1.31 world units ≈168 pixels. Density:128 pixels/world. Before every new prop generation, job.json records desired_world_size and height_relative_to_player. Draw directly at this small native pixel footprint on a sparse sheet. Extraction may crop, key, palette-map and pad; NEVER resample native props. Reject and regenerate oversize output instead of shrinking it. Existing oversized finals remain draft until replaced with fresh drawing.

Limits: `.ai/design/gpt-redo/07-review-20261020.md`, BỔ SUNG. Handheld props must remain shorter than player; sack area ≤50% of pack/crate/tent. Gate [size] must reach zero. Keep tools/hd2d_audit unchanged.
