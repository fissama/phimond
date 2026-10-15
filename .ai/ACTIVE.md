# Active Development

- **Last reviewed:** 2026-10-12
- **Phase:** **P10 design phase CLOSED** (closure report [`.ai/plan/phases/P10-pet-model/P10-closure.md`](plan/phases/P10-pet-model/P10-closure.md)). P11 design is closed; see [P11 closure](plan/phases/P11-stats/P11-closure.md).
- **Project progress:** [PROJECT_PROGRESS.md](plan/PROJECT_PROGRESS.md); master plan ở [PHIMOND_MASTER_SPEC.md](plan/PHIMOND_MASTER_SPEC.md) §5.
- **P10 redraw:** **COMPLETE 152/152 (100%)**, gồm **48/48** pet 4★–5★; chủ dự án duyệt chốt 2026-10-11. [Closure](plan/phases/P10-pet-model/P10-redraw-closure-20261011.md), [selected atlas manifest](plan/phases/P10-pet-model/redraw-kit/owner-atlas-selection.json), [final inventory](plan/phases/P10-pet-model/redraw-kit/completion-20261011/done.json). Mỗi atlas khóa theo SHA-256; đổi pixels cần duyệt phiên bản mới.
- **Next:** P11 **DESIGN UPDATED** (2026-10-13), effective catalog v3 / 160,14 revised roles and eight P10 authored allocations; layout smoke repaired and passing. [Final spec](plan/phases/P11-stats/P11-final-spec.md), [160-Species catalog](plan/phases/P11-stats/P11-species-catalog-160.md), [readiness](plan/phases/P11-stats/P11-readiness.md). Delegated F02/F03 explicitly replace total-candidate inheritance with accumulated training credit and strongest-lineage carry, including Normal Star-up; Special remains gated. Runtime/migration unchanged. P12 follows its own owner/dependencies.
- **Atlas integration pending:** đưa bộ đã duyệt vào renderer/UI theo species ID, scale/pivot theo tier, đúng loop/one-shot và test battle. P01/P02/P03/P05 sở hữu phần tích hợp phù hợp; chưa mở task runtime bằng lần cập nhật tài liệu này.
- **P10 design summary:** 152-species frozen roster (effective authoring roster is 160, see counts table below), 8-race taxonomy, 46 design decisions D01–D46, 23 acceptance scenarios, 8 open register entries (O01–O08) all tagged with explicit owners. Catalog tooling + asset validation + canonical checks all PASS (2026-09-28). P10 design does NOT include runtime code, numeric formulas, save migration, or Special server rules — those are P11/P13/P16/P19/P20.
- **Accepted:** original Race × Star distribution; MP as a P11 resource; growth reroll after Pet → Egg; APK-defined Special species/recipes/materials; basic attack available at zero learned skills; independent Race/Element and one Status Resistance.
- **Stat display accepted:** option A, `grown_stat + inheritance_bonus` (e.g. `186 +12`); permanent total is 198 and Overview adds equipment once.
- **Special Plus decision:** wait for verification of the original game; no reset/preserve fallback is approved. This blocks implementation of that outcome, not the remaining design discussion.
- **Re-hatch MP accepted:** recalculate max MP at Lv1 under P11 rules and set current MP to the new maximum; do not carry over old MP values or percentage.
- **Re-hatch skills accepted:** option A; level gates learning, not use of preserved learned skills at Lv1. MP and other P13 use conditions still apply.
- **Inherited-skill eligibility accepted:** option A; restrictions are per skill, and different Element alone does not exclude inheritance. Eligible skills enter the learnable pool, not current skills.
- **Status Resistance scope accepted:** option A; all harmful statuses (control, poison/burn, stat reductions), application chance only, not direct damage or duration.
- **Restoration accepted:** option A; a hatched fusion child may return to Egg and split into its exact pre-fusion parents. Consume the child; do not transfer child progress or refund spent fusion/reroll costs. Restored parents become usable again.
- **Equipment accepted:** automatically unequip on fusion and Pet → Egg; return to inventory, overflow to the player's mailbox. P19 defines mailbox behavior. Restored parents have no equipment; no item recreation from snapshots.
- **Restoration ownership accepted:** option A; rights follow the child through valid transfers, and the current owner receives both restored parents. Parent binding restrictions must not be bypassed.
- **Restored-pet overflow accepted:** option A; parents that do not fit in pet storage wait in the current owner's mailbox with their restored state intact. No use/trade before claim, no level reset on claim; P19/P16 own details.
- **Endgame correction accepted:** no standalone 5★ +99 build-change action. Reinforcement remains available at +99; output stays +99, normal costs/parent consumption/Egg → Lv1 flow apply.
- **Inheritance policy accepted:** option B; diminishing marginal gains without a hard inheritance cap. P11/P16 own formula/rounding; P15 verifies long-run pacing.
- **Native Skill Pool accepted:** option A; per-Species counts may differ, P13 designs contents by role/identity, six current-skill slots unchanged.
- **Reinforcement inheritance floor accepted:** option A; each inherited stat bonus cannot fall below the main parent's prior bonus, including at +99. Extra gains diminish, no minimum +1; Lv1 reset remains. Do not apply this floor automatically to Star-up/Special fusion.
- **Remaining work (P10 design):** none. Closure review [P10-closure.md](plan/phases/P10-pet-model/P10-closure.md) signed 2026-09-30. Open register items O01–O08 remain in `P10-readiness.md` with explicit owners; P10 does not own their resolution.
- **Coding contract:** [P10 data contract](plan/phases/P10-pet-model/P10-data-contract.md), 23 acceptance scenarios. Canonical authoring IDs in `data/p10/`, exact source mapping in `id_registry.json`.
- **Specification:** [P10 decisions](plan/phases/P10-pet-model/P10-design-decisions.md).
- **Review queue:** [P10 review](plan/phases/P10-pet-model/P10-review.md).
- **Species list:** [P10 roster](plan/phases/P10-pet-model/P10-roster.md); canonical authoring data `data/p10/species.json`; raw source `data/pets/roster_apk84.json`.
- **Assets:** APK gốc ở `apps/game-client/assets/pets/apk84/` — 152 portraits và 760 clips; 152 redraw atlas đã duyệt nằm ở các đường dẫn pin trong selected manifest, mỗi atlas 20 frame / 5 animation.
- **Runtime boundary:** the legacy 14-species gameplay catalog/save IDs remain active until P11/P13/P16 configuration and migration are designed. New roster has source identity/art, not invented stats or elements. New P10 fields (`element_id`, `base_stats`, `growth_baseline`, `role_ids`, `native_skill_ids`) are additive — do not modify existing entries without explicit user approval.
- **P10 implementation:** none for gameplay migration; gameplay code is owned by P11/P13/P16/P19/P20.
- **Historical phase:** P00 closed at `e66350b`; failed dev latency budget and no 50-CCU certification remain recorded there.

Layout delivery gate repaired2026-10-12: `layout_audit.gd` verifies current scene geometry and is included in `tools/check.sh`. Runtime P11 remains separate.

## Số liệu nội dung hiện hành (nguồn chuẩn)

Cập nhật 2026-10-14. Đây là số liệu thiết kế candidate; **runtime chưa kích hoạt**, P10/P11/P13 chưa promote. Các tài liệu khác dẫn về bảng này thay vì tự lặp số.

| Hạng mục | Số | Ghi chú / nguồn |
|---|---|---|
| Loài — baseline APK 8.4 đóng băng | **152** | `data/p10/species.json`, `data/pets/roster_apk84.json`; phân bố 1★–5★ = 50/30/24/21/27. Cũng là phạm vi redraw 152/152 đã duyệt. |
| Loài — roster thiết kế hiệu lực | **160** | 152 + 8 proposal (6 Normal 5★ + 2 Special Hybrid 5★). Phân bố 50/30/24/21/35; Normal 4★ 17, Normal 5★ 20, Special 4★ 4, Special 5★ 15. [P11 catalog 160](plan/phases/P11-stats/P11-species-catalog-160.md), [P13 candidate catalog](plan/phases/P13-skills/P13-candidate-species-catalog-160.json). 8 ID proposal chờ P10 mapping và art. |
| Skill — candidate P13 V7 | **97** | 95 skill cũ + 2 signature Hybrid; tổng 9 signature độc quyền. Nằm trong [roster-review-package.json](plan/phases/P13-skills/roster-review-package.json). `P13-skill-catalog.json` (95) là input trước V7. |
| Recipe — candidate P13 | **28** | 13 cặp cho 4 Special 4★ + 15 cặp cho 15 Special 5★ ([feedback v7](plan/phases/P13-skills/P13-owner-feedback-v7.md)). Chi phí, xác suất, Plus thuộc P16/P20. |
| Recipe — nguồn APK | 17 | Giữ làm bằng chứng (disabled trong `data/p10`), không phải luật game. |
| Runtime hiện tại | 14 loài / 29 skill / 6 recipe | Server vẫn nạp catalog cũ; migration 14→160 chưa thiết kế (P10-O08). |

## P12 — documentation promoted; stage execution pending

D01–D60 preserved as approved_in_brainstorm; FLOW-01/Q-P12-01…09 scope approved in conversation2026-10-12. [Scope](plan/phases/P12-world/P12-scoped-design.md), [registry](plan/phases/P12-world/P12-decision-registry.md), [gaps](plan/phases/P12-world/P12-gap-analysis.md), [documentation amendments](plan/phases/P12-world/P12-spec-change-proposals.md). Selected flow keeps P12 open through Stage3 benchmark/Stage4 expansion/Stage5 review; separately approved P12 baseline can open an authorized P01 prototype after baseline and separate stage/scope approvals. Global coverage and all critical dependencies retained. Documentation/spec updates authorized; audit, source verification, prototype execution and engine migration remain unauthorized. P12 remains OPEN.

- **P12 update 2026-10-14:** Stage 1 local outputs exist outside the repo and the owner has approved 3.2 as primary source plus 35 maps; 56 maps await naming/review. Owner decisions recorded: teleport pillars (city square Lv1–40 zones + Farm + Pirate Ship Lv40+; ship pillar → Lv40+ zones + Farm + back), arrival ≈1 unit beside the return door, no level block on the Emerald exit, new-player flow Summoning Hall (pick 1★ pet) → quest → Emerald. See [P12 README](plan/phases/P12-world/README.md). P12 remains OPEN.
- **P12 update 2026-10-14 (later):** naming settled via [P12-world-names-master.md](plan/phases/P12-world/P12-world-names-master.md) (owner names, no APK/JAR names); HanhLang = Tàu cướp biển (Hải Tặc Hào); first-run flow = Sảnh vẫy gọi (3 stone pedestals, starter pets Xương Rồng / Bọ Cạp Sa Mạc / Ưng Đỏ) → unlock one-way teleport to Emerald. Open: U1, U3, U7, hall coordinates (Stage 2, needs separate authorization). P12 stays OPEN.
- **P12 Stage 2 audit 2026-10-14:** [P12-stage2-audit.md](plan/phases/P12-world/P12-stage2-audit.md) written (read-only on APK/XAPK/JAR). Door `vector_raw` behaves as destination arrival (122/130 inside bounds, median 1.89 units from the reciprocal door); Palace Gate has no door to Emerald (teleport-pillar model confirmed); JAR has no Emerald (5 city/hall packages only); risks R-S2-1…5 (e.g. 1-unit arrival may re-trigger Door 2). Runtime unverified; P12 stays OPEN; Stage 3 needs separate authorization.
- **P12 Stage 2 approved 2026-10-14:** owner approved the four audit points (1-unit arrival + door re-trigger guard; hall→BiBo arrival at the door edge, BiBo left side; pedestal position; door-vector-as-arrival basis). Stage 2 closed; Stage 3 not authorized. P12 stays OPEN.

- 2026-10-14: P12 Stage 3 — prototype vào `prototypes/p12-stage3/` (Three.js + Godot Web, HUD game giữ nguyên + 6 tab chat); phân tích HUD: `.ai/plan/phases/P12-world/P12-stage3-hud-analysis.md`. Chờ owner đo trên iPhone 17 Pro Max Safari + macOS Safari.
- 2026-10-14: Chủ dự án chọn Three.js cho client web. Draft kế hoạch port: `.ai/plan/phases/P01-world/P01-threejs-migration-plan.md`; ADR-0001 (Proposed). Chờ debate/duyệt trước khi mở M0.
- 2026-10-15: Web client (Three.js) — bàn giao phiên ở `.ai/handoffs/2026-10-15-web-client-threejs.md` (map 60 ô, quái đi tuần, sửa nút chéo, demo wasm).
- 2026-10-15: P12 rà soát — tạo `plan/phases/P12-world/P12-closure-checklist.md` (trạng thái stage, 6 mục chờ owner, sản phẩm Stage 4, lệch thiết kế↔runtime); benchmark spec đánh dấu SUPERSEDED. P12 vẫn OPEN.
- 2026-10-15: P12 Stage 4 mở (owner). Đã có `stage4/` (portal matrix 45 cửa, design nháp, script sinh). Owner duyệt mục C, Hải Tặc Hào, 3 thần thú, scope 17 map. Chờ Q1–Q4. P12 vẫn OPEN.
- 2026-10-15 (sau): P12 Stage 4 — owner chốt Q1 (Hoàng Môn chỉ lần đầu), Q2 (trụ → Bờ Đông Ngọc Bích), cho đọc APK 3.2. Đã thêm `stage4/P12-S4-npc-matrix.md` (44 slot NPC gốc), `apk-extract/` (NPC, điểm spawn), bảng cấp vùng đề xuất. Chờ Q3, Q5–Q7. P12 vẫn OPEN.
- 2026-10-15 (sau nữa): P12 Stage 4 — owner duyệt bảng cấp vùng, giữ 6 NPC Hải Tặc Hào, chốt quy tắc mỗi map lớn có 1 vùng an toàn (chết/kẹt → vùng an toàn). Thêm `stage4/P12-S4-npc-roster.md` (48 NPC: chính tuyến, tự do, hồi máu, kỹ năng, dịch vụ), mục §7 vùng an toàn trong `P12-S4-design.md`; Bìa Rừng Lục Bảo thành vùng an toàn Emerald (đã báo owner). Chờ Q8–Q11. P12 vẫn OPEN.
- 2026-10-15 (cập nhật): owner giữ Bìa Rừng như cũ (map khởi đầu, không vùng an toàn); thầy kỹ năng chung; nông trại ngoài chỉ 1 NPC gửi/rút pet, dịch vụ pet về Phòng thú cưng. Roster còn 49 NPC. Chờ Q12–Q14.
- 2026-10-15 (chốt): owner đồng ý hồi sinh Emerald ở Bìa Rừng; ấp trứng ở Phòng thú cưng; Nông trại + Phòng thú cưng là map riêng từng người chơi; bậc kỹ năng do P13; chuỗi nhiệm vụ chính do phase quest quyết (P12 chỉ soạn NPC). Roster 49 NPC chờ duyệt cuối. P12 vẫn OPEN.
- 2026-10-15: quét APK 3.2 xác định vùng an toàn cho mọi vùng (`stage4/apk-extract/map-scan.json`, `P12-S4-design.md` §7.2). Sửa: Sa mạc = Sa Thạch Cổ Thành, Tinh Không = Tử Vân Lâm. Đảo Ác Mộng không có map an toàn thuần (Q15).
- 2026-10-15: owner chốt Đảo Ác Mộng giữ Trại Tàn Sinh trộn lẫn (không vùng an toàn). Hết câu hỏi mở về NPC/vùng an toàn của Stage 4.
