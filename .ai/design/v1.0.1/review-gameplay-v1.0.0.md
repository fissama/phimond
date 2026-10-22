# Đánh giá gameplay Phimond v1.0.0 — góc nhìn người chơi khó tính

Phạm vi: vòng chơi Đợt A (chọn linh thú khởi đầu → Bìa Rừng → Rừng Sâu → Hoàng Môn → Quảng Trường → trụ đá).
Căn cứ: chơi thử trong game thật (đăng ký, chọn bệ, đi 5 map, nói chuyện NPC, đụng quái và thoát trận, mở menu), kết hợp đọc mã di chuyển và tương tác.

**Giới hạn của lần chơi này, cần nói thẳng:**
- Môi trường chơi không có GPU nên khung hình thấp (khoảng 12 khung/giây), **không đo được độ mượt thật**. Chưa kiểm trên iPhone, Safari hay mạng yếu.
- Lượt chạy tự động đầy đủ cả 5 map bị gián đoạn giữa chừng (lỗi công cụ ở phía mình). Mục nào ghi "đọc mã" nghĩa là mình suy ra từ code, chưa tận mắt thấy.

## Kết luận ngắn

Khung chơi chạy được và liền mạch về kỹ thuật, nhưng **cảm giác điều khiển và nội dung còn mỏng**: đi như trượt, hầu hết NPC chỉ có một câu thoại cố định, bốn điểm tương tác là biển "chưa mở", chỉ có 4 nhiệm vụ, và người chơi mới không được dẫn dắt. Một người chơi khó tính đi hết Đợt A trong vài phút rồi hết việc.

## Lỗi và vấn đề, theo mức nghiêm trọng

### Nặng

**G1. NPC khởi đầu Mira không nhìn thấy trong sảnh.** Nhãn tên "Triệu Linh Sư Mira" hiện nhưng sprite nằm sau tường nên không thấy; đứng cạnh cũng chỉ thấy nhân vật đè lên cột. Đây là NPC đầu tiên của chuỗi nhiệm vụ chính. *(Quan sát trong ảnh; nguyên nhân khả dĩ là vị trí y=1 trùng vùng tường che.)*

**G2. Không có hướng dẫn cho người mới.** Vào game chỉ thấy sảnh trống, hộp chat ghi "Chưa có tin nhắn". Không mũi tên, không gợi ý "chạm vào bệ đá", không ai gọi tên mục tiêu. Người chơi mới có thể đứng yên lâu.

**G3. Di chuyển cảm giác trượt.** Nhân vật chạy bằng dải khung không có bước chân thật (xem báo cáo đồ họa N1) và không có hướng lên/xuống. Đi theo lưới ô, 4 hướng, tốc độ cố định 4 ô/giây, không đi chéo. Kết hợp lại: nhân vật "lướt" từ ô này sang ô khác. *(Đọc mã + soi khung hình.)*

**G4. Nội dung tương tác quá ít và có ngõ cụt.** 19 NPC/điểm tương tác, mỗi điểm chỉ một câu thoại cố định. Bốn điểm là biển báo chưa làm: Hội bang ("đang được chuẩn bị"), Sàn giao dịch ("chưa mở cửa"), Kho đồ ("đang sắp xếp lại"), Hòm thư ("chưa hoạt động"). Đấu trường chỉ nói "sắp mở". Người chơi đi tới và bị từ chối: cảm giác như demo.

### Trung bình

**T1. Chỉ có 4 nhiệm vụ**: tới Rừng Sâu, bắt linh thú đầu tiên, thắng một trận, phối giống. Không có nhiệm vụ nối với NPC ở Hoàng Môn hay Quảng Trường; các NPC thoại nhưng không giao việc.

**T2. Mở Menu khóa nhân vật mà không báo rõ.** Phím Esc/Backspace đóng lớp đang mở, còn khi không có lớp nào thì mở Menu (đúng thiết kế). Nhưng khi Menu mở, mọi lệnh đi/chạm bị bỏ qua mà không có thông báo, nên người chơi dễ tưởng game đơ. *(Quan sát khi test; mình ban đầu tưởng Esc là lỗi, đọc lại mã thấy hành vi đúng.)*

**T3. Chạm ô không đi được chỉ hiện thông báo nhỏ "Không đi vào đó được".** Người chơi không biết ô nào bị chặn vì ranh giới cây/bụi/đá với đường đi không rõ ràng bằng mắt (xem N2, N3 phần đồ họa). *(Đọc mã.)*

**T4. Đụng quái dễ.** Quái hiện trên đồng, đi lại gần là vào trận. Khi chạy thử xuyên Bìa Rừng, tuyến đường bị cắt bởi trận ít nhất một lần (chưa thống kê tần suất). Chạy trốn luôn dùng được nhưng làm đứt mạch đi. Cần có vùng an toàn quanh NPC và lối đi chính, hoặc báo hiệu quái trước khi vào trận.

**T5. Màn trận đấu đè lên thế giới tối đi.** Thế giới mờ đi phía sau, hộp thoại trận che gần hết D-pad ở dưới trái, khiến giao diện bên dưới nhìn như nửa hoạt động. Thông tin HP và 7 nút hành động rõ nhưng bố cục chưa gọn.

### Nhẹ

**L1. Hộp chat chiếm chỗ lớn nhưng luôn trống** ở lần đầu; các thẻ Tất cả/Hệ thống/Thế giới/Khu vực/Đội/Riêng có nhưng chưa có nội dung để thấy khác biệt.

**L2. Menu** có Linh thú, Túi đồ, Nhiệm vụ, Cài đặt, Đăng xuất; bố cục khung lệch (xem báo cáo đồ họa L2), nút "Đóng" nằm lẻ.

**L3. Người đi đường và động vật (v1.0.1)** thêm sinh khí nhưng không có tương tác: chạm vào không có phản ứng.

## Điểm đạt

- Vào game, đăng ký, chọn bệ, chuyển map đều liền mạch; nhân vật không xuyên vật cản.
- Trận đấu có đủ lựa chọn cơ bản (tấn công, kỹ năng, bắt, phòng thủ, vật phẩm, tự động, chạy).
- Tạm ổn: chuyển map qua cổng và trụ đá, khóa đích chưa mở trong bảng dịch chuyển.

## Việc cần làm (đề xuất, theo thứ tự)

1. Đưa Mira ra khỏi vùng bị tường che và thêm mũi tên/gợi ý đầu tiên cho người mới.
2. Khi Menu hoặc hộp thoại đang mở, hiện rõ trạng thái "đang tạm dừng" thay vì lặng lẽ bỏ qua lệnh đi.
3. Thêm hướng đi lên/xuống và chu kỳ bước chân thật (đồ họa A).
4. Làm hiển thị ô chặn rõ hơn hoặc cho nhân vật đi tới ô gần nhất đi được thay vì chỉ báo lỗi.
5. Quyết định cho 4 điểm "chưa mở": giấu bớt khỏi map v1.0.0 hoặc đổi thành nhiệm vụ/thoại có nội dung.
6. Thêm 2–3 nhiệm vụ nối Hoàng Môn và Quảng Trường; mỗi NPC thêm ít nhất 2–3 câu thoại đổi theo tiến độ.
7. Đo hiệu năng và độ trễ trên iPhone 17 Pro Max (Safari) và macOS Safari khi có thang chất lượng thấp/vừa/cao.
