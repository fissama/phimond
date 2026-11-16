# CODEX-DONE — 2026-11-12 (updated 2026-11-16)

## Phạm vi và trạng thái

- Roadmap: 672 task; ledger: 672 dòng, 672 ID duy nhất; mọi ID khớp CSV.
- Còn PENDING: 0. Candidate READY chưa được Claude nghiệm thu.
- **Chưa đủ 100% art** vì có FAILED và BLOCKED.

| Trạng thái | Số task |
|---|---:|
| READY_FOR_CLAUDE_REVIEW | 278 |
| FAILED_AFTER_3_TRIES | 143 |
| BLOCKED | 251 |
| PENDING | 0 |

## 2026-11-16 continuation note

- Orders 26–48 now have handoff-only candidates and are READY_FOR_CLAUDE_REVIEW; canonical art and manifests were not changed.
- `REDRAW-world_tree-floor-extra-05`: three new raw attempts were exhausted. Attempt 03 passed numeric palette/wrap/autocorrelation, but the 3×3 preview still shows a visible repeated flat-perimeter grid; remains FAILED_AFTER_3_TRIES.
- `REDRAW-gd-trunk-seg-01`: raw candidate generated, but kept BLOCKED because the exact top/bottom joining seam requires 0px vertical alpha margin, conflicting with the global ≥8px margin requirement.
- Current ledger counts: 278 READY_FOR_CLAUDE_REVIEW, 143 FAILED_AFTER_3_TRIES, 251 BLOCKED, 0 PENDING. This is not 100% complete.

## FAILED_AFTER_3_TRIES

| Task ID | Lý do / bằng chứng |
|---|---|
| REDRAW-world_tree-floor-extra-05 | 40 colors; wrap x=2.64, y=3.37 exceed 2.0 after three raw attempts; failed. |
| REDRAW-ancient-edge-03 | 3/3 attempts exhausted. Failed autocorr ≤0.25 despite seam <14, binary alpha and 37 colors. 3x1 preview, raw attempts and QA in handoff; visual motif rhythm needs new art approach. |
| REDRAW-astral-floor-extra-03 | 3/3 attempts exhausted. Best attempt 2 fails wrap_x threshold; all raw images, per-attempt metrics and best 3x3 preview in handoff. |
| REDRAW-astral-floor-extra-05 | 3/3 attempts exhausted; best attempt misses wrap_x threshold by 0.003. All raws, QA, and 3x3 preview in handoff; cross-correlation check recorded in QA. |
| REDRAW-astral-edge-03 | 3/3 attempts exhausted. Best attempt 1 metrics pass but visual 3x1 shows repeated cluster cadence; attempts 2/3 have key artifacts. Raw variants and previews in handoff. |
| REDRAW-crossroads-floor-01 | 3/3 attempts exhausted; all failed strict wrap threshold. Best attempt 1 staged with 3x3 preview; no flat navy cross. Per-attempt metrics in QA. |
| REDRAW-crossroads-floor-02 | 3/3 attempts exhausted; all fail wrap threshold. Best attempt 1, 3x3 preview saved; no navy cross. Cross-texture corr with floor-01=0.0646. |
| REDRAW-crossroads-floor-03 | 3/3 attempts exhausted; best attempt still fails wrap and visual moss cadence. 3x3 preview saved; cross-texture corr floor-01=0.0687. |
| REDRAW-crossroads-floor-05 | 3/3 attempts exhausted; all fail wrap thresholds. Best attempt 1 with 3x3 preview; cross-texture corr floor-01=0.0618. |
| REDRAW-crossroads-floor-04 | 3/3 attempts exhausted; all fail wrap thresholds. Best attempt 2 retained with 3x3 preview; no navy cross. |
| REDRAW-crossroads-floor-extra-01 | 3/3 attempts exhausted; all fail wrap thresholds. Best attempt 1 retained with 3x3 preview; corr floor-01=0.0756. |
| REDRAW-crossroads-floor-extra-02 | All 3 attempts exceeded floor wrap ≤1.25; retain best combined seam candidate-02; see QA/repeat previews. |
| REDRAW-crossroads-floor-extra-03 | All 3 attempts exhausted; strict wrap threshold missed. candidate-02 has best seam; see 3x3 previews. |
| REDRAW-desert-sandstone-floor | All 3 attempts exhausted; strict wrap threshold missed. Candidate-01 is best combined seam; see previews. |
| REDRAW-desert-sand-cracked-01 | All 3 attempts exhausted; wrap_y threshold missed. candidate-03 best combined seam retained with 3x3 previews. |
| REDRAW-desert-sand-cracked-02 | 3 attempts used. Attempt 2 best seam but repeated polygon crack-cell pattern fails visual error criteria; retained for review. |
| REDRAW-desert-limestone-grit-floor | 3 attempts exhausted; strict wrap_y threshold missed. Candidate-02 retained with QA/previews. |
| REDRAW-ghost_castle-floor-extra-01 | 3 attempts exhausted; wrap_y threshold missed. Candidate-01 retained as best combined seam. |
| REDRAW-ghost_castle-floor-extra-05 | 3 attempts exhausted; all missed floor wrap threshold. Candidate-01 best combined seam retained. |
| REDRAW-ghost_castle-edge-03 | 3 attempts exhausted. Best seam candidate has obvious repeated velvet motif in 3x1; attempt 3 drifted to wall/windows; retain attempt 2 for review. |
| REDRAW-nightmare-floor-02 | 3 attempts exhausted; strict wrap thresholds missed. Candidate-01 retained as best combined seam with 3x3 previews. |
| REDRAW-nightmare-floor-03 | 3 attempts exhausted; strict wrap_x missed. Candidate-01 retained as best combined seam. |
| REDRAW-nightmare-decal-03 | Attempt 3/3; binary alpha; margin 22px; 30 colors; candidate-03 + 4x QA preview. Claude visual review required. |
| REDRAW-nightmare-decal-04 | All 3 attempts failed: #1 <33 colors; #2 and #3 have diffuse baked glow/halo. Candidate-03 and 4x preview retained for audit. |
| REDRAW-nightmare-decal-06 | All 3 attempts below 33 colors (23/26/28); raw/candidates/4x retained. No palette edits applied. |
| REDRAW-nightmare-decal-08 | All 3 attempts failed 33-color minimum (27/27/10); attempt 1 also long trail; attempt 3 halo removed by key. Raw/candidates retained. |
| REDRAW-nightmare-decal-09 | All 3 attempts failed: colors 18/32/24; attempt 2 was a broad ground patch; attempts with glow alpha-keyed for third but sparse islands remain. |
| REDRAW-nightmare-decal-10 | All 3 attempts below 33 colors (26/30/6); attempt 3 also pale lavender/white facets and halo. Raw/candidates retained. |
| REDRAW-nightmare-backdrop-near | 3 attempts: #1 white sky; #2 repeated arches; #3 crop clips top of landmark. No compliant candidate. |
| REDRAW-tomb-wall-sprit-torch | 3 attempts; quantized results 22/29/29 colors, below required 33–48; candidate retained for audit, failure reason documented. |
| REDRAW-tomb-dead-thorn-bush | 3 fresh generations yielded 18, 21, and 24 colors after crop/resize/quantize; final below 33-color minimum. Retained candidate and raw attempts; FAILED_AFTER_3_TRIES. |
| REDRAW-tomb-dead-tree-stump | 3 fresh attempts yielded 23, 26, and 26 colors after processing, below 33–48 minimum. FAILED_AFTER_3_TRIES; all raws preserved. |
| REDRAW-tomb-guardian-statue-head | 3 fresh reference-guided generations each quantized to 26 colors (<33 minimum); candidate/raw attempts retained. Subject and approximate size met; palette complexity is blocking criterion. |
| REDRAW-tomb-hanging-censer | 3 fresh generations quantized to 17/21/19 colors, below 33–48. Failed palette complexity; raw attempts preserved. |
| REDRAW-tomb-floor-golden-sand | All 3 generated attempts reviewed; candidate 3 passes numeric seam but visibly repeats ripple bands and dark clusters in 3x3. No acceptable candidate. |
| REDRAW-tomb-edge-ruin-rubble | 3 attempts: candidate 3 meets 33 colors and seam<14 but repeats an arch motif at every tile and retains mound peaks; FAILED on visual repetition/type. |
| REDRAW-windrock-grass-snow-floor | Map palette override: brown/charcoal; snow omitted as absent from map. 3 attempts retain regular row-like grass/clump rhythm despite numeric pass; FAILED visual repetition. |
| REDRAW-windrock-snow-crust-floor | FAILED_AFTER_3_TRIES; prior three generated attempts already exhausted. One extra crop evaluation of new raw candidate retained only as diagnostic: wrap_x 1.3013 exceeds ≤1.25 and 3×3 visibly shows seams; raw/crop cannot remedy within pipeline. Map palette follows dark brown/charcoal with sparse gray snow crust. |
| REDRAW-windrock-slate-floor | 3 attempts; no seam-compliant candidate, final 3×3 visibly grids cobbles. Map palette adapted to muted dark slate/umber. |
| REDRAW-windrock-rock-floor-03 | 3 generated attempts; no candidate meets wrap≤1.25. Attempt 3 visibly tiles as a repeated cluster in 3×3. Distinct fractured-rock concept, subdued map palette. |
| REDRAW-windrock-edge-01 | 3 raw attempts; best crop is still visibly discontinuous/repeats a distinctive peak at each tile. End seam fails; not suitable for review. |
| REDRAW-windrock-edge-02 | 3 generated raw attempts; best crop still has obvious end discontinuity and repeated terrain clusters in 3×1. Cannot meet wrap criterion via crop/resize/quantize pipeline. |
| REDRAW-city-roofline-mid | 3×1 visually repeats prominent house/stall motifs inside tile; all candidates have end seam >14. Needs different, more varied raw skyline. Map refs show modest market facades; generated tall/identical forms rejected. |
| REDRAW-pet-floor-wood-fine | Three raw attempts failed wrap≤1.25; candidate 03 3×3 visibly repeats horizontal plank rows and knots. Map palette matches warm honey oak; needs a genuinely tileable new texture. |
| REDRAW-palace-floor-marble | Three raw attempts; no crop meets wrap≤1.25, final 3×3 shows distinct repeated cloud/vein forms. Dark slate palace floor palette followed; needs new tileable raw texture. |
| NEW-tower-floor-01 | 3/3 raw attempts. Every output has an unwanted inset frame/non-flat 8px border and wrap x/y > threshold; no final emitted. 3x3 preview and QA in handoff. Suggest seam-capable generation or owner-approved seam repair method. |
| NEW-tower-floor-02 | 3/3 raw attempts. Attempt 03 meets wrap ≤2 and autocorr ≤0.25, but required flat outer 8px border fails; no final emitted. Diagnostics and 3x3 preview in handoff. |
| NEW-tower-floor-03 | 3/3 attempts; attempts 1-2 wrong sand subject; attempt 03 wood but seam, cadence, and flat 8px border fail. No final emitted; 3x3 preview and QA in handoff. |
| NEW-tower-backdrop-far-01 | Three attempts exhausted. Raw waterfall/cloud forest backdrops retained; each seam fails <14. Need a seam-controllable generation method. |
| NEW-tower-floor-extra-01 | All 3 attempts low wrap seam but outer 8px border contains 3-7 colors, not flat. No code patch allowed. |
| NEW-tower-floor-extra-02 | All three have low wrap but 8px perimeter has 4-5 colors, not flat. No candidate. |
| NEW-tower-floor-extra-03 | Each generation had strong seams, but 8px perimeter not uniform (5-48 colors). |
| NEW-tower-floor-extra-04 | Moss/bark tile attempts have good wrap but perimeter contains 4-11 colors, not flat. |
| NEW-tower-floor-extra-05 | Lichen-speckled plank variants; all edges have 4-10 colors, not flat 8px perimeter. |
| NEW-tower-edge-01 | All 3 repeats visibly rhythmic; autocorr proxy >0.25. No selected candidate. |
| NEW-tower-edge-02 | Attempt 1 transparent but repeated roots/leaves; attempts 2-3 contain white background/fringe and seam worsens. No candidate. |
| NEW-tower-edge-03 | All three repeat branch/root silhouettes and leaf clumps, failing non-repeating rhythm despite seam pass. |
| NEW-tower-decal-01 | Attempts 1 and 3 have glow/haze; attempt 2 has colored fringe and dense scatter. Map-supported leaf/bark litter only; no bones. |
| NEW-tower-decal-03 | Three attempts all show diffuse colored glow; almost no opaque pixels in attempts 2-3. No candidate. |
| NEW-tower-decal-07 | Attempts 1-2 glow; attempt 3 thresholded grains too tiny/sparse to read at game scale. No candidate. |
| NEW-tower-decal-10 | 3 attempts failed: attempt 1 red/pink fringe; attempts 2–3 opaque gradient/haze. No valid cutout. |
| NEW-tower-decal-11 | 3 attempts all contain opaque atmospheric background gradients/haze. |
| NEW-tower-shadow-01 | 3 generated attempts are blurry atmospheric masses, not crisp pixel-art shadow mask. |
| NEW-tower-shadow-02 | 3 attempts yielded foggy broad shadows with no clean pixel-art silhouette. |
| NEW-tower-shadow-03 | Attempts 1/3 blurry gradient; attempt 2 has bright green border/fringe. |
| NEW-tower-backdrop-far | All 3 attempts fail seam <14; attempt 3 also has central glow; details in handoff QA. |
| NEW-tower-backdrop-mid | Attempt 1–2 seam pass but periodic motifs; attempt 3 fails seam and repeats focal trunk in 3x1. See QA. |
| NEW-tower-backdrop-near | Attempt 1 seam fail; attempts 2–3 seam pass but repeated composition; 3x1 confirms periodicity. |
| NEW-tower-marker-arrival | 3 attempts exhausted. Best visual layout is attempt 2 but 21 colors (<33); attempt 1 has black dividers/fringe; attempt 3 has horizontal divider through frames. |
| NEW-tower-fx-01 | 3 attempts exhausted. Best attempt 3 has 17 opaque colors (<33). Attempt 1 checkerboard; attempt 2 repetitive/banded background. |
| NEW-tower-fx-02 | 3 attempts exhausted. Best attempt 1 is coherent four-frame sequence but 16 colors (<33); attempt 2 repeated two rows; attempt 3 drifts. |
| NEW-tower-fx-03 | 3 attempts exhausted. Best attempt 2 is centered one-row pollen swirl but 22 colors (<33); attempt 1 has dividers; attempt 3 is 2-row 8 cells. |
| NEW-tower_region_deep_woods-landmark-01 | 3 attempts exhausted. Attempt 3 full green-striped tree silhouette, 23 colors (<33). Attempt 1 canopy cropped; attempt 2 base cropped. |
| NEW-maze-floor-01 | 3/3 generated; all fail floor seams/autocorr/flat 8px border. Raw and 3x3 previews retained; see QA/review. |
| NEW-maze-floor-02 | CSV grass prompt contradicted by all map refs; chose stone. 3/3 failed wrap/border; raw + previews retained. |
| NEW-maze-floor-03 | CSV trap floor conflicts with maps; did not bake separate spike props into floor. 3/3 fail border or repetition; raw/previews retained. |
| NEW-maze-backdrop-far-01 | 3/3 fail repetition, seam or source palette; raws/previews and per-attempt metrics retained. |
| NEW-maze-floor-extra-01 | 3/3 fail floor wrap, autocorr or flat border; raw and previews retained. |
| NEW-maze-floor-extra-02 | 3 attempts exhausted; autocorrelation >0.25 and flat outer 8px fails. See QA/review. |
| NEW-maze-floor-extra-03 | 3 attempts exhausted; autocorrelation >0.25 and outer 8px not flat. See QA/review. |
| NEW-maze-floor-extra-04 | 3 attempts exhausted; autocorrelation/flat border fail. See QA/review. |
| NEW-maze-floor-extra-05 | 3 attempts exhausted; tile seams/autocorrelation/perimeter fail. See QA/review. |
| NEW-maze-edge-01 | Three raws have baked baseline/paving, visible red fringe, nonmatching endpoints; see QA/review. |
| NEW-maze-edge-02 | Three generated raws retain paving baseline/fringe and endpoint mismatch; see QA/review. |
| NEW-maze-edge-03 | 3 raws show alpha fringe and nonmatching ends; rubble density unsuitable. See QA/review. |
| NEW-maze-decal-01 | All 3 raw images include a broad soft glow/halo; no clean decal candidate. See QA/review. |
| NEW-maze-decal-02 | All 3 generations contain broad halo/glow; see QA/review. |
| NEW-maze-decal-03 | All 3 have residual halo/background; attempt 3 only 20 colors. See QA/review. |
| NEW-maze-decal-04 | 3 raws contain broad glow/halo; threshold cannot produce clean decal. See QA/review. |
| NEW-maze-decal-05 | All 3 raw generations contain broad halo; cannot make clean decal. See QA/review. |
| NEW-maze-decal-06 | 3 generated raws have broad halo/glow; cannot form clean decal. See QA/review. |
| NEW-maze-backdrop-far | Attempt 3 seam 12.28 but autocorr 0.8198 and repeated architecture in 3×1; see QA/review. |
| NEW-maze-backdrop-mid | 3 attempts; autocorrelation exceeds 0.25 and 3x1 repeats architecture; no final candidate. Procedural deviation: one extra unscored generation preserved; cap exceeded, extra also visually repeats. |
| NEW-maze-backdrop-near | All 3 attempts exceed autocorrelation .25; all exceed horizontal seam <14. 3x1 shows repetitive architecture. |
| NEW-immortal_maze_secret_floor-landmark-01 | Map feature chose ribbed pillar; 3 attempts retain halo/soft edges; selected preview has 28 colors (<33), so no submission. |
| NEW-guild-floor-01 | All 3 failed: #1 seam=6.6221, autocorr=0.4555, colors=48, flat8=False: seam 6.622>2; autocorr 0.455>.25; outer 8px band not flat; visible repeated large slab/grid cadence | #2 seam=14.9684, autocorr=0.2615, colors=48, flat8=False: seam 14.968>2; autocorr 0.261>.25; outer 8px band not flat; texture overly dense/repetitive tile rhythm | #3 seam=4.2008, autocorr=0.3383, colors=48, flat8=False: seam 4.201>2; autocorr 0.338>.25; outer 8px band not flat; coarse lower-detail surface with repeated broad slab shapes |
| NEW-guild-floor-02 | Source map paving overrides wood floor plan. 3 generated attempts; all exceed seam/autocorr and fail flat 8px perimeter. See handoff qa.json + 3x3 previews. |
| NEW-guild-floor-03 | Source map paving overrides guild rug plan. 3 attempts; all fail seam/autocorr and flat 8px perimeter. See QA and 3x3 previews. |
| NEW-guild-floor-04 | Source-map stone overrides training-court description. 3 attempts failed seam/autocorr/flat 8px perimeter. See handoff QA/previews. |
| NEW-guild-prop-04 | Source supports indigo tower flag. Attempts quantized to 20, 25, and 31 colors (<33). Attempt 2 SAM mask damaged cloth; see previews and QA log. |
| NEW-battlefield-floor-01 | Selected measurement candidate 3 for failure evidence; 3x3 repeats broad slabs, autocorr >.25, outer 8px not flat. No final. |
| NEW-battlefield-floor-02 | All 3 attempts fail seam/autocorr; visible slab recurrence; floor-01 comparison unavailable. |
| NEW-battlefield-floor-extra-01 | All attempts fail seam<2.0 and uniform border; 1/3 also autocorr>.25. No final; base cross-check unavailable. |
| NEW-battlefield-floor-extra-02 | All 3 fail seam<2.0; attempts 1/2 also autocorr>.25. Candidate 3 autocorr .218 but seam fails. No final. |
| NEW-battlefield-floor-extra-03 | All 3 fail seam/autocorrelation; final try very high recurrence. No candidate; base floor comparison unavailable. |
| NEW-battlefield-floor-extra-04 | Failed all 3 tries: #1 seam=13.5091, autocorr=0.1934, colors=48, flat8=False | #2 seam=7.7679, autocorr=0.2816, colors=48, flat8=False | #3 seam=8.5241, autocorr=0.3601, colors=48, flat8=False |
| NEW-battlefield-floor-extra-05 | All 3 failed: #1 seam=0.4355, autocorr=0.1255, colors=48, flat8=False | #2 seam=5.6842, autocorr=0.4289, colors=48, flat8=False | #3 seam=13.5908, autocorr=0.3314, colors=48, flat8=False |
| NEW-battlefield-edge-01 | All 3 failed; #1 seam=16.6745, colors=45, alpha_binary=True: end seam 16.674 >=14; wrong object content: contains arena props/statues/columns and visible red/yellow fringe | #2 seam=15.5807, colors=45, alpha_binary=True: end seam 15.581 >=14; repetitive slab cadence, visible red/yellow edge fringe | #3 seam=1.8073, colors=45, alpha_binary=True: too regular repeated stone cadence, visible chromatic fringe; endpoint continuity needs visual rejection |
| NEW-battlefield-edge-02 | All 3 failed: #1 seam=7.6562, colors=45: visual: repeated edge/plate cadence or chromatic alpha fringe visible; not acceptable as unique irregular seamless edge | #2 seam=7.6354, colors=45: visual: repeated edge/plate cadence or chromatic alpha fringe visible; not acceptable as unique irregular seamless edge | #3 seam=5.4219, colors=45: visual: repeated edge/plate cadence or chromatic alpha fringe visible; not acceptable as unique irregular seamless edge |
| NEW-battlefield-edge-03 | All 3 failed: #1 seam=7.2708, colors=45, fringe=False: visual silhouette still has predictable rubble rhythm | #2 seam=8.0365, colors=43, fringe=False: visual cadence repeats and red/yellow fringe visible | #3 seam=17.401, colors=40, fringe=False: end seam >=14; soft translucent fringe/blur and texture noise; not crisp pixel-art and alpha edge not clean |
| NEW-battlefield-decal-01 | All 3 failed: #1 colors=40, margin=34: raw alpha not binary (threshold applied); red/yellow fringe and large decorative inscribed slabs; not intended decal | #2 colors=25, margin=0: colors out of range; alpha margin 0<8; raw alpha not binary (threshold applied); visible baked soft halo/glow; smooth halo violates no baked shadow/glow | #3 colors=26, margin=20: colors out of range; raw alpha not binary (threshold applied); visible baked soft halo/glow; smooth halo violates no baked shadow/glow |
| NEW-battlefield-decal-02 | All 3 failed: #1 colors=35, margin=0, soft_alpha=True: margin 0<8; raw alpha soft/continuous; threshold required; visible baked glow/halo | #2 colors=19, margin=0, soft_alpha=True: colors 19<33; margin 0<8; raw alpha soft/continuous; threshold required; visible baked glow/halo | #3 colors=44, margin=47, soft_alpha=True: raw alpha soft/continuous; threshold required; yellow/red chromatic fringe visible around rock silhouettes |
| NEW-battlefield-decal-03 | All 3 failed: #1 colors=24, margin=17, soft_alpha=True, fringe=False: colors 24<33; source alpha not binary; baked soft halo/glow visible | #2 colors=43, margin=0, soft_alpha=True, fringe=False: margin 0<8; source alpha not binary; colored fringe around stone silhouette | #3 colors=22, margin=0, soft_alpha=True, fringe=False: colors 22<33; margin 0<8; source alpha not binary; baked soft halo/glow visible |
| NEW-battlefield-decal-04 | All 3 failed: #1 colors=15, margin=0, soft_alpha=True, fringe=False: colors 15<33; margin 0<8; source alpha soft/continuous; visible baked glow/soft halo | #2 colors=19, margin=0, soft_alpha=True, fringe=False: colors 19<33; margin 0<8; source alpha soft/continuous; visible baked glow/soft halo | #3 colors=19, margin=0, soft_alpha=True, fringe=False: colors 19<33; margin 0<8; source alpha soft/continuous; visible baked glow/soft halo |
| NEW-battlefield-decal-05 | All 3 failed: #1 colors=20, margin=0, soft_alpha=True, fringe=False: colors 20<33; margin 0<8; raw alpha not binary; baked soft halo/glow visible | #2 colors=42, margin=0, soft_alpha=True, fringe=False: margin 0<8; raw alpha not binary; baked soft halo/glow visible | #3 colors=20, margin=0, soft_alpha=True, fringe=False: colors 20<33; margin 0<8; raw alpha not binary; baked soft halo/glow visible |
| NEW-battlefield-decal-06 | All 3 failed: #1 colors=9, margin=0, soft_alpha=True, fringe=False: colors 9<33; margin 0<8; raw alpha nonbinary/soft; baked glow | #2 colors=36, margin=0, soft_alpha=True, fringe=False: margin 0<8; raw alpha nonbinary/soft | #3 colors=43, margin=0, soft_alpha=True, fringe=False: margin 0<8; raw alpha nonbinary/soft |
| NEW-battlefield-decal-08 | All 3 failed: #1 colors=37, margin=0, soft_alpha=True, fringe=False: margin 0<8; source alpha nonbinary; baked glow/halo | #2 colors=21, margin=0, soft_alpha=True, fringe=False: colors 21<33; margin 0<8; source alpha nonbinary | #3 colors=20, margin=0, soft_alpha=True, fringe=False: colors 20<33; margin 0<8; source alpha nonbinary; baked glow/halo |
| NEW-battlefield-decal-09 | All 3 failed: #1 colors=22, margin=0, soft_alpha=True: colors 22<33; margin 0<8; source alpha nonbinary/soft; baked soft halo visible | #2 colors=27, margin=0, soft_alpha=True: colors 27<33; margin 0<8; source alpha nonbinary/soft; baked soft halo visible | #3 colors=24, margin=0, soft_alpha=True: colors 24<33; margin 0<8; source alpha nonbinary/soft |
| NEW-dungeon-floor-01 | Three attempts failed wrap/autocorr/border-flat metrics; map type/palette followed; candidates+3x3 previews saved; reopen with tileable-generation workflow. |
| NEW-dungeon-floor-02 | Three attempts fail seamless criteria; attempt3 seam=17.54, autocorr=0.145, flat8=False; source-map material retained; see QA + 3x3 previews. |
| NEW-dungeon-floor-03 | Three attempts; attempt3 seam=15.67, autocorr=0.074, flat8=False; map source overrode straw plan; see QA + 3x3 previews. |

| NEW-dungeon-floor-extra-01 | 3 raw attempts failed original floor QA. Tileable postprocess wrap=0/0, 48 colors, flat8=1, but 3x3/4x4 show cross-shaped blend streaks and repeated cadence; retained FAILED. |
| NEW-dungeon-floor-extra-02 | 3 raw attempts failed original floor QA. Tileable postprocess made obvious internal seam streaks and repeated motifs in 3x3/4x4; retained FAILED. |
| NEW-dungeon-floor-extra-03 | 3 raw attempts failed original floor QA. Tileable postprocess made obvious internal seam streaks and repeated motifs in 3x3/4x4; retained FAILED. |
| NEW-dungeon-floor-extra-04 | 3 ImageGen raws exhausted; best wrap_x/y=14.071/14.449, 48 colors at flat8; repeated tile motif visible in 3x3/4x4. |

| NEW-dungeon-floor-extra-05 | 3/3 ImageGen raws; best wrap 13.113/7.893, flat8 has 48 colors; 3x3/4x4 show tile cadence. |

| NEW-dungeon-edge-01 | 3/3 raws and edge postprocess failed; autocorrelation remains 0.612 at lag 264, RGB end seam 33.075, obvious repeated rock cadence in 3×1. |
| NEW-guild-floor-extra-01 | 3 raw attempts; offset+24px blend postprocess achieved wrap 0/0 and flat 8px border, but autocorrelation remained 0.335–0.457 (>0.25) and 3×3 shows repeated slab motifs. |
| NEW-guild-floor-extra-02 | 3 raw attempts; offset+24px blend produced 48 colors, flat8, wrap 0/0; autocorr 0.381–0.582 (>0.25) and 3×3 repeated large slabs. Cross-floor texture correlation also documented in QA. |
| NEW-guild-floor-extra-03 | 3 raw attempts; wrap 0/0, flat8, 48 colors; best autocorr 0.25378 at lag 8 (>0.25), and 3×3 shows a repeated central diagonal slab motif. |

| NEW-guild-edge-01 | 3 raws; best edge seam=1.2422, 44 colors, binary alpha after cleanup; autocorr 0.78203 at lag 456 and 3×1 repeats a mound every tile. |

| NEW-guild-floor-extra-04 | 3 raw attempts; wrap 0/0, flat8, 48 colors; best autocorr 0.38826 (>0.25) and 3×3 repeats slab clusters. |

| NEW-guild-edge-02 | 3 raw attempts; best seam 1.7318 and 46 colors after alpha cleanup; autocorr 0.75699 at lag 111 and 3×1 repeats mound/ivy cadence. |

| NEW-guild-edge-03 | 3 raw attempts; best seam 0.375, 40 colors and binary alpha; autocorr 0.78934 at lag 206 and 3×1 repeats rubble peaks. |
| NEW-maya-floor-02 | 3 raws exhausted; best attempt meets wrap and palette but autocorr 0.3343 at lag 8 and visible repeated slab cadence; handoff evidence retained. |
| NEW-maya-prop-03 | 3 raws exhausted; each retains connected near-opaque vignette after alpha key/1px erosion, leaving a visible halo. No compliant cutout. |

## BLOCKED

Có 324 task BLOCKED; các reason đã chuẩn hóa trong ledger. Phân loại hiện tại: A=196, B=45, C=83. Không có artwork thay thế được ghi cho BLOCKED.

### 196 task — A — cần ảnh mới, route hiện bị rate limit (`A_NEW_IMAGE_ROUTE_REQUIRED`)

| Task ID | Ghi chú / đề xuất |
|---|---|
| NEW-guild-backdrop-far | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-floor-extra-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-floor-extra-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-floor-extra-05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-edge-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-edge-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-edge-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-07 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-08 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-09 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-10 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-11 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-decal-12 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-backdrop-far | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-backdrop-mid | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-backdrop-near | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-portal-dormant | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-portal-active | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-marker-arrival | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-fx-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-fx-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya-fx-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-maya_floor_01-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-07 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-08 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-09 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-10 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-11 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-decal-12 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-backdrop-far | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-backdrop-mid | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-backdrop-near | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-portal-dormant | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-portal-active | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-marker-arrival | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-fx-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-fx-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon-fx-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-dungeon_floor_01-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-07 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-08 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-09 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-10 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-11 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-12 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-13 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-14 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-prop-15 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-backdrop-far-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-extra-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-extra-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-extra-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-floor-extra-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-edge-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-edge-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-edge-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-07 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-08 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-09 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-10 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-11 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-decal-12 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-backdrop-far | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-backdrop-mid | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-backdrop-near | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-portal-dormant | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-portal-active | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-marker-arrival | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-fx-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-fx-02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-minigame-fx-03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-wolf_sheep_waiting_hall-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-wolf_sheep_sheep_house-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-wolf_sheep_sheep_pen-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-wolf_sheep_middle_field-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-wolf_sheep_wolf_pen-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| NEW-wolf_sheep_wolf_house-landmark-01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-emerald_forest_main_woods | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-emerald_forest_deep_woods | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_square | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_market | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_palace_gate | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_royal_palace | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_activity_hall | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_pet_room | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_farm | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-city_deathmatch_arena | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-summoning_hall_main_hall | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-treasure_beach_fishermen_beach | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-treasure_beach_east_beach | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-treasure_beach_west_beach | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-treasure_beach_deep_sea | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-treasure_beach_prosperity_island | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-middle_corridor_main_hall | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-desert_shicheng_ruins | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-desert_entrance | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-desert_sealed_land | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-desert_hulu_tribe | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-desert_barren_sands | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-desert_disaster_sands | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-windrock_mountain_camp | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-windrock_mountain_stone_bridge | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-windrock_mountain_howling_canyon | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-windrock_mountain_mountain_range | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-windrock_mountain_mountain_path | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-windrock_mountain_summit | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-nightmare_island_survivor_camp | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-nightmare_island_east_magic_island | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-nightmare_island_ruins | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-nightmare_island_disaster_gate | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-nightmare_island_resentment_path | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-nightmare_island_despair_land | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_camp | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_resentment_path | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_despair_path | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_dead_ruins | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_deep_ruins | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_gods_tomb | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_soul_cemetery | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_unnamed_area_01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tomb_region_unnamed_area_02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-crossroads_unnamed_area_01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-crossroads_unnamed_area_02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-crossroads_unnamed_area_03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-crossroads_unnamed_area_04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-crossroads_unnamed_area_05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-crossroads_unnamed_area_06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_unnamed_area_01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_spacetime_rift | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_unnamed_area_02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_unnamed_area_03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_unnamed_area_04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_unnamed_area_05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-astral_realm_unnamed_area_06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ancient_ruins_unnamed_area_01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ancient_ruins_unnamed_area_02 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ancient_ruins_unnamed_area_03 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ancient_ruins_unnamed_area_04 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ancient_ruins_unnamed_area_05 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ancient_ruins_unnamed_area_06 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ghost_castle_gate | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ghost_castle_deep_woods | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-ghost_castle_ancient_city_secret_chamber | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-world_tree_gate | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-world_tree_deep_woods | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-world_tree_secret_chamber | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tower_region_main_tower | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tower_region_deep_woods | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-tower_region_secret_floor | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-immortal_maze_main_maze | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-immortal_maze_floor | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-immortal_maze_secret_floor | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_fortress | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_treasury | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_warehouse | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_barracks | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_shop | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_pet_stable | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-guild_battlefield_main_field | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-maya_floor_01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-dungeon_floor_01 | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-chaos_arena_main_field | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-team_arena_main_field | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-wolf_sheep_waiting_hall | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-wolf_sheep_sheep_house | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-wolf_sheep_sheep_pen | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-wolf_sheep_middle_field | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-wolf_sheep_wolf_pen | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |
| SCENE-wolf_sheep_wolf_house | Cần raw ảnh mới; ImageGen hiện trả HTTP 429 usage_limit_reached và reset sau khoảng 2 giờ; tiếp tục sau quota reset. Tạo lại sau khi ImageGen quota reset; Runway không dùng theo yêu cầu. |

### 45 task — B — cần canonical/manifest/alpha-margin review (`B_CANONICAL_MANIFEST_ALPHA_REVIEW`)

| Task ID | Ghi chú / đề xuất |
|---|---|
| FIX-ancient-marker-arrival | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=340348e285, QA sha=340348e285, actual sha=340348e285); user forbids registering/updating manifest before Claude acceptance. |
| FIX-crossroads-water-foam-frame-00 | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=55ff3542a7, QA sha=41078a321c, actual sha=41078a321c); user forbids registering/updating manifest before Claude acceptance. |
| FIX-crossroads-water-foam-frame-01 | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=2b790393c0, QA sha=d5faf74240, actual sha=d5faf74240); user forbids registering/updating manifest before Claude acceptance. |
| FIX-crossroads-water-foam-frame-02 | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=bbd62fbe8d, QA sha=a45c3cf972, actual sha=a45c3cf972); user forbids registering/updating manifest before Claude acceptance. |
| FIX-crossroads-water-foam-frame-03 | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=6a286ee519, QA sha=bbae078218, actual sha=bbae078218); user forbids registering/updating manifest before Claude acceptance. |
| FIX-city-hanging-sign | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=b178e82973); user forbids registering/updating manifest before Claude acceptance. |
| FIX-city-bunting | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=a052bfe788); user forbids registering/updating manifest before Claude acceptance. |
| FIX-city-vendor-cart | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=686c41e4ea); user forbids registering/updating manifest before Claude acceptance. |
| FIX-city-topiary | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=3aadab7f08); user forbids registering/updating manifest before Claude acceptance. |
| FIX-city-iron-fence | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=a14d6c243c); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-guard-booth | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=af28bce099); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-long-planter | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=c02c9cd750); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-lion-r | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=252da123b6); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-lion-l | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=f2c2600a64); user forbids registering/updating manifest before Claude acceptance. |
| FIX-animal-dog | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=f6bfbc4693); user forbids registering/updating manifest before Claude acceptance. |
| FIX-animal-butterflies | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=92e9745242); user forbids registering/updating manifest before Claude acceptance. |
| FIX-animal-crow | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=1092bfc69b); user forbids registering/updating manifest before Claude acceptance. |
| FIX-decal-cracks | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=b922f61ca0); user forbids registering/updating manifest before Claude acceptance. |
| FIX-decal-puddle | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=c92a6fe85f); user forbids registering/updating manifest before Claude acceptance. |
| FIX-decal-petals | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=846458e82c); user forbids registering/updating manifest before Claude acceptance. |
| FIX-decal-hopscotch | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=f3972d4874); user forbids registering/updating manifest before Claude acceptance. |
| FIX-decal-ruts | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=None, QA sha=None, actual sha=74a80fdc26); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-rug-round | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=d7db7a5c8f, QA sha=None, actual sha=d7db7a5c8f); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-rug-long | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=b03b3b27e9, QA sha=None, actual sha=b03b3b27e9); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-cage-small | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=da37fc670e, QA sha=None, actual sha=da37fc670e); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-cage-large | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=8ee3f3fd61, QA sha=None, actual sha=8ee3f3fd61); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-perch-stand | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=c9b1d6390a, QA sha=None, actual sha=c9b1d6390a); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-toy-pile | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=433ff9adc1, QA sha=None, actual sha=433ff9adc1); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-scratch-post | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=4e19fa501c, QA sha=None, actual sha=4e19fa501c); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-sleeping-01 | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=50afdb5118, QA sha=None, actual sha=50afdb5118); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-sleeping-02 | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=795ff7b587, QA sha=None, actual sha=795ff7b587); user forbids registering/updating manifest before Claude acceptance. |
| FIX-pet-shelf-alt | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=ac9480eb10, QA sha=None, actual sha=ac9480eb10); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-gate | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=efd173fbe8, QA sha=None, actual sha=efd173fbe8); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-judge-podium | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=2956d8b8a7, QA sha=None, actual sha=2956d8b8a7); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-barrier-h | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=b516d92b13, QA sha=None, actual sha=b516d92b13); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-barrier-corner | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=f86f66805e, QA sha=None, actual sha=f86f66805e); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-brazier | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=1821467bf7, QA sha=None, actual sha=1821467bf7); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-center-medallion-large | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=df11756baa, QA sha=None, actual sha=df11756baa); user forbids registering/updating manifest before Claude acceptance. |
| FIX-arena-column-short | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=e11d59b880, QA sha=None, actual sha=e11d59b880); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-throne-dais | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=4f36f4b28d, QA sha=None, actual sha=4f36f4b28d); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-window-blue | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=fec00f3097, QA sha=None, actual sha=fec00f3097); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-window-red | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=6d71dd665f, QA sha=None, actual sha=6d71dd665f); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-banner-blue-long | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=762376e0fa, QA sha=None, actual sha=762376e0fa); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-banner-red-long | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=9b0e519bf2, QA sha=None, actual sha=9b0e519bf2); user forbids registering/updating manifest before Claude acceptance. |
| FIX-palace-guard-statue-gold | BLOCKED: canonical fix needs manifest/QA and/or alpha-margin change (manifest sha=56da17bf4c, QA sha=None, actual sha=56da17bf4c); user forbids registering/updating manifest before Claude acceptance. |

### 83 task — C — baseline/dependency review (`C_BASELINE_OR_DEPENDENCY_REVIEW`)

| Task ID | Ghi chú / đề xuất |
|---|---|
| VIEW-batch-00 | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-01-octopath | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-02-octopath | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-03-octopath | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-05-octopath | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-09-octopath | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-10-octopath | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-batch-13-release | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-octopath-s01-s27-20261029 | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| VIEW-p01-release-art-20261023 | BLOCKED: task requires individual visual verdicts; Codex cannot self-approve and existing batch summaries do not supply complete fresh visual review for every ID. |
| REDRAW-gd-trunk-seg-01 | BLOCKED: later owner-approved 13d handoff says keep gd-trunk-seg-01 as the only trunk body variant; CSV redraw task is stale/conflicting. |
| REDRAW-gd-trunk-seg-02 | BLOCKED: owner retired variant 02 in 13d handoff; do not redraw or load. |
| REDRAW-gd-seal-strip-lit | BLOCKED: owner superseded asset with gd-seal-rune-glow; do not re-open retired strip-lit asset. |
| NEW-tower-prop-10 | CSV requests spiral stairs, but source refs show flat plank bridges and no spiral stair. Do not substitute another asset type. Needs roadmap/source correction or authoritative reference before drawing. |
| NEW-maze-prop-02 | BLOCKED: CSV calls for vines, absent from all three map refs. No substitute asset drawn per source-of-truth rule. |
| NEW-maze-prop-07 | BLOCKED: requested object not visible in any of the three map refs; no replacement drawn. |
| NEW-maze-prop-08 | BLOCKED: requested object not visible in any of the three map refs; no replacement drawn. |
| NEW-maze-prop-09 | BLOCKED: requested object not visible in any of the three map refs; no replacement drawn. |
| NEW-maze-prop-10 | BLOCKED: requested object not visible in any of the three map refs; no replacement drawn. |
| NEW-guild-prop-05 | Two generated attempts: 25 and 19 colors (<33); second also contains an unsupported extra mini-flag. Third generation blocked because only 3 Runway credits remain; Gen-4 request rejected by workspace_limit. See QA/review. |
| NEW-battlefield-floor-03 | CSV plan says burnt grass, but attached battlefield reference is a pale cream indoor/plaza floor with no grass or vegetation. Per source-map truth and no-substitution rule, do not create another floor type without evidence. |
| NEW-battlefield-prop-01 | BLOCKED: embedded weapon not visible in battlefield source image; source instead shows arena statues and fountain. No substitute generated. |
| NEW-battlefield-prop-02 | BLOCKED: embedded weapon not visible in battlefield source image; no such weapon class evidenced. No substitute generated. |
| NEW-battlefield-prop-03 | BLOCKED: embedded weapon not visible in battlefield source image; no such weapon class evidenced. No substitute generated. |
| NEW-battlefield-prop-04 | BLOCKED: embedded weapon not visible in battlefield source image; no such weapon class evidenced. No substitute generated. |
| NEW-battlefield-prop-05 | BLOCKED: broken chariot is absent from the source image. No substitute generated. |
| NEW-battlefield-prop-06 | BLOCKED: wooden watchtower is absent; source shows purple-gold colonnade and distant city buildings. No substitute generated. |
| NEW-battlefield-prop-07 | BLOCKED: battlefield barricade is absent from the source image. No substitute generated. |
| NEW-battlefield-prop-08 | BLOCKED: torn war flag is absent from the source image. No substitute generated. |
| NEW-battlefield-prop-09 | BLOCKED: second torn war flag is absent from the source image. No substitute generated. |
| NEW-battlefield-prop-10 | BLOCKED: bomb crater is absent from the source image. No substitute generated. |
| NEW-battlefield-prop-11 | BLOCKED: campfire is absent from the source image. No substitute generated. |
| NEW-battlefield-prop-12 | BLOCKED: broken bones/armor are absent from the source image. No substitute generated. |
| NEW-battlefield-backdrop-far-01 | BLOCKED: smoke/fire horizon conflicts with visible blue city skyline and orange roofs. No substitute generated. |
| NEW-dungeon-prop-02 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-03 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-04 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-05 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-06 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-07 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-08 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-prop-09 | BLOCKED: source map only supports beige/olive room masonry, pale scale-patterned floor and orange deer trophies; requested subject is not visible or duplicates prop-01. Await brief/map owner correction; do not invent substitute. Image route currently available. |
| NEW-dungeon-backdrop-far-01 | BLOCKED: New 2026-11-12 retry made no image. Built-in ImageGen again returned 429 usage_limit_reached. Runway nano-banana-2 rejected 3:1 as unsupported; 4:1 retry was rejected with workspace_limit. No substitute image. Resume when generation access/credits are available; then follow source map (beige/olive stone-brick wall) and seam-check. |
| NEW-arena2-floor-01 | CSV prompt says draw only differences after battlefield kit is complete; same screenshot/palette as battlefield, whose floor variants are still PENDING at orders 208–210. Cannot invent/differentiate or reuse/mirror another asset. |
| NEW-arena2-floor-02 | CSV prompt says draw only differences after battlefield kit is complete; same screenshot/palette as battlefield, whose floor variants are still PENDING at orders 208–210. Cannot invent/differentiate or reuse/mirror another asset. |
| NEW-arena2-floor-03 | CSV prompt says draw only differences after battlefield kit is complete; same screenshot/palette as battlefield, whose floor variants are still PENDING at orders 208–210. Cannot invent/differentiate or reuse/mirror another asset. |
| NEW-arena2-prop-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-prop-02 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-prop-03 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-prop-04 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-prop-05 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-backdrop-far-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-floor-extra-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-floor-extra-02 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-floor-extra-03 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-floor-extra-04 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-floor-extra-05 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-edge-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-edge-02 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-edge-03 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-02 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-03 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-04 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-05 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-06 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-07 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-08 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-09 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-10 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-11 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-decal-12 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-backdrop-far | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-backdrop-mid | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-backdrop-near | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-portal-dormant | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-portal-active | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-marker-arrival | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-fx-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-fx-02 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-arena2-fx-03 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-chaos_arena_main_field-landmark-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |
| NEW-team_arena_main_field-landmark-01 | Arena2 source map is the same battlefield screenshot and prompt says only draw differences after battlefield is complete. Battlefield floor/edge tasks at orders 208+ are still PENDING. Do not duplicate, mirror or recolor common assets; revisit after source kit is complete and only draw evidenced differences. |

## Art gate

- Lệnh: `python3 tools/hd2d_audit/art_gate.py --all` (prefix `rtk`); fresh output: [`/tmp/phimond-art-gate-all-2026-11-13.log`](/tmp/phimond-art-gate-all-2026-11-13.log).
- Kết quả: **1.434 assets, 367 lỗi, 0 cảnh báo**. Phân loại kỹ thuật: audit 295; bbox-edge 35; size 16; sheet 21.
- Ghép lỗi theo asset ID trong roadmap: **342 baseline/canonical cũ** (bao gồm lỗi canonical của task FAILED, candidate vẫn nằm handoff-only), **8 lỗi asset READY**, **17 lỗi asset BLOCKED**. Tổng 367. Các mismatch không gắn được với task asset_id, gồm lỗi batch cũ/sheet, tính baseline.
- Gate là kiểm tra cơ học canonical/manifest, không phải nghiệm thu hình. Handoff candidates chưa đăng ký.

## Latest resume status — 2026-11-13

- Verified ledger: 672 task IDs, 672 unique rows; 211 READY_FOR_CLAUDE_REVIEW, 137 FAILED_AFTER_3_TRIES, 324 BLOCKED, 0 PENDING. READY means candidate submitted for Claude review only.
- BLOCKED classes: A=196 (new image required, current ImageGen route is rate limited), B=45 (canonical/manifest/alpha-margin review), C=83 (baseline/dependency review).
- Newly READY in this resume: `NEW-maya-floor-03`, `NEW-maya-prop-01`, `NEW-maya-prop-02`, `NEW-maya-prop-04`, `NEW-maya-prop-05`, `NEW-maya-prop-06`, `NEW-maya-prop-07`, `NEW-maya-prop-08`, `NEW-maya-prop-09`, `NEW-maya-prop-10`, `NEW-maya-prop-11`, `NEW-maya-backdrop-far-01`, `NEW-maya-floor-extra-01`, `NEW-maya-floor-extra-02`.
- Newly FAILED: `NEW-maya-floor-02` (autocorr 0.3343 at lag 8 after three raws) and `NEW-maya-prop-03` (three raws retain connected vignette after alpha key and erosion).
- `NEW-maya-floor-extra-03` remains BLOCKED A: attempt 1 failed autocorr 0.4765; attempt 2 was stopped by ImageGen HTTP 429 `usage_limit_reached` (reset in about 7,385 seconds). Runway is excluded per user instruction. The current permitted image-generation route is therefore blocked; no substitute was used.
- Handoff candidates and two 3×3 Maya montages are under `.ai/design/map-checklists/handoffs/art-submit-2026-11-12/maya/`. No canonical assets or manifests were modified.

**Chưa đủ 100%:** 137 FAILED_AFTER_3_TRIES and 324 BLOCKED remain. Work paused because the only image route permitted for this task is rate limited. Resume after ImageGen quota reset.
