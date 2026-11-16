# Bản vẽ lại S07 và S04

- [city-backdrop-wide.png](city-backdrop-wide.png): 2432×486, bầu trời trong suốt, thành và mây tông ấm. [Prompt](city-backdrop-wide.prompt.txt) · [QA](city-backdrop-wide.qa.json). Ảnh nguồn được co giãn khác tỷ lệ ngang/dọc để khớp canvas; cần xem lại tỷ lệ kiến trúc.
- [fg-city-bunting.png](fg-city-bunting.png): 1024×160, dây cờ liên tục. [Prompt](fg-city-bunting.prompt.txt) · [QA](fg-city-bunting.qa.json) · [Xem lặp ba lần](fg-city-bunting-repeat-3x.png).

Đây là hai PNG riêng, không ghi đè bản cũ trong `delivery/` hoặc ảnh E19/E20. Claude đã duyệt cả hai ở mục E và ghi nhận cài đặt ở mục F của review ngày 2026-10-30. Ảnh nguồn và thông tin route nằm ở `../../raw/cli-city-transparent-v2/` và `../../raw/cli-city-bunting-v2/`.

## Visual review status

Claude duyệt bằng mắt: thành phố có trời trong suốt, tông ấm; tỷ lệ kiến trúc hơi cao/hẹp nhưng được chấp nhận cho nền xa. Dây cờ lặp liền mạch, không thấy vết nối. QA cơ học xác nhận alpha nhị phân, không có pixel bán trong suốt; dây cờ không có pixel đục giống magenta. Hai file đã được cài theo mục F trong review. QA vẫn lưu cảnh báo ảnh thành phố đã co giãn không đều; Claude chấp nhận giới hạn này cho vai trò nền xa.
