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


## Assigned batch 28 — exactly five species

Workspace: `/Users/phileanh/rust/phimond`

Run from workspace root:
```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs --batch 28
```

Image template: `.ai/plan/phases/P10-pet-model/redraw-kit/image-prompt.md`

Repair/review templates and exact tool commands are in the same kit README.

Style anchor: `apps/game-client/assets/pets/redraws/references/DocDangNu/sprites.png` SHA256 `fd3de2a91f6bc3684f29ac9f33bd27e5ed5ab2ca58aa2e648e3261fbacbc31da`

Style anchor: `apps/game-client/assets/pets/redraws/references/DaoThienDuong/sprites.png` SHA256 `043de906f8305b6a1b91ddfaf626b55071b87a43bb612bc70cfdf94d549de3e3`


### species_0136 — Chiến Sĩ Bù Nhìn

```json
{
  "species_id": "species_0136",
  "source_species_id": "ChienSiBuNhin",
  "display_name_vi": "Chiến Sĩ Bù Nhìn",
  "race_id": "spirit",
  "star": 3,
  "species_class": "normal",
  "batch": 28,
  "source_portrait": "apps/game-client/assets/pets/apk84/ChienSiBuNhin/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ChienSiBuNhin/sprites.png",
  "source_portrait_sha256": "de75a9e1ec2adcb3bb77e9b3fa947477ed501846ab0e0bed72996c758ec2ddf5",
  "source_atlas_sha256": "2bc75a5008ccb510848c4fa4708582649c9577984dd7d70c6f0e0dcaf2a0ae1b",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0136",
  "status": "queued"
}
```


### species_0137 — Ma Gương Thủy Tinh

```json
{
  "species_id": "species_0137",
  "source_species_id": "MaGuongThuyTinh",
  "display_name_vi": "Ma Gương Thủy Tinh",
  "race_id": "spirit",
  "star": 4,
  "species_class": "normal",
  "batch": 28,
  "source_portrait": "apps/game-client/assets/pets/apk84/MaGuongThuyTinh/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/MaGuongThuyTinh/sprites.png",
  "source_portrait_sha256": "bbee3a91d36f1ce6c4a0081e07116acb14dd4dfaaad99451424ce0ef31351702",
  "source_atlas_sha256": "f86f746dbccc861c4c242dd7e27b982b8c9a0aa0ed04d394882260956cbfc63b",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0137",
  "status": "queued"
}
```


### species_0138 — Thú Lớn Dung Nham

```json
{
  "species_id": "species_0138",
  "source_species_id": "ThuLonDungNham",
  "display_name_vi": "Thú Lớn Dung Nham",
  "race_id": "spirit",
  "star": 4,
  "species_class": "normal",
  "batch": 28,
  "source_portrait": "apps/game-client/assets/pets/apk84/ThuLonDungNham/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/ThuLonDungNham/sprites.png",
  "source_portrait_sha256": "9e8192a568e66c8497f677aee982ac410749db59261613786bc5168cbad9af7d",
  "source_atlas_sha256": "1ec892a31675fc9dbc78cce74fcbf7de88caab4d8b5bead79b80a01a3ddfc3ee",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0138",
  "status": "queued"
}
```


### species_0139 — Huyền Vũ

```json
{
  "species_id": "species_0139",
  "source_species_id": "HuyenVu",
  "display_name_vi": "Huyền Vũ",
  "race_id": "spirit",
  "star": 4,
  "species_class": "special",
  "batch": 28,
  "source_portrait": "apps/game-client/assets/pets/apk84/HuyenVu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/HuyenVu/sprites.png",
  "source_portrait_sha256": "113903a0c5cd5f8f9372c7d8934eb757045a7d88f5c1b5300e292ca96a71cd6b",
  "source_atlas_sha256": "36658605be8f848465e1add7f157d09390f43921a25c1be3bd8db35a8b1c61e4",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0139",
  "status": "queued"
}
```


### species_0140 — Nhân Sư

```json
{
  "species_id": "species_0140",
  "source_species_id": "NhanSu",
  "display_name_vi": "Nhân Sư",
  "race_id": "spirit",
  "star": 5,
  "species_class": "normal",
  "batch": 28,
  "source_portrait": "apps/game-client/assets/pets/apk84/NhanSu/portrait.png",
  "source_atlas": "apps/game-client/assets/pets/apk84/NhanSu/sprites.png",
  "source_portrait_sha256": "dc8b98f4cd27eee61da1798ba5f31079ebdc4a4ce3fe2936825bc681047c9367",
  "source_atlas_sha256": "adfd3946b06c59bddd09e6fa7baa99f1f0871bb5093d24fd34aec20fa76457fe",
  "output_dir": "apps/game-client/assets/pets/redraws/batches/20261005/species_0140",
  "status": "queued"
}
```
