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


## Assigned batch 17 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 17
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0081 — Rùa Nham Thạch

```json
{
  "species_id": "species_0081",
  "source_species_id": "RuaNhamThach",
  "display_name_vi": "Rùa Nham Thạch",
  "race_id": "beast",
  "star": 3,
  "species_class": "normal",
  "batch": 17,
  "source_portrait": "apps/game-client/assets/pets/apk84/RuaNhamThach/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RuaNhamThach/sprites.png",
  "source_portrait_sha256": "643b66f08f307921b62aba14a82d32fdb6cc89dd3d228333587e487f55ddb949",
  "source_atlas_sha256": "6d87a5a40255aa979b390e6a1b28def266cbaf44268d67dce5bce5a21d6dc55d",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0081",
  "status": "queued"
}
```


### species_0082 — Voi Tai To

```json
{
  "species_id": "species_0082",
  "source_species_id": "VoiTaiTo",
  "display_name_vi": "Voi Tai To",
  "race_id": "beast",
  "star": 3,
  "species_class": "normal",
  "batch": 17,
  "source_portrait": "apps/game-client/assets/pets/apk84/VoiTaiTo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/VoiTaiTo/sprites.png",
  "source_portrait_sha256": "22357b0283a4e8aa461fb737569ddf84b5490763f228e13a07738f185c9ed2fe",
  "source_atlas_sha256": "93069fdcdcec71ab37d5a0bc0875817366228f2d5a2f1b630c302a1a70c2ebd8",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0082",
  "status": "queued"
}
```


### species_0083 — Cáo Chín Đuôi

```json
{
  "species_id": "species_0083",
  "source_species_id": "CaoChinDuoi",
  "display_name_vi": "Cáo Chín Đuôi",
  "race_id": "beast",
  "star": 3,
  "species_class": "normal",
  "batch": 17,
  "source_portrait": "apps/game-client/assets/pets/apk84/CaoChinDuoi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/CaoChinDuoi/sprites.png",
  "source_portrait_sha256": "8eee716f96cf4e10e8534283817bbc60ae4d628bf3e95eb6c162526bf3a88ce6",
  "source_atlas_sha256": "12d48af1f243dca24ad8192b35dc5ff3488c40bd08224799a6d521a92fad84b9",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0083",
  "status": "queued"
}
```


### species_0084 — Tinh Tinh Rock

```json
{
  "species_id": "species_0084",
  "source_species_id": "TinhTinhRock",
  "display_name_vi": "Tinh Tinh Rock",
  "race_id": "beast",
  "star": 4,
  "species_class": "normal",
  "batch": 17,
  "source_portrait": "apps/game-client/assets/pets/apk84/TinhTinhRock/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TinhTinhRock/sprites.png",
  "source_portrait_sha256": "71784151168e3c46fbf28acb28ebc46a4880c1e211a9d7ae89c30ed6cced8d44",
  "source_atlas_sha256": "bcc0ea25eb51e8cf1486191fe5a6e97ddfca7c62adedcd62605e55a97a8039c1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0084",
  "status": "queued"
}
```


### species_0085 — Đại Tuyết Quái

```json
{
  "species_id": "species_0085",
  "source_species_id": "DaiTuyetQuai",
  "display_name_vi": "Đại Tuyết Quái",
  "race_id": "beast",
  "star": 4,
  "species_class": "normal",
  "batch": 17,
  "source_portrait": "apps/game-client/assets/pets/apk84/DaiTuyetQuai/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DaiTuyetQuai/sprites.png",
  "source_portrait_sha256": "2b7a2b1e0fe013e2d32c466b87668d4e3294502442a8168b56f5f18a1b615475",
  "source_atlas_sha256": "62a0ae908e8a7aa2d707c1de8bc64774950aa226be64502c4290efa2b18ae930",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0085",
  "status": "queued"
}
```
