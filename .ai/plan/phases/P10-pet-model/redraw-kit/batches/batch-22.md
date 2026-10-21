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


## Assigned batch 22 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 22
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0106 — Chim Cú Địa Ngục

```json
{
  "species_id": "species_0106",
  "source_species_id": "ChimCuDiaNguc",
  "display_name_vi": "Chim Cú Địa Ngục",
  "race_id": "bird",
  "star": 5,
  "species_class": "normal",
  "batch": 22,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimCuDiaNguc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimCuDiaNguc/sprites.png",
  "source_portrait_sha256": "fbd527414f1821b8571dc15fa3f1100d8797edc058101f1597b219028c3c820e",
  "source_atlas_sha256": "461904ca1eec78662fb96c594db23c1f279d1de97515808e9865dfb0425d3182",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0106",
  "status": "queued"
}
```


### species_0107 — Đại Bàng Vàng

```json
{
  "species_id": "species_0107",
  "source_species_id": "DaiBangVang",
  "display_name_vi": "Đại Bàng Vàng",
  "race_id": "bird",
  "star": 5,
  "species_class": "normal",
  "batch": 22,
  "source_portrait": "apps/game-client/assets/pets/apk84/DaiBangVang/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DaiBangVang/sprites.png",
  "source_portrait_sha256": "b35da045102648ec85668a4ab45ea1cc56980d86f7c9a1ee676da6f1c388cfaa",
  "source_atlas_sha256": "3e07eb3b0adbf929d4f999530438c27c52fd056a28e97dc654a08640b7839e40",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0107",
  "status": "queued"
}
```


### species_0108 — Ong Giết Người

```json
{
  "species_id": "species_0108",
  "source_species_id": "OngGietNguoi",
  "display_name_vi": "Ong Giết Người",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 22,
  "source_portrait": "apps/game-client/assets/pets/apk84/OngGietNguoi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/OngGietNguoi/sprites.png",
  "source_portrait_sha256": "f1a06512818331529ef06a695f775783ee7464636aeaa8832f845b7f45392933",
  "source_atlas_sha256": "b0faed92ac66ce13a76d22e5ed15423c1b45a23de30af838033e1e02ecdaec99",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0108",
  "status": "queued"
}
```


### species_0109 — Bọ Cạp Sa Mạc

```json
{
  "species_id": "species_0109",
  "source_species_id": "BoCapSaMac",
  "display_name_vi": "Bọ Cạp Sa Mạc",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 22,
  "source_portrait": "apps/game-client/assets/pets/apk84/BoCapSaMac/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/BoCapSaMac/sprites.png",
  "source_portrait_sha256": "2ce87fd39d2a67f66b709002e9c262e21ed1bd95c766529f18983df821e7e675",
  "source_atlas_sha256": "f8201ff6a8745c484c97f87a59ec41b0c663e1fd280e4b6305d7faaec4503d17",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0109",
  "status": "queued"
}
```


### species_0110 — Bọ Ngựa Móng Sắt

```json
{
  "species_id": "species_0110",
  "source_species_id": "BoNguaMongSat",
  "display_name_vi": "Bọ Ngựa Móng Sắt",
  "race_id": "insect",
  "star": 1,
  "species_class": "normal",
  "batch": 22,
  "source_portrait": "apps/game-client/assets/pets/apk84/BoNguaMongSat/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/BoNguaMongSat/sprites.png",
  "source_portrait_sha256": "d16ef486de56210dd6b3764f53af7e687cbadd6d007712a76f7739d5c1e854b7",
  "source_atlas_sha256": "6f15365d8ffaba271d9f2a53114928bff0a9bb74ce95fe1db2ca9ce4db6e8212",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0110",
  "status": "queued"
}
```
