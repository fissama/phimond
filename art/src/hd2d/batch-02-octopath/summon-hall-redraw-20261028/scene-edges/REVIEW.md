# Triệu Linh Điện — scene edge redraw review

## Scope

Candidate redraw of the complete visible scene treatment for the 19×11 Summoning Hall: far city backdrop, stone floor, and lower foreground threshold. The map data places the existing exit at x=8–10, y=9–10; the foreground trim leaves a centered opening aligned to that route. The city plate is authored behind the colonnade and the foreground trim stays at the lower map edge.

The city plate, stone tile and column master were generated with the repository's built-in Codex ImageGen route (`host_image`) using scene/style references. Palette and extraction tools were applied. The HD-2D layers are now connected to the scene file keyed by the live map ID; manifest approval status has not been changed.

## Candidate assets

| Asset | File | Dimensions | QA and use |
|---|---|---:|---|
| Far city backdrop | `city-backdrop/final.png` | 1216×405 | QA pass; conform and palette application pass; 48 colors. Fixed full-width exterior plate, not tileable. `max_delta_e` was skipped because no threshold is configured. |
| Stone floor | `stone-floor/final.png` | 512×512 | QA and palette application pass; 34 colors; no extraction warnings. Wrap-edge checks report `continuous` on X (ratio 0.236873) and Y (0.229589), but `seamless_verified` is false. Inspect repeated use in the target renderer before approval. |
| Foreground threshold | `foreground-edge/final.png` | 2432×280 | Extraction and palette application pass; 48 colors; binary alpha; no extraction warnings. Center gap is x=1029–1402, width 374 px (about 2.92 tiles vs. the 3-tile/384 px target). Fixed full-width trim, not tileable. |
| HD-2D layer kit | `hd2d-layer-kit-01/` | Separate textures | City as far plane, one transparent column sprite reused at six equal X intervals, independent lintel prop, repeating floor plane, split left/right foreground threshold. Column extraction QA passes. Threshold extraction warns because both props intentionally touch the map's outside edges. Main scene: `apps/game-web/public/scenes/summoning_hall_main_hall.json`. |

The art manifest still marks the original three edge assets as candidates. The scene layer kit is integrated under the real map ID in the working tree and appears in the renderer preview; release acceptance is not recorded.

## Review limitations

- `foreground-edge/qa.json` contains a `superseded_forge_experiment` warning (`source_edge_touch_frames` at frame [0,0]). It belongs to the earlier square sprite experiment, not `foreground-edge/final.png`; the full-width candidate's own extraction warnings are empty.
- `threshold-extract/prop-pack.json` warns `edge_touch` for `threshold-left` and `threshold-right`; both segments intentionally terminate at the outer map bounds. The center opening is 374 px (2.92 world units at the fitted scene scale) vs the 3-tile / 384 px target.
- Floor seam measurements are comparative continuity checks, not proof of exact pixel matching across opposite edges.
- The far backdrop's `max_delta_e` check is skipped (no configured threshold); palette membership and application checks pass.
- `scene-edges-preview.png` is the earlier flat layer board, not the in-engine result. The current in-engine preview uses `scene.html?map=summoning_hall_main_hall&x=0.5&q=high`.
- `columns-redraw-01/final.png` and `columns-context-preview.jpg` are superseded flat 2D studies; do not use them as the HD-2D result.
- The main HD-2D scene uses independent world positions and depth. The renderer also now honors optional `y` offsets for back layers, defaulting to 0 so existing scenes retain their placement.

## Provenance

- Per-asset prompts, generation hashes, reference list and processing notes are in each asset's `prompt.md`.
- Per-asset machine-readable checks are in each asset's `qa.json`; concise visual notes are in each asset's `review.md`.
- Composite preview: `scene-edges-preview.png`.
- Column image prompt and generation history: `columns-redraw-01/prompt.md`; the reusable extracted sprite and crop QA live under `hd2d-layer-kit-01/column-extract/`.
- Source scene definition: `data/maps/p01/summoning_hall_main_hall.json`.

## Decision

**HD-2D scene layers are wired to the live map ID and render in the game's Three.js scene viewer. The art manifest remains pending owner review.**
