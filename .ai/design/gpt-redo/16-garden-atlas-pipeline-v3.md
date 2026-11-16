# Đơn 16 — Pipeline atlas garden-b v3 (đóng gói có căn pivot) và tiêu chí sửa

Ngày: 2026-11-09. Áp dụng cho Đơn 14 (chậu) và Đơn 15 v2 (Linh Thảo). Thay các mục đo bị đánh dấu "SỬA" dưới đây; các mục khác giữ nguyên.

## Vì sao đổi (kết quả pilot 8/8 lượt, Claude review)
- Sheet gốc của image_gen là 1122×1402 và KHÔNG nằm đúng lưới 4×5. Cắt lưới cố định rồi thu về 768×960 làm mọi khung trôi ngang ~6 px mỗi cột (tâm gốc Bạc Hà 104.9, 98.0, 92.2, 86.1 lặp ở mọi hàng), lẫn pixel từ ô bên cạnh (các "vi phạm vùng an toàn" ở y=0 và y=191), và kích thước không ổn định. Đó là lỗi cắt, không phải lỗi vẽ.
- Tiêu chí "pixel thân giữ nguyên ở cùng tọa độ ở mọi khung" (invariant body = 0 màu) là bất khả với ảnh sinh độc lập từng khung. Pet (P10) cũng không đòi điều này. Thay bằng độ chồng mask sau căn thẳng.
- Tranh: hướng Linh Thảo có mặt đã ĐÚNG (Bạc Hà mèo bạc hà, Mộc Nhĩ thỏ tai nấm: biểu cảm rõ, dễ thương). Giữ nguyên thiết kế đã vẽ ở raw-09 của hai cây pilot.

## Đóng gói (theo tiền lệ P10: nearest-neighbor, pivot cục bộ, một tỉ lệ chung)
Viết `garden-b/tools/pack_atlas.py` (không sinh hình, không vá, không blend) làm các bước:
1. Với mỗi trong 20 ô danh nghĩa (lưới 4×5 của sheet 1122×1402, mở rộng mỗi ô ±12% để không cắt cụt), khử nền #FF00FF, lấy thành phần liên thông lớn nhất làm THÂN, cộng các mảnh hiệu ứng nằm trong vùng ô đó. Không lấy mảnh thuộc ô khác (loại theo tâm khối gần nhất).
2. Pivot mỗi khung: cây = (tâm x của 6 hàng pixel thấp nhất của thân, y thấp nhất của thân); chậu = (tâm x, y đáy thân chậu).
3. MỘT tỉ lệ nguyên/chia đều s cho cả atlas (nearest-neighbor), chọn lớn nhất sao cho mọi khung vừa vùng an toàn [16,175] và ripe ≤ 150 px (cây); tối thiểu s ≥ 0.6, nhỏ hơn thì phải vẽ lại.
4. Đặt từng khung tại pivot cố định của ô: cây (96,168), chậu đáy y=175 và tâm x=96, chỉ dịch nguyên pixel, không xoay/biến dạng. KHÔNG cắt xén (clip) để qua cổng; nếu hiệu ứng tràn vùng an toàn: giảm s hoặc vẽ lại.
5. Ghi vào qa.json: 20 hình chữ nhật nguồn, pivot, tỉ lệ s, offset đặt.
Các bước này là ghép/căn chuẩn (được phép như P10), KHÔNG phải vẽ.

## Tiêu chí đo (sửa; giữ a, b, c, h-bản-sửa, i)
- a, b: giữ. c: giữ nguyên nghiêm (mọi pixel alpha>0 trong x,y ∈ [16,175]; không sót pixel).
- d SỬA: tổng màu ≤ 60 (thân 33–48 + hiệu ứng ≤ 12 nếu tách được; bỏ phép đo "invariant body colors").
- e SỬA: sau đóng gói pivot đúng (96,168)/(96,175) ±1 ở mọi khung; mặt (mắt, miệng) báo trong review.md.
- f SỬA (chiều cao cây, từ đỉnh thân đến y=168): sprout 45–75 px, grow 85–112 px, ripe 120–150 px; rộng ≤ 140 px. (Nới sprout và grow để mặt còn đọc được.)
- g SỬA (chậu): mask thân chậu giữa hai khung liền kề sau căn thẳng IoU ≥ 0.95; khung nối (water f4 ≈ wet f1; upgrade f4 và clear f4 ≈ idle f1) IoU ≥ 0.93 và nhìn không giật; đất trong miệng ở hàng wet SẪM hơn idle: độ sáng trung bình vùng miệng chậu (hình ellipse miệng) thấp hơn ≥ 15% và có bóng nước.
- h SỬA: plant f4 so với sprout f1 mask IoU ≥ 0.80 (không đòi pixel).
- i: giữ (mỗi hàng lặp có ít nhất một khung chớp mắt, ghi trong review.md).
- j MỚI (thân ổn định): trong cùng hàng lặp, mask thân giữa hai khung liền kề (căn pivot) IoU ≥ 0.85.
Cập nhật `tools/measure_atlas.py` theo đúng các mục trên (đây là sửa tiêu chí có chủ đích của Claude, ghi trong file này; không sửa gì thêm).

## Điểm riêng
- Chậu G1: màu hiện quá cam bão hòa, đổi về gốm nâu cam ấm như garden-a/gd-decor-06 (không neon).
- Cây: kích thước chiều cao rộng hơn khi đóng gói (sprout/grow) là có chủ đích để mặt đọc được ở 48 px.
