# P10 — Full review and implementation gates

Reviewed: 2026-09-28. Scope: current repository, user decisions in this discussion,
152-species extraction and selected P10 item evidence. No new original-game
server behavior was recovered by this review.

## Verdict

**The foundation is coherent enough to implement catalog/model validation.
The full pet/fusion gameplay is not implementation-complete or ready to enable.**
P10's design gate permits deferred rules with named owners; it does not require
P11/P13/P16 numerical content now. No phase-delivery claim, runtime migration,
or original-server balance certification is made here.

Ready: taxonomy, 152 identities/art, 8 races, Star/Plus model, stat vocabulary,
Egg/re-hatch/reroll contracts, six current skills, per-skill eligibility,
reinforcement at +99, diminishing inheritance with per-stat main floor,
restoration ownership/equipment/mail behavior, and stable authoring IDs.

## Findings and disposition

| Finding | Impact | Disposition |
|---|---|---|
| Glossary still forbade reinforcement at +99 | Could reinstate a rejected gate in code | Fixed to accepted cap-only behavior |
| Master still questioned one/two blueprints per target | P20 could implement a different unlock model than D23 | Fixed: one target knowledge unlock; Special reinforcement remains gated |
| Master said child inherits growth/learned skills | Could copy growth or auto-teach skills | Fixed: new growth; inherited learnable pool; fusion newborn has zero learned skills |
| Special draft said normal reinforcement allowed despite unknown source rules | Could silently invent an APK rule | Marked explicitly blocked pending source verification (O02) |
| Source IDs were used as future domain IDs; APK item group mistaken for unique identity was possible | Renaming/localization and future migration risk | Frozen canonical registry, English fields, separate source IDs and localized text |
| No concise contract or indexed future acceptance cases | Implementer had to reconstruct decisions from debate | Added data contract with 23 scenarios and phase ownership |
| Snapshot “exact restore” appeared to include old owner/equipment | Could duplicate items or return pets to wrong account | Intrinsic snapshot boundary explicit; current owner and removed equipment handled separately |
| Numerical inheritance still unresolved | Cannot claim balanced diminishing growth or stable long-run stats | Deferred to P11/P16/P15, O04; no invented constants |

## Open register

Only this table is the active blocker/dependency register. P10-review.md retains
comparison rationale; it is not a second implementation checklist.

| ID | Unresolved contract | Owner | Blocks / evidence needed |
|---|---|---|---|
| **P10-O01** | Special fusion Plus, order interchangeability, level validation, costs/quantity, success and inheritance | Original-game research → P16 | Activation of all 17 Special recipes. User explicitly chose to wait; require original client/server evidence or reproducible observed behavior. Current catalog remains disabled |
| **P10-O02** | Whether Special species can Reinforce and whether extra restrictions apply | Original-game research → P16/P20 | Special reinforcement and its formula unlock; catalog identity alone is insufficient |
| **P10-O03** | First-hatch HP/MP initialization; HP/status/cooldown semantics on re-hatch and exact restoration | P11/P13/P16 | Resource initialization code. Re-hatch full recalculated MP is already decided; do not reopen it or infer other resources |
| **P10-O04** | Numeric growth, inheritance gains/precision/rounding, Plus below99 and mixed-Plus pairs | P11/P16; P15 simulation | Stat/fusion implementation. No hard inheritance cap, diminishing gain and reinforcement floor already decided. Must test long sequences, weak/strong donors, swap slots and Star-up; no minimum +1 inferred |
| **P10-O05** | Element assignments, role/stat/growth configuration, native skills and per-skill eligibility for 152 species | P11/P13 | Runtime content activation. Native pool counts may differ; do not parse source descriptions into mechanics |
| **P10-O06** | Egg/Pet instance-ID persistence, versioned snapshots, locking/idempotency and recursive restoration references | P16 implementation plan | Persistence code; prove no duplicate owned instance, loss of ancestry, replayed split or re-hatch duplication |
| **P10-O07** | Mail retention/capacity/claim ordering, pet/item binding across valid transfers | P19/P08/P16 | Mail/trade integration. Overflow/current-owner decisions are fixed. No automatic expiry or transferability policy has been invented |
| **P10-O08** | Explicit legacy14→canonical152 species mapping and stat/save migration | P11/P13/P16 implementation plan | Runtime switch. No matching by name/appearance/index. Need copied-save tests, backups, version gates and rollback |

O01/O02 are source-verification blockers. O03–O08 are later-phase design or
implementation dependencies. They do not justify silently changing approved
P10 behavior, nor do they block read-only encyclopedia/model work.

## Recommended implementation order

1. Catalog reader/validator with canonical IDs; reject unresolved content when
   activating gameplay, while permitting read-only identity/art views.
2. P11 stat/growth/resource rules and P13 skill/Element content; approve numerical
   simulations before coupling them to owned save records.
3. P16 owned lifecycle and atomic operations with P19 mailbox support; implement
   contract scenarios C01–C23 as corresponding features become available.
4. Explicit legacy migration on copied saves and versioned rollout.
5. Enable Special features only after O01/O02 evidence is reviewed.

Do not enable incomplete gameplay just because a JSON file parses or all source
portraits exist. No build implementation plan is approved by this audit alone.

## Verification for this review

Run `python3 tools/content/p10_catalog.py` and its negative-input tests to verify
normalization and references. Source asset validation uses the existing Godot
check. Build/server health confirms the legacy runtime still starts; it does
not demonstrate unimplemented P10 gameplay. Exact commands/results are appended
to P10-verification.md after execution.
