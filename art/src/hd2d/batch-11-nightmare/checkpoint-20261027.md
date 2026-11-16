# Nightmare art checkpoint — 2026-10-27

Scope: batch-11-nightmare art only; no runtime/scene edits, no commits, no approval claims. Manifest remains `approved: false`. Built-in Codex image generation only. Fresh contact sheet: 62 records, `contact-sheet.png` (1280×12400), rebuilt after edits and opened for review.

## Added or advanced this session

- Generated/native-packaged four campfire frames at 192×192; assembled `nightmare-campfire/frames.png` and `preview.gif`. Full 4× dark/checker frames inspected. Frame 01 contains two detached ember pixels; base registration is not pixel-verified.
- Generated and inspected four arrival rune frames; centered consistently, phase 02 adds pale satellites, temporal smoothness not certified. Assembled `nightmare-marker-arrival/frames.png` and `preview.gif`.
- Generated three FX assets, remapped to the existing nightmare crystal palette, then inspected full 4× dark/checker.
- Generated retry-02 mid/near backdrops; full 4× inspected, horizontal seam mechanically passes; transparent margins/large blank sky are intentional.
- Generated retry-02 decals 11/12; full 4× inspected. Rust chain links and dead leaves/twigs now read clearly; previous bad exports remain preserved in earlier job raws.
- Corrected and inspected portal pair at full 4× dark/checker; common silhouette uses intersection of the two generated masks, with no repaint.
- Inspected floor extras 04/05 and shadows 01–04; floors are visually sparse and need map-repeat review, shadows are faint.
- Generated final far island/moon backdrops; full 4× inspected, but both remain gradient and fail seam audit.

## Known failures / blockers

- `nightmare-campfire-frame-01`: mechanical=pass; status=needs_claude_visual_review; review=actual_complete_4x_dark_and_checker_viewed
- `nightmare-backdrop-far`: mechanical=fail; status=retry_exhausted_seam_failure; review=actual_complete_4x_dark_and_checker_viewed
- `nightmare-backdrop-far-02`: mechanical=fail; status=retry_exhausted_seam_failure; review=actual_complete_4x_dark_and_checker_viewed

- Wisp-lantern frame set: all three attempts exceeded its predeclared native pixel budget; no valid export.
- Core floor set and edge strips still fail tile seam/edge validation. Image attempt budgets are exhausted for these identities; do not report accepted.
- Decal 11/12 earlier rejected outputs are superseded by inspected retry-02 finals; no approval implied.
- Soft shadows are faint at normal scale.
- Primary animation metadata stays in per-animation `animation.json`; strips are assembly previews only, keeping manifest color audit per-frame.

## Validation

- `sh tools/check_hd2d_art.sh` (with bundled Python runtime on PATH): exit 0; Art gate scanned desert/nightmare/tomb/windrock, 229 assets, 0 errors, 0 warnings.
- Do not interpret the overall multi-kit audit as approval; owner/Claude approval remains false.
- `git status` was already dirty before this art work; unrelated work was preserved. No commit/push performed.


## Continuation after checkpoint

- Added optional map-specific `nightmare_island_survivor_camp-landmark-02`: collapsed mossy stone offering plinth. Image attempt 01 oversize preserved; attempt 02 packaged from generated alpha at 372×222 native pixels onto 400×256 canvas with no resampling. 48 colors, binary alpha, 14px margin; viewed full 4× dark/checker. Mechanical QA passes; warm highlights need owner review.
- Corrected Drawn checklist marks for props 04–06 and 11–12 after confirming their existing 4× reviews; added camp landmark-02. All Duyệt remain unchecked. Manifest remains approved=false.
- Art gate was invoked for batch-11-nightmare; command returned no terminal output under RTK wrapper.
- This addition does not resolve exhausted floor, edge, far backdrop, or wisp blockers. Kit remains incomplete.


## 2026-10-28 continuation

- Edge redraw retry 32 was generated from approved terrain/map-style references and inspected at source size. The model returned one continuous soil band with raised, high-detail rock clumps and abrupt endpoints instead of three detached shallow overlays. Rejected; raw, prompt, source hashes, and review are retained at `jobs/edges-repair-32/`. Nothing was selected and the checklist remains unchanged.
- Re-ran `tools/hd2d_audit/art_gate.py batch-11-nightmare` with the bundled workspace Python runtime: **289 assets, 0 errors, 0 warnings** across the gate's five configured kits. This confirms only current mechanical checks; rejected drafts and owner review state are unaffected.
- The previous manual shell run lacked Pillow/NumPy; the bundled Python path resolves this without modifying project tooling.


### 2026-10-28 — Wisp frames and floor retry 22

- Added `nightmare-wisp-lantern` animation from retry 27. Four 192×256 native frames, 48 colors, binary alpha, 30px margin, no QA failures; shared palette, 4× dark/checker review completed, preview strip/GIF assembled. `nightmare-prop-14` marked Vẽ; owner approval remains unchecked.
- Replaced prior wisp blocker in this checkpoint: retry 27 is the selected art; prior retry 25/26 remain rejected in their job folders.
- Generated six floor materials in retries 22 raw-01/raw-02. Both rejected; outer 8px bands are not uniform and opposing edges are not identical (raw-02 worst measured x/y delta 54 RGB). No floor final was selected; six floor checklist rows remain open.
- Latest art gate before floor changes: 293 assets across five kits, 0 errors/0 warnings. The six floor QA failures remain explicit in manifest: `SEAM_X_NONZERO`, `SEAM_Y_NONZERO`, `OUTER8_NOT_FLAT`.


### 2026-10-28 — Floor 01 visual review; floor 02 retry 23 rejected

- Reviewed `nightmare-floor-01/final.png`, full 4× dark/checker views, and `repeat-3x3.png`. Repeat reads continuously with no visible joins; QA reports 44 colors, binary alpha, X/Y seam max 0, uniform outer 8 px. Marked Vẽ in `kit-nightmare.md`; Duyệt remains unchecked. QA/manifest self-review fields updated.
- Built-in image_gen retry 23 produced two single-tile candidates. Both rejected before packaging: raw-01 has medium/large uneven clumps and nonuniform perimeter; raw-02 has smooth gradient/vignette and uneven edge band. Both unchanged raws and prompts are preserved at `jobs/floors-repair-23/`; no selected final changed.
- Rebuilt and viewed contact sheet: 67 assets, 1280×13600. Bundled-Python art gate exit 0: 293 assets across five configured kits, 0 errors, 0 warnings (`/tmp/nightmare-gate-20261028.log`). This does not resolve Nightmare blockers; floor 02/03/extras 01–03, edges, far backdrops remain mechanically failed or incomplete.


### 2026-10-28 — Floor texture retry 24 rejected

- Generated a six-material sheet with the required map/style/pet references and measured all six cropped cells. All failed repeatability: maximum opposing-edge differences X/Y were 68/131, 123/182, 72/172, 93/208, 125/168, and 63/194 RGB; outer 8 px rings contained 3,472–4,687 colors each.
- A single-tile follow-up produced a visible vignette; although opposing edge deltas were only 4 RGB, the perimeter was not flat (68 ring colors), and the surface remained gradient-heavy. Both raws preserved in `jobs/floors-repair-24/`; neither was packaged. Floor 02/03 and extra 01–03 stay open.
- Floor retry 24 raw-03 was an image edit of raw-02 asking for flat base and exact solid perimeter. Rejected after visual inspection: smooth vignetting and sparse isolated chips remain. Raw kept; no spatial post-edit applied.


### 2026-10-28 — Nightmare edge retry 33 rejected

- Generated two new edge candidates with required map, approved edge-style and pet-anchor references. Raw-01 rendered raised 3D-looking stones/bricks. Raw-02 still has a smooth color gradient and highlighted raised rocks in a thick strip. Both rejected before cropping/keying; raws and source hashes retained in `jobs/edges-repair-33/`. No edge final or checklist mark changed.


### 2026-10-28 — Nightmare floors 02/03 and extras 01–03 selected

- Revisited floor sheet from retry 22. Cropped five distinct material cells and applied non-dithered 48-color finishing; global palette-only remaps merged each tile’s 3–4 perimeter colors to its dominant base. No spatial repaint or edge fill.
- All five finals passed mechanical QA: `nightmare-floor-02` 45 colors, `nightmare-floor-03` 44, extras 01–03 each 45; binary alpha; X/Y seam maxima 0; uniform outer 8 px; no key residue. Pairwise normalized cross-correlation against the other Nightmare floor textures is below 0.08 (gate threshold 0.9).
- Viewed every final at 4× on dark/checker backgrounds and each 3×3 repeat. Marked Vẽ for floor-02/03 and extras-01/02/03; Duyệt remains blank. Previous finals/QA preserved with `before-floors-repair-26` suffixes; source sheet remains unchanged in `jobs/floors-repair-22/`; packaging/remap provenance in `jobs/floors-repair-26/`.
- Rebuilt and viewed fresh contact sheet (67 assets, 1280×13600). Latest art gate: exit 0, **293 assets, 0 errors, 0 warnings** across five configured kits. Remaining Nightmare blockers are the three edge visuals/seams and two far-backdrop gradient/seams.


## 2026-10-28 — retries 27 and 34 rejected

- Far backdrop retry 27 plus one edit still has smooth sky gradients and nonmatching horizontal boundaries (max raw RGB deltas 41 and 54). Both raws/prompts and ref hashes are preserved in `jobs/backdrop-repair-27/`; no candidate selected.
- Edge retry 34 is a thick, over-detailed raised root/rock wall, with partial alpha throughout and horizontal boundary delta max 127 RGB. Raw/prompt/review preserved in `jobs/edges-repair-34/`; no candidate selected.
- Nightmare remains incomplete. No checklist marks changed; all Duyệt remain blank.
- Edge retry 34 prompt 02 is visually flatter but remains too textured; crop-only seam search had best max 47 RGB, so no asset promoted. Both attempt raws and exact source hashes are recorded in its prompt.
- A global palette-only experiment on the two failed far backdrops forced seam max 0 only by collapsing the full plates to 10 and 4 RGB colors; rejected below the 33-color minimum. See `jobs/backdrop-repair-28/review.md`.
- Checklist Vẽ is now unchecked for the three edge failures and two far-backdrop failures. Latest gate: 293 assets, 0 errors, 0 warnings; these are still visual blockers.
- Retry 34 raw-03 is rejected: crop scan found no exact seam (best tested source delta max 9; full boundary max 102), with thick textured fringe and partial alpha. See job prompt/review.
- Retry 29 far backdrop plus allowed global palette finish is rejected: unchanged plate seam max 9; sky-flattened candidate has 19 colors and seam max 22. No manifest promotion.

### 2026-10-29 — edge-01 selected

- `nightmare-edge-01` now uses an image_gen-generated moss fringe crop from `jobs/edges-repair-35/raw-01.png`, crop `[1104,260,1584,380]`, nearest scale, binary alpha, nondithered palette finish. It passes 48 colors, raw integrity, key residue 0 and seam X max 0.
- Full 4x dark/checker, detail, 3x repeat, and compositions over Nightmare floor-01/02 were viewed. Vẽ marked; Duyệt remains unchecked. Manifest remains `approved:false`.
- Edge-02/03 and the two far backdrops still fail; Nightmare remains open.
