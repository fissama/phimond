# P12 — World / Maps / NPC / Spawn / Access

D01–D60: approved_in_brainstorm, source rows preserved. FLOW-01/Q-P12-01…09: owner-approved scope in conversation2026-10-12. P12 remains OPEN. Evidence verification, Documentation/spec writes authorized2026-10-12; source verification and stage execution remain separately gated.

**Việc còn lại / trạng thái từng stage: [P12-closure-checklist.md](P12-closure-checklist.md) (2026-10-15).** Benchmark spec cũ đã SUPERSEDED bởi ADR-0001. Read [scope](P12-scoped-design.md), [registry](P12-decision-registry.md), [gaps](P12-gap-analysis.md), [documentation amendments](P12-spec-change-proposals.md) and [Master](../../PHIMOND_MASTER_SPEC.md).

Selected flow: approved P12 baseline can open a separately authorized P01 prototype while P12 stays open through D51 stages. Golden Scene+traversal/benchmark before expansion; phase closure separate. Detailed City/all Forest/Beach/Farm/relevant arena + all critical dependencies; global registry/graph draft keeps all available source records, exact IDs later owner review. Evidence local-first, source-version proof, per-route review with before-after diagrams/annotated positions. No Stage1 outputs or PASS from runtime benchmark here.

P11 design CLOSED/catalog v2, runtime/migration unactivated: use versioned authored design inputs, not recovered-original formulas/balance. Numeric spawn level/XP P15; P12 identity/behavior/area/access; P13 skill chart/kit, P19/P20 items/drop/recipes.

~~Godot remains current runtime; final renderer choice pending.~~ Cập nhật 2026-10-15: renderer đã chọn Three.js (ADR-0001 Accepted); port ở `apps/game-web` thuộc P01. No Stage1 execution is authorized by these documents. Never apply obsolete v1 patches to v2 baseline.

## Checklist phase — cách đọc nhanh

1. Stage1: đọc APK/JAR và các nguồn local được cấp quyền; xác định Map IDs/world graph/portal links, version conflicts, unknowns. Owner review canonical baseline và exact detailed scope.
2. Stage2: deep audit Emerald Forest + tuyến City/safe hub và đường quay lại hoặc recovery; critical topology/access resolve trước dependent prototype, reconstruction cục bộ chỉ sau approval.
3. Stage3 phối hợp P01: Golden Scene/render trước rồi traversal X/Y/collision/portal/safe arrival/access; cùng dataset/scenarios trên Godot4 Web và Three.js. Web PC/mobile benchmark gồm compatibility/function/FPS/loading/memory/input/visual readability; chốt device/browser/budget trước run, hard gates trước scoring. Không tự engine migration.
4. Stage4: hoàn thiện thiết kế City/all Forest/Beach/Farm/relevant arena + mọi dependency critical; portal/NPC/service/spawn/access/recovery/template-instance/ownership matrices. Global registry/graph draft không bỏ nguồn/map chưa triển khai.
5. Stage5: evidence/validation/design review, zero unresolved critical trong approved scope; deferred owner/phase/reason accepted, owner quyết định phase closure.

Prototype Emerald không phải full gameplay MVP hoặc P12 closure; combat/farm lifecycle/numeric levels và XP có phase owners riêng. Mỗi stage cần quyền riêng; ghi checklist không cho phép thực thi.


## Cập nhật 2026-10-14
- **Stage 1 đã có đầu ra cục bộ (2026-10-13):** inventory 92 map, đồ thị portal nháp 3.2/8.4, bản ghi duyệt của owner (nguồn chính = APK 3.2; 35 map đã duyệt). Các tệp nằm ngoài repo (`~/Downloads/Phimond-P12-Review/`). Các câu "Stage1 NOT_RUN" trong tài liệu P12 khác phản ánh thời điểm trước đó. Gate vẫn: Stage 2/3/4/5 cần quyền riêng; P12 vẫn OPEN.
- [P12-naming-proposal-jrpg.md](P12-naming-proposal-jrpg.md): 56 map chưa duyệt, tên style JRPG (owner chọn tên riêng cho phòng giống nhau).
- [P12-city-to-field-flow.md](P12-city-to-field-flow.md): trụ teleport Quảng trường ↔ Tàu cướp biển, bằng chứng APK, quyết định owner.
- [P12-emerald-baseline-package.md](P12-emerald-baseline-package.md): gói baseline Emerald để owner duyệt từng phần; U2/U4 đã chốt, U8, U9 đã chốt; U10 chốt bố cục (3 bệ đá thần thú; còn tọa độ ở Stage 2 và duyệt 2 thần thú đề xuất); U5, U6 đã chốt; U3 chốt hướng (va chạm mới cho HD-2D); U7 còn mở.
- [P12-stage3-benchmark-spec.md](P12-stage3-benchmark-spec.md): spec benchmark Godot Web vs Three.js (DRAFT).

- [P12-world-names-master.md](P12-world-names-master.md): bảng tên JRPG tổng hợp, không dùng tên APK/JAR (owner 2026-10-14); mục A, B đã chốt; chờ duyệt mục C và tên Hải Tặc Hào.

### Việc còn lại
Xem [P12-closure-checklist.md](P12-closure-checklist.md) (thay mục cũ 2026-10-14). U1 đã chốt; Stage 2 đóng; Stage 3 đóng 2026-10-16 (Three.js, iPhone high ~60 FPS); Stage 4–5 chưa có quyền.

- [P12-stage2-audit.md](P12-stage2-audit.md): **Stage 2 audit Emerald + tuyến thành** (2026-10-14): vector cửa = điểm xuất hiện (122/130 trong bounds, trung vị 1,89 đơn vị), xác nhận mô hình trụ, JAR không có Emerald, rủi ro R-S2-1…5. Owner duyệt 2026-10-14 (4 mục); Stage 2 đóng, Stage 3 chưa mở.

- **Stage 4 (2026-10-15):** [stage4/P12-S4-design.md](stage4/P12-S4-design.md) — ma trận portal/trụ cho 17 map; 4 câu hỏi mở cho owner.
