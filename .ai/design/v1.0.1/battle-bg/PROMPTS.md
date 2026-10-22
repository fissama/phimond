# Nền màn combat (battle-bg) – prompt gửi ChatGPT

Gửi **từng ảnh một** (không zip). Với mỗi nền: đính kèm 3 ảnh
(1) `ingame-<map>.png` (cảnh trong game của đúng map đó, để bắt màu/vật thể/kiểu pixel),
(2) `our-battle-layout.png` (bố cục combat hiện tại, để biết chỗ đặt sprite và vùng HUD),
(3) `reference-battle.png` (UI game gốc 靈獸世界, chỉ để tham khảo bố cục ngang: quái trái, thú mình phải).
Sau đó dán **Prompt chung** + **Phần riêng của map**. Mỗi nền là 1 lượt riêng, lưu `battle-bg-<key>.png`.

## Prompt chung (dán đầu mọi lần)

> Hãy tạo bằng công cụ tạo ảnh (image generation), KHÔNG ghép/kéo méo bằng code: một **nền màn combat ngang** cho game mobile pixel-art phong cách **HD-2D kiểu Octopath Traveler**.
> - Khung 16:9, **1920×1080 px**, PNG, không có kênh trong suốt.
> - Góc nhìn ngang, camera cao nhẹ (~15–20° nhìn xuống), như màn combat của Octopath: một **sân khấu diorama**. Mặt đất là dải nằm ở khoảng 55–85% chiều cao ảnh, có kết cấu pixel rõ (đất, cỏ, đá...), ánh sáng quét ngang.
> - **Không có** nhân vật, sinh vật, chữ, số, khung UI, thanh máu, logo. Vùng giữa ảnh (x 15–85%, y 40–85%) phải **thoáng** để đặt hai sprite lớn (~260 px); đồ vật chi tiết chỉ đặt hai rìa trái/phải và phía xa.
> - Tầng sâu như HD-2D: tiền cảnh rất mờ ở hai góc dưới (lá, cỏ, đá làm khung), vật thể giữa sắc nét, nền xa **mờ kiểu tilt-shift**, có ánh sáng rực (bloom nhẹ), tia nắng/hạt bụi, độ tương phản và bão hòa cao như ảnh mẫu.
> - Chi tiết pixel cùng độ phân giải với ảnh mẫu trong game (1 ô đất ≈ 128 px, texture pixel sắc, **không** vẽ kiểu tranh sơn dầu mịn, không viền đen dày).
> - **12% trên cùng** để đơn giản (tán lá/bầu trời/trần) vì HUD đè lên; **18% dưới cùng** tối dần và ít chi tiết vì khung chat đè lên.
> - Chỉ vẽ ánh sáng **ban ngày**; hoàng hôn/đêm do game chỉnh màu sau.
> - Tuân thủ bảng màu, vật thể và không khí của ảnh `ingame-<map>.png` đính kèm, nhưng nhìn **ngang** thay vì chéo từ trên xuống.

## Phần riêng của từng map

### 1. `battle-bg-forest.png` – Bìa Rừng Lục Bảo (map `emerald_forest_main_woods`, có quái hoang)
Ảnh mẫu: `ingame-forest.png`.
> Rìa rừng lục bảo nắng ấm: tán cây lớn xanh vàng chồng lớp phía xa, thân cây già có rễ nổi, một con đường đất cam chạy ngang qua sân khấu, các mảng cỏ sáng, bụi hoa đỏ, nấm cam/tím ở hai rìa, vài tảng đá rêu. Ánh nắng chéo từ trên trái, hạt phấn hoa bay. Bảng màu: lục olive, vàng nắng, đất cam, điểm đỏ.

### 2. `battle-bg-deep_forest.png` – Rừng Sâu Lục Bảo (map `emerald_forest_deep_woods`, có quái hoang)
Ảnh mẫu: `ingame-deep_forest.png`.
> Rừng sâu u tối: thân cây khổng lồ xoắn, rễ cuộn, rêu dày, sương mỏng, nấm phát sáng xanh lục ở hai rìa, đom đóm, vài tia sáng hiếm xuyên tán. Mặt đất tối với lớp lá mục và rễ. Bảng màu: xanh lục thẫm, xanh ngọc bích, tím rất nhẹ ở bóng, điểm sáng vàng-lục của đom đóm. Vẫn đủ sáng để thấy sprite.

### 3. `battle-bg-gate.png` – Hoàng Môn (map `city_palace_gate`, chưa có quái, để dành)
Ảnh mẫu: `ingame-gate.png`.
> Quảng trường trước cổng cung điện: nền đá cuội sáng, tháp đá sa thạch hai bên có mái cam nhọn, tượng sư tử trên bệ, cờ xanh có huy hiệu mặt trời, cổng vòm lớn phía xa mờ, thảm đỏ chạy từ phải. Nắng chiều ấm. Bảng màu: be sa thạch, cam mái, xanh hoàng gia, đỏ thảm.

### 4. `battle-bg-city.png` – Quảng Trường Thạch Trụ (map `city_square`, chưa có quái, để dành)
Ảnh mẫu: `ingame-city.png`.
> Quảng trường thành phố đá cuội: nhà khung gỗ mái cam hai bên, đài phun nước có tượng thiên thần phía xa mờ, chậu hoa đỏ/tím, sạp chợ mái xanh lục + cờ tam giác, vài cây xanh. Trời sáng, cảm giác náo nhiệt nhưng không có người. Bảng màu: xám đá ấm, cam mái, xanh lục mái sạp, hoa rực.

### 5. `battle-bg-hall.png` – Triệu Linh Điện (map `summoning_hall_main_hall`, trong nhà, để dành cho đấu trường/luyện tập)
Ảnh mẫu: `ingame-hall.png`.
> Đại điện trong nhà: sàn gỗ tối, cột đá cẩm thạch trắng-vàng hai bên, kệ sách, đuốc tường phát quầng cam, vòng pháp trận vàng trên sàn (mờ), rèm và cờ đỏ/xanh. Ánh nến ấm cố định, tối ở rìa. Bảng màu: nâu gỗ, vàng kem, cam lửa, điểm đỏ-xanh của cờ.

## Kiểm khi nhận ảnh về
- Đúng 1920×1080, không chữ/UI/sinh vật.
- Vùng giữa thoáng, mặt đất rõ ở 55–85%, trên 12% đơn giản, dưới 18% tối.
- Màu cùng họ với `ingame-<map>.png` (không lệch sang tranh vẽ mềm).
- Đặt vào `apps/client/public/battle/battle-bg-<key>.png` (tên key: `forest`, `deep_forest`, `gate`, `city`, `hall`). Game tự nạp; thiếu ảnh thì dùng nền thế giới làm mờ như hiện nay.
