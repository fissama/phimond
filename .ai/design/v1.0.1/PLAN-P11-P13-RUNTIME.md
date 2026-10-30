# Áp P10/P11/P13 vào runtime v1.0.0 (2026-10-30)

Chủ dự án chốt: các phase đã chốt (P10 danh mục loài, P11 chỉ số, P13 kỹ năng/bảng hệ/hợp đồng trận đấu) phải được áp vào v1.0.0. Tài liệu này ghi cái đã áp, cái giản lược có chủ ý và nợ.

## Đã áp

**Dữ liệu** (sinh bằng `tools/p01/apply_p11_p13.py --plan <thư mục phases>`, chạy lại được, idempotent)
- `data/pets/species.json`: 160 loài (id `species_NNNN`) với base, growth (milli), MP, Sao, lớp, vai trò, pool kỹ năng gốc, tỉ lệ bắt theo Sao.
- `data/skills/skills.json`: 97 kỹ năng (loại, mục tiêu, MP, hồi chiêu, cấp học, hệ, uy lực, hiệu ứng, kế thừa theo Race, kỹ năng riêng loài). `statuses.json`: 14 trạng thái (thêm `slow`).
- `data/balance/rules.json`: 6 ô kỹ năng, trần cấp theo Sao 60/70/80/90/100, bảng hệ có `neutral`.
- `data/pets/legacy_species.json`: bảng id loài cũ → chuẩn, chỉ dùng để chuyển save cũ. Map, nhiệm vụ, công thức đã đổi sang id chuẩn.

**Server (Go)**
- Chỉ số P11: sáu chỉ số hp/atk/mag/def/spd/status_resistance, `grown = base + floor(growth × hệ_số_bậc × (cấp−1))`; bậc D…Perfect rút độc lập theo bảng xác suất khi tạo pet/bắt/sinh; quái hoang toàn bậc B; trần cấp theo Sao; lên cấp không hồi HP/MP.
- Kế thừa P11: tín dụng dòng dõi Q là số hữu tỉ chính xác (`big.Rat`), thưởng `z` tìm bằng so sánh số nguyên (có test cực đại), cấp bố mẹ ≤ 20 không sinh tín dụng.
- Chiến đấu P13: công thức `floor(công × uy lực × 100/(100+DEF) × hệ × bạo kích)`, trúng 95% (mù −20 điểm), bạo kích 5% ×1,5, bảng hệ Hỏa>Phong>Địa>Thủy>Hỏa và Quang↔Ám (×1,25/×0,8), hồi chiêu `R+C+1`, khống chế (ngủ/hóa đá/hỗn loạn) tiêu ở hành động kế + miễn nhiễm một vòng, trói/câm lặng chặn đúng kênh, buff/debuff theo phần trăm (dương mạnh nhất + âm mạnh nhất, chặn ±50%), khiên, hồi theo nhịp, độc/cháy, phản kích, kháng trạng thái `0,8·S/(S+100)` với một phép thử Bernoulli chính xác, thứ tự theo SPD hiệu lực, hòa theo hạng ngẫu nhiên cố định.
- Học/nâng kỹ năng: 6 ô, đòn thường không chiếm ô, học = 20 + 10×cấp học, học lại kỹ năng cũ còn 20%, thay kỹ năng khi 6/6 (quên mất bậc nâng), nâng bậc 2/3 giá 3×/6× với cổng cấp. Intent mới `pet.skill_upgrade`; `pet.learn` có `replace_id`. Nút "Phòng thủ" bị bỏ (P13 không có).
- Chuyển save cũ `MigrateLegacy` (chạy khi nạp nhân vật, idempotent): đổi id loài, đặt mọi bậc về B, bỏ kỹ năng cũ (id không còn), tính lại chỉ số giữ cấp và tỉ lệ HP/MP, hủy trận đang dở.
- Bình thuốc: Hồi 120 HP, Hồi 30 MP (cho khớp thang HP mới).

**Client**
- Protocol: `skill_ranks`, `learned`, `inherited_pool`, `grades`, `status_resistance`…; đơn vị trận có `buffs`, `shield`, `cooldowns`; sự kiện có `detail`; bỏ `defend`.
- Trận đấu: danh sách kỹ năng có MP theo bậc, thời gian chờ, mô tả; trạng thái/buff/khiên hiển thị dưới thanh máu; nhật ký có bạo kích/khắc hệ/khiên hấp thụ/phản kích.
- Học kỹ năng ở NPC: danh sách đã học (nâng bậc), có thể học (giá, học lại, thay khi đủ 6 ô). Chi tiết linh thú: sáu chỉ số, bậc (sau giám định), kỹ năng kèm bậc. Bệ chọn pet đầu: thanh chỉ số mới.
- Ba pet khởi đầu: Tiên Chưởng (`species_0021`, Thổ, phòng thủ), Sa Hạt (`species_0109`, Thổ, phép), Xích Ưng (`species_0071`, Hỏa, vật lý). Chúng **không còn biết sẵn kỹ năng nào** (P13: pet mới 0/6); học đòn đầu ở thầy Bìa Rừng (30 vàng, người chơi mới có 100 vàng).

**Kiểm tra**: Go test (character, content, transport, persistence, world) xanh; vitest 27; Playwright chromium smoke 13 bài (thêm bài học kỹ năng thật).

## Giản lược có chủ ý (đã ghi nợ)
Xem D26–D32 trong `DEBT.md`.
