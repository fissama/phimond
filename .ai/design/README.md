# `.ai/design/` — visual / UI / gameplay design specs

Living documents that describe **what the game looks / feels like** at a
higher level than any one sprint. Cross-referenced from
`plan/phases/PXX/` but not versioned per-phase.

Only create subfolders when existing content warrants them. Do not
pre-create empty directories.

## Taxonomy

```
.ai/design/
├── README.md
├── visual-style.md              ← art direction, color palette, typography, sprite silhouettes
├── ui/                          ← UI/UX contracts (control sizes, layouts, copy)
│   ├── layout-960x640.md
│   ├── combat-flow.md
│   └── ...
└── gameplay/                    ← gameplay rules / systems (not art)
    ├── combat/
    ├── progression/
    ├── monsters/
    └── ...
```

A document's folder tells you whether it concerns:

| Folder       | Question it answers                                  |
| ------------ | ---------------------------------------------------- |
| root         | Cross-cutting (e.g. `visual-style.md`).              |
| `ui/`        | How controls look / behave / layout.                 |
| `gameplay/`  | Rules and systems: combat, progression, monsters, … |

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

## When to write

- A visual / UX rule that repeats across multiple sprints.
- A contract between client and server that isn't obvious from code
  (cross-reference ADR if server-affecting).
- An asset-mapping decision that future contributors need to know.

## When NOT to write

- A bug fix (commit message suffices).
- A one-off decision inside one sprint (lives in the sprint spec).
- A duplicate of code / data facts (use git / `data/` instead).
