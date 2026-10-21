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


## Assigned batch 11 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 11
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0051 — Long Vương Hắc Ám

```json
{
  "species_id": "species_0051",
  "source_species_id": "LongVuongHacAm",
  "display_name_vi": "Long Vương Hắc Ám",
  "race_id": "dragon",
  "star": 4,
  "species_class": "normal",
  "batch": 11,
  "source_portrait": "apps/game-client/assets/pets/apk84/LongVuongHacAm/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/LongVuongHacAm/sprites.png",
  "source_portrait_sha256": "cd2b48cefbcd956688701a375d19649d36ee38a3f145f45f204cb4520231937e",
  "source_atlas_sha256": "45a978d290089ca504436097c40d6dd01056ef145a3107b69bae6ce6a0a28648",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0051",
  "status": "queued"
}
```


### species_0052 — Thánh Rồng Thái Cổ

```json
{
  "species_id": "species_0052",
  "source_species_id": "ThanhRongThaiCo",
  "display_name_vi": "Thánh Rồng Thái Cổ",
  "race_id": "dragon",
  "star": 5,
  "species_class": "normal",
  "batch": 11,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThanhRongThaiCo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThanhRongThaiCo/sprites.png",
  "source_portrait_sha256": "fd98a4f050d42e53ba5599c28e44134066686735895ac5a61cad9993a15777c7",
  "source_atlas_sha256": "02dcedb2087c9378a60370fa2b3982db6808c67acb86232bb5449af04318d08e",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0052",
  "status": "queued"
}
```


### species_0053 — Tiểu Ác Ma

```json
{
  "species_id": "species_0053",
  "source_species_id": "TieuAcMa",
  "display_name_vi": "Tiểu Ác Ma",
  "race_id": "demon",
  "star": 1,
  "species_class": "normal",
  "batch": 11,
  "source_portrait": "apps/game-client/assets/pets/apk84/TieuAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/TieuAcMa/sprites.png",
  "source_portrait_sha256": "eeceba190eac82720a2ac79941101efeb9f6ebc4c4ee1842a7953471f4cc2b2e",
  "source_atlas_sha256": "b5c0ed2a0e0356e9a89d498eb1373bd4c6150ee21f18eb8eef8afa27bc85121a",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0053",
  "status": "queued"
}
```


### species_0054 — Yêu Tinh Biển

```json
{
  "species_id": "species_0054",
  "source_species_id": "YeuTinhBien",
  "display_name_vi": "Yêu Tinh Biển",
  "race_id": "demon",
  "star": 1,
  "species_class": "normal",
  "batch": 11,
  "source_portrait": "apps/game-client/assets/pets/apk84/YeuTinhBien/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/YeuTinhBien/sprites.png",
  "source_portrait_sha256": "4717736613879d81781dc6f74ba093e6a77e9bd031c8be45d045ccb35c21e6c1",
  "source_atlas_sha256": "70016863ce9cd5869a35f420eb4e68f32f8e954ff1e15b3242778fc410300995",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0054",
  "status": "queued"
}
```


### species_0055 — Mắt Ác Ma

```json
{
  "species_id": "species_0055",
  "source_species_id": "MatAcMa",
  "display_name_vi": "Mắt Ác Ma",
  "race_id": "demon",
  "star": 1,
  "species_class": "normal",
  "batch": 11,
  "source_portrait": "apps/game-client/assets/pets/apk84/MatAcMa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MatAcMa/sprites.png",
  "source_portrait_sha256": "5899888b96b8d6a23532c573e71db9b8739e38ebec3839a9ac39d0b958c91444",
  "source_atlas_sha256": "9de7543bbc628d2c3b26b97b18cc36382f1912fa1ae23ae5369303912d855cfc",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0055",
  "status": "queued"
}
```
