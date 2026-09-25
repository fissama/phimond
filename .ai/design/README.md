# `.ai/design/` — design specs (not sprint-bound)

Living documents that describe **what the game looks / feels like** at a
higher level than any one sprint. Cross-referenced from
`plan/phases/PXX/` but not versioned per-phase.

## Index

| Doc                   | Purpose                                                        |
| --------------------- | -------------------------------------------------------------- |
| `visual-style.md`     | Color palette, typography, art direction, sprite silhouettes.  |
| `ui-layout-960x640.md` | Viewport contract, control sizes, HUD strip proportions.      |
| `combat-flow.md`      | Turn order, action menu, damage numbers, status display.       |
| `asset-mapping.md`    | APK → extracted → in-game asset map; missing assets list.     |
| `animation-states.md` | Sprite state machine conventions (idle/run/attack/hurt/...). |

(Append as new specs are added.)

## Conventions

- One topic per file; small enough to read in 5 minutes.
- Cite evidence: link to `docs/research/VIDEO_UI_AUDIT_*.md`,
  `docs/research/HUD_REFERENCE.md`, or video timestamps.
- Use ASCII diagrams or Mermaid; keep images in `docs/research/reference/`.
- Reference `data/` rules / formulas where the design depends on them.
- Reference `AGENTS.md` conventions where the design affects build/test.

## Status field

Each design doc should open with:

```markdown
- **Status**: draft | review | stable | superseded-by-<file>
- **Last reviewed**: YYYY-MM-DD
```

A `review`-status doc may still change; `stable` doc needs an ADR to
change.

## When to write a design doc

- A visual / UX rule that repeats across multiple sprints.
- A contract between client and server that isn't obvious from code
  (cross-reference ADR if it's server-affecting).
- An asset-mapping decision that future contributors need to know.

## When NOT to write

- A bug fix (commit message suffices).
- A one-off decision inside one sprint (lives in the sprint spec).
