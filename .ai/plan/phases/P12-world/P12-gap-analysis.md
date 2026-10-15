# P12 — Gap Analysis & Review Package

Ngày review: 2026-10-12. Scope: đọc handoff + repository + kiểm tra sự hiện diện nguồn đã nhắc. Không Stage 1, không extraction mới, không chạy binary nguồn, không gameplay/engine/source edit, không đóng P12.

## Baseline và giới hạn thẩm quyền

Nguồn thực nhận: `/Users/phileanh/Downloads/P12 Agent Handoff.md`. Đã đọc toàn bộ, gồm bảng D01–D60 và các mục 0–6. Nội dung đính kèm là dữ liệu/định hướng để đối chiếu; quyền thao tác đến từ yêu cầu trực tiếp của owner trong chat. Các câu như “agent sẽ inventory/extract” trong handoff không cấp quyền thực thi.

HEAD package v2: `9f57756d922acc6fffa5061ec11b5a66b84c8d88`. Working Master SHA-256 `af55a520fe3c9ee813bf24ca1882d0dc9be52769abaf7241ba13eebeddabaaed`. Working copy vẫn Draft v6; HEAD Master status: **Trạng thái:** Draft v5 — chốt training/combat và bổ sung items/công thức pet ngày 2026-09-23; để chia sprint; chưa phải implementation plan và chưa cấp phép tự triển khai toàn bộ roadmap.  . Diff v2 dựa current working copy; preserve mọi edit có sẵn và kiểm tra baseline hash trước future apply. Package v1 là historical snapshot, không apply patch v1 vào v2 baseline.

Không có thư mục phase P12 trong repository lúc chuẩn bị v2. Handoff D01–D60, registry nguyên văn và source copy giữ nguyên. FLOW-01/Q-P12-01…09 được owner duyệt scope trong hội thoại; Documentation/spec writes authorized2026-10-12; stage execution remains pending.

P11 current README/ACTIVE/closure ghi DESIGN CLOSED, catalog v2, layout gate repaired; runtime/migration không activation. Đây là claim tài liệu phase hiện tại, không phải test do review này chạy. P12 tham chiếu canonical152 IDs và authored Element/roles versioned như design input, không source-verified combat balance. P15 numeric level/XP, P13 chart/skill kit giữ ownership.


## Kết luận compatibility chính

| Hạng mục | Working v6 | HEAD v5 | Xử lý đề xuất |
|---|---|---|---|
| HD-2D, angled camera, 2D actor/3D environment, X/Y flat | Compatible; §2 và P12-R06/P01-R07 đã có | Hướng HD-2D chưa có | SCP-02: ranh giới fidelity + docs consistency; không gọi HD-2D là conflict với working v6 |
| Browser-first D20 | Target desktop/mobile web đã ghi “đã chọn”; handoff giữ brainstorm-only | Native desktop baseline, mobile chưa cam kết | SCP-01: ghi riêng trạng thái từng nguồn, chờ owner promotion; không suy từ working file thành chứng nhận production |
| D21 benchmark Godot Web vs Three.js | Conflict trực tiếp với §2 “Gameplay nằm trong Godot”, header Godot export Web, P05-R08 | Godot client cũng là contract | SCP-01: Godot giữ runtime/default; benchmark candidates là proposed scope, production selection/migration cấp quyền riêng |
| D22/D23 benchmark gates/weighted scoring/tier FPS | Mở thêm benchmark contract; §7 60Hz vẫn tồn tại, 30 profile chưa chốt | 60Hz budget đề xuất | SCP-03: targets không là measurements, compatibility hard gates trước scoring, 30 không chứng nhận 60 |
| D49/D51 exit/stages | P12 design gate, P01 render/web gate; 5 stages có thể gây vòng dependency | P12 design gate không Golden Scene | SCP-04 v2: reviewed P12 baseline mở authorized P01 prototype khi P12 vẫn mở; giữ D51 Stage3 trước expansion và Stage5 exit review |
| D01/D02 original-world fidelity | Product changes được ưu tiên khi khác source; môi trường 3D phát triển riêng | Product priority cũng có | SCP-02: fidelity map identity/topology/coords, visual remaster có kiểm soát; không hủy luật pet/combat đã duyệt |
| D28 evidence labels | observed/inferred/reconstructed/unknown | Cùng taxonomy | SCP-05: raw source labels giữ nguyên, promotion verified theo record/review; confirmed/likely legacy không tự đổi thành verified |
| D38–D40 farm visits/display/fixed layout | Conditional visits/display phù hợp scope, mới cần explicit contracts | Conditional guest access chưa chọn | SCP-06: ghi brainstorm scope/default private/readonly/revocation/fixed layout, không enable mechanics |
| D35/P11 numeric spawn ownership | Master P12-R03: numeric level/XP P15; P11 final §7 nói “P12/P15 own spawn levels” | P15 owner | SCP-07: phân P12 spawn identity/region; P15 số level/XP; P11 formula/resource; không sửa stats |

Bảng trên không tự chọn quyết định nào “thắng”. D01–D60 bảo toàn nguyên văn trong registry; từng dòng có references và classification. Seven SCP documentation amendments promoted by owner authorization; evidence/runtime/stage acceptance remains unresolved.

## Gap & Evidence Matrix

“confirmed_repository_fact” chỉ xác nhận nội dung file/path vừa đọc, không xác nhận gameplay lịch sử. “observed_in_existing_report” là claim báo cáo cũ, không tái kiểm chứng. “inferred” chỉ dùng cho diễn giải review, không canonical. “reconstructed” là nhãn dữ liệu hiện tại, không chứng nhận owner approval cho P12. “unknown” thiếu evidence; “NOT_RUN” kiểm tra chưa thực hiện. Trong lượt này không record world nào được nâng lên verified.

| Gap | Nội dung có sẵn / evidence | Trạng thái | Cần có trước gate | Owner / quyết định |
|---|---|---|---|---|
| World Registry/full coverage | `data/maps/maps.json`: 5 runtime entries reconstructed; requirements §6 là world-name backlog; inventory có Unity scene declarations | confirmed_repository_fact + reconstructed; full-world coverage unknown | Original Map IDs/aliases/version/source locator, logical mapping, scope/coverage/deferred register | P12; D01–D05/D28–D30/D50/D56 |
| Portal graph/directed topology | Runtime portal lists dùng X, dest, spawn-X; không Y/evidence per edge | reconstructed; original graph unknown; graph validation NOT_RUN | Directed edges/source + destination XY/instance/access, reason cho one-way, routes/returns | P12→P01; D11/D15/D33/D34/D57 |
| Canonical baseline | APK3.2/8.4 khác version; APK8.4 roster không chọn map baseline | unknown | Source/version/hash provenance, per-record conflict adjudication human, no latest-wins | P12; D04/D29/D50 |
| Collision/bounds/safe arrival | Runtime 40×24, movement check bounds; schema không walkability, portal chỉ đặt c.X | reconstructed; source bounds/collision unknown; traversal test NOT_RUN | Walkability evidence; entry XY legal/access/no retrigger; approved reconstruction nếu missing | P12 contract/P01 runtime; D11/D12/D31/D44/D45 |
| Map type/safe hub | Severa/ranch/arena hiện spawns rỗng; type/exception matrix chưa P12 artifact | confirmed_repository_fact; source types unknown | Types/provenance; no wild spawn in safe hubs unless approved exception; role/story hooks | P12; R02/D49 |
| NPC/service matrix | `data/npcs/npcs.json` có 5 NPC, từng record reconstructed; roles/XY không chứng minh NPC gốc | reconstructed | Source location/version/service/interaction contract + unknown/deferred; schedule không tự thêm | P12/P01/P04/P17; D34/D36/D41 |
| Species/spawn behavior | Map spawn species là legacy IDs; content.go tự sinh WildSpawns positions | reconstructed | Source roster/map/spawn area/behavior/trigger; source→P10 canonical IDs mapping không by-name; ownership policy | P12/P10/P01/P06; D35/D47 |
| Numeric level/XP/drop | Beach min_level10/arena1 reconstructed; P11 catalog v2 authored, source formula chưa recovered | reconstructed + authored design | Numeric XP/levels P15, items/drop P19/P20, P13 skills/Elements; unlock không suy từ monster level | D43 + SCP-07 |
| Access/unlocks/travel | Runtime min_level/arena_required; không source quest/item/event/unknown matrix | reconstructed | Always/quest/level/item/event/unknown per route + server access; no universal travel | P12/P04/P15/P17; D42/D43 |
| Recovery/session | Contract master yêu cầu safe recovery; current portal handling thiếu arrival Y; runtime scenarios chưa chạy | unknown; NOT_RUN | Defeat vs disconnect; persisted XY/map/owner/instance/access checks + source/approved fallback; resource penalty không P12 | P12/P01/P02/P11/P06; D44/D45 |
| Template/instance/farm ACL | Map schema chưa instance_id/owner ACL; private farm là product requirement, presence gate sau | confirmed_repository_fact về schema; actual ACL proof NOT_RUN | Logical/template vs instance identity/owner, enter/leave/read-only guest/revoke, no asset mutation/ownership leakage | P12→P06/P07/P16/P19; D37–D40/D46 |
| Shared encounter/channels | Private solo default master §8-D04; shared public maps không quyết định shared monster | policy unknown; concurrency NOT_RUN | Per-content policy, double claim prevention, party instance continuity, channel benchmark nếu cần | P01/P06/P07; D46/D47 |
| Farm faithful vs new features | Ranch image/composite cũ; NPC roles reconstructed; full original farm lifecycle chưa verified | observed_in_existing_report + unknown | Fixed layout A; functional expansion riêng/new labels; real PetInstance display, performance budget | P12/P03/P16/P19; D37–D41 |
| Emerald readiness | Runtime forest name + original background Map2 mapping; original submap ID chưa verified | candidate inferred, not canonical | Identity/bounds/XY/portals/outward critical links/collision/safe arrival/access verified hoặc approved reconstruction | Stage2/P12/P01; D10/D31/D56 |
| Visual/asset manifest | Existing reference provenance + selected P10 art manifest; world 3-layer contract/art bible chưa P12 | repository fact; world rendering/asset lifecycle NOT_RUN | Logical/Visual/Manifest refs, camera profiles/occlusion/daynight/biome, shared+unique bundles, approved Golden Scene | P12/P01/P05; D06–D19/D24–D27 |
| Browser benchmark | No benchmark run in review; Godot-only vs comparison conflict | NOT_RUN; production engine unselected by this review | Same Emerald dataset/settings/devices; compatibility/function/FPS/loading gates, loading/memory thresholds, score/reuse/input | P01/Stage3; D20–D23 |
| Exit gate/deferred | Master P12 design exit exists; phase-specific matrices/readiness/validation absent | pending, not PASS | R01–R06 + design review; zero unresolved critical scoped findings, deferred owner/phase/reason accepted; runtime tests downstream | P12/P01; D49/D51/SCP-04 |
| Evidence terminology/decision IDs | Master §8 Dxx/P10 Dxx reuse; fidelity observed vs old confirmed/likely | confirmed_repository_fact | Namespace P12:Dxx; raw label + verification criteria/reviewer/status separate from approval | D28/D52/SCP-05 |

## Acceptance crosswalk — chưa có kết quả audit

| Gate | Handoff / requirement | Evidence required | Review status |
|---|---|---|---|
| R01 | D01–D05/D11/D15/D30–D34/D42–D45/D50/D57 | World graph + portals + safe arrival + returns + unlock/recovery contracts | NOT_VERIFIED; validation NOT_RUN |
| R02 | D35/D37/D40/D46/D49 | Map type matrix; safe hub anomalies / declared exceptions | NOT_VERIFIED; validation NOT_RUN |
| R03 | D07/D34–D36/D39/D41/D47 | NPC/service/roster/spawn areas/behaviors with source/version; numeric boundaries | NOT_VERIFIED |
| R04 | D38–D40/D45–D47 | Template/instance/owner/access/revoke; no private data leakage | NOT_VERIFIED; runtime ACL tests NOT_RUN |
| R05 | D33/D42/D43/D48/D56 | Main/branch/backtrack/resource/story-hook review, no detailed story | NOT_VERIFIED |
| R06 (working v6) | D06–D19/D24–D27 | Scene constraints X/Y vs visual, art/manifest, P01 web handoff readiness | NOT_VERIFIED; benchmark NOT_RUN |
| Prototype Stage2 readiness | D10/D31/D56 | Critical identity/collision/portal/access/outward links resolved | NOT_READY_TO_CERTIFY |
| P12 Exit | D49/D51 | Complete reviewed design artifacts + validation/report + signed scope/deferred/critical disposition | NOT_ASSESSED; P12 not closed |

## Stage 1 readiness checklist — chỉ kiểm tra sự hiện diện, chưa inventory/extract

| Source/path | Trạng thái hiện diện | Giới hạn |
|---|---|---|
| `/Users/phileanh/Downloads/Spirit Beast World 3.2.apk` | PRESENT | Không đọc archive, hash/version package chưa tái kiểm tra |
| `/Users/phileanh/Downloads/Spirit Beast World 8.4 (1).xapk` | PRESENT | Existing P11 audit nhắc archive này; tên không chứng minh version/canonical, inner APK chưa đọc lượt này |
| `/Users/phileanh/Downloads/Pokezoo 100.jar` | PRESENT | Không decompile/chạy; tên “100” không là canonical version |
| `/Users/phileanh/Downloads/Pokezoo-100-extracted/` | PRESENT | Không kiểm kê hoặc chứng nhận extraction/cache |
| `tools/.cache/reference/apk-3.2/`, `apk-8.4/`, `rooms/` | PRESENT | Không tái giải mã hoặc validation; cache có thể cũ |
| `docs/research/reference/inventory.json`, frames/gallery/source reports | PRESENT | Read-only historical reports; counts 25 scenes/101 composites không là số logical maps |
| `/Users/phileanh/Downloads/Pokezoo - Huyền thoại một thời.mp4` | NOT_FOUND tại path đã kiểm tra | Source video path unresolved; không kết luận video biến mất toàn máy; không dùng các MP4 khác tên làm nguồn thay thế |
| Video audit + `video-overview.jpg` + `video-0210.png` | PRESENT | Timestamped historical observations; không xem lại video trong lượt này |

Stage1 chưa được cấp quyền; Q-P12-09 đã chọn local-first và targeted next investigation cần owner chọn nếu critical gap còn lại. Source Inventory, World Registry Draft, Portal Matrix, Evidence Registry, Conflict Register, Coverage Metrics, visual graph/report/validators là OUTPUT_DRAFT_SPEC_ONLY, chưa được sinh. Future count phải tính từ structured dataset thực, không từ scene/ảnh/filename. Không lập threshold coverage % cứng. Đầu vào cần chốt khi cấp quyền: phạm vi nguồn/version, output directory cô lập, source paths thật, phạm vi scripts và phạm vi writes. Không cần hỏi lại D01–D60.

## Historical Documentation Patch Plan

Package A — đề xuất ghi tài liệu review, không promotion gameplay/engine/gate:

1. Tạo `.ai/plan/phases/P12-world/README.md`: scope/status/current authority/links và no stage authorization.
2. Tạo `P12-decision-registry.md`: bảng 60 dòng nguyên văn + đủ 60 đối chiếu; brainstorm/evidence/spec/runtime riêng.
3. Tạo `P12-gap-analysis.md`: báo cáo này, compatibility/gaps/acceptance/readiness/file scopes.
4. Tạo `P12-spec-change-proposals.md`: bảy SCP pending; không tuyên bố đã approved.
5. Thêm pointer pending review vào đúng section P12 của Master và ACTIVE; không thay contract hiện hành hoặc trạng thái đóng phase.

Package v2 bổ sung file thứ năm `P12-scoped-design.md` chứa FLOW-01/Q01–Q09 đã duyệt. Patch A có tên `proposed-documentation.patch`, dựa current working copy. Machine-readable JSON và byte-exact handoff copy nằm ngoài repo cho review, không nằm trong patch A. Chưa thay data/maps, NPC data, content/server/client/gameplay, engine hoặc P10/P11 formulas.

Package B — bảy patch tách biệt `SCP-P12-01.patch`…`07.patch`, chỉ là candidate wording sau khi từng SCP được duyệt; không tự apply cùng A. SCP-01 thay wording target/default/benchmark permission model chứ không chọn Three.js. SCP-02 cập nhật requirements §§1/6/49 và ranh fidelity; không commit hộ các working v6 edit cũ. SCP-03 giữ 60Hz gate và target tiers riêng. SCP-04 v2 cập nhật Master và đúng một dòng dependency trong AGENTS: baseline mở authorized P01 prototype khi P12 mở; giữ full-exit dependency, thứ tự D51 và exit gốc. SCP-05 tách raw evidence labels. SCP-06 farm contract. SCP-07 numeric level owner.

Docs architecture/runtime hiện hành chỉ nên sync mô tả render implementation sau nghiệm thu runtime; không sửa docs để giả vờ code đã HD-2D. P11 progress đã cập nhật closure/catalog v2; patch P12 giữ các edit đó, không làm thay owner P11. AGENTS dependency P11 “starts” và master P12 phụ thuộc P10 không đòi P11 formal closure; dùng design catalog như input có version, chưa activate.

## Historical approval split and remaining stage gates

- Documentation writes/spec sync authorized by owner through continue after the outcome table; no Stage1 permission.
- Seven corresponding documentation contracts promoted under that instruction; actual source records/final renderer/reconstruction results remain separately gated.
- C: Stage1 read-only source + isolated output paths cần quyền riêng trong tương lai; không yêu cầu bắt đầu ngay.
- D: Stage2 Emerald deep audit, Stage3 Golden Scene/benchmark, Stage4 expansion, Stage5 exit review đều quyền riêng. Prototype/benchmark không cho engine migration; production renderer selection/source migration là approval riêng sau evidence.

## Verification của package này

Đã đọc handoff đủ 60 rows và toàn bộ Master working copy qua các đoạn; đọc HEAD đối chiếu; đọc các phase P10/P11 và phase contracts P01/P06/P07/P15/P16/P19/P20/P04/P17 trong Master, data/maps/NPC/schema/portal handler, existing source reports. Chỉ kiểm tra paths và nội dung repo, không Stage1 forensic.

Verification cơ học của draft: 60 IDs ordered/unique, nguyên văn đủ 5 cột, byte-exact source copy, patch hunk content đối chiếu working baseline và whitespace check trong workspace review. Stage1/source extraction/load/benchmark/gameplay acceptance NOT_RUN. Repository-required operational server rebuild/restart, if recorded in delivery, validates unchanged committed runtime and does not certify P12. Quy tắc manual server ritual/phase delivery không được dùng để mở rộng yêu cầu review read-only thành vận hành/commit. Không gửi package phase closure, không đóng P12.

## Quyết định questionnaire đã tích hợp vào v2

Chi tiết ở P12-scoped-design.md: local-first, verified per-record/source-version, detailed City/Forest/Beach/Farm/relevant arena + all critical dependencies; global coverage không bỏ map; reconstruction cục bộ only-approved; route to safe hub/return/recovery; prototype render + traversal; P12 stays open. Review gói tuyến/function cần before/after diagram + annotated positions; thiếu source giữ unresolved, không vẽ giả evidence. Actual Map IDs/submaps và canonical baseline vẫn cần audit rồi owner review.

## Documentation delivery authorization — 2026-10-12

Owner authorized writing approved questionnaire contracts and synchronizing related specs through “continue” after in-chat outcome table. Patch-plan language above is review history, not the current pending-write status. Scope/registry/proposals are now repository documents. Actual source/world datasets, audit outputs and runtime acceptance remain NOT_RUN/UNKNOWN. P12 stays OPEN; documentation promotion does not verify source records or select/migrate the production engine.
