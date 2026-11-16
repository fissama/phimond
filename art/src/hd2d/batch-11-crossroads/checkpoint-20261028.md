# Crossroads art checkpoint — 2026-10-28

Scope: `batch-11-crossroads` map art only. Built-in Codex image generation; no runtime/scene edits, commits, or owner approval. Manifest remains `approved: false`; Duyệt remains unchecked.

## Completed this continuation

- Added `crossroads-portal-dormant` and `crossroads-portal-active` from the selected paired image-generation sheet. Both preserve native pixel dimensions with transparent padding only, 48 colors, binary alpha, zero chroma residue, and exact shared alpha mask. Both finals were viewed at 4× over dark and checker backgrounds. Earlier portal raw attempt and selected raw are retained byte-identically under `jobs/portal-pair/`.
- Added the four-frame `crossroads-marker-arrival` loop as `crossroads-marker-arrival-frame-00..03`. Registered each frame by translation only onto a shared 288×256 canvas, no resampling. 48 colors each, binary alpha, zero chroma residue. All four frames viewed at 4× over dark and checker backgrounds; frame 03 returns to the same dim pose as frame 00. Animation preview and metadata are in `crossroads-marker-arrival/`.
- Earlier contact sheet had 46 manifest assets. The latest sheet now has 53 assets, is newer than the manifest, and was viewed after the floor updates. Checklist Vẽ is checked for floors 01–05, all three extra floors, both portal states, and the arrival marker; Duyệt remains unchecked.
- Latest art gate scanned 283 assets across the batch-11 kits and reported 0 errors, 0 warnings. The three original floor seam failures were cleared through global palette remapping: floor 01 39 colors, floor 02 39, floor 03 38; each has exact X/Y seams, uniform outer 8px, binary alpha, zero key residue, and raw integrity true.

## Still incomplete

- All eight Crossroads floor textures (floors 01–05 plus extras 01–03) now pass package QA; the maximum pairwise grayscale correlation is 0.332. A first extra-01 candidate was rejected for noisy fine sediment and preserved; replacement uses larger calm clusters. Floor-04's static water base is packaged, but its requested 4-frame foam overlay still needs a separate animation asset.
- Three edge strips and the mid/near backdrops remain to be made. Far backdrop 01–02 are drafts with package seam failures and remain unchecked/blocked.
- Shared decals 01–12, shadows 01–04, and FX 01–03 are packaged; 17 props are packaged.
- Dedicated Map 02 crate landmark is packaged; Map 01 reuses kit props. Other map placements, NPC anchors, and scene assembly remain. This checkpoint does not claim the kit or maps complete.

## Resume

Continue with Crossroads only. Preserve all raw attempts, rebuild and view the contact sheet after manifest edits, run `tools/hd2d_audit/art_gate.py batch-11-crossroads`, and keep the manifest `approved: false`. Next: generate the 4-frame shallow-water foam overlay, edge strips 01–03, and mid/near backdrops; then review map-specific landmark coverage and update checkpoint before starting the next kit.

## Rejected floor-water attempts

- Three image-generation attempts are preserved under `jobs/floor-water/`. Attempt 01 read as stone/cobble; attempt 02 read as water but returned 1254×1254 and cannot be downsampled to native 512 without violating the pixel-size rule; attempt 03 provided a 512×512 water tile but failed seam QA (X mean 11.678, Y mean 23.848) and visibly repeats with grid seams. No floor asset was added to the manifest and checklist remains unchecked.

## Edge strip attempts and Map 01 landmark review

- Two edge sheets are retained under `jobs/edges-01-03/`; both failed repeat-end QA and remain un-packaged. The second has three strip candidates with RGB edge means 16.17, 26.90, 31.39 and unequal left/right 8px regions.
- Re-reviewed the Map 01 reference. Its rear stalactite/stalagmite columns are covered by shared kit props 01–07 and 15; the crate pile is already represented by Map 02's crate landmark. Updated both Map 01 landmark rows to reuse notes; no duplicate landmark asset is needed.

## Far backdrop attempt

- Two built-in image_gen versions are preserved under `jobs/backdrop-far-01/`. The first misses the pixel-art finish; the second remains too smooth and cannot produce a seamless 1280×384 unscaled crop (best raw seam mean 5.872; 48-color nearest-palette check 5.978 mean, max 57). No backdrop was added to the manifest.
- Current unchecked shared-kit rows: floors 01–05, far backdrop 01–02, floor extras 01–03, edges 01–03, and backdrop far/mid/near. Existing floor 01–03 are present but remain unchecked because of seam failures.

## Floor water attempt 02 — rejected

- A new built-in image_gen attempt reads clearly as shallow cave water but returned 1254×1254 instead of native 512×512. Resizing is disallowed by the pixel-size rule, so it was not packaged and the checklist remains unchecked.
- Raw SHA256: `390e97c239cc6532c87b1d2801cdc5c16c46dfab85ff5ff9797b13da44f7813e`. Exploratory seam differences on the full image: X mean/max 10.6499/94; Y mean/max 7.0255/76. It fails the tile contract regardless of size.
- Raw and rejection details are retained under `jobs/floor-water-04/`.
- Two additional sheet-based variants were tested. Attempt 03 had X/Y seam means 21.3743/25.4453 and 1,810 colors across the outer 8px border. Attempt 04 edit improved X to 12.0951 but Y remained 27.0905, with 1,633 outer-border colors. Both visibly repeat with grid boundaries; neither is packaged.
- A first mid-backdrop sheet attempt is preserved in `jobs/backdrop-mid-01-raw.png`. It reads as a cave wall but has 73,974 colors and a tested 1280×384 crop seam mean/max 149.75/249. Rejected for pixel finish and repeat mismatch; no manifest entry was added.
- Two further shallow-water edits were rejected: attempt 05 still has X/Y seam means 11.5384/23.2454; attempt 06 returned 1254×1254 and 36,808 colors. Their raw files and hashes are recorded in `jobs/floor-water-04/`; no floor was packaged.
- Edge attempt 03 is preserved under `jobs/edges-01-03/raw-03.png` (SHA256 `021693a73f910358be60c6499cb4f33831bb07f2f3093c774fa0e08475a9b4a4`). A candidate 512×128 crop has 43,108 colors and X seam mean/max 29.6172/177; rejected, checklist unchanged.
- Packaged `crossroads-backdrop-far-02` as a draft from a native 1280×384 crop, quantized to 48 colors, raw integrity true, and viewed at 4× on dark/checker backgrounds. Its own QA flags `SEAM_X_NONZERO` (mean 3.8220, max 50); kept in manifest as `mechanical_status: blocked`, `approved:false`, and Vẽ remains unchecked. Contact sheet was rebuilt after manifest review metadata changed, re-viewed, and art gate then reported only the three existing floor errors.
- Packaged `crossroads-backdrop-far-01` as a second native 1280×384, 48-color draft; raw integrity true, 4× dark/checker review complete. Package QA flags `SEAM_X_NONZERO` (mean 3.1884, max 45); manifest keeps it `mechanical_status: blocked`, `approved:false`, Vẽ unchecked. Rebuilt and viewed the 48-asset contact sheet. Latest art gate: 278 assets, 3 errors, 0 warnings; only the three existing floor seam errors remain.
- Generated three floor-05 cave-bottom candidates. Best X seam mean was 8.2585, but its Y seam worsened to 27.8314 and the outer 8px border still contains 1,223 colors. All raw sheets are retained under `jobs/floor-05-new/`; none was packaged or checked on the map checklist.
- A third floor-01 repair edit is preserved in `jobs/floor-repair-01/raw-03.png`; X seam mean/max 1.0482/11, Y 38.7155/54, outer8 412 colors. Rejected; the existing selected floor remains unchanged and its QA records the attempt.
- Packaged floor-05 from candidate raw 02. Initial 48-color median-cut QA failed seams/border; applying an allowed global remap of the eight near-identical outer-border palette colors made the final 41-color tile exact-seam and flat-border. Raw stayed byte-identical; no spatial painting was used. Re-viewed final at 4× on dark/checker and the 3×3 repeat; checklist Vẽ checked, Duyệt empty, manifest `approved:false`. Contact sheet and art gate are being refreshed.


## Continuation update — 2026-10-28 (foam animation + backdrop retries)

- Added the four-frame shallow-water foam animation `crossroads-water-foam` from built-in image_gen. Raw sheet and prompt are preserved in `jobs/water-foam-04/`; source was 1254×1254, split into four exact 627×627 quadrants without resizing. Finish: binary alpha threshold (128), nondithered ≤48-color palette, translation-only registration to a shared centroid; no spatial painting. All four frames were viewed at 4× over dark and checker backgrounds. Metadata: `crossroads-water-foam/animation.json`; manifest remains `approved:false`, status awaits owner review.
- The first three foam sheets remain rejected under `jobs/water-foam-attempts/`.
- Rechecked far backdrop seam repair through global palette remap; rejected because edge-color equivalence clusters would alter visible colors too much. Imagegen attempts 07–09 are retained at `jobs/backdrop-far-07..09/`; best crop seams still fail (attempt 07 mean 6.603/max 38; attempt 08 mean 3.189/max 67; edited attempt 09 mean 4.028/max 43). Neither existing far backdrop draft was replaced or checked.
- Contact sheet now contains 57 manifest assets and was rebuilt/reviewed. Art gate: 287 assets across batch-11 kits, 0 errors, 0 warnings.
- Remaining Crossroads art blockers: far backdrops 01–02 (both seam-failing drafts), three edge strips, and mid/near backdrops. No map scene placement/collision work is in this art-only scope.


## Edge-strip retries — 2026-10-28

- Edge attempt 04 (`jobs/edges-04/`) produced a strong moss-to-wet-stone transition but no useful exact-seam crop: the only zero-seam crop was mostly transparent; the best visible-band crop did not repeat at its ends. Rejected, not packaged.
- Edge attempt 05 (`jobs/edges-05/`) produced a stone-to-water strip; seam search found no acceptable native crop (best overall crop selected water only; crops containing the actual shoreline retain endpoint mismatch). Rejected, not packaged.
- Edge checklist rows remain unchecked; manifest and contact sheet were not changed for these two attempts.


## Far backdrop 01 replaced — 2026-10-28

- Replaced the seam-failing `crossroads-backdrop-far-01` draft with attempt 10 from `jobs/backdrop-far-10-final/`. Final is native 1280×384, 36 colors, exact horizontal seam (mean/max 0/0), raw integrity true. A 56-color nondithered palette followed by a global remap of near-identical edge colors yields the exact seam; 4× dark/checker and 3× repeat were visually reviewed. Checklist Vẽ is now checked; Duyệt remains unchecked.
- `crossroads-backdrop-far-02` remains blocked.


## Far backdrop 02 replaced — 2026-10-28

- Replaced the seam-failing `crossroads-backdrop-far-02` draft with attempt 11 from `jobs/backdrop-far-11-final/`. Native 1280×384, 37 colors, exact horizontal seam (mean/max 0/0), raw integrity true. Global palette remap joins near-identical seam colors; no spatial painting. Final 4× dark/checker and 3× repeat reviewed. Checklist Vẽ is checked; Duyệt remains unchecked.
- Both far backdrops now pass mechanical and visual self-review. The remaining three edge strips and mid/near backdrops are still unchecked.


## Mid backdrop delivered — 2026-10-28

- `crossroads-backdrop-mid` packaged from attempt 03 in `jobs/backdrop-mid-03-final/`: 1280×384, 42 colors, exact horizontal seam (mean/max 0/0), raw integrity true. Final 4× dark/checker and 3× repeat reviewed. Checklist Vẽ is checked; Duyệt remains unchecked.
- Earlier attempt 02 (`jobs/backdrop-mid-02/`) was retained and rejected because global seam remapping would merge dissimilar colors (max cluster diameter 67 RGB).
- Remaining Crossroads art blockers: three edge strips and the near backdrop.


## Near backdrop delivered — 2026-10-28

- `crossroads-backdrop-near` packaged from `jobs/backdrop-near-01-final/`: native 1280×384, 34 colors, exact horizontal seam (mean/max 0/0), raw integrity true. Global remap joins near-identical palette colors (raw seam max 5 RGB). Final 4× dark/checker and 3× repeat reviewed. Checklist Vẽ is checked; Duyệt remains unchecked.
- All five backdrop rows are now packaged and visually self-reviewed. Remaining unchecked shared-kit rows are edge strips 01–03.
