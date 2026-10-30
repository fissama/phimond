# Duyệt art lô ChatGPT — 2026-10-30 (Claude, ủy quyền của chủ dự án)

Nguồn: `ARTWORK-EXPANSION-STATUS-20261030.md`, `apps/game-web/art-src/hd2d/batch-15-expansion/`, `candidates-scene-extras-20261030/`. Mọi ảnh dưới đây đã được xem trực tiếp (nền xanh xám, phóng 2–6×).

## 1. Đã duyệt và dùng trong game

| Ảnh | Việc đã làm |
|---|---|
| `fx-footstep-dust` / `fx-footstep-grass` | Cài vào `public/hd2d`; `render/footsteps.ts` phát 1 lần mỗi ~0,55 ô đi được (4 khung, 0,42 s): cỏ ở rừng, bụi ở thành phố, không phát trong sảnh, tắt ở mức Thấp |
| `ambient-birds` | Cài làm tiền cảnh `fg-ambient-birds`, trôi ngang chậm (chu kỳ 70–90 s) ở rừng thường và thành phố; không có ở Rừng Sâu |
| `minimap-markers` | Minimap vẽ mũi tên (người chơi), kim cương (NPC), xoáy tím (cổng dịch chuyển chưa khóa) thay chấm màu; chưa nạp xong thì quay về chấm |
| `fg-deep-vines`, `fg-gate-banner-edge` | Đã duyệt và lắp ở lượt trước (commit a955b6eb) |
| `player-male.run` | Duyệt làm **mỏ neo S24**: đã tự kiểm khung 1 và 5, chân gần (quần xám) ở khung 1 thành chân xa ở khung 5, chân dẫn đổi bên. Chiều cao thân 166–168 px ổn định |

## 2. Đã duyệt, đã chép vào `public/ui`, chưa nối vào HUD

Cần một lượt dàn bố cục HUD riêng (thay `.hud-card`, `.pet-mini`, `.me-row`). Không nối ngay để không phá layout đang chạy và e2e.

| Ảnh | Ghi chú nối |
|---|---|
| `hud-player-plate` 320×88 | Dải tên 168×21 đủ chữ 12–13 px |
| `hud-pet-main` 360×128, `hud-pet-sub` 264×96 | Vòng chân dung và rãnh HP/MP theo đúng toạ độ trong `GPT-PROMPTS-NHOM3-UI.md` N02; vài điểm lốm đốm rất nhỏ trong rãnh HP của thẻ chính, không ảnh hưởng vì thanh fill vẽ đè |
| `panel-frame` 192×192 | 9-slice góc 48 px; cạnh và ruột trơn nên ghép được; thay dần `panel-large` |
| `dialogue-frame` 1024×224 | Vòng chân dung ~170 px thay vì 160 px, chấp nhận; code đặt chân dung theo vòng thực |
| `hall-side-corner` | Duyệt ảnh, để dành v1.1 |

## 3. Bị từ chối / cần vẽ lại (gửi lại ChatGPT)

Quy tắc chung cho mọi lượt gửi lại (dán đầu prompt): *Pixel art for an HD-2D game in the style of Octopath Traveler, crisp pixels, painterly shading, light from the TOP-LEFT, no anti-aliasing, no blur, no watermark, max 48 colors, binary alpha. Background is a single flat magenta #FF00FF (no soft edge, no pink/lilac fringe pixels, none inside the artwork). Output PNG exactly the size stated, on a flat background, one asset per image.*

### R1. `hall-outside-roofs-side.png` (512×384, đặc)
Lý do: trời xanh bão hòa quá, lệch tông; tường gần che mất lớp xa; trùng `hall-city-backdrop`.
Đính kèm: `city-backdrop-wide.png`, `hall-city-roofs.png`
> Distant city rooftops seen from the side window of a palace hall, 512×384, opaque. Same muted dusk palette and soft aerial perspective as the attached references: desaturated warm-grey sky fading to pale amber near the horizon, terracotta roofs and sandstone towers in soft haze, faint mountains. NO foreground wall, NO near battlements, nothing sharper or more saturated than the attached backdrop. Left and right edges must continue into each other (tileable horizontally), and the bottom 48 px fade into a flat roof-tone strip so it can sit under a window.

### R2. `walker-elder.run.png`, `walker-traveller.run.png` (1536×192, 8 khung)
Lý do: khung 1 và 5 cùng chân dẫn (vi phạm tiêu chí S23). Cần gửi riêng từng ảnh.
Đính kèm: ảnh đứng của nhân vật (`walker-elder.png` hoặc `walker-traveller.png`), dải hiện tại cùng tên (để giữ nhân vật), **`player-male.run.png` (mỏ neo đã duyệt, mượn nhịp chân)**.
> Same character, outfit and prop (elder: wooden staff; traveller: travel staff and pack) as the first attachment. 8-frame walking cycle to the RIGHT in one horizontal row of eight 192×192 cells, feet at (96,184), body height ~168 px in every frame. Copy the leg timing of the attached `player-male.run.png` exactly: frame 1 = NEAR leg forward, frame 5 = FAR leg forward (the two legs must be visibly swapped between frames 1 and 5, the trailing leg in frame 1 becomes the leading leg in frame 5); frames 3 and 7 are passing poses; arms swing opposite to the legs. Do not repeat the same half-cycle twice. Magenta #FF00FF background, no painted checkerboard.
Gợi ý quy trình (ChatGPT hay lỗi khi vẽ cả dải): yêu cầu **khung 1 và khung 5 trước** (2 ảnh), kiểm chân đổi bên, rồi mới yêu cầu 6 khung còn lại dựa trên hai khung đó.

### R3. N09 `chat-frame.png` (768×176) + `chat-tab-normal.png`, `chat-tab-selected.png` (160×44)
Lý do: sáu lần thử đều trả sai kích thước/alpha/màu; tab cũ còn xanh dương.
Đính kèm: `ui-minimap.png`, `chat-panel.png`, `chat-tab-normal.png`
> Chat panel frame 768×176, 9-slice friendly: thin double gold border (outer dark gold, inner bright gold), small gold corner ornaments, interior flat #FF00FF (becomes transparent), dark navy-teal band is NOT drawn inside. Edges between corners are plain and tileable. Then, as separate images: a 160×44 chat tab, dark navy-teal with a thin gold outline (normal), and the selected tab with a brighter gold outline and an OPEN bottom edge so it joins the frame.

### R4. N03 `slot-common.png` và `slot-legendary.png` (96×96)
Lý do: `common` đang là vàng-cam, không phân biệt được với `legendary` (cam); thiếu tia sáng ở góc. `uncommon`, `rare`, `epic` đã ổn.
Đính kèm: `slot-uncommon.png`, `slot-rare.png`, `slot-epic.png` (cùng khung nền)
> Same item-slot frame as the attached, 96×96, interior #FF00FF. `slot-common`: silver-grey border, plain corners. `slot-legendary`: bright gold-orange border (clearly brighter and more yellow than any attached), with a small star-shaped spark at each of the four corners. Only the border colour and corner detail differ from the attached frames.

## 4. Chưa xem lượt này
N04 (empty/selected/locked, equipped corner có điểm lạ dưới khung), N08 nameplate/choice, FX nguyên tố, chân dung NPC/starter, foe-ring, summon. Giữ trạng thái chưa duyệt.
