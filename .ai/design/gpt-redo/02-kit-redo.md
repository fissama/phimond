# GPT redo — KIT MÔI TRƯỜNG (Batch 11+) — dán sau Master v2

Mỗi phiên = MỘT kit. Thứ tự: **desert → windrock → tomb → (owner chọn) 14 kit còn lại** (nightmare, crossroads, astral, ancient, ghost_castle, world_tree, tower, maze, guild, battlefield, maya, dungeon, arena2, minigame). Danh sách mảnh tối thiểu, bảng màu, bảng map từng kit: Phần C của `.ai/design/hd2d-maps-75-gemini-prompt.md` (không chép lại ở đây).

Hiện trạng bản Gemini (tham chiếu để KHÔNG lặp, không dùng làm style):
- desert: 85 asset, được dùng làm chuẩn BỐ CỤC (layout `desert_entrance`) nhưng art phẳng hơn GPT (trung vị 20 màu/prop). Giữ lại như nguồn tham khảo hình khối; vẽ lại bằng style batch 00–09. Khi bản GPT đạt, thay trong `batch-11-desert/` (bản cũ vào `_gemini/`).
- windrock: 74 asset, BỊ TRẢ (gate 40 lỗi: DENSITY 31, bbox-edge 8, tile trùng 1).
- tomb: 11 asset thí điểm, chưa mở rộng; cần đủ 9 map theo bảng kit.

```text
[Dán Master v2 trước.] ĐỢT: kit <TÊN KIT> (<batch-11-xxx>). 

NGUỒN
 - Nội dung/hình khối: ảnh map gốc của kit (Downloads/Phimond-P12-Review/map-images/<map_id>.png cho MỌI map trong bảng kit; mở và nhìn trước) + APK sprites trong tools/build-web-assets/source/sprites/<level>/ nếu có.
 - Style: 2–3 contact-sheet batch 00–09 sát loại (tile ← batch-01 floors; cột/tường/phế tích ← batch-02/03; cổng ← batch-01 forest-portal; cây/bụi ← batch-01) + hai anchor linh thú.
 - Bảng màu kit: Phần C của prompt 75 map. Mỗi kit có palette riêng 48 màu (`phimond-octopath-<kit>`), vẽ sheet màu mẫu trước, nộp xem rồi mới vẽ asset.

SỐ LƯỢNG VÀ ĐỘ GIÀU (tối thiểu)
 - Tile sàn: ≥ 8 (2–3 chủ đạo × 2 biến thể THẬT + 1–2 vật liệu phụ), 512×512 seamless, chi tiết đọc được (cát gợn, gạch, nứt, đá lát), mỗi biến thể khác texture.
 - Chuyển tiếp mép (edge decal): 1 bộ cho MỖI cặp tile chính, mép bất quy tắc, dạng dải lặp ngang 512×128 liền hai đầu. Không chữ nhật.
 - Prop: ≥ 36, theo danh sách mảnh tối thiểu của kit; mỗi chủng loại ≥ 2–3 biến thể thật (cột gãy 3, đá tảng 3, cây 3…), nhiều cỡ (nhỏ/vừa/lớn/landmark ≥ 3 vật cao ≥ 1.6 đơn vị). Trung vị ≥ 40 màu/prop.
 - Decal tiếp đất: ≥ 12 (vệt, mảnh vỡ, cỏ/xương/đá vụn, vết nứt), bất quy tắc.
 - Shadow: 4–6 decal bóng mềm procedural (đây là ngoại lệ alpha mềm, màu của kit).
 - Backdrop: far/mid/near mỗi tầng ≥ 1 (kit có biến thể theo map ≥ 3), 1024×384 trở lên, lặp ngang không thấy đường nối, mỗi backdrop là KHUNG CẢNH khác (không đổi màu một cảnh).
 - Portal dormant/active (1 cặp mỗi kiểu cổng của kit, cùng mask), marker xuất hiện 4 khung, fx ≥ 3 (hạt/tia sáng dạng sprite sheet).
 - Landmark ĐẶC TRƯNG của từng map trong bảng kit (xem ảnh gốc): vẽ riêng, không dùng chung một sprite cho nhiều map.

CHẶNG NỘP (dừng đợi Claude ở mỗi chặng)
 Chặng 1: bảng màu + 3 tile + 3 prop đại diện (1 lớn, 1 vừa, 1 nhỏ) + 1 backdrop + 1 cổng. Claude xem ảnh, so với batch 00–09.
 Chặng 2: toàn bộ tile + edge + decal + shadow.
 Chặng 3: toàn bộ prop + landmark.
 Chặng 4: backdrop + portal + marker + fx + manifest + contact-sheet.
Sau chặng 4: `sh tools/check_hd2d_art.sh` = 0 lỗi, 3 ảnh tự ghép thử (nền + 6 prop ghép bằng ảnh phẳng chỉ để xem) để chắc các mảnh cùng tông, rồi báo Claude.

ĐIỀU KIỆN ĐẠT (Claude kiểm bằng ảnh)
 1. Đặt cạnh batch-01 trên cùng một màn hình, không thấy "hai họa sĩ".
 2. Mọi prop đọc ra là gì ở 1× (không cần phóng).
 3. Không có hai asset cùng hình khác màu; không hai tile cùng texture.
 4. 3×3 tile không ca-rô; backdrop lặp không nối.
 5. check_hd2d_art.sh 0 lỗi, không waiver mới.
```

## Ghi chú riêng từng kit
- **desert** (cát #D9B26B/#B88A44, sa thạch #A5522B, bóng tím nhạt): nhiều tông cát/đá phải khác nhau rõ; cồn cát là PROP có đổ khối, không phải elip; bia cổ không chữ.
- **windrock** (đá lam xám, bóng #4A525D): vách, cầu treo (có khe + hai mố), bậc đá; map gốc `windrock_mountain_camp` có cổng [643,374],[111,573],[2143,485] px (đã xác nhận trục Y).
- **tomb** (9 map; gạch mộ, đất nghĩa địa, bia ×2+, quách, cổng vòm, ma trơi 4 khung): thí điểm 11 asset Gemini chỉ là điểm xuất phát; làm đủ kit ≥ 36 prop.
