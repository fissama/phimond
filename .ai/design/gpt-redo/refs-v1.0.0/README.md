# Ảnh tham chiếu cho đơn GPT 09

Dùng kèm [`../09-v1.0.0-full-redo-prompt.md`](../09-v1.0.0-full-redo-prompt.md). Mỗi thư mục ứng với chặng:

| Thư mục | Chặng | Nội dung |
|---|---|---|
| `01-player/` | 1–2 | Sprite gốc APK của người chơi nam/nữ (idle, run; phóng ×4, canh đáy), bản HD-2D đã duyệt làm khóa thiết kế, so tỉ lệ 128 px/đơn vị, ảnh map gốc Bìa Rừng |
| `02-city-floor/` | 3 | Ảnh map gốc Quảng Trường, Hoàng Môn, Triệu Linh Điện; sprite gốc QTTP (×3); 5 tile bị trả (ghép 2×2 để thấy seam) và bản gốc để giữ vật liệu; tile đã duyệt liền mạch làm chuẩn |
| `03-city-skyline/` | 4 | Ảnh map gốc Quảng Trường, Hoàng Môn, Vương Cung, Thương Phố; kit thành đã duyệt; dải far đã duyệt; bản Gemini bị trả |
| `04-npc/` | 5–6, 9 | NPC gốc APK (×4), ảnh map gốc Triệu Linh Điện, NPC Đợt A đã duyệt và toàn bộ NPC đã duyệt (phải khác), vật liệu cho hòm thư |
| `05-later/` | 7–9 | Ảnh map gốc nông trại, đấu trường, Vương Cung, 4 map biển, Rừng Sâu; sprite gốc NongTrai/DauTruong/BaiBien/rungsau (×3); tile/mảnh bị trả; huy hiệu hạng; khung loading |

Quy ước tên: `orig-*` = ảnh game gốc (nguồn nội dung); `style-*`, `design-lock-*`, `approved-*` = asset đã duyệt (nguồn style); `rejected-*` = lỗi cần tránh, không dùng làm style.

## Dựng lại

```sh
# từ gốc repo; tham số là thư mục ảnh map gốc (chỉ đọc)
python3 .ai/design/gpt-redo/refs-v1.0.0/build_refs.py ~/Downloads/Phimond-P12-Review/map-images
```

Script chỉ ghép và phóng to (nearest) ảnh có sẵn, không sinh nội dung. Chạy lại sau mỗi lượt duyệt để các ảnh `approved-*` khớp manifest.

## Dùng trên ChatGPT web

Nén thư mục của chặng cần làm (ví dụ `01-player/`) rồi tải lên cùng prompt Phần 0 + prompt chặng đó.
