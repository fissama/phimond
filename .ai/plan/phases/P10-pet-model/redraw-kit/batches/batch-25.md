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


## Assigned batch 25 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 25
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0121 — Hải Mã Bong Bóng

```json
{
  "species_id": "species_0121",
  "source_species_id": "HaiMaBongBong",
  "display_name_vi": "Hải Mã Bong Bóng",
  "race_id": "insect",
  "star": 3,
  "species_class": "normal",
  "batch": 25,
  "source_portrait": "apps/game-client/assets/pets/apk84/HaiMaBongBong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HaiMaBongBong/sprites.png",
  "source_portrait_sha256": "bb60be9532c3c5dad94788fd3623b7afc5fa9cdbb18e177c905063e04bdfa89a",
  "source_atlas_sha256": "34f6f3aef4307400a98782fc2a81e233b6efdd1c6d6aebb1768935140e1daf84",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0121",
  "status": "queued"
}
```


### species_0122 — Trùng Hốt Lỗ

```json
{
  "species_id": "species_0122",
  "source_species_id": "TrungHotLo",
  "display_name_vi": "Trùng Hốt Lỗ",
  "race_id": "insect",
  "star": 4,
  "species_class": "normal",
  "batch": 25,
  "source_portrait": "apps/game-client/assets/pets/apk84/TrungHotLo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TrungHotLo/sprites.png",
  "source_portrait_sha256": "326a9ab526c372281e640e2e06e2a9e6cd5e9ef969a0aad6bc1b0e112f41a9a7",
  "source_atlas_sha256": "22c2e8f78bdbd1caf30690460c79418179c8cf7dd28aa32a223c93263a6700b0",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0122",
  "status": "queued"
}
```


### species_0123 — Trùng Gai Nhọn

```json
{
  "species_id": "species_0123",
  "source_species_id": "TrungGaiNhon",
  "display_name_vi": "Trùng Gai Nhọn",
  "race_id": "insect",
  "star": 4,
  "species_class": "normal",
  "batch": 25,
  "source_portrait": "apps/game-client/assets/pets/apk84/TrungGaiNhon/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TrungGaiNhon/sprites.png",
  "source_portrait_sha256": "1f60afd013bac6cc56c5b8965f6dd810caff7264a5aff051cba8bd7b13109504",
  "source_atlas_sha256": "317e03c670569cd8e52e5cf726b87ddf94c4311be443b29ae6c3f4ad75611284",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0123",
  "status": "queued"
}
```


### species_0124 — Trùng Bất Tử Địa Huyệt

```json
{
  "species_id": "species_0124",
  "source_species_id": "TrungBatTuDiaHuyet",
  "display_name_vi": "Trùng Bất Tử Địa Huyệt",
  "race_id": "insect",
  "star": 5,
  "species_class": "normal",
  "batch": 25,
  "source_portrait": "apps/game-client/assets/pets/apk84/TrungBatTuDiaHuyet/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TrungBatTuDiaHuyet/sprites.png",
  "source_portrait_sha256": "77b9e7abbeea6a44b2ca38e97673eb4e0dd3a6118e6bef941715175ad30b8cd9",
  "source_atlas_sha256": "cb835a79298db8992f2ad78da7a6fa7adc201fc95785994b05ccec2f76df454d",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0124",
  "status": "queued"
}
```


### species_0125 — Nhện Phu Nhân

```json
{
  "species_id": "species_0125",
  "source_species_id": "NhenPhuNhan",
  "display_name_vi": "Nhện Phu Nhân",
  "race_id": "insect",
  "star": 5,
  "species_class": "normal",
  "batch": 25,
  "source_portrait": "apps/game-client/assets/pets/apk84/NhenPhuNhan/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NhenPhuNhan/sprites.png",
  "source_portrait_sha256": "e601d03af9985d6672ac1dceb8aa001d3c49cf2748d76fa53846bccc66d74814",
  "source_atlas_sha256": "e46cb4557448a9df44e6b2925ca292766f5caa818f5ba887cce321d6f3900150",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0125",
  "status": "queued"
}
```
