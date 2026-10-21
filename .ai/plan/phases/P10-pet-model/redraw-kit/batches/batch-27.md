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


## Assigned batch 27 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 27
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0131 — Hư Không Hắc Ám

```json
{
  "species_id": "species_0131",
  "source_species_id": "HuKhongHacAm",
  "display_name_vi": "Hư Không Hắc Ám",
  "race_id": "spirit",
  "star": 1,
  "species_class": "normal",
  "batch": 27,
  "source_portrait": "apps/game-client/assets/pets/apk84/HuKhongHacAm/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HuKhongHacAm/sprites.png",
  "source_portrait_sha256": "c26cb677dc67514792b488768078bf4752291d3450300f62d121384d63d2b02d",
  "source_atlas_sha256": "201814e95ce82234f21d4904954d84d7cbab529776407e6866ad44978fc0d94e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0131",
  "status": "queued"
}
```


### species_0132 — Sách Ma Pháp

```json
{
  "species_id": "species_0132",
  "source_species_id": "SachMaPhap",
  "display_name_vi": "Sách Ma Pháp",
  "race_id": "spirit",
  "star": 2,
  "species_class": "normal",
  "batch": 27,
  "source_portrait": "apps/game-client/assets/pets/apk84/SachMaPhap/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/SachMaPhap/sprites.png",
  "source_portrait_sha256": "fd1df91a1d9913b831b7cf59c566864870e18033634d31e82ca37ab0849053fc",
  "source_atlas_sha256": "8728ebec6651e0f0ae4e41e9a5a77d0bed2664d7f73e1287e22bb6d11e6b4d02",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0132",
  "status": "queued"
}
```


### species_0133 — Ma Kiếm

```json
{
  "species_id": "species_0133",
  "source_species_id": "MaKiem",
  "display_name_vi": "Ma Kiếm",
  "race_id": "spirit",
  "star": 2,
  "species_class": "normal",
  "batch": 27,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaKiem/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaKiem/sprites.png",
  "source_portrait_sha256": "75365067795bf7bf5819c8af02aa6a205fcea28f69b91917d619e1a889ae3f40",
  "source_atlas_sha256": "8f32af6cfd22fd4c2ce9a129bcd408955a7ea7c7974256d17ebc280100d65ec5",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0133",
  "status": "queued"
}
```


### species_0134 — Con Rối Gạch Đá

```json
{
  "species_id": "species_0134",
  "source_species_id": "ConRoiGachDa",
  "display_name_vi": "Con Rối Gạch Đá",
  "race_id": "spirit",
  "star": 3,
  "species_class": "normal",
  "batch": 27,
  "source_portrait": "apps/game-client/assets/pets/apk84/ConRoiGachDa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ConRoiGachDa/sprites.png",
  "source_portrait_sha256": "50a8d98b60cdca4074735f2d82e1b5bbb798fade635d2a30bdc624cb5a93adbe",
  "source_atlas_sha256": "5c5b9c5eb0292dd6c5d77c711627d4f45d2dd57856c8dfdae3c661286aeb6116",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0134",
  "status": "queued"
}
```


### species_0135 — Thằng Hề Hộp

```json
{
  "species_id": "species_0135",
  "source_species_id": "ThangHeHop",
  "display_name_vi": "Thằng Hề Hộp",
  "race_id": "spirit",
  "star": 3,
  "species_class": "normal",
  "batch": 27,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThangHeHop/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThangHeHop/sprites.png",
  "source_portrait_sha256": "9f487175e40cab17eb0032efc559504ff0edc3f6e6f7a3a4bf5cf2b170247de5",
  "source_atlas_sha256": "80fef5b29c5135befd88c2a471243ef2fbe39f911dc7c64ed52c0b38ddc08b5c",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0135",
  "status": "queued"
}
```
