# P01 Đợt A — nghiệm thu và sửa artwork, 2026-10-22

Scope do owner giao: phân tích, chỉnh/vẽ bổ sung assets cho 5 map Đợt A; **không sửa code**. Route vẽ: built-in `image_gen`. Không dùng code để vẽ, ghép tư thế hay kéo méo animation. Xử lý cơ học chỉ cắt sheet, key, palette, đăng ký pivot và tạo ảnh kiểm tra.

## Kết luận đầu vào

**Chưa đạt nghiệm thu phát hành.** Đã trực tiếp xem ảnh 1280×720 `refs-v1.0.1-city/current-city-square.png`, `current-palace-gate.png`, dải chạy nam và hai master người chơi. Ảnh thành xác nhận chân đế vuông, cạnh mảng gạch/thảm rõ, nền cuội có nhịp lặp lớn. Dải chạy nam giữ nguyên tư thế đứng, không có bước chân thật.

Đây là bộ artwork ứng viên, không phải tuyên bố đã đạt chất lượng Octopath hoặc đã tích hợp vào game. Mọi ảnh mới `approved=false` tới khi kiểm trong cảnh thật. Không ghi đè batch đang được các luồng khác sửa; không commit cả working tree đang bẩn.

## Chuẩn hình ảnh

- Giữ thiết kế người chơi đã duyệt; NPC theo chuẩn Elin/Selka, không đổi thành chibi.
- 128 px/world unit; người chơi/NPC cell 192×192, pivot (96,184), người cao khoảng 168 px. Nhân vật mập/gầy khác nhau có chủ ý, không ép mọi silhouette thành một người.
- Pixel clusters rõ; outline tối cùng sắc, ánh sáng ấm trên-trái-trước, bóng trung tính hơi lạnh. ≤64 màu/asset, ưu tiên 48 màu; alpha 0/255.
- Path transition là mảnh mặt đất; rìa rừng tách far/mid/foreground; không nướng DOF/sương vào props.
- Bóng tiếp xúc là decal riêng: không nướng bóng xuống chân sprite dựng đứng. Owner yêu cầu bóng ưu tiên hơn quy tắc cũ cấm vẽ bóng.

## Deliverables theo báo cáo owner

| Nhóm | Artwork cần có | Điều kiện kiểm |
|---|---|---|
| A | Nam/nữ: walk 6 + idle 4, side/down/up | Đổi chân thật, cùng costume/scale/pivot, không warp |
| B | 4 cạnh, 4 góc trong, 4 góc ngoài; đầu/cuối, T, cong | Cỏ lấn bất quy tắc; không cạnh hình chữ nhật; kiểm mối nối |
| C | Tán xa, thân giữa, bụi trước; góc, viền camera, portal | Silhouette nhiều lớp và giá trị sáng tối phân biệt |
| D | Thảm tua, brick/cobble edge, bậc đá, nền cuội biến thể, đế giếng tròn | Nhìn trong cảnh, kiểm repeat, không vá mép bằng code |
| E | Bóng nhỏ/lớn/chữ nhật/tán | Dither nhị phân, cùng hướng sáng, separate ground decal |
| F | Mira, bia_skill, bia_free, sq_pillar, sq_skill, sq_exchange, sq_warehouse: idle 4 | Khớp danh tính roster; tỉ lệ và độ nét khớp nhóm cũ |
| G | Menu panel có title band/content gutter, chat viền vàng | Không vẽ chữ; safe regions ghi rõ; kiểm nine-slice |
| Bổ sung | Mảnh nối mặt tiền, chân tường sảnh, debris rừng | Khớp vật liệu và mật độ pixel của kit |

## Giới hạn được xác minh qua đọc code (không sửa)

- `apps/client/src/render/engine.ts:setPlayer` chỉ truyền cờ lật trái/phải. `CharacterSprite` chỉ có một strip idle/run, không chọn lên/xuống. Artwork 3 hướng tự nó không sửa được hành vi này.
- `scene.ts` dựng mặt đất theo ô; bộ góc/cạnh mới cần được đặt/tra theo adjacency. Vẽ tile đẹp không tự đổi bố cục đường chữ nhật.
- Rìa rừng hiện rải theo hash và xác suất. Layer kit mới cần được dựng thành các lớp tương ứng.
- Bóng đã có trong engine nhưng phụ thuộc quality/castShadow/decor. Asset bóng mới chưa tự hiện dưới mọi vật.
- Lỗi Mira bị tường che, tiêu đề/nút UI tràn khung và nhãn tên nổi cần kiểm placement/depth/layout. Không đánh dấu đã sửa chỉ vì vẽ panel.

Chỉ nghiệm thu toàn cảnh sau khi owner/Claude tích hợp artwork và kiểm 1280×720, walk 8 giây/route, đổi 4 hướng, góc/portal đủ 5 map; iPhone/Safari vẫn là lượt kiểm riêng.
