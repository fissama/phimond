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


## Assigned batch 26 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 26
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0126 — Trùng Mẫu Mào Vàng

```json
{
  "species_id": "species_0126",
  "source_species_id": "TrungMauMaoVang",
  "display_name_vi": "Trùng Mẫu Mào Vàng",
  "race_id": "insect",
  "star": 5,
  "species_class": "special",
  "batch": 26,
  "source_portrait": "apps/game-client/assets/pets/apk84/TrungMauMaoVang/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TrungMauMaoVang/sprites.png",
  "source_portrait_sha256": "21001fe214f014022c909298e13f741ec3d0da177bbc7326fc360f7e4aa08de9",
  "source_atlas_sha256": "0a9c575453eba58de761caa4e20f9a449610290ad319b5fa76337a71f5109aae",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0126",
  "status": "queued"
}
```


### species_0127 — Quái Vật Rương Báu

```json
{
  "species_id": "species_0127",
  "source_species_id": "QuaiVatRuongBau",
  "display_name_vi": "Quái Vật Rương Báu",
  "race_id": "spirit",
  "star": 1,
  "species_class": "normal",
  "batch": 26,
  "source_portrait": "apps/game-client/assets/pets/apk84/QuaiVatRuongBau/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/QuaiVatRuongBau/sprites.png",
  "source_portrait_sha256": "d9a2f8b609c4ba203b67f24ea42f72d64277d53241abddb3f7d4eed02a3d6d01",
  "source_atlas_sha256": "2216b92d09b1d5c253bfb6761feeb912c76b6f7f43cea9355235752a776843f5",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0127",
  "status": "queued"
}
```


### species_0128 — Chong Chóng Gió

```json
{
  "species_id": "species_0128",
  "source_species_id": "ChongChongGio",
  "display_name_vi": "Chong Chóng Gió",
  "race_id": "spirit",
  "star": 1,
  "species_class": "normal",
  "batch": 26,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChongChongGio/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChongChongGio/sprites.png",
  "source_portrait_sha256": "5d9b7394557b2fad2a5b83de0495d603878c2240a469923f3667855928ad4c38",
  "source_atlas_sha256": "805d9b3c9aa4855bd8ae61ce4711d559f256a3af2bc381cb8abcceb24ca2d1e8",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0128",
  "status": "queued"
}
```


### species_0129 — Quái Vật Nham Thạch

```json
{
  "species_id": "species_0129",
  "source_species_id": "QuaiVatNhamThach",
  "display_name_vi": "Quái Vật Nham Thạch",
  "race_id": "spirit",
  "star": 1,
  "species_class": "normal",
  "batch": 26,
  "source_portrait": "apps/game-client/assets/pets/apk84/QuaiVatNhamThach/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/QuaiVatNhamThach/sprites.png",
  "source_portrait_sha256": "04c384a594f6396384ec83eb83bfc14ad583b08386ae40d0447d35ad2f3e5329",
  "source_atlas_sha256": "0a61f759f64b89c008dc9984175ed6d429aa073e28b10c4ab46f8632d2d81836",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0129",
  "status": "queued"
}
```


### species_0130 — Đá Mặt Quỷ

```json
{
  "species_id": "species_0130",
  "source_species_id": "DaMatQuy",
  "display_name_vi": "Đá Mặt Quỷ",
  "race_id": "spirit",
  "star": 1,
  "species_class": "normal",
  "batch": 26,
  "source_portrait": "apps/game-client/assets/pets/apk84/DaMatQuy/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DaMatQuy/sprites.png",
  "source_portrait_sha256": "503bceacc88479b6e4c071b81047fad4a64602cb3ba8dafd45ac5d581cb53a0b",
  "source_atlas_sha256": "d0f3740acf5a4d78a3fc6145e996fe615bc77cef18b3472a0c3093af660df738",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0130",
  "status": "queued"
}
```
