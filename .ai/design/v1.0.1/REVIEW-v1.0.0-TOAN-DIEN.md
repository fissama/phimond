# Review toàn diện Phimond v1.0.0 (kèm sửa v1.0.1) — góc nhìn người chơi khó tính

Ngày 2026-10-22. Chơi lại từ đầu bằng tài khoản mới, chất lượng Trung bình, 1280×720 và 430×932:
đăng ký → Triệu Linh Điện → chọn bệ → Bìa Rừng → menu (Linh thú, Túi, Nhiệm vụ, Cài đặt) → NPC → Rừng Sâu →
Hoàng Môn → Quảng Trường → trụ đá; thêm một tài khoản ban đêm đánh trận 2 quái bằng Tự động.
Số liệu trận lấy từ mô phỏng 200 trận mỗi ô bằng engine server thật (pet khởi đầu Lv1, chỉ bấm Tự động).
Ảnh: `review-v1.0.0-full/`.

**Không kiểm được:** máy không GPU nên không chấm độ mượt; chưa thử iPhone/Safari, mạng yếu; chưa soi lại chu kỳ đi bộ.

## Kết luận một câu

Nhìn thì đã ra HD-2D (Quảng Trường đẹp nhất), nhưng **vòng chơi lõi đang hỏng: người chơi mới không thắng nổi trận nào**, và mọi thứ quanh trận đấu (nhiệm vụ, thưởng, hồi máu, phát triển pet) quá mỏng để giữ người chơi quá 10 phút.

## Chấm điểm (thang 10, so với game gốc / Octopath / game mobile hiện nay)

| Hạng mục | Điểm | Vì sao |
|---|---|---|
| Đồ họa thế giới | 6.5 | Asset đẹp, Quảng Trường sống động; nền đất ô vuông, thảm đỏ chữ nhật, sảnh có khoảng đen. |
| HUD / UI | 5 | Năm kiểu khung khác nhau, chữ tràn nút, cài đặt bị cắt, chat mất ở màn dọc. |
| Combat | 3 | Không thắng được; pet không có kỹ năng; trận dài, ít phản hồi. |
| Dẫn dắt người mới | 4 | Có gợi ý chữ và mục tiêu, nhưng trận đầu thua ngay. |
| Nội dung / lý do chơi tiếp | 2.5 | 4 nhiệm vụ, NPC một câu, nhiều điểm "chưa mở". |
| Cảm giác "game thật" | 4 | Chạy ổn, không lỗi console, nhưng thiếu âm thanh, thiếu phần thưởng có cảm xúc. |

## P0 — phải sửa trước khi cho ai chơi

**P0-1. Pet khởi đầu không thắng được quái hoang.** (Mô phỏng 200 trận/ô, auto.)

| Map | 1 quái | 2 quái | 3 quái |
|---|---|---|---|
| Bìa Rừng | thắng 37–62% (tùy pet), ~8–9 lượt | **0%** | **0%** |
| Rừng Sâu | **0–1%** | **0%** | **0%** |

Với luật mới (chỉ ra 2–3 quái), **người chơi mới thua 100% trận ở map đầu tiên**. Trong lần chơi thật: Xích Ưng bị 2 Hoa Loa hạ, bị đưa về điểm hồi sinh. Mỗi đòn của pet chỉ ~7 sát thương trên 60 HP quái (~12%/đòn), quái đánh lại ~8. Đây là lỗi do đợt 1v3 vừa làm phơi ra, nhưng cả 1v1 cũng đã chỉ ngang cơ.
*Sửa (chọn một hoặc kết hợp, cần bạn quyết):*
- Quái trong encounter nhiều con yếu hơn: HP/ATK × 0.5 (2 con) / × 0.4 (3 con), như Octopath dùng "đàn quái nhỏ".
- Tăng sát thương nền (`damage_scale` 0.6 → ~1.2) để trận 1v1 còn 3–4 lượt, 1v3 còn 5–7 lượt.
- Pet khởi đầu có sẵn 1 kỹ năng tấn công diện rộng hoặc mạnh (hiện nút Kỹ năng ghi "Chưa có").
- Bìa Rừng tạm giữ 1 quái cho tới Lv3–5 (encounter_weights theo map).
- Mục tiêu nghiệm thu: pet Lv1 auto thắng ≥90% ở Bìa Rừng, ≥60% ở Rừng Sâu, trận 4–8 lượt.

**P0-2. Chạy trốn vẫn mất máu và không có hồi máu dọc đường.** Đi Bìa Rừng → Hoàng Môn chỉ chạy trốn, tới nơi pet còn 18/58 HP. Không có cảnh báo máu thấp, không hồi dần, chỉ hồi ở Kiểm Lâm Lio (map đầu). Người chơi vào thành với pet sắp chết mà không biết.
*Sửa:* Chạy luôn đi trước (ưu tiên lượt) hoặc tỉ lệ chạy thoát không bị đánh; cảnh báo HP <30% trên HUD (viền đỏ, nháy); thêm điểm hồi ở Hoàng Môn/Quảng Trường (Y Sư Selka đã có tên).

**P0-3. Thua trận lướt qua quá nhanh.** Bảng "Thất bại" tự đóng sau 1.7 s, người chơi bị dịch chuyển về Bìa Rừng; chỉ còn một dòng chat. Không ai giải thích vì sao thua, nên làm gì.
*Sửa:* Thua thì giữ bảng tới khi chạm, kèm gợi ý ("Hồi phục ở Kiểm Lâm Lio", "Bắt thêm linh thú", "Dùng Thuốc Rễ Dại"). Thắng/bắt mới tự đóng.

## P1 — thấy ngay trong 5 phút đầu

**Combat**
- Nút **Kỹ năng "Chưa có"** chiếm vị trí đẹp nhất mà không dùng được → ẩn khi chưa có, hoặc cho pet khởi đầu một kỹ năng.
- **Khung tên quái bị gãy dòng** ("Hoa Loa / A", "Hoang / dã") ở màn ngang khi có 2–3 quái → bỏ chữ "Hoang dã", hiện "Lv N" (cần server gửi level, D13).
- **Phản hồi đòn đánh yếu**: chỉ số trôi và lắc nhẹ; không có tia chém, chớp trắng mục tiêu, âm thanh. Octopath/game gốc đều có hiệu ứng theo hệ. Đề xuất bộ VFX tối thiểu: chém (vật lý), quả cầu (phép), lá chắn (phòng thủ), vòng ấn (bắt).
- **Nền trận vẫn là thế giới làm mờ** (chưa có ảnh nền vẽ theo map, đã gửi prompt ở `battle-bg/PROMPTS.md`). Trông như popup, không phải "đấu trường".
- **Tự động** không có tốc độ ×2, không hiện số lượt còn lại; người chơi sẽ muốn bật auto rồi xem nhanh như mọi game mobile.
- Log trận (thanh xanh đậm) khác hẳn chat ngoài thế giới (xanh nhạt) → một ngôn ngữ khung.
- Bóng ma của thẻ HUD thế giới (thẻ người chơi) lộ mờ phía sau thẻ pet ở góc trên trái.

**HUD / UI**
- **Năm kiểu khung cho năm bảng**: Linh thú (khung lá xanh), Túi (da nâu), Nhiệm vụ (giấy da), Cài đặt/Trụ đá (sắt xám), Hội thoại NPC (xanh đậm viền vàng). Game gốc và Octopath dùng **một** bộ khung. Chọn một (đề xuất khung xanh đậm viền vàng giống hội thoại), các bảng chỉ khác biểu tượng tiêu đề.
- **Mỗi bảng có 3 cách đóng** (X, "Trở về", "Đóng") → giữ X và Esc; "Trở về" chỉ khi có cấp con.
- **Cài đặt bị cắt đáy**: hai nút cuối nằm dưới khung, không thấy thanh cuộn; đoạn giải thích chất lượng dài như tài liệu kỹ thuật.
- **Chữ tràn nút ngữ cảnh**: nút bầu dục phải dưới đổi thành "Hỏi chuyện", "Dùng trụ" nhưng chữ vượt khỏi nút.
- **Màn dọc (điện thoại) mất hẳn khung chat**, tên NPC bị cắt ở mép phải, theo dõi nhiệm vụ đè lên cảnh. Đây là thiết bị chính (iPhone).
- **Bản đồ nhỏ** chỉ là vài chấm trên nền đen: không thấy đường, cổng, NPC. Hoặc làm thật (đường, cổng, chấm NPC), hoặc bỏ để lấy chỗ.
- Tên **mọi NPC luôn hiện** → Quảng Trường bị chồng chữ (Huấn Luyện Viên Elin đè người khác). Chỉ hiện tên khi gần hoặc khi có việc (dấu "!"/"?").
- Thanh dưới (D-pad, chat, 2 nút) chiếm ~19% chiều cao màn ngang, dải đen trơn. Game gốc để chat nổi trên cảnh.

**Thế giới**
- **Triệu Linh Điện**: 1/3 dưới màn hình là khoảng đen dưới lan can; mở đầu game mà trông như chưa vẽ xong.
- **Nền đất rừng** vẫn là các ô chữ nhật có mép thẳng, ban đêm còn lộ rõ hơn (N2 cũ chưa sửa).
- **Hoàng Môn**: gạch đỏ + thảm đỏ là hình chữ nhật dán phẳng (N4 cũ).
- **Rừng Sâu** khác Bìa Rừng chủ yếu ở độ tối; cần dấu hiệu riêng (rễ lớn, sương, đá rêu, ánh sáng tia) để người chơi cảm thấy "đi sâu hơn".
- **Quái trên map** (nấm vàng, nấm tím) trông như vật trang trí; không biết cái nào đụng vào sẽ đánh. Thêm nhún nhảy, mắt, bóng, hoặc biểu tượng nhỏ trên đầu.
- Quảng Trường đã tốt nhất: đông vui, đồng bộ; còn cái cây giữa quảng trường trông như đặt nhầm chỗ.

## P2 — giữ người chơi sau 10 phút

- **Chỉ 4 nhiệm vụ** (tới Rừng Sâu, bắt 1, thắng 1, phối giống). Bảng Nhiệm vụ mở ra trống trơn. Cần chuỗi chính 8–10 bước nối 5 map, mỗi NPC có việc (Thợ Săn Rowan: diệt 5 nhện; Người Hái Nấm Tuli: nhặt nấm; Y Sư Selka: hồi máu/bán thuốc).
- **Thưởng nghèo cảm xúc**: thắng chỉ có dòng chat "+vàng +EXP". Game gốc có tiếng "ting", số EXP chạy, rơi đồ. Thêm rơi vật phẩm theo quái và bảng thắng đẹp 1–2 s.
- **Linh thú**: bảng chỉ có một dòng "HP · MP · Đang theo"; không xem được chỉ số, hệ, kỹ năng, kháng. Đây là game nuôi thú: màn chi tiết pet phải là màn đẹp nhất.
- **Túi đồ**: không có mô tả, không có nút Dùng ngoài trận.
- **Chọn pet khởi đầu**: chỉ có một câu mô tả; thiếu hệ, chỉ số, kỹ năng để so sánh 3 con.
- **NPC**: vẫn một câu thoại cố định; chân dung là sprite thu nhỏ, không có tranh bán thân như game gốc/Octopath.
- **Âm thanh**: hoàn toàn chưa có (nhạc nền theo map, tiếng bước, tiếng đánh, tiếng nút). Thiếu âm thanh là thứ người chơi nhận ra đầu tiên.
- 4 điểm "chưa mở" (Hội bang, Sàn giao dịch, Kho, Hòm thư) và Đấu trường vẫn là ngõ cụt (D1).

## Đã tốt hơn v1.0.0 lần đầu (giữ)

- Mira đứng giữa vòng triệu hồi, nhìn thấy rõ; có gợi ý chữ và khung "Mục tiêu" cho người mới.
- HUD trái gọn: pet HP/MP/EXP + Lv người chơi.
- Ngày/đêm có hồn hơn; Quảng Trường, Hoàng Môn đúng chất HD-2D.
- Trận ngang có đội hình 2–3 quái, chọn mục tiêu, nút Tự động ở đầu; không popup chặn.
- Không có lỗi console trong cả chuyến đi.

## Thứ tự làm đề xuất

1. **Cân bằng trận** (P0-1) — chốt hướng sửa, đo lại bằng mô phỏng tới khi đạt mục tiêu nghiệm thu.
2. Chạy trốn + cảnh báo HP + điểm hồi ở thành (P0-2), bảng thua có gợi ý (P0-3).
3. Thống nhất **một** bộ khung UI; sửa cài đặt bị cắt, chữ tràn nút, chat ở màn dọc.
4. Ẩn nút kỹ năng khi trống, sửa khung tên quái, thêm VFX tối thiểu và tốc độ ×2 cho auto.
5. Âm thanh cơ bản (2 nhạc nền + 10 hiệu ứng).
6. Màn chi tiết pet + chọn starter có chỉ số.
7. Chuỗi nhiệm vụ 8–10 bước và thoại NPC theo tiến độ.
8. Đồ họa: nền đất cong tự nhiên, sảnh không khoảng đen, Rừng Sâu có bản sắc, quái trên map dễ nhận.
