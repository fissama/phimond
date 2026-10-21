# Rồng Xương Băng — miêu tả và cấu trúc redraw

Nguồn: portrait/sprites APK của RongXuongBang và xác nhận trực tiếp của chủ dự án ngày 2026-10-09. Đây là mô tả mỹ thuật, không bổ sung công thức hoặc hệ chiến đấu.

## Miêu tả

Rồng Xương Băng là một con rồng undead thuộc race Bất Tử, mang hình hài bộ xương rồng bốn chân có cánh. Hộp sọ dài với sừng nhọn, hốc mắt đỏ và hàm răng lộ rõ tạo vẻ hung dữ cổ xưa. Cổ nối liền cột sống dài, lồng ngực và khung chậu; các đốt xương tiếp tục chạy dọc chiếc đuôi cong. Xương màu ngà với bóng nâu sẫm. Hai cánh có khung xương phân nhánh và màng nâu đỏ, gắn chắc với phần vai và có thể đập để nâng toàn thân bay. Bên trong lồng ngực hở là một lõi đỏ phát sáng; lõi nằm trong cơ thể, không do chân trước cầm.

## Bộ phận và hoạt ảnh

- Bốn chân: hai chân trước và hai chân sau có khớp, bàn chân và móng; đứng chịu lực ở Idle. Giữ chiều dài thân đủ để phân biệt hai cặp chân.
- Cánh: hai cánh riêng với gốc cánh, khớp và các ngón xương chống màng. Move là bay với cánh nâng → đập xuống → hồi lên; thân được nâng và bốn chân thu tự nhiên dưới bụng.
- Đầu: mặt nhìn cùng một hướng qua tất cả các trạng thái, giữ hốc mắt đỏ, mõm dài và hàm rõ; không làm mặt tròn hài hước.
- Attack thường: động tác ngoạm bằng hàm, có chuẩn bị, tiếp xúc và thu về; giữ cấu trúc bốn chân và hai cánh.
- Cast: lõi trong lồng ngực sáng lên, giải phóng hiệu ứng đỏ sắc nét rồi tắt dần; hiệu ứng không che mắt và không khiến lõi trông như vật cầm tay.
- Down: khung xương hạ xuống và nằm hoàn toàn; cánh xếp có khớp, giữ đủ bốn chân và đuôi.

Không suy diễn màu xanh hoặc quy tắc Băng từ tên loài. Dùng bảng màu ngà/nâu/đỏ quan sát ở APK. Bản hai chân trước đây không đạt nhận diện và bị loại khỏi tiến độ.
