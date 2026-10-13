# P11 — Current numeric tables v1

Owner-approved Q7–Q13 except marked F decisions. Authority:
[final spec](P11-final-spec.md). [Superseded history](P11-stat-tables-interview-history.md).

## Growth grades

| Grade | Probability | HP/ATK/MAG/DEF | SPD/SR |
|---|---:|---:|---:|
| D | 3% | .90 | .970 |
| C | 12% | .95 | .985 |
| B | 40% | 1.00 | 1.000 |
| A | 28% | 1.03 | 1.009 |
| S | 12% | 1.06 | 1.018 |
| SS | 4% | 1.08 | 1.024 |
| Perfect | 1% | 1.10 | 1.030 |

Fixed values; expected multiplier1.0108 main/1.00324 aux. F01 independent draws.

## Star/class targets

| Class | Base main | Growth main | Main tolerance | SPD factor | SR factor | Cap+00/+99 |
|---|---:|---:|---:|---:|---:|---:|
| Normal1 | 100 | 2.000 | ±3% | 1.00 | 1.00 | 60/159 |
| Normal2 | 110 | 2.200 | ±3% | 1.02 | 1.03 | 70/169 |
| Normal3 | 122 | 2.440 | ±3% | 1.04 | 1.06 | 80/179 |
| Normal4 | 136 | 2.720 | ±3% | 1.06 | 1.09 | 90/189 |
| Special4 | 148 | 2.960 | ±2% | 1.07 | 1.105 | 90/189 |
| Normal5 | 160 | 3.200 | ±3% | 1.08 | 1.12 | 100/199 |
| Special5 | 172 | 3.440 | ±2% | 1.09 | 1.135 | 100/199 |

Main budget=HP/10+ATK+MAG+DEF. Neutral Normal1 SPD base40/growth1.020;
SR base20/growth.510. At Lv60 B: SPD100/SR50; at Lv159 B: SPD201/SR100.

## Role templates

| Role | HP/10 | ATK | MAG | DEF | SPD | SR | MP (F04) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Physical DPS | 25% | 45% | 10% | 20% | 1.00 | 1.00 | 1.00 |
| Magic DPS | 25% | 10% | 45% | 20% | 1.00 | 1.00 | 1.30 |
| Tank | 40% | 15% | 10% | 35% | .90 | 1.10 | 1.00 |
| Hybrid | 25% | 30% | 30% | 15% | 1.00 | 1.00 | 1.15 |
| Support | 25% | 25% | 25% | 25% | 1.05 | 1.10 | 1.30 |
| Disruptor | 25% | 25% | 25% | 25% | 1.10 | 1.00 | 1.15 |

Same base/growth shares; independent Species modifiers. Blend75/25 then author.
Main per-stat±10%; SPD/SR each±5% inclusive. Actual values:
[current catalog160 JSON](P11-species-catalog-160.json).

## Inheritance/resource defaults — delegated F02/F04

| Stat | R | Earned-credit a |
|---|---:|---:|
| HP | 500 | .15 |
| ATK | 50 | .15 |
| MAG | 50 | .15 |
| DEF | 50 | .15 |
| SPD | 100 | .04 |
| Status Resistance | 50 | .04 |

Phimond defaults, not recovered APK constants or separate owner selections.
See formulas for exact accumulated-Q semantics.

MP Normal1 neutral base50/growth.500 scaled by main Star factor and blended
MP role factor; half-up integer/milli once during authoring. Lv60 single-role:
Physical/Tank79, Magic/Support103, Hybrid/Disruptor91 (base58+floor(.575×59)).

SR .80×S/(S+100): S0/50/100/200/400 gives resistance0%/26.6667%/40%/53.3333%/64%.
Probability only; not damage/duration.

## Owner-approved Bird content priority — F07

Catalog v1.1 authors Bird SPD at floor-to-grid(105% of the exact blended
Star/class target), separately for integer base and milli growth. Other Races
retain neutral rounded targets. This stays inside±5% and introduces no runtime
multiplier. Same-cohort ordering is an additional authoring invariant; see
[P11-race-identity-direction.md](P11-race-identity-direction.md).

## Roster160 / top-tier role reconciliation — 2026-10-13

The numeric tables above are unchanged. Fourteen ordered role blends change
which targets each Species uses; base/growth and MP are regenerated independently.
Current full values and the eight registered authored additions are in catalog160.
[Change ledger](P11-roster-160-reconciliation.md) separates Normal coverage,
Special directions and source evidence.
