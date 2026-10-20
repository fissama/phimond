# P13 — Verification of review candidate

Date: 2026-10-13. Status: **READY FOR OWNER REVIEW**, phase acceptance pending.
Initial v1 SHA256: `fd618e564db82122a93fb6953c0ae2d801332accc36e12d2e85f33925dc61be5`.
No handoff/closure/commit/push yet: owner requested the web acceptance first.

## V1 checks (historical)

| Command / check | Result | Meaning |
|---|---|---|
| `rtk proxy tools/.cache/asset-venv/bin/python tools/content/p13_source_audit.py` | PASS |60+60 records,13 changed records,8 direct JAR probes found |
| `rtk proxy python3 tools/content/p13_design.py` | PASS |66 skills,152 species,18 decisions,24 scenarios; pool size5–15 |
| `rtk proxy python3 -m unittest discover -s tools/content -p 'test_*.py'` |32 passed | Includes7 new P13 exact arithmetic/catalog tests and25 existing content tests |
| `rtk proxy python3 -m unittest discover -s tools/p13_review -p 'test_*.py'` |8 passed | Restart persistence, stale tab/package, invalid approval, verdict reset/history, reject, malformed feedback/origin, path access |
| `rtk proxy node --check tools/p13_review/app.js` | PASS | JS syntax |
| `rtk proxy sh tools/check.sh` | PASS | Go tests/vet,6 Godot checks,7 harness tests,3 companion tests and typecheck |
| `rtk proxy go build -o /tmp/phimond-server ./cmd/server` (game-server cwd) | PASS | Fresh server build; Go source unchanged from HEAD |
| `rtk proxy go test -race ./... -count=1` (game-server cwd) | PASS | Fresh race suite;4 packages with tests, remaining packages report no test files |
| Godot `--headless --path apps/game-client --script res://scripts/min_smoke.gd` | PASS | Auth/catalog/connection/movement via current game server |
| `rtk proxy curl -sf http://127.0.0.1:8090/healthz` | HTTP200 | `{"service":"Phimond","status":"ok"}` |
| `rtk proxy git diff --check` | PASS | Tracked working-tree whitespace; new artifacts separately inspected |
| `rtk git fetch origin`; `HEAD...origin/main` |0/0 | HEAD9f57756d matches remote; preserved dirty working tree |

P13 tests:15 passed,0 skipped,0 observed flaky. Full Python content/review runs:
40 passed (including25 existing). Godot contact_check and layout_audit produced
PASS lines in canonical run. reference_menus_check reports its own
REFERENCE_MENUS_CHECK marker; it is not relabeled as a nonexistent PASS line.
Existing client art/room edits precede this task; Godot checks use that working
tree, not a claim that a clean HEAD client was run. P13 changes do not touch runtime.

## V1 browser QA (historical)

Local QA endpoint8134 used `/tmp/phimond-p13-browser-qa-feedback`, never real owner
storage. Expanded a decision, requested changes, entered a test comment, saved
and confirmed saved comment after reload. During later candidate edits an old
tab retained its prior hash; stale write correctly failed without overwriting
the new revision. A fresh tab on8133 loaded the final exact hash with all18pending.

Final candidate read-only browser checks:36-cell chart, source-ID search for
HoaDa→Hóa đá, species search species_0103→Chim Đại Phì; narrow390×844 viewport
with no body horizontal overflow, horizontally scrollable chart/navigation.
Browser logs inspected: no JS errors/warnings at inspected checkpoint. Final
viewport reset. Screenshots: `evidence/review-desktop.jpg`, `review-mobile.jpg`.
Main8133 tab kept open as deliverable. QA8134 process/tab stopped.

Real GET `/api/review` confirmed package hash equals file hash, feedback version0,
all dispositions pending, zero real feedback files. No synthetic owner approval.

## V1 manual validation services (historical)

- Review: `127.0.0.1:8133`, PID18938, retained local tool session. Feedback created
  on save in `review/responses/<sha256>.json` (gitignored mutable authoring state).
- Game: `127.0.0.1:8090`, PID18776, `GAME_METRICS=1`, `/tmp/p00-serve.log`.
  Prior log retained at `/tmp/p00-serve-before-p13-20261013.log` if present.
- Godot editor debug6007: no listener at validation checkpoint.
- Working tree intentionally contains prior P10/P12/client work and new uncommitted
  P13 artifacts. No blanket stage/clean/reset/pull performed.

PIDs are this validation snapshot, not persisted service guarantees. The review
server reads candidate bytes per request, so content edits require page reload
and start a separate hash-bound review.

## Still pending

Owner feedback and phase acceptance. Numeric tuning, actual PvE1v3/party/PvP kit
balance, cost/retraining economy, canonical save migration, multi-owner timing
and50CCU performance require downstream integration. Static consistency and
baseline runtime smokes do not certify those outcomes.

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
