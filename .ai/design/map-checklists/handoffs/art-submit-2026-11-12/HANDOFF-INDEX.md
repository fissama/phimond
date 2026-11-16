# Handoff index — 2026-11-12

Evidence is grouped by CSV kit. `READY` files are review candidates; `FAILED` files are diagnostic evidence; `BLOCKED` copies are unchanged canonical files awaiting manifest/review resolution. None of these labels means Claude accepted the image.

| Kit | READY ART | FAILED ART | BLOCKED source copy | READY montages | FAILED montages | BLOCKED montages |
|---|---:|---:|---:|---:|---:|---:|
| ancient | 2 | 1 | 4 | 1 | 1 | 1 |
| arena2 | 0 | 0 | 44 | 0 | 0 | 0 |
| astral | 0 | 3 | 0 | 0 | 1 | 0 |
| batch-00 | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-01-octopath | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-02-octopath | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-03-octopath | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-05-octopath | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-09-octopath | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-10-octopath | 0 | 0 | 0 | 0 | 0 | 0 |
| batch-13-release | 0 | 0 | 0 | 0 | 0 | 0 |
| battlefield | 18 | 18 | 14 | 2 | 2 | 0 |
| beach | 0 | 0 | 0 | 0 | 0 | 0 |
| city | 0 | 0 | 0 | 0 | 0 | 0 |
| crossroads | 4 | 8 | 4 | 1 | 1 | 1 |
| desert | 7 | 4 | 0 | 1 | 1 | 0 |
| dungeon | 1 | 9 | 43 | 1 | 2 | 0 |
| forest | 2 | 0 | 0 | 1 | 0 | 0 |
| garden | 2 | 0 | 3 | 1 | 0 | 0 |
| ghost_castle | 3 | 3 | 0 | 1 | 1 | 0 |
| guild | 5 | 13 | 51 | 1 | 10 | 1 |
| maya | 18 | 3 | 29 | 2 | 0 | 0 |
| maze | 23 | 22 | 5 | 3 | 3 | 0 |
| minigame | 0 | 0 | 58 | 0 | 0 | 0 |
| nightmare | 11 | 9 | 0 | 2 | 1 | 0 |
| octopath-s01-s27-20261029 | 0 | 0 | 0 | 0 | 0 | 0 |
| p01 | 7 | 3 | 40 | 1 | 1 | 5 |
| p01-release-art-20261023 | 0 | 0 | 0 | 0 | 0 | 0 |
| ship | 1 | 0 | 0 | 1 | 0 | 0 |
| tomb | 10 | 7 | 0 | 2 | 1 | 0 |
| tower | 21 | 28 | 1 | 3 | 4 | 0 |
| windrock | 6 | 6 | 0 | 1 | 1 | 0 |
| world_tree | 4 | 1 | 0 | 1 | 1 | 0 |


## Resume additions — dungeon floor extras

ImageGen was available; Runway was not used. Five dungeon floor extra tasks exhausted three raw attempts each and remain FAILED_AFTER_3_TRIES. The three postprocess candidates for extras 01–03 achieved wrap=0/0 mechanically but failed 3×3 and 4×4 visual review due to cross-shaped blend streaks and repeated cadence.

- 3×3 kit montage: [montage-3x3-resume-floor-tiles.png](dungeon/montage-3x3-resume-floor-tiles.png)
- [Extra 01 tileable postprocess 3×3](dungeon/NEW-dungeon-floor-extra-01/preview-3x3-tileable-postprocess.png)
- [Extra 02 tileable postprocess 3×3](dungeon/NEW-dungeon-floor-extra-02/preview-3x3-tileable-postprocess.png)
- [Extra 03 tileable postprocess 3×3](dungeon/NEW-dungeon-floor-extra-03/preview-3x3-tileable-postprocess.png)
- [Extra 04 attempt 03 3×3](dungeon/NEW-dungeon-floor-extra-04/preview-3x3-attempt-03.png)
- [Extra 05 attempt 03 3×3](dungeon/NEW-dungeon-floor-extra-05/preview-3x3-attempt-03.png)

- Guild floor postprocess montage: [montage-3x3-resume-floor-postprocess.png](guild/montage-3x3-resume-floor-postprocess.png); extras 02–04 retained FAILED after 3×3/4×4 grid/cadence review.

- Dungeon edge 01 raw/postprocess QA: [3×1 attempt 03](dungeon/NEW-dungeon-edge-01/preview-3x1-attempt-03.png), [tileable postprocess 3×1](dungeon/NEW-dungeon-edge-01/preview-3x1-tileable-postprocess.png), [qa.json](dungeon/NEW-dungeon-edge-01/qa.json).


## Resume update — battlefield shadow redo-v2

- `NEW-battlefield-shadow-01` replacement attempts 1–3: [redo-v2 raw outputs](battlefield/NEW-battlefield-shadow-01/redo-v2/).
- All three renders retain soft alpha with 256 levels; requested stepped/dither treatment was not achieved. The task is recorded FAILED_AFTER_3_TRIES. Existing candidate was left unchanged.


## Resume update — battlefield shadows 01–04 redo-v2

Each shadow has three new raw attempts under its `redo-v2/` folder. ImageGen continued producing smooth alpha (256 levels); glow/halo is visible on some outputs. These replacements are recorded FAILED_AFTER_3_TRIES, with prior candidates left untouched. No Runway used.


## Resume update — guild backdrop far

- [`NEW-guild-backdrop-far-01` 3×3 diagnostic montage](guild/NEW-guild-backdrop-far-01/redo-v3/montage-3x3.png): 3 attempts; numeric seam on best=2.73, autocorr=0.603, retained FAILED.


## Resume update — guild floor extras

- `NEW-guild-floor-extra-01` 3×3: [tileable postprocess preview](guild/NEW-guild-floor-extra-01/redo-v3/preview-3x3-tileable-postprocess.png) — repeated slab motif; FAILED.
- `NEW-guild-floor-extra-02` 3×3: [tileable postprocess preview](guild/NEW-guild-floor-extra-02/redo-v3/preview-3x3-tileable-postprocess.png) — repeated broad slabs; FAILED.
- `NEW-guild-floor-extra-03` 3×3: [tileable postprocess preview](guild/NEW-guild-floor-extra-03/redo-v3/preview-3x3-tileable-postprocess.png) — repeated central diagonal motif; FAILED.
- `NEW-guild-floor-extra-04` 3×3: [tileable postprocess preview](guild/NEW-guild-floor-extra-04/redo-v3/preview-3x3-tileable-postprocess.png) — repeated slab cadence; FAILED.
- `NEW-guild-floor-extra-03` 3×3: [tileable postprocess preview](guild/NEW-guild-floor-extra-03/redo-v3/preview-3x3-tileable-postprocess.png) — repeated diagonal motif; FAILED.


## Resume update — guild edge

- `NEW-guild-edge-01`: [3×1 preview](guild/NEW-guild-edge-01/redo-v3/preview-3x1.png) — high autocorr and repeated mound; FAILED.


## Resume update — guild edge 02

- `NEW-guild-edge-02`: [3×1 preview](guild/NEW-guild-edge-02/redo-v3/preview-3x1.png) — autocorr 0.75699 and recurring mound/ivy; FAILED.


## Resume update — guild edge 03

- `NEW-guild-edge-03`: [3×1 preview](guild/NEW-guild-edge-03/redo-v3/preview-3x1.png) — autocorr 0.78934 with repeated rubble peaks; FAILED.


## Resume update — guild decal 01

- `NEW-guild-decal-01`: [candidate and 4× previews](guild/NEW-guild-decal-01/redo-v3/preview-4x-light.png) — rubble cutout with thresholded alpha; READY_FOR_CLAUDE_REVIEW.


## Resume update — guild decals

- `NEW-guild-decal-01`: [candidate preview](guild/NEW-guild-decal-01/redo-v3/preview-4x-light.png) — thresholded debris cutout; no visible halo; READY_FOR_CLAUDE_REVIEW.
- `NEW-guild-decal-02`: [candidate preview](guild/NEW-guild-decal-02/redo-v3/preview-4x-light.png) — cracked paving scuff distinct from debris; READY_FOR_CLAUDE_REVIEW.


## Resume update — guild backdrop mid

- `NEW-guild-backdrop-mid`: [3×1 attempt 03](guild/NEW-guild-backdrop-mid/redo-v1/preview-3x1-attempt-03.png) — seam 8.64, 48 colors, opaque; visible parapet/shrub cadence repeats, FAILED after 3 attempts.

- `NEW-guild-backdrop-near`: [3×1 attempt 03](guild/NEW-guild-backdrop-near/redo-v1/preview-3x1-attempt-03.png) — seam 1.15, 48 colors, opaque; shrub/pier/gap cadence repeats, FAILED after 3 attempts.

- `NEW-guild-portal-dormant`: [4× preview](guild/NEW-guild-portal-dormant/redo-v1/preview-4x.png) — 48 colors, binary alpha, margin 8px; candidate READY, pair mask comparison pending active counterpart.
- `NEW-guild-portal-active`: [4× preview](guild/NEW-guild-portal-active/redo-v1/preview-4x.png) — mask matches dormant exactly, 48 colors, binary alpha, margin 8px; candidate READY.
- `NEW-guild-marker-arrival`: [4× sprite sheet preview](guild/NEW-guild-marker-arrival/redo-v1/preview-4x.png) — 4 frames, 47 colors, binary alpha, 23px margin each; READY candidate.
- `NEW-guild-fx-01`: [4× preview](guild/NEW-guild-fx-01/redo-v1/preview-4x.png) — 4 frames, 48 colors, binary alpha, margin 8px; READY candidate.
- `NEW-guild-fx-02`: [4× preview](guild/NEW-guild-fx-02/redo-v1/preview-4x.png) — four dispersing particle frames, 47 colors, binary alpha, 8px margin; READY.
- `NEW-guild-fx-03`: [4× preview](guild/NEW-guild-fx-03/redo-v1/preview-4x.png) — 4-frame ascending/dispersing particles, 46 colors, binary alpha, 8px margins; sparse fragments noted.
- `NEW-guild_fortress-landmark-01`: [4× preview](guild/NEW-guild_fortress-landmark-01/redo-v1/preview-4x.png) — sandstone gatehouse landmark, 48 colors, binary alpha, margin 8px; READY.
- `NEW-guild_treasury-landmark-01`: [4× preview](guild/NEW-guild_treasury-landmark-01/redo-v1/preview-4x.png) — marble treasury pavilion, 48 colors, binary alpha, margin 8px; READY.
- `NEW-guild_warehouse-landmark-01`: [4× preview](guild/NEW-guild_warehouse-landmark-01/redo-v1/preview-4x.png) — timber storehouse, 48 colors, binary alpha, margin 8px; READY.
- `NEW-guild_barracks-landmark-01`: [4× preview](guild/NEW-guild_barracks-landmark-01/redo-v1/preview-4x.png) — barracks landmark, 48 colors, binary alpha, margin 8px; READY.
- `NEW-guild_shop-landmark-01`: [4× preview](guild/NEW-guild_shop-landmark-01/redo-v1/preview-4x.png) — guild storefront landmark, 48 colors, binary alpha, margin 8px; READY.
- `NEW-guild_pet_stable-landmark-01`: [4× preview](guild/NEW-guild_pet_stable-landmark-01/redo-v1/preview-4x.png) — pet stable landmark, 48 colors, binary alpha, margin 8px; READY.

- `NEW-maya-floor-01`: [attempt 03 3×3](maya/NEW-maya-floor-01/redo-v1/preview-3x3-attempt-03.png) — seam=0/0, 48 colors, but large slab cadence repeats; FAILED after three raw attempts.


Maya resume candidates: 14 READY images and 3 FAILED diagnostic sets, with two 3×3 montages under `maya/`.


Maya handoff contains 18 READY art images, 3 FAILED diagnostic sets, 29 BLOCKED source copies, and two 3×3 READY montages.
