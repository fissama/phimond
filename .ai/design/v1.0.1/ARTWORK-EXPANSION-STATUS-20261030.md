# Artwork expansion status — 2026-10-30

Purpose: track the newly requested art against existing files so we finish real gaps without regenerating approved work. Do not mark an item done merely because a draft or raw PNG exists. Final delivery requires expected dimensions, alpha/color/edge QA, visual review, and any required owner approval.

## Priority 1 — movement strips S23–S24

- Required: 6 player strips (male/female × side/down/up) plus 18 walker strips (baker/elder/boy/girl/guard/traveller × side/down/up). Horizontal movement can be mirrored by the renderer for the opposite lateral direction.
- Existing `player-male.run.png` is a potential anchor: Codex manually verified opposite lead legs in frames 1 and 5 and stable 166–168 px body height, but owner approval is still pending. Other player/NPC sheets remain unapproved until individual gait and frame-height checks pass; `walker-elder.run` and `walker-traveller.run` visibly repeat the same lead leg in frames 1 and 5.
- Codex image_gen S23 male horizontal attempts 03 and 04 are rejected: the first repeats a four-pose cycle; the localized frame-5 edit did not reverse the leading leg and introduced red/magenta edge pixels. Evidence: `art/src/hd2d/octopath-s01-s27-20261029/rejected/host-image-male-run-attempt-03/` and `.../attempt-04/`.
- Status: **0/24 owner-approved**. S24 remains gated on owner approval of the male horizontal candidate as its style anchor. Current capability evidence in `forge-doctor-20261030-current.json` confirms there is no video route configured; the built-in image tool has repeatedly returned unsuitable sprite-sheet dimensions/alpha and cannot replace the required image-to-video route.

## Priority 2 — UI group 3 N01–N09

- Exact-target candidates `hud-player-plate.png`, `hud-pet-main.png`, and `hud-pet-sub.png` now exist under their requested names and are ready for owner review after mechanical QA and a 4× visual check. N01 namewell is 168×21 versus the approximate 150×28 request; N02 wells are close to contract geometry. Other exact new targets still need per-file comparison; older generic UI drafts in batches 06–08 do not automatically satisfy the newer geometry and palette contracts.
- N05 minimap frame is already satisfied by approved `ui-minimap.png`. N03/N04 have generic slot candidates; N07/N08/N09 have panel, dialogue and chat candidates, but each needs comparison against the new brief before reuse.
- N01 attempts were tested and rejected. Candidate 02 resized to 320×88 and 33 colors, but had 107 magenta-like opaque edge pixels and incorrect ring/title-strip proportions. Candidate 03 edit returned 2048×768, alpha 0–254 (255 levels), 100,781 RGB colors, and filled the transparent wells; see `art/src/hd2d/batch-14-missing-art/n01-player-plate/candidate-03/rejected/`.
- Prompt inconsistency to resolve internally: N08 `dialogue-choice.png` is initially described as 288×56, then as two vertical states in a 288×112 image. Use 288×112 (two 56 px states) as the consistent interpretation.
- Status: **N05 done; N01 and N02 main/sub candidates are ready for owner review with the geometry caveats above; N06 candidate is ready for owner review; N07 candidate has multi-size composition proof but still needs seam/engine and owner review; N03, N04, N08 and N09 need per-file reuse/redraw decisions and QA.**
- N06 `minimap-markers.png` now has a new 72×24 candidate with three 24×24 markers, binary alpha, and 48 visible colors. Pipeline and visual review are recorded in `art/src/hd2d/batch-15-expansion/minimap-markers/delivery/`; it is ready for owner review and has not been installed. Raw-sheet QC still reported `safe_frame` (value 1, threshold 0, cell [0,2]) and `faint_specks` (floor_px 11278, detached_components 8, threshold 0); processing removed the alpha haze.
- N07 `panel-frame.png` is 192×192, binary alpha and 48 visible colors. A multi-size composition preview now exists at 192×192, 320×240, 512×320 and 768×512. This shows the candidate scales as a standard 48px-corner 9-slice, but pixel continuity at all boundaries and engine sampling remain unverified; owner review is pending. Evidence: `art/src/hd2d/batch-15-expansion/ui-panel-n07/delivery/panel-frame-9slice-proof.png` and updated QA JSON.
- N02 main and sub cards now have separate processed candidates at the exact 360×128 and 264×96 canvas sizes. Both have 48 visible colors, binary alpha, and 0 heuristic magenta-like opaque pixels adjacent to transparency after a 2px edge despill. Both received a 4× checkerboard visual review; measured empty-well geometry is recorded in their QA JSON, is close to target, and remains explicitly pending owner comparison/approval. They are not installed. Files: `art/src/hd2d/batch-15-expansion/ui-pet-card-n02/delivery/`.

## Priority 3 — FX

Existing candidates are in `art/src/hd2d/batch-07-octopath/`:

| Requested effect | Existing candidate | Current state |
|---|---|---|
| Gió | `fx_wind_hit` | Draft; `approved:false`; owner/in-engine phase and pivot review pending |
| Quang | `fx_light_hit` | Draft; `approved:false`; owner/in-engine phase and pivot review pending |
| Ám | `fx_dark_hit` | Draft; `approved:false`; owner/in-engine phase and pivot review pending |
| Vô | `fx_neutral_hit` | Draft; `approved:false`; owner/in-engine phase and pivot review pending |
| Tia trúng đòn | `fx_physical_hit` | Draft; `approved:false`; owner/in-engine review pending |
| Hạ gục | `fx_ko_dissolve` | Draft; `approved:false`; owner/in-engine review pending |
| Bắt thú | `fx_capture_seal` | Draft; `approved:false`; owner/in-engine review pending |
| Triệu hồi | `fx-summon.png` | Existing owner approval is recorded in manifest/checklist; per-file QA still says `approved:false/status:needs_visual_temporal_review`, so runtime timing/pivot review remains open |

The requested elemental/effect candidates exist, but their presence is not approval or runtime activation. Verify frame sequence, pivot, and contact-sheet readability before release.

## Priority 4 — supplementary scene art

- Dedicated footstep dust and grass sheets now exist as owner-review candidates; the generic `fx_escape_dust` remains a separate escape effect.
- Ambient birds now exist as a static scene-overlay candidate; `race_bird` and `skill_bird_boon` remain icons/skill art, not replacements for this overlay.
- Deep Forest and Palace Gate foreground pieces: some forest foreground (S01–S02), palace gate/passage, and city connector candidates already exist. Verify the exact requested layers and use restrictions before creating duplicates.
- Hall connector fragments: inventory exact scene-layer destinations before generating; do not reuse facade connectors as hall joints without review.

### New candidates — 2026-10-30

- `minimap-markers.png`: delivered at 72×24, QA attached, ready for owner review; not installed.
- `fx-footstep-dust.png`: Codex rechecked the 4× preview on 2026-10-30; the progression reads as ground puff → expanding crescent → motes → fade. Delivered at 256×64 (four 64×64 frames), 24 visible colors, binary alpha; ready for owner/game-size timing review, not installed. QA retains raw-sheet WARNs: `safe_frame=2` in cells 1–2 and `faint_specks` (`floor_px=15232`, `detached_components=6`).
- `fx-footstep-grass.png`: Codex rechecked the 4× preview on 2026-10-30; upright → bend → flatten → spring-back is readable and returns to the same upright tuft. Delivered at 256×64 (four 64×64 frames), 24 visible colors, binary alpha; ready for owner/game-size timing review, not installed. QA retains raw-sheet WARNs: `safe_frame=2` in cells 1–2 and `faint_specks` (`floor_px=53397`, `detached_components=38`).
- `ambient-birds.png`: Codex rechecked the pale-sky preview on 2026-10-30; five silhouettes remain distinct. Delivered as a 388×155 transparent scene overlay, 16 visible colors and binary alpha; ready for contrast/placement review against final map backdrops, not installed. Static overlay, not an animation.

### S23 retry — 2026-10-30

- Male side-run attempt 05 produced eight figures but failed the mandatory opposite-leg contact check (frames 1/5 still read as the same lead). Raw `sheet_qc.py spill` failed: `cross_cell_components` 2/0 and `cross_cell_visible` 3/0; ownership slicing resolved the small overhangs for review only. Evidence and all warnings are in `art/src/hd2d/octopath-s01-s27-20261029/rejected/host-image-male-run-attempt-05/`. S23 remains 0/6 accepted and S24 remains blocked.

Status: **partly covered by existing art; exact missing pieces still need identification and creation.** The S07 `city-backdrop-wide.png` and S04 `fg-city-bunting.png` redraws now exist in `delivery/redraw-v2/`; README records Claude visual approval and installation via checklist F. The backdrop has a documented nonuniform-resize proportion limitation that Claude accepted for a far background. These close the two prior redraw requests, subject to keeping their recorded caveat.

## Existing assets requiring review; do not redraw by default

- 19 NPC bust portraits: exact R45 filenames and review sheets exist in the P01 release delivery. Codex has reviewed the original 13-image sheet and the six remaining portraits individually. Across the 22 portrait/starter QA files, 18 say `needs_visual_review` and 4 say `identity_visually_matched_existing`; all 22 still have `approved:false`. Two edge cases remain: `portrait-bia_shop` has an uninstalled despill candidate, and `portrait-sq_board` still needs a decision on purple hair pixels near alpha. No owner-approved final portrait set is established.
- Three large starter portraits: `starter-tien_chuong`, `starter-sa_hat`, and `starter-xich_ung` exist and were visually checked; their QA JSONs still say `needs_visual_review` / `approved:false`, so owner approval remains open.
- Monster warning rune: `foe-ring.png` exists with prompt, QA and review GIF. Codex reviewed the four-frame pulse on 2026-10-30; current QA still says `approved:false/status:needs_visual_temporal_review`, despite an older checklist/manifest approval. Runtime pivot and owner acceptance remain unresolved.
- Summon effect: `fx-summon.png` exists with prompt, QA and review GIF. Codex reviewed the six-frame sequence on 2026-10-30; current QA still says `approved:false/status:needs_visual_temporal_review`, despite an older checklist/manifest approval. Runtime pivot and owner acceptance remain unresolved.

## Execution order

1. Produce and validate the S23 male side strip as the anchor; do not start S24 before it passes visual frame 1/5 approval.
2. Complete remaining five S23 player strips.
3. Produce the 18 S24 strips from the approved player anchor, then run per-strip and contact-sheet QA.
4. Resolve/reuse/redraw N01–N09 in the prompt's priority order; test 9-slice joins and N02 coordinates.
5. Review the existing FX candidates, repair only failed assets, and generate the missing footstep/ambient/foreground pieces.
6. Update the v1.0.1 checklist and delivery index with exact approved filenames; do not install unapproved files.


### Additional continuation — 2026-10-30

- N02 generated candidate 01 was rejected before processing. Source dimensions 2103×748; inspection found 147,375 RGBA colors and multiple intermediate alpha values, so it fails the pixel-art contract. Rejection and exact N02 geometry re-prompt are recorded in `art/src/hd2d/batch-15-expansion/ui-pet-card-n02/rejected/candidate-01/`.
- N07 now has a 9-slice composition proof at four sizes. It remains a candidate: no owner approval, and seam pixel continuity/runtime renderer behavior are not proven.
- The earlier S07 city backdrop and S04 bunting redraws are confirmed by their delivery README as Claude-reviewed/installed (checklist F), though this workspace turn did not change game installation.

### Continuation note — N02 UI cards

- `hud-pet-main.png` and `hud-pet-sub.png` now exist in `batch-15-expansion/ui-pet-card-n02/delivery/`, each with a separate prompt, provenance, QA JSON and 4× checkerboard preview. Palette/alpha/dimensions and edge-fringe checks pass; exact geometry remains under owner review. Main and sub are not installed and are not marked approved.
- Candidate generations 01–06 for the main card were retained/rejected as appropriate; the final candidates use an exact layout guide, chroma key, edge despill and a 48-color palette.


### N01 player plate continuation

- `ui-player-plate-n01/delivery/hud-player-plate.png` now has separate prompt, provenance, QA and 4× checkerboard preview. Exact 320×88, binary alpha, 48 colors, 0 heuristic magenta-like opaque edge pixels. Ready for owner review, not approved; its transparent namewell measures 168×21 against the approximate 150×28 target.
- A localized edit attempt tried to correct only the namewell to ~150×28 while preserving the exact 320×88 plate. ImageGen redrew the canvas at 2168×725, with 256 alpha values and 126,108 colors. Rejected at `art/src/hd2d/batch-17-ui-n01-adjustment/rejected/`; the existing mechanically valid N01 candidate remains unchanged with its geometry caveat.

### FX contact-sheet review — continuation 2026-10-30

- Reviewed the final seven-effect contact sheet. Six-frame sequences are visually coherent as candidates. The light impact sheet has tiny dark specks near the frame-3 flash; preserve as a flagged issue pending repair. Dark and KO sheets retain purple edge-near pixels because they may be intentional art colors; inspect on a light background.
- Separate PNG candidates and review notes are in `art/src/hd2d/batch-07-octopath/delivery/review-20261030/`. All are 1152×192, binary alpha, 48 colors. Edge heuristic counts: wind 0, light 150, dark 4161, neutral 23, physical 0, KO 3558, capture 0.
- This is contact-sheet visual review only. Pivot, timing, impact scale, engine playback, and owner approval remain unverified; no FX is marked approved or installed here. The older checklist/manifest approval for summon and foe ring conflicts with their current per-file QA JSON and is recorded as an approval discrepancy below.
- Rebuilt contact sheets from the delivered `foe-ring.review.gif` and `fx-summon.review.gif` for frame-by-frame inspection. Foe ring is a four-frame centered pulse (frame 1→2→3 grows brighter, frame 4 returns near frame 1); summon is a six-frame low→peak→recovery sequence with its floor rune on a stable baseline. Both GIFs report 100 ms/frame (10 fps). Visual sequence review found no obvious frame-order or registration jump at contact-sheet scale. This does not validate game-size impact, runtime pivot, or owner acceptance. QA JSONs still say `approved:false/status:needs_visual_temporal_review`, so checklist R51–R52 are now `[!]` despite the older manifest/DELIVERY-BOOK approvals; reconcile that record before release.
- A frame-3-only cleanup attempt for `fx_light_hit` requested removal of isolated dark/purple specks without changing the six-frame FX. The image editor redrew and enlarged the burst instead: 1254×1254, 256 alpha values, 188,167 RGBA colors. It is rejected and preserved under `art/src/hd2d/batch-17-fx-light-frame3-edit/rejected/`; the original 1152×192 candidate remains the only usable review candidate, with the specks still flagged. No sheet frame was replaced.
- N07 9-slice proof was visually reviewed at 192×192, 320×240, 512×320, and 768×512: frame/corner details are readable and center remains plain. This does not prove renderer sampling/seam continuity; owner review remains pending.

### S23 retries — continuation

- Attempt 06 was generated from the attempt-05 identity/style reference. It contains eight figures, but its source is 2172×724, has 256 alpha values and ~221,055 RGBA colors, plus visible red edge fringe. It is not a finished sprite sheet. Attempt 07 asked for a frame-5-only leg swap; visual comparison shows no meaningful change and frame 1/5 still fail the opposite-contact check. Both attempts are rejected and preserved under `raw/host-image-male-run-attempt-06/` and `rejected/host-image-male-run-attempt-07/`.
- The built-in image-generation tools available here do not provide the image-to-video interface required by the character-animation skill; Forge's current diagnostic also reports no configured video API route. Do not claim this is a video-generated or accepted animation. S23 is still 0/6 and S24 still cannot start.

### UI group 3 inventory — continuation

- N03/N04/N08/N09 exploratory per-file candidates and metadata now exist under `art/src/hd2d/batch-15-expansion/ui-group3-continuation-candidates/`. They are not approved. Review found N03 rarity palette drift (including wrong-looking legendary/uncommon hues and some >48-color files); N04 equipped-corner is a scaled lock tile rather than a small corner badge; N08 dialogue-frame still needs portrait-socket geometry QA; N09 retains a blue palette and its selected-tab join is unverified. These do not close the UI requirements.

### Portrait / starter review queue reconciliation

- Source delivery has exactly 19 portrait entries. Six still explicitly await visual review: `bia_free`, `gate_guild`, `sq_exchange`, `sq_mailbox`, `sq_skill`, `sq_warehouse`. `sq_mailbox` is intentionally an object portrait per its prompt; preserve it unless the owner says the roster contract expects a human.
- Three starter portraits look coherent in the existing review images, but their current QA envelopes still say `needs_visual_review` / `approved:false`. Earlier DELIVERY-BOOK approval conflicts with those current per-image QA files; require confirmation against current deliverables before claiming completion.

### N03/N04 candidate correction and portrait review — continuation

- N03 rarity variants now use green, blue, purple and orange-gold frames; each replacement is 96×96, binary alpha and 48 colors. N04 equipped-corner is a separate 32×32 gold ribbon with 5 colors, not a scaled lock tile. A composition preview over common/rare/epic/legendary slots shows the badge is legible. Further visual QA flagged a possible detached dark pixel below the slot frame and the legendary corner-spark detail is not clearly present; these need correction/review before N03/N04 pass. Owner review and slot-edge join checks remain pending.
- Codex visually reviewed all six pending NPC portraits and three starter portraits using the existing contact/review images. No redraw defect was found. Current QA remains `approved:false/status:needs_visual_review`; checklist approval was cleared for R45 and R48–R50 until Claude/owner confirms the current delivered versions. Details: `art/src/hd2d/p01-release-art-20261023/delivery/portrait-review-codex-20261030.md`.
- Attempt 06 frame-QA result: `status=fail`, `leg_alternation=fail`, `torso_drift` warning. The report records contact pairs 0/4 and 2/6 with the same lead; it is at `art/src/hd2d/octopath-s01-s27-20261029/rejected/host-image-male-run-attempt-06-qc/sheet-qc.json`.
- N03 Legendary attempt 02 was edited for a distinct top-right spark and processed by `generate2dsprite` to 96×96, then quantized to the shared 48-color palette. Mechanics pass (binary alpha, 39 output RGBA colors), but visual QA rejects it: the spark disappears at game size with default alpha hygiene; disabling hygiene retains detached inner-edge specks, and both variants have oversized/different corner geometry. Evidence and both processed variants are at `art/src/hd2d/batch-17-ui-n03-legendary/`. Existing N03 stays unchanged and incomplete.

### Existing S23 male side-run candidate — visual gate update

- Re-reviewed the current P01 delivery `player-male.run.png` against all 8 frames and the enlarged frame 1/5 contact comparison. Frame 1 has the brown/near leg forward; frame 5 has the blue/far leg forward. Manual opposite-contact requirement passes. Its source QA has 1536×192 output, 8×192×192 cells, pivot [96,184], 48 colors, binary alpha, body heights 166–168 px, no isolated alpha pixels, no warnings, and one shared uniform scale with translation-only registration.
- Automated `leg_alternation` stays `needs-visual-review` because it cannot infer NEAR/FAR for several pairs; it did not fail as a duplicated half-cycle. Record: `art/src/hd2d/p01-release-art-20261023/delivery/player-male.run.codex-review-20261030.md`.
- This is now ready for Claude/owner review as a potential S24 anchor. It is not approved or installed. The new Oct 30 attempt 06/07 were independently rejected and are not replacements.

### N09 chat-frame redraw attempt — continuation

- A new image-edit attempt targeted a transparent interior and the approved gold minimap frame language. The model returned 2170×725 instead of 768×176, with red/green fringe on the border; it is rejected and preserved at `art/src/hd2d/batch-15-expansion/ui-group3-continuation-candidates/rejected-chat-frame-edit-01/`. Existing blue-palette N09 candidate also remains unsuitable. N09 is still open.

### N08 dialogue frame candidate — continuation

- New `dialogue-frame.png` candidate is in `art/src/hd2d/batch-15-expansion/ui-dialogue-n08-attempt-02/delivery/`, with prompt, provenance, QA and review. It meets 1024×224, 48 colors, binary alpha; palette apply passes (0 off-palette output pixels, 0 partial-alpha pixels, max dE 0.077033). Both the dialogue interior and portrait socket are transparent. Visual review passes with one caveat: portrait ring looks ~170 px across vs 160 px requested. Owner/HUD comparison and approval remain pending; not installed.

### Full run-strip visual audit — continuation

- Manual review report for the 24 existing P01 run sheets: `art/src/hd2d/p01-release-art-20261023/delivery/run-review-codex-20261030.md`. 22 are reviewable by Claude with recorded mechanical caveats; `walker-elder.run` and `walker-traveller.run` clearly repeat the same side-run lead in frames 1/5 and must be redrawn. `player-male.run` is visually cleared for opposite-leg contact and stable 166–168 px body scale, but the source QA heuristic remains `needs-visual-review`; owner approval is still required. `walker-guard.run` and `.run-up` have head-ratio detector failures that need targeted owner inspection, not automatic redraw. No strip was installed or approved. This replaces the earlier incomplete statement that all run strips were absent; accepted count remains 0 until owner sign-off.

### Scene-extra candidates — continuation

- Four individually generated candidates exist in `.ai/design/v1.0.1/candidates-scene-extras-20261030/`: Deep Forest hanging vines/mushrooms, Palace Gate paired banners, a hall front-corner pier/balustrade connector, and an opaque side-roof city plate. Each includes prompt, references, provenance and visual/mechanical review. They match planned dimensions, palette limit, and binary alpha where transparent. All remain unapproved/uninstalled pending exact anchor, blur/scale and mirrored-side decisions documented in that README.
- Rechecked all four files and their SHA-256 hashes on 2026-10-30 and added one QA JSON per PNG. The contact-sheet review found no obvious detached or composition defects; all four are `ready_for_owner_review`, not approved. Each QA file lists the unresolved scene placement/scale/anchor checks.

### Animation-capability discovery — continuation

- Re-ran `forge_doctor` and searched available plugins for image-to-video. Built-in routes still report no video API/CLI. Runway and Higgsfield are available plugin listings that can animate reference images, but neither is installed or connected in this session; no clip was generated or charged. The current diagnostic is `.ai/design/v1.0.1/forge-doctor-20261030-current.json`.

### N09 chat-frame redraw attempt 02 — continuation

- Retried a constrained edit against the 768×176 legacy frame, requesting only a transparent interior while preserving the gold border. The host image tool returned 2170×725 RGB (no alpha), 42,857 colors; dimensions, alpha and palette all fail. Preserved raw result and prompt/provenance/QA in `art/src/hd2d/batch-15-expansion/ui-group3-continuation-candidates/rejected-chat-frame-edit-02/`. Do not resize or install. The existing blue tabs also remain outside the requested dark-gold palette; selected-tab open-bottom join is unverified. N09 remains incomplete.

### N09 redraw attempts 03–04 — continuation

- Attempt 03 used `transparent_background=true` and the approved minimap frame as reference. It produced a gold frame but kept a dark, partially transparent interior; raw output is 2048×768 RGBA, 255 alpha values and 87,946 colors. Attempt 04 asked to clear the interior of that image; it remained filled, changed 1,547,557 pixels across the canvas, and measured 2048×768 RGBA, 255 alpha values and 96,279 colors. Both are rejected and preserved with prompts/provenance/QA in `art/src/hd2d/batch-16-ui-n09/redraw-01/` and `redraw-02/`. N09 remains incomplete.

### N09 redraw attempt 05 — continuation

- A new edit used the current 768×176 frame and matching chat tabs as references and requested a transparent hole. The visible composition is closer to the required border-only overlay, but the raw tool output is 2172×724 RGBA, with 256 alpha values and 60,861 RGBA colors. Exact dimensions, binary alpha, and ≤48 colors all fail; transparency of the center is not certified. Preserved and rejected at `art/src/hd2d/batch-17-ui-n09-attempt05/rejected/`. Do not resize or install. N09 remains incomplete.

### NPC portrait edge QA and candidate — continuation

- Recounted all 19 NPC portraits and 3 starter portraits at their delivered sizes: NPC portraits are 256×256 and starter portraits 512×512; each current QA file remains `approved:false`. Re-reviewed the pending six portrait sheet and all three starter previews; no new anatomy/crop defect found. This does not satisfy owner/game-UI approval.
- Detected 180 opaque magenta-hued edge pixels `(197,25,139)` on `portrait-bia_shop.png`; reprocessed its original 1254×1254 raw source through `generate2dsprite process` (binary hard key, nearest, despill radius 2, 256×256) then quantized against its existing 48-color palette. Review candidate is in `art/src/hd2d/batch-16-portrait-edge-repair/delivery/`. Counts: key-like alpha-edge pixels 180 → 0; binary alpha retained; palette apply pass, max ΔE 0.145981 / 0.15. Process QA has one `source_edge_touch_frames` warning for the intentional lower-torso crop; `key_ring_spill` and output-edge checks pass. Candidate is not installed and awaits Claude/owner visual approval.
- `portrait-sq_board` has 277 edge-adjacent fuchsia-purple pixels `(191,17,173)`, but the character is explicitly purple-haired and the preview shows the hue as part of the hair palette; retain pending a targeted owner look rather than blindly despilling intentional character color.

### S23 elder side-run redraw attempt 08 — continuation

- Generated against the existing elder strip (identity) and `player-male.run` (gait reference). Raw result is preserved at `art/src/hd2d/batch-16-run-redraw/elder-side/generated-raw.png` with prompt, provenance, QA and rejection note. It contains 8 recognizable poses but fails the contract: 2172×724 RGB, painted checkerboard, 125,831 RGBA colors, and the same leading-leg relation at frames 1 and 5. Do not crop, resize, key, or install it; such processing cannot repair the wrong gait or painted background. The existing elder/traveller strips remain the only outputs, both still fail frame-1/5 alternation.
- Elder attempt 09 used the explicit `transparent_background=true` image option. It returned real RGBA, but still 2172×724, 256 alpha levels and 166,654 RGBA colors; frames 1/5 still show the same leg lead. A targeted attempt-10 edit changed 327,669 pixels overall and did not produce a meaningful frame-5 leg swap. Both attempts are preserved with per-attempt prompts/provenance/QA in `art/src/hd2d/batch-16-run-redraw/elder-side-attempt02/` and `elder-side-attempt03/`; both rejected.
- Traveller side-run attempt 01 is at `art/src/hd2d/batch-16-run-redraw/traveller-side/`. It returned 2172×724 RGB with a painted checkerboard, 188,738 RGBA colors and the same leg lead in frames 1/5; rejected. Neither NPC strip has a new acceptable replacement yet.


## Scene-extras decision — 2026-10-30 (Claude, owner-delegated review)

| Asset | Decision | State |
|---|---|---|
| `fg-deep-vines` (M11) | **Approved, installed, used** | deep_forest top-centre foreground (`scene.ts`), dark tint |
| `fg-gate-banner-edge` (M12) | **Approved, installed, used** | `city_palace_gate` foreground, centre sightline open |
| `hall-side-corner` (M13) | **Approved art, installed in assets.json, not placed** | asymmetric corner vs existing pier at z=9.8; placement deferred to v1.1 |
| `hall-outside-roofs-side` (M14) | **Needs redraw / hold** | saturated sky clashes, duplicates backdrop layers; redraw brief in its QA json |

Not covered by this decision: all other items above stay `approved:false` (S23/S24 strips, N01–N09, FX, portraits). Their state is unchanged.
