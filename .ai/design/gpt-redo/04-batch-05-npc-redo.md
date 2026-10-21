# GPT redo — Batch 05 NPC (bỏ sprite trùng) — dán sau Master v2

Hiện trạng đo 2026-10-19: batch-05 có nhiều thư mục `npc-*` nhưng nhiều NPC dùng cùng một final.png byte-identical (19 nhóm trùng, vd nightmare_03 = ghost_01 = ghost_05; tower_03 = ranch_keeper = summoner_mira; 8 NPC chung một sprite). Mục tiêu: mỗi NPC một ngoại hình riêng, đọc ra vai.

```text
[Dán Master v2 trước.] ĐỢT: Batch 05 — vẽ lại CHỈ các NPC trùng sprite (danh sách nhóm trùng Claude sẽ gửi kèm; giữ lại 1 NPC đại diện của mỗi nhóm nếu sprite đó đã đẹp, vẽ mới cho các NPC còn lại).
- Style: sprite NPC đã duyệt của batch-05 (chọn 3 NPC không trùng làm anchor) + hai anchor linh thú. Ô 192×192, thân ~160–170 px, pivot giữa-đáy, 33–48 màu, alpha nhị phân, lề ≥ 8 px.
- Mỗi NPC khác nhau ở: dáng/giới/tuổi, trang phục theo vùng (bảng tên và vai: .ai/plan/phases/P12-world/P12-world-names-master.md và roster ở brief map), đạo cụ đặc trưng vai (thợ rèn–búa, thương nhân–túi hàng, y sĩ–cuốn thuốc, đội trưởng–giáo/áo giáp...). Không đổi màu một sprite để thành NPC khác; không lật gương.
- Mỗi NPC 1 hướng nhìn thẳng (như batch-05 hiện tại); nếu batch hiện có đủ hướng thì giữ cùng bộ hướng.
- Vẽ theo sheet 6 NPC/lần, nền #FF00FF, raw-01 giữ nguyên; thư mục riêng; review.md ghi vai + điểm khác biệt; kiểm trùng: không hai final trùng hash và không trùng mặt nạ alpha.
- Chặng 1: 6 NPC đầu xem trước, chờ Claude.
```
