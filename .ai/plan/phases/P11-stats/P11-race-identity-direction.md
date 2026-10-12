# P11 — Race identity direction, 2026-10-12

Status: **Bird comparison policy owner-approved and authored in catalog v1.1**.
The seven other Race identities below remain proposed; runtime is not activated.

## Owner steering

“Mô tả đó hiện tại có thể điều chỉnh lại, loại bỏ các chữ nhất. Nhưng mà ưu tiên
[từng] Race có mỗi ưu điểm giúp mình, như Chim thì nên có SPD cao nhất giúp mình.”

Accepted direction:
- Source-derived descriptions may be adapted for Phimond. Remove absolute
  species-level claims such as “cao nhất/mạnh nhất/tốt nhất” from authored
  gameplay descriptions; do not erase the archived verbatim source evidence.
- Every Race should have a recognizable advantage. Bird is the speed-leading
  Race. A specific old description does not override this new design intent.
- Frozen Race identities remain; looking like a bird does not move a Dragon or
  Beast Species into Bird. Element remains independent from Race.

## How this fits existing P10/P11

Race identity is an **authoring constraint on Species base/growth and native
function briefs**, not an extra multiplier applied at hatch or in combat.
Species numeric values embed all authoring decisions once. Main budgets and
role guards still apply; being a Dragon or Special is not permission to win
all stats. The already approved Species modifier bounds are the starting scope.
Any necessary change to an auxiliary template/band must be explicit.

Role defines dominant battle function; Race defines a shared tendency and
tradeoff. Species can specialize within both. Individual growth, inheritance,
level, equipment and effects can still change an owned matchup.

## Proposed identities for the remaining Races — not individually approved

| Race | Distinctive direction | P11 expression | P13 function / tradeoff |
|---|---|---|---|
| Bird / Chim | Lead speed | Higher SPD authoring priority | Initiative/mobility utility; lower bulk where role permits |
| Beast / Thú | Large health reserve | HP emphasis | Sustained physical presence; less specialized magic utility |
| Dragon / Rồng | Durable defense | DEF emphasis | Sturdy mixed offense; reduced speed or another main allocation |
| Spirit / Linh | Magic aptitude | MAG emphasis for suitable roles | Magic/utility tools; reduced physical or bulk investment |
| Demon / Ác Ma | Offensive pressure | Primary damage-stat emphasis; Hybrid can split | Burst with resource/cooldown or durability tradeoff |
| Undead / Vong Linh | Resist disruption | Incoming Status Resistance emphasis | Persistence; no free immunity or automatic regeneration |
| Plant / Thực Vật | Recovery and protection | Sustainable HP/MAG allocation by role | Ally heal/protect/cleanse; lower initiative or direct damage |
| Insect / Côn Trùng | Attrition and disruption | Allocation supporting intended kit | Control/debuff/DoT with output tradeoffs; pure DoT alone is not Disruptor |

These are a recommendation for owner discussion. Six stats need not provide
eight unique stat maxima; some Race advantages are concrete native functions.
MP/SR do not imply learned skills. SR is incoming resistance, never outgoing
control potency. No automatic Race skills, immunities or damage multipliers.
A Physical Spirit or Support Demon keeps its role; do not force every member
into the Race's most common role to satisfy the identity table.

## Bird comparator — selected A by owner

**A — APPROVED:** compare the same Star/class, role blend, level and grade,
zero inheritance/gear/buffs. Bird occupies the higher SPD authoring band;
other roles or invested individuals can be faster. V1.1 has a strict integer base SPD advantage and nonlower growth in every
checked cohort. Therefore common-grade cumulative-floor growth preserves the
strict advantage at every legal level. Compare the complete ordered
Primary/Secondary blend; changing Secondary changes the cohort.

**B — NOT SELECTED:** stronger requirement: at the same Star/class/level/grade, every Bird beats
every non-Bird, even Tank versus Disruptor. Existing role factors and ±5% bounds
cannot guarantee this. Example: solo Tank maximum .90×1.05=.945 while solo
Disruptor minimum1.10×.95=1.045 of the same neutral target. Even the actual
Bird Tank/Support blend maximum(.75×.90+.25×1.05)×1.05=.984375 is lower.
This option needs a deliberate SPD authoring-template/band revision.

Neither interpretation promises a low-level Bird beats a fully trained,
inherited or buffed non-Bird. Normal/Special comparison must use the same class
or explicitly define whether premium overrides Race ordering.

## Description authoring rule

Add a Phimond gameplay-description field separate from source_description_vi.
Use measurable tendencies and intended functions, e.g. “Thiên về tốc độ, hỗ trợ
đồng đội và tấn công vật lý; sức chịu đòn hạn chế.” Avoid “nhanh nhất” for an
individual Species. Record the Bird speed policy at the Race level with its
comparison conditions. Do not merely strip a word while leaving an unsupported
stat/skill claim. Descriptions must match the eventual authored values and kit.

## Current Bird authoring rule and remaining scope

Catalog v1.1 authors Bird SPD at floor-to-grid(1.05 × exact role/Star target),
integer base and .001 growth separately. Flooring keeps it within the existing
inclusive+5% bound; it is not an extra multiplier during runtime growth.
Other Races use the existing neutral rounded target. No main-budget increase.
The validator checks current cross-Race pairs plus252 possible template cohorts.
At matching cohort, base_Bird>base_other and growth_Bird>=growth_other prove
strict grown SPD ordering for every common positive grade multiplier and level.
Future non-Bird or Bird modifiers must retain this invariant; +5% by itself is
not permission for future non-Birds to tie Bird SPD.

Next authoring revision can resolve the other seven Race profiles and remaining
catalog-review findings. This update implements only the specifically approved
Bird ordering; it does not claim all proposed Race signatures are complete.
