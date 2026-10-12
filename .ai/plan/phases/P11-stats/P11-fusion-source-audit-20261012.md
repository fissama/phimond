# P11 — Fusion investment: source audit, 2026-10-12

Status: research evidence and design recommendations, **not owner approval of
new numbers or mechanics**. No runtime, simulation harness, original-server
experiment, or server formula recovery was performed. This audit owns only
this document. P10 and accepted P11 decisions remain authoritative.

## Finding

The sources support a long-term breeding loop that rewards parent preparation,
skill selection, species progression and repeated fusion. They do **not**
establish that the original uses a square root, a particular inherited-percent
target, a guaranteed minimum increase, or an unlimited useful stat gain at +99.
An inheritance function can be unbounded as an input function while a repeated
breeding loop with bounded parent training reaches an effective plateau.

The owner's concern about substantial grinding producing a tiny result is a
real design risk in Phimond's current contracts: a newly fused pet hatches at
Lv1 with zero current skills, while retained inheritance may barely change.
Preserving the old inherited bonus prevents lineage loss; it does not repay
the current parent's level grind or restore immediate battle utility.

## Freshly inspected evidence

### Developer description: revived iOS version

[Spirit Beast World, developer Hung Do](https://apps.apple.com/vn/app/spirit-beast-world/id6446976981),
read 2026-10-12. The description promotes repeated combination and idle
leveling. It states fusion requires two different Races, at least Lv20 and a
matching recipe; the result is an Egg whose child can inherit skills and
beneficial attributes. This supports inheritance as a progression feature and
leveling assistance as part of the product context. It does not specify a
numerical transfer rate, the child's level, relearning costs, or the exact
parent-consumption transaction. The Vietnamese parent wording is ambiguous;
do not use it to override P10's lifecycle rules. iOS 7.9.9 listing prose is not
proof that Android 8.4 and historical Java have identical rules.

### Firsthand guide: parent selection and cheap breeding

[2010-08-05 player guide](https://m.ali213.net/gonglue/100805/10818.html),
read 2026-10-12. Recommends repeatedly breeding one-Star pets toward +50,
matching physical parents with physical goals and magic parents with magic
goals, and learning skills before fusion. It recommends EXP items/sharing and
warns that a high-EXP-requirement pet slows training. Its appraisal and growth
examples are player testimony, not a recovered authoritative formula.

### Firsthand guide: second-generation Hell Owl preparation

[2010-10-27 Hell Owl guide](https://m.ali213.net/gonglue/101027/10193.html),
read 2026-10-12. The author describes collecting desired control/support skills
from Lv20 donors, accumulating Plus on cheap pets, choosing parents to improve
the desired attributes, and training important parents to maximum level.
It says the first Big Fat Bird result often has low inheritance and recommends
a second generation before proceeding. A claimed fast training session relies
on large EXP multipliers; it is not evidence of ordinary free-player pacing.
Its recipe route supports deliberate stat specialization, not a uniform
percentage gain or guarantee that every pairing helps.

### Firsthand guide: Dodo lineage and visible milestones

[2010-10-27 Dodo account](https://m.ali213.net/gonglue/101027/10187.html),
read 2026-10-12. The author narrates roughly two months toward a desired species,
then second/third generations; max-level preparation is repeatedly emphasized.
The account reports donor inheritance around600 and a second-generation Dodo
around1500. These refer to different pets and incompletely specified states,
so they are **not** a measured600→1500 gain or calibration pair. Skills must
be learned before each intermediate fusion; a later generation can omit the
initial skill-collection step. This is one player's experience of meaningful
lineage progress, not general retention or satisfaction evidence.

### Android8.4: directly rechecked archive and extracted assets

Archive: `/Users/phileanh/Downloads/Spirit Beast World 8.4 (1).xapk`.
SHA256 freshly verified:
`b8e02a75e49d5d02703a0b05ec52b450cdfaf69d544f04df2f4a2a465199a18e`.
Read primary `com.HCGame.SpiritBeastWorld.apk` in memory; inspected
`assets/bin/Data/Managed/Metadata/global-metadata.dat` (7,830,952 bytes).
Identifiers include `KeThua`, `KeThuaBanDau`, `KeThuaBanDauModel`,
`PokeKeThuaModel`, `KetHopPoke`, `UpdateTextShowKeThua`, `TCSucManh`,
`TCTinhThan`, `CTSucManh`, `CurrentMP`. Names corroborate separate inheritance,
growth and resource concepts; string presence cannot recover execution logic.

Rechecked [roster extraction](../P10-pet-model/evidence/apk84-roster-extraction.json):
`PokeModelData` contains identity, parent, Race, Star and description fields;
its recovered schema has no numeric base/growth table. `PokeInfo` includes
`Level`, `LevelMax`, `Cong`, separate stat groups, `ListSkill` and equipment;
`InfoPokePanel` includes `CoSo`, `PhuTro`, `KeThua`, `BanDau`, `TuChat`.
This supports distinct displayed components, not the arithmetic joining them.
It does not prove numeric data is absent elsewhere.

Rechecked [selected item descriptions](../P10-pet-model/evidence/apk84-selected-items.json):
full/individual aptitude refresh, Plus candy, Special fusion materials and
4/5-Star split items exist as described capabilities. No transfer percentage,
probability, eligible Egg policy or reset-cost schedule is recovered here.

### Supplied video: limited visual evidence

[Pokezoo video](https://www.youtube.com/watch?v=FXJtLBPoGgo).
Freshly viewed local `tools/.cache/reference/video/overview.jpg` and
`tools/.cache/reference/video/0210.png`. The latter shows a learned-skill
list with level and MP columns and a water-spell tooltip. It does not show a
fusion transaction, parent/child before-and-after totals, or training time.
The contact sheet confirms gameplay/pet UI, not numerical inheritance.
[Existing video audit](../../../../docs/research/VIDEO_UI_AUDIT_2026-09-23.md)
likewise records fusion/ranch interfaces as not clearly demonstrated.

A fresh web search for the game's inheritance formula produced no usable
primary formula source. No unrelated search results were used as evidence.

## Consequences for Phimond's approved design

1. **Judge the payoff at matched level and as time to regain usefulness.**
   Comparing Lv1 child to max-level parent conflates reset cost with inherited
   improvement. Compare both at the same legal level, then separately measure
   the time/EXP/skill cost required to regain the parent's practical role.
2. **Separate level investment from lineage preservation.** P10's per-stat
   reinforcement floor preserves the main's old bonus, not its grown totals.
   P11's current-total inputs make higher levels potentially valuable; neither
   rule promises a worthwhile marginal return on the final training hours.
3. **Treat inherited skills as retained options, not current combat power.**
   P10 D36–D38 preserves eligible learned-parent skills in the child's learnable
   pool, while new fusion hatch starts0/6. P13 must specify learning gates,
   costs and early recovery of a usable loadout; a tiny stat gain cannot be
   justified by merely counting inaccessible skills in a pool.
4. **Do not sell Plus as direct stat strength.** In Phimond Plus raises the cap
   only. Its potential becomes strength after retraining. At +99 even this
   cap reward stops; another fusion needs an explicit purpose visible to the
   player, or an honest preview that it offers no useful stat improvement.
5. **Calibrate an actual loop, not just a curve.** Compare low-level/max-level
   donor, weak/strong donor, fresh/reinforced main, same-species reinforcement,
   Star-up, and +99 under identical growth assumptions. Record all six bonus
   deltas, same-level totals and costs. Include fresh child-profile variance:
   a preserved bonus alone does not prevent worse eventual totals.

These are recommendations for P11/P13/P15/P16/P19 to resolve; they introduce
no new floor, refund, catch-up multiplier or source-claimed rule. In particular,
do not silently reopen P10's no-automatic+1 and Lv1/skill-reset decisions.

## Recommended next design gate

Before choosing inheritance coefficients, agree what a well-prepared fusion
must accomplish at early, middle and +99 progression, and what retraining cost
is acceptable. Require visible, useful early/middle progress under intended
training rather than merely a nonnegative mathematical bonus. At late plateau,
show the projected stat result and remaining skill/species purposes honestly.
If the desired payoff is perpetual meaningful stat gain at fixed cap with
bounded training, explicitly revisit the accepted curve/loop requirements;
source evidence cannot certify that requirement or choose its replacement.

No numerical percentage or generation count is approved by this audit. The
original square-root formula, exact transfer rates, skill costs, maximum-level
premiums, ordinary retraining durations, +99 long-run behavior and Special
Plus outcome remain unverified.
