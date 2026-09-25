# P00 — Baseline + Measurement (CLOSED)

> Phase folder index. Closed 2026-09-24, commit `e66350b`. Kept for
> historical reference; do not modify unless updating evidence.

## Status

- **State**: closed (not certified for 50 CCU online; combat p95 1659ms
  exceeded budget on dev topology).
- **Closure commit**: `e66350b`
- **Closure report**: see verification + review docs in this folder.

## Documents in this phase

| File                              | Purpose                                             |
| --------------------------------- | --------------------------------------------------- |
| `P00-baseline.md`                 | Phase baseline narrative + scope.                   |
| `P00-S01-spec.md`                 | Sprint 1 spec.                                      |
| `P00-S02-spec.md`                 | Sprint 2 spec.                                      |
| `P00-S03-spec.md`                 | Sprint 3 spec.                                      |
| `P00-implementation-plan.md`      | File-level execution plan for the sprints.          |
| `P00-verification.md`             | Build/test evidence, acceptance results.           |
| `P00-review.md`                   | Per-phase gameplay & game design review.            |
| `P00-performance-baseline.md`     | Latency budget / measurement baseline.              |
| `P00-reference-ledger.md`         | Evidence provenance ledger (assets / sources).      |
| `P00-continuation-beads.md`       | Carry-over task list into P01+ (mostly historical). |
| `progress.md`                     | Live progress notes during P00 work.                |
| `evidence/`                       | Raw logs, metrics, screenshots, JSON snapshots.     |

## Carry-over (P00 → later phases)

See `P00-continuation-beads.md` for tasks pushed to P01+ / P02 / P03.

## Evidence retention

`evidence/` contains 80+ files (~99 MB total). A 93 MB tarball
(`source-before-p00.tgz`) is a pre-P00 source snapshot — kept for
historical provenance but **not** typical evidence; future phases
should not generate files of that size. See
`.ai/README.md → Evidence retention rules`.

## Do not

- Edit `P00-*-spec.md` / `P00-verification.md` / `P00-review.md` to
  retroactively mark P00 as passing 50 CCU. P00 was closed honestly.
- Add new sprint specs under `P00-baseline/` — phase is closed.
