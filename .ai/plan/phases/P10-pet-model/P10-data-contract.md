# P10 — Data contract for implementation

Status: reviewed authoring contract, 2026-09-28. No runtime/save migration yet.
Gameplay decisions are [D01–D46](P10-design-decisions.md). Open gates are tracked
only in [readiness](P10-readiness.md); research history stays in P10-review.md.

## 1. Layers and authority

| Layer | Location | Authority |
|---|---|---|
| Raw source | `data/pets/roster_apk84.json`, `evidence/` | APK observations; preserve original IDs/text |
| Canonical authoring | `data/p10/` | New catalog IDs and normalized cross references |
| Product behavior | P10-design-decisions.md | User-approved behavior, including deliberate departures from APK |
| Runtime legacy | existing `data/{pets,items,skills,recipes}/` | Currently loaded/save-compatible content, not the new P10 model |
| Numeric configuration | future P11/P13/P16 content | Must be approved before feature activation |

Priority: latest explicit user decisions → phase decisions → master summary.
Do not resolve conflicts by treating source descriptions as approved mechanics.
Unknowns remain gated, never represented as free cost, zero stat or default skill.

## 2. Catalog fields and names

Conventions and all allocated IDs: [catalog README](../../../../data/p10/README.md).

| Entity | Canonical fields | Invariant / missing content owner |
|---|---|---|
| Species | `id`, `display_name`, `description`, `race_id`, `star`, `species_class`, `assets`, `source` | 152 records; exactly one Race/Star/class; text can change without changing ID |
| Species later | `element_id`, `base_stats`, `growth_baseline`, `role_ids`, `native_skill_ids` | P11/P13; omitted until configured, not inferred from source prose |
| Item reference | `id`, localized text, `adoption_status`, `enabled`, `source` | Eight selected references only; two Special material identities adopted, others source-only |
| Special recipe | `id`, `kind`, `target_species_id`, `main_species_id`, `secondary_species_id`, `material_item_id`, `material_quantity`, `enabled`, `blocked_by` | 17 exact pairs; no wildcard parents; disabled while P10-O01 unresolved |
| Formula knowledge | account-owned set of `species_id` | A blueprint unlocks target knowledge, not a single-use fusion permission; physical blueprint item IDs assigned by P20 |

Canonical operation names: `star_up`, `reinforcement`, `special_fusion`,
`pet_reversion`, `hatch`, `split`, `growth_reroll`, `mail_claim`.
Do not use `synthesis` for one specific branch; it is a legacy umbrella term.

Core stat keys: `hp`, `atk`, `mag`, `def`, `spd`, `status_resistance`.
`mp` is a separate resource; P11 determines how max MP is derived.
Use `inheritance_bonus` consistently, replacing conceptual aliases
`fixed_inheritance_by_stat` / `child.inheritance` in new code.
Derived terms: `grown_stat`, `permanent_total`, `overview_stat`.

## 3. Owned data (contract, not an implemented wire schema)

All dynamic entities carry `schema_version`, a server-assigned instance ID and
`owner_account_id`. Never use `species_id` as an individual pet's ID.

| Record | Required concepts | Constraints |
|---|---|---|
| Pet | `pet_id`, `species_id`, `level`, `xp`, `plus`, `gender`, `growth_profile`, `inheritance_bonus`, `current_skill_ids`, `inherited_skill_ids`, `lineage_id`, location/binding | `level >= 1`, `0 <= plus <= 99`, at most six unique current skills; no stored Race/Element that can diverge from Species |
| Egg item instance | `egg_id`, `item_instance_id`, `species_id`, `plus`, `gender`, `growth_profile`, `inheritance_bonus`, skill pools, `origin`, restoration/reversion references | Individual payload, not a stack count interchangeable with other Eggs. Hatch validates active-team capacity before consumption |
| Lineage/restoration record | record ID/version, ordered two-parent references, immutable intrinsic snapshots and each parent's prior restoration reference | Direct references suffice; preserve prior ancestry/restoration links so restoring a fused parent does not erase its own history. No full-tree traversal requirement |
| Mail attachment | mail/attachment ID, recipient, equipment or restored-pet reference, pending/claimed state | Exact-once ownership transfer; pending pet unavailable for use/trade; preserve restored state |
| Learned formula | account ID + target `species_id` | Unique pair; reusing known blueprint rejects without consuming it |

`origin`: `capture`, `star_up`, `reinforcement`, `special_fusion`, `pet_reversion`,
or explicit acquisition source defined by later content. New fusion/capture Eggs
have zero learned skills; `pet_reversion` preserves current learned skills.

P16 implementation plan must choose the Pet↔Egg instance-ID strategy and
persist it explicitly. It must preserve logical identity/reversion linkage and
never create two usable copies. Re-hatch is not a new fusion lineage event.
This storage choice is a technical gate, not permission to alter gameplay.

## 4. Lifecycle contracts

| Operation | Preserve / derive | Result and constraints |
|---|---|---|
| Capture | Species selected by content; new growth profile | Only eligible wild 1★; Egg, not immediately an owned combat Pet |
| Normal Star-up | Target Species from known formula; two same-Star Lv20+ parents, at least one target Race | Consume both + costs; next Star; Plus 0; new growth, fixed inheritance; Egg → Lv1; zero learned skills |
| Reinforcement | Main Species/Race/Element/Star; parents same Star and Lv20+ | Consume both + costs; output Plus ≤99, main99→99; new growth and inheritance; per-stat inheritance floor at main bonus; Egg → Lv1, zero learned skills |
| Special fusion | Exact source target and ordered pair at same Star | Gate P10-O01/O02; do not borrow normal Star-up Plus/reset or minimum-level rules as APK facts |
| Pet reversion | Species, Plus, gender, growth, inheritance, learned skills, lineage/restoration | Unequip to inventory/mail; Egg; no automatic reroll |
| Hatch | Existing Egg growth/inheritance | Requires free active slot of 3; consumes Egg only on success; Lv1/XP0. Re-hatch recomputes max MP and fills it; HP/first-hatch resource initialization tracked in P10-O03 |
| Growth reroll | Inheritance, Species Lv1 base and parent snapshots fixed | Egg-only; replace all or one selected stat's growth; new profile may be better/equal/worse |
| Split | Restore intrinsic pre-fusion parents, not child's progress | Consume child Egg + split item; no refunds; current owner gets parents; store first, overflow to mail; no restored equipment |
| Mail claim | Same pet/item and ownership | Require destination space; no pet reset/rehatch, no duplicate copy; claim once |

A pet in battle, retired/consumed, pending mail, trade escrow or another mutation
cannot simultaneously be used as a fusion input. Two distinct parent instances
must be owned/available to the caller. Server validates before consuming inputs;
failed validation has no cost. Transactions lock/check current ownership and
revision, not only client/UI state. Binding specifics still belong to P08/P19.

Inventory overflow authorization is specific to returned equipment and restored
parents. It does **not** override the accepted hatch rule (active team 3/3 rejects
hatch) or silently route every future reward into mail.

## 5. Stat and skill invariants

- `permanent_total[s] = grown_stat[s] + inheritance_bonus[s]`, once.
- Parent inheritance input excludes equipment and battle effects.
- Reinforcement floor: `child.inheritance_bonus[s] >= main.inheritance_bonus[s]`.
  Applies to bonuses, not high-level totals; not automatically to Star-up/Special.
- Inheritance gains diminish, no hard bonus cap. No automatic minimum +1;
  precision/rounding must be designed before simulation claims are made.
- +99 does not close reinforcement; it limits Plus and level capacity only.
- Raw Status Resistance can receive inheritance; resulting probabilities must
  remain valid [0,1]. P11/P13 choose the conversion; this is not a hard cap on raw
  inherited bonuses or an automatic immunity rule.
- Only parents' current skills contribute to the child's inherited pool.
  Deduplicate and apply per-skill eligibility. Different Element alone does not
  exclude; level gates learning, not pool membership or preserved-skill use.
- Native pool size varies by Species. Six current skills remain the active limit.
- No growth-profile copying from parents. New fusion resets learned set even if
  main Species is preserved; only reversion/re-hatch preserves it.

## 6. Implementation acceptance scenarios

These are required future gameplay tests, **not claims of implemented behavior**.

| ID | Scenario / expected assertion |
|---|---|
| C01 | Capture eligible wild1★ produces an individual Egg; wild2★ capture rejected |
| C02 | Team3/3 hatch fails with Egg and costs intact; free slot hatches Lv1/XP0 |
| C03 | Re-hatch preserves skills/growth/inheritance/Plus, recalculates/full MP |
| C04 | Reroll modifies only intended growth keys; no inherited/snapshot mutation |
| C05 | Main+99 reinforcement accepted, result+99; retry does not consume twice |
| C06 | Weak donor cannot lower any main inherited bonus after rounding |
| C07 | Multiple generations count old inheritance once; diminishing gains measured |
| C08 | Normal Star-up next Star and Plus0; invalid Race/Star/level rejects atomically |
| C09 | Special wrong parent pair rejected; unverified rules prevent activation |
| C10 | Fusion/reversion unequips each item once into bag or mail on overflow |
| C11 | Split after hatch/reversion restores exact intrinsic parents, child removed |
| C12 | Split after valid trade delivers parents to current owner, never old owner |
| C13 | Restored parent retains its own prior restoration reference |
| C14 | Full pet storage sends overflow parents to mail; claim requires space |
| C15 | Pending-mail pet cannot fight/trade/fuse; repeated claim yields one pet |
| C16 | Parent binding cannot be bypassed through child transfer/split |
| C17 | Same pet in both slots, battle pet, stale owner/revision and concurrent mutation reject |
| C18 | Death/timeout/reconnect at each commit boundary loses/duplicates no input/output |
| C19 | Different-element eligible skill enters inherited pool; newborn learns none automatically |
| C20 | Preserved learned high-level skill usable at Lv1 if other use conditions pass |
| C21 | Direct hit damage remains when attached poison is resisted |
| C22 | Duplicate formula learning rejects without consuming blueprint; reuse knowledge across fusions |
| C23 | Legacy→canonical save mapping is explicit; unknown IDs fail validation, not auto-remap |

Numeric assertions for C03/C06/C07 and branch costs cannot be written as final
fixtures until P11/P16 chooses the corresponding formula/configuration.
