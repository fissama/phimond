# login-layer-1-sky — self review

Trạng thái: bản nộp chặng A, **chờ Claude duyệt ảnh**. Không tự cấp approved.

Đã nhìn final và bản nearest-neighbor 4× trên nền caro/nền tối, cùng crop chi tiết 4×. Cụm pixel, silhouette và viền alpha đọc được; không thấy chữ, fog hay quầng key magenta trên bản xuất cuối. Highlight vật liệu có sẵn trong art; không thêm lớp glow/bloom bằng code.

Dải trời vẫn hơi đều; biến thiên màu nhỏ bên trong dải còn hiện ở 4×. Đây là lớp yếu nhất về độ tự nhiên của cụm pixel.

Kiểm tra cơ học: 1280×720 RGBA; 64 màu; alpha trung gian 0; dư key 0; raw nguyên vẹn True; lỗi 0. Pass cơ học không đồng nghĩa đạt style hoặc đã được duyệt.

Nguồn chọn: `raw-03.png`, hộp cắt `[24, 24, 813, 454]`. `raw-01.png` luôn giữ nguyên sheet gốc lần đầu; các lần thử sau được giữ riêng. Prompt và SHA256 của từng ảnh đính kèm nằm trong prompt.md. Không dùng art Gemini làm style.

Viền trái/phải/đáy chạm canvas là chủ ý của tầng phủ toàn viewport, không phải prop rời. Overlap ba cặp lớp đo trong overlap-qa.json. Bảng màu và phép xử lý xem production.md ở thư mục cha.
