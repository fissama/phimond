# GLOSSARY.md — project-specific terminology

Use these terms consistently across code, commits, handoffs, and reviews.
Add a new term the first time it appears more than once.

## Core

| Term                     | Meaning                                                                          |
| ------------------------ | -------------------------------------------------------------------------------- |
| **Server-authoritative** | All RNG, damage, capture, progression, and ownership decisions live on server.   |
| **Phimond**              | Internal name for the reconstruction of 《靈獸世界 Online》 / PokeZoo Online.   |
| **Reconstruction**       | Preserve source roster/art and presentation; approved gameplay changes are labeled in the active P10 spec rather than presented as historical facts. |
| **Confidence**           | Tag on reconstructed data: `observed` / `inferred` / `reconstructed` / `unknown`. |
| **POC art**              | Current artwork is proof-of-concept quality; not the final visual standard.     |

## Game domain

| Term          | Meaning                                                                              |
| ------------- | ------------------------------------------------------------------------------------ |
| **Pet**       | Combat unit owned by a player. Has species + variance + lineage.                    |
| **Species**   | Template with source identity/Race/Star/art. Approved baseline: 152 in `roster_apk84.json`; legacy runtime still uses 14 in `species.json` pending stat/skill/save migration. |
| **Race**      | Species taxonomy and eligibility dimension; eight source races. Does not automatically assign combat Element or grant a stat bonus. |
| **Element**   | Species combat property independent of Race; interaction uses skill Element vs target Element, with chart owned by P13. |
| **Special**   | APK-defined thần thú: four 4★ and thirteen 5★ species with exact same-Star parent pairs. Not an extra Star. |
| **MP**        | Combat resource; maxMP/growth/recovery owned by P11, consumption by P13. Separate from the six core stats. |
| **Status Resistance** | One shared stat affecting status application probability; not duration reduction or a per-status map. |
| **Basic attack** | Separate attack-button action available at zero learned skills; consumes no learned-skill slot. |
| **Star (★)**   | Pet tier 1★–5★; controls level cap (60/70/80/90/100).                              |
| **+00..+99**  | "Plus" rating on a pet; opens extra level room above star cap. **+99 cannot** be upgraded. |
| **Synthesis** | Two-pet fusion into Egg: normal next-Star ascension, source-defined same-Star Special recipe, or reinforcement preserving main Species. Exact Special server rules still need review. |
| **Capture**   | Convert wild pet to owned; bounded by HP threshold + status + luck.                 |
| **Room**      | A discrete map (40×24 tiles currently). One of: severa / forest / beach / ranch / arena. |
| **Portal**    | Edge-of-room transition to another room. Min-level + arena-tier gated.               |
| **NPC**       | Stationary role in a room (trainer, ranch_keeper, arena_master, …). 7 roles total. |
| **Encounter** | Wild combat trigger from a spawn tile (1 pet vs 3 wilds in solo PvE).              |

## Architecture

| Term                  | Meaning                                                                    |
| --------------------- | -------------------------------------------------------------------------- |
| **Engine**            | The apply-handler in `internal/character/`; all live ops go through it.   |
| **Envelope**          | WebSocket message format: `{op, request_id, data, ...}`.                   |
| **Receipt**           | Persisted log entry in `receipts` table; used for retry / reconnect dedup.  |
| **Snapshot**          | Server's full view of a character sent on connect / after reconnect.        |
| **Movement allowed keys** | `rules.json` whitelist of fields client can read from state JSON.    |
| **Fail-soft**         | When persistence fails (DB outage), live ops still proceed; receipts queue.|
| **Live**              | A WebSocket session, vs `e.HTTP` which is stateless.                       |

## Process

| Term                  | Meaning                                                                    |
| --------------------- | -------------------------------------------------------------------------- |
| **Phase**             | A product milestone (P00, P01, …). One or more sprints. Has an exit gate. |
| **Sprint**            | A bounded work unit inside a phase. Has spec + implementation plan + verification. |
| **Sprint spec**       | Mandatory structure from `SPRINT_SPEC_TEMPLATE.md`. Authored before code.  |
| **Implementation plan** | File-level action plan. Written after sprint spec, before coding.       |
| **Handoff**           | Cross-session / cross-agent context for unfinished work. Output of `phimond-phase-handoff` skill. |
| **Worker**            | A bounded-scope subagent (code / docs / operational split, see AGENTS.md). |
| **Evidence**          | Raw logs / metrics / screenshots stored under `plan/phases/PXX/evidence/`. |

## Data conventions

- Test accounts: prefix `p00_*`, then `ref_*`, then `contact_*`.
- Server PID logs: `/tmp/p00-serve.log` (rotated on restart).
- Diff size policy: inline ≤ 500 lines, else `/tmp/phase-<id>-<short>.diff`.
- DB name: `phimond_reconstruction` (never `philandz`).
- `.env` is gitignored at workspace root; **never** commit values.
