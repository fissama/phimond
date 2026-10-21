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


## Assigned batch 16 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 16
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0076 — Thú Răng Kiếm

```json
{
  "species_id": "species_0076",
  "source_species_id": "ThuRangKiem",
  "display_name_vi": "Thú Răng Kiếm",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 16,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuRangKiem/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuRangKiem/sprites.png",
  "source_portrait_sha256": "92199f3533a11cec2fb60c9626613b0b89b21f9b9c050ce1108bed59e4b9a3b1",
  "source_atlas_sha256": "708e00900bb52aee134c551442f61313149bf2bc4696246310741901880b27ed",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0076",
  "status": "queued"
}
```


### species_0077 — Thiên Nga Cực Địa

```json
{
  "species_id": "species_0077",
  "source_species_id": "ThienNgaCucDia",
  "display_name_vi": "Thiên Nga Cực Địa",
  "race_id": "beast",
  "star": 2,
  "species_class": "normal",
  "batch": 16,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThienNgaCucDia/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThienNgaCucDia/sprites.png",
  "source_portrait_sha256": "90248ac437683efc3bbcb02fbdb36fdf6be92c7d0a9058c450c04ffd79d2d5d4",
  "source_atlas_sha256": "53a6f75ab021c3660c57a764a92ebace6b4ee64f28c124d8661ce1afbc4a036b",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0077",
  "status": "queued"
}
```


### species_0078 — Dương Dương Dương

```json
{
  "species_id": "species_0078",
  "source_species_id": "DuongDuongDuong",
  "display_name_vi": "Dương Dương Dương",
  "race_id": "beast",
  "star": 2,
  "species_class": "normal",
  "batch": 16,
  "source_portrait": "apps/game-client/assets/pets/apk84/DuongDuongDuong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DuongDuongDuong/sprites.png",
  "source_portrait_sha256": "0d2b5e0575d0c9beaf5af1de16dc5e25419a09d3fc0ddaa25a77e3f8677984c6",
  "source_atlas_sha256": "fc3f0e160005526431e23fab18904a4f5c4d0e396b84d550a882b358d35ceb34",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0078",
  "status": "queued"
}
```


### species_0079 — Mực Hắc Ám

```json
{
  "species_id": "species_0079",
  "source_species_id": "MucHacAm",
  "display_name_vi": "Mực Hắc Ám",
  "race_id": "beast",
  "star": 2,
  "species_class": "normal",
  "batch": 16,
  "source_portrait": "apps/game-client/assets/pets/apk84/MucHacAm/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MucHacAm/sprites.png",
  "source_portrait_sha256": "51f94c73264ad3201710c29503ec52b5668c438b7a1aecc5c6388ecb4f807cdb",
  "source_atlas_sha256": "a860b52394c8c86c93939dacd031ec0f8f58a680cd29d26385f02e8c3fb49fdb",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0079",
  "status": "queued"
}
```


### species_0080 — Gấu Vết Dao

```json
{
  "species_id": "species_0080",
  "source_species_id": "GauVetDao",
  "display_name_vi": "Gấu Vết Dao",
  "race_id": "beast",
  "star": 2,
  "species_class": "normal",
  "batch": 16,
  "source_portrait": "apps/game-client/assets/pets/apk84/GauVetDao/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/GauVetDao/sprites.png",
  "source_portrait_sha256": "315f95773cf2c527c99c1c0f1d2608af2a0b973b75720f664384e43e239846d4",
  "source_atlas_sha256": "b43f9398775eacf98a69c94b5a4c9017bd30b4583a5fd1a6ec180846ad870c77",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0080",
  "status": "queued"
}
```
