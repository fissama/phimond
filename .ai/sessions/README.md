# `.ai/sessions/` — chronological journal of agent work

One short file per session (1–2 screens). Purpose: **restore context**
when a new agent inherits a half-finished task, and **audit** who did
what when.

## Naming

`YYYY-MM-DD-<short-descriptor>.md`. Examples:

- `2026-09-25-routine-setup.md`
- `2026-09-24-debug-battle-replay.md`

## What's inside

```markdown
# Session YYYY-MM-DD — <one-line summary>

- **Agent**: Mavis / GPT 6 Astra / contractor
- **Phase / sprint**: PXX-S0N (or free-form)
- **Started**: <link to first user message of the session>
- **Ended**: <link to last assistant message>

## What I did

1. <step 1>
2. <step 2>

## What I found out

- <finding 1>
- <finding 2>

## What's left for next session

- [ ] <open item>
- [ ] <open item>

## Blockers / questions

- <question for user or other agent>
```

## When to write

At the end of every non-trivial session, before signing off. If the
session produced a `phimond-phase-handoff`, the session journal is the
lighter-weight complement.

## When NOT to write

- Pure-chat sessions with no code / context change.
- Sessions where the user asked a single question and got an answer.

## Retention

Keep last 30 days in `sessions/`. Older ones move to `sessions/archive/`
or fold into `reviews/PXX-review.md` if they're part of a phase review.
