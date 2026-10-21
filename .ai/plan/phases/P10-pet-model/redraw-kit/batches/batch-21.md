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


## Assigned batch 21 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 21
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0101 — Đại Bàng Sư Tử

```json
{
  "species_id": "species_0101",
  "source_species_id": "DaiBangSuTu",
  "display_name_vi": "Đại Bàng Sư Tử",
  "race_id": "bird",
  "star": 3,
  "species_class": "normal",
  "batch": 21,
  "source_portrait": "apps/game-client/assets/pets/apk84/DaiBangSuTu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DaiBangSuTu/sprites.png",
  "source_portrait_sha256": "e8d9bafac09a75c66cda0fc67644dccf7a43a8d9ff95975371f2248576d01b06",
  "source_atlas_sha256": "86f86ae5b1abcfbb5f5afd94dd4442a745f0916c0478b93cd084a2f659c5ebfb",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0101",
  "status": "queued"
}
```


### species_0102 — Ưng Hồng Vũ

```json
{
  "species_id": "species_0102",
  "source_species_id": "UngHongVu",
  "display_name_vi": "Ưng Hồng Vũ",
  "race_id": "bird",
  "star": 3,
  "species_class": "normal",
  "batch": 21,
  "source_portrait": "apps/game-client/assets/pets/apk84/UngHongVu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/UngHongVu/sprites.png",
  "source_portrait_sha256": "1df51cb9ab54e1fc32f0e57881f4e5cdad3beb7460d60f0293e51c05b1f08b1d",
  "source_atlas_sha256": "04a41a7e6090983a9bd90100cdbeb95af38143ca79ecbbea319edf8aceacd57a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0102",
  "status": "queued"
}
```


### species_0103 — Chim Đại Phì

```json
{
  "species_id": "species_0103",
  "source_species_id": "ChimDaiPhi",
  "display_name_vi": "Chim Đại Phì",
  "race_id": "bird",
  "star": 4,
  "species_class": "normal",
  "batch": 21,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimDaiPhi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimDaiPhi/sprites.png",
  "source_portrait_sha256": "3f176cb25889058b43731cae25c764d440374d64070afc2cdafa49a1ea3dda63",
  "source_atlas_sha256": "9395c89c4cce93e1664619adce83e04bfae1fd8c10e203a223712d2a9cc30092",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0103",
  "status": "queued"
}
```


### species_0104 — Chim Đa Đa

```json
{
  "species_id": "species_0104",
  "source_species_id": "ChimDaDa",
  "display_name_vi": "Chim Đa Đa",
  "race_id": "bird",
  "star": 4,
  "species_class": "normal",
  "batch": 21,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimDaDa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimDaDa/sprites.png",
  "source_portrait_sha256": "9291ad1cdf7c16c0df02f69fc8f309aa63c292cc83b60b008f47dbf7fc34f003",
  "source_atlas_sha256": "9d2063e1351406dcae8303f4c59289b70d671cc408c815d6770a8c63e0761a34",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0104",
  "status": "queued"
}
```


### species_0105 — Chu Tước

```json
{
  "species_id": "species_0105",
  "source_species_id": "ChuTuoc",
  "display_name_vi": "Chu Tước",
  "race_id": "bird",
  "star": 4,
  "species_class": "special",
  "batch": 21,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChuTuoc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChuTuoc/sprites.png",
  "source_portrait_sha256": "62669db11e8ec4b225cd07a9033bb58a7c91bd3a37ef9274c5d582c9132b5bfc",
  "source_atlas_sha256": "d6d6ae81c525da60c55ab91d79be144166b2cfd3e60a366e0a6ff0dd24f89663",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0105",
  "status": "queued"
}
```
