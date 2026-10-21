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


## Assigned batch 14 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 14
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0066 — Đại Ác Ma

```json
{
  "species_id": "species_0066",
  "source_species_id": "DaiAcMa",
  "display_name_vi": "Đại Ác Ma",
  "race_id": "demon",
  "star": 4,
  "species_class": "normal",
  "batch": 14,
  "source_portrait": "apps/game-client/assets/pets/apk84/DaiAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/DaiAcMa/sprites.png",
  "source_portrait_sha256": "21167ed2b5acf0107f50f2d233f59c21176408e230b04c1408c558128415380f",
  "source_atlas_sha256": "d0694e37afb5812aff0b2b715058445a3d6857eb06beb7e1e83710e6a1a3946e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0066",
  "status": "queued"
}
```


### species_0067 — Ma Vương Địa Ngục

```json
{
  "species_id": "species_0067",
  "source_species_id": "MaVuongDiaNguc",
  "display_name_vi": "Ma Vương Địa Ngục",
  "race_id": "demon",
  "star": 4,
  "species_class": "normal",
  "batch": 14,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaVuongDiaNguc/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaVuongDiaNguc/sprites.png",
  "source_portrait_sha256": "362ac11c32675a8e3a712734bca113df3e460dc72555c3748f6239e01f60fe59",
  "source_atlas_sha256": "8633abfe7ef757e0367778d0ec4f9e06a37781f20100d0aec94615bce57a347c",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0067",
  "status": "queued"
}
```


### species_0068 — Thanh Long

```json
{
  "species_id": "species_0068",
  "source_species_id": "ThanhLong",
  "display_name_vi": "Thanh Long",
  "race_id": "demon",
  "star": 4,
  "species_class": "special",
  "batch": 14,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThanhLong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThanhLong/sprites.png",
  "source_portrait_sha256": "5d80eb1719371404f7f61eeb2591a35c52f65721ed28f52f532625050c405f48",
  "source_atlas_sha256": "0af7badccf5ad96e6554d7dfd7b4de238dcfe108f8c716ce41897a79e9d5f7c5",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0068",
  "status": "queued"
}
```


### species_0069 — Trụy Thiên Sứ

```json
{
  "species_id": "species_0069",
  "source_species_id": "TruyThienSu",
  "display_name_vi": "Trụy Thiên Sứ",
  "race_id": "demon",
  "star": 5,
  "species_class": "normal",
  "batch": 14,
  "source_portrait": "apps/game-client/assets/pets/apk84/TruyThienSu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TruyThienSu/sprites.png",
  "source_portrait_sha256": "a4afe350c368f97b9bf54dab9fca6bb26485ec2a604c38410e9d8f5295163df7",
  "source_atlas_sha256": "3144b4deac1f4432a80621a2f9f96bbe81b672be1063c16592e4b23bc8b24c2b",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0069",
  "status": "queued"
}
```


### species_0070 — Thú Móng Lớn

```json
{
  "species_id": "species_0070",
  "source_species_id": "ThuMongLon",
  "display_name_vi": "Thú Móng Lớn",
  "race_id": "beast",
  "star": 1,
  "species_class": "normal",
  "batch": 14,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuMongLon/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuMongLon/sprites.png",
  "source_portrait_sha256": "d74db643afeda977d94ec4535ad61bbdee304543c161b5ede9cb924b9d7fe615",
  "source_atlas_sha256": "9eb8182548c7a020095360d9abd72a8a9f53ecf79b8ca839398d1710c6292e9d",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0070",
  "status": "queued"
}
```
