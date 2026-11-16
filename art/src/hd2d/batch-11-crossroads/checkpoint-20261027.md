# Crossroads art checkpoint — 2026-10-27

Scope: `batch-11-crossroads` map art only. Built-in Codex image generation; no runtime/scene edits, commits, or owner approval. Manifest remains `approved: false`; Duyệt remains unchecked.

## Current work

- 17/17 shared props are packaged, mechanically clean, and have full 4× dark/checker visual review recorded. This turn added `crossroads-prop-07` as a single hanging stalactite: native footprint 96×290 px on 256×320, 48 colors, binary alpha, zero key residue, margin 15, no resampling.
- Props 08–17 had already been inspected at full 4×; added review notes and synchronized QA/manifest visual-review fields.
- Contact sheet rebuilt: 20 records, 1280×4000.
- Core floors 01–03 remain visually reviewed but rejected for tiling. The selected finals still fail `SEAM_X_NONZERO`, `SEAM_Y_NONZERO`, and `OUTER8_NOT_FLAT`; they remain unchecked in the checklist. One additional floor-01 image edit was inspected and rejected because it returned a framed/altered square image without uniform edges; its raw and rejection note are preserved under `jobs/floor-repair-01/`.
- Latest art gate: 250 assets scanned across batch-11 crossroads/desert/nightmare/tomb/windrock; 3 errors, 0 warnings. All 3 errors are the Crossroads floor seam failures; no other gate errors.

## Incomplete scope

- Crossroads shared kit still needs floor 04/05, backdrops, 3 extra floor variants, edges 01–03, decals 01–12, shadows 01–04, portal pair, arrival marker, and FX 01–03.
- Six map-specific landmarks and map scene assets have not been created. This checkpoint does not claim a completed map kit.
- Nightmare remains incomplete from its prior checkpoint: floor/edge/far-backdrop seam failures and missing valid wisp-lantern remain blockers.

## Resume

Continue with Crossroads only. Keep failed assets unchecked, preserve all raw attempts, rebuild the contact sheet after manifest edits, run `tools/hd2d_audit/art_gate.py`, and keep both manifests `approved: false`.

## Continuation — decals 01–06

- Re-inspected all six final decal images at 4× on dark and checker backgrounds. Added per-asset `review.md`, synchronized `qa.json` and manifest `visual_review=actual_complete_4x_dark_and_checker_viewed`; all six remain `approved: false` and status `needs_claude_visual_review`.
- Checklist now marks Vẽ for decals 01–06; Duyệt remains unchecked. Notes flag brighter cyan on 04/06 and saturated violet-pink on 05 for owner consideration.
- Rebuilt and opened contact sheet: 26 assets, 1280×5200.
- Latest `art_gate.py batch-11-crossroads`: 256 assets scanned across five kits; 3 errors, 0 warnings. Exact failures: `crossroads-floor-01 SEAM_Y 20.7/0.6`; `crossroads-floor-02 SEAM_Y 26.2/0.4`; `crossroads-floor-03 SEAM_Y 21.4/0.6`. All are existing floor blockers; decals add no new gate failures.


## Continuation — decals 07–12

- Generated a six-decal sheet with built-in image_gen. Attempt 01 exceeded native footprint; attempt 02 remained too wide; attempt 03 fit. All source attempts are preserved under `jobs/decals-07-12/`; selected raw is `raw-03.png`, SHA256 recorded by package provenance. Native 1:1 finish only; no post-generation resampling.
- Packaged and visually reviewed decals 07–12 at full 4× dark/checker. Each has 48 colors, binary alpha and no mechanical failures; added review notes and synchronized QA/manifest. Checklist marks Vẽ for decals 01–12; all Duyệt boxes remain unchecked. Manifest remains `approved:false`.
- Opened rebuilt contact sheet: 32 assets, 1280×6400. Color notes: decal 08 has bright cyan accents; decal 11's violet shell is a focal element; both await owner judgment.


## Continuation — shadows 01–04 and current gate

- Generated shadows using built-in image_gen. First package lost soft alpha; rejected exports were archived. One edit attempt rendered a fake checkerboard (RGB, alpha 255) and was rejected. Final set uses actual soft-alpha pixels from the original sheet, separated by alpha cleanup and premultiplied Lanczos resizing for these soft effects only; four variants are 112×32, 176×48, 256×64 and 384×96 source pixels. Soft alpha is preserved (24,741–88,893 partial-alpha pixels), no errors. Full 4× dark/checker viewed and reviewed; checklist Vẽ checked, Duyệt empty.
- Contact sheet rebuilt/opened: 36 assets, 1280×7200.
- Latest art gate: 266 assets scanned; 3 errors, 0 warnings. Exact failures remain `crossroads-floor-01 SEAM_Y 20.7/0.6`, `crossroads-floor-02 SEAM_Y 26.2/0.4`, `crossroads-floor-03 SEAM_Y 21.4/0.6`; no new gate errors from decal/shadow work.


## Floor repair attempt 02 — rejected

- Tried a focused image edit on `crossroads-floor-01`; it returned a 1254×1254 re-render rather than the native 512×512 tile. Preserved as `jobs/floor-repair-01/raw-02.png` and documented in the job and floor QA; selected floor and checklist state unchanged.


## Map 02 — Hành Lang Rêu Biếc

- Inspected the original map and brief. Identified one unique landmark: a three-crate wooden supply stack by the rear wall. Cave columns and coral are represented by shared kit props; no second unique landmark is visible. Checklist names landmark-01 and records landmark-02 as not present.
- Generated the crate stack with built-in image_gen, matching source composition. Six raw attempts are preserved under `jobs/crossroads02-landmark01/`; selected `raw-06.png`. Packaged native 1:1 at 224×192, 48 colors, binary alpha, no key residue; no resampling. Full 4× dark/checker reviewed; review note and manifest synchronized. Owner approval remains false; checklist Vẽ checked, Duyệt unchecked.
- Contact sheet rebuilt/opened: 37 assets, 1280×7600.
- Latest art gate: 267 assets; 3 errors, 0 warnings. No new errors. Existing failures unchanged: `crossroads-floor-01 SEAM_Y 20.7/0.6`, `crossroads-floor-02 SEAM_Y 26.2/0.4`, `crossroads-floor-03 SEAM_Y 21.4/0.6`.

## Map 03 — Đoạn Thủy Quang (in progress)

- Inspected original maps 03–06 and their briefs. Repeated landmarks are the small cairn and three-crate stack; cave columns and coral use shared kit props. Reuse the existing approved `batch-01-octopath/rock-small` and Map 02 crate landmark rather than adding duplicates. Checklists record no standalone landmark assets for maps 03–06.
- Made seven built-in image_gen attempts for the cairn. Preserved all source images under `jobs/crossroads03-landmark01/raw-01.png` through `raw-07.png`; prompt refs and hashes are recorded in `job.json`.
- Rejected all seven: the single renders and 3x2 sheets retain a diffuse halo and are too large for the source landmark; the second sheet also adds too much bright moss. No attempt was packaged; the existing approved shared rock is used instead.

## Continuation — FX 01

- Generated and packaged `crossroads-fx-01` with built-in image_gen: a 4×4 sheet with four 4-frame rows for water motes, cave bubbles, coral glint and mineral shimmer. Raw-01 is byte-identical; raw-02 color-edit attempt was rejected for broad baked halos and preserved.
- Mechanical QA: 48 colors, binary alpha, key residue 0, margin 86 px, failures none. Viewed final at full 4× on dark and checker backgrounds. Row 3 has a restrained indigo-violet edge; the bright core is mostly white/cyan. Manifest remains `approved:false`; checklist Vẽ marked, Duyệt empty.
- Rebuilt/opened contact sheet: 38 assets, 1280×7600. Latest `art_gate.py batch-11-crossroads`: 268 assets across five kits; 3 errors, 0 warnings. Existing failures: `crossroads-floor-01 SEAM_Y 20.7/0.6`; `crossroads-floor-02 SEAM_Y 26.2/0.4`; `crossroads-floor-03 SEAM_Y 21.4/0.6`.


## Continuation — FX 02 (2026-10-28)

- Generated and packaged `crossroads-fx-02` with built-in image_gen: 4×4 sheet, four 4-frame rows for splash, cave drips, stone chips and moss spores. Raw-01 is byte-identical; no rejected follow-up attempt.
- Mechanical QA: 48 colors, binary alpha, key residue 0, margin 77 px, failures none. Full 4× final reviewed on dark and checker backgrounds; checklist Vẽ checked, Duyệt remains empty, manifest `approved:false`.
- Rebuilt/opened contact sheet: 39 assets, 1280×8000. Latest art gate: 269 assets scanned across five kits; 3 errors, 0 warnings. Exact failures remain `crossroads-floor-01 SEAM_Y 20.7/0.6`; `crossroads-floor-02 SEAM_Y 26.2/0.6`; `crossroads-floor-03 SEAM_Y 21.4/0.6`.


## Continuation — FX 03 (2026-10-28)

- Generated and packaged `crossroads-fx-03` with built-in image_gen: 4×4 sheet, four 4-frame rows for coral pollen, crystal glint, lavender motes and portal sparks. Raw-01 is selected and byte-identical; the brighter row-1 edit was rejected for broad baked halos and preserved as raw-02.
- Mechanical QA: 48 colors, binary alpha, key residue 0, margin 77 px, failures none. Viewed the selected final at full 4× on dark/checker backgrounds. Row 1 is darker than other rows but legible; noted for owner review. Checklist Vẽ checked; Duyệt empty; manifest `approved:false`.
- Rebuilt/opened contact sheet: 40 assets, 1280×8000. Latest art gate: 270 assets across five kits; 3 errors, 0 warnings. Exact existing failures: `crossroads-floor-01 SEAM_Y 20.7/0.6`; `crossroads-floor-02 SEAM_Y 26.2/0.6`; `crossroads-floor-03 SEAM_Y 21.4/0.6`. FX 01–03 coverage is now complete; other shared kit assets remain.


### 2026-11-04 — Crossroads source landmark reconciliation

- Opened source images for maps 01–06 and replaced generic placeholder rows with observed content. Map 01 uses the existing `batch-01-octopath/rock-small` cairn and the already-drawn Map 02 crate-stack candidate; Map 02 keeps its crate stack; maps 03–06 have no additional unique landmark asset. Source hashes are recorded at the end of `kit-crossroads.md`.
- This avoids inventing duplicate landmark art. `Duyệt` remains empty; no manifest changed.
