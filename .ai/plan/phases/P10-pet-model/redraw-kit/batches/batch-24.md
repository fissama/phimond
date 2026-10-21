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


## Assigned batch 24 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 24
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0116 — Châu Chấu Móng Lớn

```json
{
  "species_id": "species_0116",
  "source_species_id": "ChauChauMongLon",
  "display_name_vi": "Châu Chấu Móng Lớn",
  "race_id": "insect",
  "star": 2,
  "species_class": "normal",
  "batch": 24,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChauChauMongLon/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChauChauMongLon/sprites.png",
  "source_portrait_sha256": "910a878d5a3606c7983e2c2e4e23c356faf3cba48bd2ea940b31c40618f002b6",
  "source_atlas_sha256": "83466ab7e70e634b6155b16fb3d376521619592508de52b96702873e90f167f3",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0116",
  "status": "queued"
}
```


### species_0117 — Thú Một Sừng Vỏ Cứng

```json
{
  "species_id": "species_0117",
  "source_species_id": "ThuMotSungVoCung",
  "display_name_vi": "Thú Một Sừng Vỏ Cứng",
  "race_id": "insect",
  "star": 2,
  "species_class": "normal",
  "batch": 24,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuMotSungVoCung/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuMotSungVoCung/sprites.png",
  "source_portrait_sha256": "818e36a071266b08d87baab40bc6d4e5d13d32bc8703fcf65495c44465fc9c9d",
  "source_atlas_sha256": "939195e7792c4997bb99d9e417e68c494c816c938d6b9e819f48ebc10bc97cd8",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0117",
  "status": "queued"
}
```


### species_0118 — Bướm Hoa Vũ

```json
{
  "species_id": "species_0118",
  "source_species_id": "BuomHoaVu",
  "display_name_vi": "Bướm Hoa Vũ",
  "race_id": "insect",
  "star": 2,
  "species_class": "normal",
  "batch": 24,
  "source_portrait": "apps/game-client/assets/pets/apk84/BuomHoaVu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/BuomHoaVu/sprites.png",
  "source_portrait_sha256": "8e565cc96264eef9a7e888ad2cf2b1545f7b73eb3a904d3cc06a4bdfdcd960b3",
  "source_atlas_sha256": "23a4245117e234a43042fe6b69ebb59979c199db5e221d5e1c0ef73c2bc073aa",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0118",
  "status": "queued"
}
```


### species_0119 — Cua Ký Sinh

```json
{
  "species_id": "species_0119",
  "source_species_id": "CuaKySinh",
  "display_name_vi": "Cua Ký Sinh",
  "race_id": "insect",
  "star": 3,
  "species_class": "normal",
  "batch": 24,
  "source_portrait": "apps/game-client/assets/pets/apk84/CuaKySinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/CuaKySinh/sprites.png",
  "source_portrait_sha256": "e5c691d33699aefdbc1f1985c2064d5a8417508e9c4c7af2b4e098f4f54f966c",
  "source_atlas_sha256": "2295028c21813e2257a192c66cb6db12dcbc95d1134c0149966bd05b7ece05bc",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0119",
  "status": "queued"
}
```


### species_0120 — Tôm Hùm Răng Cưa

```json
{
  "species_id": "species_0120",
  "source_species_id": "TomHumRangCua",
  "display_name_vi": "Tôm Hùm Răng Cưa",
  "race_id": "insect",
  "star": 3,
  "species_class": "normal",
  "batch": 24,
  "source_portrait": "apps/game-client/assets/pets/apk84/TomHumRangCua/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TomHumRangCua/sprites.png",
  "source_portrait_sha256": "3a862caab2552daaec9b7af4b0e71f1025a82f62f18e24ed65311ef87847c168",
  "source_atlas_sha256": "d218cf97a0368d0785992fff70321354229e98787be9f2e27d13048404545772",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0120",
  "status": "queued"
}
```
