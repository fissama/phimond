# Kế hoạch đưa v1.0.x lên chất Octopath (2026-10-29)

Nguyên tắc chia việc: **bạn gửi GPT vẽ** những gì ở Phần A; **Claude làm mọi việc còn lại** ở Phần B (duyệt, nạp, code, giao diện, kiểm). Giữ nguyên bố cục và điểm dịch chuyển map đã duyệt ở P12. Không đụng lưới đi của server.

Quy cách GPT: như `GPT-PROMPTS-OCTOPATH.md` (khối chung dán đầu mỗi prompt; một ảnh một lượt; đính kèm ảnh tham chiếu trực tiếp, không zip; nền ma-gen-ta, alpha nhị phân, ≤48 màu).

## Hiện trạng (đã đối chiếu repo)
- **HUD đã sửa (code, bản này):** khi chưa có linh thú (Triệu Linh Điện trước khi chọn bệ) chỉ hiện tấm người chơi, không còn thẻ linh thú trống; ô mục tiêu dời lên cho khỏi hở.
- Đã đủ: nền trận, bộ khung UI, nền/mái thành phố rộng, sàn B, vệt sáng kính, viền hai bên sảnh.
- GPT đã giao 45 ảnh lô S01–S27 (chờ Claude duyệt và nạp). Còn thiếu: 24 dải chạy S23–S24 (người chơi + 6 người đi đường).
- Đã vẽ nhưng chưa nạp: fx 6 hệ (lửa, nước, đất, thú, côn trùng, thực vật), fx triệu hồi, idle 7 NPC (R25–R31).

## Phần A. Gửi GPT vẽ (thứ tự ưu tiên)

### A0. Còn nợ từ lô S01–S27: S23, S24 (24 dải chạy)
Prompt có sẵn trong `GPT-PROMPTS-OCTOPATH.md`. Đây là việc làm game hết "lướt", nên làm trước nhất.

### A1. Hiệu ứng trận (khung 192×192, 6 khung ngang = 1152×192, nền ma-gen-ta)
Đính kèm mỗi lượt: `fx-fire.png` (làm mẫu độ lớn, nhịp khung, bảng màu) và ảnh chiến đấu hiện tại.
- **M01** `fx-wind.png`: gió xoáy xanh ngọc, các đường cắt cong, lá cuốn.
- **M02** `fx-light.png`: tia sáng vàng trắng bùng từ trung tâm, đốm lấp lánh.
- **M03** `fx-dark.png`: khói tím đen cuộn, vài tia tím sáng, mắt đỏ mờ.
- **M04** `fx-neutral.png`: sóng va chạm trắng xám, vòng xung kích (đòn vật lý thường).
- **M05** `fx-hit-spark.png`: tia lửa va chạm trắng vàng, 6 khung bung ra rồi tan.
- **M06** `fx-defeat.png`: linh thú bị hạ: vòng khói trắng xanh bốc lên rồi tan, vài mảnh sáng bay lên.
- **M07** `fx-capture.png`: bắt thú: vòng phong ấn vàng thu lại, tia sáng cuốn vào giữa.

Prompt mẫu (đổi dòng mô tả theo từng mục):
> [Khối chung] Create a 6-frame horizontal strip, each frame 192×192 (total 1152×192), magenta #FF00FF background. Battle skill effect, WIND element: swirling teal-green wind cuts and curved slash lines with a few leaves caught in the spiral, bright white-cyan core. Same scale, frame pacing and palette depth as the attached fx-fire.png: frame 1 small spark, frames 2–4 full size, frames 5–6 dissipating. Effect centered in each frame, no ground, no character, no text.

### A2. Hiệu ứng nền / chuyển động
- **M08** `fx-step-dust.png`: bụi bước chân, 4 khung 128×64 (512×64), nền ma-gen-ta, màu be nhạt, nhỏ dần.
- **M09** `fx-step-grass.png`: cỏ bị đạp, 4 khung 128×64, mảnh lá xanh bắn nhẹ.
- **M10** `animal-birds.png`: một con chim nhỏ bay, 6 khung 128×96 (768×96); làm hai màu (nâu, xanh) thành hai lượt `animal-birds-a.png`, `animal-birds-b.png`.

> [Khối chung] Create a 6-frame horizontal strip, each frame 128×96 (total 768×96), magenta background. A small forest songbird in a flapping flight cycle seen from the side (flying right), wings fully up in frame 1 and fully down in frame 4, body ~40 px long, brown back and cream belly. 1px dark outline, no shadow.

### A3. Hoàn thiện cảnh (tiền cảnh và mảnh nối còn thiếu)
- **M11** `fg-deep-vines.png` (512×384): dây leo rủ và nấm phát sáng xanh lục để làm tiền cảnh mờ ở Rừng Sâu. Đính kèm `fg-forest-branch-a.png` (đã giao) và ảnh Rừng Sâu hiện tại.
- **M12** `fg-gate-banner-edge.png` (384×512): hai cờ xanh huy hiệu mặt trời rủ từ trên, mép lá cờ rách nhẹ, cho tiền cảnh Cổng Cung Điện. Đính kèm `palace-gate.png`.
- **M13** `hall-side-corner.png` (256×400): trụ góc và đầu lan can khép góc trước của sảnh, cùng chất liệu `hall-side-pier.png` và `hall-side-balustrade.png` đã lắp.
- **M14** `hall-outside-roofs-side.png` (512×384): cảnh ngoài tường hai bên sảnh (mái nhà, tháp xa, bầu trời) để lấp phần trống khi nhân vật sát mép. Nền đặc.

### A4. Bộ HUD, viền ô đồ và minimap (để giao diện thành một bộ thống nhất kiểu Octopath)
Hướng chung: khung vàng mảnh hai nét trên nền tối ngả xanh, góc trang trí nhỏ, không tô màu rực; cùng ngôn ngữ với `frame-portrait.png`, `panel-large.png`, `slot-normal.png` hiện có (đính kèm làm mẫu bảng màu) nhưng sạch và đồng bộ hơn. Mọi mục: nền ma-gen-ta ngoài khung, **ruột khung trong suốt** (alpha nhị phân), có đường 9-slice rõ: góc 48 px không co giãn, cạnh lặp được.

Prompt khung chung cho A4 (dán sau khối chung, rồi thêm dòng riêng của từng mục):
> UI frame asset, flat front view (no perspective), thin double gold line border (outer line dark gold, inner line bright gold), small ornate corner pieces, dark navy-teal inside left TRANSPARENT (magenta in the source), crisp pixels, no text, no icons inside, max 48 colors, same gold hue and corner ornament language as the attached references.

- **N01** `hud-player-plate.png` (480×128): tấm thông tin người chơi hiện ra **một mình** khi chưa có linh thú (ở Triệu Linh Điện trước khi chọn bệ): ô tròn nhỏ trái cho huy hiệu cấp, dải tên ở giữa, rãnh EXP mảnh phía dưới, ô vàng nhỏ bên phải. Đính kèm `frame-bars.png`, `badge-level.png`.
- **N02** `hud-pet-plate.png` (480×200): thẻ linh thú: vòng chân dung 128 px bên trái (nửa đè mép khung), tên ở trên, 3 rãnh HP/MP/EXP xếp dọc bên phải, chỗ huy hiệu cấp ở góc dưới vòng. Cùng ngôn ngữ N01 để hai tấm xếp chồng khít nhau. Đính kèm `frame-portrait.png`, `frame-bars.png`, `pet-card.png`.
- **N03** `slot-common.png`, `slot-uncommon.png`, `slot-rare.png`, `slot-epic.png`, `slot-legendary.png` (mỗi ô 96×96): viền ô đồ theo độ hiếm; chỉ khác màu viền và độ tinh xảo (xám bạc, xanh lục, xanh lam, tím, vàng cam có tia sáng ở góc). Ruột trong suốt. Một lượt một ảnh, giữ cùng khung nền. Đính kèm `slot-normal.png`, `slot-rare.png`.
- **N04** `slot-empty.png`, `slot-selected.png`, `slot-locked.png`, `slot-equipped-corner.png` (96×96; riêng `slot-equipped-corner.png` là mảnh huy hiệu nhỏ 32×32 góc trên phải): trạng thái ô. Đính kèm `slot-selected.png`, `slot-locked.png` hiện có.
- **N05** `minimap-frame.png` (384×256): khung minimap, cửa sổ trong suốt chiếm ~80% chính giữa, bốn góc trang trí, một khía la bàn nhỏ ở cạnh trên, bóng đổ nhẹ phía ngoài. Đính kèm `ui-minimap.png` (bản cũ có viền hồng lỗi), `ui-bottombar.png`.
- **N06** `minimap-markers.png` (3 biểu tượng 24×24 trên một dải 72×24, nền ma-gen-ta): chấm người chơi (mũi tên vàng), chấm NPC (kim cương xanh), chấm điểm dịch chuyển (xoáy tím). Viền tối 1 px để đọc được trên nền xanh lá.
- **N07** `panel-frame.png` (192×192, 9-slice, góc 48 px): bảng chung cho menu/túi/nhiệm vụ/cài đặt thay `panel-large`; ruột là nền giấy tối ngả xanh có thể co giãn (không hoa văn lớn), viền vàng hai nét, góc có hoa văn nhỏ. Đính kèm `panel-large.png`, `ornament-corner.png`.
- **N08** `dialogue-frame.png` (1024×256) và `dialogue-nameplate.png` (320×64): khung thoại NPC thấp-rộng nền tối mờ, viền vàng mảnh, phiến tên nhô lên góc trái trên. Đính kèm `dialogue-panel.png`.
- **N09** `chat-frame.png` (768×192, 9-slice) và `chat-tab-normal/selected.png` (160×48): đổi khung chat từ xanh nhạt sang cùng tông tối-vàng của HUD. Đính kèm `chat-panel.png`, `chat-tab-normal.png`.

## Phần B. Claude làm (không phải vẽ)
Thứ tự và mỗi bước một commit, có ảnh trước/sau và `tsc` + e2e.
1. **Duyệt và nạp lô S01–S27 đã giao** (45 ảnh): tiền cảnh cành/bụi/mái hiên/cờ/đèn/rèm, rừng xa 3 lớp, lối xuyên cổng, tường thành, thanh HP/MP/EXP, minimap, bóng, mảnh nối nhà. Nạp bằng tool có kiểm kích thước/màu/alpha như đã làm với lô sảnh. Trả lại GPT những ảnh lỗi.
2. **Lớp tiền cảnh mờ**: dựng lớp sprite lớn sát camera, làm mờ theo độ sâu (làm mờ riêng lớp hoặc bake texture mờ), ẩn tự động khi che nhân vật.
3. **Nạp và nối hiệu ứng trận**: fx 6 hệ đã có vào trận (đòn kỹ năng theo hệ, tia trúng đòn, thua, bắt thú), cộng M01–M07 khi có. Giữ nhịp và lướt tới hiện có.
4. **Bóng đổ dài theo hướng nắng** cho cây, cột, nhà: giả bằng bóng bóp méo ở mức Trung bình, bóng thật ở mức Cao; theo giờ trong ngày.
5. **Giao diện**: nạp bộ A4 (N01–N09) khi GPT giao; trước mắt dùng hết bộ khung có sẵn trong `public/ui` cho menu, Cài đặt (nút, ô chọn bật/tắt, tab), khung chat chỉnh tông với HUD; thêm phông serif/pixel có giấy phép; biểu tượng menu và icon vật phẩm to hơn.
6. **Chuyển động và sự sống**: nạp idle 7 NPC (vá tool đồng bộ), nạp dải chạy khi GPT giao (A0), bụi/cỏ bước chân, chim và lá rơi ở rừng, biển tên khu vực khi vào map, chuyển cảnh vào/ra trận.
7. **Địa hình có độ cao (S12–S19)**: chỉ dùng làm trang trí mép/bục/cầu, **không đổi lưới đi hay vị trí điểm dịch chuyển** của P12. Cần bạn duyệt chỗ đặt trước khi sửa từng map.
8. **Âm thanh**: kiểm repo đã có nhạc nền/hiệu ứng nào, báo bạn trước khi đề xuất nguồn (không tự thêm nhạc có bản quyền).
9. **Kiểm**: sửa script dev `tour2` và `dev battle 1v1` (chọn bệ 3 không tồn tại), chơi thử lại toàn tuyến, cập nhật `PLAYTEST-OCTOPATH-GAP.md`, đo trên GPU thật nhờ bạn thử Mac/iPhone.

## Việc cần bạn quyết
- Gửi GPT theo thứ tự A0 → A1 → A3 → A2? (Đề nghị vậy: chuyển động, hiệu ứng trận, rồi hoàn thiện cảnh.)
- Mục 7 (độ cao) có làm trong v1.0.x không, hay để v1.1.
- Nhạc: dùng nguồn nào (tự có, thư viện miễn phí, hay chưa cần ở v1.0.x).
