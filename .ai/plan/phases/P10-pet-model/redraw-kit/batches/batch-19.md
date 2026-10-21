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


## Assigned batch 19 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 19
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0091 — Chim Chào Mào

```json
{
  "species_id": "species_0091",
  "source_species_id": "ChimChaoMao",
  "display_name_vi": "Chim Chào Mào",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 19,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimChaoMao/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimChaoMao/sprites.png",
  "source_portrait_sha256": "8ef9a3774ccfd35756794ef5571defd34cce1013f65c9bc244a64dfeae5e41c0",
  "source_atlas_sha256": "11b46955a1559b2a68221ebe609fde15aa6b2f51f769b92e8d5e0b02f955452e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0091",
  "status": "queued"
}
```


### species_0092 — Chim Sấm

```json
{
  "species_id": "species_0092",
  "source_species_id": "ChimSam",
  "display_name_vi": "Chim Sấm",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 19,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimSam/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimSam/sprites.png",
  "source_portrait_sha256": "e04a57309bab4be1fccde5a988277c702d5bdc602a80bef608f96eeddabe55ba",
  "source_atlas_sha256": "8b838d0958965e2405276d7e9dd5b8d0cbfee9fb5d386e2e1f05f4c6694d3147",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0092",
  "status": "queued"
}
```


### species_0093 — Ưng Trọc Ma

```json
{
  "species_id": "species_0093",
  "source_species_id": "UngTrocMa",
  "display_name_vi": "Ưng Trọc Ma",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 19,
  "source_portrait": "apps/game-client/assets/pets/apk84/UngTrocMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/UngTrocMa/sprites.png",
  "source_portrait_sha256": "8c4f617dc73db6c5a4a34c3cb294fd3674de5bf7a28c0b867350e0e126ec5e7a",
  "source_atlas_sha256": "e44e325f2e3b2260c1f8621095aeee9919edd9c69f3ff73c9f43c5000d9b1d9a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0093",
  "status": "queued"
}
```


### species_0094 — Chim Cú

```json
{
  "species_id": "species_0094",
  "source_species_id": "ChimCu",
  "display_name_vi": "Chim Cú",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 19,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimCu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimCu/sprites.png",
  "source_portrait_sha256": "6431498d58434012573dde4d3faa4bf7864295fb0069101979399f752434cb74",
  "source_atlas_sha256": "df8411ad98bf1d674f756aecb57978f8c3c20320f0eae25000c21406d301d16f",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0094",
  "status": "queued"
}
```


### species_0095 — Ưng Trọc

```json
{
  "species_id": "species_0095",
  "source_species_id": "UngTroc",
  "display_name_vi": "Ưng Trọc",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 19,
  "source_portrait": "apps/game-client/assets/pets/apk84/UngTroc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/UngTroc/sprites.png",
  "source_portrait_sha256": "abd3bb42cc38b3232b8df7e0342d8ef3e5217d68cd19b9a5cb271ad81c93c9a6",
  "source_atlas_sha256": "f5ad7b89beffe37dee562e5e224f72c2f892afa2f96de0a48ec9131ff1d57808",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0095",
  "status": "queued"
}
```
