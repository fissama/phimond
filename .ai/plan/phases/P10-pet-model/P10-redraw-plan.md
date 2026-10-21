# P10 pixel-sprite redraw contract

Status: CLOSED — all160 selected atlas art bundles owner-approved,2026-10-21. Historical152closure retained below.
Current closure: [P10-redraw-closure-160-20261021.md](P10-redraw-closure-160-20261021.md). Historical closure: [P10-redraw-closure-20261011.md](P10-redraw-closure-20261011.md).
Supersedes the former untracked anime redraw draft, not P10 gameplay gates.
Previous draft and all 20 pre-existing dirty/untracked files preserved at
`/tmp/phimond-p10-dirty-backup-20260930/`; hashes recorded in
`/tmp/phimond-p10-preservation-20260930.json`.

## Ownership and scope

Owner confirmed no one is still editing the four-species art/client work.
Lead assigns exclusive ownership below. No push, merge, deploy, server restart,
DB mutation or gameplay migration.

- Lead: this plan and P10-provenance-milestone.md, integration and dispositions.
- Tooling/client Peer: tools/content/p10_provenance.py and its test;
  tools/assets/check_p10_atlas.py and its test; the four existing dirty
  apps/game-client/assets/pets/apk84/{DaoThienDuong,DocDangNu,MaVuongHutMau,NuVuongBachCot}/
  directories; new assets/pets/redraws/references/ and redraws/rejected/ under
  apps/game-client; scripts/reference_art.gd, room.gd, p10_sheet_smoke.gd and UID.
  Preserve dirty assets separately, then restore source directories exactly from
  8510ed33aea979eff591f2155640c9c1d3db0efb. Client edits limited to explicit asset
  routing and correct frame-duration/loop semantics. No generated-candidate
  activation until independent review and Lead acceptance.
  Owner additionally authorized deterministic Pillow packing: this Peer owns
  tools/assets/pack_p10_atlas.py and test_pack_p10_atlas.py, with temporary test
  fixtures only; the Art Peer invokes it on their exclusively owned candidates.
- Art Peer: only new apps/game-client/assets/pets/redraws/candidates/
  MaVuongHutMau/ and NuVuongBachCot/ PNGs, prompts and candidate metadata.
  No code, source or reference writes.
- Reviewer: read-only exact-candidate review, no authored implementation.
  Human retains final acceptance and material art decisions.

## References and provenance

PRIMARY STYLE REFERENCES: existing DaoThienDuong and DocDangNu atlases.
Preserve their PNG bytes exactly. Style-reference approval does not assert
their own geometry/timing meets the new output contract.

MaVuongHutMau and NuVuongBachCot are failed anchor candidates, not references.
Correct these two first as a bounded pilot; no 150-species batch is assigned.
Use actual anchor files or byte-identical preserved copies.

Each original APK sprite supplies identity only: silhouette, anatomy,
costume/accessories, weapon, palette and personality. Read original sprites
from the pinned source commit, not failed redraws. Source manifest and hashes
stay unchanged. Redraws live outside apk84/; never rewrite source hashes to
bless replacement pixels.

## Artifact and geometry

- One transparent RGBA PNG per species, exactly 1124×1405.
- Four columns × five rows, 281×281 cells, 20 distinct occupied frames.
- Every alpha > 0 pixel, including faint effects, stays in cell-local
  x/y [22,259), centered 237×237 safe area: 22 fully transparent pixels per side.
- Typical silhouette height 55–72% of 281px, smaller when wide.
  Containment takes priority over size; stable pivot and readable game scale.
- Same head/body/horns/wings/hair/clothing, weapon/accessory counts,
  palette and facial design throughout all 20 frames.

## Animation

| Row | Frames 1 → 4 | Playback |
|---|---|---|
| 1 idle | Four subtle breathing/wing/hair/tail/hover changes, seamless 4→1 | Loop |
| 2 movement | Four loopable locomotion poses; only locomotion row | Loop |
| 3 basic attack | Anticipation, wind-up, forward impact, recovery | One-shot |
| 4 signature skill | Gather, form, release, dissipate | One-shot |
| 5 hurt/down | Stagger, weakened, collapse, fully down, non-gory | One-shot |

Basic impact faces opponent, preferably screen-right. Compact directional
effect usually ≤20–25% of safe area; signature effect usually ≤35–40%, all
in-cell. These are composition guides, not exceptions to exact alpha bounds.
No cross-cell effects, oversized auras or upright stun replacing fully down.
Only rows 1–2 loop.

## Pixel style

Match approved anchors' pixel-cluster detail density: dark colored pixel
outlines, crisp larger clusters, clustered shadows, controlled saturation,
compact highlights. No smooth anime/vector/painting style, blur, antialiasing,
bloom, noisy microtexture or full-silhouette glow. Five-star species may have
richer detail/effects, never larger sprites or cell-spanning effects.
No text, watermark, borders or background.

## Validation and acceptance

1. Mechanical: actual RGBA PNG, dimensions, transparency, 20 occupied/distinct
   cells, all alpha > 0 pixels within [22,259). Report per-cell bounds and
   scale observations. Owner explicitly authorized Python/Pillow deterministic
   nearest-neighbor packing after imagegen missed exact dimensions. Preserve raw
   attempts unchanged; record 20 complete source rectangles, local pivots and a
   common uniform scale on the exact canvas. Do not crop away visible parts or
   erase alpha to fake a pass. Packing cannot repair inconsistent anatomy,
   weapons, row meaning or style; those require artistic correction/re-review.
2. Visual: both anchors plus original identity; row meaning, forward impact,
   consistency, pivot/scale, compact effects, pixel style and loop/one-shot
   sequences. Mechanical success alone is insufficient; repair/re-review failures.
3. Source: 304 original PNG hashes match original manifest; strict catalog and
   catalog tests pass after separation.
4. Client: correct reference/source routing and duration-aware playback;
   candidate idle/run loop, attack/magic/die hold final frame.
   No server rules/save IDs change or unreviewed candidate activation.
5. Independent exact-hash review and explicit Lead dispositions precede Human
   pilot acceptance. No P10 gameplay or phase-completion claim.

## Retained gates

152 identities, 1★–5★ model and 17 disabled Special recipes unchanged.
DaoThienDuong is 5★ Special, not 6★. No runtime merge, invented stats/Elements/
skills or save migration. P10-O01–O08 remain in P10-readiness.md.

## Owner size direction — 2026-10-08

Owner selected tier-based apparent size with species exceptions (option A):
1–3★ share a similar body presence, 4★ slightly larger, 5★ clearly larger,
and Special 5★ receive species-appropriate presence and personality.
This supersedes “never larger sprites” above for display size; atlas cell
geometry and alpha containment remain required. Exact ratios, pivots and
battle layout must be trialed before runtime approval. No candidate activation
or source/anchor pixel changes are authorized by this sizing decision.
See redraw-kit/review-20261008/review.md for all 48 late-game species notes.

## Owner anchor correction — 2026-10-08

DocDangNu and DaoThienDuong are style bases, not exempt finished assets.
Owner explicitly requests review and repair when needed in this art review
scope. This supersedes the earlier immutable-anchor restriction for new
versioned repair candidates. Preserve historical references and pinned APK
sources; author repairs in separate folders and review before selection.
Owner also approved heavy/brutal direction A for MaVuongHutMau.

## Owner closure — 2026-10-11

Owner confirmed approval of all 152 current atlases and requested completion.
All selected versions are locked by path and SHA-256 in
`redraw-kit/owner-atlas-selection.json`; each is `owner_approved_done`.
Final inventory: `redraw-kit/completion-20261011/done.json`.
152/152 redraw art completed; the late-game subset is 48/48 owner-approved.
Historical rejected attempts, comments and independent reviews remain audit
history and do not replace this final owner disposition. Any future pixel
change requires a new hash and renewed approval.

## Owner160-art closure —2026-10-21

Owner approved the final0147 APK-faithful registered preview and all remaining art, then requested review/closure.160/160mechanical checks and68unit tests pass;304original PNG hashes preserved. Current acceptance authority is `redraw-kit/owner-atlas-selection-160.json`, including0138attempt05,0141attempt03,0147attempt13 and eight authored extensions. The historical152manifest/IDs/source PNGs remain frozen.

The approved0147 bundle includes explicit manual contact origins and one displayfactor reaching190px; native140.25px is not density/registration-equivalent to prior170px. Display profiles remain unactivated. ClosureART-I01–06 transfer runtime mapping,origin/timing consumption,camera/UI/1v3FX,memory/mobile/50CCU checks to P01/P02/P03/P05/P06/P09. No art approval implies gameplay fidelity or runtime performance certification. No push/restart/DB mutation is authorized by this art closure.
