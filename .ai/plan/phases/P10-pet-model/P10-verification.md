# P10 data/asset verification — 2026-09-28

Scope: accepted 152-Species identity/art package and confirmed design amendments.
**P10 remains in design review; this is not a phase-completion report.**

## Source extraction

- Exact supplied XAPK SHA-256 checked by `tools/assets/import_p10_roster.py`.
- PokeModelData field order and Race/Star enum defaults decoded from metadata v31.
- 152 unique records; 24,412/24,412 serialized bytes consumed.
- Approved Race × Star matrix matched exactly; 135 normal + 17 Special.
- All 17 Special pairs resolve to normal parents at the same Star; main Race matches target.
- All 152 source portrait references resolve to Sprite objects.
- 152 source actor mappings; one explicit spelling alias (`QuaiVatNhamThach`).
- 760 source animation clips and 1,241 timed frame entries decoded from their
  discrete SpriteRenderer curves. Source loop flags retained. No guessed frame spacing.
- Source animation pixels are compared with their packed image regions during import.
- Import rerun succeeds; generated data/art remain sourced from the same locked XAPK.

## Checks executed

| Check | Result |
|---|---|
| Offline importer, run twice after adding asset support | PASS: 152 / 760 / 1,241 |
| Independent expected matrix, parent class/Star and asset-path checks | PASS |
| Godot headless editor import | Exit 0; no ERROR/SCRIPT ERROR/Parse Error diagnostics |
| Godot `tools/assets/check_p10_assets.gd` | PASS: all portraits/resources, five clips each, frame counts, loop flags and exact durations |
| `sh tools/check.sh` | PASS: Go race suite/vet, five active Godot checks, seven load harness tests, three web tests and TypeScript |
| `go build -o /tmp/phimond-server ./cmd/server` | PASS |
| Visual spot check | Portrait and first idle frame reviewed for six species, including the spelling alias and surprising race assignments |

Canonical Go tests reused cache where valid. No gameplay formulas changed.
Opt-in live MySQL/load tests were not rerun for this identity/art/documentation import.
The legacy `layout_audit.gd` is not an active canonical check; its existing stale
scene assumptions remain recorded in ACTIVE.md.

## Reproduce

From the workspace root:

```sh
rtk proxy tools/.cache/asset-venv/bin/python tools/assets/import_p10_roster.py \
  '/path/Spirit Beast World 8.4 (1).xapk' .
rtk proxy apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
  --headless --editor --path apps/game-client --import
rtk proxy apps/game-client/.tools/Godot.app/Contents/MacOS/Godot \
  --headless --path apps/game-client --script "$PWD/tools/assets/check_p10_assets.gd"
rtk proxy sh tools/check.sh
```

## Boundaries and open work

- `roster_apk84.json` is the canonical source identity/art baseline. The server
  still loads legacy `species.json`; no arbitrary stats/Elements/native skills
  or save-ID migration were introduced.
- Extracted clips are valid Godot resources, not a port of Unity Animator
  transitions, renderer scaling or battle-event synchronization.
- Embedded catalog existence does not prove original server obtainability.
- Exact Special server costs/Plus/validation and stat formulas remain unverified.
- D14/D21/D22 was pending at import verification; the subsequent user review
  accepted option A (`grown_stat + inheritance_bonus`). Numeric formulas remain unresolved.
- All data/assets are local source exports; no source APK executable or credentials
  are included in the package.

## Full design audit and canonical ID normalization — 2026-09-28

This section records the later full-review pass, including all subsequent user
choices. The earlier import checks above describe their original scope.

| Check executed | Result |
|---|---|
| `python3 tools/content/p10_catalog.py` | PASS: 152 species, 8 selected item references, 17 disabled recipes; complete unique IDs, references, matrix, asset hashes/paths and deterministic generated data |
| `python3 -m unittest discover -s tools/content -p 'test_p10_catalog.py' -v` | PASS: 9 tests; corruption cases include duplicate IDs/JSON keys, missing mapping, localized ID, wrong Star/parent, missing asset and wrong source hash |
| Godot `tools/assets/check_p10_assets.gd` | PASS: 152 portraits/resources, 760 clips, 1,241 timed frames |
| `sh tools/check.sh` | Exit 0: Go race/vet (cached where valid), five client checks, seven harness tests, three web tests and TypeScript |
| `go build -o /tmp/phimond-server ./cmd/server` | Exit 0 |
| Local Markdown link check | PASS: 324 relative links in P10 documents resolve |
| `git diff --check` | PASS |
| Diff check for legacy runtime catalogs, raw APK catalog/evidence and original assets | Unchanged; ID normalization is additive, no live save rewrite |

Nine new tests cover **catalog tooling**, not future P10 gameplay. The 23
scenarios in P10-data-contract.md remain acceptance requirements for later
implementation. No balance formula, original Special server rule, mail gameplay
or 14→152 save migration was implemented or certified in this review.

New source-ID mapping and authoring catalogs are in `data/p10/`. See
P10-readiness.md for findings and owner/gate assignments; P10 remains a reviewed
design foundation rather than a delivered gameplay phase.
