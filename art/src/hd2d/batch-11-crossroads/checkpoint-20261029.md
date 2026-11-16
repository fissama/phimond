# Crossroads checkpoint — 2026-10-29

Current work: Crossroads kit, per user's request to continue the next map kits after Nightmare. Checklist/manifest owner approval remains unchecked / false.

## Status

- Shared floors 01–05, props 01–17, far layers 01–02, floor extras 01–03, decals 01–12, shadows 01–04, mid/near backdrops, portal pair, arrival marker, water foam, and FX 01–03 have selected assets checked as Vẽ. All Duyệt fields remain blank.
- Floors 01–03 currently pass seam QA: X/Y max 0, uniform outer 8px. Previous checkpoint's seam errors are stale.
- Remaining kit checklist rows: edge-01/02/03 and shared far backdrop. Map-specific landmark table records reuse/no-additional-asset cases; map 02 crate stack is the one selected unique landmark.

## Attempts this continuation

- Edge-01: four fresh image_gen raws plus crop/palette tests preserved at `jobs/edge-repair-01/`. Rejected for bevel/soft shading, noisy ground, lack of a clear material boundary, high partial alpha, palette/seam issues. No final selected.
- Far backdrop: two image_gen raws and a crop/nearest-scale/palette candidate preserved at `jobs/backdrop-repair-01/`. The candidate reached 36 colors but the cave silhouette visibly breaks at the horizontal tile join; rejected before packaging.
- Current official multi-kit gate: exit 0, 293 assets across five kits, 0 errors, 0 warnings. This does not certify unselected attempts or owner approval.

Next: continue image_gen redraws for the remaining Crossroads edges/backdrop; preserve every rejected raw; only update manifest/contact sheet after an asset passes visual and mechanical QA.

## Continuation after Claude review — 2026-10-29

- Floor repeat redraft study: four new image_gen raws retained under `jobs/floors-repeat-redraft-20261029/`; none resolves the visible repeat pattern or exact tile seams. No floor final changed.
- Edge study: one sheet retained under `jobs/edges-study-20261029/`; bands are oversized (153–159 px vs 128 px), semi-transparent, over-palette, bevel-lit, and have nonzero horizontal seam differences. No edge was promoted.
- Current `sh tools/check_hd2d_art.sh`: **293 assets, 0 errors, 0 warnings**. Job-only studies are outside manifest.
