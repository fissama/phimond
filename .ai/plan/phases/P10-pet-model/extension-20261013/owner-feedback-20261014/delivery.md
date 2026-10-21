# Bản sửa theo nhận xét — 14/10/2026

Đã tạo sáu atlas mới để duyệt lại. Thiết Giáp Long và Đao Ma Huyết Giáp giữ nguyên đúng byte của hai bản bạn đã duyệt. Đây là bàn giao bản vẽ để xem thử, chưa chọn art hoặc kích hoạt trong game.

Xem tại [trang review](http://127.0.0.1:8125/), chọn **Lọc nguồn thiết kế → 8 loài Phimond-authored mới**. Chọn **Bản sửa mới · chờ duyệt** để chỉ xem sáu bản sửa. Thử Move, Đánh thường, Cast skill và Die ở 64/96/192 px; chỉ Idle/Move lặp, các hàng còn lại giữ frame cuối.

| Loài | Bản mới | Thay đổi |
|---|---|---|
| Hươu Rêu Nguyệt | attempt-09 | Gạc trăng lưỡi liềm, dáng thanh lịch, bước chân thay đổi và đòn thường dùng gạc. Thu gọn phép để tránh mảnh hiệu ứng từ ô bên cạnh. |
| Tinh Vân Long | attempt-10 | Giữ xanh đêm và sao vàng; mặt trưởng thành hơn, chân và đuôi phối hợp. Dựng lại bố trí để giữ trọn đuôi, đổi luồng dài thành ba tia gọn. |
| Ma Nhãn Hư Không | attempt-09 | Thân tối cùng xúc tu, giữ một mắt và ba rune trên đầu; thay hiệu ứng giống mắt phụ bằng vệt quất và xung góc cạnh. |
| Hộ Vệ Thạch Linh | attempt-08 | Đá chạm khắc, vai/nắm đấm góc cạnh, điểm vàng và ngọc; đấm ngang và đập đất riêng biệt. |
| Long Thần Song Ấn | attempt-12 | Vàng kim chủ đạo, dáng cao và đuôi cuộn gọn; hai hoa văn ấn xanh trên giáp. Vuốt Quang rồi sáng hai ấn. |
| Ma Chủ Song Cực | attempt-11 | Nam shonen trưởng thành khoảng 20 tuổi, khuôn mặt trẻ và tóc bạc ánh tím; giữ cơ bắp, thương, giáp chân và phép tím. Bỏ hạt hiệu ứng rời ở frame hồi đòn thường. |

## Kiểm chứng

- Sáu atlas: PNG RGBA 1124×1405; 4×5 ô 281 px; 20 frame khác nhau; mọi alpha nằm trong cell-local [22,259).
- Hướng cơ sở bên trái. Bản raw, prompt, hash đầu vào, 20 source rectangles, scale chung và preview giữ trong thư mục từng attempt. Packing nearest-neighbor không xóa alpha để đạt kiểm tra.
- Roster authoring vẫn 160; giữ 152 stable IDs và bộ art đã khóa. Tám loài mới vẫn có provenance Phimond-authored.
- Hai atlas được duyệt giữ nguyên hash. Sáu hash mới cần duyệt lại; nhận xét cũ được giữ trong input-snapshot.json và owner-reviews.json.
- Kết quả chi tiết: mechanical-evidence.json và independent-review.json/md. Kiểm tra hình học không tự chứng minh anatomy, độ mượt hay chất lượng pixel.

## Điểm cần xem khi duyệt

- Hai ấn Long Thần vẫn là các chi tiết tròn lớn trên giáp: cần bạn đánh giá độ ăn khớp và cảm giác sang trọng.
- Số đầu xúc tu của Ma Nhãn có thể bị che trong một số pose; không khẳng định đếm rõ sáu đầu ở mọi frame.
- Ma Chủ: tuổi khuôn mặt và màu tóc bạc ánh tím cần bạn duyệt. Chi tiết nhỏ và hiệu ứng sáng có thể khó đọc ở 64 px.
- Độ mượt vòng đi bộ, độ sắc nét pixel và mức hiệu ứng còn là điều kiện duyệt hình ảnh, không được coi là đã đạt chỉ nhờ mechanical PASS.

Các bản thử bị cắt thân/đuôi đã được thay bằng bản mới; giữ lịch sử trong các thư mục attempt và independent-review history. Không thay sprite runtime, gameplay, server, DB hoặc bản chọn của 152 loài.

## Vị trí assets và prompts

Assets: `apps/game-client/assets/pets/redraws/extension-20261013/species_0153…species_0160/`. Bản hiện tại và SHA nằm trong `../art-manifest.json` và `result.json` từng loài.

Prompt gốc và prompt sửa nằm trong thư mục này; mỗi attempt giữ bản `prompt.txt` đã dùng. Tạo/sửa bằng công cụ ImageGen tích hợp, sau đó dùng quy trình packing đã được chủ dự án cho phép.
