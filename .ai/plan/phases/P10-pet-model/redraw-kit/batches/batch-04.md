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


## Assigned batch 04 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 4
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0012 — Xác Chết Nửa Người

```json
{
  "species_id": "species_0012",
  "source_species_id": "XacChetNuaNguoi",
  "display_name_vi": "Xác Chết Nửa Người",
  "race_id": "undead",
  "star": 3,
  "species_class": "normal",
  "batch": 4,
  "source_portrait": "apps/game-client/assets/pets/apk84/XacChetNuaNguoi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/XacChetNuaNguoi/sprites.png",
  "source_portrait_sha256": "bf6cdb257d36aa16a3463daff7fafac4af62b967d4986e22e15675ef116c751e",
  "source_atlas_sha256": "0ac69096d584c74d7673a33c28d35fecb2f5e500d35abba1bbca79e24405ecea",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0012",
  "status": "queued"
}
```


### species_0013 — Ma Ảnh

```json
{
  "species_id": "species_0013",
  "source_species_id": "MaAnh",
  "display_name_vi": "Ma Ảnh",
  "race_id": "undead",
  "star": 3,
  "species_class": "normal",
  "batch": 4,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaAnh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaAnh/sprites.png",
  "source_portrait_sha256": "61152f861a27f7ec0009d50303e00bd89001ad53e7f703696d66bed928f5fb1b",
  "source_atlas_sha256": "78d8adc16734561d28e9a98f3f178a326c187fb438845a0600d9f1e6d924bf90",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0013",
  "status": "queued"
}
```


### species_0014 — Tinh Tinh Xanh Ma Giới

```json
{
  "species_id": "species_0014",
  "source_species_id": "TinhTinhXanhMaGioi",
  "display_name_vi": "Tinh Tinh Xanh Ma Giới",
  "race_id": "undead",
  "star": 3,
  "species_class": "normal",
  "batch": 4,
  "source_portrait": "apps/game-client/assets/pets/apk84/TinhTinhXanhMaGioi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TinhTinhXanhMaGioi/sprites.png",
  "source_portrait_sha256": "5e4eaf6de6ecc1dc4744191afbbd7686da0bbd01d7d06ba32e5d0780ab3c2a38",
  "source_atlas_sha256": "c72729682e67684af739a8cd1ee4d6a9e5599c328b136e08b407752be978a0c3",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0014",
  "status": "queued"
}
```


### species_0015 — Tử Thần

```json
{
  "species_id": "species_0015",
  "source_species_id": "TuThan",
  "display_name_vi": "Tử Thần",
  "race_id": "undead",
  "star": 4,
  "species_class": "normal",
  "batch": 4,
  "source_portrait": "apps/game-client/assets/pets/apk84/TuThan/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TuThan/sprites.png",
  "source_portrait_sha256": "72aa1bb8dfc370f16d8c801d8a5f35c6ff07b6021c5a69f2fb70d80b8a2bcbe8",
  "source_atlas_sha256": "e8bf0f2fa7af46e37a5ea48b9d5070ee1e0b3fab7a1bfbde36a8aeae2bcb4323",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0015",
  "status": "queued"
}
```


### species_0016 — Pharaon

```json
{
  "species_id": "species_0016",
  "source_species_id": "Pharaon",
  "display_name_vi": "Pharaon",
  "race_id": "undead",
  "star": 4,
  "species_class": "normal",
  "batch": 4,
  "source_portrait": "apps/game-client/assets/pets/apk84/Pharaon/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/Pharaon/sprites.png",
  "source_portrait_sha256": "a4d392aa5ff594ac086cf4012a6edbea14dd564fb9b616989b4e0dea3be92c6c",
  "source_atlas_sha256": "9ccda5c9c5291cc2a633560026f182346c094b48dd53548a510e73fb20e55315",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0016",
  "status": "queued"
}
```
