# P13 — Candidate self-review, 2026-10-13

Initial v1 candidate: `P13-candidate-v1-20261013`, exact byte SHA256 of review-package.json:
`fd618e564db82122a93fb6953c0ae2d801332accc36e12d2e85f33925dc61be5`.
Reviewer: lead agent, self-review only. Independent workers could not start
because of account usage limits; no independent peer-review verdict is claimed.
Owner acceptance PENDING. Handoff/closure not generated.

## Actually delivered

- APK3.2 and8.4 serialized catalogs:60 records each, full byte-consumption proof,
  same IDs and13 different requirement records. JAR original-byte probes corroborate
  trainer/forget/group-skill/signature text; historical server formulas unresolved.
- Proposed18 decision groups,36-cell Element chart,66 concrete skills,152 explicit
  native pools and illustrative builds of up to6 skills. Existing P10/P11 identity/stats untouched.
- Behavioral semantics for learning/rank/cost, exact numbers, target/action validation,
  CD/round timing, stack/control grace, recovery, effects, save/replay and downstream.
-24 scenario contracts tagged by mode and planned verification method.
- Local review website with per-group approve/change/reject/comment, progress,
  filters, source/spec readers, overall submission and JSON export.
- Atomic/hash/version-bound owner feedback. Browser QA storage separate from owner
  storage; real candidate starts18pending, feedback version0 and zero feedback files.

## Findings and disposition

| ID | Finding | Disposition / owner |
|---|---|---|
| F01 | Raw APK Mana/Dame encoding/server interpretation unverified | Keep raw source, do not copy numbers as certified; candidate numbers clearly authored. Historical verification remains open. |
| F02 | Source passive regen/rebirth/MP return, instant death and petrify immunity conflict with resource/counterplay direction | Explicit candidate adaptations in D11/D14; owner may reject. No passive behavior inferred from Race. |
| F03 | Initial examples for two duplicate-stat birds shared a6-slot build despite different pools | Fixed: include own-Element physical attack in primary build. Validator now requires duplicate-stat pools AND sample builds differ. |
| F04 | Initial pet auto text omitted control/buff/cleanse triggers | Fixed: default valid heal→cleanse→control→buff→AoE→single→basic; per-skill channel exposed. |
| F05 | Source maxHP impairment briefs do not define safe current/maxHP semantics | Proposed frailty ATK/MAG impairment instead, clearly called an adaptation. Owner must judge identity fit; P11 stats unchanged. |
| F06 | Static pool functions cannot certify role utility, homogenization, stall or control pressure | P02/P07 live kit audit required. No measured balance claim. Costs/time-to-useful measured by P15/P19. |
| F07 | Runtime content/save activation could be mistakenly inferred from design completeness | All artifacts label candidate/no runtime. Versioning and legacy migration gates remain explicit. |

## Requirement coverage

R01/R01a/R01b: D02–D04,D15,D16; basic separate, newborn0, preserved skills usable
atLv1, pool counts5–15. R02: D05–D14; chart, status, damage, hit/crit, duration,
stack, cleanse and UI semantics. R03: D09/D14/D16 + mode-tagged scenarios. R04:
D04/D17; current-only deterministic inheritance and per-skill whitelist. R05:
D10–D14/D18; control/reaction/MP loops and downstream proof. R06: D04/D15;
152 native pools carry named Species accents while preserving P11 roles/Element.

## Technical acceptance

Prepared for owner review, not phase accepted. No runtime/DB/save changes; UI
feedback is the only new mutable authoring state. Game checks prove baseline
regression only. Concrete evidence and reproduction: P13-verification.md.

Important review choices: training prices and rank economics; Element multipliers;
one-action hard control/grace; paid active recovery; no guaranteed resurrection or
instant-death attack; native learning vs inheritance restrictions; scope of common
skills. These are intentionally surfaced as rejectable cards rather than hidden
implementation assumptions. Subsequent owner feedback creates a versioned revision.

## V2 — owner feedback incorporated, 2026-10-13

Current candidate `P13-candidate-v2-20261013`, SHA256 `cc4a060abd88593fdaaae4874916979cadcad95bbd6fd0978149d06a94b07dbf`.
Owner v1 feedback v8 requested changes;17approved/1pending. Archived original
feedback and package under evidence; only unchanged15decision objects retain
approval. D02/D04/D15 pending; v2 draft, no agent approval or handoff.

Updated6slot rationale and7 species-exclusive authored Special signatures;
73skills/152species/18groups/28scenarios. Native pools5–15; frozen P11 intact.
V2 retains existing numbers and protocols outside these explicit additions.
Signature combo semantics use existing status/buff types; static proof does not
measure combat balance. Review response details: P13-owner-feedback-v2.md.

Verification rerun:34content Python tests (9P13)+8reviewserver tests=42passed,
0skipped/flaky observed. New tests prove7owners, bothStars, all6Elements,
no inheritance,≤6builds, fixedrank1, and reject a signature leaked into another
pool. Generator validation, JS syntax, canonical tools/check.sh, fresh build,
fresh Go race -count=1, git diff --check passed. Fetch succeeded.

Review8133 PID39254; game8090 rebuilt/restarted PID39267, metrics1, health200,
log /tmp/p00-serve.log (previous log /tmp/p00-serve-before-p13-v2-20261013.log).
Source/runtime unchanged; prior dirty workspace preserved, no commit/push yet.
Browser loaded v2:15/18approved,3pending,73skill/28scenario navigation;
owner notes retained. New source-reader document added. Manual validation
continues on v2 before closing phase.

## Current v3 — tiers, taxonomy and Race audit

Revision P13-candidate-v3-20261013; current exact SHA256 `35f0159baccd379ce120474e68ff2795ebd6bae677998f8f24f69466b96d6107`.
95skills/152species/18groups/32scenarios, pool6–22, samplebuilds≤6.
Separate28APK AoE tiers and2groupheal; strong tier never replaces light.
7Special signatures keep all oldfields/behavior/numbers; only target/effect
classification metadata added. Source artifacts unchanged; AoE source names/
target/channel observed, candidate costs/power/gates authored. P11 frozen.

All8Race have≥2primaryphysical and≥2primarymagic; explicit single/lightAoE
kit checks pass. This is metadata/coverage, not 50:50 or balanced winrate.
Normal star gaps including Beast1/5 lack magic exposed; no unauthorizedP11
role/stat edits. Race audit and revision detail: P13-owner-feedback-v3.md.

Executed:40content Python tests (15P13)+8reviewserver=48pass,0skip/flaky
observed. Added regression for missinglight, monotonicMP/power, separateIDs,
current-tier inheritance, primarycaster depletion, typed single/AoE/effect,
cheap farming arithmetic. Fresh generator, JSsyntax, tools/check.sh, Go build,
race -count=1, live min_smoke andhealth200, gitfetch/diffcheck passed.

BrowserQA: filter AoE+physical+pure damage shows exactly4Cànquét tiers;
comparison table correct. RaceThú+magic filter shows3species including2
primarycasters; race table12physical/2magic andNormal1/5 gaps.390×844body375
with no body horizontal overflow; table scrollable. Screenshots
evidence/review-v3-tiers.jpg andreview-v3-mobile.jpg, viewportreset.

Owner tabv2 had unsaved draft (D02approved/notes cleared). Kepttab andsnapshot
evidence/owner-unsaved-v2-draft.json, carried only unchanged groups/notes into
v3 draft withprovenance/history.10unchanged savedapprovals +D02browserdraft
selection now show11/18approved;7groupspending. No owner final submission
or phase acceptance inferred. v1/v2hash-bound responses remain unchanged.

Review8133PID43469, game8090PID43529, metrics1, health200, log/tmp/p00-serve.log;
oldlog/tmp/p00-serve-before-p13-v3-20261013.log. Prior dirty changes preserved.
No handoff/closure/commit/push yet; owner review and downstreamcombat balance
pending. Numeric AoE/farm examples assume hits and do not certify clear speed.
