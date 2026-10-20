# P13 — Behavior contract, candidate v3

Date: 2026-10-13. Owner acceptance PENDING. Phimond-authored rules below are
proposals within delegated P13 design. No battle engine or migration is enabled.
Master P13-R01–R06 and accepted P10/P11 remain authoritative.

V2 signature behavior unchanged. V3 supersedes source-tier/rank/AoE/learning
sections below and P13-owner-feedback-v3.md. Slot rationale: P13-owner-feedback-v2.md.

## Independent APK tiers (v3)

Seven damage-AoE families have four IDs: light/regular/advanced/super.
Per-target power .45/.75/1.05/1.35. Physical MP10/18/26/36; magic12/20/28/38.
LearnLv1/5/20/40, CD0/1/1/2, fixedrank1, no rank2/3upgrade; no additional
AoE .75 multiplier. Source tier names/targets/channels have APK evidence;
numbers/gates authored, not decoded original Mana/Dame. Groupheal normal and
super separate fixedrank1: .85MAG+6/28MP/CD2/Lv20;1.10MAG+10/40MP/CD3/Lv40.

Each eligible family expands Native Pool to alltiers. Learning checks exact
ID,level,gold,currentslot and eligibility, never consumes/replaces/locks another
tier unless owner explicitly selected thatID as fullslot replacement. Keeping
light+super takes2/6slots; one currenttier inherited does not grant siblings.
Damage+effect separates damage fromproc; enemy effect-only never infers damage.
Ally AoE heal/buff has no damage/crit/enemy accuracy roll. Each row explicitly
records target_shape and damage_mode, visible/filterable in review UI.

Auto tier tie follows learned-slot priority; farm order light before strong,
burst order can change before battle. No downgrading upgraded nontier skills or
looking ahead at RNG. Quái ties use pool order light first; spawn selects level
valid subset, not every Native skill. Real pacing/AI remains P02/P07 proof.

## Species-exclusive Special signatures (v2)

Seven authored skills have `exclusive_species`; a native pool or acquisition
request from another species is invalid. Empty inheritance prevents donor
transfer regardless of Race/Element; common pool never includes them. A future
species-changing lifecycle must reject incompatible signature ownership before
transaction commit; this does not authorize a new species-changing operation.
Same-species re-hatch retains current skill as in P10. No auto-grant or slot7.
Fixed rank1 overrides generic damage/heal rank policy for these combo skills.
All cost once and CD3; signature4 learnsLv30/MP24, signature5 Lv40/MP28.

- `azure_tide`: damage1.10MAG Water, then one70%base SR-adjusted slow draw,
  SPD−20% for2rounds. Same slow status/group as existing slow, no hard control.
- `tiger_gale`: damage1.25ATK Wind, then successful hit grants selfSPD+20%,
  2rounds in haste group. Missing/invalid target or miss gives no selfbuff.
- `vermilion_ember`: damage1.10MAG Fire, then70%base burn; existing snapshot
  sourceMAG .30-power tick R+1/R+2, no new burn stack/type.
- `turtle_tide`: valid living ally/self, remove burn if present then shield
  floor(1.20MAG+.08sourceMaxHP) for2rounds. No burn prerequisite. Existing shield
  strongest/nonstack policy; no reduced-cost refund if burn absent.
- `empress_eclipse`: damage1.40MAG Dark, then70%base misfortune, receiving
  healing−25% for2rounds. Existing status/SR/cleanse, no instant death.
- `giant_bastion`: damage1.40ATK Earth, then successful hit grants selfDEF+25%
  for2rounds in armor group. No selfbuff on miss or invalid action.
- `flower_radiance`: living ally/self missingHP OR with removable bad status;
  remove1 by generic cleanse priority, then heal floor(1.50MAG+10). Either
  operation alone is valid at full cost; both absent means invalid/free/noaction.
  Cleanse hard control grants existing grace. Misfortune removed before heal
  does not reduce that heal. Cannot revive or restore MP.

Damage signatures use normal hit/crit/chart and water-hit extinguish ordering;
negative procs resolve after damage only for a living target. Selfbuff applies
on successful hit even if that hit kills target, provided source survives.
Selfbuff/heal/shield/cleanse are not amplified by Element chart or crit. Existing
stack caps, expire timing, dispel and channel gates apply. No hidden passive or
automatic signature from Star/Race. New power values need P02/P07 playtests.

## 1. Actions and learning

Each actor has one scheduled action per round. Basic attack is neutral physical
1.00×ATK, 0 MP, zero cooldown; separate from six current-skill slots. Roles are
metadata and confer no automatic skills/bonuses. Common available skills are
strike, heal and guard; they still require explicit learning. A Native Pool entry
permits that Species to learn the skill. A Race whitelist controls inheritance,
not native learning; native eligibility is allowed to be broader than inheritance.
No quest/event/item-only acquisition in this candidate except future trainer/item
integration. Trainers offer every currently eligible Native/Inherited/Common skill;
P12/P19 own placement, access and currency sources. Learning is out-of-battle only.

Learning requires level >= skill.learn_level, ownership, currency and an available
slot or explicit replacement. Confirmation shows old/new skill and exact cost.
Cost rank1 = 20 + 10×learn_level gold; rank2 = 3×rank1; rank3 = 6×rank1, charged
per upgrade, not a cumulative target price. Excludes fixed APK tiers and7
new signatures above. Other damage/heal rank2 learn gate is
max(20, learn_level+15), rank3 max(40, learn_level+30). Rank2/3 scale direct power
or complete heal amount by 1.15/1.30; MP by ceil(base×1.20)/ceil(base×1.40).
DoT, secondary effects/chances, penetration, hit count, duration and CD do not
scale. Fixed-rank buff/control/cleanse/resource/shield/revive skills remain rank1.
Lower ranks cannot be selected to reduce cost once upgraded.

A record of prior learned skill IDs belongs to the pet, not account. Relearning
rank1 costs ceil(0.20×rank1 price), requires its original learn gate, and requires
current eligibility. Forgetting an upgraded skill loses its rank; relearn rank1.
An inherited option never learned on this pet receives no relearning discount.
Upgrade/replace/learn intents have expected pet revision and idempotency key;
currency, slot and history update atomically. Invalid/stale/rejected/cancelled
requests charge nothing. Retry returns the original receipt; UI shows authoritative
state before trying a new operation. Busy intent disables duplicate confirmation;
disconnect shows pending receipt lookup, not assumed success/refund.

Current skills only propagate: union parent current IDs → deduplicate → filter
per-skill inheritance whitelist for child's Race → stable sorted child inherited
pool. No RNG; no Element mismatch filter; no child-level pool filter. Only IDs
propagate, not rank or learned-history discounts. Newly created fusion/capture
Eggs first hatch 0 current skills. Pet→Egg→re-hatch preserves current skills/ranks,
inherited pool and personal learned-history, usable at Lv1 if current MP/other
conditions permit. P16 stores exact snapshots; split restores parent state and
never transfers child's learned history or rank backwards.

## 2. Target and action validation

PvE solo: one lead pet vs three opponents. Party: up to three owners, one pet each.
PvP: three pet per side. All-target skills cover currently eligible living targets
on the declared side, at most three for these modes; single/other/fainted/self
selectors are separate. Ally_one includes self. Ally_other excludes self.
Ally_fainted excludes self and requires a defeated admitted teammate. Skill target
sets and mode limitations are displayed before confirmation. Revive is unavailable
in solo PvE, but native access does not grant a free substitute ability.

At execution, revalidate ownership, active battle/actor, learned ID/rank, target
admission/side/life state, control, MP, cooldown and action rights. A manual target
that becomes invalid is not silently redirected. The actor falls back to its
legal auto policy if available, otherwise basic/skip with a reason, and only the
action actually executed is charged. Invalid RPC alone does not spend action/MP.
No valid enemy for basic means skip; basic under bind means skip, not magic.
A counter reaction is not a new scheduled action and is not blocked by action-list
admission changes; bind prevents its physical hit.

Pet auto uses an explicitly ordered list of its six current skills, selecting
only valid actions. Default: eligible ally/self-heal when HP<40%; matching cleanse; control on a
grace-free target without that status; missing buff; AoE with >=2 enemies;
then single attack; then basic. Support/utility actions require declared triggers:
ally heal picks lowest currentHP/maxHP; cleanse requires matching status; buffs
only when no equal/stronger same-group buff; revive only an eligible teammate.
Tie break target by stable actor instance ID. Enemy AI uses an authored subset
of Native Pool with learn gate <= spawn level and explicit rank; no inherited
skills unless that encounter is authored with provenance. Priority: control absent
and grace-free target; heal ally <40%; AoE >=2; missing buff; single; basic.
Same priority resolves by subset order. No RNG pick of the enemy's entire pool.
P15 owns actual encounter levels/XP, P02 validates AI and auto pressure.

## 3. Round and resource semantics

At each round start: collect living admitted actors, freeze order by P11 effective
SPD descending and its stored battle random tie rank. Every actor has at most one
scheduled action. SPD changes do not reorder current round. Death removes an
actor's unexecuted action. Revive/replacement does not create an immediate action;
first scheduled opportunity is next round. P07 command deadline candidate is 30s
for the selection window; timeout uses valid configured auto, never pauses others
indefinitely. P02 remains default auto with optional valid manual override.

Skill CD C cast in round R is next usable at R+C+1; C=0 permits next round, not a
second action in R. Charge MP once just before the valid action starts; miss still
charges. A skill with all targets invalid is not charged. Single target death during
multi-hit ends that skill's remaining hits without retarget/refund. Battle-local
CD/status ends at battle end. No passive world/battle regen or end-battle refill;
P11 lifecycle/account cooldown policies survive unchanged.

## 4. Resolution order and numbers

Resolve direct effects in this order:

1. Validate action/targets; charge once; set cooldown; snapshot source effective
   damage/heal and rank inputs for this cast, using P11 modifier pipeline.
2. For each target sorted stable instance ID, draw hit. Base hit95%; blind −20
   percentage points, clamped50–95%. Friendly heals/buffs/cleanses have no hit roll.
   Hostile pure control/debuff/dispel requires hit. No SPD hit bonus.
3. Direct damage hit: draw5% crit, multiplier1.50; physical uses ATK, magic MAG.
   Base = offense×power×100/(100+max(0,DEF)); multiply Element and crit then floor
   once. Penetration modifies DEF before denominator. For positive offense minimum
   damage1; offense0 means0. Normal/basic neutral Element factor1.
4. Absorb with shield, then HP loss clamped to current HP; wake a sleeping target
   on successful direct damage even if shield absorbed all HP loss. Mark death.
5. Water direct hit removes burn, after direct damage; no reaction damage/cascade.
   For a surviving target, check explicit status eligibility/immunity; status roll
   p_base×(1−0.80×max(0,SR)/(max(0,SR)+100)). Exactly one Bernoulli per eligible
   status, not proc+resist rolls. Distinct effects draw independently in declared
   catalog order. No automatic status from skill name, Race or Element.
6. Resolve drain from actual HP lost only; floor25%, cap at source maxHP. Do not
   heal dead source. Reactions run after direct action, max one counter/actor/round;
   counter cannot trigger counter. Dead targets do not react.

All probability arithmetic uses exact rationals; production RNG must specify
unbiased rejection sampling and deterministic replay. No intermediate float rounding.
Multi-hit/target rolls are independent, source inputs fixed for this cast; target
DEF and life/status read at each hit. Event order includes hit/crit/status outcomes.
Seeds/private RNG and hidden appraisal inputs are not exposed in public events.

Examples: ATK100,DEF50,power1.20 gives80 neutral,100 favorable,64 unfavorable.
Basic100/50 gives66. AoE0.75× with offense100/DEF50 gives50/target,150 total if
three successful noncrit neutral hits. These are arithmetic examples, not TTK
balance evidence. Heal rank1=floor(1.50×MAG+10); normal group=floor(0.85×MAG+6) per ally; supergroup=floor(1.10×MAG+10),
no rank scaling for either group tier.
Only healing received is multiplied by misfortune0.75; it also affects regeneration
and drain, not revival's explicit HP initialization. Shield is a separate capacity,
not heal, DEF or immunity. Generic shield=floor(1.20×MAG+0.08×source maxHP), kissing
shield=floor(1.80×MAG+0.10×source maxHP); same shield group keeps larger remaining
capacity, refreshes its declared expiry, never sums. Absorbed damage does not feed
lifesteal. Dispel removes shield as one buff and does not restore absorbed HP.

## 5. Status timing and counterplay

Two-round buff/debuff cast in R expires end R+2. DoT/regen has ticks at end R+1
and end R+2, never immediate. At round end process poison then burn, each actor
stable ID, then regen; dead actors receive no later tick/heal. DoT snapshots source
offense at application, uses0.30× per tick and current target DEF/Element, no crit,
rank scaling or new status attempts; SR affects application only. Poison neutral,
burn Hỏa. Reapply same type keeps stronger raw tick potency and refreshes endR+2;
weaker cast cannot replace stronger source/Element. One stack/type, at most two
DoTs. A new shield can absorb DoT. Drain does not occur on DoT.

Sleep and petrify prevent the next scheduled action; confuse replaces it with basic
into one living opponent selected by authoritative RNG, with ordinary hit/crit.
They expire immediately after that action opportunity or end R+1 if unused; at most
one action affected. They do not coexist; reapply while one active is rejected.
Sleep wakes on direct damage, no bonus2×. Petrify temporarily adds25%DEF and still
accepts damage. Every termination (consume/expiry/wake/cleanse) grants grace against
sleep/petrify/confuse through end of the following round. If control applied after
an actor has already acted, it can affect the next round only. Grace is explicit
immunity against these three, independent of SR; no immunity to DoT/debuff.

Bind blocks physical attack actions (including basic); silence blocks channel magic.
Channels are explicit in each skill. Guard/counter/beast_instinct/resilience/protect/
haste/attack_up use utility; physical skills use physical; other skills use magic.
Bind and silence cannot coexist: later application rejected while other active;
same status can refresh2-round duration but CD2 creates a gap without multiple
casters. This anti-lock rule is intentional Phimond design. Blind reduces hit20pp;
misfortune reduces incoming healing25%, not instant kill. Frailty is ATK/MAG−10%,
an explicit adaptation of source vitality debuff briefs; maxHP-changing buffs and
forced-death marks are excluded from v1 to avoid unreviewed exploit/identity rules.

Stat buffs: strongest positive per stat + strongest negative per stat, additive
inside P11 battle_percent; total clamped−50%..+50% per stat. Different named casts
cannot accumulate endless percentages. Armor and protect share DEF group; magic_up
and magic_focus share MAG group. Flat battle stat effects absent in v1. Different
actor inherited stat totals remain untouched. All clear/expire restores calculated
effective inputs without creating HP/MP top-ups.

Generic cleanse removes one negative status with priority hardcontrol → silence/bind
→ stat debuff/misfortune/blind/frailty → DoT, then oldest apply timestamp, then
status ID. Specialized cleanse removes its named status, cost8/CD1. Cleanse must
have something removable at execution; otherwise invalid/no-charge. Enemy dispel
has hit check, removes one buff: shield → ATK/MAG → DEF → SPD/SR; ties oldest then
ID; no SR because removal is not application of a harmful status. No passive buff
is inferred from Race. Water-hit burn removal is deterministic on hit, not a new
status and not resisted by SR.

## 6. Presentation, safety and save boundary

Skill rows show rank, MP, target, Element, cooldown, learn level and eligible source.
Disabled reason distinguishes unlearned/MP/level-to-learn/control/cooldown/invalid
mode/target. Tooltip explains single/group, direct and secondary components;
no “cannot use at low level” for preserved skills. Current pool is displayed
separately from options; before replace/fusion show exact current skills that will
propagate, filtering reasons, output0/6 and relearning costs/gates.

Combat presentation consumes server receipts/events once by battle+sequence;
terminal damage/status/result before returning world. Reconnect snapshots do not
replay old VFX or charge resources. Public events include source/target instance,
skill/rank, actual resource deltas, hit/crit and status outcomes; text explains
resisted versus immune/grace versus invalid target. Keep HUD/log readable under
Low/Medium/High settings; no graphics preset changes gameplay probabilities.

Pin ruleset/catalog versions in saves and battles. No inferred14→152 mapping or
“nearest skill name” conversion. Learned-history/rank fields and parent snapshots
need explicit compatibility/backfill/rollback proof before activation. Review UI
is an authoring tool, not gameplay HUD. Its feedback endpoints mutate only local
P13 review JSON; no accounts, DB, item inventory or original game services.

## 7. Acceptance and ownership

P13's design exit: owner approves explicit decisions/catalog/chart, including
physical/magic, basic0skills, neutral/counter/synergy/cleanse examples and mode tags.
24 scenarios are in review-package.json. Static tests prove consistency and exact
sample arithmetic only. P02 owns runtime1v3/AI/idempotency/replay; P07 owns party/
PvP/formation/deadlines and multi-owner authority; P14 owns gear interaction budgets;
P15/P19 own actual costs/time-to-regain-usefulness. Live playtests must challenge
stall, control pressure, AoE value, MP exhaustion, repeated-heal economy, revivals
and signature uniqueness. P13 requires a versioned revision when tuning rules;
no test result or agent-authored pool counts as owner approval.
