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


## Assigned batch 09 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 9
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0041 — Rắn Xương Trắng

```json
{
  "species_id": "species_0041",
  "source_species_id": "RanXuongTrang",
  "display_name_vi": "Rắn Xương Trắng",
  "race_id": "dragon",
  "star": 1,
  "species_class": "normal",
  "batch": 9,
  "source_portrait": "apps/game-client/assets/pets/apk84/RanXuongTrang/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RanXuongTrang/sprites.png",
  "source_portrait_sha256": "47b5d04fe5ef72c38feb9965fe6d1f6297db056a648d5d5d23884b3cf119ac52",
  "source_atlas_sha256": "26f5d3e038b8bd5e838db65cd3b94853822086325611b9501236300a1646624a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0041",
  "status": "queued"
}
```


### species_0042 — Tiểu Ma Long

```json
{
  "species_id": "species_0042",
  "source_species_id": "TieuMaLong",
  "display_name_vi": "Tiểu Ma Long",
  "race_id": "dragon",
  "star": 1,
  "species_class": "normal",
  "batch": 9,
  "source_portrait": "apps/game-client/assets/pets/apk84/TieuMaLong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TieuMaLong/sprites.png",
  "source_portrait_sha256": "aee267a03628341a458278c144aa6800d6f2216c8cc85aa6eb654682a5be7318",
  "source_atlas_sha256": "bb6a776caa19dc38b8b761fe7a0e34beb98118a94c04fb22c464a486bc9763d6",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0042",
  "status": "queued"
}
```


### species_0043 — Rồng Cổ Dài

```json
{
  "species_id": "species_0043",
  "source_species_id": "RongCoDai",
  "display_name_vi": "Rồng Cổ Dài",
  "race_id": "dragon",
  "star": 2,
  "species_class": "normal",
  "batch": 9,
  "source_portrait": "apps/game-client/assets/pets/apk84/RongCoDai/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RongCoDai/sprites.png",
  "source_portrait_sha256": "94640d9136c91721b08816dc0c4c8022154d6462518c64732735d7917da3f657",
  "source_atlas_sha256": "54ef863c0ea2c458b5aec593f7ba00f16de9869e72e692bdfef49922d665c296",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0043",
  "status": "queued"
}
```


### species_0044 — Rồng Vuốt Xương

```json
{
  "species_id": "species_0044",
  "source_species_id": "RongVuotXuong",
  "display_name_vi": "Rồng Vuốt Xương",
  "race_id": "dragon",
  "star": 2,
  "species_class": "normal",
  "batch": 9,
  "source_portrait": "apps/game-client/assets/pets/apk84/RongVuotXuong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RongVuotXuong/sprites.png",
  "source_portrait_sha256": "b9ff37fa9a6aebea2b428d9874f60944caa1b9ce366a9cfd029e0fb5f40c4c78",
  "source_atlas_sha256": "81fb0d66c71a095adaf9e90ee05be896a15341a206b7af20be9caae65b000d40",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0044",
  "status": "queued"
}
```


### species_0045 — Nham Long

```json
{
  "species_id": "species_0045",
  "source_species_id": "NhamLong",
  "display_name_vi": "Nham Long",
  "race_id": "dragon",
  "star": 2,
  "species_class": "normal",
  "batch": 9,
  "source_portrait": "apps/game-client/assets/pets/apk84/NhamLong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NhamLong/sprites.png",
  "source_portrait_sha256": "90da1d2847cbac3b9b4872438d9e7350a62467914585478d4aea778084b39c54",
  "source_atlas_sha256": "4e9284443902f399eec62aad61c867305ddd3a25b3ce0193a6c7a4e15e5abfd8",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0045",
  "status": "queued"
}
```
