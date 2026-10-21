# Phimond HD-2D — Đợt 0, chờ chọn style

Ngày: 2026-10-15. Chưa hoàn thành redraw toàn game. Đây là mốc chọn style bắt buộc trước Đợt 1+ theo `.ai/design/hd2d-art-master-plan.md`.

Đã dùng `agent-sprite-forge` từ https://github.com/0x0funky/agent-sprite-forge tại commit `5324342fdfab72430f4e9604f3fe427009f8596d`: generate2dmap để tách prop/tile và kiểm seam; generate2dsprite để chuẩn hóa palette/alpha. Artwork sinh bằng công cụ image_gen tích hợp, không dùng API thay thế hay code vẽ vật thể. Bộ skill đã được cài ở ~/.codex/skills/.

## Chọn mẫu

- `contact-sheet.png`: 28 mảnh, nhãn A/B, trạng thái kiểm tra cơ học.
- `style-guide.png`: palette và mẫu thật từng kit.
- `nineslice-preview.png`: hai panel được thử ở ba kích thước.
- `<asset_id>/review-light-dark.png`: xem PNG ở 1x/2x trên nền sáng/tối.
- `<floor_id>/repeat-3x3.png`: tile lặp để soi seam và motif.

Có thể chọn A/B khác nhau cho rừng, thành và UI. B rừng tiết chế hơn; A UI giữ sắc sapphire gần nguồn hơn. Đây là gợi ý để xem mẫu, không phải quyết định thay chủ dự án.

## Nội dung

- Rừng A/B: mỗi bộ có cây lớn, bụi, cỏ, hoa vàng, hoa hồng, dương xỉ và tile cỏ — 14 PNG.
- Thành A/B: đèn, thùng gỗ và tile đá — 6 PNG.
- UI A/B: panel 9-slice và nút nghiêng thường/nhấn/khóa — 8 PNG.

28 final PNG RGBA; 25 đạt kiểm tra cơ học; 3 blocked; 0 đã được chủ dự án duyệt. Mọi final có tối đa 48 màu và alpha nhị phân; prop được căn theo điểm tiếp đất đo bởi Forge. Panel đã sửa cạnh giữa thành thanh thẳng để 9-slice không kéo méo hoa văn góc. Reviewer độc lập xác nhận bản sửa; xem `independent-review.md`.

## Blockers và giới hạn

Ba tile còn lỗi sau ba lần sinh, không được đưa vào game:

| ID | Sai lệch seam X/Y (0–255) | Lỗi |
|---|---|---|
| forest-a-floor | 1.946 / 8.7155 | ngưỡng Y < 6 không đạt; Forge wrap_seams fail |
| forest-b-floor | 1.7839 / 8.6771 | ngưỡng Y < 6 không đạt; Forge wrap_seams fail |
| city-a-floor | 0.457 / 6.5872 | ngưỡng Y < 6 không đạt |

city-b-floor: 0.0254 / 3.7995, đạt số đo nhưng vẫn phải duyệt bằng mắt về motif lặp. Toàn bộ cảnh báo/lỗi từ các lần thử được giữ trong `qa-history.json`, các manifest Forge và `qa-summary.json`; không bỏ lịch sử lỗi.

Forge forest A cảnh báo: `20 visible px belong to no auto box (small or faint parts); review auto-boxes.json or pass --boxes-file`. Pixel rời ngoài vật thể bị bỏ ở bước extraction; raw giữ nguyên. Hai lần đầu của rừng A có haze/alpha sai và không được dùng làm final. Các thư mục Forge cũ chứa nhãn auto-detect chưa review, chỉ dùng làm lịch sử; final identity mapping dùng `forge-forest-*-reviewed`.

Nút B có sai khác silhouette 1px giữa trạng thái thường và các trạng thái khác. Đèn có kính sáng, nhìn như đang bật dù không có glow ngoài vật thể. Cây có chi tiết lá dày hơn anchor linh thú. Không có video generation route trong phiên này; không coi đây là bộ animation nhân vật đã hoàn thiện.

## Cho Claude sau khi chủ dự án duyệt

1. Chỉ đọc `manifest.json` → `assets`; không quét đệ quy mọi PNG trong thư mục.
2. Bỏ qua `status=blocked`; mọi asset hiện có `approved=false` cho đến khi chủ dự án chọn.
3. Lấy PNG từ trường `file`, đối chiếu `sha256`, `px`, `world` và `pivot_px`/`pivot_uv`. Điểm pivot nằm ở chân thực, chừa 8px alpha dưới; không lấy đáy canvas làm mặt đất.
4. `scene_targets` chỉ là gợi ý cảnh dùng kit; `replaces=null` vì chưa có đối chiếu texture một-một. Không thay nguyên scene JSON bằng PNG.
5. UI dùng canvas 960x640 ở @3x, `design_px`/`ui_scale`; `world` của UI chỉ để tương thích schema. 9-slice theo [left,top,right,bottom] đơn vị pixel ảnh gốc. Text do engine vẽ. Đừng stretch nút nghiêng; giữ cùng canvas giữa các trạng thái.
6. Đây là asset rời; Claude phụ trách WebP, scene JSON, lighting, fog, bloom, water, shadows và kiểm tra trong game, theo master plan.

Art worker không kích hoạt asset, sửa runtime, commit hay push theo phạm vi riêng của master plan. Manual validation của đợt này là xem các artifact trên; không đổi server/game đang chạy.

## Audit và tiếp tục

Mỗi asset có raw nguyên vẹn, final.png, prompt.md (prompt, thứ tự reference, SHA256), review.md và qa.json. `generation-jobs.json` ghi route và các lần thử; model/chi phí không được tool công bố nên không suy đoán. `production-plan.md` giữ queue Đợt 0–11+; chưa mở các vùng P12 chưa được phép.

Python đi kèm Codex: `/Users/phileanh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Các script chuẩn bị là nhật ký pipeline đã chạy, không tự động chạy lại generation. `verify_delivery.py` và `preview_nineslice.py` có thể chạy lại để kiểm chứng final/preview. Thư mục đầu ra Forge là bất biến; một lượt sửa tiếp theo phải dùng output directory mới.
