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


## Assigned batch 10 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 10
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0046 — Giáp Long Răng Nhọn

```json
{
  "species_id": "species_0046",
  "source_species_id": "GiapLongRangNhon",
  "display_name_vi": "Giáp Long Răng Nhọn",
  "race_id": "dragon",
  "star": 2,
  "species_class": "normal",
  "batch": 10,
  "source_portrait": "apps/game-client/assets/pets/apk84/GiapLongRangNhon/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/GiapLongRangNhon/sprites.png",
  "source_portrait_sha256": "a8ddd477994710d2c69d1bd91a8bf06a5108e7556ff9f2a21955b61a2c2e7f3e",
  "source_atlas_sha256": "a8ea8183ea1f2d8e06b53ed878ea38951a3c970b1adf0526e89b7dfd75415949",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0046",
  "status": "queued"
}
```


### species_0047 — Viêm Long

```json
{
  "species_id": "species_0047",
  "source_species_id": "ViemLong",
  "display_name_vi": "Viêm Long",
  "race_id": "dragon",
  "star": 3,
  "species_class": "normal",
  "batch": 10,
  "source_portrait": "apps/game-client/assets/pets/apk84/ViemLong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ViemLong/sprites.png",
  "source_portrait_sha256": "818948411c4a82cc3d51edcb185ec2714f17335982c24cc9bce63da80460f970",
  "source_atlas_sha256": "08dfab65a78a743d94b287738e72846b826e155c55bc5890ce4c90eda2c91ed0",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0047",
  "status": "queued"
}
```


### species_0048 — Rồng Sấm

```json
{
  "species_id": "species_0048",
  "source_species_id": "RongSam",
  "display_name_vi": "Rồng Sấm",
  "race_id": "dragon",
  "star": 3,
  "species_class": "normal",
  "batch": 10,
  "source_portrait": "apps/game-client/assets/pets/apk84/RongSam/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RongSam/sprites.png",
  "source_portrait_sha256": "44bb080ef155ba2f39cf119dc393cb276e9de9088bbd3a0c238798171374545b",
  "source_atlas_sha256": "095a67b068d619e04302e4368071329e4d33223d6a094a2ce24c661dd5037de7",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0048",
  "status": "queued"
}
```


### species_0049 — Rồng Phỉ Thúy

```json
{
  "species_id": "species_0049",
  "source_species_id": "RongPhiThuy",
  "display_name_vi": "Rồng Phỉ Thúy",
  "race_id": "dragon",
  "star": 3,
  "species_class": "normal",
  "batch": 10,
  "source_portrait": "apps/game-client/assets/pets/apk84/RongPhiThuy/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RongPhiThuy/sprites.png",
  "source_portrait_sha256": "6a05fa78f1512fd2c626dc582fc213408cbbc5fb8c1e5f94dae2981913ee918e",
  "source_atlas_sha256": "28f7e3b508a684b5f3eccd335c4aa74cda6924c1528f8ab91bb1ae9b7ac66ef0",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0049",
  "status": "queued"
}
```


### species_0050 — Hải Long Ba Đầu

```json
{
  "species_id": "species_0050",
  "source_species_id": "HaiLongBaDau",
  "display_name_vi": "Hải Long Ba Đầu",
  "race_id": "dragon",
  "star": 4,
  "species_class": "normal",
  "batch": 10,
  "source_portrait": "apps/game-client/assets/pets/apk84/HaiLongBaDau/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HaiLongBaDau/sprites.png",
  "source_portrait_sha256": "fae6ce56a0909701651eda64527be48b07a4be69e9d4a5eac504e65d5de9c3db",
  "source_atlas_sha256": "56e473ff3a5ec0132e4fdf41cc236da9167728a7b4fd89b312cdc60c3e7f2d92",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0050",
  "status": "queued"
}
```
