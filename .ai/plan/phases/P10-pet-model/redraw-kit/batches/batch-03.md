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


## Assigned batch 03 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 3
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0007 — Chó Ác Ma

```json
{
  "species_id": "species_0007",
  "source_species_id": "ChoAcMa",
  "display_name_vi": "Chó Ác Ma",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 3,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChoAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChoAcMa/sprites.png",
  "source_portrait_sha256": "a9e9f4234feafa1f92ce4b66b626030d362acf496be2158f5ca5529d7b6aabf6",
  "source_atlas_sha256": "75bdb08c916e98878a386c1ab73850c7b3483852d6b2c5f335841b360786abb4",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0007",
  "status": "queued"
}
```


### species_0008 — Lửa Yêu

```json
{
  "species_id": "species_0008",
  "source_species_id": "LuaYeu",
  "display_name_vi": "Lửa Yêu",
  "race_id": "undead",
  "star": 2,
  "species_class": "normal",
  "batch": 3,
  "source_portrait": "apps/game-client/assets/pets/apk84/LuaYeu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/LuaYeu/sprites.png",
  "source_portrait_sha256": "01a9deb1c05a3ad925fbe3fbf066ea3b820043123b89812999878d8812e1a76c",
  "source_atlas_sha256": "3479c3f27d2c95dc87313f3787ee7973518a7b73a2ea889282a75d4345ec3ced",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0008",
  "status": "queued"
}
```


### species_0009 — Xác Chết Vuốt Sắc

```json
{
  "species_id": "species_0009",
  "source_species_id": "XacChetVuotSac",
  "display_name_vi": "Xác Chết Vuốt Sắc",
  "race_id": "undead",
  "star": 2,
  "species_class": "normal",
  "batch": 3,
  "source_portrait": "apps/game-client/assets/pets/apk84/XacChetVuotSac/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/XacChetVuotSac/sprites.png",
  "source_portrait_sha256": "ac11f6ad33f5d1931c1864043cc4c3af0ef5adf3528b5c00309237bdf7111c68",
  "source_atlas_sha256": "ca1fd91bd39666fca1fa0b01c594d5d933c97d4b65afa63e976411bc64ec5a11",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0009",
  "status": "queued"
}
```


### species_0010 — Cá Xương

```json
{
  "species_id": "species_0010",
  "source_species_id": "CaXuong",
  "display_name_vi": "Cá Xương",
  "race_id": "undead",
  "star": 2,
  "species_class": "normal",
  "batch": 3,
  "source_portrait": "apps/game-client/assets/pets/apk84/CaXuong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/CaXuong/sprites.png",
  "source_portrait_sha256": "d0ab53e15306fcf5a7c8fd2667eb0cf7a684bbc96bfad36e2df9664fe12a8e30",
  "source_atlas_sha256": "aea34b7c25a54d0de697f34c1dbe10b306c67ddcf9763a2820fd22690902a4d1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0010",
  "status": "queued"
}
```


### species_0011 — Kẻ Đồ Tể

```json
{
  "species_id": "species_0011",
  "source_species_id": "KeDoTe",
  "display_name_vi": "Kẻ Đồ Tể",
  "race_id": "undead",
  "star": 2,
  "species_class": "normal",
  "batch": 3,
  "source_portrait": "apps/game-client/assets/pets/apk84/KeDoTe/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/KeDoTe/sprites.png",
  "source_portrait_sha256": "11294ed7cff2ec9f208ca06951bf04c468f5b1198dee514759d16e3e3d1aba46",
  "source_atlas_sha256": "66ca4d0e81959714351812b04078e932f725392b62f4bb1b5064fcba8e3ed21a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0011",
  "status": "queued"
}
```
