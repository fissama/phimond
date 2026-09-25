# `.ai/` — agent navigation layer for Phimond

This folder is the **canonical agent-oriented navigation layer** for
project context, intent, planning, decisions, workflows, and handoffs.
It is not a second wiki and not a duplicate of the codebase.

**Authoritative sources (in priority order):**

| Question                                        | Authoritative source                            |
| ----------------------------------------------- | ----------------------------------------------- |
| What is the code actually doing right now?      | Source code, tests, schemas, runtime.           |
| What should the code be doing?                  | Currently accepted product / phase specification. |
| Why does an architectural choice exist?         | Latest accepted, non-superseded ADR.            |
| What is currently being worked on?              | `.ai/ACTIVE.md`                                 |
| Unfinished work crossing agent boundaries?      | Latest relevant handoff in `.ai/handoffs/`.     |
| Archived / historical material?                 | `.ai/archive/` — **historical only**, never load into cold-start. |

When two authoritative sources conflict, surface the conflict instead of
silently reconciling. Do not copy implementation state into documentation
unless it provides durable semantic value.

**Hard rule:** Session / handoff history must never silently override
active specifications.

## Cold-start sequence (HOT / WARM / COLD)

Read in this order. Do not bypass.

```
HOT   1. .ai/CONTEXT.md       — stable project context (one screen)
HOT   2. .ai/ACTIVE.md        — what is in flight right now
HOT   3. Active sprint/phase docs referenced by ACTIVE.md
WARM  4. Relevant ADRs referenced by the active spec / ACTIVE.md
WARM  5. Latest relevant handoff, only if one exists
WARM  6. .ai/plan/PHIMOND_MASTER_SPEC.md — only the sections needed
WARM  7. Relevant SKILL.md — only when the task needs that procedure
COLD  (everything else, including evidence, design, archive)
```

Master spec, design docs, historical ADRs, and archive are loaded on
demand — not at cold-start.

## Map

```
.ai/
├── README.md                       ← you are here (index + authority rules)
├── CONTEXT.md                      ← HOT: stable project context (≤ 1 screen)
├── ACTIVE.md                       ← HOT: pointer to current work
├── GLOSSARY.md                     ← HOT: terminology used everywhere
│
├── plan/
│   ├── PHIMOND_MASTER_SPEC.md     ← WARM: product contract, phases, exit gates
│   ├── SPRINT_SPEC_TEMPLATE.md     ← WARM: mandatory sprint spec structure
│   └── phases/
│       └── PXX-name/
│           ├── README.md           ← phase index (status, carry-over, evidence)
│           ├── PXX-S0N-spec.md
│           ├── PXX-implementation-plan.md
│           ├── PXX-verification.md
│           ├── PXX-review.md
│           └── evidence/           ← COLD: raw logs, metrics, screenshots
│
├── design/                         ← WARM: visual / UX / gameplay specs
│   ├── README.md
│   ├── visual-style.md
│   ├── ui/
│   └── gameplay/
│
├── decisions/                      ← WARM: ADR pattern (immutable bodies)
│   ├── README.md
│   └── ADR-NNNN-short-title.md
│
├── skills/                         ← WARM: repeatable procedures
│   ├── README.md
│   └── phimond-<verb-noun>/SKILL.md
│
├── handoffs/                       ← WARM (only if unfinished work exists)
│   ├── README.md
│   ├── CURRENT.md                  (optional, only if it simplifies retrieval)
│   ├── YYYY-MM-DD-*.md
│   └── archive/
│
└── archive/                        ← COLD: superseded; never load into cold-start
```

## Folder rules

| Folder        | Rule                                                                       |
| ------------- | -------------------------------------------------------------------------- |
| `plan/`       | Never delete from here. Add new phases by copying template.                |
| `skills/`     | One folder per skill, `SKILL.md` inside. Procedural — knowledge belongs elsewhere. |
| `decisions/`  | Immutable body after acceptance. Lifecycle via `Status:` field, not edits. |
| `design/`     | Living docs; iterate freely. Cross-reference from plan specs.              |
| `handoffs/`   | Only for unfinished cross-session / cross-agent work. Completed work moves to specs / verifications / archive. |
| `archive/`    | Move-only. Never delete. Add `_moved.md` header pointing to replacement.   |

## Evidence retention rules

`evidence/` is **not** a dump for build artifacts. Allowed:

- `.json` summaries (load results, metrics summaries, snapshots)
- `.csv` tables
- small `.log` summaries (≤ ~300 KB)
- selected screenshots showing acceptance criteria
- benchmark summary numbers

Disallowed (unless genuinely required):

- full build logs
- large videos
- profiling traces
- temporary outputs
- full test dumps
- source-tree tarballs > a few MB

Prefer `verification.md` to record:

- command executed
- result
- relevant metrics
- selected durable evidence
- reproducibility instructions

Raw large artifacts belong in CI artifacts, temporary storage, or
Git LFS — not in `evidence/`.

## Naming conventions

| Kind                        | Pattern                                | Example                          |
| --------------------------- | -------------------------------------- | -------------------------------- |
| Chronological artifact      | `YYYY-MM-DD-kebab-case.md`             | `2026-09-25-routine-setup.md`    |
| Stable semantic document    | stable descriptive filename             | `README.md`, `CONTEXT.md`        |
| ADR                         | `ADR-NNNN-kebab-title.md` (zero-pad 4) | `ADR-0001-2d-movement.md`        |
| Phase / sprint doc          | `PXX-S0N-purpose.md`                   | `P01-S01-portal-proximity.md`    |
| Skill                       | `phimond-<verb-noun>/SKILL.md`         | `phimond-phase-handoff/SKILL.md` |
| Evidence                    | `YYYY-MM-DD-short-descriptor.ext`      | `2026-09-25-load-10.json`        |

Dates are part of identity **only when chronology matters**. Stable
documents (READMEs, master specs, ADRs) keep their canonical name.

## What does NOT belong here

- Source code (lives in `apps/`).
- Asset files (lives in `apps/game-client/assets/`).
- Build artifacts (`/tmp/...`).
- Secrets (`.env` is gitignored at workspace root; never copy into `.ai/`).
- Session journals or "what I did today" notes — git log captures history.
