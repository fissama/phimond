# Prompt GPT cho Nhóm 3: bộ khung giao diện (cập nhật 2026-10-29, theo HUD mới)

Gửi **từng ảnh một**, đính kèm trực tiếp ảnh tham chiếu (không zip). Lưu đúng tên file. Ảnh tham chiếu nằm trong `apps/client/public/ui/`; riêng `bar-frame-*`, `bar-label-*`, `ui-minimap.png` (bản mới đã duyệt) nằm ở `apps/game-web/art-src/hd2d/octopath-s01-s27-20261029/delivery/` và `ui-bottombar.png` ở `apps/game-web/art-src/hd2d/p01-release-art-20261023/delivery/`. Trước khi gửi, GPT cần biết các điểm sau, vì lô trước đã vướng lỗi này:

- **Viền hồng/tím nhạt ở mép**: lô S01–S27 có 12 file dính điểm ảnh hồng sát mép. Nền ma-gen-ta phải là một màu duy nhất `#FF00FF`, **không khử răng cưa**, không làm mềm mép, không có điểm ảnh hồng, tím nhạt hay đỏ tươi nằm trong viền vàng.
- **Vết nối**: ảnh lặp được (cạnh 9-slice) phải liền mạch khi ghép; không dùng đường chéo cắt ngang.
- **Dải đen đặc ở rìa**: không để hàng/cột đen đặc nằm ngoài khung.
- Alpha nhị phân, tối đa 48 màu, đúng kích thước từng mục.

## Đã có, không vẽ lại
Lô S01–S27 đã giao và được duyệt: `bar-frame-hp/mp/exp.png` (256×32), `bar-label-hp/mp/exp.png` (64×32) và `ui-minimap.png` (512×320, khung minimap, ruột rỗng). Dùng làm **ảnh mẫu bảng màu và hoa văn góc** cho mọi mục dưới đây. N05 (khung minimap) coi như xong bằng `ui-minimap.png`; chỉ còn N06 (chấm minimap).

## Hướng chung (cho cả nhóm)
Khung vàng mảnh hai nét (nét ngoài vàng sẫm, nét trong vàng sáng) trên nền tối ngả xanh teal, góc trang trí nhỏ, không tô màu rực; cùng ngôn ngữ với `ui-minimap.png` và `bar-frame-hp.png`. Nhìn thẳng, không phối cảnh.

## Khối chung (dán đầu mỗi prompt)

> Pixel art UI asset for an HD-2D game in the style of Octopath Traveler: crisp pixels, painterly shading, warm light from the TOP-LEFT, thin double gold line border (outer line dark gold, inner line bright gold), small ornate corner pieces, dark navy-teal fill, flat front view with no perspective, no text, no icons unless stated, 1px dark outline, no anti-aliasing, no blur, no watermark. Max 48 colors, palette and corner ornament language matching the attached references. Background outside the asset is a single flat magenta #FF00FF with binary alpha: no semi-transparent pixels, no pink or lilac fringe pixels along any edge, no pink pixels inside the gold. Areas marked TRANSPARENT are also pure #FF00FF in the source. Output PNG exactly the size stated.

---

## Thứ tự ưu tiên
N01 → N02 → N08 → N07 → N09 → N03 → N04 → N06.

### N01 `hud-player-plate.png` (320×88)
Đính kèm: `ui-minimap.png`, `bar-frame-exp.png`, `badge-level.png`
Tấm người chơi **nhỏ**, là thẻ phụ chỉ để mở bản đồ, không chiếm chú ý của linh thú. Bố cục từ trái sang phải: ô tròn 56 px chứa huy hiệu cấp (để trống để code in số), dải tên (TRANSPARENT, ~150×28) ở giữa, rãnh EXP mảnh 8 px bên dưới dải tên. Viền mảnh hơn hẳn thẻ linh thú. Mảnh tối thấp nhất 4 px còn trong suốt quanh khung để code đổ bóng.
> [Khối chung] Small player plate, 320×88: left a round 56 px level badge ring (empty centre, TRANSPARENT), centre a name strip (TRANSPARENT, about 150×28), under it a thin 8 px EXP trough with gold ends (empty trough, dark teal). The whole plate is slim and light, thinner border than a pet card.

### N02 `hud-pet-main.png` (360×128) và `hud-pet-sub.png` (264×96)
Đính kèm: `ui-minimap.png`, `bar-frame-hp.png`, `frame-portrait.png`, `badge-level.png`
Thẻ linh thú dạng **cột dọc**: hình chân dung tròn + cấp nhỏ + 2 vạch mảnh (đỏ HP, xanh MP). Thẻ chính (`hud-pet-main`) to hơn, hai thẻ phụ (`hud-pet-sub`) nhỏ hơn và bằng nhau. **Hình học (đúng toạ độ, code sẽ in lên):**
- `hud-pet-main` 360×128: vòng chân dung đường kính 104 px, tâm tại (68, 64), nửa đè mép trái khung; huy hiệu cấp tròn 28 px ở góc dưới phải vòng, tâm (104, 100); hai rãnh vạch trong khối bên phải: rãnh HP x 132–344, y 40–52; rãnh MP x 132–344, y 62–72; rãnh rỗng (TRANSPARENT).
- `hud-pet-sub` 264×96: vòng chân dung 76 px, tâm (50, 48); huy hiệu 22 px tâm (76, 74); rãnh HP x 98–248, y 28–38; rãnh MP x 98–248, y 48–56.
> [Khối chung] Pet card for the HUD, vertical-stack layout, 360×128 (main). Left a round portrait ring 104 px (centre empty, TRANSPARENT) overlapping the left edge of the plate, a small round level badge on its lower right, and to the right two thin empty bar troughs (upper trough taller than lower), troughs TRANSPARENT, gold-capped ends. No name text. Same gold hue as the attached references. Then the same design scaled to 264×96 as `hud-pet-sub.png` (separate request).

### N08 `dialogue-frame.png` (1024×224), `dialogue-nameplate.png` (288×56), `dialogue-choice.png` (288×56)
Đính kèm: `ui-bottombar.png`, `panel-large.png`, `frame-portrait.png`
Khung hội thoại NPC kiểu Octopath, **nằm đáy màn hình**, thấp rộng.
- `dialogue-frame`: nền tối mờ ngả xanh (ruột TRANSPARENT để code đặt nền mờ), viền vàng mảnh, một khoảng trống 160×160 bên trái làm chỗ chân dung (khung tròn nhỏ viền vàng, ruột TRANSPARENT, tâm (112, 112)), vùng chữ x 220–980.
- `dialogue-nameplate`: phiến tên nhô lên góc trái trên khung thoại, hai đầu cắt chéo nhẹ.
- `dialogue-choice`: nút lựa chọn dài, hai trạng thái trong cùng ảnh xếp dọc: trên là bình thường, dưới là được chọn (sáng hơn, một mũi tên vàng nhỏ ở trái). Ảnh 288×112.
> [Khối chung] Octopath-style bottom dialogue box: very wide and low, thin gold double border, dark translucent navy-teal interior (TRANSPARENT in the source), a round portrait socket 160 px on the left, small gold corner ornaments, a subtle gold line along the top edge. 1024×224.

### N07 `panel-frame.png` (192×192, 9-slice, góc 48 px)
Đính kèm: `panel-large.png`, `ornament-corner.png`
Bảng chung cho menu/túi/nhiệm vụ/cài đặt thay `panel-large`. Ruột nền giấy tối ngả xanh, co giãn được (**không hoa văn lớn, không vệt chéo**), viền vàng hai nét, góc có hoa văn nhỏ 48×48. Cạnh lặp liền mạch.
> [Khối chung] 9-slice panel frame, 192×192, corners 48×48 px with small gold ornaments, edges and the 96×96 centre are plain and tileable (no large pattern, no diagonal marks), dark ink-teal paper interior with very subtle grain.

### N09 `chat-frame.png` (768×176, 9-slice) và `chat-tab-normal.png`, `chat-tab-selected.png` (160×44)
Đính kèm: `chat-panel.png`, `chat-tab-normal.png`, `chat-tab-selected.png`
Đổi khung chat từ xanh nhạt sang tối-vàng cùng tông HUD. Ruột TRANSPARENT; tab thường tối, tab chọn viền vàng sáng và đáy hở nối vào khung.

### N03 `slot-common.png`, `slot-uncommon.png`, `slot-rare.png`, `slot-epic.png`, `slot-legendary.png` (96×96)
Đính kèm: `slot-normal.png`, `slot-rare.png`
Viền ô đồ theo độ hiếm: chỉ khác màu viền và độ tinh xảo (xám bạc, xanh lục, xanh lam, tím, vàng cam có tia sáng ở góc). Ruột TRANSPARENT, cùng một khung nền để ghép cạnh nhau. Gửi một ảnh một lượt, giữ nguyên khung nền giữa các lượt.

### N04 `slot-empty.png`, `slot-selected.png`, `slot-locked.png` (96×96) và `slot-equipped-corner.png` (32×32)
Đính kèm: `slot-selected.png`, `slot-locked.png`
Trạng thái ô: `empty` (khung mờ, ruột TRANSPARENT), `selected` (viền sáng, góc sáng), `locked` (ổ khoá nhỏ giữa, tối đi). `slot-equipped-corner.png` là huy hiệu nhỏ ở góc trên phải ô đang trang bị.

### N06 `minimap-markers.png` (72×24, 3 biểu tượng 24×24 ngang hàng)
Chấm người chơi (mũi tên vàng), NPC (kim cương xanh), điểm dịch chuyển (xoáy tím). Viền tối 1 px để đọc được trên nền xanh lá. Nền ma-gen-ta thuần, không khử răng cưa.

---

## Cách mình sẽ kiểm khi GPT giao
1. Đo máy: kích thước, alpha nhị phân, ≤48 màu, đếm điểm ảnh hồng/tím ở mép, hàng/cột đen.
2. Xem contact sheet, ghép thử cạnh 9-slice ở nhiều cỡ.
3. Kiểm hình học N02 bằng cách chồng lên HUD thật (rãnh HP/MP đúng toạ độ).
4. Cài từng file đã duyệt bằng tool, không cài hàng loạt.
