# P10 redraw closure — 160 species — 2026-10-21

Status: **CLOSED — 160/160 redraw art owner-approved.** This closes the separate art scope, including eight authored extensions and the size-remedy review. P10 gameplay/design and runtime integration remain separate.

## Final acceptance and selected versions

Owner explicitly approved all current previews, then approved the APK-faithful Người Tuyết revision and requested final review/closure. Approval is recorded as chat confirmation, not invented web checkbox events.

- 149 unchanged versions from the original152 selection; updated0138 attempt05,0141 attempt03 and0147 attempt13; eight extension atlases0153–0160. Exactly160 unique IDs,160 distinct PNG hashes,3200 occupied/distinct per-atlas frames,800 action rows.
- **Current art authority:** [owner-atlas-selection-160.json](redraw-kit/owner-atlas-selection-160.json). Every species pins path/SHA256 and approval. Do not choose the largest attempt number:0147 attempt14 is rejected; accepted art is attempt13.
- [Final inventory](redraw-kit/completion-20261021/done.json), [owner confirmation](size-audit-20261019/remedy-20261020/owner-review-20261021.json). Historical152 selection/closure stay frozen for provenance; the160 manifest supersedes them for future art integration.
- Eight extensions remain **Phimond-authored**, with their existing stable IDs and P13 proposal mapping. No APK/JAR provenance is invented.
- All56 4★/5★ display previews accepted.55 profiles retain the reviewed snapshot;0147 uses its separate registered profile. PNG source pixel dimensions and stage presence are distinct.

## Final review and verification

- Fresh checker on160 selected PNGs:160PASS,0FAIL. RGBA1124×1405,4×5 cells281px,20 occupied and pixel-distinct frames each; allalpha>0 in cell-local[22,259). [Full mechanical evidence](redraw-kit/completion-20261021/mechanical.json).
- Fresh provenance against pinned commit8510ed33…:304/304 original PNGs intact,0modified/missing.160 prior review sources also unchanged. [Provenance](redraw-kit/completion-20261021/provenance.json), [source integrity](redraw-kit/completion-20261021/source-integrity.json).
- **68 unit tests passed:**33 asset/checker/packer/review-server;35 catalog/extension/provenance.0skipped,0flaky. Logs [assets](redraw-kit/completion-20261021/tests-assets.log), [content](redraw-kit/completion-20261021/tests-content.log). Asset fixtures emit non-failing ResourceWarnings while cleaning expected HTTP404/409 test responses; no failed assertion.
- Strict source catalogPASS. Extension reproducibility initially found stale cached `design_candidate.record.stable_id` and P13 reference hashes. Regenerated only the eight stable-ID metadata fields/reference hashes; no numeric/role/skill/recipe change. Extension check nowPASS; frozen152 source/registry/approved bytes preserved.
- Lead reviewed five final native-idle contact sheets covering all160 for selection/identity mistakes, reusing prior owner acceptance and existing per-atlas review evidence; this is not a claim to have newly watched every one of3200 poses in this closure turn. Contacts [01](redraw-kit/completion-20261021/contact-01.jpg), [02](redraw-kit/completion-20261021/contact-02.jpg), [03](redraw-kit/completion-20261021/contact-03.jpg), [04](redraw-kit/completion-20261021/contact-04.jpg), [05](redraw-kit/completion-20261021/contact-05.jpg).
- Earlier56-size review has96/192 filmstrips and35 browser row observations. The final0147 exact-hash independent static review and registered96/192 proof review found no mandatory visible art blocker; lead sampled five browser rows, idle/move repeat and one-shots hold4. [Independent review](size-audit-20261019/remedy-20261020/species_0147/attempt-13/independent-review.md).
- Earlier attempted expanded independent47-filmstrip pass was interrupted by usage limits and is not relabeled complete. The final0147 review tools subsequently succeeded. These histories remain explicit.

## Accepted limitations transferred to integration

These are runtime/integration gates, not unapproved art leftovers. Their presence must not be hidden by this closure.

| ID | Requirement / owner |
|---|---|
| ART-I01 | P01/P03 load exact160 mapping by stableID/hash. Never fall back to the first atlas for unmapped species. Current web manifest has only10 first-tier species; closure does not mean160 are live. |
| ART-I02 | P01/P02 consume the accepted56 profiles with species-specific mass; preserve one scale per species, pixel finish and low quadruped anatomy. Owner chose0144 as humanoid reference. |
| ART-I03 | **0147 native idle140.25px, prior170px.** Accepted190px stage presence uses factor1.3547237 and manual sole/body-contact origins in the [profile](size-audit-20261019/remedy-20261020/species_0147/art-redo-20261021/profile.json), SHAaac53dc3…. The PNG alone still has row/frame registration offsets; do not call it a drop-in170px atlas or density-equivalent replacement. P01/P02 must consume origins, or author/review a new registered packing.0156 likewise has explicit action-row origins in its profile. |
| ART-I04 | P01/P02 integrate duration-aware playback: only idle/move loop; basic/skill/hurt-down hold final. Re-check game timing/events; art preview timing is not a combat rule. |
| ART-I05 | P02/P05 check actual world/battle cameras, player comparison,1v3 neighbor/UI clearance and occlusion.0156 widefire impacts especially need real scene checks.0015/0069/0051/0126 face/body contrast must be checked on actual map backgrounds. |
| ART-I06 | P01/P05/P06/P09 own bounded texture loading/cache, filtering/mobile GPU budget and50CCU/latency certification. No runtime memory/performance approval follows from PNG checks. |

No original/approved PNG overwritten, no gameplay/DB/migration/stat change, no runtime activation. New art approval authority is the160 manifest; cached allocation-time `art.approved:false` in generated authoring records is not the current owner review ledger and is not runtime permission.

## Operational boundary

The art contract prohibits push/merge/deploy/game-server restart/DB mutation. No commit/push or game-server rebuild/Go race/Godot runtime smoke is claimed for this art-only closure. Unrelated dirty/untracked work was preserved. Review server remains PID66822 at127.0.0.1:8127, log`/tmp/p10-roster-size-review.log`; latest reviewed files served directly.

The named `phimond-phase-handoff` skill is absent from the catalog and local skill folders. [Handoff](handoff-redraw-160-20261021.md) therefore uses AGENTS.md's mandatory format directly; no invocation is claimed.
