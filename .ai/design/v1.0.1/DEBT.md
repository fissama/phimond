# Nợ (debt) sau v1.0.1

Các mục đánh giá gameplay thuộc Phase sau, giữ lại ở dạng nợ. Mỗi mục: nguồn → việc cần làm → khi nào làm.

| ID | Nguồn | Việc | Khi nào |
|---|---|---|---|
| D1 | G4 | 4 NPC/điểm "chưa mở" (Hội bang, Sàn giao dịch, Kho, Hòm thư) và Đấu trường vẫn là biển báo. Chức năng thật: Phase guild, giao dịch, kho, thư, đấu trường. Tạm thời quyết định ẩn hoặc giữ biển báo. | Phase tương ứng |
| D2 | G4, T1 | Nội dung: mỗi NPC 2–3 câu thoại đổi theo tiến độ; thêm 2–3 nhiệm vụ nối Hoàng Môn và Quảng Trường. | Phase nội dung |
| D3 | T4 | An toàn đụng quái: vùng an toàn quanh NPC và lối chính, báo hiệu quái trước khi vào trận. Phải sửa ở server (ngoài phạm vi client). | Phase cân bằng |
| D4 | review | Hiệu năng và độ trễ trên iPhone 17 Pro Max (Safari), macOS Safari, thang chất lượng thấp/vừa/cao. | Trước khi public |
| D5 | L3 | Người đi đường và động vật chưa có tương tác khi chạm. | Phase sau |
| D6 | G3 | Di chuyển vẫn theo lưới 4 hướng, không đi chéo, tốc độ cố định. Cân nhắc đi chéo và tăng tốc khi giữ. | Phase cân bằng |
| D7 | HUD | Mũi tên nhún trên bệ đá cho người mới (cần API marker trong engine). Hiện thay bằng khung Mục tiêu + nút Chọn nháy. | Sau v1.0.1 |
| D8 | HUD | Cho người chơi tự đặt lại vị trí điều khiển; chat có nội dung thật (kênh Thế giới/Khu vực/Đội/Riêng chờ server). | Phase xã hội |
| D9 | HUD | Khung ảnh riêng cho bản đồ nhỏ, khung mục tiêu, chat (hiện dùng CSS thuần, không có sprite duyệt). Xem `GPT-REMAINING.md` mục UI. | Khi GPT có lượt |
| D10 | N2 | Chỉnh fringe đường đất để hết lộ nhịp ô vuông; có thể cần thêm biến thể từ GPT. | Sau khi duyệt ảnh trong cảnh |
| D11 | starter | 3 loài khởi đầu mới dùng chỉ số mượn từ Hoa Tinh/Sơn Chu/Lam Lang; chưa có chỉ số, kỹ năng P11/P13 riêng. Pet Lv1 đấu quái Bìa Rừng chưa cân bằng. Server vẫn dùng 14 loài cũ cho quái. | P11 |
| D12 | HD-2D | Ánh sáng thật theo đèn (hiện là quầng cộng sáng + chỉnh màu toàn cảnh), bóng đổ theo giờ, thời tiết (mưa, sương), nước phản chiếu. Chưa đo hiệu năng bloom trên iPhone/Safari. | Sau khi đo D4 |
| D13 | Combat | Trận đấu là cảnh DOM trên nền cảnh thế giới làm mờ, chưa phải diorama 3D riêng; chưa có hiệu ứng kỹ năng, chưa có tên Lv cho quái hoang (server không gửi level trong BattleUnit). | Sau v1.0.1 |
| D14 | HUD | EXP cần lên cấp (cấp × 25) đang hard-code ở client theo `data/balance/rules.json`; nên server gửi `xp_next` trong snapshot. | Cùng đợt chỉnh server |
| D15 | Combat | Encounter 3 quái làm pet mới có thể chết trước khi kịp Chạy; thành phần encounter theo party, AoE, mục tiêu đồng đội cho 3v3 chưa có. Xem `COMBAT-HUD-SPEC.md` cờ 1–4. | Phase cân bằng / PvP 3v3 |
| D16 | Âm thanh | Âm thanh hiện tổng hợp bằng WebAudio (đánh, phép, thắng/thua, tiền, nút); chưa có nhạc nền theo map và bộ âm thanh vẽ riêng. | Khi có âm thanh |
| D17 | NPC | Hội thoại dùng sprite NPC thu nhỏ làm chân dung; game gốc/Octopath dùng tranh bán thân. | Khi GPT có lượt (GPT-REMAINING 14) |
| D18 | Cân bằng | Hệ số `wild_scale`/`pack_scale`/`damage_scale` chỉnh bằng mô phỏng auto (`balance_test.go`), chưa thử với người chơi thật và kỹ năng trạng thái. Pet khởi đầu biết sẵn đòn hệ (lệch learn_level 2). | Phase cân bằng |
