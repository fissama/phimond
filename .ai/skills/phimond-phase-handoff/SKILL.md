---
name: phimond-phase-handoff
description: Generate the standard GPT 6 Astra handoff package for a completed Phimond phase/sprint. Reads git state and composes a tight summary with diff, files, decisions, tests, and known issues. Trigger when the user says "handoff", "phase summary", "package for GPT 6 Astra", or after marking a phase done per AGENTS.md "Phase delivery ritual".
---

# Phimond Phase Handoff

Generate the handoff package specified in `AGENTS.md` → "Phase delivery ritual"
step 4. Output goes to `.ai/plan/phases/<phase>/handoff-<YYYYMMDD>.md` for
the audit trail and is also printed so the user can forward it to GPT 6
Astra unchanged.

## When to use

- After step 3 (self-review) of the phase delivery ritual passes.
- The user explicitly asks for a handoff / phase summary / GPT 6 Astra package.
- Another agent asks you to produce a structured summary of recent work.

Do not use for:
- Mid-phase status (that's just a normal chat reply).
- Tasks without a clear "phase" boundary (use a free-form summary instead).

## Inputs

Collect these from the user or from current session context:

| Input             | Required | Source                                                    |
| ----------------- | -------- | --------------------------------------------------------- |
| Phase ID + name   | yes      | `.ai/plan/phases/<phase>/` or the conversation            |
| Implemented list  | yes      | user-supplied OR distilled from commit message + diff     |
| Files changed     | auto     | `git diff --stat <base>..HEAD`                            |
| Architecture dec. | yes      | user-supplied (otherwise mark "see commit message")       |
| Tests summary     | auto     | smoke outputs already captured this session               |
| Known issues      | yes      | user-supplied OR inferred from test failures / TODOs      |
| Base ref for diff | auto     | default `HEAD~1` if HEAD is a phase commit, else `main`   |

If any required input is missing, ask the user once before guessing.

## Steps

1. Confirm git working tree:
   ```sh
   git -C <workspace> status --porcelain
   ```
   If non-empty (uncommitted changes), warn the user: "Working tree has
   uncommitted changes — handoff will only cover committed work. Commit
   first or pass `--allow-dirty`."
2. Resolve the base ref:
   - Default `HEAD~1`.
   - Override via `--base <ref>` argument.
   - If `git diff HEAD~1..HEAD` is empty (HEAD is not a phase commit),
     fall back to `git diff main..HEAD`.
3. Capture diff:
   ```sh
   git -C <workspace> diff --stat <base>..HEAD
   git -C <workspace> log <base>..HEAD --oneline
   git -C <workspace> diff <base>..HEAD > /tmp/phase-<id>-<short>.diff
   ```
   Line count: `wc -l /tmp/phase-<id>-<short>.diff`.
4. Compose the package using the exact format from AGENTS.md (see
   "Handoff format" section). Replace `<bullets>` with the inputs above.
5. Write to disk:
   ```sh
   .ai/plan/phases/<phase>/handoff-$(date +%Y%m%d).md
   ```
   Create the directory if missing. Print the package to stdout.
6. Report:
   - Path of saved handoff file.
   - Path of full diff file (if saved separately).
   - Number of files changed, total diff size.

## Handoff format (verbatim)

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

## Honesty rules

- "Tests: N passed" must count only what actually passed in this session.
- Anything that *should* have passed but didn't goes in Known issues, not
  Tests. Never inflate test counts.
- If the user supplied the inputs and you can't verify them, say so in a
  comment line at the bottom of the handoff (e.g. `# supplied by user;
  not verified by this skill`).
- Never invent values. Use `confidence: "reconstructed"` markers if the
  user follows that convention (Phimond uses this in data JSONs).

## Edge cases

- **Empty diff** (HEAD == base): tell the user no changes detected, ask
  if they want a context-only handoff (architecture / decisions only).
- **Single-commit phase**: diff is just that commit; cite SHA + subject.
- **Cross-cutting changes** (data + code + docs): list all in Files changed,
  group by area (server / client / data / docs / scripts).
- **Forwarded to another agent**: keep the package self-contained — no
  abbreviations the receiving agent won't recognize.

## After delivery

- Confirm the file was written (read it back to verify size).
- Tell the user: "Handoff saved at <path>. Forward this to GPT 6 Astra or
  paste into the next agent session."
- If the commit + push step (step 5 of the ritual) hasn't happened yet,
  remind the user to run it.
