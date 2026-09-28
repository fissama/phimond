# Active Development

- **Last reviewed:** 2026-09-28
- **Phase:** P10 — pet model foundation, design baseline audited; gameplay implementation not delivered.
- **Current objective:** P10 audit and ID normalization completed; use readiness gates and data contract before implementation.
- **Accepted:** original Race × Star distribution; MP as a P11 resource; growth reroll after Pet → Egg; APK-defined Special species/recipes/materials; basic attack available at zero learned skills; independent Race/Element and one Status Resistance.
- **Stat display accepted:** option A, `grown_stat + inheritance_bonus` (e.g. `186 +12`); permanent total is 198 and Overview adds equipment once.
- **Special Plus decision:** wait for verification of the original game; no reset/preserve fallback is approved. This blocks implementation of that outcome, not the remaining design discussion.
- **Re-hatch MP accepted:** recalculate max MP at Lv1 under P11 rules and set current MP to the new maximum; do not carry over old MP values or percentage.
- **Re-hatch skills accepted:** option A; level gates learning, not use of preserved learned skills at Lv1. MP and other P13 use conditions still apply.
- **Inherited-skill eligibility accepted:** option A; restrictions are per skill, and different Element alone does not exclude inheritance. Eligible skills enter the learnable pool, not current skills.
- **Status Resistance scope accepted:** option A; all harmful statuses (control, poison/burn, stat reductions), application chance only, not direct damage or duration.
- **Restoration accepted:** option A; a hatched fusion child may return to Egg and split into its exact pre-fusion parents. Consume the child; do not transfer child progress or refund spent fusion/reroll costs. Restored parents become usable again.
- **Equipment accepted:** automatically unequip on fusion and Pet → Egg; return to inventory, overflow to the player's mailbox. P19 defines mailbox behavior. Restored parents have no equipment; no item recreation from snapshots.
- **Restoration ownership accepted:** option A; rights follow the child through valid transfers, and the current owner receives both restored parents. Parent binding restrictions must not be bypassed.
- **Restored-pet overflow accepted:** option A; parents that do not fit in pet storage wait in the current owner's mailbox with their restored state intact. No use/trade before claim, no level reset on claim; P19/P16 own details.
- **Endgame correction accepted:** no standalone 5★ +99 build-change action. Reinforcement remains available at +99; output stays +99, normal costs/parent consumption/Egg → Lv1 flow apply.
- **Inheritance policy accepted:** option B; diminishing marginal gains without a hard inheritance cap. P11/P16 own formula/rounding; P15 verifies long-run pacing.
- **Native Skill Pool accepted:** option A; per-Species counts may differ, P13 designs contents by role/identity, six current-skill slots unchanged.
- **Reinforcement inheritance floor accepted:** option A; each inherited stat bonus cannot fall below the main parent's prior bonus, including at +99. Extra gains diminish, no minimum +1; Lv1 reset remains. Do not apply this floor automatically to Star-up/Special fusion.
- **Remaining work:** resolve named gates in [P10 readiness](plan/phases/P10-pet-model/P10-readiness.md). Special source rules remain unverified; formulas/content/persistence/migration belong to the specified later phases.
- **Coding contract:** [P10 data contract](plan/phases/P10-pet-model/P10-data-contract.md), 23 acceptance scenarios. Canonical authoring IDs in `data/p10/`, exact source mapping in `id_registry.json`.
- **Specification:** [P10 decisions](plan/phases/P10-pet-model/P10-design-decisions.md).
- **Review queue:** [P10 review](plan/phases/P10-pet-model/P10-review.md).
- **Species list:** [P10 roster](plan/phases/P10-pet-model/P10-roster.md); canonical authoring data `data/p10/species.json`; raw source `data/pets/roster_apk84.json`.
- **Assets:** `apps/game-client/assets/pets/apk84/` — 152 portraits and 760 clips.
- **Runtime boundary:** the legacy 14-species gameplay catalog/save IDs remain active until P11/P13/P16 configuration and migration are designed. New roster has source identity/art, not invented stats or elements.
- **Implementation plan:** none for gameplay migration; do not mark P10 closed while decisions remain pending.
- **Historical phase:** P00 closed at `e66350b`; failed dev latency budget and no 50-CCU certification remain recorded there.

Existing unrelated issue: legacy `layout_audit.gd` targets the old scene structure; the active canonical gate is `tools/check.sh`.
