# `.ai/decisions/` — Architecture Decision Records (ADR)

Immutable log of **why** the code looks the way it does. Once an ADR is
**Accepted**, its body is never edited; lifecycle is tracked only via
the `Status:` field. Reversing a decision requires a new ADR.

## Lifecycle

```
Proposed ───► Accepted ───► Superseded (by ADR-XXXX)
            ╲
             ╲──► Rejected (recorded for context)
              ╲
               ──► Deprecated (still in effect, but flagged to avoid for new work)
```

| Status      | Meaning                                                                              |
| ----------- | ------------------------------------------------------------------------------------ |
| Proposed    | Under discussion. Body may change.                                                   |
| Accepted    | Decision is in force. Body is **immutable**; only the status header may change.     |
| Rejected    | Considered but not adopted. Recorded for context.                                    |
| Superseded  | Replaced by a later ADR. Body kept for context; the new ADR cites it.               |
| Deprecated  | Still in force but flagged as a poor choice; new work should prefer alternatives.    |

A `Superseded` ADR must contain:

```markdown
Status: Superseded
Superseded by: ADR-XXXX-...
```

Do not infer supersession from dates alone — the link is explicit.

The **latest Accepted, non-Superseded ADR on a topic** is authoritative
for that topic's rationale.

## Index

| ID      | Title                                | Status   | Date       |
| ------- | ------------------------------------ | -------- | ---------- |
| _none yet_ |                                  |          |            |

(Append each new ADR here on acceptance.)

## Template (`ADR-NNNN-short-title.md`)

```markdown
# ADR-NNNN: <short title>

- **Status**: Proposed | Accepted | Rejected | Superseded | Deprecated
- **Date**: YYYY-MM-DD
- **Deciders**: <who>

## Context

What is the situation that requires a decision? What forces are at play
(technical, schedule, team, compatibility)? Include links to evidence
in `.ai/plan/phases/PXX/evidence/` or `docs/research/`.

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

- Architectural choice that affects multiple modules (server-client
  contract, package boundaries, data shape).
- Trade-off between two valid approaches (sync vs async, REST vs WS,
  monolith vs split, stub vs full impl).
- Reversal of a previous ADR (write a new one that supersedes).
- Rejection of a "popular" or "default" approach for project reasons.

## When NOT to write an ADR

- A bug fix that follows an existing convention (commit message suffices).
- An implementation detail that's obvious from the code.
- A user-facing feature that lives entirely in one sprint spec (lives in
  `plan/phases/PXX/` instead).
- Routine session work (lives in git log / `handoffs/` if unfinished).
