---
name: phimond-phase-handoff
description: Generate the standard GPT 6 Astra handoff package for a completed Phimond phase/sprint. Reads git state and composes a tight summary with diff, files, decisions, tests, and known issues. Trigger when the user says "handoff", "phase summary", "package for GPT 6 Astra", or after marking a phase done per AGENTS.md "Phase delivery ritual".
---

# Phimond Phase Handoff

## Trigger

Use this skill when:

- After step 3 (self-review) of `AGENTS.md → Phase delivery ritual` passes.
- The user explicitly asks for a handoff / phase summary / GPT 6 Astra package.
- Another agent asks for a structured summary of recent phase work.

Do **not** use for:

- Mid-phase status (use a chat reply or `handoffs/CURRENT.md`).
- Tasks without a clear "phase" boundary (use a free-form summary).
- Routine completed work that does not cross agent / session boundaries.

## Inputs

| Input             | Required | Source                                                                 |
| ----------------- | -------- | ---------------------------------------------------------------------- |
| Phase ID + name   | yes      | `.ai/plan/phases/<phase>/` or conversation context                     |
| Implemented list  | yes      | user-supplied OR distilled from commit message + diff                 |
| Files changed     | auto     | `git diff --stat <base>..HEAD`                                         |
| Architecture dec. | yes      | user-supplied (otherwise mark "see commit message")                    |
| Tests summary     | auto     | smoke outputs captured this session                                    |
| Known issues      | yes      | user-supplied OR inferred from test failures / TODOs                   |
| Base ref for diff | auto     | default `HEAD~1` if HEAD is a phase commit, else `main`                |

If any required input is missing, ask the user once before guessing.

## Preconditions

- Git working tree state verified:
  ```sh
  git -C <workspace> status --porcelain
  ```
  If non-empty (uncommitted changes), warn: "Working tree has uncommitted
  changes — handoff will only cover committed work. Commit first or pass
  `--allow-dirty`."
- Base ref resolved:
  - Default `HEAD~1`.
  - Override via `--base <ref>` argument.
  - If `git diff HEAD~1..HEAD` is empty, fall back to `git diff main..HEAD`.

## Procedure

1. Capture diff:
   ```sh
   git -C <workspace> diff --stat <base>..HEAD
   git -C <workspace> log <base>..HEAD --oneline
   git -C <workspace> diff <base>..HEAD > /tmp/phase-<id>-<short>.diff
   ```
   Line count: `wc -l /tmp/phase-<id>-<short>.diff`.

2. Compose the package using the format below. Replace `<bullets>` with
   the inputs collected above.

3. Write to disk:
   ```sh
   .ai/plan/phases/<phase>/handoff-$(date +%Y%m%d).md
   ```
   Create the directory if missing. Print the package to stdout.

4. Report:
   - Path of saved handoff file.
   - Path of full diff file (if saved separately).
   - Number of files changed, total diff size.

## Outputs

The skill produces a single Markdown file in the format below, plus a
`/tmp/phase-<id>-<short-sha>.diff` file when the diff is too large to
inline (> 500 lines).

### Handoff format (verbatim)

```markdown
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

## Validation

After writing the file:

1. Read it back to confirm size > 0 and contains all 6 sections
   (Phase / Implemented / Files / Architecture / Tests / Known issues /
   Git diff).
2. Confirm diff file exists and matches `git diff <base>..HEAD` byte count
   (modulo line-ending normalization).
3. Report file paths + line counts to the user.

## Failure conditions

| Failure                                       | Recovery                                                 |
| --------------------------------------------- | -------------------------------------------------------- |
| Working tree has uncommitted changes          | Tell user to commit, or proceed with `--allow-dirty`.     |
| `git diff <base>..HEAD` is empty              | Tell user no changes detected; ask if context-only handoff is wanted. |
| Required input missing                        | Ask user once; if no answer, write handoff with placeholder + `# not verified` comment. |
| Diff > 500 lines                              | Save to `/tmp/phase-<id>-<short>.diff`; reference path inline. |
| PhimondClient / server not running            | N/A — this skill is documentation-only, no runtime deps. |

## Honesty rules

- "Tests: N passed" must count only what actually passed in this session.
- Anything that *should* have passed but didn't → **Known issues**, not Tests.
- Never inflate test counts.
- If user-supplied inputs can't be verified, mark with `# supplied by
  user; not verified by this skill` comment at the bottom of the handoff.
- Never invent values. Use `confidence: "reconstructed"` markers if the
  Phimond data JSONs use them.
