# P12 owner review (web local)

Một trang để duyệt một lần: phạm vi (`review_detailed_scope`), chốt Three.js (Stage 3) và roster NPC theo từng map (Stage 4).
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
