# P12 — Documentation Spec Change Record

Ngày: 2026-10-12. Owner authorized documentation and corresponding spec updates via “continue” after the in-chat outcome table. All seven documentation proposals below promoted2026-10-12; previous rules/impacts retained for traceability. No audit/prototype/source evidence/final renderer selection or engine migration approval.

Owner approved supplemental scope FLOW-01/Q01–Q09; documentation/spec promotion authorized; execution remains pending. Baseline v2 cập nhật P11 closure/catalog v2, preserve current unrelated edits.

## SCP-P12-01

```json
{
  "change_id": "SCP-P12-01",
  "source_decisions": [
    "D20",
    "D21",
    "D22"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:6,50,71,78–80,525,653; docs/PROJECT_REQUIREMENTS.md:34–38,1703–1720",
  "current_spec_rule": "Godot client bắt buộc; working v6 đã chọn Godot export Web và P05-R08 Godot Web. Handoff D20 giữ brainstorm status và D21 benchmark trước chọn engine.",
  "proposed_rule": "Giữ Godot runtime/default; browser-first target không là chứng nhận production. Benchmark Godot4 Web vs Three.js với same Emerald dataset là candidate scope riêng; final engine selection/promotion/migration chỉ sau measured gates + owner approval.",
  "reason_and_evidence": "Direct engine-selection conflict; document approval-status divergence. Không có benchmark mới.",
  "affected_phases": [
    "P12",
    "P01",
    "P05",
    "P06",
    "P07",
    "P09"
  ],
  "risk": "high",
  "validation_required": "Review default/target/authority wording; authorized Stage3 equivalent scenes on desktop/iOS Safari/Android; function/input/reuse/memory/loading/FPS gates; production decision và migration separate.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-01.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.

## SCP-P12-02

```json
{
  "change_id": "SCP-P12-02",
  "source_decisions": [
    "D01",
    "D02",
    "D05",
    "D06",
    "D07",
    "D08",
    "D11",
    "D12",
    "D34"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:34–36,51,60–74,338; docs/PROJECT_REQUIREMENTS.md:255–268,1703–1720",
  "current_spec_rule": "Working v6 cho phát triển môi trường 3D riêng và ưu tiên product changes; requirements §6 nói 2D horizontal, chưa tách visual. HEAD v5 chưa HD-2D.",
  "proposed_rule": "World fidelity giới hạn identity/IDs/topology/XY/function; controlled visual remaster compatible, gameplay/layout/collision overrides review riêng. Logical 2D room model không bắt buộc renderer 2D. Giữ gameplay product P10/P11/P02/P16 đã duyệt.",
  "reason_and_evidence": "Working v6 art compatible; ambiguity with broader original-fidelity and stale requirements, not an assertion of new historical evidence.",
  "affected_phases": [
    "P12",
    "P01",
    "P10",
    "P02",
    "P05"
  ],
  "risk": "medium",
  "validation_required": "Review coordinate/topology vs visual boundaries and approval status of dirty v6; no source-coordinate changes; art/collision before-after review when later authorized.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-02.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.

## SCP-P12-03

```json
{
  "change_id": "SCP-P12-03",
  "source_decisions": [
    "D19",
    "D22",
    "D23",
    "D24"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:104–108,625–640; P01-R08/R10",
  "current_spec_rule": "§7 baseline 60Hz p95/p99; 30FPS budget chưa chốt; weighted benchmark và device tiers chưa official.",
  "proposed_rule": "Hard gates compatibility/function/FPS/loading trước scoring 30/30/15/15/10; FPS tiers là targets, presets ≠ FPS cap; thresholds/device/memory/loading budgets finalize trước run; preserve separate60Hz certification.",
  "reason_and_evidence": "Gate extension, no measured results; no arbitrary budget or universal mobile60 promise.",
  "affected_phases": [
    "P01",
    "P05",
    "P06",
    "P07",
    "P09"
  ],
  "risk": "medium",
  "validation_required": "Authorize device matrix/budgets beforehand; score sum100 check; failing hard gate cannot win score; repeatable measured raw results/warmup/thermal/background/cache/preset/portal peaks.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-03.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.

## SCP-P12-04

```json
{
  "change_id": "SCP-P12-04",
  "source_decisions": [
    "D09",
    "D10",
    "D27",
    "D31",
    "D49",
    "D51",
    "D53",
    "D56"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:§5 dependencies, P12/P01 §6; AGENTS.md:139",
  "current_spec_rule": "P12 design gate trước P01 dependency; AGENTS ghi không start P01 trước P12. Prototype entry từ approved P12 baseline chưa phân biệt full phase exit.",
  "proposed_rule": "P12 reviewed baseline mở một authorized P01 prototype slice khi P12 vẫn mở; Stage3 render+traversal/benchmark trước Stage4 expansion và Stage5 owner exit review. Giữ full-exit dependency và P12 original gate; global coverage + detailed City/all Forest/Beach/Farm/relevant arena + all critical dependencies, exact IDs owner review sau inventory.",
  "reason_and_evidence": "Owner chọn FLOW-01=A và Q01…09 trong questionnaire bổ sung. Không đóng design P12 trước Stage3; không đổi thứ tự D51. Scope approval không là repository promotion hoặc execution approval.",
  "affected_phases": [
    "P12",
    "P01",
    "P05"
  ],
  "risk": "high",
  "validation_required": "Review revised Master/AGENTS wording and whole package; future zero-critical portal/NPC/spawn/access/type/ownership/recovery matrices, route/safe hub checks, before-after diagrams/annotated images, separate baseline/Stage3/phase-signoff approval.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "supplemental_decisions": [
    "FLOW-01",
    "Q-P12-01",
    "Q-P12-03",
    "Q-P12-04",
    "Q-P12-05",
    "Q-P12-06",
    "Q-P12-08",
    "Q-P12-09"
  ],
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-04.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.

## SCP-P12-05

```json
{
  "change_id": "SCP-P12-05",
  "source_decisions": [
    "D28",
    "D32",
    "D50",
    "D52",
    "D55",
    "D60"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:52,645–673; docs/PROJECT_REQUIREMENTS.md:1511–1540; data/maps/maps.json",
  "current_spec_rule": "Master observed/inferred/reconstructed/unknown; legacy requirements confirmed/likely/reconstructed/unknown; handoff confirmed/verified chưa criteria unified; Dxx reused across docs.",
  "proposed_rule": "Preserve raw source confidence; record approval_status/evidence_status/spec_promotion_status/implementation_status independently. verified requires locator/version/review/checks per record; no raw observed/confirmed/likely auto-promotion. Use P12:Dxx namespace without changing D01–D60. Source locator/version + reading/semantic checks + known conflict resolution trước verified; review theo gói exact records, diagrams before/after + annotated positions; local-first, targeted further investigation khi owner chọn.",
  "reason_and_evidence": "Terminology/spec clarification, no relabel existing data; avoids false verified and namespace collisions.",
  "affected_phases": [
    "P12",
    "P10",
    "P11",
    "P01",
    "P04",
    "P09"
  ],
  "risk": "medium",
  "validation_required": "Review evidence-status criteria with owner; ensure source labels immutable and 60 IDs preserved; counts later computed from dataset; documentation approval not evidence approval.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "supplemental_decisions": [
    "Q-P12-07",
    "Q-P12-08",
    "Q-P12-09"
  ],
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-05.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.

## SCP-P12-06

```json
{
  "change_id": "SCP-P12-06",
  "source_decisions": [
    "D37",
    "D38",
    "D39",
    "D40",
    "D41",
    "D46"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:336–338,487–488,534,665 (§8-D15)",
  "current_spec_rule": "Farm private owner; guests conditional chưa chọn; display vs map customization chưa formal P12 contract.",
  "proposed_rule": "Default private/account-owned fixed layout OptionA; guests only permission/read-only movement with revocation, no pet/egg/item action; selected real PetInstance display optional limited roaming, no duplicate inventory/EXP; approved functional expansion separate source/new; runtime future P06/P07/P16/P19.",
  "reason_and_evidence": "Compatible conditional scope clarification/new approved-in-brainstorm design, not source-verified original buildings.",
  "affected_phases": [
    "P12",
    "P03",
    "P06",
    "P07",
    "P16",
    "P19"
  ],
  "risk": "medium",
  "validation_required": "Design ACL/permission/revoke and data disclosure review; future two-owner isolation/concurrent revocation/display ownership/performance tests; no placement system.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-06.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.

## SCP-P12-07

```json
{
  "change_id": "SCP-P12-07",
  "source_decisions": [
    "D35",
    "D43",
    "D47",
    "D49"
  ],
  "current_spec_location": ".ai/plan/PHIMOND_MASTER_SPEC.md:335 (P12-R03),435 (P15-R01); .ai/plan/phases/P11-stats/P11-final-spec.md:288",
  "current_spec_rule": "Master numeric level/XP P15; P11 final “P12/P15 own spawn levels” can imply shared numeric ownership.",
  "proposed_rule": "P12 owns map/spawn identity/area/behavior/provenance/access and encounter policy contract. P15 owns numeric level/XP/progression; P11 owns stat/resource formula + legal profile; P13 chart/skills; P19/P20 sources/drops/recipes.",
  "reason_and_evidence": "Cross-document owner ambiguity; no numeric edits or reopening P11 decisions.",
  "affected_phases": [
    "P12",
    "P11",
    "P15",
    "P13",
    "P19",
    "P20",
    "P01",
    "P06"
  ],
  "risk": "low",
  "validation_required": "Owners review scope wording; canonical species ID/version references; P11 final changes limited single ownership sentence, no formulas/catalog edits.",
  "status": "promoted_documentation_contract_2026-10-12",
  "allowed_now": "Document approved decisions and synchronize corresponding spec contracts only.",
  "prohibited_now": "Stage1/2/3/4/5 execution without separate authorization; engine migration; gameplay/data edits; automatic P12 closure.",
  "scope_approval_status": "FLOW-01/Q01–Q09 and corresponding documentation updates approved in conversation",
  "location_note": "Previous-rule locations refer pre-promotion baseline. Current spec contains documentation amendment; exact applied diff preserved in external delivery package.",
  "approval_basis": "Owner scope acceptance, then continue authorizing writing documentation/updating corresponding spec after plain-language outcome table."
}
```

Candidate exact diff: `SCP-P12-07.patch` in external review workspace. Historical review diff; do not reapply after documentation promotion.
