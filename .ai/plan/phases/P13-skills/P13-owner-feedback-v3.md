# P13 v3 — Tier nhẹ cho farm, target/effect và Race coverage

Owner xác nhận skill mới ổn; muốn làm rõ skill nguồn APK tăng damage và MP theo
tier, vẫn có Nhẹ để farm; skill đơn thể/AoE, có/không damage đi kèm hiệu ứng;
mỗi Race có pet vật lý và phép. V3 giữ nguyên7 signature authored của v2.
Candidate/feedback v2 giữ ở evidence. Handoff tiếp tục chờ nghiệm thu.

## Tách tier gốc thành skill riêng

Source APK8.4 có Càn quét nhẹ, Càn quét, Càn quét cao cấp, Càn quét siêu cấp;
cả7 family AoE gồm vật lý +6hệ phép đều4tier. Không gọi Cao cấp là “Mạnh” nếu
không phải tên source. V3 giữ nguyên từng ID và tên source, thành28skill riêng.
Trị liệu nhóm và siêu cấp thành2skill riêng.60sourceIDs đều được mapping.
Numbers dưới đây là Phimond-authored: raw Mana/Dame chưa giải mã nên không
nhận là công thức gốc. Gộp tier thànhrank trong v1/v2 bị thay bởi v3.

|Tier AoE|Power mỗi địch|MP vật lý|MP phép|CD|Level học|
|---|---|---|---|---|---|
|Nhẹ|.45×ATK/MAG|10|12|0|1|
|Thường|.75×ATK/MAG|18|20|1|5|
|Cao cấp|1.05×ATK/MAG|26|28|1|20|
|Siêu cấp|1.35×ATK/MAG|36|38|2|40|

Power đã là mỗi target, không nhân thêm “AoE.75”. Hit/crit độc lập từng địch.
AoE chỉ một địch không được tăng power. Chart/rules damage và MP P11 giữ nguyên.
Không tạo status miễn phí theo tên Lốc Xoáy/Bão Tuyết/Hủy Diệt.

Ví dụ ATK100/DEF50, neutral, khôngcrit:30/50/70/90 damage mỗi target; nếu đủ3hit
tổng90/150/210/270. Với3quái25HP, cảNhẹ vàSiêu cấp kill nếuhit, nhưng Nhẹ
chỉ10MP thay36MP. Ngân sách50MP cho5cast Nhẹ hoặc1cast Siêu cấp trước hồi MP,
không tínhmiss/CD/thay target. Đây là arithmetic, không đo clear speed thật.

Mỗi tier học riêng tại trainer và chiếm1slot; mangNhẹ+Siêu cấp=2/6slot.
Học mạnh không consume skill nhẹ, không auto-upgrade/khóa nhẹ. AoE family và
groupheal tier cố địnhrank1;7signature cũngrank1. Damage/heal khác vẫnrank1–3.
Giá học từngtier theolevel D03; chỉ skillcurrent truyền, không cảfamily.
QuênNhẹ để lấy mạnh là replacement owner chọn; muốn học lại dùng luậtrelearn.
Pet auto dùng thứ tự đã chọn; farm đặtNhẹ trước mạnh, burst có thể đổi trước
trận. Không đọc RNG tương lai để chọn “đủkill”. Quái tie pool order Nhẹ trước
mạnh, chỉ dùng subset learned/level-valid; P02 phải đo chiến thuật NPC.

Groupheal thường .85MAG+6/ally,MP28/CD2/Lv20; siêu cấp1.10MAG+10/ally,
MP40/CD3/Lv40. Ally sống, khôngdamage/crit/revive; không rank scaling thêm.

## Hai trục độc lập: target và damage/effect

|Ví dụ|Target|Công dụng|
|---|---|---|
|Cường kích|Đơn thể địch|Damage thuần|
|Càn quét nhẹ và4tier|AoE tất cả địch|Damage thuần|
|Hỏa ấn/Độc châm/Minh ấn|Đơn thể địch|Damage +status sauhit, SR chỉ giảm proc|
|Sleep/bind/blind/slow|Đơn thể địch|Hiệu ứng khôngdamage; không dựng damage ngầm|
|Trị liệu|Đơn thể ally/self|HồiHP, khôngdamage|
|Trị liệu nhóm|AoE ally sống|HồiHP, khôngdamage|
|Thiên thần hạ phàm|AoE ally|Buff, khôngdamage|

Khôngdamage không đồng nghĩa miễn kiểm tra hit/SR: enemy debuff/control vẫn
kiểm tra chance theo contract; ally buff/heal khôngcrit/khôngenemy-hit roll.
Damage+effect vẫn códirectdamage khi procstatus thất bại. Target/type/channel,
MP/CD/learnlevel và sourceIDs hiện ngay card/detail; web có3filter riêng.

## Mỗi Race có đủ hai hướng damage

Kiểm tra Primary roles riêng để không gọi pet phụMAG thấp là caster. MỗiRace
có ít nhất2primaryphysical và2primarymagic; primaryHybrid đếm riêng. Frozen
P11 identity/stats/role không sửa. Các poolprimarydamage vàHybrid đều có skill
single vàtierAoEnhẹ đúngchannel, cùngtiers để lựa chọn; samplebuild≤6.

|Race|Primary vật lý|Primary phép|PrimaryHybrid|
|---|---|---|---|
|Vong Linh|9|7|0|
|Thực Vật|5|3|0|
|Rồng|4|4|3|
|Ác Ma|6|7|2|
|Thú|12|2|0|
|Chim|11|6|0|
|Côn Trùng|7|6|1|
|Linh|6|6|1|

Đây là đủ lựa chọn theo toànRace, không phải50/50 hoặc đủ từngStar. Web công
khai gapsNormal theoStar có tínhsecondary/Hybrid: ví dụ Thú1★ chưa córolephép,
Thú5★ chưa córolephép; Plant4★ thiếuphép; Demon5★ thiếuvật lý; Insect5★
thiếuvật lý. Cần P11 owner sửa role/stats nếu scope sau này yêu cầu mọiStar có
cảhai. Không bù bằng cách ép caster yếu lênPhysical pet rồi gọi là balanced.

## Phạm vi revision

95skills:73v2+21AoE tier bổ sung+1groupheal siêu cấp. Pool lớn hơn không auto
grant. D01/D03/D07/D14/D15/D16 thay đổi, mở lại approval các nhóm đó; những
nhóm pending từv2 vẫnpending.7signature v2 giữ nguyên hành vi/số/cost trongcatalog, chỉ thêm metadata target_shape/damage_mode, ghi nhận
owner đã thấy ổn, không suy ra chấp thuận cảphase. Feedback/candidate cũ giữ
nguyên; bảnv3draft và approval unchanged carry có provenance.

Owner v2 có lựa chọn D02approved chưalưu và notes trống trong tab. Giữ tab
và snapshot evidence/owner-unsaved-v2-draft.json; chuyển bảnnháp các mục không
đổi vào v3 với provenance, không gửi kết luận hoặc gọi là finalacceptance.
