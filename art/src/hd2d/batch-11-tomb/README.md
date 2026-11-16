# Batch 11 — Lăng Mộ (`kit_tomb`)

## Trạng thái — 2026-11-03

- 76 asset candidates in manifest; all remain `approved: false`.
- Coverage: 8 floor, 3 edge, 39 prop, 13 decal, 4 procedural shadow, 3 backdrop, 2 portal, 1 spawn marker, 3 FX.
- 18 map landmark rows were reviewed against the nine source map images. They reuse two shared foliage props (dry sapling and orange bloom); screenshots do not show 18 distinct named monuments.
- Portal redraw pair uses a shared binary alpha mask. Far/mid/near backdrop candidates include repeat previews and a stacked composite preview. Repeating motifs remain visible at long close inspection; final scene composition and owner review are pending.
- Latest full art gate (rerun 2026-11-03) scanned 494 assets and found one unrelated Ancient floor seam error; no Tomb-kit error. This is mechanical QA, not art approval.
- Contact sheet was regenerated from the current manifest after the final decal redraw; every asset keeps raw source, prompt/provenance and review/QA files where listed.
- `tomb-floor-cracked-slate` was redrawn as candidate 04 from a saved raw source. Final-size QA: 512×512, 48 colors, X seam 5.807, Y seam 4.620; 3×3 repeat reviewed. Owner approval remains false.
- `tomb-graveyard-dirt` redraw 01 and `tomb-floor-ashen-dust` redraw 03 are now selected candidates with 48 colors and final-size seam means 2.766/2.740 and 5.793/5.705. Their raw-01 sources remain preserved; new raw-02 sources and prompts are recorded.
- Brick-floor and dry-gravel redraw attempts were rejected after visual repeat review despite passing numeric seam means; raw and candidate previews are retained under `jobs/floors-redraw-20261103/`.
- Latest full art gate scanned 494 assets across configured kits and reported one existing failure: `[audit] batch-11-ancient/ancient-floor-02: SEAM_X 14.2/8.1`. No tomb-kit error was reported; full gate is not clean until the Ancient tile is fixed.

- `tomb-floor-crypt-mossstone` redraw attempts 02–04 were generated and inspected; none was promoted. 02/03 pass edge means (3.383/3.665 and 0.970/1.581) but fail visual/style review; 04 fails both seams (6.389/6.941; threshold 6) and visual repeat. 05/06 pass seams (4.873/4.508 and 4.359/5.975) but remain too mottled/soft and repeat visibly. Raw files, candidate renders, 3×3 previews, prompts and QA are preserved under `jobs/floors-redraw-20261103/`. The current manifest final remains unchanged.
- Manifest revision is 37; contact sheet was rebuilt after the manifest update and is newer than the manifest.

- `tomb-tile-edge-decal` redraw 03 is the current replacement draft: 512×512, 48 colors, seam X/Y 3.585/5.775, 3×3 cadence is low contrast but still visible at close inspection. Earlier draft and all retries are preserved under `jobs/tile-edge-redraw-20261103/`; current candidate remains `approved:false`.

- `tomb-necropolis-wall-far` redraw 03 was packaged as an unapproved draft; original output, QA and previews are backed up under `jobs/backdrop-far-redraw-20261103/`.

## Review shortlist

1. `tomb-necropolis-wall-mid` / `near`: seams meet, but the wall motif repeats visibly across long spans.
2. `tomb-decal-moss-soil`: readable irregular silhouette, but texture looks softer than the approved prop cluster style at 4×.
3. `tomb-fx-stone-chips-01`: clear six-chip burst, though the stone shading is softer than the cleanest approved assets.

Claude/owner must decide visual approval. No runtime scenes were changed and nothing was committed.

### 2026-11-03 follow-up

Crypt mossstone redraws 07–09 were retained under `jobs/floors-redraw-20261103/` and rejected after QA. Their X/Y seam means were 8.345/8.208, 8.456/8.545, and 4.018/7.043; all three show recognizable repeat cadence in 3×3. No Tomb manifest entry changed. The full gate still has the existing Ancient floor-02 seam failure.

### Mid backdrop redraw — 2026-11-04

- Replaced the tall arch/tower draft with an unapproved low ruined-wall candidate from redraw 05 alpha-bbox packaging. Final: 1024×384, 47 colors, horizontal seam RGB MAE 5.403 / adjacent 3.188, transparent-alpha seam MAE 3.32. The 3×1 repeat has no repeated landmark; mild capstone cadence remains for composite scene review.
- Prompts, five raw attempts, candidates, previews, and QA are retained in `jobs/backdrop-mid-redraw-20261104/`. `approved:false` remains. Contact sheet rebuilt after manifest update.


### Crypt mossstone redraw retries — 2026-11-04 (10–13)

- Attempts 10–13 were retained under `jobs/floors-redraw-20261104/` with raw images, exact prompts, 512×512/48-color candidates, seam QA and 3×3 repeats.
- 10 cropbest rejected: seam X/Y 19.801/20.278; obvious tile cadence. 11 rejected: 6.602/5.811 but dark tile grid persists. 12 rejected: 5.180/10.536 and tile boundary/cadence visible. 13 used Octopath dirt-floor style reference; seams 4.565/4.546 but faint tile grid and regular fine-stone rhythm remain.
- No manifest change; current crypt mossstone stays a draft. Need a less regular stone grammar or a non-repeating floor treatment; do not promote based only on seam score.


### Near backdrop redraw 05 — 2026-11-04

- New low masonry strip (1024×384, 47 opaque colors, binary alpha) from the original cemetery map reference and Octopath forest-hedge style reference. Horizontal seam RGBA MAE 3.118 / adjacent 1.170.
- Rejected after 3×1 repeat review: root and capstone rhythm recurs visibly; no manifest change. Raw, packaged candidate, exact prompt, QA and repeat preview saved in `jobs/backdrop-near-redraw-20261104/`. Need a different composition grammar than continuous modular masonry.


### Near backdrop redraw 06 — 2026-11-04

- Broken-rubble strip: 1024×384, 48 opaque colors, binary alpha. Seam and adjacent RGBA MAE are both 0 because both endpoints are fully transparent.
- Rejected after 3×1 review: the same tall rubble heap and root recur once per tile; empty endpoints hide the seam metric. Raw, exact prompt, packaged candidate, QA and repeat preview are retained. No manifest change.


### Near backdrop redraw 05 selected for composition draft — 2026-11-04

- Replaced the tall-column near layer with a low broken masonry strip (1024×384, 47 opaque colors, binary alpha), chosen for map composition review. QA: horizontal seam RGBA MAE 3.118 / adjacent 1.170. The 3×1 repeat still shows a mild root/capstone cadence; this remains `approved:false` and needs composite/owner review.
- Prior final, prompt, QA and review are backed up in `jobs/backdrop-near-redraw-20261104/before-near-draft-20261104/`. Raw and exact prompt retained. Manifest revision 38; Tomb contact sheet rebuilt at 76 assets. Redraw 06 was rejected because a transparent seam score of 0 concealed a repeated tall rubble motif.
- Full multi-kit gate rerun after the manifest update: 494 assets, 0 errors, 0 warnings. This is mechanical QA only.


### Composite review update — 2026-11-04

A temporary review scene stacked the current far, mid, and near drafts. The low near wall reads as a separate depth band and did not obscure visible grave props/floor in the center camera frame. Horizontal cadence was not proven across the full map from that narrow view; the repeat remains visible in its 3×1 sheet. Scene JSON, three texture inputs, and review notes are retained in `jobs/backdrop-composite-review-20261104/`. Temporary files were removed from `apps/game-web/public/`; no runtime scene was changed. Owner review is still pending.


### Crypt mossstone retries 14–15 — 2026-11-04

- Both attempts are archived with exact prompts, raw image_gen outputs, 512×512/48-color candidates, QA and 3×3 previews in `jobs/floors-redraw-20261104/`.
- 14 (X/Y 5.102/8.101) rejected for visible horizontal patch cadence and soft finish. 15 (3.563/3.630) rejected as too smooth/featureless for a crypt flagstone tile. Manifest unchanged; current final remains a draft.


### Crypt mossstone retries 14–16 — 2026-11-04

- Attempts are archived with exact prompt, raw, candidate, QA and 3×3 preview under `jobs/floors-redraw-20261104/`.
- 14: X/Y 5.102/8.101; rejected for repeated horizontal texture patches and soft finish. 15: 3.563/3.630; rejected as too smooth/featureless. 16: 9.144/8.630; rejected for seam failure and noisy cluster cadence. No manifest update.


### Crypt brick-floor redraws 05–07 — 2026-11-04

Three attempts retained under `jobs/floors-redraw-20261104/`; rejected after 3×3 review for repeat cadence and seam errors (05: 6.639/8.671, 06: 8.836/8.555, 07: 14.518/15.515). No manifest update; revision 39 / 76 assets remains. The session's active image tool did not accept reference attachments, so these generations used text prompts only and do not satisfy the checklist's attached-reference instruction. Gate rerun after these unmanifested retries: 494 assets, 0 errors, 0 warnings; mechanical check only.


### Crypt brick-floor redraws 08–10 — 2026-11-04

Attempts 08–10 used attached references and were rejected after 3×3/seam review: 08 (5.212/7.145, soft grouping), 09 (10.806/14.507, small-stone cadence), 10 (4.861/9.745, broad cluster cadence). Exact prompts/raw/candidate/QA/previews are in `jobs/floors-redraw-20261104/`. No manifest update.
