# `.ai/decisions/` — Architecture Decision Records (ADR)

Immutable log of **why** the code looks the way it does. Once an ADR is
accepted, it is **never edited**; if the decision is reversed, write a
new ADR that supersedes it.

## Index

| ID      | Title                                | Status   | Date       |
| ------- | ------------------------------------ | -------- | ---------- |
| ADR-0001 | 2D world movement (server + client) | accepted | 2026-09-23 |
| ADR-0002 | Stub packages over empty impls       | accepted | 2026-09-23 |
| ADR-0003 | Server-authoritative damage/RNG      | accepted | 2026-09-17 |
| ADR-0004 | ...                                  |          |            |

(Append here as ADRs are written. Keep the table compact; details live in
the individual files.)

## Template (`ADR-NNNN-short-title.md`)

```markdown
# ADR-NNNN: <short title>

- **Status**: proposed | accepted | superseded by ADR-MMMM
- **Date**: YYYY-MM-DD
- **Deciders**: <who>

## Context

What is the situation that requires a decision? What forces are at play
(technical, schedule, team, compatibility)? Include links to evidence.

## Decision

What did we decide? State it in active voice ("We will …").

## Consequences

What becomes easier? What becomes harder? What new risks appear? Include
both positive and negative consequences.

## Alternatives considered

- **Alternative A**: <one-line description>. Why rejected.
- **Alternative B**: <one-line description>. Why rejected.
```

## Naming

`ADR-NNNN-kebab-case-title.md`. Zero-pad to 4 digits. Monotonic counter
across the project; do not renumber when superseding.

## When to write an ADR

- Architectural choice that affects multiple modules (e.g. server-client
  contract, package boundaries, data shape).
- Trade-off between two valid approaches (e.g. sync vs async, REST vs WS,
  monolith vs split).
- Reversal of a previous ADR (write a new one that supersedes).
- Rejection of a "popular" or "default" approach for project reasons.

## When NOT to write an ADR

- A bug fix that follows an existing convention.
- Implementation detail that's obvious from the code.
- A user-facing feature that lives entirely in one sprint spec (lives in
  `plan/phases/PXX/` instead).
