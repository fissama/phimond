> **P13 design CLOSED 2026-10-20** — candidate V7.1: 160 loài, 97 skill, 28 recipe candidate; owner duyệt 18/18 nhóm và gửi kết luận *duyệt toàn bộ*. Đọc [P13-closure.md](P13-closure.md) trước. Runtime/migration chưa kích hoạt.

# P13 — Skill pet/quái và tương tác giữa các hệ

**Status: DESIGN CLOSED 2026-10-20 (owner acceptance, candidate V7.1).** Đây là đóng phase thiết kế, không phải runtime activation; runtime/migration thuộc phase khác.

- [Final spec candidate](P13-final-spec.md): 18 nhóm quyết định, P13 requirement mapping.
- [Behavior contract](P13-behavior-contract.md): action, học/rank, RNG, timing, target, stacking, save.
- [Source audit](P13-source-audit.md): APK3.2/8.4 đều60 records,13 conflicts và JAR1.00.
- [Closure](P13-closure.md): kết luận, bằng chứng, việc chuyển phase sau.
- [V7.1 review package](roster-review-package.json): **hiện hành, đã duyệt** — 160 loài (ID P10 `species_0001…0160`), 97 skill, 28 recipe candidate, 32 acceptance scenarios; kèm [candidate catalog 160](P13-candidate-species-catalog-160.json) (khoá theo proposal ID, có `stable_id`).
- [Skill catalog](P13-skill-catalog.json): 97 skill V7.1 (gồm 2 signature Hybrid); bản 95 skill cũ ở `evidence/P13-skill-catalog-v3-95.json`.
- [152 Species pools](P13-species-pools.json): pool 152 loài **trước V7**, giữ làm lịch sử.
- [Review package cũ](review-package.json): candidate trước V7 (95 skill, 152 loài), giữ để đối chiếu hash.
- [Verification](P13-verification.md): kiểm tra đã chạy và giới hạn.
- [Scope](P13-review-scope.md): authority, ownership và review-tool contract.

## Web nghiệm thu

```sh
python3 tools/p13_review/server.py --port 8133 --package .ai/plan/phases/P13-skills/roster-review-package.json
```

URL: http://127.0.0.1:8133. Bắt buộc `--package`, mặc định server trỏ gói cũ. Duyệt / yêu cầu sửa / từ chối từng nhóm, ghi góp ý,
nhấn **Lưu phản hồi**. **Gửi kết luận** hỗ trợ nháp, duyệt toàn bộ, yêu cầu sửa,
từ chối. Chỉ duyệt toàn bộ khi18 nhóm đềuapproved. Mỗi lần chỉnh phản hồi đưa
kết luận cũ vềdraft để gửi lại; lịch sử kết luận cũ được giữ. Có xuấtJSON.

Phản hồi thật ở `review/responses/<candidate-sha256>.json`, được tạo khi owner
lưu. Hash là SHA256 của toàn bộ bytes review-package.json. Phản hồi không tự
duyệt một candidate khác khi source thay đổi. Tests/browser QA dùng storage
tạm riêng, không tạo phản hồi owner giả. UI nằm ở tools/p13_review, tách HUD game.

## Bước sau nghiệm thu

Agent đọc exact candidate hash + phản hồi đã gửi. Các yêu cầu sửa/từ chối được
xử lý và trình revision mới. Khi owner chốt, cập nhật decision acceptance,
review/closure/master scope có chọn lọc, chạy phase gates, tạo handoff theo skill
phimond-phase-handoff, commit/push đúng file scope và run latest committed source
theo AGENTS.md. Không stage unrelated P10/P12/client work.

P02/P07 vẫn chịu runtime/playtest; P15/P19 chịu pacing/relearning-cost evidence;
P14 effect budgets; P16 lifecycle/snapshots; migration cần gate riêng. Chưa có
measured combat balance hoặc50CCU certification.

## Revision v2 sau owner feedback v8

Xem [phản hồi và thay đổi](P13-owner-feedback-v2.md). Owner đã duyệt17 nhóm v1;
v2 giữ15 nhóm nguyên nội dung, mở lại D02/D04/D15. Thêm7 signature Special
độc quyền và giải thích6slot; draft mới không phải phase approval. Feedback
v1v8 và candidate cũ được giữ trong evidence.

## Lịch sử: revision v3 (đã bị V7.1 thay thế)

[Phản hồi v3](P13-owner-feedback-v3.md): APK tiers riêng, nhẹ cho farm, target/effect
filters,8Race audit.7signature v2 giữnguyên behavior/numbers.6decision groups sửa
được mở lại; các pending v2 vẫnpending, owner chưa gửiphase acceptance.
