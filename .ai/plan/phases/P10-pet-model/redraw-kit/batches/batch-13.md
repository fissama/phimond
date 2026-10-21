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


## Assigned batch 13 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 13
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0061 — Lợn Ác Ma

```json
{
  "species_id": "species_0061",
  "source_species_id": "LonAcMa",
  "display_name_vi": "Lợn Ác Ma",
  "race_id": "demon",
  "star": 2,
  "species_class": "normal",
  "batch": 13,
  "source_portrait": "apps/game-client/assets/pets/apk84/LonAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/LonAcMa/sprites.png",
  "source_portrait_sha256": "caf9733d11e5c9e527d8a64769597fac49e55b9997c17494412e5f8f14287692",
  "source_atlas_sha256": "f83d7d6bae3cdd3e2ebda7aff3d6923d73451246602a5017f3b0d6d57c492d29",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0061",
  "status": "queued"
}
```


### species_0062 — Quái Vật Đầu Dê

```json
{
  "species_id": "species_0062",
  "source_species_id": "QuaiVatDauDe",
  "display_name_vi": "Quái Vật Đầu Dê",
  "race_id": "demon",
  "star": 2,
  "species_class": "normal",
  "batch": 13,
  "source_portrait": "apps/game-client/assets/pets/apk84/QuaiVatDauDe/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/QuaiVatDauDe/sprites.png",
  "source_portrait_sha256": "e93f853fe11ae9bcd2ec0e9549cdf0976a4f9fe05165c00a76d1debe1470b218",
  "source_atlas_sha256": "3a1335c423f7c5860d9b65edca9a2cbdc6ee2777550d1a39489c3b0571249f23",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0062",
  "status": "queued"
}
```


### species_0063 — Ma Tướng Địa Ngục

```json
{
  "species_id": "species_0063",
  "source_species_id": "MaTuongDiaNguc",
  "display_name_vi": "Ma Tướng Địa Ngục",
  "race_id": "demon",
  "star": 3,
  "species_class": "normal",
  "batch": 13,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaTuongDiaNguc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaTuongDiaNguc/sprites.png",
  "source_portrait_sha256": "d7a2f39c28c366ce2cf5524a4c17d3100d3af094c077d684ee11348426abf0b5",
  "source_atlas_sha256": "5b25cc0b72177e32474334de1f7123c36338ad460ce28682c2661941e3ffea80",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0063",
  "status": "queued"
}
```


### species_0064 — Ma Muội

```json
{
  "species_id": "species_0064",
  "source_species_id": "MaMuoi",
  "display_name_vi": "Ma Muội",
  "race_id": "demon",
  "star": 3,
  "species_class": "normal",
  "batch": 13,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaMuoi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaMuoi/sprites.png",
  "source_portrait_sha256": "63c87942203b3c155e72e5d22532557bd838bfd1a8abf24b24b1bad9fa0c872b",
  "source_atlas_sha256": "f8e78ee27b7a50fe77c435a393dbc902048e22279ef7174f52376b564bb39a23",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0064",
  "status": "queued"
}
```


### species_0065 — Thầy Bói Ác Ma

```json
{
  "species_id": "species_0065",
  "source_species_id": "ThayBoiAcMa",
  "display_name_vi": "Thầy Bói Ác Ma",
  "race_id": "demon",
  "star": 3,
  "species_class": "normal",
  "batch": 13,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThayBoiAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThayBoiAcMa/sprites.png",
  "source_portrait_sha256": "66d69c8f94cb23e5aead4e5a12544fb41e87614510ae8bf248866e2a768a4345",
  "source_atlas_sha256": "d09274a5b7e2146b5978d12a9af97458227390b0e9c9b299086147c785291ae6",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0065",
  "status": "queued"
}
```
