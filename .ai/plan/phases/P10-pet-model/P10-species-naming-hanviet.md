# P10 — Quy ước đặt tên tiếng Việt cho 160 loài

Status: **owner yêu cầu thống nhất phong cách Hán-Việt / JRPG, áp dụng 2026-10-21**.

Phạm vi: chỉ đổi `display_name.vi` (tên hiển thị). ID `species_NNNN`, ID nguồn APK (`NhenVongLinh`, `Pharaon`…), mô tả nguyên bản, asset và art giữ nguyên. Tên nguyên bản của APK vẫn nằm trong [roster_apk84.json](../../../../data/pets/roster_apk84.json).

Bản đối chiếu máy đọc được: [P10-species-naming-hanviet.json](P10-species-naming-hanviet.json).

## Quy ước

1. Trật tự Hán-Việt: bổ ngữ trước, danh từ loài sau (Xích Viêm Lang, Băng Cốt Long, Địa Ngục Ma Vương).
2. Độ dài theo bậc sao: 1-2★ thường 2 âm tiết; 3-4★ 3-4 âm; 5★ và thần thú 4 âm hoặc tước hiệu.
3. Danh từ gốc theo loài: Long, Lang, Hổ, Hùng, Quy, Ưng, Điểu, Chu (nhện), Hạt (bọ cạp), Điệp (bướm), Trùng; Bất Tử dùng Thi/Cốt/Hồn; Ác Ma dùng Ma/Quỷ.
4. Ưu tiên từ đã quen qua truyện và game kiếm hiệp; không dùng chữ tiếng Anh, từ mượn, dịch máy hay từ suồng sã.
5. Không trùng tên map, tên race hoặc tên species khác; Tứ linh và các tên Hán-Việt đã tốt được giữ nguyên.

## Bảng đổi tên

133 tên đổi, 27 tên giữ nguyên.

| ID | Race | Sao | Tên cũ | Tên mới | Nghĩa / ghi chú |
|---|---|---|---|---|---|
| `species_0001` | Bất Tử | 1★ | Nhện Vong Linh | **Âm Chu** | Nhện âm giới (chu = nhện) |
| `species_0002` | Bất Tử | 1★ | Chiến Sĩ Đầu Lâu | **Cốt Binh** | Lính xương |
| `species_0003` | Bất Tử | 1★ | Cua Hắc Ám | **Hắc Giải** | Cua đen (giải = cua) |
| `species_0004` | Bất Tử | 1★ | Xác Ướp | **Triền Thi** | Xác quấn vải, xác ướp |
| `species_0005` | Bất Tử | 1★ | Xác Chết Ác Ma | **Cự Thi** | Xác khổng lồ; khớp vai tường chậm, lì |
| `species_0006` | Bất Tử | 1★ | U Linh | **Tử Hồn** | Hồn ma tím; tránh trùng "U Linh Cổ Thành" |
| `species_0007` | Bất Tử | 1★ | Chó Ác Ma | **Thi Lang** | Sói xác sống; tách khỏi Ngục Khuyển (0058) |
| `species_0008` | Bất Tử | 2★ | Lửa Yêu | **Quỷ Hỏa** | Lửa ma, ma trơi |
| `species_0009` | Bất Tử | 2★ | Xác Chết Vuốt Sắc | **Lợi Trảo Thi** | Xác vuốt sắc |
| `species_0010` | Bất Tử | 2★ | Cá Xương | **Cốt Ngư** | Cá xương |
| `species_0011` | Bất Tử | 2★ | Kẻ Đồ Tể | **Đồ Phu** | Đồ tể |
| `species_0012` | Bất Tử | 3★ | Xác Chết Nửa Người | **Tàn Thi** | Xác tàn, nửa người |
| `species_0013` | Bất Tử | 3★ | (giữ) | **Ma Ảnh** | Bóng ma |
| `species_0014` | Bất Tử | 3★ | Tinh Tinh Xanh Ma Giới | **Phệ Hồn Thảo** | Cỏ nuốt hồn; hình là cây bẫy ruồi, không phải tinh tinh |
| `species_0015` | Bất Tử | 4★ | (giữ) | **Tử Thần** |  |
| `species_0016` | Bất Tử | 4★ | Pharaon | **Sa Thi Vương** | Vua xác cát; bỏ từ mượn "Pharaon" |
| `species_0017` | Bất Tử | 5★ | Rồng Xương Băng | **Băng Cốt Long** | Rồng xương băng |
| `species_0018` | Bất Tử | 5★ | Nữ Vương Bạch Cốt | **Bạch Cốt Nữ Vương** | Đảo về trật tự Hán-Việt |
| `species_0019` | Bất Tử | 5★ · thần thú | Nữ Đế Minh Giới | **Minh Giới Nữ Đế** | Đảo về trật tự Hán-Việt |
| `species_0020` | Bất Tử | 5★ · thần thú | Thủ Lĩnh Hắc Ám | **Hắc Kỵ Vương** | Vua kỵ sĩ đen; hình là kỵ sĩ cưỡi ngựa |
| `species_0021` | Thực Vật | 1★ | Xương Rồng | **Tiên Chưởng** | Xương rồng (từ 仙人掌) |
| `species_0022` | Thực Vật | 1★ | Yêu Tinh Hoa | **Hoa Tinh** | Tinh linh hoa |
| `species_0023` | Thực Vật | 1★ | Nấm Hoa | **Xích Linh Chi** | Nấm linh chi đỏ; hình là nấm, không có hoa |
| `species_0024` | Thực Vật | 1★ | Tinh Tinh Xanh | **Bích Hồ Thảo** | Cỏ bình ngọc, cây nắp ấm; không phải tinh tinh |
| `species_0025` | Thực Vật | 1★ | (giữ) | **Hải Quỳ** |  |
| `species_0026` | Thực Vật | 1★ | Gỗ Quỷ | **Quỷ Mộc** | Cây quỷ |
| `species_0027` | Thực Vật | 1★ | Quả Mặt Quỷ | **Quỷ Diện Quả** | Quả mặt quỷ |
| `species_0028` | Thực Vật | 2★ | (giữ) | **Thủy Linh** |  |
| `species_0029` | Thực Vật | 2★ | Trúc Địa Linh | **Trúc Linh** | Linh hồn trúc |
| `species_0030` | Thực Vật | 2★ | Hoa Ăn Thịt Người | **Thực Nhân Hoa** | Hoa ăn thịt người |
| `species_0031` | Thực Vật | 2★ | Yêu Tinh Dứa | **Kim Thứ Quả** | Quả gai vàng (dứa) |
| `species_0032` | Thực Vật | 3★ | Hoa Môi | **Chu Thần Hoa** | Hoa môi son (chu thần = môi đỏ) |
| `species_0033` | Thực Vật | 3★ | Hoa Hướng Dương | **Thái Dương Hoa** | Hoa mặt trời |
| `species_0034` | Thực Vật | 3★ | Bí Đỏ Quỷ Quái | **Quỷ Nam Qua** | Bí ngô quỷ (nam qua = bí đỏ) |
| `species_0035` | Thực Vật | 4★ | Trưởng Lão Người Cây | **Mộc Trưởng Lão** | Trưởng lão cây |
| `species_0036` | Thực Vật | 4★ | Hoa ăn Thịt Người Ba Đầu | **Tam Thủ Thực Hoa** | Hoa ăn thịt ba đầu |
| `species_0037` | Thực Vật | 5★ | (giữ) | **Độc Đằng Nữ** | Nàng dây leo độc |
| `species_0038` | Thực Vật | 5★ | Tinh Linh Bách Hoa | **Bách Hoa Tiên Tử** | Tiên tử trăm hoa |
| `species_0039` | Rồng | 1★ | Rồng Có Cánh | **Dực Long** | Rồng cánh |
| `species_0040` | Rồng | 1★ | Rồng Mào Đỏ | **Xích Quan Long** | Rồng mào đỏ |
| `species_0041` | Rồng | 1★ | Rắn Xương Trắng | **Cốt Xà** | Rắn xương |
| `species_0042` | Rồng | 1★ | (giữ) | **Tiểu Ma Long** |  |
| `species_0043` | Rồng | 2★ | Rồng Cổ Dài | **Thứ Bối Long** | Rồng lưng gai; hình không có cổ dài |
| `species_0044` | Rồng | 2★ | Rồng Vuốt Xương | **Cốt Trảo Long** | Rồng vuốt xương |
| `species_0045` | Rồng | 2★ | (giữ) | **Nham Long** |  |
| `species_0046` | Rồng | 2★ | Giáp Long Răng Nhọn | **Tiêm Nha Long** | Rồng răng nhọn; tránh lẫn Thiết Giáp Long (0154) |
| `species_0047` | Rồng | 3★ | (giữ) | **Viêm Long** |  |
| `species_0048` | Rồng | 3★ | Rồng Sấm | **Lôi Long** | Rồng sấm |
| `species_0049` | Rồng | 3★ | Rồng Phỉ Thúy | **Phỉ Thúy Long** | Rồng ngọc phỉ thúy |
| `species_0050` | Rồng | 4★ | Hải Long Ba Đầu | **Tam Thủ Hải Long** | Rồng biển ba đầu |
| `species_0051` | Rồng | 4★ | Long Vương Hắc Ám | **Hắc Long Vương** | Vua rồng đen |
| `species_0052` | Rồng | 5★ | Thánh Rồng Thái Cổ | **Thái Cổ Thánh Long** | Rồng thánh thời thái cổ |
| `species_0053` | Ác Ma | 1★ | (giữ) | **Tiểu Ác Ma** |  |
| `species_0054` | Ác Ma | 1★ | Yêu Tinh Biển | **Hải Yêu** | Yêu tinh biển |
| `species_0055` | Ác Ma | 1★ | Mắt Ác Ma | **Tiểu Ma Nhãn** | Mắt quỷ nhỏ; cùng họ với Ma Nhãn Hư Không (0157) |
| `species_0056` | Ác Ma | 1★ | Ma Móng Rồng | **Long Trảo Quỷ** | Quỷ móng rồng |
| `species_0057` | Ác Ma | 1★ | Báo Địa Ngục | **Dạ Xoa** | Quỷ cầm đinh ba; hình không phải con báo |
| `species_0058` | Ác Ma | 1★ | Chó Săn Ác Ma | **Ngục Khuyển** | Chó săn địa ngục |
| `species_0059` | Ác Ma | 2★ | Tướng Chiến Ma Rồng | **Ma Giáp Binh** | Chiến binh giáp quỷ |
| `species_0060` | Ác Ma | 2★ | Ma Thú Địa Ngục | **Ngục Thú** | Thú địa ngục |
| `species_0061` | Ác Ma | 2★ | Lợn Ác Ma | **Ma Trư** | Lợn quỷ |
| `species_0062` | Ác Ma | 2★ | Quái Vật Đầu Dê | **Dương Đầu Ma** | Quỷ đầu dê |
| `species_0063` | Ác Ma | 3★ | Ma Tướng Địa Ngục | **Ma Tướng** | Tướng quỷ |
| `species_0064` | Ác Ma | 3★ | Ma Muội | **Ma Cơ** | Nữ quỷ múa, quyến rũ |
| `species_0065` | Ác Ma | 3★ | Thầy Bói Ác Ma | **Chiêm Tinh Quỷ** | Quỷ bói sao |
| `species_0066` | Ác Ma | 4★ | (giữ) | **Đại Ác Ma** |  |
| `species_0067` | Ác Ma | 4★ | Ma Vương Địa Ngục | **Địa Ngục Ma Vương** | Đảo về trật tự Hán-Việt |
| `species_0068` | Ác Ma | 4★ · thần thú | (giữ) | **Thanh Long** | Tứ linh |
| `species_0069` | Ác Ma | 5★ | Trụy Thiên Sứ | **Đọa Thiên Sứ** | Thiên sứ sa ngã (thuật ngữ quen hơn "Trụy") |
| `species_0070` | Dã Thú | 1★ | Thú Móng Lớn | **Kim Chủy Thú** | Thú mỏ vàng; hình nổi bật cái mỏ, không phải móng |
| `species_0071` | Dã Thú | 1★ | Ưng Đỏ | **Xích Ưng** | Ưng đỏ |
| `species_0072` | Dã Thú | 1★ | Ma Cây | **Lâm Yêu** | Yêu cây rừng; tránh lẫn Quỷ Mộc (0026) |
| `species_0073` | Dã Thú | 1★ | Rùa Phú Quý | **Phú Quý Quy** | Rùa phú quý |
| `species_0074` | Dã Thú | 1★ | Sói Ngớ Ngẩn | **Lam Lang** | Sói xanh lam; bỏ "Ngớ Ngẩn" |
| `species_0075` | Dã Thú | 1★ | Tê Tê Vàng | **Xuyên Sơn Giáp** | Con tê tê |
| `species_0076` | Dã Thú | 1★ | Thú Răng Kiếm | **Kiếm Xỉ Hổ** | Hổ răng kiếm |
| `species_0077` | Dã Thú | 2★ | Thiên Nga Cực Địa | **Cực Băng Nga** | Chim cánh cụt vùng cực; hình không phải thiên nga |
| `species_0078` | Dã Thú | 2★ | Dương Dương Dương | **Miên Dương** | Con cừu; bỏ "Dương Dương Dương" |
| `species_0079` | Dã Thú | 2★ | Mực Hắc Ám | **Mặc Ngư** | Con mực (cá mực) |
| `species_0080` | Dã Thú | 2★ | Gấu Vết Dao | **Đao Ba Hùng** | Gấu sẹo dao |
| `species_0081` | Dã Thú | 3★ | Rùa Nham Thạch | **Nham Quy** | Rùa đá nham thạch |
| `species_0082` | Dã Thú | 3★ | Voi Tai To | **Cự Nhĩ Tượng** | Voi tai to |
| `species_0083` | Dã Thú | 3★ | Cáo Chín Đuôi | **Cửu Vĩ Hồ** | Cáo chín đuôi |
| `species_0084` | Dã Thú | 4★ | Tinh Tinh Rock | **Thạch Viên** | Vượn đá; bỏ chữ tiếng Anh "Rock" |
| `species_0085` | Dã Thú | 4★ | Đại Tuyết Quái | **Tuyết Mao Quái** | Quái tuyết lông trắng (mao = lông) |
| `species_0086` | Dã Thú | 4★ | Gấu Trúc Ma Pháp | **Ma Pháp Hùng Miêu** | Gấu trúc phép thuật (hùng miêu = gấu trúc) |
| `species_0087` | Dã Thú | 4★ · thần thú | (giữ) | **Bạch Hổ** | Tứ linh |
| `species_0088` | Dã Thú | 5★ | Sói Xích Viêm | **Xích Viêm Lang** | Sói lửa đỏ |
| `species_0089` | Chim | 1★ | Chim Ong | **Phong Điểu** | Chim ruồi (蜂鳥); "Chim Ong" là dịch máy |
| `species_0090` | Chim | 1★ | Dơi | **Biên Bức** | Con dơi |
| `species_0091` | Chim | 1★ | Chim Chào Mào | **Hoa Quan Điểu** | Chim mào hoa |
| `species_0092` | Chim | 1★ | Chim Sấm | **Lôi Điểu** | Chim sấm |
| `species_0093` | Chim | 1★ | Ưng Trọc Ma | **Ma Ưng** | Ưng quỷ |
| `species_0094` | Chim | 1★ | Chim Cú | **Dạ Kiêu** | Cú đêm |
| `species_0095` | Chim | 1★ | Ưng Trọc | **Thiết Ưng** | Ưng sắt; tránh lẫn Ma Ưng |
| `species_0096` | Chim | 2★ | Nữ Yêu Minh Ưng | **Ưng Yêu** | Yêu nữ mình ưng |
| `species_0097` | Chim | 2★ | Dơi Một Mắt | **Độc Nhãn Bức** | Dơi một mắt |
| `species_0098` | Chim | 2★ | Quạ Nghĩa Trang | **Mộ Nha** | Quạ nghĩa địa |
| `species_0099` | Chim | 2★ | (giữ) | **Tê Điểu** | Chim mỏ sừng |
| `species_0100` | Chim | 3★ | Vẹt Độc Vuốt | **Độc Trảo Anh Vũ** | Vẹt vuốt độc |
| `species_0101` | Chim | 3★ | Đại Bàng Sư Tử | **Sư Thứu** | Đại bàng đầu sư tử (griffin) |
| `species_0102` | Chim | 3★ | Ưng Hồng Vũ | **Hồng Vũ Ưng** | Đảo về trật tự Hán-Việt |
| `species_0103` | Chim | 4★ | Chim Đại Phì | **Đại Phúc Điểu** | Chim tròn phúc hậu; bỏ "Đại Phì" |
| `species_0104` | Chim | 4★ | Chim Đa Đa | **Liệt Phong Ưng** | Ưng gió dữ; hình không phải chim đa đa |
| `species_0105` | Chim | 4★ · thần thú | (giữ) | **Chu Tước** | Tứ linh |
| `species_0106` | Chim | 5★ | Chim Cú Địa Ngục | **Địa Ngục Quái Điểu** | Quái điểu địa ngục; hình không phải cú |
| `species_0107` | Chim | 5★ | Đại Bàng Vàng | **Kim Sí Đại Bằng** | Đại bàng cánh vàng |
| `species_0108` | Sâu | 1★ | Ong Giết Người | **Độc Phong** | Ong độc |
| `species_0109` | Sâu | 1★ | Bọ Cạp Sa Mạc | **Sa Hạt** | Bọ cạp cát (hạt = bọ cạp) |
| `species_0110` | Sâu | 1★ | Bọ Ngựa Móng Sắt | **Thiết Đường Lang** | Bọ ngựa sắt |
| `species_0111` | Sâu | 1★ | Ốc Sên Hoa | **Hoa Loa** | Ốc hoa (loa = ốc) |
| `species_0112` | Sâu | 1★ | Nhện Độc | **Sơn Chu** | Nhện núi |
| `species_0113` | Sâu | 1★ | (giữ) | **Thiên Ngưu** | Bọ xén tóc |
| `species_0114` | Sâu | 1★ | Bọ Cánh Cứng Răng Kiếm | **Kiếm Giáp Trùng** | Bọ cánh cứng hàm kiếm |
| `species_0115` | Sâu | 2★ | Giun Đất Móng Sắt | **Thứ Sa Trùng** | Sâu gai trong cát |
| `species_0116` | Sâu | 2★ | Châu Chấu Móng Lớn | **Cự Trảo Trùng** | Châu chấu càng lớn |
| `species_0117` | Sâu | 2★ | Thú Một Sừng Vỏ Cứng | **Độc Giác Trùng** | Bọ một sừng; tránh lẫn kỳ lân (0149) |
| `species_0118` | Sâu | 2★ | Bướm Hoa Vũ | **Hoa Vũ Điệp** | Bướm cánh hoa (điệp = bướm) |
| `species_0119` | Sâu | 3★ | Cua Ký Sinh | **Ký Cư Giải** | Ốc mượn hồn (寄居蟹); không phải cua ký sinh |
| `species_0120` | Sâu | 3★ | Tôm Hùm Răng Cưa | **Cự Ngao Hà** | Tôm càng lớn |
| `species_0121` | Sâu | 3★ | Hải Mã Bong Bóng | **Thủy Bào Hải Mã** | Cá ngựa bong bóng |
| `species_0122` | Sâu | 4★ | Trùng Hốt Lỗ | **Ách Vận Trùng** | Sâu xui rủi; khớp skill gây vận rủi |
| `species_0123` | Sâu | 4★ | Trùng Gai Nhọn | **Thạch Thứ Trùng** | Sâu gai hóa đá |
| `species_0124` | Sâu | 5★ | Trùng Bất Tử Địa Huyệt | **Địa Huyệt Ma Trùng** | Ma trùng hang đất; bỏ "Bất Tử" vì trùng tên race |
| `species_0125` | Sâu | 5★ | Nhện Phu Nhân | **Điệp Hậu** | Nữ hoàng bướm; hình là tiên cánh bướm, không có nhện |
| `species_0126` | Sâu | 5★ · thần thú | Trùng Mẫu Mào Vàng | **Kim Quan Chu Hậu** | Nữ hoàng nhện đội mũ vàng; hình là nữ hoàng cưỡi nhện |
| `species_0127` | Linh Thể | 1★ | Quái Vật Rương Báu | **Bảo Tương Yêu** | Yêu hòm báu (tương = hòm, rương) |
| `species_0128` | Linh Thể | 1★ | Chong Chóng Gió | **Phong Xa Linh** | Linh chong chóng (phong xa = chong chóng gió) |
| `species_0129` | Linh Thể | 1★ | Quái Vật Nham Thạch | **Nham Quái** | Quái đá |
| `species_0130` | Linh Thể | 1★ | Đá Mặt Quỷ | **Quỷ Diện Thạch** | Đá mặt quỷ |
| `species_0131` | Linh Thể | 1★ | Hư Không Hắc Ám | **Hư Ảnh** | Bóng hư không |
| `species_0132` | Linh Thể | 2★ | Sách Ma Pháp | **Ma Đạo Thư** | Sách ma đạo |
| `species_0133` | Linh Thể | 2★ | (giữ) | **Ma Kiếm** |  |
| `species_0134` | Linh Thể | 3★ | Con Rối Gạch Đá | **Thạch Khôi Lỗi** | Con rối đá |
| `species_0135` | Linh Thể | 3★ | Thằng Hề Hộp | **Tiểu Sửu Hạp** | Chú hề trong hộp (tiểu sửu = chú hề) |
| `species_0136` | Linh Thể | 3★ | Chiến Sĩ Bù Nhìn | **Thảo Nhân Binh** | Lính bù nhìn (thảo nhân = bù nhìn) |
| `species_0137` | Linh Thể | 4★ | Ma Gương Thủy Tinh | **Thủy Tinh Ma Kính** | Gương ma thủy tinh |
| `species_0138` | Linh Thể | 4★ | Thú Lớn Dung Nham | **Dung Nham Cự Nhân** | Người khổng lồ dung nham |
| `species_0139` | Linh Thể | 4★ · thần thú | (giữ) | **Huyền Vũ** | Tứ linh |
| `species_0140` | Linh Thể | 5★ | (giữ) | **Nhân Sư** |  |
| `species_0141` | Linh Thể | 5★ | Totem Thượng Cổ | **Thượng Cổ Đồ Đằng** | Vật tổ thượng cổ (đồ đằng = totem) |
| `species_0142` | Linh Thể | 5★ · thần thú | (giữ) | **Thần Tướng Cự Ma** |  |
| `species_0143` | Linh Thể | 5★ · thần thú | Thần Đèn | **Đăng Thần** | Thần đèn |
| `species_0144` | Thực Vật | 5★ · thần thú | (giữ) | **Linh Tiên Hoa Hương** | Đã duyệt (Triệu Linh Điện) |
| `species_0145` | Thực Vật | 5★ · thần thú | Cây Cự Linh | **Cự Linh Mộc** | Cây khổng lồ có linh hồn |
| `species_0146` | Ác Ma | 5★ · thần thú | Ma Vương Hút Máu | **Huyết Ma Vương** | Ma vương khát máu; tách khỏi Địa Ngục Ma Vương |
| `species_0147` | Dã Thú | 5★ | Người Tuyết Viễn Cổ | **Viễn Cổ Tuyết Nhân** | Người tuyết viễn cổ |
| `species_0148` | Dã Thú | 5★ · thần thú | Ngựa Bùn Cỏ | **Vân Mao Đà** | Lạc đà lông mây (alpaca); bỏ "Ngựa Bùn Cỏ" vì là chơi chữ tục 草泥马 |
| `species_0149` | Dã Thú | 5★ · thần thú | Thú Vàng Một Sừng | **Kim Kỳ Lân** | Kỳ lân vàng; đổi từ tên thuần Việt đã duyệt ở Triệu Linh Điện |
| `species_0150` | Chim | 5★ · thần thú | Đảo Thiên Đường | **Thiên Đường Điểu** | Chim thiên đường; "Đảo" là dịch sai |
| `species_0151` | Sâu | 5★ · thần thú | Đại Vương Bọ Cạp | **Độc Hạt Vương** | Vua bọ cạp độc; đổi từ tên thuần Việt đã duyệt ở Triệu Linh Điện |
| `species_0152` | Chim | 5★ · thần thú | Chim Ái Thần | **Ái Thần Điểu** | Chim thần tình yêu |
| `species_0153` | Dã Thú | 5★ | Hươu Rêu Nguyệt | **Nguyệt Đài Lộc** | Hươu rêu trăng (đài = rêu, lộc = hươu) |
| `species_0154` | Rồng | 5★ | (giữ) | **Thiết Giáp Long** |  |
| `species_0155` | Rồng | 5★ | (giữ) | **Tinh Vân Long** |  |
| `species_0156` | Ác Ma | 5★ | (giữ) | **Đao Ma Huyết Giáp** |  |
| `species_0157` | Ác Ma | 5★ | (giữ) | **Ma Nhãn Hư Không** |  |
| `species_0158` | Linh Thể | 5★ | (giữ) | **Hộ Vệ Thạch Linh** |  |
| `species_0159` | Rồng | 5★ · thần thú | (giữ) | **Long Thần Song Ấn** |  |
| `species_0160` | Ác Ma | 5★ · thần thú | (giữ) | **Ma Chủ Song Cực** |  |

## Phạm vi áp dụng

- Đã đổi: `data/p10/species.json`, `data/p10/species_authored.json`, `data/p10/species_effective.json`, catalog P11 (152 và 160), candidate P13 160, `apps/game-web/public/assets/i18n/vi.json`, và các tài liệu P10-P13 đang dùng.
- Giữ nguyên làm bản ghi lịch sử: dữ liệu nguồn APK, asset và prompt vẽ lại trong `apps/game-client/assets/pets`, các package review P13 đã được owner duyệt cùng response theo hash (`review-package.json`, `roster-review-package.json`, `review/`, `evidence/`), và các snapshot evidence khác. Những file này vẫn mang tên cũ vì hash của chúng gắn với phản hồi duyệt.
- Các hash pin đã được cập nhật tường minh: `baseline_catalog_sha256` trong `roster-amendment-160.json`, `source_species_sha256` trong các catalog, `candidate_sha256` trong mapping P13→P10, và `species.json` trong `preservation-before.json`.

## Kiểm chứng

```sh
python3 .ai/plan/phases/P11-stats/evidence/build_species_catalog.py --check
python3 .ai/plan/phases/P11-stats/evidence/build_effective_catalog.py --check
python3 tools/content/p10_extension.py
python3 tools/build-web-assets/build_i18n.py   # sinh lại vi.json
(cd tools/content && python3 -B -m unittest -q test_p13_design test_p13_roster_review test_p10_catalog test_p10_extension test_p10_provenance)
```

## Đổi tên lần sau

1. Sửa `display_name.vi` trong `data/p10/species.json` (và `species_authored.json` nếu là loài mới).
2. Chạy lại `build_species_catalog.py --write`, cập nhật `baseline_catalog_sha256` trong `evidence/roster-amendment-160.json`, rồi `build_effective_catalog.py --write`.
3. Cập nhật hash của `species.json` trong `extension-20261013/preservation-before.json`, rồi chạy `p10_extension.py --write` và `build_i18n.py`.
4. Cập nhật bảng trong tài liệu này và chạy các lệnh ở mục Kiểm chứng.
