# Fresh redraw execution — GPT-6.1 Sol, 2026-10-05

User explicitly requested deleting all previous redraw assets except the two
approved anchors, then redrawing all other150 species using GPT-6.1 Sol.
Cleanup evidence: `cleanup-20261005.json`; all10 files belonging to the two
approved species were preserved byte-identically. Previous candidates,
rejected art and aborted batch outputs were deleted as requested.

## Current authoritative art policy

- Identity comes ONLY from original APK portrait and actor atlas, even when blurry.
- Style comes ONLY from approved DocDangNu and DaoThienDuong sheets.
- No old/rejected/procedural/MiniMax artwork may be a reference.
- Faithfully reconstruct silhouette/proportions/colors/equipment; no new ornate redesign.
- All20 frames use one fixed camera, default LEFT three-quarter matching anchors.
  A clearly frontal/symmetric original can retain its fixed frontal camera
  (CuaHacAm is recorded as an exception); never alternate cameras within a sheet.
- Frames must articulate meaningful body/limb poses; shifting particles does not
  establish animation diversity. No alternating directions or mirrored duplicates.
- Own newly generated sheets can be repair targets, never alternate style/identity references.

These user corrections supersede the older plan's preferred rightward impact,
unassigned-150 wording and former pilot scope. Geometry contract remains
1124×1405 RGBA,4×5,cells281,alpha inside[22,259). Final human acceptance and
runtime activation remain separate from generation/review.

## Exclusive ownership

Fresh queue indices refer to `/tmp/phimond-redraw-source-review/generation-queue-gpt61.json`.
All150 jobs correspond to the canonical `manifest.json`, excluding only two anchors.

- Lead: indices0–4 (5 species), execution reports and independent review;
  additionally indices140–149 (10 species) released by workerC after raw generation.
- GPT-6.1 Sol worker A: indices5–52 (48 species).
- GPT-6.1 Sol worker B: indices53–101 (49 species).
- GPT-6.1 Sol worker C: generated indices102–149; now finalizes indices102–139
  (38 species). Tail10 released explicitly with no repair call in flight.

Each worker writes only its assigned species directories. Old GPT-6 Sol workers
were interrupted before cleanup. Inputs/identity/prompt for every fresh job are
already recorded; preparation is not counted as generated artwork.

Status: **in progress**. Actual generation/review/disposition evidence resides
in each species' result.json; no accepted/completed150 claim yet.

## Review observations

- Transparent image inspection can display saturated RGB from alpha1 pixels as
  an apparent opaque halo. Verify RGBA values and diagnostic normal alpha
  composites on light/dark backgrounds before requesting a halo repair. Keep
  all source alpha in packing; diagnostics do not alter artwork.
- Independent review has found equipment disappearing/floating, neighboring
  fragments and overly smooth vector style even in mechanically passing sheets.
  Findings are recorded against exact candidate hashes in independent-review.md
  and returned to the owning worker. Ready for review does not mean accepted.
- Initial three-call per-species budget is a triage limit, not acceptance.
  Targeted additional repairs may be required (lead MaVuongHutMau used four);
  record all attempts and do not silently promote a failing version.

## Resume — 2026-10-07

User explicitly resumed all150. Built-in image generation available again; continued original-only identity and two-anchor-only style policy. Canonical ownership on this resume:

- Lead: species0003/0018/0030/0039, species0053, and tail0141..0152 excluding approved0150 anchor (16 jobs).
- WorkerA: canonical jobs0001..0052 except lead four and approved0037 anchor (47 jobs). Species0024 is an ordinary redraw job, not an approved anchor.
- WorkerB:0054..0102 (49jobs).
- WorkerC:0103..0140 (38jobs).

Additional independent review ownership: workerC reviews lead/A selected art, lead reviews B/C art, workerA reviews B0095..0102. Peer edits limited to independent-review.md; no shared image/result mutations.

Normal RGBA peer inspection found actual equipment transfer/extra arms and small neighboring fragments despite geometry checkerPASS. Each defect is attached to exacthash; new selection requires renewed review. Lead0018/0147 targeted repairs resolve duplicated cast arm and switched weaponhand, respectively. Whole-pose source rectangles and common nearest-neighbor scale preserve all source alpha. Composition repairs reduce wholepose size to create gutters; undersized silhouettes require human64px readability review. No procedural paint, alpha erasure, runtime activation, DB change or server8090 restart.

Latest snapshots are resume-parent-snapshot-20261007.json and gallery-status.json; these are progress evidence, not final acceptance. Source provenance audit source-audit-20261007.json verifies committed original304 PNGs and manifest.

### Explicit repair ownership transfers on October 7

- B released 0054/0056/0057/0059 to Lead; selected repaired candidates received exact-hash independent A reviews.
- B released 0062/0069/0097/0098 to A. Lead reviews their selected candidates.
- B released 0087/0090/0094/0102 to C after pending outputs were persisted. Lead reviews their selected candidates.
- A retains repair ownership for its independently rejected 0022 plant-head identity and 0050 neighboring fragment.
- B subsequently released 0079 to Lead after its style-only attempt04 output was persisted; Lead owns subsequent packing/repair/result selection.
- B retains 0065/0073/0076/0082/0083 and other unreleased B jobs. Final repair ownership totals: Lead21, A51, B36, C42. No overlapping image/result ownership.

All150 now have actual raw output. This milestone does not establish 150 completed atlases: unresolved identity, equipment, camera, style and packing findings remain blocked. `resume-parent-integrity-20261007.json` checks selected hashes/checker/metadata; `resume-C-provenance-20261007.json` checks originals, anchors and allowed input roles. Both are timestamped progress snapshots while repairs continue.

`readability-snapshot-20261007.json` measures opaque idle silhouettes without changing pixels. Many are below the typical155px height guidance; containment and wide shapes can require smaller composition. Human64px readability and continuous playback remain required before game-ready acceptance. No sprite has been marked human-approved or activated.
