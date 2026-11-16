# Triệu Linh Điện — HD-2D layer kit review

This is a set of separate scene textures for the existing Three.js HD-2D renderer. It is not a single composed map image.

## Layers

| Layer | Source | Scene use |
|---|---|---|
| Far city | `raw/far-city.png` | Opaque distant `back` plane behind architecture. |
| Marble column | `column-extract/marble-column/prop.png` | One transparent reusable billboard sprite, placed six times at X = −7.5, −4.5, −1.5, 1.5, 4.5, 7.5 (3 world units apart), at a shared rear Z depth. Display size is 1.28×3.2 world units. |
| Lintel module | `raw/lintel-module.png` | Separate upper `props` plane behind the columns; depth lets the columns overlap it. |
| Stone floor | `raw/stone-floor.png` | Repeating horizontal `floor` plane. |
| Foreground threshold | `threshold-extract/threshold-left/prop.png`, `threshold-extract/threshold-right/prop.png` | Two low front props at the near map edge, with a centered exit gap. |

`column-extract/prop-pack.json` records the crop, measured foot anchor and source SHA. Extractor QA passes with one accepted sprite and no warnings. The source pixels were palette-finished with the established environment palette before extraction.

`threshold-extract/prop-pack.json` records both threshold crops. Its `edge_touch` warning is expected: each piece deliberately reaches the outside edge of the map; the center ends remain separated for the exit.

## Renderer preview

The game scene is `apps/game-web/public/scenes/summoning_hall_main_hall.json`, keyed by the live map ID. It uses floor, back and prop layers with independent world coordinates and Z ordering, plus the three summon pedestals and split foreground threshold. The local renderer preview is available at:

`http://127.0.0.1:5173/scene.html?map=summoning_hall_main_hall&x=0.5&q=high`

The renderer now honors optional `y` offsets on `back` layers; omitted values still resolve to zero. This allows the far city to extend behind the column openings without flattening the scene into one image.

## Status

The layers are connected to the live map scene ID. The older `columns-redraw-01/final.png` six-column strip and its comparison board are superseded 2D studies, not the HD-2D deliverable. The separate `summoning_hall_hd2d_review.json` remains a visual sandbox; the game uses `summoning_hall_main_hall.json`.
