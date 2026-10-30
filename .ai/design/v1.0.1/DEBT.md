# Nợ (debt) sau v1.0.1

Các mục đánh giá gameplay thuộc Phase sau, giữ lại ở dạng nợ. Mỗi mục: nguồn → việc cần làm → khi nào làm.

| ID | Nguồn | Việc | Khi nào |
|---|---|---|---|
| D1 | G4 | 4 NPC/điểm "chưa mở" (Hội bang, Sàn giao dịch, Kho, Hòm thư) và Đấu trường vẫn là biển báo. Chức năng thật: Phase guild, giao dịch, kho, thư, đấu trường. Tạm thời quyết định ẩn hoặc giữ biển báo. | Phase tương ứng |
| D2 | G4, T1 | Nội dung: mỗi NPC 2–3 câu thoại đổi theo tiến độ; thêm 2–3 nhiệm vụ nối Hoàng Môn và Quảng Trường. | Phase nội dung |
| D3 | T4 | An toàn đụng quái: vùng an toàn quanh NPC và lối chính, báo hiệu quái trước khi vào trận. Phải sửa ở server (ngoài phạm vi client). | Phase cân bằng |
| D4 | review | Hiệu năng và độ trễ trên iPhone 17 Pro Max (Safari), macOS Safari, thang chất lượng thấp/vừa/cao. | Trước khi public |
| D5 | L3 | Người đi đường và động vật chưa có tương tác khi chạm. | Phase sau |
| D6 | G3 | Di chuyển vẫn theo lưới 4 hướng, không đi chéo, tốc độ cố định. Cân nhắc đi chéo và tăng tốc khi giữ. | Phase cân bằng |
| D7 | HUD | Mũi tên nhún trên bệ đá cho người mới (cần API marker trong engine). Hiện thay bằng khung Mục tiêu + nút Chọn nháy. | Sau v1.0.1 |
| D8 | HUD | Cho người chơi tự đặt lại vị trí điều khiển; chat có nội dung thật (kênh Thế giới/Khu vực/Đội/Riêng chờ server). | Phase xã hội |
| D9 | HUD | Khung ảnh riêng cho bản đồ nhỏ, khung mục tiêu, chat (hiện dùng CSS thuần, không có sprite duyệt). Xem `GPT-REMAINING.md` mục UI. | Khi GPT có lượt |
| D10 | N2 | Chỉnh fringe đường đất để hết lộ nhịp ô vuông; có thể cần thêm biến thể từ GPT. | Sau khi duyệt ảnh trong cảnh |
| D11 | starter | 3 loài khởi đầu mới dùng chỉ số mượn từ Hoa Tinh/Sơn Chu/Lam Lang; chưa có chỉ số, kỹ năng P11/P13 riêng. Pet Lv1 đấu quái Bìa Rừng chưa cân bằng. Server vẫn dùng 14 loài cũ cho quái. | P11 |
| D12 | HD-2D | Ánh sáng thật theo đèn (hiện là quầng cộng sáng + chỉnh màu toàn cảnh), bóng đổ theo giờ, thời tiết (mưa, sương), nước phản chiếu. Chưa đo hiệu năng bloom trên iPhone/Safari. | Sau khi đo D4 |
| D13 | Combat | Trận đấu là cảnh DOM trên nền cảnh thế giới làm mờ, chưa phải diorama 3D riêng; chưa có hiệu ứng kỹ năng, chưa có tên Lv cho quái hoang (server không gửi level trong BattleUnit). | Sau v1.0.1 |
| D14 | HUD | EXP cần lên cấp (cấp × 25) đang hard-code ở client theo `data/balance/rules.json`; nên server gửi `xp_next` trong snapshot. | Cùng đợt chỉnh server |
| D15 | Combat | Encounter 3 quái làm pet mới có thể chết trước khi kịp Chạy; thành phần encounter theo party, AoE, mục tiêu đồng đội cho 3v3 chưa có. Xem `COMBAT-HUD-SPEC.md` cờ 1–4. | Phase cân bằng / PvP 3v3 |
| D16 | Âm thanh | Âm thanh hiện tổng hợp bằng WebAudio (đánh, phép, thắng/thua, tiền, nút); chưa có nhạc nền theo map và bộ âm thanh vẽ riêng. | Khi có âm thanh |
| D17 | NPC | Hội thoại dùng sprite NPC thu nhỏ làm chân dung; game gốc/Octopath dùng tranh bán thân. | Khi GPT có lượt (GPT-REMAINING 14) |
| D18 | Cân bằng | Hệ số `wild_scale`/`pack_scale`/`damage_scale` chỉnh bằng mô phỏng auto (`balance_test.go`), chưa thử với người chơi thật và kỹ năng trạng thái. Pet khởi đầu biết sẵn đòn hệ (lệch learn_level 2). | Phase cân bằng |

## Bổ sung 2026-10-29 (chủ dự án chốt: để các phase sau quyết định)

| ID | Nguồn | Việc | Khi nào |
|---|---|---|---|
| D19 | G4 | Hội bang, Sàn giao dịch, Kho, Hòm thư, Đấu trường: giữ nguyên biển "chưa mở" ở v1.0.x. Thiết kế và chức năng thật do các phase sau quyết định (guild, giao dịch, kho/thư P19, đấu trường PvP). Không làm thêm ở bản này. | Các phase sở hữu từng hệ |
| D20 | Combat | Trận 3v3 (3 pet ra trận cùng lúc) và quyền đổi pet giữa trận: P02/P07. Đội hình hiện chỉ để chọn **pet ra trận (vị trí đầu)** và 2 pet dự bị mang theo (`character.party`, intent `pet.party_set`, tối đa 3 con, pet retired không dùng được). Tên `party` trùng với "party người chơi" (tối đa 3 người) của P07: đổi tên khi làm P07, chưa đổi ở v1.0.x. | P02 / P07 |
| D21 | Server | Snapshot chưa gửi `xp_next` (EXP cần để lên cấp) và cấp quái trong BattleUnit đủ cho mọi pha; client vẫn dùng công thức cứng cấp × 25 (D14). Phase sau quyết định hợp đồng dữ liệu. | Phase sau |
| D22 | Huyết Chiến Đài | Chỉ có cảnh và lối vào ở v1.0.x. Logic (giờ mở cố định hằng ngày, vào qua nhiệm vụ phụ ở Quảng Trường) thuộc phase nhiệm vụ/sự kiện. | Phase nhiệm vụ |
| D23 | P11 | (ĐÃ ÁP 2026-10-30, xem `PLAN-P11-P13-RUNTIME.md`; giữ dòng để truy vết) Áp P11 cho pet đang chạy: mô hình chỉ số của server vẫn là mô hình cũ (strength/agility/... + chất lượng/tăng trưởng ngẫu nhiên). Danh mục P11 (160 loài, base + tăng trưởng + MP) đổi cả hệ và vai trò của 3 loài khởi đầu (ví dụ Tiên Chưởng thành hệ đất, vai tank), nên việc áp phải cùng P13 (kỹ năng) và cân bằng lại quái. Chờ quyết định phạm vi của chủ dự án (xem tin nhắn 2026-10-29). | P11 + P13 runtime |
| D24 | Nhạc | Bộ phát nhạc nền đã có (`music.ts`); file nhạc do chủ dự án tải (CC0) hoặc tạo bằng MiniMax theo `AUDIO-MUSIC.md`. Chưa có bài cho Triệu Linh Điện và Hoàng Môn. | Khi có file |
| D25 | Đo | Đo hiệu năng iPhone/Safari: chủ dự án tự đo sau khi hoàn thiện (thay D4 phần "ai đo"). Lớp tiền cảnh mờ (FgBlurPass) và bóng vẽ là phần mới cần đo. | Sau hoàn thiện |

## Bổ sung 2026-10-30 (áp P10/P11/P13 vào v1.0.0)

| ID | Nguồn | Việc | Khi nào |
|---|---|---|---|
| D26 | P15 | `wild_scale` (0,6) và `pack_scale` (1/0,55/0,4) là lớp điều chỉnh **tạm**. Sau P11, trận dài hơn: Xích Ưng ~8 lượt, hai pet còn lại 11–25 lượt ở Bìa Rừng bằng "Tự động" (thắng ≥ 90%). Đường cong quái (cấp, chỉ số, kỹ năng AI) cần P15. `balance_test.go` nới trần lượt tới 25. | P15 |
| D27 | P13 | Hiện chỉ có chiến đấu 1 pet vs 1–3 quái. Các kỹ năng nhắm đồng đội (hồi/khiên/buff đồng đội, hồi sinh, Suy tưởng) tự rơi về bản thân hoặc không dùng được; mục tiêu đồng đội và hồi sinh chờ 3v3. | P02 / P07 |
| D28 | P11/P16 | Trứng và nở trứng chưa có: pet mới chỉ đến từ bắt, khởi đầu và tổng hợp (con sinh ra Lv1, toàn bộ bậc rút mới). Egg/hatch chờ P16. | P16 |
| D29 | P13 | (ĐÃ XỬ LÝ 2026-10-30) Pet khởi đầu 0/6 kỹ năng; nhiệm vụ đầu `first_battle` (nhận ở Lio) tặng một đòn tấn công cấp 1 của loài (Cường kích cho Xích Ưng/Tiên Chưởng, Linh kích Địa cho Sa Hạt) qua trường quest `gift_skill`. Kỹ năng sau đó học ở thầy dạy. |
| D30 | P13 | Nhịp độc/cháy làm tròn theo đơn vị 1/1000 của tấn công nguồn lúc áp; chưa khớp từng chữ số với bảng P13 cho các trường hợp biên. Cần đối chiếu khi có bảng kiểm. | P13 QA |
| D31 | Migration | Save cũ: kỹ năng cũ bị bỏ (không đối ứng 1-1 sang 97 kỹ năng mới), bậc về B, tín dụng dòng dõi 0. Chấp nhận vì chưa có người chơi thật. Phải dừng migration hoặc giữ bảng ánh xạ kỹ năng nếu sau này có dữ liệu thật. | Trước khi public |
| D32 | Client | `viName` và `i18n/vi.json` còn mục cho tên tiếng Anh cũ; tên loài mới đã là tiếng Việt từ catalog. Chưa xóa mục cũ. | Dọn dẹp |
