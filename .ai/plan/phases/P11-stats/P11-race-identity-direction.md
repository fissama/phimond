# P11 — Race identity direction, 2026-10-12

Status: **Bird comparison policy owner-approved and authored in catalog v1.1**.
The owner approved the seven other Race directions on2026-10-12; catalog v2 now authors them. Runtime is not activated.

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

## Owner-approved Race directions

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

The owner approved this direction table and delegated concrete Species tradeoffs. Six stats need not provide
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

V1.1 implemented only Bird ordering. V2 additionally authors the approved seven
Race directions, per-Species accents and descriptions; see the revision below.

## Catalog v2 — concrete authoring choices

The percentages below are agent-selected authoring strengths under the approved
directions, not recovered APK values or separately approved numerical answers.
They apply to exact templates before quantization, independently at Lv1/growth.

| Race | Main-stat emphasis | Separate auxiliary / native brief |
|---|---|---|
| Bird | Per-Species accent | Preserve v1.1 SPD priority |
| Beast | HP +6% | Endurance; paid from other main stats |
| Dragon | DEF +6% | Defense; paid from other main stats |
| Spirit | MAG +6% for M/H/S/D; no forced MAG emphasis for P/T | Preserve physical/Tank role |
| Demon | Main damage channel +6%; Hybrid ATK/MAG +5% each | Burst direction must fit actual role; Support retains ally function |
| Undead | Per-Species accent | SR at highest representable value <=105% target |
| Plant | HP/MAG +4% each for M/H/S/D; HP +6% for P/T | Ally sustain for Support; self/protection utility for other roles; no auto-heal |
| Insect | Role-compatible attack +3%; Tank DEF +3% | Attrition/control direction; pure DoT does not create Disruptor |

Every ID has an explicit +2% accent (HP/ATK/MAG/DEF); dual-damage accents split
+1% ATK/+1% MAG. The builder lists these IDs explicitly, without random jitter.
The expense is subtracted proportionally from unboosted main-stat allocations
in normalized budget units. If insufficient donor budget exists, reduce all
boosts uniformly so donor loss is at most8%; no budget is minted. Quantize
nearest integer/.001, clamp to representable +/-10% bounds and validate every
role/budget guard afterward. Actual modifiers and budget drift are in the JSON.
All auxiliary templates stay intact; no non-Bird SPD boost is introduced.

This revision creates137 distinct vectors versus94 in v1.1;27 Species still
share vectors. Equal stats are allowed when roles/native briefs differ; P13 must
supply distinct usable kits rather than assume static numerical uniqueness
establishes combat balance. All152 authored descriptions avoid “nhất”;97 source
quotes are preserved verbatim and55 remain explicitly missing.

## Roster160 / roles4–5★ follow-up, 2026-10-13

Race IDs of source152 are unchanged. The eight new authored additions use the
same approved Race directions, and14 existing role blends are revised. The
[effective catalog160](P11-species-catalog-160.md) regenerates all affected
base/growth/MP without changing the Race modifier strengths or budgets.
Bird proof now covers67 actual pairs and252 template cohorts. Changed role
factors can change a Bird's previous SPD value, while preserving its advantage
in the new ordered-role cohort. Native skills and measured battle value remain P13.
