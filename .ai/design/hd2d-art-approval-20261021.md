# Duyệt art HD-2D batch 01–10 — 2026-10-21

- **Người duyệt:** Claude, theo ủy quyền của owner trong chat 2026-10-21 ("review tất cả assets hiện có, nếu không chê thì duyệt giúp mình").
- **Quyết định máy đọc:** [`hd2d-approval-20261021.json`](hd2d-approval-20261021.json), áp vào manifest bằng `python3 tools/hd2d_audit/apply_approval.py .ai/design/hd2d-approval-20261021.json`.
- **Cách duyệt:** xem contact sheet từng batch và ảnh bản hiện tại của các mảnh Gemini bổ sung sau; ghép thử tile 2×2; đo seam mép tile, mảnh rời (connected components), ảnh trùng hash, alpha chạm mép.
- **Ngoài phạm vi:** batch-00 (mẫu style, lưu trữ), batch-11 (GPT đang vẽ lại).

## 1. Kết quả

| Batch | Nội dung | Duyệt | Vẽ lại | Không dùng |
|---|---|---|---|---|
| 01 | Rừng Lục Bảo | 61 | 1 | 0 |
| 02 | Thành, cung, sảnh, nông trại, đấu trường | 89 | 13 | 0 |
| 03 | Bãi biển | 36 | 4 | 0 |
| 04 | Tàu + ký hiệu dùng chung | 21 | 0 | 0 |
| 05 | Người chơi, NPC, chân dung | 51 | 21 | 58 |
| 06 | HUD thế giới | 66 | 0 | 0 |
| 07 | HUD trận, FX, trạng thái | 71 | 0 | 0 |
| 08 | Menu, panel, trứng, ngọc | 83 | 0 | 0 |
| 09 | Icon | 118 | 4 | 0 |
| 10 | Đăng nhập, loading, logo, intro | 14 | 1 | 0 |
| **Tổng** | | **610** | **44** | **58** |

## 2. Vì sao vẽ lại

- **Tile không liền mạch (12):** `city-paving-01/02/03`, `city-brick-path`, `hall-floor-stone`, `farm-tilled-01/02`, `arena-floor`, `farm-dirt-path-strip`, `sand-dry-warm`, `sand-seagrass`, `coastal-cliff-mid`. Mép lệch 4–20 đơn vị màu so với 2–4 bên trong; ghép 2×2 thấy rõ đường cắt (nặng nhất ở paving-02). Đây đúng là các mục batch tự ghi `blocked`. `forest-canopy-mid` cũng ghi `blocked` nhưng chỉ lặp ngang và seam ngang = 0, nên duyệt.
- **Mảnh Gemini bổ sung (6):** `city-skyline-far`, `arena-stands-far`, `royal-carpet-runner` còn dải/mảnh thừa của sheet; `farm-hills-far` vẽ kiểu vector phẳng, lệch kit; `deep-sea-floor-tile` còn viền magenta; `deep-woods-giant-tree` bị cắt phẳng ngọn. Duyệt 3 mảnh Gemini đạt: `royal-throne`, `palace-marble-pillar`, `prosperity-treasure-chest`.
- **NPC trùng ảnh hoặc sai loại (21):** 19 nhóm dùng chung một ảnh; mỗi nhóm giữ ảnh cho 1 NPC ưu tiên (Đợt A trước, rồi map lõi, rồi tier main), NPC còn lại vẽ mới. Thêm `sq_pillar` (Trụ Sư Orsa) và `ship_pillar` (Hoa Tiêu Trụ Kael): roster ghi là người vận hành trụ nhưng sprite là khối pha lê.
- **Không dùng (58):** `npc-ancient_01…npc-tree_06` là bản Gemini đặt tên theo roster 49 cũ, không khớp ID nào trong roster P12 hiện hành (107 NPC). Không gán, chỉ giữ làm tham khảo; NPC vùng ngoài thật sự (55 ID) vẫn là việc vẽ mới.
- **Khác (5):** `rank33/41/53/54` còn mảnh vụn; `loading-bar-fill` hoa văn lệch phong cách khung.

## 3. Đủ asset cho Đợt A (v1.0.0) chưa

| Map | Có sẵn (đã duyệt) | Thiếu / chặn | Kết luận |
|---|---|---|---|
| Triệu Linh Điện | sàn gỗ, tường đá/gỗ, 3 bệ triệu hồi tắt/sáng, hoa văn sàn, nến, đuốc, rèm, cột, cửa | tường hoa văn sau bệ, cửa sổ sáng (nên có) | **Dựng được** |
| Bìa Rừng Lục Bảo | đủ kit rừng: 3 cỏ, 2 đất, chuyển tiếp, cây/bụi/đá/nấm, cổng, nền xa/giữa/trước, đom đóm, lá bay | — | **Dựng được** |
| Rừng Sâu Lục Bảo | dùng kit rừng | bộ "rừng sâu" riêng (nợ N06) | **Dựng được** (tối hơn bằng ánh sáng) |
| Hoàng Môn | cổng cung, tường, tháp, tượng lính, cột, cờ, thảm | **sàn lát thành**, **nền xa thành** | Dựng được với placeholder; **chặn phát hành** |
| Quảng Trường Thạch Trụ | mặt tiền ×4, đài phun + nước, trụ dịch chuyển + vòng, medallion, đèn, ghế, cây, chậu hoa, tượng | **sàn lát thành**, **nền xa thành**, đèn sáng (nên có) | Dựng được với placeholder; **chặn phát hành** |

**Nhân vật (chặn phát hành):**
- Người chơi nam/nữ chỉ có 1 ảnh tĩnh → cần idle + đi 4 hướng.
- 19 mục Đợt A: 13 NPC có ảnh riêng; 3 cần vẽ lại (`bia_free`, `sq_skill` trùng ảnh; `sq_pillar` đang là khối pha lê); 2 NPC chưa có ảnh (`sq_exchange`, `sq_warehouse`); `sq_mailbox` là vật thể (hòm thư), vẽ thành prop.
- Idle NPC: nên có, có thể để 1.0.z.

**Không chặn:** HUD (06), menu (08), icon (09), FX trận (07), login/intro (10), atlas 160 linh thú.

Đơn hàng GPT đầy đủ (chặng 1–5 chặn v1.0.0): [`gpt-redo/09-v1.0.0-full-redo-prompt.md`](gpt-redo/09-v1.0.0-full-redo-prompt.md), ảnh tham chiếu ở `gpt-redo/refs-v1.0.0/`.

**Sửa 2026-10-21 (lượt sau):** bổ sung trạng thái `unused` và trả lại `sq_pillar`, `ship_pillar` (xem trên); số liệu bảng §1 đã cập nhật.
