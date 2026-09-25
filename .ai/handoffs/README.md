# `.ai/handoffs/` — cross-session / cross-agent context

Output of the `phimond-phase-handoff` skill. One file per delivery,
named `YYYY-MM-DD-short-descriptor.md`. Old files move to `archive/`.

## Naming

`YYYY-MM-DD-<phase-or-topic>.md`. Examples:

- `2026-09-25-P01-sprint-1.md`
- `2026-09-25-routine-setup.md`
- `2026-09-24-P00-closure.md`

## What's inside

Each handoff follows the format from `AGENTS.md → Phase delivery ritual`:

```
Phase: <ID + name>

Implemented:
- ...

Files changed:
- ...

Architecture decisions:
- ...

Tests:
- <N> passed
- <N> skipped
- <N> flaky: <reason>

Known issues:
- ...

Git diff:
<inline diff if ≤ 500 lines, else path to /tmp/phase-<id>-<short>.diff>
```

## When to write

- After every phase / sprint delivery (mandatory per AGENTS.md).
- After any major refactor that another agent needs to pick up from.
- When the session ends with non-trivial work left half-done.

## When NOT to write

- For trivial changes (typo fix, doc update).
- For mid-session status (use a chat reply or `sessions/` journal).

## Reading order

Cold-start an agent on a new session:

1. `ls -t .ai/handoffs/*.md | head -1` — read the most recent.
2. `cat .ai/CONTEXT.md` — check it still matches.
3. If CONTEXT.md disagrees with the latest handoff, **fix CONTEXT.md first**.

## Archive

Move (don't delete) to `handoffs/archive/<original-name>` when:

- The session was superseded by a later handoff.
- More than 90 days old and no longer referenced.
- Replaced by a structured summary in `reviews/` or `sessions/`.
