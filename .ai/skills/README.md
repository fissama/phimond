# `.ai/skills/` — project-scoped skills

Reusable procedures specific to Phimond. Each skill is one folder with a
`SKILL.md` body; the loader maps the skill `name:` field in the frontmatter
to its invocation.

> **How skills get discovered**
>
> Skills at `.ai/skills/<name>/SKILL.md` are **not** auto-loaded by the
> runtime skill loader. They are project-scoped reference material; an
> agent working on this project should `read` the file before invoking
> the procedure, or copy it into its own agent skill dir to make it
> tool-invokable.
>
> For runtime auto-loading, copy `SKILL.md` to
> `~/.minimax/agents/<agent-name>/skills/<name>/SKILL.md`.

## Index

| Skill                              | Use when                                                  |
| ---------------------------------- | --------------------------------------------------------- |
| `phimond-phase-handoff/`           | After completing a phase/sprint, generate the GPT 6 Astra handoff package. |

## Adding a new skill

1. Pick a name: `phimond-<verb-noun>/`.
2. Create folder + `SKILL.md` with frontmatter:
   ```markdown
   ---
   name: phimond-<verb-noun>
   description: <one-line when-to-trigger description, must include trigger phrases>
   ---
   ```
3. Body: when to use / not use, inputs, steps, output contract, edge cases.
4. Reference from `AGENTS.md` workflow if it slots into a ritual step.
5. Commit; do NOT delete the old skill from agent dir until runtime
   migration is confirmed.
