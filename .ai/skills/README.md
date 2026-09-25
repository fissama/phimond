# `.ai/skills/` — project-scoped agent procedures

Reusable procedures specific to Phimond. Each skill is one folder with a
`SKILL.md` body. Skills are **procedural**, not informational — knowledge
belongs in specs, ADRs, design docs, or context docs.

## Index

| Skill                              | Use when                                                  |
| ---------------------------------- | --------------------------------------------------------- |
| `phimond-phase-handoff/`           | After completing a phase/sprint, generate the GPT 6 Astra handoff package. |

## How skills get discovered

Skills at `.ai/skills/<name>/SKILL.md` are **not** auto-loaded by the
runtime skill loader. They are project-scoped reference material; an
agent working on this project should `read` the file before invoking
the procedure, or copy it into its own agent skill dir to make it
tool-invokable.

For runtime auto-loading, copy `SKILL.md` to
`~/.minimax/agents/<agent-name>/skills/<name>/SKILL.md`.

## Skill body structure

Every skill follows this structure (see `phimond-phase-handoff/SKILL.md`
for a complete example):

```markdown
# <Skill Name>

## Trigger

<when this skill fires — concrete user phrases + workflow-step labels>

## Inputs

<inputs the skill consumes; which are required vs optional; where they come from>

## Preconditions

<state the world must be in before the skill runs; what to verify>

## Procedure

<numbered steps the agent follows; each step concrete and reproducible>

## Outputs

<what the skill produces; file paths, formats, naming conventions>

## Validation

<how to verify the output is correct>

## Failure conditions

<what to do if a step fails; partial outputs; cleanup>
```

## Adding a new skill

1. Pick a name: `phimond-<verb-noun>/` (lowercase, kebab-case).
2. Create folder + `SKILL.md` with frontmatter:
   ```markdown
   ---
   name: phimond-<verb-noun>
   description: <one-line when-to-trigger description; include concrete trigger phrases>
   ---
   ```
3. Body follows the structure above.
4. Reference from `AGENTS.md` workflow if it slots into a ritual step.
5. Update this README's index.
6. Commit; do NOT delete the old skill from agent dir until runtime
   migration is confirmed.

## What is NOT a skill

- "How Phimond architecture works" → belongs in `.ai/plan/PHIMOND_MASTER_SPEC.md`.
- "What does this code do" → read the code.
- "History of decision X" → belongs in `.ai/decisions/ADR-NNNN-...md`.
- "Design rationale for visuals" → belongs in `.ai/design/visual-style.md`.
