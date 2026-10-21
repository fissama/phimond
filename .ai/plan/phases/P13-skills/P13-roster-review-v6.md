# P13 — Review Normal / Special và cặp bố mẹ

Trạng thái: đề xuất để owner duyệt. Baseline 152; candidate 160 chưa kích hoạt.

- Phương án chính 160 loài: thêm 6 Normal 5★ và 2 Special Hybrid 5★. Normal 4★ có 17 loài, Normal 5★ có 20; Special 4★ có 4, Special 5★ có 15. Không dùng Special để lấp độ phủ Normal.
- Mỗi race có primary vật lý + primary phép ở Normal 4★ và 5★. 4★ đổi Mộc Trưởng Lão sang phép/Support, Hắc Long Vương sang vật lý/Disruptor, Đại Phúc Điểu sang phép/Disruptor. Thạch Viên giữ Tank, secondary vật lý để có đường dung hợp phù hợp.
- Normal 5★: Bách Hoa Tiên Tử vật lý/Support; Độc Đằng Nữ phép/Disruptor; Địa Huyệt Ma Trùng vật lý/Tank; Totem phép/Support; Đọa Thiên Sứ Hybrid/Support. Thái Cổ Thánh Long và Nhân Sư giữ Hybrid. Sáu Normal mới lấp các kênh còn thiếu, không thay thế ba Hybrid.
- Special 4★ giữ bốn bản sắc: Thanh Long Hybrid, Bạch Hổ vật lý, Chu Tước phép/Support, Huyền Vũ Tank/Support. Native kit theo role, signature đã review không thay đổi.
- Special 5★: Hắc Kỵ Vương vật lý/Tank; Kim Quan Chu Hậu phép/Support; Vân Mao Đà phép/Support; Cự Linh Mộc Tank/vật lý; Thiên Đường Điểu vật lý/Tank. Các Special khác giữ role baseline. Long Thần Song Ấn (Rồng) và Ma Chủ Song Cực (Ác Ma) là hai Special Hybrid mới.
- Recipe candidate: cùng Star, hai Normal khác species, ít nhất một bố mẹ cùng race với con. Con vật lý cần hai bố mẹ có hướng vật lý; con phép cần hai bố mẹ có hướng phép. Hybrid cho phép vật lý + phép hoặc Hybrid + Hybrid. Tank/Support có điều kiện và lý do theo kit; không dùng ngoại lệ này để ép caster tiêu pet vật lý.
- Nữ Đế dùng Bạch Cốt Nữ Vương + Ma Nhãn Hư Không, đều phép. Thái Cổ Thánh Long + Nhân Sư → Long Thần Song Ấn; Đọa Thiên Sứ + Nhân Sư → Ma Chủ Song Cực. Ba Normal Hybrid đều có đường Special Hybrid 5★.
- Chọn Special và recipe trước, đảo slot không đổi kết quả. Có 28 cặp candidate không trùng: 13 cặp cho 4 Special 4★ và 15 cặp cho 15 Special 5★. Mọi Normal 4★ và 5★ có ít nhất một đường dung hợp; không dùng Special làm material trong các recipe này.
- 17 recipe APK giữ riêng làm bằng chứng, không bắt buộc dùng làm luật game. Các recipe thay thế 4★ cho cùng Special phải có preview kết quả/kit, không random đổi species. Chi phí/xác suất/Plus và vai trò Chính/Phụ trong kế thừa vẫn thuộc P16/P20.
- Ghép cùng damage channel chưa đảm bảo truyền được skill: current skills bố mẹ còn lọc Race whitelist của con. Cần preview skill truyền được; Native Pool của Special tự có kit theo role. Basic 0MP luôn còn; skill nhẹ vẫn riêng để farm, không bị tier mạnh thay thế.
- Hybrid chia ngân sách ATK/MAG, không cộng hai stat trong một hit, không có hai action/vòng. Bộ sáu slot phải đánh đổi hai damage channel, tier farm và utility. Stat/growth dùng budget và role template P11 của species kết quả, không lấy trung bình stat hoặc total level bố mẹ để tăng power ngoài budget.
- Độ phủ và độ hợp role được kiểm tra tự động; cân bằng số/trận/kinh tế còn cần author numeric stat/MP/pool theo role mới, nơi nhận pet và playtest P02/P07/P15/P16/P19/P20. Đây là bản nghiệm thu design, chưa bật runtime hay yêu cầu vẽ trước owner review.

## 6 Normal 5★ cần brief/vẽ sau duyệt

- P13-NEW-01 — Nguyệt Đài Lộc (Thú, magic_dps, hệ Địa đề xuất): Hươu có gạc phủ rêu và hạt sáng; silhouette khác Vân Mao Đà. AoE phép nhẹ để farm, đơn thể phép và hồi phục phụ.
- P13-NEW-02 — Thiết Giáp Long (Rồng, physical_dps, hệ Địa đề xuất): Rồng thấp, giáp đá và đuôi chùy; khác Thái Cổ Thánh Long. Đơn thể vật lý, quét nhẹ, khiên phụ.
- P13-NEW-03 — Tinh Vân Long (Rồng, magic_dps, hệ Quang đề xuất): Rồng mảnh, vây sao và lõi sáng; nhận diện phép từ xa. AoE phép nhẹ, phép đơn thể và dispel phụ.
- P13-NEW-04 — Đao Ma Huyết Giáp (Ác Ma, physical_dps, hệ Hỏa đề xuất): Ác ma vai rộng, lưỡi đao và giáp nứt đỏ. Chém đơn thể, quét nhẹ và debuff phụ.
- P13-NEW-05 — Ma Nhãn Hư Không (Ác Ma, magic_dps, hệ Âm đề xuất): Ác ma bay với một mắt và vòng ấn; khác Đọa Thiên Sứ. AoE phép nhẹ, phép đơn thể và control phụ.
- P13-NEW-06 — Hộ Vệ Thạch Linh (Tinh Linh, physical_dps, hệ Địa đề xuất): Linh thể đá có nắm đấm lớn, lõi nhỏ; khác Nhân Sư và Cự Ma. Vật lý đơn thể, quét nhẹ và bảo vệ phụ.

## 2 Special Hybrid 5★ mới

- P13-SPECIAL-01 — Long Thần Song Ấn (Rồng): Rồng hai cụm giáp và vây ấn sáng, nhìn rõ cả móng/vuốt vật lý và lõi phép; không sao chép Thanh Long. Kit có hai damage channel, buff phụ; không cộng ATK+MAG trong một hit.
- P13-SPECIAL-02 — Ma Chủ Song Cực (Ác Ma): Ác ma có một tay vũ khí và một tay ấn phép, silhouette khác Huyết Ma Vương. Kit vật lý/phép và debuff phụ, giữ đánh đổi sáu slot.

## Recipe nguồn (không phải recipe mới hoặc runtime đã bật)

- recipe_special_0001: Bạch Cốt Nữ Vương [Chính] + Bách Hoa Tiên Tử [Phụ] → Minh Giới Nữ Đế (bố mẹ 5★).
- recipe_special_0002: Băng Cốt Long [Chính] + Kim Sí Đại Bằng [Phụ] → Hắc Kỵ Vương (bố mẹ 5★).
- recipe_special_0003: Đại Ác Ma [Chính] + Ma Pháp Hùng Miêu [Phụ] → Thanh Long (bố mẹ 4★).
- recipe_special_0004: Thạch Viên [Chính] + Thạch Thứ Trùng [Phụ] → Bạch Hổ (bố mẹ 4★).
- recipe_special_0005: Đại Phúc Điểu [Chính] + Thủy Tinh Ma Kính [Phụ] → Chu Tước (bố mẹ 4★).
- recipe_special_0006: Điệp Hậu [Chính] + Thượng Cổ Đồ Đằng [Phụ] → Kim Quan Chu Hậu (bố mẹ 5★).
- recipe_special_0007: Dung Nham Cự Nhân [Chính] + Tuyết Mao Quái [Phụ] → Huyền Vũ (bố mẹ 4★).
- recipe_special_0008: Nhân Sư [Chính] + Viễn Cổ Tuyết Nhân [Phụ] → Thần Tướng Cự Ma (bố mẹ 5★).
- recipe_special_0009: Thượng Cổ Đồ Đằng [Chính] + Bạch Cốt Nữ Vương [Phụ] → Đăng Thần (bố mẹ 5★).
- recipe_special_0010: Độc Đằng Nữ [Chính] + Địa Huyệt Ma Trùng [Phụ] → Linh Tiên Hoa Hương (bố mẹ 5★).
- recipe_special_0011: Bách Hoa Tiên Tử [Chính] + Xích Viêm Lang [Phụ] → Cự Linh Mộc (bố mẹ 5★).
- recipe_special_0012: Đọa Thiên Sứ [Chính] + Nhân Sư [Phụ] → Huyết Ma Vương (bố mẹ 5★).
- recipe_special_0013: Xích Viêm Lang [Chính] + Địa Ngục Quái Điểu [Phụ] → Vân Mao Đà (bố mẹ 5★).
- recipe_special_0014: Viễn Cổ Tuyết Nhân [Chính] + Nhân Sư [Phụ] → Kim Kỳ Lân (bố mẹ 5★).
- recipe_special_0015: Địa Ngục Quái Điểu [Chính] + Điệp Hậu [Phụ] → Thiên Đường Điểu (bố mẹ 5★).
- recipe_special_0016: Địa Huyệt Ma Trùng [Chính] + Độc Đằng Nữ [Phụ] → Độc Hạt Vương (bố mẹ 5★).
- recipe_special_0017: Kim Sí Đại Bằng [Chính] + Băng Cốt Long [Phụ] → Ái Thần Điểu (bố mẹ 5★).

## Recipe candidate — không bắt buộc giữ công thức APK

- Minh Giới Nữ Đế: Bạch Cốt Nữ Vương + Ma Nhãn Hư Không. Hai caster Âm; giữ kit phép khi đi từ Normal lên Nữ Đế.
- Hắc Kỵ Vương: Băng Cốt Long + Kim Sí Đại Bằng. Giữ cặp vật lý nguồn; Tank có vật lý phụ.
- Thanh Long: Đại Ác Ma + Thạch Thứ Trùng. Phép + vật lý có chủ đích để tạo Thanh Long Hybrid; không áp dụng cho Special chuyên phép.
- Bạch Hổ: Tuyết Mao Quái + Thạch Thứ Trùng. Hai vật lý; tránh dùng Tank/control không có hướng vật lý làm bố mẹ chính.
- Chu Tước: Đại Phúc Điểu + Thủy Tinh Ma Kính. Hai caster 4★; Đại Phúc Điểu chuyển primary phép, có bố mẹ Chim.
- Kim Quan Chu Hậu: Điệp Hậu + Thượng Cổ Đồ Đằng. Phép + phép/Support phù hợp Support/control sử dụng MAG.
- Huyền Vũ: Dung Nham Cự Nhân + Thạch Viên. Linh vật lý + Thú Tank/vật lý cho Huyền Vũ; giữ bố mẹ cùng race Linh.
- Thần Tướng Cự Ma: Hộ Vệ Thạch Linh + Địa Huyệt Ma Trùng. Vật lý + vật lý/Tank cho Cự Ma; không cần tiêu Nhân Sư Hybrid.
- Đăng Thần: Thượng Cổ Đồ Đằng + Tinh Vân Long. Hai caster; Support phụ của Totem hỗ trợ kit hồi phục.
- Linh Tiên Hoa Hương: Độc Đằng Nữ + Điệp Hậu. Hai caster cho Linh Tiên Hoa Hương Support/phép; bỏ bố mẹ vật lý.
- Cự Linh Mộc: Bách Hoa Tiên Tử + Viễn Cổ Tuyết Nhân. Hai hướng vật lý → Cự Linh Mộc Tank/vật lý; giữ gốc race Thực Vật và khả năng đánh theo ATK.
- Huyết Ma Vương: Ma Nhãn Hư Không + Địa Ngục Quái Điểu. Hai caster; không buộc người chơi bỏ hai Hybrid để nhận caster thuần.
- Vân Mao Đà: Nguyệt Đài Lộc + Bạch Cốt Nữ Vương. Hai caster; Nguyệt Đài Lộc là Normal Thú phép, Ngựa vẫn Special.
- Kim Kỳ Lân: Thiết Giáp Long + Xích Viêm Lang. Hai vật lý cho Kim Kỳ Lân; không dùng Hybrid làm material mặc định.
- Thiên Đường Điểu: Viễn Cổ Tuyết Nhân + Kim Sí Đại Bằng. Tank/vật lý + Chim vật lý → Thiên Đường Điểu vật lý/Tank; giữ race Chim, không tiêu caster.
- Độc Hạt Vương: Địa Huyệt Ma Trùng + Đao Ma Huyết Giáp. Hai vật lý cho Độc Hạt Vương; không tiêu caster Độc Đằng Nữ.
- Ái Thần Điểu: Địa Ngục Quái Điểu + Độc Đằng Nữ. Hai caster cho Ái Thần Điểu Support/phép; thay cặp hai vật lý nguồn.
- Thanh Long: Địa Ngục Ma Vương + Mộc Trưởng Lão. Ác Ma vật lý + Thực Vật phép → Thanh Long Ác Ma Hybrid.
- Thanh Long: Địa Ngục Ma Vương + Ách Vận Trùng. Ác Ma vật lý + Côn Trùng phép → Thanh Long Ác Ma Hybrid.
- Bạch Hổ: Tử Thần + Thạch Viên. Tử Thần + Thạch Viên Tank/vật lý: hướng vật lý, bố mẹ Thú giữ gốc race của Bạch Hổ.
- Bạch Hổ: Hắc Long Vương + Tuyết Mao Quái. Hắc Long Vương + Tuyết Mao Quái: hai vật lý, có bố mẹ Thú.
- Bạch Hổ: Liệt Phong Ưng + Tuyết Mao Quái. Liệt Phong Ưng + Tuyết Mao Quái: hai vật lý, có bố mẹ Thú.
- Chu Tước: Đại Phúc Điểu + Sa Thi Vương. Đại Phúc Điểu + Sa Thi Vương: hai caster, có bố mẹ Chim.
- Chu Tước: Đại Phúc Điểu + Tam Thủ Hải Long. Đại Phúc Điểu + Tam Thủ Hải Long: hai caster, có bố mẹ Chim.
- Chu Tước: Đại Phúc Điểu + Ma Pháp Hùng Miêu. Đại Phúc Điểu + Ma Pháp Hùng Miêu: hai caster, có bố mẹ Chim.
- Huyền Vũ: Dung Nham Cự Nhân + Tam Thủ Thực Hoa. Dung Nham Cự Nhân + Thực Nhân Hoa Ba Đầu: vật lý + vật lý/Tank cho Huyền Vũ.
- Long Thần Song Ấn: Thái Cổ Thánh Long + Nhân Sư. Thái Cổ Thánh Long + Nhân Sư, cả hai Hybrid: giữ đường phát triển song công của Rồng.
- Ma Chủ Song Cực: Đọa Thiên Sứ + Nhân Sư. Đọa Thiên Sứ + Nhân Sư, cả hai Hybrid: giữ đường phát triển song công của Ác Ma.

## Gap còn lại

Hai Special Hybrid 5★ đã đưa vào candidate 160: Long Thần Song Ấn (Rồng) và Ma Chủ Song Cực (Ác Ma). Cả ba Normal Hybrid 5★ có recipe sang Special Hybrid 5★; không còn nhánh 158 bỏ lửng Hybrid.

Normal 5★ chưa có recipe candidate: 
