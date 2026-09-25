# `.ai/handoffs/` — cross-session / cross-agent context

**Use only for unfinished work crossing agent / session boundaries.**
Do not create a handoff for every successful completed task.

Completed work consolidates into:

- accepted specifications (`plan/phases/PXX/PXX-S0N-spec.md`)
- verifications (`plan/phases/PXX/PXX-verification.md`)
- ADRs (`decisions/ADR-NNNN-...md`)
- design docs (`design/...`)

When a phase / sprint completes, the relevant handoff moves to
`handoffs/archive/`.

## Naming

`YYYY-MM-DD-<phase-or-topic>.md`. Examples:

- `2026-09-25-P01-sprint-1.md`
- `2026-09-25-routine-setup.md`
- `2026-09-24-P00-closure.md`

## Handoff structure

Each handoff uses this structure (consumed by `phimond-phase-handoff`
skill):

```markdown
# Handoff

- **Date**: YYYY-MM-DD
- **Agent**: <name>
- **Commit / working tree state**: <sha> / <working-tree-state>
- **Related phase**: PXX-name
- **Related sprint**: PXX-S0N

## Goal

<one-paragraph intent of this work>

## Completed

- [x] <item>
- [x] <item>

## Current state

<where the code / data / docs are right now>

## Partial / uncommitted work

<uncommitted changes, drafts, partial implementations>

## Decisions already made

<ADRs drafted, scope decisions, default choices>

## Do not redo

<explicit list of things the next agent should NOT re-do>

## Remaining work

- [ ] <open item>
- [ ] <open item>

## Verification already performed

<test commands run, results, screenshots>

## Known failures

<flaky tests, regressions, blocked checks>

## Relevant files

<key files with line refs>

## Recommended next action

<one sentence — what should the next agent do first?>
```

## Optional: `CURRENT.md`

If multiple in-flight handoffs exist, `.ai/handoffs/CURRENT.md` may
point to the most relevant one (or the one without which the next
session cannot proceed). Keep it tiny: 5–10 lines, pointer + 1-line
context per active handoff.

Do not create `CURRENT.md` unless there are ≥ 2 active handoffs and
they conflict on priority.

## When to write

- A new sprint starts and the previous agent's session ended mid-sprint.
- A long-running refactor crosses session boundaries.
- A blocker needs to be flagged for the next agent.

## When NOT to write

- For trivial changes (typo fix, doc update).
- For every successful commit (git log is the audit trail).
- For mid-session status updates (use chat reply).
- For a finished phase with no follow-up work — consolidate into specs
  / verifications / ADRs and archive.

## Archive

Move (don't delete) to `handoffs/archive/<original-name>` when:

- The session was superseded by a later handoff.
- The associated work has consolidated into specs / verifications.
- More than 90 days old and no longer referenced.
