# Batch 10 / chặng A — production

Chỉ bốn lớp login. Vẽ bằng built-in image_gen, ba lần tạo/sửa sheet 2×2. Không API trả phí; không code vẽ nội dung. Dùng lại quy trình raw → key → palette → export → QA từ batch-01; package.py chỉ xử lý ảnh đã tạo và ghép ảnh kiểm tra.

Đã nhìn contact sheet batch 01, 02, 03, 06 và hai anchor linh thú trước khi vẽ. Năm tham chiếu thật được đính kèm: ảnh farm gốc (nội dung thế giới), canopy batch01, facade batch02, DocDangNu, DaoThienDuong. Giới hạn tool năm ảnh; edit đính kèm raw đích cùng hai style và hai anchor. Thứ tự, prompt đầy đủ và SHA256 từng lượt: jobs/login-stage-a/selection.json và prompt.md từng asset. Thành lấy mô tả chặng A và ngôn ngữ kiến trúc facade đã duyệt; ảnh farm không phải nguồn hình thành.

Chọn sky/forest lần 3, citadel/foreground lần 1. Bản Gemini cũ: _gemini-rejected/, 123 file giữ nguyên byte, inventory SHA256 tại rejected-archive-inventory.json.

Cắt theo hộp đã đo, bỏ 3px gutter mỗi cạnh. Key nền qua Forge extract_prop_pack.key_sheet: threshold180, border220, despill radius3; loại dư magenta có R>G+30 và B>G+30. Không tô bù hình. Scale nearest-neighbor lên1280×720. Palette không dithering: forest44 màu từ palette batch01, bỏ ramp tím không dùng cho lá/đất; town64 từ town48 +16 màu cây đã duyệt; dawn64 MEDIANCUT, là palette bình minh bổ sung duy nhất. Sky opaque; các lớp còn lại alpha nhị phân. Không blur, gradient code, fog, text, shadow hoặc bloom code.

Chạy lại: python3 package.py (cần Pillow/numpy và skill generate2dmap local). Rerun tạo lại QA cơ học và đặt visual review pending; phải nhìn lại rồi ghi review trước khi nộp. Contact sheet + qa-layer-stack chỉ là ảnh kiểm tra. Không xuất login-panorama trước khi duyệt các tầng.

Cổng: sh tools/check_hd2d_art.sh và python3 tools/hd2d_audit/art_gate.py --all. Cả hai exit1 do lỗi ngoài Batch10; xem gate-summary.json và log nguyên văn. Không sửa gate, waiver hay runtime. Không commit.
