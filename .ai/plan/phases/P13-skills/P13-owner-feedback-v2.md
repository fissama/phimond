# P13 — Phản hồi owner và đề xuất v2

2026-10-13. V1 hash `fd618e564db82122a93fb6953c0ae2d801332accc36e12d2e85f33925dc61be5`.
Owner feedback v8: `changes_requested`,17 nhóm approved, D02 pending.
Nguyên văn: `evidence/owner-feedback-v1-v8.json`. Candidate cũ:
`evidence/review-package-v1.json`. Chưa phải phase acceptance.

## Sáu slot có đủ không?

Owner: “Review lại số lượng 6 ổn không? thiếu/đủ/dư?”

Đề xuất giữ **6 current skill + basic riêng** theo P10 D35. Native/Inherited
là menu lựa chọn, không phải tất cả phải mang vào trận. Rank cùng slot;
signature cũng phải chọn trong6. Không gọi6 là số tối ưu đã chứng minh.

|Limit|Đánh đổi thiết kế|
|---|---|
|4|2damage+defense+support đã đầy; Hybrid/hai role dễ phải bỏ control/signature|
|6|2damage+defense+heal/cleanse+control+signature; vẫn phải bỏ một số AoE/buff/cleanse|
|8|Thêm nhiều đáp án vào cùng kit, tăng UI/auto và số current truyền qua dung hợp; chưa có bằng chứng cần mở|

Template không bắt buộc: support thuần không cần2damage, basic vẫn fallback.
Thanh Long sample6 gồm signature, claw_water, strike, bolt_water, sweep,
beast_instinct; muốn wave/silence phải thay. Huyền Vũ có thể thay shield trùng
công dụng với signature bằng cleanse/revive đã học. Sample kit không tự grant
và không phải kit tối ưu; quyết định chọn/thay có chủ đích.

P02/P07 so4/6/8 cùng species/pool/stats/MP/đối thủ/AI/seed suite; đo skill
usage, secondary role hữu ích, thời lượng trận, control/stall, đổi kit trước
đối thủ và thao tác UI. Nếu6 vẫn thiếu role dù kit hợp lý, owner mở lại
P10/P03/P16 trước đổi. Không có runtime simulator: không báo win-rate giả.

## Độc quyền Special4★/5★ có dấu ấn hệ

Owner yêu cầu một số Special4★/5★ có skill độc quyền và hiệu ứng hệ để tăng giá trị.
Chọn7 loài: cả4 Special4★ và3 Special5★, đủ6 Element. Giữ nguyên17Special/135Normal,
stats P11 và các gate Special operation P16/P20. Signature mới **Phimond-authored**,
không claim được khôi phục từ APK/JAR. Signature source-adapted cũ giữ nguyên.

|Loài|Skill / hệ|Hiệu ứng và counterplay|
|---|---|---|
|Thanh Long4★|Triều áp / Thủy|1.10MAG+70%base slow SPD−20%; SR/cleanse|
|Bạch Hổ4★|Phong trảo / Phong|1.25ATK+selfSPD+20% khi hit; dispel, không thêm lượt|
|Chu Tước4★|Ly hỏa / Hỏa|1.10MAG+70%base burn .30MAG×2tick; SR/water/cleanse|
|Huyền Vũ4★|Thủy giáp / Thủy|Gỡburn rồi shield1.20MAG+.08sourceHP; dispel, strongest|
|Nữ Đế Minh Giới5★|Minh ấn / Âm|1.40MAG+70%base misfortune hồiHP−25%; SR/cleanse|
|Thần Tướng Cự Ma5★|Địa chấn hộ thể / Địa|1.40ATK+selfDEF+25% khi hit; armor strongest, dispel|
|Linh Tiên Hoa Hương5★|Quang tịnh / Quang|Cleanse1 rồi heal1.50MAG+10; không revive/refill|

Tất cả CD3/rank1/1action/1slot, không kế thừa, chỉ species sở hữu học.
4★ họcLv30/MP24;5★ Lv40/MP28. Giá học rank1 theo D03. Preserved skills qua
re-hatch dùngLv1 nếu đủMP theo P10. Damage hit/crit/chart; negative effect chịu
SR; selfbuff chỉ sau hit thành công. Element không tăng heal/shield/chance.
Không có status mới/miễn nhiễm/instant-kill. Nén hai công dụng vào1action đổi
bằng MP/CD/slot; P02/P07 đo Special có/không signature với Normal cùng level/grade
để điều chỉnh nếu lấn mọi lựa chọn. Static checks không chứng nhận balance.

## Nghiệm thu lại

D02 giữ6 và gate4/6/8; D04 exclusive eligibility; D15 nội dung7signature.
15 nhóm nguyên nội dung giữ approval của owner v1v8. Ba nhóm sửa là pending,
kết luận v2 draft. Feedback cũ giữ nguyên; record v2 ghi `carried_from`, history,
source `carried_owner_review`, phân biệt với lần owner lưu mới. Agent không duyệt
thay owner. Handoff/closure tiếp tục chờ nghiệm thu v2.
