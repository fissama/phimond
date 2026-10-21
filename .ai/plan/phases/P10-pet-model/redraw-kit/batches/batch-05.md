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


## Assigned batch 05 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 5
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0017 — Rồng Xương Băng

```json
{
  "species_id": "species_0017",
  "source_species_id": "RongXuongBang",
  "display_name_vi": "Rồng Xương Băng",
  "race_id": "undead",
  "star": 5,
  "species_class": "normal",
  "batch": 5,
  "source_portrait": "apps/game-client/assets/pets/apk84/RongXuongBang/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/RongXuongBang/sprites.png",
  "source_portrait_sha256": "c557d0c6694d8075bf7a60e8188b87d6bb649f4efe17b0ad7d2647a3bd03092b",
  "source_atlas_sha256": "1967803d565aa716d812c74b4d19b75bf073561ad5437a15d2a8f75622b5f9a1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0017",
  "status": "queued"
}
```


### species_0019 — Nữ Đế Minh Giới

```json
{
  "species_id": "species_0019",
  "source_species_id": "NuDeMinhGioi",
  "display_name_vi": "Nữ Đế Minh Giới",
  "race_id": "undead",
  "star": 5,
  "species_class": "special",
  "batch": 5,
  "source_portrait": "apps/game-client/assets/pets/apk84/NuDeMinhGioi/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NuDeMinhGioi/sprites.png",
  "source_portrait_sha256": "4ad3263ddd75e6cb7fb9895a7734b0b910cba9a63ad89d9b696a6f8409deffe5",
  "source_atlas_sha256": "d2ba4d242d36c077eeb7dfbe28d7e4ace42ce2f15e69a976e6fb5720d5ffa0e1",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0019",
  "status": "queued"
}
```


### species_0020 — Thủ Lĩnh Hắc Ám

```json
{
  "species_id": "species_0020",
  "source_species_id": "ThuLinhHacAm",
  "display_name_vi": "Thủ Lĩnh Hắc Ám",
  "race_id": "undead",
  "star": 5,
  "species_class": "special",
  "batch": 5,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuLinhHacAm/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuLinhHacAm/sprites.png",
  "source_portrait_sha256": "c751c9a2563bb73d888b13df620763509735f53082d52ff2531591c83004ee66",
  "source_atlas_sha256": "38505d382ea269deae0b6f96c14161a4367470e1cd9f708aeca84c0ff1913d4f",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0020",
  "status": "queued"
}
```


### species_0021 — Xương Rồng

```json
{
  "species_id": "species_0021",
  "source_species_id": "XuongRong",
  "display_name_vi": "Xương Rồng",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 5,
  "source_portrait": "apps/game-client/assets/pets/apk84/XuongRong/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/XuongRong/sprites.png",
  "source_portrait_sha256": "88abb91e9b91a619066799c65ba3c5e6c572980d0652cbd738519d0d00a9750d",
  "source_atlas_sha256": "b30698fd845c30d0da7f0fa101e819b7a030d76c5cf5198f03541355b785e65c",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0021",
  "status": "queued"
}
```


### species_0022 — Yêu Tinh Hoa

```json
{
  "species_id": "species_0022",
  "source_species_id": "YeuTinhHoa",
  "display_name_vi": "Yêu Tinh Hoa",
  "race_id": "plant",
  "star": 1,
  "species_class": "normal",
  "batch": 5,
  "source_portrait": "apps/game-client/assets/pets/apk84/YeuTinhHoa/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/YeuTinhHoa/sprites.png",
  "source_portrait_sha256": "f54601a382ed864e5c210c852a288a11a7fb25d32cfe79bffd9ef11f7d1ae52a",
  "source_atlas_sha256": "21cc3ff808328d88e3e59ed7afee4c85c38e041c0c2e7ce39079ec5e292fe515",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0022",
  "status": "queued"
}
```
