# P13 — Review Normal / Special và cặp bố mẹ

Trạng thái: đề xuất để owner duyệt. Baseline 152; candidate 160 chưa kích hoạt.

- Phương án chính 160 loài: thêm 6 Normal 5★ và 2 Special Hybrid 5★. Normal 4★ có 17 loài, Normal 5★ có 20; Special 4★ có 4, Special 5★ có 15. Không dùng Special để lấp độ phủ Normal.
- Mỗi race có primary vật lý + primary phép ở Normal 4★ và 5★. 4★ đổi Trưởng Lão Người Cây sang phép/Support, Long Vương Hắc Ám sang vật lý/Disruptor, Chim Đại Phì sang phép/Disruptor. Tinh Tinh Rock giữ Tank, secondary vật lý để có đường dung hợp phù hợp.
- Normal 5★: Tinh Linh Bách Hoa vật lý/Support; Độc Đằng Nữ phép/Disruptor; Trùng Bất Tử Địa Huyệt vật lý/Tank; Totem phép/Support; Trụy Thiên Sứ Hybrid/Support. Thánh Rồng Thái Cổ và Nhân Sư giữ Hybrid. Sáu Normal mới lấp các kênh còn thiếu, không thay thế ba Hybrid.
- Special 4★ giữ bốn bản sắc: Thanh Long Hybrid, Bạch Hổ vật lý, Chu Tước phép/Support, Huyền Vũ Tank/Support. Native kit theo role, signature đã review không thay đổi.
- Special 5★: Thủ Lĩnh Hắc Ám vật lý/Tank; Trùng Mẫu Mào Vàng phép/Support; Ngựa Bùn Cỏ phép/Support; Cây Cự Linh Tank/vật lý; Đảo Thiên Đường vật lý/Tank. Các Special khác giữ role baseline. Long Thần Song Ấn (Rồng) và Ma Chủ Song Cực (Ác Ma) là hai Special Hybrid mới.
- Recipe candidate: cùng Star, hai Normal khác species, ít nhất một bố mẹ cùng race với con. Con vật lý cần hai bố mẹ có hướng vật lý; con phép cần hai bố mẹ có hướng phép. Hybrid cho phép vật lý + phép hoặc Hybrid + Hybrid. Tank/Support có điều kiện và lý do theo kit; không dùng ngoại lệ này để ép caster tiêu pet vật lý.
- Nữ Đế dùng Nữ Vương Bạch Cốt + Ma Nhãn Hư Không, đều phép. Thánh Rồng Thái Cổ + Nhân Sư → Long Thần Song Ấn; Trụy Thiên Sứ + Nhân Sư → Ma Chủ Song Cực. Ba Normal Hybrid đều có đường Special Hybrid 5★.
- Chọn Special và recipe trước, đảo slot không đổi kết quả. Có 28 cặp candidate không trùng: 13 cặp cho 4 Special 4★ và 15 cặp cho 15 Special 5★. Mọi Normal 4★ và 5★ có ít nhất một đường dung hợp; không dùng Special làm material trong các recipe này.
- 17 recipe APK giữ riêng làm bằng chứng, không bắt buộc dùng làm luật game. Các recipe thay thế 4★ cho cùng Special phải có preview kết quả/kit, không random đổi species. Chi phí/xác suất/Plus và vai trò Chính/Phụ trong kế thừa vẫn thuộc P16/P20.
- Ghép cùng damage channel chưa đảm bảo truyền được skill: current skills bố mẹ còn lọc Race whitelist của con. Cần preview skill truyền được; Native Pool của Special tự có kit theo role. Basic 0MP luôn còn; skill nhẹ vẫn riêng để farm, không bị tier mạnh thay thế.
- Hybrid chia ngân sách ATK/MAG, không cộng hai stat trong một hit, không có hai action/vòng. Bộ sáu slot phải đánh đổi hai damage channel, tier farm và utility. Stat/growth dùng budget và role template P11 của species kết quả, không lấy trung bình stat hoặc total level bố mẹ để tăng power ngoài budget.
- Độ phủ và độ hợp role được kiểm tra tự động; cân bằng số/trận/kinh tế còn cần author numeric stat/MP/pool theo role mới, nơi nhận pet và playtest P02/P07/P15/P16/P19/P20. Đây là bản nghiệm thu design, chưa bật runtime hay yêu cầu vẽ trước owner review.

## 6 Normal 5★ cần brief/vẽ sau duyệt

- P13-NEW-01 — Hươu Rêu Nguyệt (Thú, magic_dps, hệ Địa đề xuất): Hươu có gạc phủ rêu và hạt sáng; silhouette khác Ngựa Bùn Cỏ. AoE phép nhẹ để farm, đơn thể phép và hồi phục phụ.
- P13-NEW-02 — Thiết Giáp Long (Rồng, physical_dps, hệ Địa đề xuất): Rồng thấp, giáp đá và đuôi chùy; khác Thánh Rồng Thái Cổ. Đơn thể vật lý, quét nhẹ, khiên phụ.
- P13-NEW-03 — Tinh Vân Long (Rồng, magic_dps, hệ Quang đề xuất): Rồng mảnh, vây sao và lõi sáng; nhận diện phép từ xa. AoE phép nhẹ, phép đơn thể và dispel phụ.
- P13-NEW-04 — Đao Ma Huyết Giáp (Ác Ma, physical_dps, hệ Hỏa đề xuất): Ác ma vai rộng, lưỡi đao và giáp nứt đỏ. Chém đơn thể, quét nhẹ và debuff phụ.
- P13-NEW-05 — Ma Nhãn Hư Không (Ác Ma, magic_dps, hệ Âm đề xuất): Ác ma bay với một mắt và vòng ấn; khác Trụy Thiên Sứ. AoE phép nhẹ, phép đơn thể và control phụ.
- P13-NEW-06 — Hộ Vệ Thạch Linh (Tinh Linh, physical_dps, hệ Địa đề xuất): Linh thể đá có nắm đấm lớn, lõi nhỏ; khác Nhân Sư và Cự Ma. Vật lý đơn thể, quét nhẹ và bảo vệ phụ.

## 2 Special Hybrid 5★ mới

- P13-SPECIAL-01 — Long Thần Song Ấn (Rồng): Rồng hai cụm giáp và vây ấn sáng, nhìn rõ cả móng/vuốt vật lý và lõi phép; không sao chép Thanh Long. Kit có hai damage channel, buff phụ; không cộng ATK+MAG trong một hit.
- P13-SPECIAL-02 — Ma Chủ Song Cực (Ác Ma): Ác ma có một tay vũ khí và một tay ấn phép, silhouette khác Ma Vương Hút Máu. Kit vật lý/phép và debuff phụ, giữ đánh đổi sáu slot.

## Recipe nguồn (không phải recipe mới hoặc runtime đã bật)

- recipe_special_0001: Nữ Vương Bạch Cốt [Chính] + Tinh Linh Bách Hoa [Phụ] → Nữ Đế Minh Giới (bố mẹ 5★).
- recipe_special_0002: Rồng Xương Băng [Chính] + Đại Bàng Vàng [Phụ] → Thủ Lĩnh Hắc Ám (bố mẹ 5★).
- recipe_special_0003: Đại Ác Ma [Chính] + Gấu Trúc Ma Pháp [Phụ] → Thanh Long (bố mẹ 4★).
- recipe_special_0004: Tinh Tinh Rock [Chính] + Trùng Gai Nhọn [Phụ] → Bạch Hổ (bố mẹ 4★).
- recipe_special_0005: Chim Đại Phì [Chính] + Ma Gương Thủy Tinh [Phụ] → Chu Tước (bố mẹ 4★).
- recipe_special_0006: Nhện Phu Nhân [Chính] + Totem Thượng Cổ [Phụ] → Trùng Mẫu Mào Vàng (bố mẹ 5★).
- recipe_special_0007: Thú Lớn Dung Nham [Chính] + Đại Tuyết Quái [Phụ] → Huyền Vũ (bố mẹ 4★).
- recipe_special_0008: Nhân Sư [Chính] + Người Tuyết Viễn Cổ [Phụ] → Thần Tướng Cự Ma (bố mẹ 5★).
- recipe_special_0009: Totem Thượng Cổ [Chính] + Nữ Vương Bạch Cốt [Phụ] → Thần Đèn (bố mẹ 5★).
- recipe_special_0010: Độc Đằng Nữ [Chính] + Trùng Bất Tử Địa Huyệt [Phụ] → Linh Tiên Hoa Hương (bố mẹ 5★).
- recipe_special_0011: Tinh Linh Bách Hoa [Chính] + Sói Xích Viêm [Phụ] → Cây Cự Linh (bố mẹ 5★).
- recipe_special_0012: Trụy Thiên Sứ [Chính] + Nhân Sư [Phụ] → Ma Vương Hút Máu (bố mẹ 5★).
- recipe_special_0013: Sói Xích Viêm [Chính] + Chim Cú Địa Ngục [Phụ] → Ngựa Bùn Cỏ (bố mẹ 5★).
- recipe_special_0014: Người Tuyết Viễn Cổ [Chính] + Nhân Sư [Phụ] → Thú Vàng Một Sừng (bố mẹ 5★).
- recipe_special_0015: Chim Cú Địa Ngục [Chính] + Nhện Phu Nhân [Phụ] → Đảo Thiên Đường (bố mẹ 5★).
- recipe_special_0016: Trùng Bất Tử Địa Huyệt [Chính] + Độc Đằng Nữ [Phụ] → Đại Vương Bọ Cạp (bố mẹ 5★).
- recipe_special_0017: Đại Bàng Vàng [Chính] + Rồng Xương Băng [Phụ] → Chim Ái Thần (bố mẹ 5★).

## Recipe candidate — không bắt buộc giữ công thức APK

- Nữ Đế Minh Giới: Nữ Vương Bạch Cốt + Ma Nhãn Hư Không. Hai caster Âm; giữ kit phép khi đi từ Normal lên Nữ Đế.
- Thủ Lĩnh Hắc Ám: Rồng Xương Băng + Đại Bàng Vàng. Giữ cặp vật lý nguồn; Tank có vật lý phụ.
- Thanh Long: Đại Ác Ma + Trùng Gai Nhọn. Phép + vật lý có chủ đích để tạo Thanh Long Hybrid; không áp dụng cho Special chuyên phép.
- Bạch Hổ: Đại Tuyết Quái + Trùng Gai Nhọn. Hai vật lý; tránh dùng Tank/control không có hướng vật lý làm bố mẹ chính.
- Chu Tước: Chim Đại Phì + Ma Gương Thủy Tinh. Hai caster 4★; Chim Đại Phì chuyển primary phép, có bố mẹ Chim.
- Trùng Mẫu Mào Vàng: Nhện Phu Nhân + Totem Thượng Cổ. Phép + phép/Support phù hợp Support/control sử dụng MAG.
- Huyền Vũ: Thú Lớn Dung Nham + Tinh Tinh Rock. Linh vật lý + Thú Tank/vật lý cho Huyền Vũ; giữ bố mẹ cùng race Linh.
- Thần Tướng Cự Ma: Hộ Vệ Thạch Linh + Trùng Bất Tử Địa Huyệt. Vật lý + vật lý/Tank cho Cự Ma; không cần tiêu Nhân Sư Hybrid.
- Thần Đèn: Totem Thượng Cổ + Tinh Vân Long. Hai caster; Support phụ của Totem hỗ trợ kit hồi phục.
- Linh Tiên Hoa Hương: Độc Đằng Nữ + Nhện Phu Nhân. Hai caster cho Linh Tiên Hoa Hương Support/phép; bỏ bố mẹ vật lý.
- Cây Cự Linh: Tinh Linh Bách Hoa + Người Tuyết Viễn Cổ. Hai hướng vật lý → Cây Cự Linh Tank/vật lý; giữ gốc race Thực Vật và khả năng đánh theo ATK.
- Ma Vương Hút Máu: Ma Nhãn Hư Không + Chim Cú Địa Ngục. Hai caster; không buộc người chơi bỏ hai Hybrid để nhận caster thuần.
- Ngựa Bùn Cỏ: Hươu Rêu Nguyệt + Nữ Vương Bạch Cốt. Hai caster; Hươu Rêu Nguyệt là Normal Thú phép, Ngựa vẫn Special.
- Thú Vàng Một Sừng: Thiết Giáp Long + Sói Xích Viêm. Hai vật lý cho Thú Vàng Một Sừng; không dùng Hybrid làm material mặc định.
- Đảo Thiên Đường: Người Tuyết Viễn Cổ + Đại Bàng Vàng. Tank/vật lý + Chim vật lý → Đảo Thiên Đường vật lý/Tank; giữ race Chim, không tiêu caster.
- Đại Vương Bọ Cạp: Trùng Bất Tử Địa Huyệt + Đao Ma Huyết Giáp. Hai vật lý cho Đại Vương Bọ Cạp; không tiêu caster Độc Đằng Nữ.
- Chim Ái Thần: Chim Cú Địa Ngục + Độc Đằng Nữ. Hai caster cho Chim Ái Thần Support/phép; thay cặp hai vật lý nguồn.
- Thanh Long: Ma Vương Địa Ngục + Trưởng Lão Người Cây. Ác Ma vật lý + Thực Vật phép → Thanh Long Ác Ma Hybrid.
- Thanh Long: Ma Vương Địa Ngục + Trùng Hốt Lỗ. Ác Ma vật lý + Côn Trùng phép → Thanh Long Ác Ma Hybrid.
- Bạch Hổ: Tử Thần + Tinh Tinh Rock. Tử Thần + Tinh Tinh Rock Tank/vật lý: hướng vật lý, bố mẹ Thú giữ gốc race của Bạch Hổ.
- Bạch Hổ: Long Vương Hắc Ám + Đại Tuyết Quái. Long Vương Hắc Ám + Đại Tuyết Quái: hai vật lý, có bố mẹ Thú.
- Bạch Hổ: Chim Đa Đa + Đại Tuyết Quái. Chim Đa Đa + Đại Tuyết Quái: hai vật lý, có bố mẹ Thú.
- Chu Tước: Chim Đại Phì + Pharaon. Chim Đại Phì + Pharaon: hai caster, có bố mẹ Chim.
- Chu Tước: Chim Đại Phì + Hải Long Ba Đầu. Chim Đại Phì + Hải Long Ba Đầu: hai caster, có bố mẹ Chim.
- Chu Tước: Chim Đại Phì + Gấu Trúc Ma Pháp. Chim Đại Phì + Gấu Trúc Ma Pháp: hai caster, có bố mẹ Chim.
- Huyền Vũ: Thú Lớn Dung Nham + Hoa ăn Thịt Người Ba Đầu. Thú Lớn Dung Nham + Hoa Ăn Thịt Người Ba Đầu: vật lý + vật lý/Tank cho Huyền Vũ.
- Long Thần Song Ấn: Thánh Rồng Thái Cổ + Nhân Sư. Thánh Rồng Thái Cổ + Nhân Sư, cả hai Hybrid: giữ đường phát triển song công của Rồng.
- Ma Chủ Song Cực: Trụy Thiên Sứ + Nhân Sư. Trụy Thiên Sứ + Nhân Sư, cả hai Hybrid: giữ đường phát triển song công của Ác Ma.

## Gap còn lại

Hai Special Hybrid 5★ đã đưa vào candidate 160: Long Thần Song Ấn (Rồng) và Ma Chủ Song Cực (Ác Ma). Cả ba Normal Hybrid 5★ có recipe sang Special Hybrid 5★; không còn nhánh 158 bỏ lửng Hybrid.

Normal 5★ chưa có recipe candidate: 
