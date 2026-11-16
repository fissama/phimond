# Prompt K1 — Kit nhỏ garden-c: hạt theo họ + bong bóng "thiếu nước"
Copy khối dưới gửi Codex. Có thể chạy song song với P1 và các đợt cây.

```
NHIỆM VỤ: Vẽ và đóng gói kit nhỏ garden-c: (1) seeds: hạt dùng chung theo 6 họ cây; (2) bubble-thirsty: bong bóng "thiếu nước". KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: chỉ báo xong khi cả hai atlas qua cổng bên dưới, hoặc có số đo chứng minh bất khả. Không hỏi lại.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md (pipeline đóng gói pivot, nearest-neighbor, không sửa pixel tay), master rules 00-master-v2.md. Tạo thư mục art/src/hd2d/garden-c/ với manifest.json cùng định dạng garden-b, tools/ (mở rộng pack_atlas.py và measure_atlas.py nhận kích thước ô và pivot qua tham số, không đổi hành vi bản garden-b).

1. seeds — atlas 256x384 RGBA, 4 cột x 6 hàng, ô 64x64. Mỗi hàng là một họ, 4 khung lặp nhấp nháy/nhịp thở nhẹ (hạt nằm trong mô đất nhỏ, thấy hạt rõ): hàng 1 H thảo/rau (hạt nhỏ xanh nhạt trong đất), hàng 2 F hoa (hạt có cánh nhỏ hồng), hàng 3 D quả (hạt tròn nâu vàng), hàng 4 R củ (mảnh củ nhỏ kem), hàng 5 N nấm (bào tử trắng li ti trên mô đất), hàng 6 T tinh thể (mảnh tinh thể xanh tím trong đất). Pivot: đáy mô đất tại (32,56). Thân hạt gần như đứng yên (IoU liền kề >=0.90), chỉ nhịp nhẹ/nhấp nháy. Mỗi hàng <=24 màu, tổng <=60 màu, alpha nhị phân, mọi pixel trong [4,59], viền cùng tông, không glow/bóng/chữ baked.
2. bubble-thirsty — atlas 256x64 RGBA, 4 khung ô 64x64, bong bóng chat tròn nhỏ có đuôi trỏ xuống, bên trong giọt nước mặt buồn xanh nhạt (mắt, miệng nhỏ), viền tối. Bập bềnh nhẹ lên xuống 2–3 px qua 4 khung, đuôi bong bóng giữ pivot (32,60). <=24 màu, alpha nhị phân, mọi pixel trong [4,59].

LUẬT CỨNG: image_gen vẽ trên nền #FF00FF; code chỉ cắt, tách nền, giảm palette, đóng gói, đo. Không sửa pixel tay, không tự đặt approved:true. Mỗi atlas tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo và đề xuất, KHÔNG nới ngưỡng.

GIAO: final.png, anim.json (cell, cols, rows, fps, loop, pivot), prompt.md, review.md, qa.json, preview PNG/GIF, ảnh 4x có lưới pivot, manifest.json (ready_for_claude_review, approved:false), contact-sheet.png. Báo cuối: bảng cổng + số đo, file đã tạo/sửa.
```
