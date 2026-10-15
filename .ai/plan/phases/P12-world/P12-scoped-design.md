# P12 — Scope design từ questionnaire bổ sung

Ngày: 2026-10-12. Status: owner_scope_approved_in_conversation_2026-10-12; documentation_promoted_2026-10-12.
Nguồn: lựa chọn trực tiếp của owner trong cuộc trao đổi sau review D01–D60.
Bản này được ghi repository và đồng bộ Master theo owner authorization2026-10-12. Không cấp quyền audit/prototype/engine migration/closure.

## 1. Mục đích và authority

Hoàn thiện P12 bằng world design có evidence, đủ rõ để P01 triển khai, bảo toàn đầy đủ D01–D60. Questionnaire bổ sung chốt cách tổ chức gate/phạm vi/evidence/review, không thay lựa chọn gốc. D01–D60 vẫn approved_in_brainstorm theo nguồn handoff, không tự chuyển verified/promoted/implemented.

Master working v6 và HEAD v5 khác nhau theo review package ban đầu. Package v2 đã chỉnh các SCP theo scope approved và rebase trên working copy hiện tại. SCP-P12-01…07 đã promotion documentation contracts; đặc biệt SCP-04 v2 giữ P12 mở qua các stages và mở authorized P01 prototype từ reviewed baseline. Các patch v1/v2 là review history, không apply lại sau promotion.

## 2. Decision log bổ sung — giữ namespace riêng

| ID | Owner choice | Nội dung đã chọn |
|---|---|---|
| FLOW-01 | A | Baseline P12 được duyệt mở prototype P01; P12 vẫn mở qua các stages còn lại. Benchmark trước mass conversion. Baseline không phải closure. |
| Q-P12-01 | C | Topology/access unresolved chặn phần prototype phụ thuộc; collision/safe arrival cục bộ có thể reconstructed được duyệt, không shortcut/bỏ gate/đổi interaction. |
| Q-P12-02 | C | Cân bằng fidelity tham chiếu và chất lượng dữ liệu; sau audit agent trình một canonical baseline chính để owner chọn. Conflict topology/progression review riêng, không latest/majority-wins. |
| Q-P12-03 | B | Emerald cùng tuyến tối thiểu tới safe hub và đường quay lại hoặc recovery hợp lệ. Không ép portal một chiều thành hai chiều. |
| Q-P12-04 | B | Golden Scene + traversal: X/Y, collision, portal, safe arrival, access. Hai lát cắt render trước rồi traversal; không chỉ visual demo. |
| Q-P12-05 | B + 3 conditions | World Registry/graph draft bao phủ nguồn tìm được, không bỏ map vì chưa làm; detailed scope owner duyệt rõ, Emerald prototype không là toàn P12; mọi dependency critical về routes/unlocks/recovery/resources phải resolve kể cả ngoài vùng dự kiến. |
| Q-P12-06 | B | Detailed scope: City, toàn vùng Emerald Forest, Treasure Beach, Farm; arena/challenge phục vụ tuyến đó, cùng mọi dependency critical. Exact Map IDs/submaps chốt sau inventory. |
| Q-P12-07 | B | Verified cần source locator/version, kiểm tra cách đọc/ý nghĩa và xử lý conflict đã biết. Không yêu cầu cứng hai nguồn; inference/reconstruction không trở thành verified. |
| Q-P12-08 | B + owner addition | Review theo gói tuyến/chức năng, record scope cụ thể; kèm sơ đồ trước/sau và ảnh đánh dấu vị trí. Cho partial approval, không bao gồm record mới phát sinh. |
| Q-P12-09 | A | Local sources trước; gap critical còn lại được báo kèm targeted next investigation để owner chọn. Không tự mở rộng web/source scope. |

## 3. Phạm vi P12

Global coverage: inventory Map IDs/aliases/versions/sources và graph draft từ các nguồn được phép; những record missing/conflicted hiển thị unresolved. Counts lấy từ actual structured dataset, không suy logical map count từ scene/composite count.

Detailed scope candidate đã chọn: City, toàn Forest, toàn Beach, Farm, arena/challenge cần cho tuyến; bổ sung dependency critical ngoài vùng. Đây là scope theo tên vùng, chưa là danh sách Map IDs. Agent trình scope manifest sau inventory để owner duyệt exact records; không coi năm runtime maps hiện tại là original map scope.

Per-map contract: type/role/identity/bounds/XY, directed portals, arrivals/access/unlocks/routes/returns/recovery, NPC/services, species/spawn areas/behavior, template vs instance/ownership, resource/story hooks, evidence/conflicts/deferred. P12 không chốt numeric level/XP/drop rate/combat/formulas/quest story; chuyển owner P15/P19/P20/P11/P13/P02/P04/P17 tương ứng. Full matrices cần cho P12 Exit; NPC/spawn noncritical có thể chưa hoàn chỉnh khi prototype baseline nhưng không tự bỏ khỏi exit.

Farm giữ D40 Option A fixed layout, D38 default private/read-only visits future, D39 real PetInstance display không copy inventory/EXP/ownership. Farm functional expansion/source-original phải phân biệt; không thực thi cơ chế ở P12 design vì chúng có trong questionnaire.

## 4. Baseline để mở prototype P01

Cần owner review một versioned design baseline đủ để P01 dùng (versioned packaging là đề xuất kỹ thuật, chưa tạo data): candidate Emerald identity/submap; critical route tới safe hub và lối quay lại/recovery; bounds/XY/collision; portal destination/arrival/access. Topology/access chưa giải quyết phải chặn phần phụ thuộc, không tự lock/open cửa như gameplay rule mới.

Collision/safe arrival reconstructed chỉ khi phạm vi cục bộ, có provenance/before-after, không tạo shortcut/gate bypass/interaction change và owner approval. Nếu collision thay connectivity thực tế thì nâng thành topology-impact, không dùng ngoại lệ cục bộ.

Baseline gồm unresolved/deferred records với impact; không phải P12 closed. D31 readiness không thay D49 Exit. P01 prototype thực hiện trong stage scope được cấp quyền riêng; không cần đợi P12 closure, nhưng không được vượt contract baseline.

## 5. Staged flow và ranh giới ownership

1. Stage1 local global inventory/cross-version world graph draft/source/evidence/conflict/coverage report. Không chọn canonical tự động.
2. Owner review evidence/conflicts và chọn baseline chính; duyệt exact detailed scope, candidate Emerald và Stage2 scope riêng.
3. Stage2 deep audit Emerald + critical outward route/hub/return/recovery; resolve critical records hoặc trình reconstruction approval.
4. Owner duyệt P12 baseline bàn giao và Stage3 scope riêng. Stage3 phối hợp P01: Golden Scene/render slice rồi traversal slice; benchmark Godot4 Web/Three.js cùng logical dataset/scripted scenarios. Budget/device/gates cần chốt trước run; không chọn production renderer hoặc migration tự động.
5. Stage4 expansion sau representative validation; hoàn thiện detailed scope/contracts/matrices, giữ global draft coverage và deferred register. Mỗi stage cần approval riêng.
6. Stage5 exit review: P12-R01–R06 theo Master working baseline được promotion hợp lệ, design/evidence/validation/route/farm-access/readability reviews, zero unresolved critical trong approved scope, deferred có owner/target/reason/accepted disposition. Owner phase sign-off riêng; không đóng P12 từ stage label hoặc Golden Scene pass.

Tách baseline acceptance khỏi phase closure tránh vòng dependency P12→P01→P12. Không đổi thứ tự D51; stage expansion vẫn sau Golden Scene/benchmark. Benchmark participation không phải hoàn tất P01 hoặc production renderer certification.

## 6. Evidence và review package

Mỗi critical record: source path + version + locator, raw observation, parser/reading check phù hợp, semantic proof, related conflicts, evidence status và điều chưa chứng minh. Verified theo record/version; không dùng kiểm tra “trông hợp lý” thay source proof. Raw confidence/source labels giữ; brainstorm approval/spec promotion/implementation validation là trạng thái riêng.

Gói tuyến/chức năng: exact record list; current evidence và missing; before/after directed graph; annotated source/reference images thể hiện portal/arrival/collision/interaction khi có data; change impacts; approve/change/unresolved per record. Không bịa tọa độ để làm ảnh annotation, không vẽ trước như đã biết khi source thiếu. Diagram sinh từ cùng dataset; human art/fidelity review vẫn riêng. Partial approval ghi rõ accepted IDs/hunks, các record phát sinh cần review mới.

Local-first investigation dùng APK3.2, XAPK8.4, JAR và caches/reports đã có trong scope được cấp quyền. Missing video path giữ SOURCE_PATH_UNRESOLVED, không lấy MP4 khác tên thay source. Source missing không tự chặn mọi inventory; critical dependent records mới bị chặn. Sau khi điều tra local mà vẫn thiếu, agent trình gap/impact/findings và targeted investigation tiếp; owner chọn research/reconstruction/keep blocked theo risk contract.

## 7. Các approval còn cần — không suy từ questionnaire

- Scope này đã được owner đồng ý trong hội thoại. Owner đã duyệt ghi tài liệu/spec sau bảng outcome trong chat và “continue”; Q choices không cấp quyền stage.
- Owner đã cấp file-scope documentation/spec writes cho package này qua “continue”; không gồm data/gameplay edits.
- Stage1 source paths và isolated output/script scope cần cấp quyền riêng. Proposed external audit path: `/tmp/phimond-p12-stage1/` (chưa tạo, chưa approved).
- Stage2/3/4/5 scope/gates riêng; production renderer/migration quyền riêng sau evidence.

## 8. Acceptance của bản design draft

Không sửa D01–D60; không chốt Map ID/coords/source results chưa audit; không bỏ global coverage, detailed matrices hoặc critical dependencies; không giới hạn P12 bằng Emerald prototype; giữ staged flow và P01 coordination; đề xuất thiếu source giữ explicit; farm và numeric/gameplay phase boundaries giữ nguyên.

Delivery này ghi questionnaire scope và documentation/spec contracts vào repository. Stage1, extraction, runtime/game tests, benchmark: NOT_RUN. Repository changes: documentation/spec only; gameplay source/data/engine migration unchanged. P12: OPEN. Owner đã duyệt scope; file-scope documentation/spec writes đã được phép; stage execution vẫn cần approval riêng, không chạy audit ngầm.

> **Cập nhật 2026-10-14:** câu trên đúng tại 2026-10-12. Sau đó Stage 1 đã có đầu ra cục bộ (2026-10-13; xem [README](README.md)). Runtime/game tests, benchmark và verification đồ thị vẫn NOT_RUN; P12 vẫn OPEN.


Current package baseline: HEAD `9f57756d922acc6fffa5061ec11b5a66b84c8d88`; working Master SHA-256 `af55a520fe3c9ee813bf24ca1882d0dc9be52769abaf7241ba13eebeddabaaed`. P11 [closure](../P11-stats/P11-closure.md) ghi DESIGN CLOSED/catalog v2; runtime/migration chưa activation.

## Checklist phase — cách đọc nhanh

1. Stage1: đọc APK/JAR và các nguồn local được cấp quyền; xác định Map IDs/world graph/portal links, version conflicts, unknowns. Owner review canonical baseline và exact detailed scope.
2. Stage2: deep audit Emerald Forest + tuyến City/safe hub và đường quay lại hoặc recovery; critical topology/access resolve trước dependent prototype, reconstruction cục bộ chỉ sau approval.
3. Stage3 phối hợp P01: Golden Scene/render trước rồi traversal X/Y/collision/portal/safe arrival/access; cùng dataset/scenarios trên Godot4 Web và Three.js. Web PC/mobile benchmark gồm compatibility/function/FPS/loading/memory/input/visual readability; chốt device/browser/budget trước run, hard gates trước scoring. Không tự engine migration.
4. Stage4: hoàn thiện thiết kế City/all Forest/Beach/Farm/relevant arena + mọi dependency critical; portal/NPC/service/spawn/access/recovery/template-instance/ownership matrices. Global registry/graph draft không bỏ nguồn/map chưa triển khai.
5. Stage5: evidence/validation/design review, zero unresolved critical trong approved scope; deferred owner/phase/reason accepted, owner quyết định phase closure.

Prototype Emerald không phải full gameplay MVP hoặc P12 closure; combat/farm lifecycle/numeric levels và XP có phase owners riêng. Mỗi stage cần quyền riêng; ghi checklist không cho phép thực thi.
