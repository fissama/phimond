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


## Assigned batch 23 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 23
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0111 — Ốc Sên Hoa

```json
{
  "species_id": "species_0111",
  "source_species_id": "OcSenHoa",
  "display_name_vi": "Ốc Sên Hoa",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 23,
  "source_portrait": "apps/game-client/assets/pets/apk84/OcSenHoa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/OcSenHoa/sprites.png",
  "source_portrait_sha256": "58e24a93435543d1c5f9fb0f6134a2dd527f0133e18deb219c1c2b8f9fff5833",
  "source_atlas_sha256": "73c7e21f86db64d01d1ae03bb6cfecea0b41e09bf2663ae3538e846fe73d870a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0111",
  "status": "queued"
}
```


### species_0112 — Nhện Độc

```json
{
  "species_id": "species_0112",
  "source_species_id": "NhenDoc",
  "display_name_vi": "Nhện Độc",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 23,
  "source_portrait": "apps/game-client/assets/pets/apk84/NhenDoc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NhenDoc/sprites.png",
  "source_portrait_sha256": "56f7f513f1813e75aed46072ae143957ff687fc0a520f7a8487182a5fcdae533",
  "source_atlas_sha256": "9d706cc23e545ef2485d2a9bb768e521cff3e79359aa7fdcfe9b7c9302f185ef",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0112",
  "status": "queued"
}
```


### species_0113 — Thiên Ngưu

```json
{
  "species_id": "species_0113",
  "source_species_id": "ThienNguu",
  "display_name_vi": "Thiên Ngưu",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 23,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThienNguu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThienNguu/sprites.png",
  "source_portrait_sha256": "f157c67686c095fc49c874b4eb105cfab17279c6b920e5e6244d8a15b2b3c6d7",
  "source_atlas_sha256": "a7418f97014503c9e6a8068833c2c8b828a6e0807a818967a9c538fc4749bfa9",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0113",
  "status": "queued"
}
```


### species_0114 — Bọ Cánh Cứng Răng Kiếm

```json
{
  "species_id": "species_0114",
  "source_species_id": "BoCanhCungRangKiem",
  "display_name_vi": "Bọ Cánh Cứng Răng Kiếm",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 23,
  "source_portrait": "apps/game-client/assets/pets/apk84/BoCanhCungRangKiem/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/BoCanhCungRangKiem/sprites.png",
  "source_portrait_sha256": "03656d1e5fa63bb559237dc5c305cc5d4483365fe78a64b2187c33105b45787e",
  "source_atlas_sha256": "42a636976c2f58f3b90bd8106b688fefcdd922366517c78171b7e306bc9b0216",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0114",
  "status": "queued"
}
```


### species_0115 — Giun Đất Móng Sắt

```json
{
  "species_id": "species_0115",
  "source_species_id": "GiunDatMongSat",
  "display_name_vi": "Giun Đất Móng Sắt",
  "race_id": "insect",
  "star": 2,
  "species_class": "normal",
  "batch": 23,
  "source_portrait": "apps/game-client/assets/pets/apk84/GiunDatMongSat/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/GiunDatMongSat/sprites.png",
  "source_portrait_sha256": "36e6b8a823fb8552a2d4441547e3aff47e810a546baa62731a4115f0b75d5ebc",
  "source_atlas_sha256": "26a8abdaaaedadfc87f73aff8b267ba500939a3599f367c7ac33b51b8f8c57c1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0115",
  "status": "queued"
}
```
