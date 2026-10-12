# P11 — Stats design closure, 2026-10-12

Status: **DESIGN CLOSED**. Current authority: final-spec F01–F09 and catalog v2.
This closes the design/content phase, not runtime stats/migration or measured
combat/economy balance. No next phase is launched by this delivery.

## Delivered

- Six-stat growth, seven grades, exact odds/rounding, Star/Special targets,
  role blending/guards, MP/resource/effect interfaces are pinned.
- Inheritance credit preserves trained lineage and permits continued growth
  without a hard bonus cap; diminishing gains, grade-reset losses, Lv1 reset
  and future training-time/economy acceptance are explicitly disclosed.
- 152 frozen Species have Element/roles, integer base, milli growth, Species
  accents and separate authored descriptions. All eight approved Race directions
  are embodied in stats or P13 native-function briefs. Bird SPD invariant held.
- Đại Bàng Vàng is Wind by owner approval; Normal5 covers all six Elements.
- 304 numeric layers pass constraints.137 vectors,27 Species share stats; this
  is tracked for distinct usable P13 kits, not hidden as certified balance.
- Source names/Race/Star/class/recipes remain frozen;97 source prose quotes
  preserved,55 missing. APK/video/web evidence is separated from authored rules.
- Mandatory layout gate repaired to actual scene structure and frame layout;
  canonical Godot checks now run it. min_smoke emits a positive PASS: marker.

## Validation and self-review

Server build and fresh race tests passed. tools/check.sh passed: Go tests/vet,
six Godot checks, seven load harness tests, three planner tests, web typecheck.
min_smoke passed authentication/catalog/connection/movement. Catalog deterministic
--check passed; negative layout fixture rejected old incorrect login geometry.
Diff review confirms changes are design artifacts and verification scripts,
not a runtime stat engine or migration. Unrelated P10 redraw/client changes in
this shared worktree are retained and excluded from this delivery commit.

## Downstream gates retained

P13: actual Native Skill Pools, six-element chart, hit/damage/status contracts
and role/Race kit value, including equal-stat cohorts. P15/P19: real progression,
donor supply/time/cost and repeated-fusion reward calibration. P16/P20: atomic
transactions, exact snapshots/rollback, Plus and Special eligibility source
gates. P14/P02/P07: gear budgets, replay/scheduling and PvP progression. Migration:
explicit legacy mapping and copied-save proof before enabling catalog152.

Manual server validation follows commit/push; it runs current legacy gameplay.
It cannot display the new P11 numeric catalog until a separate implementation.
