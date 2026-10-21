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


## Assigned batch 15 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 15
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0071 — Ưng Đỏ

```json
{
  "species_id": "species_0071",
  "source_species_id": "UngDo",
  "display_name_vi": "Ưng Đỏ",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 15,
  "source_portrait": "apps/game-client/assets/pets/apk84/UngDo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/UngDo/sprites.png",
  "source_portrait_sha256": "1c3f4ccb68e4a224728d6117a63efc6ed987757a1c8c8238c0de1b3cdf0f7486",
  "source_atlas_sha256": "cab5ee7fc0111d670544ee9ffe546d767c7a870238fa49ece5694d9f65a46046",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0071",
  "status": "queued"
}
```


### species_0072 — Ma Cây

```json
{
  "species_id": "species_0072",
  "source_species_id": "MaCay",
  "display_name_vi": "Ma Cây",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 15,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaCay/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaCay/sprites.png",
  "source_portrait_sha256": "969b692ee86bf05941d3767ad4b7d3115b86bb48ed1c0b88d697d9be532cc959",
  "source_atlas_sha256": "cb9a8c7ba0fa8cad3ec34f72e914de1472ae16afbf60edae066df862a986bca6",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0072",
  "status": "queued"
}
```


### species_0073 — Rùa Phú Quý

```json
{
  "species_id": "species_0073",
  "source_species_id": "RuaPhuQuy",
  "display_name_vi": "Rùa Phú Quý",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 15,
  "source_portrait": "apps/game-client/assets/pets/apk84/RuaPhuQuy/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RuaPhuQuy/sprites.png",
  "source_portrait_sha256": "9eb96851bfc3fab97c756ae73a7a15711cba64d378d12a7bc3fac85c1deeb7ce",
  "source_atlas_sha256": "5f7c4e079489c127bb8a9b324b2313e48750dd4f0a63ce4c9944050946ae2491",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0073",
  "status": "queued"
}
```


### species_0074 — Sói Ngớ Ngẩn

```json
{
  "species_id": "species_0074",
  "source_species_id": "SoiNgoNgan",
  "display_name_vi": "Sói Ngớ Ngẩn",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 15,
  "source_portrait": "apps/game-client/assets/pets/apk84/SoiNgoNgan/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/SoiNgoNgan/sprites.png",
  "source_portrait_sha256": "0f82a6c70cc9875b188799d09034b7aff5da5a06d7c2d6ab09e416e7fb7fb72a",
  "source_atlas_sha256": "0872ff5d5b8fa48da1b6deb7559188d85d9b02a8a3fc0811676681234a05b0b5",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0074",
  "status": "queued"
}
```


### species_0075 — Tê Tê Vàng

```json
{
  "species_id": "species_0075",
  "source_species_id": "TeTeVang",
  "display_name_vi": "Tê Tê Vàng",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 15,
  "source_portrait": "apps/game-client/assets/pets/apk84/TeTeVang/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TeTeVang/sprites.png",
  "source_portrait_sha256": "d484f5f738624d11cb97fc22477bcd3a92d5cde18704d84982bb4e40e07d0a3e",
  "source_atlas_sha256": "0d11c45430e1279da4f52fe1a7b0dc4971a79eb2f68b8b02053dbd30b31eecdb",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0075",
  "status": "queued"
}
```
