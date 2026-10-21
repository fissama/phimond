# Worker brief — batch art only

You are the art worker for the EXACT five jobs appended below, in the Phimond
workspace. Use GPT-6.1 Sol as the task model chosen by the user; use the available
built-in image-generation tool to draw. GPT text output alone is not artwork.
If that tool is unavailable, report the limitation; do not switch to a paid
API/CLI fallback or draw placeholder shapes in Python.

Read `AGENTS.md`, the existing `P10-redraw-plan.md`, and this kit's README.
This dated kit expands the older two-species pilot into planning for 150 jobs;
it does not modify other tasks' ownership or authorize runtime integration.
The human starts this batch by pasting this brief. Do not start other batches,
message other tasks, spawn agents, push, merge, restart servers, touch DB/saves,
or activate candidate art. Preserve concurrent dirty work.

## Exclusive write scope

Only the five appended `output_dir` directories. Do not modify shared catalogs,
source `apk84/`, references/, earlier candidates/, rejected/, runtime scripts,
this kit, or shared status files. Write each job's state in its own directory.
Existing helper scripts may be read/executed, never patched to bypass failures.
If a target directory is already owned by a running task, stop that job and
report the conflict. Do not overwrite any attempt or accepted output.

## Per-species workflow (one species per generation call)

1. Run the printed batch input check. Inspect both style anchors and this
   species' source portrait/atlas with image-view tools before generation.
2. Create `identity.md`: anatomy counts, palette, head/face, clothes, weapons and
   which hand, distinguishing silhouette, movement type, camera and ground/hover
   pivot. Resolve source conflicts explicitly; never invent from a translated
   name alone. Only the original APK images and the two approved anchors may be art references. Never inspect or reuse any rejected redraw.
3. Fill `image-prompt.md` using this identity; save exact submitted prompt and
   ordered input paths/hashes in `attempt-01/prompt.md` + metadata.
4. Generate a single 20-pose sheet with actual transparent alpha. Persist the
   tool output byte-identically as `attempt-01/raw.png`. Inspect it immediately.
5. If identity, style, anatomy, weapon continuity, row meaning or final down
   pose fails: use the repair prompt with concrete row/column findings. Save a
   NEW attempt directory. Never hide failed attempts or claim a mechanical pass
   fixes their meaning. Maximum 3 generation calls per species in this batch;
   after 3 mark `blocked` with findings and continue to the next assigned species.
6. Only if the art is semantically sound, inspect geometry. Directly compliant
   output can be the candidate. Otherwise use the existing deterministic packer
   with 20 COMPLETE source rectangles and explicit local pivots. Preserve every
   alpha>0 pixel, including effects; no clipping/masking/alpha erasing. Use one
   common nearest-neighbor scale. Never fake 20 poses with transformed duplicates.
7. Run the atlas checker on the exact candidate; save its JSON report. Mechanical
   failure blocks review. Do not copy geometry errors from the style references.
8. Export an isolated HTML animation preview and portrait crop from the candidate using
   this kit's helper. Preview at 64/96px and 2× nearest on light/dark backgrounds;
   play each row and record loop seam, pivot jitter, LEFT-facing orientation in all 20 cells, impact direction and final
   down pose. The export command does NOT confer visual acceptance.
9. Save `self-review.md` with 20 row/column observations, findings and exact
   candidate SHA256. Save `result.json` with species IDs, attempt count, paths,
   hashes, mechanical status and `status: ready_for_review` or `blocked`.
   Human approval is never self-assigned. An external reviewer checks exact hashes.

Output summary: for each of the five IDs, candidate path/hash, generation calls,
mechanical result, self-review findings, status and any unresolved blocker.
Never report all 150 completed from this batch. No commit/stage of shared work;
Lead handles integration separately after visual review and human acceptance.


## Assigned batch 06 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 6
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0023 — Nấm Hoa

```json
{
  "species_id": "species_0023",
  "source_species_id": "NamHoa",
  "display_name_vi": "Nấm Hoa",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 6,
  "source_portrait": "apps/game-client/assets/pets/apk84/NamHoa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NamHoa/sprites.png",
  "source_portrait_sha256": "8328099e8e4fc86573395ba55b0f88b6b47dbfb8272146319b04c2e4280952b0",
  "source_atlas_sha256": "5dfdacbe965c016b32429677a4efd2b2a131e752c86c8564f609d05bea1cb62a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0023",
  "status": "queued"
}
```


### species_0024 — Tinh Tinh Xanh

```json
{
  "species_id": "species_0024",
  "source_species_id": "TinhTinhXanh",
  "display_name_vi": "Tinh Tinh Xanh",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 6,
  "source_portrait": "apps/game-client/assets/pets/apk84/TinhTinhXanh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TinhTinhXanh/sprites.png",
  "source_portrait_sha256": "6849823b2a5c81424f936619f8d6725f28efa46c119133c4acd0f916ab70f214",
  "source_atlas_sha256": "166b137c7dc3a816457dd05107582ad8cdb8ad1522bb4928c8f8955284c466fb",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0024",
  "status": "queued"
}
```


### species_0025 — Hải Quỳ

```json
{
  "species_id": "species_0025",
  "source_species_id": "HaiQuy",
  "display_name_vi": "Hải Quỳ",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 6,
  "source_portrait": "apps/game-client/assets/pets/apk84/HaiQuy/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HaiQuy/sprites.png",
  "source_portrait_sha256": "f35dde80573640eba320c1c93f958308e53e4f0572f3f8f52570897d4f9f47ec",
  "source_atlas_sha256": "aa995611d7fb70c83a8b9e30c91df37841770ff3c0b74ea27445277559162f2c",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0025",
  "status": "queued"
}
```


### species_0026 — Gỗ Quỷ

```json
{
  "species_id": "species_0026",
  "source_species_id": "GoQuy",
  "display_name_vi": "Gỗ Quỷ",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 6,
  "source_portrait": "apps/game-client/assets/pets/apk84/GoQuy/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/GoQuy/sprites.png",
  "source_portrait_sha256": "109814ccbc58ab360cc93bef9008facec708b56b0b736975ea9653fca76d2a37",
  "source_atlas_sha256": "479d78ce3da840d59745959a7420a7fdc2ad6aede9f5eed178ee485bba1357a2",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0026",
  "status": "queued"
}
```


### species_0027 — Quả Mặt Quỷ

```json
{
  "species_id": "species_0027",
  "source_species_id": "QuaMatQuy",
  "display_name_vi": "Quả Mặt Quỷ",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 6,
  "source_portrait": "apps/game-client/assets/pets/apk84/QuaMatQuy/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/QuaMatQuy/sprites.png",
  "source_portrait_sha256": "533307ad0da9dcb985278dd6bbc94899b69f1d3e2aad38bb20615c4e44c62593",
  "source_atlas_sha256": "c8a32382e36e825f7142bcde9a37526ea723df3819797fd74b6ad9b8cbd58d9a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0027",
  "status": "queued"
}
```
