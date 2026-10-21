Cảm ơn bạn đã đối chiếu trục Y: ghi nhận công thức `px_y = round((ymax - y) * 100)` đúng, giữ nguyên. Quyết định:

## 1. Hoang Mạc — GO dựng layout đầu tiên
Làm `desert_entrance` ngay (một map, nộp rồi chờ kiểm). Dùng prompt `.ai/design/hd2d-map-layout-prompt.md`, brief `map-briefs/desert/desert_entrance.{md,json}`, ảnh gốc `level6_Phiadong.png`. Bắt buộc: layout.json qua `validate_hd2d_map_layout.py` 0 lỗi; 57 neo "CẦN ĐẶT" của map này có px + why; ảnh phác đối chiếu ảnh gốc; ảnh render 3 camera + zoom 2× vùng cổng và NPC mà BẠN THẬT SỰ XUẤT RA ĐĨA. Prop không xếp thành hàng ngang cùng độ sâu; chia 3 tầng back/mid/front theo cụm.
Các tồn đọng nhỏ của Hoang Mạc (viền halo quanh dune/sphinx, đuôi decal wind-sand bị cắt, bóng hơi nhạt) sửa kèm.

## 2. Núi Phong Thạch — TỪ CHỐI, chưa được dựng `windrock_mountain_camp`
Claude dựng cảnh thật và đo lại. Các điểm bạn báo "đạt" không đúng với ảnh:
1. Bốn ảnh nghiệm thu không có trên đĩa; contact-sheet.png vẫn là sheet cũ 19 asset. Phải xuất file thật và cập nhật sheet đủ 74.
2. `grass-snow-floor` và `snow-crust-floor` tương quan 1.00 (cùng một ảnh đổi màu); "snow crust" thành xanh ô-liu chứ không phải tuyết. Vẽ lại tuyết thật.
3. Luma đạt bằng ép trung bình RGB: rock-floor-01/02 và slate-floor có trung bình RGB y hệt [76,90,102]; các tile còn lại gần như cùng một trung bình. Không ép màu. Chỉ yêu cầu độ sáng gần nhau (±12/255); mỗi tile giữ màu và bản sắc riêng (đá phiến xanh lạnh, sỏi nâu, cỏ-tuyết, tuyết trắng xanh, đá vụn xám). Làm ít nhất 6 tile khác nhau thật.
4. `windrock-cliffs-near` có vệt nhòe dọc giữa cảnh do làm mượt đường nối đã làm bẹt pixel. Vẽ lại nền liền mạch, không blend cưỡng bức.
5. Cầu treo chỉ ~130 px, nằm trên mảng tối dạng decal, không bắc qua khe; cầu đứt lơ lửng; khe bị cắt mép ở rìa phải. Cầu phải dài ngang khe, hai đầu chạm hai mố ở hai bờ; khe là asset có bờ vực thật.
6. Đường chân trời cắt thẳng ngang, thiếu dải chuyển horizon-gradient trong scene.
7. 36 prop xếp một hàng ngang, nửa dưới trống (đúng lỗi đã cấm). Cần ≥70 prop/decal trên map dài, chia back/mid/front theo cụm.
8. `windrock-cliff-snow-ledge` vẫn là vách cát vàng cỏ khô kiểu sa mạc, mép phải răng cưa cắt dọc. Vẽ lại tông tuyết + đá lạnh.
9. Thông vặn có vệt rêu xanh neon trên thân; điểm đỏ lẻ gần chân cột (dư magenta); mảnh cột gãy lơ lửng (pillar-01). Sửa sạch.
10. audit báo 38/74 cảnh báo DENSITY, trong khi báo cáo ghi "0 cảnh báo". Giải thích hoặc sửa từng asset, không bỏ qua.
Mỗi lần nộp lại: 3 render (cam 0.15/0.5/0.85) + zoom 2× vào chỗ đổi sàn/chân prop, file thật trên đĩa, và bạn phải nhìn ảnh trước khi nói "đạt". Cảnh báo số liệu không thay cho mắt nhìn.

## 3. Thứ tự
1) `desert_entrance` layout (làm ngay). 2) Sửa lại kit Phong Thạch theo mục 2 và nộp lại. 3) Chỉ sau khi Phong Thạch đạt mới dựng `windrock_mountain_camp`.
17 map chưa có brief: hoãn, đồng ý.
