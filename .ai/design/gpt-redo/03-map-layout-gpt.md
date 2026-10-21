# GPT — BỐ CỤC MAP bám map gốc (thay `hd2d-map-layout-prompt.md` khi giao cho GPT)

Giữ nguyên toàn bộ nội dung 7 mục của `.ai/design/hd2d-map-layout-prompt.md` (bám map gốc, neo cố định, độ sinh động, vị trí hợp lý, schema layout.json, tự kiểm, lỗi đã bị trả). Dán khối dưới đây SAU khối đó (hoặc sau Master v2 nếu GPT chưa có bộ kit).

```text
BỔ SUNG CHO GPT (mỗi phiên MỘT map)
 A. Đầu vào đính kèm: ảnh gốc map-images/<map_id>.png, brief .ai/design/map-briefs/kit_<kit>/<map_id>.md và .json, manifest.json của kit đã đạt.
 B. Chỉ dùng asset trong manifest của kit đã đạt gate. Thiếu thì ghi vào asset_requests, đừng vẽ chen.
 C. Công thức tọa độ: px = ((x−xmin)·100, (ymax−y)·100), CHÂN vật. Đã xác nhận đúng trên desert_entrance (cổng [118,490], [2406,441]). Nếu cổng lệch ảnh gốc, báo ở reading.notes.
 D. Đủ: reading, anchors (không dời trừ khi moved+reason), floor (1 tile chủ đạo + patch có edge decal), placements 3 tầng back/mid/front với cụm 2–4 vật, shadow dưới mỗi vật đứng, fx từ danh sách engine.
 E. Nộp: layout.json + preview.png (phác phẳng chỉ để xem). Chạy `python3 tools/build-web-assets/validate_hd2d_map_layout.py layout.json brief.json manifest.json` = 0 lỗi.
 F. Claude dựng render 3 camera (_cam_015/_cam_050/_cam_085) + zoom cổng/NPC; bạn xem ảnh và sửa theo nhận xét. Không báo "đạt" khi chưa xem ảnh. Không sửa validator/gate.
 G. Chuẩn so sánh: layout `desert_entrance` (round 4) ở .ai/design/map-layouts/desert/ là benchmark về bố cục; style art phải theo batch 00–09.
```
Lưu ý cho Claude: 17 map chưa có brief (đấu trường, bang hội, Maya, địa lao, Sói–Cừu) cần dữ liệu bounds trước khi giao.
