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


## Assigned batch 30 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 30
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0147 — Người Tuyết Viễn Cổ

```json
{
  "species_id": "species_0147",
  "source_species_id": "NguoiTuyetVienCo",
  "display_name_vi": "Người Tuyết Viễn Cổ",
  "race_id": "beast",
  "star": 5,
  "species_class": "normal",
  "batch": 30,
  "source_portrait": "apps/game-client/assets/pets/apk84/NguoiTuyetVienCo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NguoiTuyetVienCo/sprites.png",
  "source_portrait_sha256": "531d03e6e9d4d61114e90b6fc8d3bae984ae633e5db73d9bacc08b06f51fa416",
  "source_atlas_sha256": "658f608cf5b14c7b3ad4e0bedcc01367e3afb84bb436c4a189424a020208abe1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0147",
  "status": "queued"
}
```


### species_0148 — Ngựa Bùn Cỏ

```json
{
  "species_id": "species_0148",
  "source_species_id": "NguaBunCo",
  "display_name_vi": "Ngựa Bùn Cỏ",
  "race_id": "beast",
  "star": 5,
  "species_class": "special",
  "batch": 30,
  "source_portrait": "apps/game-client/assets/pets/apk84/NguaBunCo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NguaBunCo/sprites.png",
  "source_portrait_sha256": "3e448c92d3f4916125f341a0e02f0ba6f3a84c11b6b6d08e220010341e5a54dd",
  "source_atlas_sha256": "55b3ed355fa52deefeaa12db0b6cfdf889e1deb29c401c21e7164b4a7d808e4d",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0148",
  "status": "queued"
}
```


### species_0149 — Thú Vàng Một Sừng

```json
{
  "species_id": "species_0149",
  "source_species_id": "ThuVangMotSung",
  "display_name_vi": "Thú Vàng Một Sừng",
  "race_id": "beast",
  "star": 5,
  "species_class": "special",
  "batch": 30,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuVangMotSung/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuVangMotSung/sprites.png",
  "source_portrait_sha256": "86ee6134832e6b2a9c5dab284c824fa4c407f7e128f57d1cea91d4bd8cff16e6",
  "source_atlas_sha256": "669cf28272013a049ed225f6a4ab8b9948b5cf1fc20c58d668391342e9b3baea",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0149",
  "status": "queued"
}
```


### species_0151 — Đại Vương Bọ Cạp

```json
{
  "species_id": "species_0151",
  "source_species_id": "DaiVuongBoCap",
  "display_name_vi": "Đại Vương Bọ Cạp",
  "race_id": "insect",
  "star": 5,
  "species_class": "special",
  "batch": 30,
  "source_portrait": "apps/game-client/assets/pets/apk84/DaiVuongBoCap/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DaiVuongBoCap/sprites.png",
  "source_portrait_sha256": "66158355774c320fda9920326bff46a7ff1877c71fab23edbf188242c02356fe",
  "source_atlas_sha256": "3952b34cbceccf86deb162ba914cd0855fb821b2f23d4631b4e889be5c1cc1bc",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0151",
  "status": "queued"
}
```


### species_0152 — Chim Ái Thần

```json
{
  "species_id": "species_0152",
  "source_species_id": "ChimAiThan",
  "display_name_vi": "Chim Ái Thần",
  "race_id": "bird",
  "star": 5,
  "species_class": "special",
  "batch": 30,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimAiThan/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimAiThan/sprites.png",
  "source_portrait_sha256": "1c79937b34e06c139dbc0f5097ef8c60fa216f24b29ec5d5e5d1d98a715f1f2e",
  "source_atlas_sha256": "b2cd5c21a983f0b3f1ead601199e31838e10af529ab1a8f7422f0f340a74fac0",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0152",
  "status": "queued"
}
```
