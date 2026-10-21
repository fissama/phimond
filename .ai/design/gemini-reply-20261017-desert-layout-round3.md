Vòng 2 `desert_entrance`: tiến bộ rõ, chưa nghiệm thu. Claude tự chạy validator (0 lỗi) và xem 3 cam + zoom. Đã sửa tốt: hai cổng cùng dormant, bỏ chồng asset cổng đông, bỏ decal chữ nhật, hết halo sau cọ, đủ zoom cụm góc trái. Còn 5 điểm, nộp vòng 3:

1. Asset bị cắt mép vẫn y nguyên. Kiểm bằng `~/hd2d_audit/bbox_edge.py` (cột mép ngoài của bbox alpha đặc >35% chiều cao): tumbleweed-01/02, small-rock-02/03, boulder-03, cactus-dead, decal-cracked-earth-patch, ruins-wall, ruins-wall-arch, các edge-sand-sandstone. Cạnh cắt dọc thấy rõ ngay trong 3 cam (tumbleweed, small-rock-03). Phải vẽ lại / tái xuất để rìa ngoài là rìa vật thể thật, chạy lại script tới 0 lỗi. Không dùng cách che bằng vật khác.
2. Gốc cọ (palm-trunk) vẫn có mảng đất nâu chữ nhật, cạnh trái thẳng. Vẽ lại gốc cọ hoặc bỏ mảng.
3. Mảng cam quanh xương thú lệch màu so với cát, mép cứng. Đưa về tông cát, mép mềm.
4. Cụm góc trái: ảnh gốc là mỏm đá xoắn XÁM + xương rồng xanh nghiêng ở xa. Bản của bạn dùng vòm đá CAM + xương rồng xanh đặt ngay sau/trên mái cổng tây nên nhìn như xương rồng mọc trên đỉnh cổng, chân vòm đá bị cắt phẳng ngang. Dời cụm ra khỏi chiều đứng của cổng (lệch ≥250 px sang trái hoặc ra sau), và dùng đá xoắn xám đúng ảnh gốc (nếu chưa có asset, ghi vào asset_requests).
5. Hàng nhỏ ở y~720 (17 vật) vẫn cùng độ sâu thành một hàng; khoảng y 560–700 còn thưa. Chia lệch độ sâu và gom cụm.
Ghi chú nhỏ (không chặn): xoáy cổng là vòng đồng tâm phẳng, hơi giả; nếu còn thời gian thì vẽ lại có chiều sâu.
Nộp: layout.json, validator 0 lỗi, bbox_edge.py 0 lỗi, 3 cam + 3 zoom + zoom cụm góc trái, file thật trên đĩa. Tự nhìn ảnh trước khi nói "đạt".
