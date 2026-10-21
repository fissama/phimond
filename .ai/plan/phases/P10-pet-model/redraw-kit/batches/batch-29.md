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


## Assigned batch 29 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 29
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0141 — Totem Thượng Cổ

```json
{
  "species_id": "species_0141",
  "source_species_id": "TotemThuongCo",
  "display_name_vi": "Totem Thượng Cổ",
  "race_id": "spirit",
  "star": 5,
  "species_class": "normal",
  "batch": 29,
  "source_portrait": "apps/game-client/assets/pets/apk84/TotemThuongCo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TotemThuongCo/sprites.png",
  "source_portrait_sha256": "3493d704c00f6f2fdb1e6fc95177c5aa675006bd11fc0adcbfa7dd275a4f0734",
  "source_atlas_sha256": "0dd21788e889c2e1c419d4392e704e8d8d39b0f008eab244feb9d1830bd8f931",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0141",
  "status": "queued"
}
```


### species_0142 — Thần Tướng Cự Ma

```json
{
  "species_id": "species_0142",
  "source_species_id": "ThanTuongCuMa",
  "display_name_vi": "Thần Tướng Cự Ma",
  "race_id": "spirit",
  "star": 5,
  "species_class": "special",
  "batch": 29,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThanTuongCuMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThanTuongCuMa/sprites.png",
  "source_portrait_sha256": "da2961ed687867c54aba57467e43cbc738a7d952b69dac301bd462ecef695b3c",
  "source_atlas_sha256": "92991914d5d1a25c9ee63063ad58dd7953db39eaf1697402855b7d9c8bf743ec",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0142",
  "status": "queued"
}
```


### species_0143 — Thần Đèn

```json
{
  "species_id": "species_0143",
  "source_species_id": "ThanDen",
  "display_name_vi": "Thần Đèn",
  "race_id": "spirit",
  "star": 5,
  "species_class": "special",
  "batch": 29,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThanDen/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThanDen/sprites.png",
  "source_portrait_sha256": "adf762a329158fcc3086ca9b0e1106ed6fd79985e961997222372c877328a8a5",
  "source_atlas_sha256": "a64831ee6408169decd83fa403c801e1bf5ee5f921f3994673236c5243641924",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0143",
  "status": "queued"
}
```


### species_0144 — Linh Tiên Hoa Hương

```json
{
  "species_id": "species_0144",
  "source_species_id": "LinhTienHoaHuong",
  "display_name_vi": "Linh Tiên Hoa Hương",
  "race_id": "plant",
  "star": 5,
  "species_class": "special",
  "batch": 29,
  "source_portrait": "apps/game-client/assets/pets/apk84/LinhTienHoaHuong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/LinhTienHoaHuong/sprites.png",
  "source_portrait_sha256": "72c291261b9ab3406523174dd34263b6534c6fd449e36b86c58e4582b2495c19",
  "source_atlas_sha256": "8eb414ca3a0fa27c070794dff048b515e486113b5affc67420d84e5fbf89d8f2",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0144",
  "status": "queued"
}
```


### species_0145 — Cây Cự Linh

```json
{
  "species_id": "species_0145",
  "source_species_id": "CayCuLinh",
  "display_name_vi": "Cây Cự Linh",
  "race_id": "plant",
  "star": 5,
  "species_class": "special",
  "batch": 29,
  "source_portrait": "apps/game-client/assets/pets/apk84/CayCuLinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/CayCuLinh/sprites.png",
  "source_portrait_sha256": "808654253e4e00b7684d7a96f5fab71a18fdd2fd6ffb93f15ddcbe67ec4032e2",
  "source_atlas_sha256": "7129c3f41ae4d0d5918413ddd0ac0e607582724c0428e3295a69829bec261264",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0145",
  "status": "queued"
}
```
