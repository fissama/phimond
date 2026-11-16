# FX candidates — 2026-10-30

Individual PNGs below are presentation candidates, not approved runtime assets. They were selected from the source batch, palette-limited to 48 colors, and visually reviewed as a six-frame contact sheet. They retain the 1152×192 canvas (six 192×192 cells).

## Visual review

- Wind: readable crescent/swirl progression, then dissipates; no obvious detached specks in the selected preview.
- Light: readable flash-to-sparks progression. Tiny dark specks appear around the central flash in frame 3; repair/review before approval.
- Dark: coherent purple crescent progression. Purple pixels near transparent edges are expected by the current heuristic and were preserved; inspect on light background before approval.
- Neutral: readable compact burst-to-sparks progression; a few edge-near pixels flagged by the heuristic.
- Physical hit: readable warm impact burst and contraction to sparks.
- KO dissolve: clear silhouette-to-particles progression. Purple edge-near pixels are preserved as intentional effect color pending light-background review.
- Capture seal: recognizable seal/rune with dissipating particles; confirm runtime scale and pivot.

## Mechanical QA

All seven selected sheets measure 1152×192, use binary alpha [0,255], and have 48 visible colors. Palette application passed. Counts from the edge-color heuristic: wind 0, light 150, dark 4161, neutral 23, physical 0, KO 3558, capture 0. The heuristic flags bright magenta-like colors near transparent pixels; these counts alone do not establish defects, especially for purple FX.

## Not validated

Fixed pivot, per-frame timing, impact scale, engine playback, and owner approval. Do not install or set `approved:true` based on this review.

Art route: existing generated source (`host_image` / Codex built-in ImageGen per prior provenance; model not reported), then local palette/despill processing. No new image-generation call in this continuation.
