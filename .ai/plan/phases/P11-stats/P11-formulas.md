# P11 — Current formula contract v1

Authority: [final spec](P11-final-spec.md), including delegated F02/F03 changes.
Superseded development: [history](P11-formulas-interview-history.md).

## Exact growth

Let b=baseline×1000 and m=grade multiplier×1000, both integers.

```
grown[s,L] = base[s] + (b[s] × m[s] × (L−1)) div 1_000_000
permanent[s,L] = grown[s,L] + bonus[s]
```

Inputs nonnegative, level legal; div floors. Never floor each level increment.
No random draw after profile creation. No Star/role/Race/Plus multiplier here.

## Authoring

Main budget=HP/10+ATK+MAG+DEF. Template HP=10×target×HP_share;
others=target×share. Blend Primary/Secondary75/25, single100%Primary.
SPD/SR=neutral anchor×Star/class factor×blended role factor.
Validate final integer base/milli growth against exact targets and every budget,
modifier and Primary guard. Nearest half-up is an authoring seed, not permission
to waive failed bounds. Catalog v1 passes final checks.

## Accumulated inheritance — Normal operations only

```
t = max(0, min((Lm−20)/(Cm−20), (Ld−20)/(Cd−20)))
E[s] = a[s] × (grown_m[s]+grown_d[s])/2 × t
Qchild[s] = max(Qm[s], Qd[s]) + E[s]
Braw[s] = R[s] × (sqrt(1+2Qchild[s]/R[s])−1)
bonus[s] = floor(1000×Braw[s])/1000
```

R/a in [tables](P11-stat-tables.md). Cm/Cd exclude Plus. Exact Q starts at0
on capture. Store reduced rational numerator/denominator as decimal integer
strings. Never reconstruct Q from a rounded displayed bonus. Q is not a second
stat addend. Use arbitrary precision or explicitly reject unsupported operations;
never silently saturate/wrap or present a storage limit as a design stat cap.

Exact floor: choose largest integer z≥0 satisfying
`z/1000+(z/1000)²/(2R)<=Q`; bonus=z/1000. For Q=N/D and integer R:
`D×(2000Rz+z²)<=2R×1_000_000×N`.
Use exact integer square root/search, not floating-point boundary comparisons.

Fixed E>0 gives Qn=Q0+nE, unbounded Bn with diminishing derivative dB/dQ.
E=0 preserves principal. Max carry protects both parents per stat in Normal
Reinforcement and Star-up, including+99; no additional old-bonus floor addend.
Equipment, buffs, MP/currentHP, Plus itself and old bonus do not earn new E.
Matching inheritance versions are required; output uses that version. Any
mixed-version conversion requires a separate explicit migration contract.

## Effective stats / response boundaries

```
equipped = (permanent + sum(gear_flat)) × max(0,1+sum(gear_pct))
effective = (equipped + sum(battle_flat)) × max(0,1+sum(battle_pct))
maxHP = floor(max(1,effective_hp))
S = max(0,effective_status_resistance)
resistance = (4×S)/(5×(S+100))
p_after = p_before × (1−resistance)
order_key = (−max(0,effective_spd), fixed_battle_rank, stable_instance_id)
```

Flat inputs milli, percentages basis points; no intermediate rounding. Retain
exact rational results until explicit consumer rounding. One rational Bernoulli
status draw; zero chance remains zero. SPD comparator adds no rounding, extra
actions or mid-list reorder. Full MP/resource/source/order rules: final-spec§§5–6.

## Invalid inputs

Reject unknown/missing IDs/versions, illegal levels/grades, negative Q,
nonpositive denominators, malformed integers and nonfinite input. No fallback
Species, fresh RNG, clamped profile or guessed migration. Failures consume no
parent/item and award no credit; P16 owns atomicity/retries.
