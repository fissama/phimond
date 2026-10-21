Phase: P10 — 152-species sprite redraw art closure

Implemented:
- 152/152 exact atlas versions marked owner_approved_done (100%).
- 48/48 late-game species owner-approved.
- Final inventory and hash-bound owner disposition persisted.

Files changed:
- P10-redraw-plan.md
- P10-redraw-closure-20261011.md
- handoff-redraw-20261011.md
- redraw-kit/owner-atlas-selection.json
- redraw-kit/owner-reviews.json
- redraw-kit/polish-20261008/progress.json
- redraw-kit/completion-20261011/{done,mechanical}.json

Architecture decisions:
- Atlas paths and SHA-256 hashes define accepted versions.
- Explicit owner chat confirmation recorded with its own source.
- Historical review records retained; runtime integration is separate.

Tests:
- 152 atlas mechanical checks passed.
- 1 review persistence/version/path-guard test passed.
- Runtime Go/Godot tests not run: no runtime changes in this closure.
- 0 flaky tests observed in these checks.

Known issues:
- Runtime integration and in-battle sizing are not certified by art closure.
- Named phimond-phase-handoff skill unavailable; mandated format used directly.

Git diff:
- Closure files listed above; final inventory lists all selected asset paths.
- Working tree includes pre-existing art/client/spec work, preserved.
- No commit/push: current redraw contract explicitly forbids these operations.
