# P12 owner review (web local)

Hai trang để duyệt Stage 4 một lần: (1) `/` phạm vi (`review_detailed_scope`), chốt Three.js (Stage 3), roster NPC theo map, registry map, spawn, instance; (2) `/portals.html` trình chỉnh điểm dịch chuyển có ảnh map.
Python stdlib, không cài đặt; chỉ nghe ở loopback.

```sh
python3 tools/p12_review/build_package.py        # sinh gói duyệt từ roster (chạy lại khi roster đổi)
python3 tools/p12_review/server.py --port 8134   # mở http://127.0.0.1:8134
```

- Gói duyệt: `.ai/plan/phases/P12-world/review/review-package.json`.
- Phản hồi lưu tại `.ai/plan/phases/P12-world/review/responses/<sha256 của gói>.json`; đổi roster/gói thì bắt đầu lượt duyệt mới, phản hồi cũ vẫn giữ.
- Mỗi nhóm chọn Chờ / Duyệt / Cần sửa / Từ chối kèm góp ý. "Duyệt tất cả mục đang chờ" chỉ đổi các nhóm còn Chờ. "Duyệt toàn bộ" yêu cầu mọi nhóm đã duyệt.
- Có kiểm tra phiên bản (tab cũ không ghi đè tab mới) và kiểm tra Host/Origin.
- Sau khi gửi kết luận, báo mình để cập nhật `P12-closure-checklist.md`, README P12 và `PROJECT_PROGRESS.md`.
- App cũ ở `~/Downloads/Phimond-P12-Review` (serve.py, `reviews.json`) giữ nguyên chỉ đọc; thẻ `S1-SCOPE` thay cho mục `review_detailed_scope` còn "unresolved" ở đó.

## Trình chỉnh điểm dịch chuyển (`/portals.html`)

```sh
python3 tools/p12_review/build_portals.py         # sinh review/portal-package.json từ ~/Downloads/Phimond-P12-Review (chỉ đọc)
python3 tools/p12_review/server.py --port 8134    # --images <thư mục map-images> nếu không nằm ở ~/Downloads/Phimond-P12-Review/map-images
```

- Dữ liệu: 75 map (17 map phạm vi + 58 map của 11 vùng ngoài), 157 cửa APK 3.2 ghép cặp theo cửa đối ứng thành liên kết hai chiều hoặc một chiều, cộng 2 trụ (Quảng Trường, Hải Tặc Hào) theo quyết định của bạn. Vị trí trụ Quảng Trường lấy từ vật thể `TTTD` trong APK (trùng bệ phép xanh ngọc).
- **Mind map:** mỗi ô là một map, nhóm theo vùng; đường xanh = đã duyệt, cam = cần sửa, xám = chờ, vàng nét đứt = trụ. Bấm chọn bản đồ trái, Shift+bấm chọn bản đồ phải, bấm đúp hoặc bấm đường để mở hai bản đồ.
- **Hai bản đồ:** ảnh ghép sprite APK với các điểm đánh dấu (xanh dương = cửa, vàng = trụ, xanh lá = điểm đến, viền cam nét đứt = cần đặt). Chế độ **Nối**: kéo từ điểm này sang điểm kia, hoặc thả vào chỗ trống ở bản đồ kia để tạo điểm đến mới. **Di chuyển**: kéo điểm. **Thêm cổng**: bấm lên ảnh.
- Bảng bên phải: chọn liên kết để đổi chiều, bật một chiều, Chờ/Duyệt/Cần sửa/Từ chối, nhận xét, xóa. Nút "Điểm cần đặt kế tiếp" nhảy tới các điểm đến APK không cho biết.
- Bộ lọc trên thanh công cụ: **Tất cả / Đã duyệt / Chưa duyệt / Chờ / Cần sửa / Mới sửa** (số liệu cập nhật theo từng lần bấm). Lọc áp dụng cho sơ đồ, đường nối hai bản đồ, danh sách liên kết và nút "Duyệt … liên kết chờ" (chỉ duyệt các liên kết đang hiện).
- "Mới sửa" = khác bản nháp APK (liên kết mới, đổi đầu nối, đổi chiều một/hai chiều, có nhận xét mới). Dấu ✎ và nét dày/viền tím đánh dấu chúng; mục "Đã xóa" liệt kê liên kết bạn xóa kèm nút **Khôi phục**.
- Biểu tượng ↻ trên một map = liên kết nối hai cửa trong cùng map (đi tầng); bấm để mở map đó.
- Lưu tại `.ai/plan/phases/P12-world/review/portal-edits/portal-graph.json` (mỗi lần lưu giữ bản trước trong `history/`). Chạy lại `build_portals.py` không xóa bản bạn đã sửa; khi dữ liệu gốc đổi, thanh trạng thái báo "dữ liệu gốc đã đổi".
- Giới hạn: ảnh map là ảnh ghép sprite tĩnh, không chứng nhận collision hay đường đi; tọa độ cửa là của APK. Điểm đến của cửa một chiều không có trong APK được đề xuất cạnh cửa đối ứng (khoảng 1 đơn vị) hoặc đánh dấu "cần đặt".
