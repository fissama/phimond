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


## Assigned batch 20 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 20
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0096 — Nữ Yêu Minh Ưng

```json
{
  "species_id": "species_0096",
  "source_species_id": "NuYeuMinhUng",
  "display_name_vi": "Nữ Yêu Minh Ưng",
  "race_id": "bird",
  "star": 2,
  "species_class": "normal",
  "batch": 20,
  "source_portrait": "apps/game-client/assets/pets/apk84/NuYeuMinhUng/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NuYeuMinhUng/sprites.png",
  "source_portrait_sha256": "f076b266bb1e844ec10505e719c13d41eb4907b2729d7db3bdf5486f8df2c8c9",
  "source_atlas_sha256": "45574b7a00a2c541b19a0cdbdc34bf67e395df55eceabbd9cffca922a638929f",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0096",
  "status": "queued"
}
```


### species_0097 — Dơi Một Mắt

```json
{
  "species_id": "species_0097",
  "source_species_id": "DoiMotMat",
  "display_name_vi": "Dơi Một Mắt",
  "race_id": "bird",
  "star": 2,
  "species_class": "normal",
  "batch": 20,
  "source_portrait": "apps/game-client/assets/pets/apk84/DoiMotMat/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DoiMotMat/sprites.png",
  "source_portrait_sha256": "62a3c0b79056bdec4999f48e29f632881175d3bf345b36d722bd2533ca50e651",
  "source_atlas_sha256": "880268e1ebe767e7085f1f395f417fe63945d988729a6b329496cfd3bd6ede30",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0097",
  "status": "queued"
}
```


### species_0098 — Quạ Nghĩa Trang

```json
{
  "species_id": "species_0098",
  "source_species_id": "QuaNghiaTrang",
  "display_name_vi": "Quạ Nghĩa Trang",
  "race_id": "bird",
  "star": 2,
  "species_class": "normal",
  "batch": 20,
  "source_portrait": "apps/game-client/assets/pets/apk84/QuaNghiaTrang/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/QuaNghiaTrang/sprites.png",
  "source_portrait_sha256": "912718969358a1c8b3a0496f32065da19dc30b1c29efbc81c2b651fae80e004a",
  "source_atlas_sha256": "5ff9ec3b3a4e075a278f6d110dcb4a4809b187a735f54f9936b2f65bb632a79e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0098",
  "status": "queued"
}
```


### species_0099 — Tê Điểu

```json
{
  "species_id": "species_0099",
  "source_species_id": "TeDieu",
  "display_name_vi": "Tê Điểu",
  "race_id": "bird",
  "star": 2,
  "species_class": "normal",
  "batch": 20,
  "source_portrait": "apps/game-client/assets/pets/apk84/TeDieu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TeDieu/sprites.png",
  "source_portrait_sha256": "3181eac7fe060aed35c3fc1cfdd000474ae37818c5c6bd4229295d74d16b4fa7",
  "source_atlas_sha256": "bcb0be550aadc48546f8c45d2ca4ecfa9e989164eb7e4dfd113f62ba0efe7492",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0099",
  "status": "queued"
}
```


### species_0100 — Vẹt Độc Vuốt

```json
{
  "species_id": "species_0100",
  "source_species_id": "VetDocVuot",
  "display_name_vi": "Vẹt Độc Vuốt",
  "race_id": "bird",
  "star": 3,
  "species_class": "normal",
  "batch": 20,
  "source_portrait": "apps/game-client/assets/pets/apk84/VetDocVuot/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/VetDocVuot/sprites.png",
  "source_portrait_sha256": "f7e7f34140993ad5045eeb00c95a2d139f20ea713ca03dc1fdbfbdd17824aa8e",
  "source_atlas_sha256": "2a847e71562c0066de846a52cc14a61d1f37555f9e2336edb93cdeb455b2a84d",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0100",
  "status": "queued"
}
```
