# v1.0.1 — sửa theo đánh giá "người chơi khó tính"

Nguồn: `review-graphics-v1.0.0.md`, `review-gameplay-v1.0.0.md` (cùng thư mục). Trạng thái ghi ngày 2026-10-22.

## Đã làm trong bản này

### Đồ họa (đợt GPT vẽ lại, đã cắt và nối vào client)
| Mục review | Việc đã làm | Trạng thái |
|---|---|---|
| N1 chu kỳ đi | Dải đi 6 khung thật: nam (bên, xuống), nữ (bên). `CharacterSprite` có dải theo hướng (`run`, `run-down`, `run-up`), lên/xuống không còn lật ngang. | Còn thiếu hướng lên (nam, nữ) và xuống (nữ): hiện dùng dải bên. |
| N2 đường đất chữ nhật | 6 mảnh chuyển đất↔cỏ (`path-fringe-*`, `path-cap-*`) đè lên mép đường (`fringe()` trong `scene.ts`). | Cần chỉnh thêm: ảnh trong cảnh vẫn lộ nhịp ô vuông; mảnh sáng/chi tiết hơn cỏ nền. |
| N3 viền rừng | 6 mảnh viền theo lớp (`forest-*`), `dressForest()` dựng tán xa, thân giữa, bờ trước, góc, bờ phía camera, cổng portal. | Đạt trong ảnh chụp; chưa kiểm map Rừng Sâu kỹ. |
| N4 thảm/gạch/bệ | Chưa vẽ. | GPT còn nợ (xem `GPT-REMAINING.md`). |

Tất cả asset mới `approved=false` cho tới khi người duyệt trong cảnh thật. Cắt bằng `tools/p01/cut_release_art.py`, nạp bằng `python3 tools/p01/sync_client_assets.py --merge` (KHÔNG chạy bản đầy đủ: nó xóa `public/hd2d` và làm hỏng các file theo dõi trong sparse checkout).

### Gameplay
| Mục review | Sửa |
|---|---|
| G1 Mira bị tường che | Tường sảnh lùi sau hàng 1 (`scene.ts`). |
| G2 không hướng dẫn | Khung "Mục tiêu" ở HUD (`game/goal.ts`), nút Chọn đổi nhãn theo ngữ cảnh và nháy khi có thể tương tác, 3 dòng chào ở chat. |
| T2 Menu khóa mà không báo | Chạm/giữ phím khi bảng đang mở hiện thông báo "Đóng bảng đang mở để tiếp tục di chuyển". |
| T3 chạm ô chặn | Tự đi tới ô đi được gần nhất trong bán kính 2. |
| T5 trận đè D-pad | HUD thế giới ẩn hẳn khi đang trong trận. |
| L1 chat trống | Chat gọn 2 dòng, bấm để mở 6 tab, tự mờ sau 7 giây. |
| L2 Menu lệch khung | Nội dung lùi vào trong khung kim loại, tiêu đề giữa, nút rộng bằng vùng nội dung. |
| G3 trượt | Một phần nhờ dải đi mới; xem nợ về hướng lên. |

### HUD (hướng "game thật", không còn là bản demo)
Căn cứ nghiên cứu: vùng an toàn, mục tiêu chạm ≥ 44–48 px, neo theo cạnh/góc, hiện dần theo ngữ cảnh, mờ khi không cần, tùy chọn mật độ, hỗ trợ ngang/dọc.
- Bản đồ nhỏ góc phải trên (vẽ từ lưới đi được; ô cổng, NPC, bệ/trụ, vị trí người chơi).
- Cột menu 4 nút dưới bản đồ nhỏ; nút Chọn theo ngữ cảnh ("Nói chuyện", "Chọn bệ", "Dùng trụ").
- Cài đặt → "Mật độ giao diện": Đầy đủ / Gọn (ẩn mục tiêu, bản đồ nhỏ, chat).
- Điện thoại nằm ngang (cao ≤ 500 px): bỏ mục tiêu và bản đồ nhỏ, thu nhỏ nút, D-pad nhỏ lại. Dựng đứng (≤ 520 px): xếp lại tên map, bản đồ nhỏ, menu.
- Tôn trọng `prefers-reduced-motion` cho hiệu ứng nháy của nút Chọn.

## Kiểm
`vitest` 21/21, `tsc` sạch, `npm run build` ổn, Playwright chromium 7/7 (SwiftShader, không đại diện hiệu năng).
Chưa kiểm: iPhone/Safari thật, hiệu năng GPU thật.

## Xem thêm
- `DEBT.md`: nợ kỹ thuật/nội dung chưa làm (Phase sau).
- `GPT-REMAINING.md`: danh sách việc vẽ còn lại, gửi GPT khi hết giới hạn.
