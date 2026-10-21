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


## Assigned batch 07 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 7
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0028 — Thủy Linh

```json
{
  "species_id": "species_0028",
  "source_species_id": "ThuyLinh",
  "display_name_vi": "Thủy Linh",
  "race_id": "plant",
  "star": 2,
  "species_class": "normal",
  "batch": 7,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuyLinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuyLinh/sprites.png",
  "source_portrait_sha256": "24d0ded24f83e0e099153d670493ff4a6b0e30a0ec05b95e735651add01c93f6",
  "source_atlas_sha256": "b69e14853bdcadaef336fe1fb86c0a0273a4b7ac9d7e9b828bbfa0316f3a6290",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0028",
  "status": "queued"
}
```


### species_0029 — Trúc Địa Linh

```json
{
  "species_id": "species_0029",
  "source_species_id": "TrucDiaLinh",
  "display_name_vi": "Trúc Địa Linh",
  "race_id": "plant",
  "star": 2,
  "species_class": "normal",
  "batch": 7,
  "source_portrait": "apps/game-client/assets/pets/apk84/TrucDiaLinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TrucDiaLinh/sprites.png",
  "source_portrait_sha256": "ef7b8609b2f8cd7489de0cbf0be06911f5b3e0f1cc3fac5407a1a6ad7f873f9f",
  "source_atlas_sha256": "2b912adcf328aa6429d7cff04fd86c28c225884cb59de7359d6713ca8a7ed93e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0029",
  "status": "queued"
}
```


### species_0031 — Yêu Tinh Dứa

```json
{
  "species_id": "species_0031",
  "source_species_id": "YeuTinhDua",
  "display_name_vi": "Yêu Tinh Dứa",
  "race_id": "plant",
  "star": 2,
  "species_class": "normal",
  "batch": 7,
  "source_portrait": "apps/game-client/assets/pets/apk84/YeuTinhDua/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/YeuTinhDua/sprites.png",
  "source_portrait_sha256": "7923e661b8cc508b254cbf9f05dddb0e1781b7d60525d4e71ed966a33a08b664",
  "source_atlas_sha256": "faa0b64981dfec2ee96a0bcd469d4e37c12e490fcafec8873c146d5c317c1f36",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0031",
  "status": "queued"
}
```


### species_0032 — Hoa Môi

```json
{
  "species_id": "species_0032",
  "source_species_id": "HoaMoi",
  "display_name_vi": "Hoa Môi",
  "race_id": "plant",
  "star": 3,
  "species_class": "normal",
  "batch": 7,
  "source_portrait": "apps/game-client/assets/pets/apk84/HoaMoi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HoaMoi/sprites.png",
  "source_portrait_sha256": "873d8d6fadc978e5b1365ca3076b075380c7a83975e5dd678adad9d828134d93",
  "source_atlas_sha256": "e57ef5a1bc112031949f3f5b0e5568822c825c43ca3f8140c7f26a5cf56ad813",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0032",
  "status": "queued"
}
```


### species_0033 — Hoa Hướng Dương

```json
{
  "species_id": "species_0033",
  "source_species_id": "HoaHuongDuong",
  "display_name_vi": "Hoa Hướng Dương",
  "race_id": "plant",
  "star": 3,
  "species_class": "normal",
  "batch": 7,
  "source_portrait": "apps/game-client/assets/pets/apk84/HoaHuongDuong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HoaHuongDuong/sprites.png",
  "source_portrait_sha256": "8be39292cb544d8138b90d60572d05809f3f6cc19cc8be066a3b491da0c07dec",
  "source_atlas_sha256": "17316f7536277b6f9899104dea4eeaaae53d1d70e1c7844a3853dcd078a3f9e2",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0033",
  "status": "queued"
}
```
