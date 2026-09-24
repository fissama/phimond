# Sprint spec — hướng dẫn tách từ master plan

Đây là cấu trúc để tạo sprint mới, không phải một sprint đã được chốt. Master reference: [PHIMOND_MASTER_SPEC_PLAN.md](PHIMOND_MASTER_SPEC_PLAN.md).

## Quy ước lưu

- Phase folder: `.ai/plan/phases/P00-baseline/` (các phase khác dùng ID/tên tương ứng).
- Sprint spec: `P00-S01-spec.md`.
- Implementation plan: `P00-S01-implementation-plan.md`, chỉ viết sau khi chốt sprint spec và khảo sát code hiện tại.
- Evidence: `P00-S01-verification.md` và ảnh/log đã loại secrets.
- Review phase: `P00-gameplay-gamedesign-review.md` trong cùng folder; mỗi sprint cập nhật finding, quyết định và bằng chứng của mình.
- Chưa tạo sẵn các sprint rỗng; chỉ tạo khi chọn thực hiện để tránh backlog giả trông như đã được phân tích.

## Nội dung bắt buộc của một sprint spec

1. **Identity/status:** sprint ID, phase ID, ngày, người thực hiện/review, draft/ready/in progress/verified.
2. **Player outcome:** một đoạn mô tả thay đổi người chơi nhận được; kèm tình huống trước/sau cụ thể.
3. **Traceability:** danh sách requirement IDs và findings của master plan mà sprint giải quyết; những requirement nào chỉ làm một phần.
4. **Evidence baseline:** file/code path đang active, reference timestamp nếu liên quan hình ảnh, capture/test/log tái hiện; phân biệt observed, inferred và unverified.
5. **Scope / non-goals:** có gì được ship và những việc dễ bị kéo theo nhưng không thuộc sprint.
6. **Behavior contract:** happy path, empty/invalid state, busy/loading, cancel/back, focus loss, disconnect/reconnect, terminal result và persistence. Không cần mô tả trường hợp không liên quan nhưng phải ghi lý do loại trừ.
7. **Data/API/save impact:** field/event/intents chịu tác động; server ownership; compatibility với client/save/catalog cũ; migration và restore nếu có.
8. **Presentation contract:** source frame, layout/scale, icons/fonts, actor facing/anchor, selected/disabled states, text; phần adapted phải có nhãn trong evidence. Đồ họa hiện tại là POC; nêu mức chất lượng cần đạt và visual debt còn lại. Giữ silhouette, tỷ lệ, nét tạo hình, bảng màu nhận diện và phong cách sprite/raster của nhân vật/quái vật; so sánh bộ ảnh chuẩn trước/sau, không tự redesign.
9. **Acceptance:** các scenario Given/When/Then có kết quả quan sát được; ghi rõ test tự động, live integration hay manual playtest chứng minh từng scenario.
10. **Failure focus:** những điều kiện dễ gây mất/nhân dữ liệu, sai target, phát lại effect, mắc kẹt UI hoặc mất điều khiển; acceptance riêng cho từng điều kiện thuộc scope.
11. **Dependencies/decisions:** phase gates đã đạt, câu hỏi cần quyết định trước code, default nào đã được chấp nhận; không chôn blocker vào một dòng “làm sau”.
12. **Delivery/evidence:** build/commit/restore point, cách chạy, test accounts, screenshot/trace, perf comparison nếu có, known deviations, rollback và checklist cập nhật master plan.

13. **Task review gameplay & game design:** dẫn chiếu requirement review của phase, xác định task review trước thay đổi, sau lát cắt chơi được và đóng sprint; sprint cuối phase phải có task review tổng thể cùng exit gate. Nêu scenario, reviewer/người chơi, giả thuyết thiết kế, chỉ số và evidence cần thu. Review điều khiển, độ rõ, lựa chọn, pacing, độ khó, grind, công sức/phần thưởng và recovery theo scope; phần không liên quan ghi lý do.
14. **Tuning và kết luận review:** ghi kết quả trước/sau, feedback định tính, giữ/chỉnh/hoãn và lý do; task tối ưu gameplay phải có acceptance riêng, không thay bằng FPS tốt hơn. Finding chưa đóng có severity, owner, phase/sprint đích; finding chặn outcome không được hoãn để đánh dấu verified. Thay đổi mechanics/ruleset cần decision và kiểm tra save compatibility.

15. **Online/performance impact:** nêu tác động tới mục tiêu 50 active CCU: tần suất intent, fan-out, payload, queue, query/transaction và render nhiều actor. Chọn profile/metric liên quan từ master, ghi baseline→budget→kết quả và kiểm tra regression. Sprint không tác động runtime phải ghi lý do; không yêu cầu full soak cho chỉnh tài liệu. P06/P09 bắt buộc có task full load/soak 50 CCU cùng client thật, report cấu hình/RTT/action rate/percentiles/errors và review gameplay đông người. Không đánh dấu đạt bằng 50 idle sockets hoặc chỉ bot tests.

## Mẫu report review của phase

- **Phạm vi/baseline:** phase, requirement IDs, build, save/test account, ngày, người chơi/reviewer và reference.
- **Review đầu phase:** scenario đã chơi, friction/bug/design gap, giả thuyết và mục tiêu trải nghiệm; bộ ảnh chuẩn actor và mức chất lượng POC/alpha/release.
- **Các vòng review trong phase:** sprint, thay đổi, scenario, số đo trước/sau và phản hồi; link evidence thật, không ghi test dự định làm như đã chạy.
- **Finding/decision log:** ID, loại gameplay/game design/art/performance, severity, evidence, giữ/chỉnh/hoãn, lý do, owner và task đích.
- **Review cuối phase:** chơi lại outcome/core loop bị ảnh hưởng, kết quả tuning và regression; checklist bảo toàn thiết kế nhân vật/quái vật; visual debt còn lại.
- **Kết luận:** đạt/chưa đạt exit gate, blocker còn mở và điều kiện review lại. Không đóng phase chỉ vì code/test đã xong.

## Ranh giới với sprint implementation plan

Sprint spec trả lời **làm gì, vì sao, thế nào là đúng**. Implementation plan trả lời **sửa file nào, theo thứ tự nào, test nào tái hiện, thay đổi contract ra sao, kiểm chứng và rollback thế nào**.

Không viết implementation plan bằng cách kéo nguyên một phase nhiều subsystem vào danh sách việc. Nếu reviewer có thể chấp nhận một kết quả nhưng từ chối phần khác độc lập, cân nhắc tách sprint hoặc task. Không ấn định số tuần trước khi có capacity và độ bất định của sprint.

## Ví dụ acceptance cho sprint đầu P00-S01

- Given public snapshot không chứa `battle.events`, when server gửi damage trong `data.events`, then renderer vẫn hiển thị đúng actor/target/amount một lần và cập nhật resource đúng authoritative state.
- Given request finishing blow, when response chuyển `battle` sang null, then feedback cuối và result vẫn hoàn tất trước khi trả quyền khám phá, không cần truy cập private RNG hoặc full battle history.
- Given reconnect sau một lượt đã xử lý, when nhận lại snapshot/state, then không phát lại damage/reward hoặc gửi lại mutation.
- Given public pet chưa appraisal, when thay contract presentation, then quality/growth/resistance ẩn vẫn không lộ.

Implementation plan của sprint này phải kiểm tra sequence semantics hiện tại trước khi chọn khóa dedup; không mặc định `event.seq` toàn cục vì domain có thể đánh lại số theo response.
