# Triệu Linh Điện — aligned colonnade candidate

Redraw the uneven columns visible in the v1.0.0 Summoning Hall reference as a reusable foreground colonnade. Target scene width is 19 map tiles and must preserve the open play area and central summon-pedestal sightlines. Reference screenshot: `/Users/phileanh/Downloads/Phimond-P12-Review/map-images/summoning_hall_main_hall.png` (SHA-256 `ce0dea34c91e401e5050a4c217fde2dbe34da4aac8ba0aa2309f949b73213621`). Material/style anchors: approved `hall-wall-stone/final.png` and the new `scene-edges/city-backdrop/final.png`.

Generation request: one wide transparent foreground layer, with exactly six matching ivory marble columns, uniform shaft/capital/base dimensions, even spacing and equal outer margins; one straight, continuous shallow cornice; broad clear window gaps; restrained gold trim; warm upper-left light; crisp clustered Octopath-like HD-2D pixel finish. No sky/city, wall fill, curtains, banners, floor, actors, summon props, text or UI. Preserve actual alpha transparency.

Route: built-in Codex ImageGen (`host_image`). Raw output is `raw-01.png`; model identity is not exposed by the host tool. The generation is a first visual candidate, not owner-approved or runtime-integrated.

Processing: columns and lintel were measured, separated and composed into a 2432×384 layer. The six column centers are 200, 606, 1012, 1418, 1824 and 2230 px (406 px spacing). Final colors were snapped to the existing 48-color environment-inserts palette using `generate2dsprite/scripts/palette_tool.py apply`.

This first pass produced `final.png` and `columns-context-preview.jpg`, but that assembled strip was a flat 2D study and is **superseded**. Do not use it as the game scene. The current deliverable is the separated sprite in `../hd2d-layer-kit-01/column-extract/marble-column/prop.png`, placed as six world-space props by `apps/game-web/public/scenes/summoning_hall_hd2d_review.json`.
