# Hàng chờ nghiệm thu — 2026-10-24

Chưa chứng nhận release. Kết quả máy giữ nguyên ngưỡng mặc định. Kiểm tra hướng dọc không dùng suy đoán NEAR/FAR từ ánh sáng của hướng ngang; cần xem hình trực tiếp.

## Lượt sửa mới

Đã bổ sung đạo cụ trong đủ tám khung: baker xuống (giỏ), elder xuống/lên (gậy), girl xuống (táo), guard lên (giáo), traveller xuống/lên (gậy). PNG, prompt, QA và preview được cập nhật từng file. Dải elder/traveller ngang có bản vẽ từng keypose mới; vẫn chưa vượt QA.

## Kết quả 24 dải hiện tại

pass: 7, warn: 11, needs-visual-review: 2, fail: 4. Cả 24 căn khung thành công. Pass ở đây không phải duyệt thẩm mỹ hay giải phẫu.

| Asset | Kết quả | Điểm cần xem |
|---|---|---|
| [player-female.run-down](delivery/player-female.run-down.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [player-female.run-up](delivery/player-female.run-up.review.gif) | warn | seam: warn |
| [player-female.run](delivery/player-female.run.review.gif) | needs-visual-review | leg_alternation: needs-visual-review — unknown: no pair of half-cycle frames shows a clear NEAR/FAR lead |
| [player-male.run-down](delivery/player-male.run-down.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [player-male.run-up](delivery/player-male.run-up.review.gif) | warn | seam: warn |
| [player-male.run](delivery/player-male.run.review.gif) | needs-visual-review | leg_alternation: needs-visual-review — unknown: no pair of half-cycle frames shows a clear NEAR/FAR lead |
| [walker-baker.run-down](delivery/walker-baker.run-down.review.gif) | warn | near_duplicates: warn |
| [walker-baker.run-up](delivery/walker-baker.run-up.review.gif) | warn | seam: warn |
| [walker-baker.run](delivery/walker-baker.run.review.gif) | warn | leg_alternation: warn — mixed: some half-cycle pairs repeat the lead |
| [walker-boy.run-down](delivery/walker-boy.run-down.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [walker-boy.run-up](delivery/walker-boy.run-up.review.gif) | warn | near_duplicates: warn; seam: warn |
| [walker-boy.run](delivery/walker-boy.run.review.gif) | warn | seam: warn |
| [walker-elder.run-down](delivery/walker-elder.run-down.review.gif) | warn | seam: warn |
| [walker-elder.run-up](delivery/walker-elder.run-up.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [walker-elder.run](delivery/walker-elder.run.review.gif) | fail | leg_alternation: fail — duplicated half-cycle: the same leg leads in both halves |
| [walker-girl.run-down](delivery/walker-girl.run-down.review.gif) | warn | near_duplicates: warn |
| [walker-girl.run-up](delivery/walker-girl.run-up.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [walker-girl.run](delivery/walker-girl.run.review.gif) | warn | leg_alternation: warn — mixed: some half-cycle pairs repeat the lead |
| [walker-guard.run-down](delivery/walker-guard.run-down.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [walker-guard.run-up](delivery/walker-guard.run-up.review.gif) | fail | identity_head_ratio: fail; seam: warn |
| [walker-guard.run](delivery/walker-guard.run.review.gif) | fail | identity_head_ratio: fail; leg_alternation: warn — mixed: some half-cycle pairs repeat the lead |
| [walker-traveller.run-down](delivery/walker-traveller.run-down.review.gif) | warn | near_duplicates: warn |
| [walker-traveller.run-up](delivery/walker-traveller.run-up.review.gif) | pass | Không có cảnh báo máy; vẫn cần Claude duyệt |
| [walker-traveller.run](delivery/walker-traveller.run.review.gif) | fail | leg_alternation: fail — duplicated half-cycle: the same leg leads in both halves; seam: warn |

## Ưu tiên sửa tiếp

1. Elder ngang: máy báo cùng chân dẫn ở hai nửa chu kỳ; cần xác nhận overlap hai đùi ở contact 1/5 và sửa keypose nếu sai.
2. Guard ngang: tỷ lệ đầu và đổi chân; guard lên: máy báo tỷ lệ đầu khung 5/6, cần đối chiếu cả mũ và giáo vì head-band có thể chứa đầu giáo. Không tự miễn lỗi.
3. Traveller ngang: máy báo cùng chân dẫn và thay đổi lớn giữa tư thế; cần kiểm chân trụ/nhấc và nối vòng.

Audit file của 110 PNG chạy độc lập với QA chuyển động. Không dùng audit file để thay nghiệm thu các mục trên. Không nạp ứng viên mới vào public.
