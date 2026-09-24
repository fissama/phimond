# P00-S01 — Baseline, reference và canonical checks

Scope: P00-R01/R03/R05, phần review đầu phase R06. Người thực hiện: Codex; chủ dự án review sản phẩm. Implementation: [P00 plan T01–T02](P00-implementation-plan.md).

Player outcome: có cùng một đường chạy để tái hiện lỗi và kiểm tra game, giữ chuẩn tạo hình hiện có khi sửa runtime.

Acceptance: restore archive không secrets; entry scenes và commands xác minh từ code; có reference ledger với timestamp/unknown; offline gate phân biệt live mutations và bắt lỗi script Godot kể cả exit 0. Không sửa gameplay rules/catalog/art.

Failure focus: script legacy được báo pass thay active scene, fixture chứa private history, asset nguồn khác phiên bản bị ghi confirmed. Evidence và các giới hạn ở [baseline](P00-baseline.md), [ledger](P00-reference-ledger.md) và [review](P00-gameplay-gamedesign-review.md).

Review đầu/cuối sprint: ghi F01/F02, art POC và UI friction; chuyển vấn đề ngoài P00 về phase sở hữu. Baseline tests ban đầu có go vet fail (unkeyed literals); không coi là regression mới. No schema/save migration.
