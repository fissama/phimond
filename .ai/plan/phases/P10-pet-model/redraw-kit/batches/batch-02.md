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


## Assigned batch 02 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 2
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0001 — Nhện Vong Linh

```json
{
  "species_id": "species_0001",
  "source_species_id": "NhenVongLinh",
  "display_name_vi": "Nhện Vong Linh",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 2,
  "source_portrait": "apps/game-client/assets/pets/apk84/NhenVongLinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NhenVongLinh/sprites.png",
  "source_portrait_sha256": "dd154ecaeec2bd5af773a5e8e2b1c39da6494d55b92f412224ae400a8940c628",
  "source_atlas_sha256": "d86f156cf2dceca6e9bb3c6fd2a26f2870fc1972f018a2ca714a109759a8cc19",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0001",
  "status": "queued"
}
```


### species_0002 — Chiến Sĩ Đầu Lâu

```json
{
  "species_id": "species_0002",
  "source_species_id": "ChienSiDauLau",
  "display_name_vi": "Chiến Sĩ Đầu Lâu",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 2,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChienSiDauLau/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChienSiDauLau/sprites.png",
  "source_portrait_sha256": "5f086585825769c94ab536b4b7fce0ce439f9998c9161aaf69feb7640c8f4672",
  "source_atlas_sha256": "650b4b7551f745490b749384c544869dae9ee0ebfabe35090c17821e41fee745",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0002",
  "status": "queued"
}
```


### species_0004 — Xác Ướp

```json
{
  "species_id": "species_0004",
  "source_species_id": "XacUop",
  "display_name_vi": "Xác Ướp",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 2,
  "source_portrait": "apps/game-client/assets/pets/apk84/XacUop/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/XacUop/sprites.png",
  "source_portrait_sha256": "e23074b067e13ef7063ec24735efd103c387da1643272e9715998e070d0367f9",
  "source_atlas_sha256": "c6512e3d1cac090f563afd10b9ad69213dfda6bfeca7768f9c781df971cee8a1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0004",
  "status": "queued"
}
```


### species_0005 — Xác Chết Ác Ma

```json
{
  "species_id": "species_0005",
  "source_species_id": "XacChetAcMa",
  "display_name_vi": "Xác Chết Ác Ma",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 2,
  "source_portrait": "apps/game-client/assets/pets/apk84/XacChetAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/XacChetAcMa/sprites.png",
  "source_portrait_sha256": "45c26108c7f60c7b8e14d0ccc58fd7cdcd58d050ef395733d5eed9cbdf1efdd2",
  "source_atlas_sha256": "08b3c35d1e0ec8c72f6352d982a29cf4c1bc4c69f6687e90d9e9ecf4ecc251ff",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0005",
  "status": "queued"
}
```


### species_0006 — U Linh

```json
{
  "species_id": "species_0006",
  "source_species_id": "ULinh",
  "display_name_vi": "U Linh",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 2,
  "source_portrait": "apps/game-client/assets/pets/apk84/ULinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ULinh/sprites.png",
  "source_portrait_sha256": "2e26bb3619e4eb67a623f78b90d77087f8417b33163a63dfc8ae75f61fee5aab",
  "source_atlas_sha256": "10a4371e3c011605427188115354b93f6ccb952d336f2aae3e06970e69406b7e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0006",
  "status": "queued"
}
```
