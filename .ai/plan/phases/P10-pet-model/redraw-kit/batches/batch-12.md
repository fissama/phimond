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


## Assigned batch 12 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 12
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0056 — Ma Móng Rồng

```json
{
  "species_id": "species_0056",
  "source_species_id": "MaMongRong",
  "display_name_vi": "Ma Móng Rồng",
  "race_id": "demon",
  "star": 1,
  "species_class": "normal",
  "batch": 12,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaMongRong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaMongRong/sprites.png",
  "source_portrait_sha256": "946c98c1f8f8de0389651a461e4f4a6c4816e3ccef381ac1fb20b858d31269c0",
  "source_atlas_sha256": "0412515ace21c75e1db33ea828404708a5b73f63f84a77539f8f0c873c72ee9a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0056",
  "status": "queued"
}
```


### species_0057 — Báo Địa Ngục

```json
{
  "species_id": "species_0057",
  "source_species_id": "BaoDiaNguc",
  "display_name_vi": "Báo Địa Ngục",
  "race_id": "demon",
  "star": 1,
  "species_class": "normal",
  "batch": 12,
  "source_portrait": "apps/game-client/assets/pets/apk84/BaoDiaNguc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/BaoDiaNguc/sprites.png",
  "source_portrait_sha256": "78297392d8cd9adc5cbd8a4ae7263e3939ec975681e84cdec24292e64b6614a4",
  "source_atlas_sha256": "a249ca89eba014f947f5363c00114fe07e22c3e448ac1788bdcaec21b087f79b",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0057",
  "status": "queued"
}
```


### species_0058 — Chó Săn Ác Ma

```json
{
  "species_id": "species_0058",
  "source_species_id": "ChoSanAcMa",
  "display_name_vi": "Chó Săn Ác Ma",
  "race_id": "demon",
  "star": 1,
  "species_class": "normal",
  "batch": 12,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChoSanAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChoSanAcMa/sprites.png",
  "source_portrait_sha256": "83a54f50dc70eaeabc12068dbdbf4f8d7822f81322f5ab908fcf1fcc4a055869",
  "source_atlas_sha256": "d983244bb3db63fa94fcbe923df6477d17510a66d45d1c85819251493b966a7e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0058",
  "status": "queued"
}
```


### species_0059 — Tướng Chiến Ma Rồng

```json
{
  "species_id": "species_0059",
  "source_species_id": "TuongChienMaRong",
  "display_name_vi": "Tướng Chiến Ma Rồng",
  "race_id": "demon",
  "star": 2,
  "species_class": "normal",
  "batch": 12,
  "source_portrait": "apps/game-client/assets/pets/apk84/TuongChienMaRong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TuongChienMaRong/sprites.png",
  "source_portrait_sha256": "f6733e6d73155215bd52808d876c1cccbcac1a6c8ba69cbfb166078b83696aa2",
  "source_atlas_sha256": "ac3dc2983e21d19b4ca1d0c168bdd46a6b058f2b71abbcdeac0862d7bb08d516",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0059",
  "status": "queued"
}
```


### species_0060 — Ma Thú Địa Ngục

```json
{
  "species_id": "species_0060",
  "source_species_id": "MaThuDiaNguc",
  "display_name_vi": "Ma Thú Địa Ngục",
  "race_id": "demon",
  "star": 2,
  "species_class": "normal",
  "batch": 12,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaThuDiaNguc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaThuDiaNguc/sprites.png",
  "source_portrait_sha256": "ae8c0a184d534e87a6477c40bff9206d5fe4915b954fdf1c5cf964f7508a3ccf",
  "source_atlas_sha256": "1bcdf6167992e96bcb5d28f9be20c1abf5ce862221e6b4669d7ee9e5e42cfe3a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0060",
  "status": "queued"
}
```
