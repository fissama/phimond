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


## Assigned batch 18 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 18
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0086 — Gấu Trúc Ma Pháp

```json
{
  "species_id": "species_0086",
  "source_species_id": "GauTrucMaPhap",
  "display_name_vi": "Gấu Trúc Ma Pháp",
  "race_id": "beast",
  "star": 4,
  "species_class": "normal",
  "batch": 18,
  "source_portrait": "apps/game-client/assets/pets/apk84/GauTrucMaPhap/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/GauTrucMaPhap/sprites.png",
  "source_portrait_sha256": "619a66cdbde9bb235d2ee23803e403dea3816490eed0030cdb987de52e244e8f",
  "source_atlas_sha256": "20522510e906e452cba0f86880fde24cb9e42b5af925f2821fb2893f647084f8",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0086",
  "status": "queued"
}
```


### species_0087 — Bạch Hổ

```json
{
  "species_id": "species_0087",
  "source_species_id": "BachHo",
  "display_name_vi": "Bạch Hổ",
  "race_id": "beast",
  "star": 4,
  "species_class": "special",
  "batch": 18,
  "source_portrait": "apps/game-client/assets/pets/apk84/BachHo/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/BachHo/sprites.png",
  "source_portrait_sha256": "404bf68c163e729736e0af89ba75040abf5eb53a94e61f2b1a6b0c9158272e0d",
  "source_atlas_sha256": "6fed953e47e3f8bafcadfc569fabf0a3ccf19b2f97049f711a15aee4f7cdea98",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0087",
  "status": "queued"
}
```


### species_0088 — Sói Xích Viêm

```json
{
  "species_id": "species_0088",
  "source_species_id": "SoiXichViem",
  "display_name_vi": "Sói Xích Viêm",
  "race_id": "beast",
  "star": 5,
  "species_class": "normal",
  "batch": 18,
  "source_portrait": "apps/game-client/assets/pets/apk84/SoiXichViem/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/SoiXichViem/sprites.png",
  "source_portrait_sha256": "f0cc7e68ba162477c92d8170974de282f7678324e803d3d39b5970b002c7601e",
  "source_atlas_sha256": "e371915519435bb48d2e3d4c747ab10ed4ab06716d553a19e7976a87c78ef2a1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0088",
  "status": "queued"
}
```


### species_0089 — Chim Ong

```json
{
  "species_id": "species_0089",
  "source_species_id": "ChimOng",
  "display_name_vi": "Chim Ong",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 18,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChimOng/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChimOng/sprites.png",
  "source_portrait_sha256": "f8af8d63eb49d37d8f9c4384a1efaedd32ed7418e2e6e01764e149380aceb403",
  "source_atlas_sha256": "05104433b80473500803d44c9ffefaba5972919e8ce06e7763eed5eaca95b30d",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0089",
  "status": "queued"
}
```


### species_0090 — Dơi

```json
{
  "species_id": "species_0090",
  "source_species_id": "Doi",
  "display_name_vi": "Dơi",
  "race_id": "bird",
  "star": 1,
  "species_class": "normal",
  "batch": 18,
  "source_portrait": "apps/game-client/assets/pets/apk84/Doi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/Doi/sprites.png",
  "source_portrait_sha256": "77ba071846c739e94b8d913fbf647b7c28c74e6e3d761a982d5e6e831f761aeb",
  "source_atlas_sha256": "99dfeb27a0971c0dff8a8148a5b2e66a705a5b736db08f10b63f72594b0bb5ba",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0090",
  "status": "queued"
}
```
