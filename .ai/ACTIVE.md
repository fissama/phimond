# Active Development

- **Last reviewed:** 2026-09-28
- **Phase:** P10 — pet model foundation, design review in progress.
- **Current objective:** adopt the 152-species APK 8.4 roster/art and debate remaining pet/stat/fusion contracts with the user.
- **Accepted:** original Race × Star distribution; MP as a P11 resource; growth reroll after Pet → Egg; APK-defined Special species/recipes/materials; basic attack available at zero learned skills; independent Race/Element and one Status Resistance.
- **Current question:** distinguish the grown stat component, fixed inheritance, permanent total and equipment; choose player-facing stat display before finalizing D14/D21/D22.
- **Specification:** [P10 decisions](plan/phases/P10-pet-model/P10-design-decisions.md).
- **Review queue:** [P10 review](plan/phases/P10-pet-model/P10-review.md).
- **Species list:** [P10 roster](plan/phases/P10-pet-model/P10-roster.md); machine data `data/pets/roster_apk84.json`.
- **Assets:** `apps/game-client/assets/pets/apk84/` — 152 portraits and 760 clips.
- **Runtime boundary:** the legacy 14-species gameplay catalog/save IDs remain active until P11/P13/P16 configuration and migration are designed. New roster has source identity/art, not invented stats or elements.
- **Implementation plan:** none for gameplay migration; do not mark P10 closed while decisions remain pending.
- **Historical phase:** P00 closed at `e66350b`; failed dev latency budget and no 50-CCU certification remain recorded there.

Existing unrelated issue: legacy `layout_audit.gd` targets the old scene structure; the active canonical gate is `tools/check.sh`.
