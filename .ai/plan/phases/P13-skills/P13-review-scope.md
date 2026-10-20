# P13 — Design completion and owner review

Date: 2026-10-13. Status: IN PREPARATION, owner acceptance pending.

The owner delegated completion choices and requested a web acceptance interface
before handoff: “Complete phase này theo bạn thấy là phù hợp và trước khi handoff
đưa cho mình 1 bản nghiệm thu để mình duyệt, góp ý và từ chối,... trên web ui”.
This authorizes autonomous design preparation and its local review tool. The
owner reviews the concrete result; no additional intermediate design approval
is required. P13's master exit is a design gate; gameplay integration is P02/P07.

## Outcome and boundaries

Produce an evidence-backed P13 candidate: elemental matrix; skills, status and
resource rules; all 160 native pools (152 frozen + 8 authored); inheritance/learning contracts; scenarios,
review findings and downstream gates. Preserve accepted P10/P11 decisions.
New choices are proposed Phimond design, never source facts or owner-approved
decisions. Phase closure and handoff wait for owner review.

The review UI runs on loopback in this workspace, matching the existing P10
review workflow. It saves revision-bound comments and dispositions to local
files, so the next iteration can read them. No hosted deployment is needed.

## Ownership and execution

- Lead: all P13 spec/content/catalog/review-package files and verification.
- Source worker: only `P13-source-audit.md` and `evidence/source-audit.json`.
- UI worker: only `tools/p13_review/` (server, buildless HTML/CSS/JS, tests).
- Final reviewer: read-only review of exact deliverables and evidence.
- Preserve unrelated working-tree changes. No master/P10/P11/runtime edits.

## Work plan

1. Audit local APK3.2/XAPK8.4/JAR evidence with hashes and version boundaries.
2. Author a coherent candidate against master P13-R01–R06 and P11 interfaces.
3. Generate 160 explicit native pools; verify references, role coverage,
   inheritance eligibility, six-slot sample builds, and source identity.
4. Build local review UI with search, rules, chart, skills, species, scenarios,
   per-decision feedback, persisted revision checks, and export.
5. Test persistence, stale versions, invalid approval and catalog invariants;
   inspect UI in browser. Record exact checks and remaining balance limitations.
6. Present candidate for owner acceptance. Keep handoff/phase closure pending.

## Review package interface

`review-package.json` contains `phase`, `revision`, `title`, `status`, `summary`,
`decisions[]` (id, category, title, summary, rationale, alternatives[],
acceptance[], evidence[], impact), `elements[]` (id,name,color), `chart`
(attacker element -> defender -> multiplier), `skills[]` (id,name,element,
kind,target,mp,cooldown,learn_level,description,inheritance,provenance),
`species[]` (id,name,race,star,element,roles[],native_skills[],sample_build[],
rationale), `scenarios[]` (id,title,mode,given,when,then,verification),
`sources[]` (id,title,path,note), `checks[]` (name,status,detail).
Additional content fields are permitted and should be displayed when useful.

The server calculates a package content hash. A feedback submission includes
that hash and a feedback version, preventing silent overwrite by stale tabs.
Feedback statuses: pending/approved/changes_requested/rejected. Overall owner
verdict: draft/approved/changes_requested/rejected. Overall approval requires all
decision cards approved. A card edit invalidates a previous overall submission.
No automated test writes into real owner-feedback storage.

## Acceptance of the review tool

- Read, filter and inspect all content on desktop and narrow screens.
- Save comments and each disposition; reload/restart preserves them.
- Reject stale package/version writes and invalid/partial overall approval.
- Export includes package hash, per-card feedback and overall verdict.
- UI never turns tests or agent choices into human approval.
- Keep review server available for the user's manual acceptance.
