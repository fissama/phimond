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


## Assigned batch 01 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 1
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0018 — Nữ Vương Bạch Cốt

```json
{
  "species_id": "species_0018",
  "source_species_id": "NuVuongBachCot",
  "display_name_vi": "Nữ Vương Bạch Cốt",
  "race_id": "undead",
  "star": 5,
  "species_class": "normal",
  "batch": 1,
  "source_portrait": "apps/game-client/assets/pets/apk84/NuVuongBachCot/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NuVuongBachCot/sprites.png",
  "source_portrait_sha256": "1b140411eec2e7fffefbd73de505b30e0faf8f422d670bebe6dc06fce766f873",
  "source_atlas_sha256": "8a5962de5a03fb48d79c012743553477399bf05aef35e085549f160a51a145a3",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0018",
  "status": "queued"
}
```


### species_0146 — Ma Vương Hút Máu

```json
{
  "species_id": "species_0146",
  "source_species_id": "MaVuongHutMau",
  "display_name_vi": "Ma Vương Hút Máu",
  "race_id": "demon",
  "star": 5,
  "species_class": "special",
  "batch": 1,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaVuongHutMau/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaVuongHutMau/sprites.png",
  "source_portrait_sha256": "99793fc486c18a9fcf98f2b7e1517f2eb644a53d58db836cdfb3dc91a2d6cb37",
  "source_atlas_sha256": "0f4e964eeb3acb47491e59ce381aca687b33fb2539b99395d9039d6f1ff723e9",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0146",
  "status": "queued"
}
```


### species_0039 — Rồng Có Cánh

```json
{
  "species_id": "species_0039",
  "source_species_id": "RongCoCanh",
  "display_name_vi": "Rồng Có Cánh",
  "race_id": "dragon",
  "star": 1,
  "species_class": "normal",
  "batch": 1,
  "source_portrait": "apps/game-client/assets/pets/apk84/RongCoCanh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RongCoCanh/sprites.png",
  "source_portrait_sha256": "5f5af26de29f145e46b7d0ac303e757464795042922b6ac244cfc9a28bec5f15",
  "source_atlas_sha256": "17eed94d7810fb98a11c93084b9b31c70f0d7352aabab1b2d74ea31f9809ba71",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0039",
  "status": "queued"
}
```


### species_0003 — Cua Hắc Ám

```json
{
  "species_id": "species_0003",
  "source_species_id": "CuaHacAm",
  "display_name_vi": "Cua Hắc Ám",
  "race_id": "undead",
  "star": 1,
  "species_class": "normal",
  "batch": 1,
  "source_portrait": "apps/game-client/assets/pets/apk84/CuaHacAm/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/CuaHacAm/sprites.png",
  "source_portrait_sha256": "e14e3ccb6984ec2940b90b7bcc1f6fa5f324b294e3afe487eb9d268679000212",
  "source_atlas_sha256": "d2faac435cdd8d4e1f94764d04a7151735fdb32736415d1048031cb2192b21d2",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0003",
  "status": "queued"
}
```


### species_0030 — Hoa Ăn Thịt Người

```json
{
  "species_id": "species_0030",
  "source_species_id": "HoaAnThitNguoi",
  "display_name_vi": "Hoa Ăn Thịt Người",
  "race_id": "plant",
  "star": 2,
  "species_class": "normal",
  "batch": 1,
  "source_portrait": "apps/game-client/assets/pets/apk84/HoaAnThitNguoi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HoaAnThitNguoi/sprites.png",
  "source_portrait_sha256": "fa0c0f31ebdec0b1bfc234f1c15eef146ae89fc0a8d7462df0a4cf7a43b779a5",
  "source_atlas_sha256": "04ba23d2709d2be5c51ef0788964b6ad721cad163976636f74ed8320c3bf0a97",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0030",
  "status": "queued"
}
```
