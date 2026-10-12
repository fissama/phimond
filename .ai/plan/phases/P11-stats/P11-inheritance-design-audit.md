# P11 inheritance mathematical design audit

Date: 2026-10-12. Independent design review; no runtime changes.
Authority: prior individually approved decisions remain historical facts. The
alternatives and numbers below are **agent-authored proposals under delegated
design authority**, not additional individual owner approvals or recovered
original-game formulas. Final integrated P11 decision records select the actual
model; this document compares alternatives and acceptance conditions.

## Selected integration model: shifted training potential

The integrating agent selected the following refinement after comparing the
alternatives below. This section is the audit recommendation for integration;
Alternatives A/B remain explanatory comparisons, not competing final defaults.

```text
R[HP,ATK,MAG,DEF,SPD,SR] = [500,50,50,50,100,50]
a[HP,ATK,MAG,DEF,SPD,SR] = [.15,.15,.15,.15,.04,.04]
Q(B) = B + B²/(2R)
effort(p) = max(0,(p.level-20)/(p.base_star_cap-20))
t = min(effort(main),effort(donor))
G = mean(main.grown,donor.grown)
Qchild = max(Qmain,Qdonor) + a*G*t
Bexact = R*(sqrt(1+2*Qchild/R)-1)
Bderived = floor(1000*Bexact)/1000
```

All operations are independent per matching stat. Store Q exactly; Bderived is
a view, not the value converted back into Q at the next fusion. In particular,
never repeatedly compute Q from a previously rounded Bderived. Q is not a
second permanent stat contribution; permanent total includes Bderived once.
Inherited bonuses remain fixed at Egg creation. The effort definition has zero
fresh credit at Lv20, rewards above-base-cap leveling without a clamp at1,
and does not modify the existing fusion eligibility gate or Plus rules.

This curve keeps the practical benefit of exact accumulated training investment
while avoiding Alternative A's comparatively large first jump and immediate
steep drop. For R=G and full effort t=1:

| Fusions | Main B/R | Last main increment/R | Auxiliary B/R |
|---:|---:|---:|---:|
| 1 | .140175425 | .140175425 | .039230485 |
| 2 | .264911064 | .124735639 | .077032961 |
| 3 | .378404875 | .113493811 | .113552873 |
| 10 | 1.000000000 | .076461594 | .341640786 |
| 25 | 1.915475947 | .051911735 | .732050808 |
| 100 | 4.567764363 | .027006292 | 2.000000000 |
| 1000 | 16.349351573 | .008648012 | 8.000000000 |

For ATK R=G=50, the first gain is7.008771 and the 100th gain1.350315,
with total228.388218 after100 fusions. These are fixed-quality mathematical
fixtures, not promises about a Species at any particular level.

Proof: with fixed earned credit E=aGt>0 and a fresh weaker donor each cycle,
`Q_n=Q_0+nE`. The inverse curve has derivative
`dB/dQ=1/sqrt(1+2Q/R)>0` and negative second derivative. Consequently B_n is
unbounded, its successive gains strictly decrease, and B_n grows as sqrt(n).
If E=0, exact principal is preserved with zero new progress. For any bounded
current B, persistent positive lower-bounded E cannot cause permanent stagnation.
Changing G or effort changes that comparison, so never assert successive gains
must decrease across arbitrary improving-quality parents.

Same-investment audit: max(Qmain,Qdonor) counts the stronger consumed investment
once. Repeated split/fuse cannot accumulate Q because split deletes the child
and restores immutable pre-fusion Q snapshots; previously generated E belongs
only to the deleted child. Pet-to-Egg carries Q unchanged and produces no E.
Retrying a fusion must reuse its committed result or fail; it must never add E
again. Storing direct restoration snapshots must include Q, its configuration
version and derived-bonus policy. Parent identities remain unavailable while
consumed. Consuming both parents and restoring only through child destruction
is essential; formula arithmetic alone cannot prevent duplicated entities.

A balanced tree does not sum its two inherited Q values. At equal quality,
its root Q grows with depth; a chain with the same total fusion count generally
gets more Q. Strongest-per-stat selection intentionally preserves complementary
lineage investment without doubling any one matching stat. The newly trained
parents still create one E payment for the current operation.

With rational a,G,t and fixed rational references, Q increments can be exact
rational values in a shared integer scale; storage bounds/versioning remain an
implementation contract. To derive floor-to-.001 without floating square-root
ambiguity, choose the largest nonnegative integer z satisfying
`z/1000+(z/1000)²/(2R)<=Q`; compare rational quantities exactly. This preserves
a deterministic view at exact boundaries. Q residuals survive every operation,
so a temporarily unchanged millipoint bonus is not a permanent cap. Arbitrary
integer growth or an explicit versioned overflow policy is still necessary.
Do not state that fixed-width storage itself supports literal unlimited values.

Assessment: internally coherent and meets the mathematical repeat-grind goal.
It requires the explicit amendments listed next. Numeric pacing is a delegated
design default pending gameplay/economy validation; no test here establishes
EXP-time parity between Stars, PvP balance, or source-game equivalence.

## Finding

The replacement-bonus formula `Bnew = max(Bmain, k sqrt(R M))`, with
`M = mean(grown + bonus)`, has a finite invariant bound when grown stats are
bounded. Increasing k changes that bound, not the existence of a plateau.
For grown stats bounded by Gmax and initial bonuses bounded by C, choose H at
least C satisfying `H² >= k² R (Gmax + H)`. Every future bonus remains <= H,
even with branching, equal-quality donors, max carry or arbitrarily many fusions.
A floor prevents loss but cannot turn this recurrence into unlimited progress.
Integer rounding causes visible stalls even before that mathematical limit.

Repeated meaningful grind without a finite natural bound therefore requires an
explicit change to the response contract, rather than claiming that no hard cap
already provides this property.

## Explicit amendments required

The following must be called out if an accumulation design is selected:

- P10 D14: replace the prohibition on directly preserving parent inheritance
  with one explicit preserved principal, counted once. Grown stats remain
  separate from inheritance and exclude equipment/temporary effects.
- P10 D16: replace the instruction that the old bonus must only enter the
  total-based candidate. Retain diminishing gains, no hard bonus cap, no minimum
  +1, and Main bonus protection. If strongest-parent carry is selected, state
  that donor inheritance is protected too and Normal Star-up also carries it.
- Q14.1: the raw 50/50 mean of permanent totals can remain an inspection value,
  but it is no longer a sufficient input to the whole inheritance function.
  The function now distinguishes old investment from current grown stats.
- Q14.2: fixed per-stat references may be retained unchanged in concept.
- Q14.3–Q14.4: explicitly replace the total-candidate square-root mapping.
  An accumulating square-root response is a different function with additional
  state, not algebraically equivalent to the approved original formula.
- Independent matching-stat calculation, source-gated Special recipes, Egg to
  Lv1 reset, fixed inheritance after creation, and +99 Plus cap stay applicable.

## Principal selection and donor accounting

Let `C[s] = max(main.B[s], donor.B[s])` independently for each stat.
This preserves the strongest investment consumed by the fusion. Parent order
cannot launder an existing bonus into new earned gain; reversing parents leaves
C and the new earned term unchanged when training inputs are symmetric.
Main-only carry is also coherent, but discards the donor's stronger inheritance
when the desired child Species must occupy Main. That discourages donor-tree
investment and creates strong slot dependence. It does not implement the same
product policy as strongest-parent carry.

Per-stat max can assemble the best stats of complementary lineages. It never
sums their bonus values for one stat. This is a deliberate build-combination
benefit, not a free arithmetic increment: both parents are consumed. Define
marginal earned gain as `Bnew-C`, separately from `C-Bmain`, which is an existing
investment transferred from donor. Otherwise a strong donor appears to violate
any promised diminishing marginal gain relative to Main.

Do not use `C + k sqrt(R mean(grown + bonus))`: the principal is retained and
then its inherited value amplifies another additive payment. Gains rise as
principal grows, contrary to repeat-grind diminishing returns. Counting donor
prior bonus again as fresh training creates the same problem.

## Alternative A: accumulated training energy

Illustrative mathematically simple design:

```text
G[s] = (main.grown[s] + donor.grown[s]) / 2
C[s] = max(main.B[s], donor.B[s])
effort(parent) = max(0, (parent.level - 20)/(parent.base_star_cap - 20))
t = min(effort(main), effort(donor))
Bnew[s] = sqrt(C[s]^2 + k[s]^2 * R[s] * G[s] * t)
```

Base caps are the Species Star's base caps, excluding Plus; Special operations
remain blocked pending source/recipe rules. Use each parent's own cap in the
effort calculation. Common fusion eligibility is still both parents Lv20 and
same Star. Above-base-cap levels can give t>1, rewarding Plus-enabled training.
No separate Plus multiplier is introduced. At least one Lv20 parent gives t=0:
fusion may still affect Plus/Species, but creates no additional inheritance
beyond the carried principal. This is an explicit design choice and needs to be
stated; it does not follow from the existing Lv20 eligibility rule.

There is no need to subtract nearly equal floating totals. Evaluate G directly
from grown stats. The historical raw permanent mean is `M=G+mean(B)` and can be
shown in diagnostics, but its inherited part is handled only by C.

For a fixed fresh-donor quality G and fixed t>0, repeatedly retraining the Main
and replacing donor gives `B_n²=B_0²+n*k²*R*G*t`. Therefore B is unbounded,
while each increment decreases to zero. If G/t vary within fixed bounds,
there is an upper bound proportional to sqrt(number of operations); positive
lower-bounded training investment gives divergence. No claim of positive gains
when t=0 or the matching G=0 is implied.

Example-only defaults: R main stats 1000/100/100/100 for HP/ATK/MAG/DEF;
R SPD/SR 100/50; k main 0.20, k auxiliaries 0.08. These are proposed scale
anchors, not a recovered formula or owner-approved balance values. At G=R and
t=1, first bonus is 20% of R for main stats and 8% for auxiliaries. Actual
Species grown values will differ. For ATK R=G=100, k=.20, B0=0:

| Full-effort fusions | Bonus | Increment on last fusion |
|---:|---:|---:|
| 1 | 20.000000 | 20.000000 |
| 2 | 28.284271 | 8.284271 |
| 3 | 34.641016 | 6.356745 |
| 10 | 63.245553 | 3.245553 |
| 25 | 100.000000 | 2.020410 |
| 100 | 200.000000 | 1.002513 |
| 1000 | 632.455532 | 0.316307 |

At C=100, effort 0/.25/.5/1/2 gives incremental ATK
0/.498756/.995049/1.980390/3.923048 respectively, holding G fixed. In real
leveling, G also rises, so this table isolates the effort factor only.

## Alternative B: inverse-square-root marginal payment

Another coherent design, considered by the integrating agent:

```text
Bnew = C + a * R * sqrt(G/R) * t / sqrt(1+C/R)
```

For fixed G,t, gains decline with C and remain positive; B is unbounded and
asymptotically grows as n^(2/3), faster than Alternative A's sqrt(n). This is
not the old `k sqrt(R M)` response: it square-roots grown quality, preserves
principal, and adds an inverse-square-root damped payment. Record all three
changes. At R=G=100,t=1,a=.08, bonuses after 1/2/3/10/25/100/1000 operations
are approximately 8/15.698/23.136/69.984/153.170/454.347/2347.678. First gain
looks smaller than Alternative A, but the long-run curve is much larger.

Using `t=min((Lmain-1)/(capmain-1),(Ldonor-1)/(capdonor-1))` gives positive
payment for both parents Lv20. Endless minimum-level fodder can then produce
unlimited growth, albeit slower. It blocks literal Lv1 fodder via eligibility,
but does not block cheap eligible Lv20 fodder. Choose which behavior is intended
and describe it honestly. Subtracting the Lv20 eligibility threshold instead
makes the marginal term zero at that threshold. Even then Lv21 donors can
produce unlimited growth with enough repeated nonzero effort: a mathematical
formula cannot promise no cheap strategy without actual EXP/economy costs.

## Branching, quality changes, and Star-up

Under strongest carry, two equal bonus lineages do not double their bonuses.
A balanced tree's root bonus reflects its strongest path plus new investment
at each path step; exponentially many equivalent leaves do not provide an
exponential bonus. A chain is generally more resource-efficient in total
fusion count, while parallel lineages can assemble complementary stats.
This intentional weaker reward for redundant parallel inheritance should be
visible in previews. A donor's stronger stat contributes carry, not a second
new-training payout.

Lower grade reduces future grown contribution, but never deletes old principal.
High-level Main plus minimally trained donor is limited by the weaker effort;
it cannot count the Main's previous training as full new two-parent investment.
Higher Star has larger grown stats and higher absolute training requirements;
normalizing by Star cap only defines comparable maturity, not equal EXP/time.
EXP per level, capture rates, materials and leveling automation can dominate
which Star offers the cheapest inheritance. P15/P16/P19 must measure those
costs before calling the curve economically balanced.

Applying strongest carry to Normal Star-up deliberately prevents losing old
inheritance. Output level still resets to Lv1 and Plus resets under P10, so
output total stats may be lower immediately. A low-grade child still preserves
inheritance; new growth grade affects only later grown stats. Special remains
source-gated. Pet-to-Egg conversion preserves existing inheritance without
paying another gain. Splitting restores immutable parents and destroys the
child, so split/refuse cannot preserve the child gain or duplicate principal.

## Fractional precision and visible progress

Flooring each operation's delta can create a permanent artificial stall. Merely
storing six decimals delays that stall: every finite fixed precision has a
smallest nonzero unit and eventually a positive diminishing increment falls
below it. Do not advertise mathematically unlimited progress from a bounded
precision accumulator without this qualification.

Alternative A admits exact latent energy `E[s]=B[s]^2`:
`Echild=max(E_main,E_donor)+k²*R*G*t`. With rational configuration and finite
approved cap denominators, increments are rational and can be stored in a
common exact integer unit; arbitrary-size integers avoid a hidden overflow
ceiling. Old integer bonus imports map to exact squared energy. Compute B as
a square-root view for display/combat; never write its rounded display value
back over E. This changes the storage contract and needs a later implementation
plan. Fixed-width storage requires an explicit safety bound/versioned migration,
not silent saturation. Alternative B needs its own precision proof or different
exact potential formulation; saying 'keep fractions' alone is insufficient.

An integer UI/combat bonus may remain unchanged for many operations even when
exact progress exists. Show the precise preview or progress toward the next
visible point. No guaranteed +1 is added. Arbitrarily long grind and every
fusion giving a visible integer increase are incompatible with diminishing
gains tending to zero.

## Acceptance conditions for whichever model is selected

1. Record amendments above and the selected effort-zero boundary, carry policy,
   Star-up policy, coefficients and reference values as delegated choices.
2. Preserve matching-stat independence. Changes to one parent's ATK must not
   redistribute another stat's bonus; a shared level-effort signal is explicit.
3. Verify fresh-donor chains, balanced trees, asymmetric donor-heavy lineage,
   complementary-stat lineages and swapped slots. Count transferred principal
   separately from newly earned gain in every assertion.
4. For fixed positive trained quality, prove positive diminishing marginal
   gain and unbounded accumulated bonus, then simulate 1/10/100/1000 operations.
5. Verify exactly zero earned bonus at the chosen no-training boundary and
   explain whether Lv20 and Lv21 grinding are intended. Do not claim economy
   exploit resistance from level normalization alone.
6. Exercise decreased grade, pre/post base cap, Plus99, Normal Star-up, blocked
   Special, Lv1 hatch and save/load without inherited-principal loss.
7. Verify split/re-fuse and Pet-to-Egg have no inheritance duplication, growth
   replay or child-progress restoration; parent snapshots are immutable.
8. Store latent progress beyond display rounding and define arithmetic bounds.
   An integer display stall must not overwrite real progression.
9. Distinguish mathematical validation from economic pacing and combat balance.
   Unlimited stat accumulation eventually dominates finite native Species gaps;
   that is a real consequence of the requested unbounded long-run design.

Verification: numerical tables computed with an independent Python calculation
on 2026-10-12. For each selected coefficient .15/.04, 10,000 fixed-quality
steps passed positive strictly decreasing marginal-gain assertions; zero-effort
exact principal preservation also passed. They are illustrations, not automated production tests. No server,
client, database, Species content or other design file was changed by this audit.
