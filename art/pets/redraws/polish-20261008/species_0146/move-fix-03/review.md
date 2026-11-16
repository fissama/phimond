# Ma Vương Hút Máu — move correction, 2026-10-08

Owner feedback: các hàng khác đã ổn, nhưng move trông gần đứng yên.

Diagnosis: preview đã phát đủ4 frame; chân đổi pose ít và đao che bàn chân. Lỗi nằm ở art poses, không phải chọn nhầm row.

Repair: built-in imagegen tạo bốn pose bước đi; đao được cầm cao khi move để lộ chân, hai passing poses nhấc hai chân khác nhau. Dùng cùng một NN scale đóng bốn pose mới vào row2. 16 frame của idle/attack/cast/hurt-down copied RGBA byte-identically. Không repaint/xóa alpha bằng Python; giữ đầy đủ raw và nguồn cũ.

Evidence: verification.json mechanical PASS,20 distinct/safe cells,16 unchanged nonmove cells,4 changed move cells,preview copy hash match. Browser preview observed row2 frame4→frame1. playback-proof.jpg lưu UI thật. Preview mở sẵn Move với160ms/frame (review preset, chưa phải gameplay timing).

Selected candidate: move-fix-03/packed.png. Raw2x2 source has1254×1254 pixels; four complete627×627 cells and pivots recorded in assembly.json. Common NN scale≈0.3469. Opaque move height≈156–159px, idle168px; move baseline≈225 vs idle≈231. Đây là khác biệt nhẹ cần owner xem trong preview, không được gọi là khớp kích thước tuyệt đối. Runtime sizing/pivots còn chưa triển khai.

Status: focused move preview reviewed; owner acceptance of move pending. Runtime not activated. Old candidate remains available. Two other pets unchanged in this correction.
