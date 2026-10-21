# Prompt bổ sung ĐỘ PHONG PHÚ cho kit batch-11 (Hoang Mạc, Núi Phong Thạch, Lăng Mộ và các kit sau) — 2026-10-16

Dán nguyên khối dưới đây vào đầu phiên của Gemini, kèm Phần A của `hd2d-maps-75-gemini-prompt.md` và `hd2d-batch-11-next-kits-prompt.md`.

```text
VẤN ĐỀ: các kit batch-11 hiện quá nghèo. Rừng (batch-01) có 71 asset, batch-02..09 có 26–138 asset mỗi batch; Hoang Mạc có 18, Núi Phong Thạch 19, Lăng Mộ 11. Một map HD-2D Octopath cần dựng được địa hình nhiều tầng bằng nhiều biến thể, không phải 1 tile + vài prop lặp lại. Dựng thử cho thấy: sàn lặp lộ lưới, decal là hình chữ nhật cạnh cứng, prop không dính đất, backdrop chỉ một mảnh, không có chuyển tiếp.
Nhiệm vụ: BỔ SUNG đủ số lượng và độ đa dạng như kit Rừng, tự vẽ bằng công cụ tạo ảnh (không code vẽ nội dung), giữ mọi quy tắc seam/mép trên/front-facing đã có. Nộp lại cả kit (asset cũ giữ nếu đạt, thêm asset mới).

SỐ LƯỢNG TỐI THIỂU MỖI KIT (đếm asset thật, không tính contact sheet, qa, palette):
A. Sàn tile 512² xy seamless: 6 (2 loại chủ đạo × 3 biến thể khác hoa văn nhưng cùng bảng màu, + 1 sàn đặc biệt). Mỗi cặp tile cạnh nhau phải ghép được, độ sáng viền/giữa ≤ 3.
B. Decal chuyển tiếp mép mềm (alpha mềm bằng chấm lẻ/vụn, KHÔNG hình chữ nhật, KHÔNG tile vuông): 8 — gồm 4 mép thẳng (trên/dưới/trái/phải) và 4 góc/vệt loang tròn bất quy tắc, giữa sàn chủ đạo A1 ↔ A2 và sàn ↔ nền phụ. Kích thước ≥ 256, viền răng cưa hữu cơ, nửa trong suốt dạng chấm.
C. Decal bề mặt rải trên sàn (không chân, nằm phẳng): 10 — vết nứt, vũng, mảng cát/sỏi/rêu/tuyết, dấu chân, vệt máu cũ, lá/mảnh vỡ, vòng ma thuật mờ… mỗi cái 1 hình riêng, mép bất quy tắc.
D. Prop nhỏ rải nền (cao < 0.6 đơn vị): 14 — ≥ 3 biến thể mỗi loại chính (đá nhỏ, cỏ/bụi, sỏi, xương, mảnh vỡ, hoa/nấm hợp chủ đề…).
E. Prop vừa (0.6–1.5 đơn vị): 12 — ≥ 2 biến thể mỗi loại (đá, bụi cây/xương rồng/bia, hàng rào, thùng, cột gãy, đống gạch…).
F. Prop lớn / điểm nhấn (1.5–3 đơn vị): 8 — cây lớn tách canopy/trunk (mỗi cây 2–3 mẫu khác hình), tảng đá lớn, cột, tượng, lều/công trình nhỏ, vách đá (có chân đất và bóng chân).
G. Cấu trúc bản đồ (mỗi cái chỉ 1 thành phần): cổng vòm, cổng dịch chuyển dormant/active (front-facing), tường chắn, bậc thang, cột trụ, 2 mẫu cầu/lối đi/khe nếu kit yêu cầu: tối thiểu 8.
H. Backdrop xa nhiều lớp (mỗi lớp 1024×384 lặp X, 64 px/đv): 3 — trời+xa, giữa, gần; trần/đỉnh mép trên hữu cơ ≥ 8 px alpha, không cắt phẳng; 3 lớp dựng chồng không hở; MÀU 3 lớp cùng gam để dựng không nhòe vệt. Thêm 2 mẫu dải nền (chân backdrop → sàn) đổ dốc tối 40–60% để chuyển tiếp chân trời.
I. Hoạt họa/FX 4 khung: 5 — lửa/đèn/ma trơi/nước/bụi hợp chủ đề, spawn marker, vòng rune; lề ≥ 8 px mỗi khung, dịch ≤ 1 px giữa khung.
J. Chân đất và bóng: mỗi prop từ nhóm E–G phải kèm 1 decal contact-shadow nhỏ riêng (alpha tối mềm dạng chấm, ≥ 3 cỡ chung cho cả kit: nhỏ/vừa/lớn) để dựng gắn vật vào đất. Tổng 6 decal bóng.
Tổng: ≥ 70 asset mỗi kit.

ĐA DẠNG BẮT BUỘC: mỗi nhóm D–F có ≥ 3 hình dáng khác nhau rõ rệt (không phải cùng một hình đổi màu/lật gương). Bảng màu chung của kit ≤ 48 màu/asset nhưng palette kit tối đa ~64 màu; sàn A1 và A2 phải cùng sắc độ (chênh độ sáng trung bình ≤ 12/255) để không bị "mảng lệch màu". Mọi prop màu nhấn (cồn cát, đá đỏ…) phải cùng gam với sàn, không cam/hồng tách biệt.

CHI TIẾT THEO KIT:
HOANG MẠC (đã có: sand-floor 01/02, sandstone-floor, monster-bones, cactus 01/02, boulder-01, ruins-pillar/wall, nomad-tent, ancient-stele, sand-mound, arch-gate, portal, spawn, dunes-wall-far):
 + sàn: cát mịn 3 biến thể, cát nứt khô 2 biến thể, sa thạch gạch cổ 1; decal mép cát↔sa thạch, cát↔đá nứt; vệt cát gió; dấu chân; xương rải.
 + prop: 3 loại xương rồng thêm (cao/thấp/chết), 3 đá sa thạch hình khác, cọc lều/lò than/bao vải/thùng gỗ du mục, 2 cột phế tích gãy khác hình, tượng nhân sư/thú đá đổ, giếng cạn, lều thêm 2 mẫu, vại gốm vỡ, kén cỏ khô (tumbleweed), đụn cát 3 cỡ (cùng màu sàn!), mỏm đá đỏ có chân, bộ xương rồng chết, cây chà là khô (tách tán/thân).
 + backdrop 3 lớp: trời hoàng hôn + obelisk xa; đụn cát giữa; đá lớn gần; dải chân backdrop đổ dốc tối.
NÚI PHONG THẠCH (đã có: rock-floor, gravel-floor, grass-snow-floor, edge-decal, peaks-wall-far, arch-gate, portal, campfire, spawn, bridge repeat/broken, fence, signpost, tent, pine trunk/canopy, pillar, cliff):
 + sàn: đá nứt 3 biến thể, sỏi 2, cỏ khô tuyết 2, tuyết dày 1; decal mép đá↔sỏi↔tuyết↔cỏ, tuyết loang, vệt băng, vũng nước đóng băng.
 + prop: thông 3 mẫu hình khác (cao, thấp, chết), bụi gai núi, đá tảng phủ tuyết 3 mẫu, cột đá gió bào 2 mẫu thêm, cột băng, hang/cửa hầm nhỏ, cọc có cờ vải, thùng/rương leo núi, đống gỗ chụm, biển báo 2 mẫu, lều 2 mẫu thêm, mỏm vách đá CÓ chân đất và bóng, bậc đá lên dốc, cây cầu: đoạn lặp, trụ đầu cầu 2 phía, đoạn đứt, VÀ 2 mẫu KHE NỨT/VỰC (decal tối, mép đá lởm chởm, rộng ≥ 512) để cầu bắc qua.
 + backdrop 3 lớp: đỉnh núi xa mờ sương; sườn núi giữa; vách đá gần có thông; chân dốc tối.
LĂNG MỘ (đã có chỉ 11 asset: brick-floor, graveyard-dirt, edge-decal, gravestone 01/02, sarcophagus, lantern-spirit, arch-gate, portal, necropolis-wall-far): nâng đủ nhóm A–J: bia mộ 5 mẫu, thập tự/thiên thần đá, cổng sắt hàng rào, tường gạch vỡ, nấm mồ, quan tài hở, đèn hồn ma, cây chết xoắn, rễ lộ, xương, sương cục bộ, đất nứt phát quang.
Kit sau (Đảo Ác Mộng…) áp dụng ngay khung A–J này, không nộp dưới 70 asset.

CHẤT LƯỢNG VẼ (so với ảnh mẫu batch-01/05/09 đính kèm):
 - Tả thực pixel-HD kiểu Octopath: tối thiểu 3 sắc độ sáng-tối + 1 điểm sáng rìa mỗi khối; có chi tiết bề mặt (nứt, vân, rêu/sạn, vải nhăn), không phẳng, không biểu tượng đơn giản.
 - Mỗi prop có chân tiếp đất tự nhiên (cỏ/sỏi/cát bám quanh chân) hoặc đi kèm decal bóng; không để đáy cắt phẳng.
 - Vẽ cùng ánh sáng: nguồn sáng từ trên-trái cho toàn kit; bóng đổ sang phải-dưới; màu bóng cùng gam (không đen thuần).
 - Mỗi asset có tối đa 1 thành phần liên thông (trừ decal), không pixel lạc, lề ≥ 8 px, alpha nhị phân (trừ decal mềm nếu ghi rõ: vẫn dùng chấm nhị phân, không bán trong suốt).

NỘP (mỗi kit): batch-11-<kit>/ gồm final.png mỗi asset, contact-sheet.png (kèm nhãn), manifest.json, palette.json, qa.json (đủ seam_x_max/seam_y_max, luma viền/giữa, mask diff portal, row-jump, số thành phần, số màu), review.md (xem từng ảnh, nêu điểm yếu), và BẮT BUỘC dựng thử scene <kit>_hd2d trên engine với 3 ảnh chụp camera 0.15/0.5/0.85 + ảnh phóng 2× vùng chuyển tiếp sàn/decal, backdrop/sàn, chân prop. Claude sẽ nghiệm thu bằng ảnh và đo; báo số không thay cho ảnh.
```

Ghi chú nội bộ (không gửi Gemini): quy mô ~70 asset × 17 kit ≈ 1.200 asset; nếu quá nặng, ưu tiên A, B, C, F, H, J trước (sàn, decal mềm, bóng, backdrop nhiều lớp) vì đây là những thứ làm map xấu hiện nay.
