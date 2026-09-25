# Active Development

> Canonical pointer to current work. Updated at end of every phase delivery.
> Cheap to read — pointers only, no duplicated specs.

- **Last verified**: 2026-09-25
- **Verified against commit**: `452dbc0` (`.ai/: project context structure`)

## Current phase

P00-baseline (closed 2026-09-24, commit `e66350b`).

## Current sprint

None. Next phase to pick: **P01 — map / proximity / collision**.

## Status

Idle. Awaiting user choice on next phase or sprint.

## Current objective

Pick a single sprint from P01 master scope and write the sprint spec
before any code change.

## Active specification

- Master: `.ai/plan/PHIMOND_MASTER_SPEC.md` (sections for P01 not yet
  drafted; see master "Next phases" list).
- Active phase: `.ai/plan/phases/P00-baseline/` (closed; for reference only).

## Implementation plan

None. Will be authored when a sprint is picked, after the sprint spec is
accepted.

## Relevant ADRs

None accepted yet. Folder scaffold: `.ai/decisions/README.md`.

## Latest handoff

None outstanding. Most recent commit is project-context structure work,
not a phase delivery — no handoff was produced.

## Current blockers

- User has not picked P01 sprint scope yet.
- `layout_audit.gd` (Godot smoke) was written for the previous
  MainMap/BattleScene paradigm and is now stale after the
  `reference_game.gd` restructure; needs decision (rewrite vs delete).

## Known failing checks

- None currently blocking. `go test -race ./... -count=1` green;
  `min_smoke.gd` PASS; `contact_check.gd` PASS; `layout_audit.gd`
  expected to FAIL until rewritten.

## Next recommended action

User to confirm which P01 sprint to start. Suggested first slice: portal
proximity + collision (smallest path to a verifiable player outcome —
"can the player walk through a wall and into a portal?"). Do not begin
implementation until the sprint spec is accepted.
