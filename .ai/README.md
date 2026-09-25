# `.ai/` — workspace context, plans, decisions, skills

This folder is the **only** place where agents (this Mavis instance, GPT 6
Astra, future sessions, contractors) read project-level context before
touching code. Keep it lean, dated, and self-contained.

> **Cold-start order** for any new agent / session:
>
> 1. `.ai/CONTEXT.md` — where the project is *right now*
> 2. `.ai/plan/PHIMOND_MASTER_SPEC_PLAN.md` — the product contract
> 3. `.ai/decisions/` (latest 5 ADRs) — why the code looks the way it does
> 4. `.ai/handoffs/` (latest) — what the previous session left you
> 5. `.ai/skills/` — repeatable procedures available in this project

## Map

```
.ai/
├── README.md                          ← you are here (index + conventions)
├── CONTEXT.md                         ← cold-start one-pager (≤ 1 screen)
├── GLOSSARY.md                        ← project-specific terminology
│
├── plan/                              ← spec & per-phase planning
│   ├── PHIMOND_MASTER_SPEC_PLAN.md   ← product contract, phases, exit gates
│   ├── SPRINT_SPEC_TEMPLATE.md       ← mandatory structure for any new sprint
│   └── phases/
│       └── PXX-name/
│           ├── PXX-S0N-spec.md      ← what to build & why
│           ├── PXX-implementation-plan.md  ← file order, test order
│           ├── PXX-verification.md   ← build/test evidence + acceptance
│           ├── PXX-gameplay-gamedesign-review.md
│           └── evidence/             ← raw logs, metrics, screenshots
│
├── skills/                            ← project-scoped repeatable procedures
│   ├── README.md
│   ├── phimond-phase-handoff/SKILL.md  ← standard handoff package
│   └── ...
│
├── decisions/                         ← Architecture Decision Records (ADR)
│   ├── README.md                      ← ADR template + index
│   └── ADR-NNNN-short-title.md
│
├── design/                            ← visual / UX specs (not sprint-bound)
│   ├── README.md
│   ├── visual-style.md
│   ├── ui-layout-960x640.md
│   ├── combat-flow.md
│   └── ...
│
├── reviews/                           ← gameplay / design reviews per phase
│   ├── README.md
│   └── PXX-review.md
│
├── handoffs/                          ← cross-session / cross-agent context
│   ├── README.md                      ← naming convention
│   ├── 2026-09-25-AGENTS-md-routine.md
│   └── archive/
│       └── ...
│
├── sessions/                          ← chronological journal of agent work
│   ├── README.md
│   └── 2026-09-25-routine-setup.md
│
└── archive/                           ← superseded docs (do not delete; only move)
```

## Conventions

| Folder        | Rule                                                                       |
| ------------- | -------------------------------------------------------------------------- |
| `plan/`       | Never delete from here. Add new phases by copying template.                |
| `skills/`     | One subfolder per skill, `SKILL.md` inside. Mirror agent-skill format.     |
| `decisions/`  | Immutable. Once accepted, an ADR is never edited; supersede with a new one. |
| `design/`     | Living documents; OK to iterate. Cross-reference from plan specs.         |
| `reviews/`    | One per phase. Linked from `plan/phases/PXX/`.                            |
| `handoffs/`   | One file per delivery, dated. Use `phimond-phase-handoff` skill to write. |
| `sessions/`   | Append-only. Each session writes a 1-page summary at end of work.          |
| `archive/`    | Moved-out, not deleted. Keep git history of removals via commit message.  |

## Naming conventions

- Files: `YYYY-MM-DD-kebab-case.md` (date first for chronological sort).
- Phases: `PXX-name` (zero-padded two digits + kebab name), e.g. `P03-enemy-ai`.
- Skills: `phimond-<verb-noun>/SKILL.md`.
- ADRs: `ADR-NNNN-kebab-title.md` (zero-padded 4 digits).
- Evidence files: `YYYY-MM-DD-short-descriptor.{json,log,png,csv}`.

## What does NOT belong here

- Source code (lives in `apps/`).
- Asset files (lives in `apps/game-client/assets/`).
- Build artifacts (`/tmp/...`).
- Secrets (`.env` is gitignored at root; never copy into `.ai/`).
