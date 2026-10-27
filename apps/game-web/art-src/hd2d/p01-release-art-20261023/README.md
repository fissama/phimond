# Artwork P01 v1.0.1 — cập nhật 2026-10-24

Phạm vi: artwork 2D và metadata, không sửa code game. Chuyển động được vẽ bằng các tư thế 2D; không tạo video. Sprite Forge được dùng cho guide, căn khung và QA, không dùng pipeline video.

## Bản xem và hồ sơ

- [DELIVERY-BOOK.md](DELIVERY-BOOK.md): xem từng PNG riêng với prompt, QA và preview nếu có; không ZIP.
- [manifest.json](manifest.json): danh sách 110 PNG ứng viên, phân biệt lịch sử duyệt với bản sửa đang chờ duyệt.
- [asset-audit.json](asset-audit.json): audit file/kích thước/lề/palette/alpha của lô riêng. Kết quả này không chứng minh gait hoặc chất lượng release.
- [forge-registration-v2/summary.json](forge-registration-v2/summary.json): kiểm tra chuyển động, giữ nguyên ngưỡng mặc định và cảnh báo.

## Trạng thái thật

Đã có 24 dải chuyển động: nam/nữ và sáu walkers, mỗi nhân vật ba hướng, mỗi dải 8 khung 1536×192. Các dải dùng cùng palette 48 màu, alpha nhị phân và chân neo (96,184). Boy/girl giữ chiều cao theo idle gốc (128/124 px), không phóng thành người lớn. Các tư thế là hình sinh độc lập, không lật nửa chu kỳ hay nhân khung để giả bước.

Đã vẽ các hạng mục cảnh R32–R37, bóng R60, mảnh nối mặt tiền R61 và khung/nhãn R62. Đã bổ sung bộ chân dung, starter, NPC idle, FX, UI và địa hình theo inventory. Những mục được Claude duyệt trước đây giữ lịch sử duyệt; bản sửa palette/cắt khung/alpha cần duyệt lại.

Đã sửa đạo cụ bị mất ở một số hướng của baker, elder, girl, guard và traveller. Dải nữ ngang, elder ngang và traveller ngang đã thử vẽ từng tư thế từ cùng master để giữ identity. Cần đọc QA mới nhất: không tự coi đủ 8 ảnh khác nhau là một chu kỳ đi đạt.

**Chưa chứng nhận release.** Các dải ngang elder, guard, traveller và dải guard lên vẫn bị máy báo fail trong lần audit gần nhất; kiểm tra lại sau mọi bản sửa. Các điểm nối chu kỳ và khung gần trùng của một số dải khác cũng cần xem preview. Claude có quyền duyệt; Codex chỉ ghi Đã vẽ.

## Nạp và phạm vi thay đổi

Không nạp bản chưa duyệt vào public. Năm battle background đã được nạp ở lượt trước và có hồ sơ hash riêng trong battle-installed.json. Các asset mới còn lại nằm tại art-src để review.

Chỉ dùng sync_client_assets.py --merge khi được nạp. Công cụ hiện chưa xử lý idle override đầy đủ; phần đó thuộc người triển khai code, không sửa trong lượt artwork. Không thay gate hoặc waiver để làm kết quả xanh. Audit toàn repo gặp KeyError: file ở manifest cũ; audit riêng lô này chạy bằng chính audit.py không sửa đổi.

Working tree có thay đổi từ các luồng khác; không tự commit/push toàn workspace. Các helper xử lý crop/key/palette/căn nguyên pixel nằm ở /tmp; không dùng chúng vẽ lại hình, warp thân hay tạo chuyển động giả.

Kết quả mới nhất và các bước còn lại: [REVIEW-QUEUE.md](REVIEW-QUEUE.md).
