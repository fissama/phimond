# Review Element, role, base/growth của 152 Species — 2026-10-12

**Kết luận: v1 đạt kiểm tra cấu trúc và ngân sách; chưa đủ để chốt cân bằng và
bản sắc nội dung. Cần một lượt authoring v2 trước khi coi đây là stat catalog
cuối cùng.** Review không đổi số hay identity của152 loài.

Evidence: [catalog-review JSON](evidence/catalog-review-20261012.json),
[catalog hiện tại](P11-species-catalog.json), [builder](evidence/build_species_catalog.py).
Toàn bộ152 record được kiểm tra số,97 mô tả nguồn được đọc đối chiếu;55 record
không có mô tả nguồn được đánh dấu rõ.22 cờ về signature là danh sách cần curator
xử lý, không phải22 lỗi công thức đã được chứng minh.

## Những phần đã ổn

- 152 frozen ID,135 Normal/17 Special đúng; không đổi Race/Star/class/recipe/art.
- 304 lớp base/growth đạt precision, budget tolerance, bounds và Primary guards.
- Role vocabulary hợp lý; phân biệt Hybrid dual damage, Support phục vụ đồng đội,
  Disruptor có khống chế/debuff ngoài mấtHP. Không cấp skill tự động.
- Growth deterministic, grade giới hạn riêng main/aux, Plus không nhân stat.
- Main-budget bands tại Lv60/B không đảo thứ tự Normal1→5 và các half-step Special:
  N1 216–218; N2 236.9–239.9; N3 263.4–265.4; N4 296.1–296.4;
  S4 320.6–321.6; N5 346.2–348.2; S5 372.7–374.8.
  Đây là actual catalog budget range trên các role, không phải chỉ số combat duy nhất.
- Equal-budget không có nghĩa equal DPS/survival/control. Chưa có damage/cost/kit
  P13 để kết luận vai trò nào mạnh nhất hay pet nào thắng mọi trận.

## Findings theo mức ưu tiên

### R-C01 — High: template chưa thành bản sắc Species

Builder targets() chỉ dùng Star/class/Primary/Secondary, rồi round_half_up;
không có authored modifier theo Species.152 loài có79 vector base+growth khác nhau;
31 nhóm trùng vector gồm104 loài.19 nhóm gồm50 loài còn trùng cả Element.
Nhóm Physical1 gồm13 loài có cùng cả12 giá trị. Nhện Vong Linh, Chó Ác Ma,
Rồng Có Cánh, Rồng Mào Đỏ đều cùng HP250/ATK45/MAG10/DEF20/SPD40/SR20,
growth5/.9/.2/.4/1.02/.51.

Trùng stats không tự động làm game mất cân bằng: Native Skill Pools khác nhau
có thể tạo khác biệt. Tuy nhiên hiện P13 chưa cung cấp kit; hơn nữa mô tả nguồn
đã nói các signature trái nhau mà v1 không thể hiện. Vì vậy không thể dùng
PASS của validator làm bằng chứng rằng authoring152 loài đã hoàn thiện.

**Sửa đề xuất:** thêm modifier có chủ đích cho cả base và growth theo loài,
main±10%/aux±5%, giữ budget/tolerance và Primary guard. Không thêm random jitter
để chỉ tạo vẻ đa dạng; mỗi modifier phải có rationale và tradeoff đo được.

### R-C02 — High: signature tốc độ/phòng thủ/HP từ nguồn bị mất

| Species | Nguồn nói | V1 đang thể hiện |
|---|---|---|
| 0039 Rồng Có Cánh | nhanh nhẹn cao, tự phòng thủ thấp | vector giống Nhện Vong Linh; Lv60B SPD100/DEF43 |
| 0007 Chó Ác Ma | di chuyển nhanh | SPD100 tại Lv60B, bằng Physical1 trung tính |
| 0057 Báo Địa Ngục | rất nhanh, ma võ song thần | Hybrid đúng hướng nhưng SPD100 trung tính |
| 0131 Hư Không Hắc Ám | ma pháp và tốc độ | SPD100, cùng vector với Xác Ướp/U Linh |
| 0106 Chim Cú Địa Ngục | nhanh nhẹn cao nhất | Normal5 Lv60B SPD110; Độc Đằng Nữ115, Trụy Thiên Sứ/Totem112 |
| 0055 Mắt Ác Ma | HP/phòng thủ kém | HP bằng solo Magic1, DEF46 cao hơn solo Magic1 DEF43 tại Lv60 |
| 0038 Tinh Linh Bách Hoa | phòng ngự trưởng thành cao nhất | DEF growth.880 thấp hơn Trùng Bất Tử Địa Huyệt1.120 cùng Normal5 |
| 0125 Nhện Phu Nhân | HP trưởng thành cực cao | HP growth8.000 bằng solo Magic5 template, chưa có signature riêng |

Nguồn là mô tả định tính; không ép mọi chữ “cao nhất” thành xếp hạng tuyệt đối
xuyên Star/class/buff. Nhưng cần định nghĩa cohort (cùng Star/class/role hoặc
cùng Race) và lưu một kiểm tra so sánh cụ thể. Không để “tốc độ thuộc skill P13”
thay cho innate SPD khi chính mục tiêu authoring là phản ánh signature đó.

**Sửa đề xuất:** ưu tiên22 record trong evidence; phân biệt nhanh/chậm, tank HP/
DEF, glass cannon và caster bền. Giữ ±5% SPD/SR đã chốt; nếu không đủ để đạt
mục tiêu, ghi conflict thay vì tự nới band hoặc tráo role chỉ để lấy SPD.

### R-C03 — High: cân bằng role/Element chưa được kiểm chứng bằng kit

Gán Role dựa trên intended function là đúng, nhưng hiện hợp đồng P13 chỉ có
nhãn chung như physical damage hoặc ally recovery. Không có skill, coefficient,
MP cost, cooldown, target/stacking để định giá lợi ích role. Support/Disruptor
cũng chưa được chứng minh tạo value tương xứng phần tấn công đã nhường.

17/17 Special và tổng55/152 Species thiếu mô tả nguồn: assignment là sáng tác
Phimond có khai báo, không phải dữ liệu recovered. Mỗi loài vẫn cần native
function brief cụ thể; premium Special không tự chứng minh kit khỏe/hợp lý.

**Sửa đề xuất:** mỗi Species có brief tối thiểu về đòn chính, công cụ utility,
điểm yếu và kiểu trận hữu ích. P13 hoàn thiện nội dung/số skill theo loài; không
áp skill-count quota. Cần tiêu chí target ally/self để chứng minh Support, và
phân biệt maxHP reduction với raw damage khi xác nhận Disruptor.

### R-C04 — Medium: coverage Element có khoảng trống ở Normal5

Phân bố: earth52 (34.2%), dark36 (23.7%), fire18, water18, wind16, light12.
Normal5 không có Wind; Fire chỉ có Sói Xích Viêm. Wind5 hiện chỉ có Special
Thần Đèn. Special acquisition/source gates chưa mở, nên không được coi Special
Wind5 là phương án Normal progression luôn tiếp cận được.

Không cần ép mỗi hệ bằng số lượng; chart và encounter supply mới quyết định
có mất cân bằng thật không. Hiện chưa có chart P13 nên độ lệch này là rủi ro
coverage có thể kiểm chứng, chưa phải bằng chứng Earth quá mạnh.

**Sửa đề xuất:** lập coverage theo Star, role, acquisition và vùng. Cân nhắc
Đại Bàng Vàng (107) Wind thay vì Light nếu native identity không cần holy magic;
đây là đề xuất authoring, không khẳng định element gốc. Cho phép giữ khoảng
trống nếu có chủ ý và low-Star/high-level Wind có đường dùng rõ.

### R-C05 — Medium: Element thematic hiện là quy ước chưa có contract chiến thuật

Thunder→Wind và ice→Water có thể là cách gộp tốt, nhưng phải ghi Wind bao gồm
storm/lightning và Water bao gồm ice; skill theme không tự quyết định pet element.
Gấu Trúc Ma Pháp→Light, Đại Bàng Vàng→Light, Sách Ma Pháp→Light là lựa chọn
sáng tác cần rationale cụ thể; “phương Đông”, “vàng” hay “ma pháp” tự chúng không
chứng minh Light. Không gán lại Race và không thêm STAB/Race stat bonus.

**Sửa đề xuất:** giữ sáu hệ v1 làm baseline, bổ sung rationale/skill-theme brief
và kiểm tra `skill.element` vs `target.element` cùng P13. Không mở thêm hệ chỉ
để chữa số lượng roster trước khi cân nhắc chart và content cost.

### R-C06 — Medium: có stat domination do rounding, cần định giá utility

Cùng Special5, Lv60B, noinherit/gear:
- Nữ Đế Minh Giới(019) so với Thần Đèn(143): năm stat giống nhau, SPD112>110.
- Đại Vương Bọ Cạp(151) so với Ngựa Bùn Cỏ(148): năm stat giống nhau, SPD112>110;
  cặp này còn cùng Earth.

Các cặp chỉ khác Secondary Disruptor/Support: SR chênh nhỏ của template Support
bị integer/cumulative-floor làm mất tại mốc này, nhưng SPD Disruptor còn lợi.
Đây là **raw six-stat Pareto dominance tại một mốc**, không chứng minh stronger
kit: heal/protect có thể trả lại value. Cần kiểm tra nhiều level/grade và skill.

**Sửa đề xuất:** lưu các cặp dominance trong review; species modifiers hoặc
native utility phải giải thích đánh đổi. Không tự động tăng budget cho loài yếu.

## Authoring v2 đề xuất

1. Giữ bảng grade, anchor, tolerance, main-role shares và half-step đã chốt.
2. Sửa signature có nguồn trước; xác định cohort cho “nhanh nhất/cao nhất”.
3. Viết rõ brief55 loài sáng tác, đặc biệt17 Special; kiểm Element coverage.
4. Thêm modifier theo mục đích, kiểm riêng base/growth và allB/allPerfect ở
   Lv1/Lv60/basecap/+99cap. Không bắt152 vector phải unique nếu kit khác có chủ ý.
5. Làm comparator giữa species same Star/role, tốc độ, SR effectiveness và
   stat dominance; P13/P02 kiểm chứng combat khi có kit/damage/action contracts.

Review này không sửa catalog hoặc số đã chốt: đó là một content revision cần
lưu version rõ. Catalog v1 vẫn là baseline số hợp lệ, **chưa balance-approved**.
