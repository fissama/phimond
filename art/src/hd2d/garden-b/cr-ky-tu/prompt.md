# Prompt & provenance — cr-ky-tu

- Art source: built-in ImageGen; existing retained output, no new generation in this continuation.
- C06 source brief: `.ai/design/gpt-redo/20-batch-C06-prompt.md` SHA-256 `bfa29d31a71f28168d1239146291aef37e15ddc9021d221cded3024efa5e0be5`.
- Selected raw source `raw-03.png`, SHA-256 `8e6b503a32158d84dd872f8adae8df12b9df7c29a882ca85c18cef3818716386`.
- References in C06 order: `cr-bac-ha/final.png` SHA-256 `8762627f89c593c6e0992febfb337b2387fd176ddba8e74bffbfa0e883aa73e8`; `cr-moc-nhi/final.png` SHA-256 `2a6f0b7d813c7a6da3f5229c8559d4c593875a9f0df7fc60ce6d810391fa0f51`.
- Character brief: curved pale-green goji branch with red-orange berry-birds; each ripe berry-bird has a small face and chirping personality.
- Sheet brief: 4×5 magenta-key atlas; sprout/grow/ripe distinct sizes; stable loops and blink frames; harvest wave to sparse motes; plant f4 silhouette close to sprout f1; crisp pixel clusters, no baked glow/shadow/blur/text.

## Pipeline v3 source
- Packed candidate selected from `raw-03.png`; see `qa.json` for packed source geometry and measured gates.
- Eight ImageGen outputs were already retained for this asset. Mechanical gate f fails (max body width 144 px > 140 px); visual review records slight pink/violet contour fringe. No pixel edits were made.

## Selected repair source — 2026-11-13

Repacked from `raw-03.png` (SHA-256 `8e6b503a32158d84dd872f8adae8df12b9df7c29a882ca85c18cef3818716386`) with the existing pipeline v3: fixed-pivot component packing, edge-only defringe, shared palette reduction, and measured using `tools/measure_atlas.py`. No manual pixel edits. Latest gate result: 9/10; purple edge count 7441→1853. width 144 px fails f; edge 7441→1853.


## Targeted width repair — 2026-11-16

Built-in ImageGen edited row 3 only, moving outer berry-birds/leaves inward by a few pixels; kept each output as raw-13.png and raw-14.png. Selected raw-14 SHA-256 `cb12d1c484718a529f247228fd8e33026b9315ecb7cec2da2487e56dc7135403`.
