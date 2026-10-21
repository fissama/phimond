# P10 provenance diagnostics milestone — 2026-09-30

Status: provenance/source separation/client/checker subsets technically accepted;
two-species art pilot and packing tool in progress. Human acceptance pending.
Base: `8510ed33aea979eff591f2155640c9c1d3db0efb` (also HEAD when Docs checked).
This milestone does not resolve dirty-art provenance, deliver P10 gameplay,
select a visual direction, authorize migration, or close P10.

## Current owner update and dispositions — 2026-09-30

The owner confirmed no other editor is active and approved DaoThienDuong and
DocDangNu as PRIMARY STYLE REFERENCES. MaVuongHutMau and NuVuongBachCot are
failed candidates requiring correction. The exact pixel-sprite output contract,
updated disjoint ownership and pilot acceptance gates now live in
[P10-redraw-plan.md](P10-redraw-plan.md). It supersedes the former redraw draft.
The original 20 dirty/untracked files were copied byte-identically into
`/tmp/phimond-p10-dirty-backup-20260930/` before assigning writes.

Lead accepted the following exact provenance-tool candidate after independent
review by `/root/p10_review`, who authored neither file:

- `tools/content/p10_provenance.py` SHA256
  `c9ea71fd62d3f2c034019db15e0b3f4768251e0838888c1b47016abc0a29db4c`
- `tools/content/test_p10_provenance.py` SHA256
  `4e00f6769695d07646d27282d2e800a5eff7ddf722ed00882f2fbbfa98a506be`

Writer, Lead and Reviewer each ran the 16 hermetic tests successfully. Reviewer
also checked inherited Git-environment isolation and committed manifest symlink
rejection in temporary fixtures: both passed. No blocking findings. Clean exit 0
certifies only manifest-listed PNG provenance and manifest agreement, not
frames.tres, Godot behavior, visual correctness or art approval.

The documentation candidate was accepted for review; its independent review had
no blockers. The optional PNG-only clarification is adopted above. New artwork
remains unaccepted. Source separation, client playback and atlas-checker work completed
their own exact-candidate review as recorded below. No push/merge/deploy or phase
closure is implied.

### Source/client/checker disposition

`/root/p10_provenance` delivered the candidate; independent `/root/p10_review`
found no blockers; Lead technically accepted this subset. Exact reviewed hashes:

| File | SHA256 |
|---|---|
| `tools/assets/check_p10_atlas.py` | `d7666e8d8ff8acaeff2e237969bb792cf12e51c2708a0b91c9b80ce21f142487` |
| `tools/assets/test_check_p10_atlas.py` | `863917fb6986babffe9c7a2dc300ea7af72c94020e94e6335081f277ddc78caa` |
| `apps/game-client/scripts/reference_art.gd` | `71d7c87389c7dec2e76b472a430f74d4b8de62b4635576189aca0224c2bdce3f` |
| `apps/game-client/scripts/room.gd` | `423afdc9775550e59ad75f7b9eecabece2dd8199ed216f241009eec6d50a3f4f` |
| `apps/game-client/scripts/p10_sheet_smoke.gd` | `a4f28587e831d77ea3950d501ca950cab2108d9e248b46156143a59c2d3a5d9b` |

Lead and Reviewer independently verified the 12 APK source files exactly match
base and eight separated PNGs exactly match the preserved dirty snapshot. The
304 source PNGs and original manifest now pass strict validation in this checkout;
the initial failure below is resolved by separation, not weakened validation.

Lead and Reviewer each ran 34 Python tests (9 catalog, 16 provenance, 9 atlas)
successfully. Each also ran the isolated Godot smoke and saw its PASS marker,
exit 0 and no script errors. Reviewer verified fixture script/resource bytes
match the candidate. It covers reference/source routing, unequal frame durations,
loop versus final-frame clamp, attack onset after 1000 seconds and death/reset.
The working server/editor was not restarted or deployed.

Approved references live in `assets/pets/redraws/references/`; failed prior
drafts in `redraws/rejected/`; candidates stay inactive. Reference PNGs retain
1122×1402 geometry and are style guidance, not compliant production atlases.
The existing battle renderer still chooses attack for skill_cast; direct magic
playback is tested, but new skill-event presentation is outside this milestone.

### Art and packing status

Owner explicitly authorized Python/Pillow nearest-neighbor packing. Preserve
raw attempts, record source rectangles/pivots/common scale, and review the packed
result independently. Geometry cannot waive character or animation requirements.
MaVuongHutMau attempts 01/02 were rejected for geometry; independent visual review
also rejected attempt 02 for disappearing weapons, weak movement cadence and
excessively fine detail. Lead requested targeted repair. Both attempts remain
evidence, not accepted art. NuVuongBachCot and the packer await their own review.

## Initial diagnostic scope (historical, superseded where noted above)

The accepted technical route adds only a read-only provenance CLI and hermetic
unit tests, plus this evidence document. Existing strict catalog validation
remains unchanged. User-authorized continuation excludes push, merge and deploy.
No asset restoration/import/generation, runtime restart, DB mutation, save
rewrite, or existing-file edits belong to this milestone.

Follow [local protocol](../../../../docs/WORKSPACE_PROTOCOL.md), its shared
protocol, [active scope](../../../ACTIVE.md), [readiness](P10-readiness.md),
[data contract](P10-data-contract.md) and [authoring policy](../../../../data/p10/README.md).
The readiness register remains the authority for P10-O01–O08; this document
adds evidence and bounded milestone criteria, not a competing gameplay register.

| Owner | Brief / exclusive scope |
|---|---|
| Code Peer | New `tools/content/p10_provenance.py` and `tools/content/test_p10_provenance.py`; read-only CLI, isolated fixtures and negative tests |
| Docs Peer | This new document only; independently reconcile evidence and preserve every existing file |
| Reviewer | Read-only review of the exact candidate hashes supplied by Lead; findings and limitations, no repairs |
| Lead | Scope reservation, candidate integration and verification, explicit finding dispositions and technical acceptance; Human retains final acceptance and art approval |

## Initial independently observed checkout evidence (before source separation)

Docs used read-only Git blob reads and Python SHA-256 comparisons on 2026-09-30:

- `apps/game-client/assets/pets/apk84/manifest.json` is byte-identical to base.
- All **304 committed PNG blobs** (152 portraits plus 152 atlases) match their
  respective hashes in that unchanged manifest.
- Exactly **8 working PNGs** differ from those expected hashes; 296 match.
- The four accompanying `frames.tres` resources and two client scripts also
  differ from base. They are reserved work, outside the diagnostics candidate.
- All **20 protected files** matched Lead's preservation hashes at Docs' check:
  `/tmp/phimond-p10-preservation-20260930.json`. Lead must recheck at integration;
  this local snapshot path is session evidence, not a permanent repository input.
- The raw source, canonical authoring catalogs and strict validator have no
  tracked diff against base. All **17 Special recipes remain disabled**.

Exact changed PNG paths:

```text
apps/game-client/assets/pets/apk84/DaoThienDuong/portrait.png
apps/game-client/assets/pets/apk84/DaoThienDuong/sprites.png
apps/game-client/assets/pets/apk84/DocDangNu/portrait.png
apps/game-client/assets/pets/apk84/DocDangNu/sprites.png
apps/game-client/assets/pets/apk84/MaVuongHutMau/portrait.png
apps/game-client/assets/pets/apk84/MaVuongHutMau/sprites.png
apps/game-client/assets/pets/apk84/NuVuongBachCot/portrait.png
apps/game-client/assets/pets/apk84/NuVuongBachCot/sprites.png
```

Reserved alongside them: `frames.tres` in each of these four directories;
`apps/game-client/scripts/reference_art.gd` and `room.gd`; untracked
[P10-redraw-plan.md](P10-redraw-plan.md), `.serena/.gitignore`,
`.serena/project.yml`, `apps/game-client/scripts/p10_sheet_smoke.gd` and its
`.uid`, and `docs/WORKSPACE_PROTOCOL.md`. Their author/creator is **unknown**;
Lead's reservation is not authorship or approval. Creator ownership and intended
art disposition still require clarification before any overlapping write.

Current strict check, run by Docs without `--write`:

```text
rtk proxy python3 tools/content/p10_catalog.py
exit 1
ValueError: asset hash changed: NuVuongBachCot/portrait.png
```

This is the current expected failure on the dirty checkout, not a waiver.
Manifest changes to bless replacement pixels would destroy the distinction
between original extraction and replacement art. Technical recommendation:
retain immutable APK evidence and place any separately approved visual variant
in a distinct asset/manifest layer. No variant design or visual style is selected
by that recommendation, and no relocation/restoration is authorized here.

## Conflicts in the preserved former redraw draft

The former draft is preserved in the backup above; the active plan has now been
reconciled to the owner contract. These were its unaccepted statements:

- **Star/class:** it labels DaoThienDuong 6★; the source record is bird,
  **5★ Special**. Special is a class, not a sixth Star. Its roster/batch totals
  also need reconciliation against the accepted 152 identities and 17 Specials.
- **Runtime merge:** its proposed parallel P10-MERGE would cross P10-O05/O08.
  Stats, Elements and native skills are unresolved; a merge cannot establish
  correct stats. Explicit mapping, configured content, copied-save tests,
  version gates and rollback precede any runtime switch. Legacy14 remains active.
- **Grid:** four columns by five rows of 281px cells require **1124×1405**,
  not 1122×1402. Its front/three-quarter idle rows also conflict with its
  separate list of `idle`, `run`, `attack`, `magic`, `die` states.
- **Animation semantics:** blanket four-frame loops and stun-to-die mapping
  cannot be claimed as preserved source semantics. Accepted extraction records
  discrete frame durations and loop flags (760 clips, 1,241 timed entries).
  The reserved `sheet_texture()` change uses equal frame timing and modulo
  looping; this is a review concern, not approved source equivalence. Art approval
  and a reviewed action/timing contract are needed before replacing resources.

The draft's anchor approval, estimates and runtime correctness claims are not
confirmed by this provenance check. No draft edits or image generation occurred.

## Initial diagnostics contract and milestone criteria

1. CLI reads a resolved committed base and working files without modifying them.
   JSON on stdout includes the resolved base, counts, status and affected paths.
   Exit **0** means clean against valid source; **1** means working drift with
   valid source; **2** means invalid/unverifiable source or input. Source failure
   must not be downgraded to ordinary working drift.
2. Hermetic fixtures cover clean source/working state, working drift and invalid
   source/input, with deterministic reports. Tests must use temporary repositories
   and avoid the real checkout, DB, Godot import and external services.
3. Keep `p10_catalog.py` and its strict gate unchanged. The new diagnostic is
   additive; exit 1 on this dirty checkout does not make strict validation pass.
4. Preserve every reserved byte, the original manifest and source evidence.
   No runtime data/server/client edits or save migration; all disabled branches
   remain disabled, including Special recipes/reinforcement and unadopted items.
5. Lead verifies the exact three-file candidate, protected hashes and focused
   test results; an independent reviewer checks that same candidate read-only.
   Unresolved critical findings block acceptance. Review and final dispositions
   are **pending**, with no inferred PASS from a completion message.
6. Human acceptance of this preparation milestone is separate from any later art
   decision or phase delivery. No commit/push/merge/deploy is part of this brief.

## Initial verification provenance and blockers (historical snapshot)

| Evidence | Scope and result |
|---|---|
| Docs' current-session blob/hash checks | 304/304 base PNGs match manifest; 8 working PNG mismatches; 20/20 protected hashes intact at check |
| Docs' current-session strict catalog command | Exit 1 on dirty checkout, first mismatch `NuVuongBachCot/portrait.png` |
| Lead-reported current-session isolated baseline check | Temporary archive of exact base: catalog exit 0; existing `test_p10_catalog.py` 9/9 passed; not a dirty-checkout pass and not independently rerun by Docs |
| [2026-09-28 verification](P10-verification.md) | Historical importer, Godot, canonical gate, build and catalog results only; not current candidate evidence |
| New provenance CLI/unit suite and exact-candidate review | Results pending Lead verification/reviewer; no final test count or approval asserted here |

Concrete blockers: creator ownership and approval for reserved art remain unknown;
the strict working catalog gate fails; the draft conflicts above remain unresolved;
new tooling verification and independent review remain pending. P10-O01–O08 retain
their existing source-verification/later-phase owners. None is resolved by the
fact that original committed blobs are valid. No runtime or gameplay test was
performed by Docs, and no historical result is promoted to current certification.
