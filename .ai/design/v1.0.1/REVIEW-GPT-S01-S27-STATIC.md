# Review 41 PNG tĩnh GPT (octopath-s01-s27-20261029) — Claude, 2026-10-29

Kiểm máy: alpha nhị phân OK (0 pixel bán trong suốt), ≤48 màu OK, không magenta key thật.
Kiểm mắt: 7 contact sheet. Chưa cài file nào vào client.

## A. Duyệt nguyên trạng (23; số ở bản đầu ghi sai là 21)
bar-frame-{hp,mp,exp}, bar-label-{hp,mp,exp}, ui-minimap (khung 512x320, lòng rỗng), city-facade-column, city-facade-gutter, city-facade-alley, fx-beast, fx-insect, fx-plant (6 frame, frame 0/5 nhỏ là chủ ý), shadow-{canopy,rect,round-large,round-small}, stone-plinth-square, stone-wall-face (CHỈ kéo 1 lần, không lặp ngang; seam 14), fg-city-awning-edge, fg-forest-bush-{a,b,c}

## B. Duyệt sau khi mình tự despill viền hồng (12; bản đầu ghi sai là 13) — không cần GPT vẽ lại
city-near-roofs(277px), fg-city-lantern-pair(415px; mạng nhện tím nhạt cần xoá hoặc đổi nâu xám), fg-forest-branch-{a,b}(~590px), fg-hall-curtain(203), stone-plinth-round(19), stone-step-{face,side-left,side-right}, grass-ledge-top(167), palace-courtyard-passage(135), fence-stone-low (mảnh, dùng được)

## C. Cần sửa / nhờ GPT (6 file)
- forest-far-layers: 29 hàng đen đặc đáy → mình cắt/làm trong suốt; sau đó duyệt.
- dirt-cliff-face: 1 hàng đen trên + mép trái/phải lệch màu (seam 27) → không lặp ngang được; dùng 1 lần theo chiều rộng hoặc GPT vẽ bản lặp.
- city-backdrop-wide: trời xanh dương bão hoà phẳng (#0070FF), lệch tông Octopath hoàng hôn; mình có thể đục trời để scene tự đổ gradient, nhưng mây dính trời → nên GPT vẽ lại trời trong suốt hoặc mình chấp nhận bỏ mây.
- fg-city-bunting: giữa dải (~x=500) mẫu cờ bị cắt và nối lại, thấy rõ vết nối → GPT vẽ lại liền mạch.
- palace-wall-fill, wood-bridge-plank (stone-wall-face đã xếp ở A với cùng hạn chế): seam trái/phải 11–14 → chỉ dùng kéo 1 lần, không lặp; nếu cần lặp phải bản tileable.

## D. Chưa duyệt được
S07/S08 khác hash so với E19/E20 đã duyệt: cần so cạnh nhau (chưa làm); S23 phải vẽ lại; S24 chờ player-male.run.png.

## E. Bản vẽ lại redraw-v2 (review lần 2)
- city-backdrop-wide v2: DUYỆT. Trời trong suốt, tông ấm, mây ấm. Kiến trúc hơi cao/hẹp do co giãn không đều nhưng chấp nhận được ở vai trò nền xa.
- fg-city-bunting v2: DUYỆT. Dây liền mạch, lặp 3 lần không thấy vết nối, màu teal/cam/kem hợp tông.
- Run male/female (owned/, processed/*-qc): vẫn chưa phải ứng viên; frame 6–7 đầu 0.96, chân dẫn "unclear" ở frame 2 và 5 → giữ trạng thái từ chối.

## F. Đã cài (tool `tools/p01/install_s01_s27.py`, chạy lại được)
- 31 ảnh nhóm A, B, C đã xử lý (khử viền hồng, cắt dải đen) vào `apps/client/public/hd2d/` và đăng ký `assets.json` (loại prop / decal / backdrop_far / backdrop_mid / fg; ảnh có hạn chế lặp mang `repeat: never`). `city-backdrop-wide` và `fg-city-bunting` dùng bản redraw-v2.
- `fx-beast/insect/plant` + `fx-fire/water/earth` (lô P01) vào `public/battle/`, **đã nối vào trận**: đòn có hệ lửa/nước/đất dùng bảng hệ, còn lại dùng bảng theo tộc kẻ ra đòn (thú/côn trùng/thực vật), hệ khác vẫn hiệu ứng CSS tới khi có M01–M04.
- `ui-minimap` **đã nối** làm khung minimap (9-slice). `bar-frame-*`/`bar-label-*` đã duyệt nhưng CHƯA cài (HUD mới dùng vạch mảnh).
- **Chưa nối vào cảnh**: mặt tiền thành phố, bóng, bệ đá, bậc, vách, cầu, hàng rào, nền xa/gần, tiền cảnh (cần quyết bố cục từng map và hệ thống lớp tiền cảnh mờ). File đã nằm sẵn trong `public/hd2d` để dùng.
