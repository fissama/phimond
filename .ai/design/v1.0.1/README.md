# v1.0.1 — sửa theo đánh giá "người chơi khó tính"

Nguồn: `review-graphics-v1.0.0.md`, `review-gameplay-v1.0.0.md` (cùng thư mục). Trạng thái ghi ngày 2026-10-22.

## Đã làm trong bản này

### Đồ họa (đợt GPT vẽ lại, đã cắt và nối vào client)
| Mục review | Việc đã làm | Trạng thái |
|---|---|---|
| N1 chu kỳ đi | Dải đi 6 khung thật: nam (bên, xuống), nữ (bên). `CharacterSprite` có dải theo hướng (`run`, `run-down`, `run-up`), lên/xuống không còn lật ngang. | Còn thiếu hướng lên (nam, nữ) và xuống (nữ): hiện dùng dải bên. |
| N2 đường đất chữ nhật | 6 mảnh chuyển đất↔cỏ (`path-fringe-*`, `path-cap-*`) đè lên mép đường (`fringe()` trong `scene.ts`). | Cần chỉnh thêm: ảnh trong cảnh vẫn lộ nhịp ô vuông; mảnh sáng/chi tiết hơn cỏ nền. |
| N3 viền rừng | 6 mảnh viền theo lớp (`forest-*`), `dressForest()` dựng tán xa, thân giữa, bờ trước, góc, bờ phía camera, cổng portal. | Đạt trong ảnh chụp; chưa kiểm map Rừng Sâu kỹ. |
| N4 thảm/gạch/bệ | Chưa vẽ. | GPT còn nợ (xem `GPT-REMAINING.md`). |

Tất cả asset mới `approved=false` cho tới khi người duyệt trong cảnh thật. Cắt bằng `tools/p01/cut_release_art.py`, nạp bằng `python3 tools/p01/sync_client_assets.py --merge` (KHÔNG chạy bản đầy đủ: nó xóa `public/hd2d` và làm hỏng các file theo dõi trong sparse checkout).

### Gameplay
| Mục review | Sửa |
|---|---|
| G1 Mira bị tường che | Tường sảnh lùi sau hàng 1 (`scene.ts`). |
| G2 không hướng dẫn | Khung "Mục tiêu" ở HUD (`game/goal.ts`), nút Chọn đổi nhãn theo ngữ cảnh và nháy khi có thể tương tác, 3 dòng chào ở chat. |
| T2 Menu khóa mà không báo | Chạm/giữ phím khi bảng đang mở hiện thông báo "Đóng bảng đang mở để tiếp tục di chuyển". |
| T3 chạm ô chặn | Tự đi tới ô đi được gần nhất trong bán kính 2. |
| T5 trận đè D-pad | HUD thế giới ẩn hẳn khi đang trong trận. |
| L1 chat trống | Chat gọn 2 dòng, bấm để mở 6 tab, tự mờ sau 7 giây. |
| L2 Menu lệch khung | Nội dung lùi vào trong khung kim loại, tiêu đề giữa, nút rộng bằng vùng nội dung. |
| G3 trượt | Một phần nhờ dải đi mới; xem nợ về hướng lên. |

### HUD (hướng "game thật", không còn là bản demo)
Căn cứ nghiên cứu: vùng an toàn, mục tiêu chạm ≥ 44–48 px, neo theo cạnh/góc, hiện dần theo ngữ cảnh, mờ khi không cần, tùy chọn mật độ, hỗ trợ ngang/dọc.
- Bản đồ nhỏ góc phải trên (vẽ từ lưới đi được; ô cổng, NPC, bệ/trụ, vị trí người chơi).
- Cột menu 4 nút dưới bản đồ nhỏ; nút Chọn theo ngữ cảnh ("Nói chuyện", "Chọn bệ", "Dùng trụ").
- Cài đặt → "Mật độ giao diện": Đầy đủ / Gọn (ẩn mục tiêu, bản đồ nhỏ, chat).
- Điện thoại nằm ngang (cao ≤ 500 px): bỏ mục tiêu và bản đồ nhỏ, thu nhỏ nút, D-pad nhỏ lại. Dựng đứng (≤ 520 px): xếp lại tên map, bản đồ nhỏ, menu.
- Tôn trọng `prefers-reduced-motion` cho hiệu ứng nháy của nút Chọn.

## Kiểm
`vitest` 21/21, `tsc` sạch, `npm run build` ổn, Playwright chromium 7/7 (SwiftShader, không đại diện hiệu năng).
Chưa kiểm: iPhone/Safari thật, hiệu năng GPU thật.

## Xem thêm
- `DEBT.md`: nợ kỹ thuật/nội dung chưa làm (Phase sau).
- `GPT-REMAINING.md`: danh sách việc vẽ còn lại, gửi GPT khi hết giới hạn.

## Đợt 2 (2026-10-22): sảnh, menu, hiệu ứng HD-2D, thanh dưới

- **Sảnh vẫy gọi:** Mira đứng trước 3 bục (9,6), người chơi vào ở (9,8). Trên bục là 3 thần thú 5★ (Linh Tiên Hoa Hương `0144`, Độc Hạt Vương `0151`, Kim Kỳ Lân `0149`, trưng bày, lơ lửng nhẹ, chạm được). Chọn bục nào thì nhận pet 1★ Lv1 cùng race: Tiên Chưởng (cây), Sa Hạt (côn trùng), Xích Ưng (thú). Dữ liệu: `pedestals[].species/display` trong `build_maps.py`; loài mới `tien_chuong`, `sa_hat`, `xich_ung` trong `data/pets/species.json` (chỉ số mượn từ loài cũ tương đương, chờ cân bằng P11); atlas thêm bằng `tools/build-web-assets/legacy-species-map.json` + `build_assets.py`.
- **Menu phải:** một nút Menu, bấm mới sổ Linh thú, Túi đồ, Nhiệm vụ, Cài đặt.
- **Hiệu ứng HD-2D** (`render/post.ts`, `daylight.ts`, `atmosphere.ts`): Cao = tilt-shift + bloom + chỉnh màu theo giờ + tối góc + quầng sáng đèn + tia nắng + hạt bụi/phấn hoa; Trung bình = tilt-shift + chỉnh màu + đèn/tia nắng (không bloom); Thấp = không hậu kỳ. Giờ theo đồng hồ máy (sáng, ban ngày, hoàng hôn, đêm); Cài đặt → "Thời gian trong game" để ép cố định. Sảnh là trong nhà nên ánh nến cố định.
- **Thanh dưới:** dải đá che cả cạnh dưới, cảnh 3D kết thúc phía trên thanh; D-pad, chat, nút Chọn/Trở về nằm trong thanh.

## Đợt 3 (2026-10-22): combat ngang, HUD trái, chat, viền chặn, ngày đêm

- **Trận đấu** (`ui/Battle.tsx`): cảnh ngang kiểu Octopath, quái bên trái (lật mặt), linh thú mình bên phải, bảng tên trên cùng (quái trái, mình phải: tên, Lv, HP, MP), banner "Lượt N", menu lệnh dùng sprite `battle_*`, log 3 dòng. Kết quả, vàng, EXP, vật phẩm, lên cấp **ghi vào khung chat**, không còn popup vàng hay hộp kết quả bắt bấm Tiếp tục: cảnh tự đóng sau ~1,7 s. Giữ testid `battle`, `battle-player/enemy`, `battle-log`, `act-*`, `battle-result` (banner mờ); bỏ `battle-continue`.
- **HUD trái trên**: chân dung pet + cấp pet (badge) + 3 thanh khung vàng HP/MP/EXP (sprite `frame-bars`, ruột `hp/mp/xp-fill`), dưới là dải người chơi: Lv + tên + EXP + vàng. EXP cần = cấp × 25 (`xp_per_level`).
- **Chat**: tab luôn hiện phía trên, khung `chat-panel` viền vàng, 3 dòng khi thu gọn, mở rộng bằng nút ▴/▾ hoặc bấm tab; nằm giữa D-pad và nút Chọn/Trở về trong thanh dưới.
- **Viền chặn Triệu Linh Điện**: cột đá hai bên, cờ treo, chậu cây dài và thùng ở phía trước. Rừng và thành phố đã có viền từ đợt trước.
- **Ngày đêm** (`daylight.ts`, `post.ts`): thêm tương phản, tách tông bóng tối/vùng sáng. Xem `OCTOPATH-ASSESSMENT.md`.
- E2E: bỏ bước bấm Tiếp tục; test D-pad đi lệch trái 2 ô vì Mira chặn (9,6).

## Đợt 4 (2026-10-22): sửa theo nhận xét "player khó tính"

- **Combat:** bảng của mình (chân dung, Lv, HP/MP/EXP pet) ở góc trên trái như game gốc; bảng quái nổi ngay trên đầu quái (tên, "Hoang dã" vì server chưa gửi Lv, HP); hai con thú đứng gần nhau, cùng cỡ; menu lệnh nổi dạng thuốc dưới sân khấu (Tấn công, Kỹ năng, Bắt, Chạy, Thêm → Phòng thủ/Vật phẩm/Tự động); nút khóa ghi lý do ("Hết Phù", "Chưa có", "Trống"); số sát thương to hơn, màn rung khi trúng, lướt tới khi đánh, ánh sáng rìa + hạt bụi + tia sáng; log ghi rõ "Ai → Ai: −X HP".
- **Thắng:** khung thưởng không chặn (vàng, EXP, lên cấp pet/người chơi, học chiêu, bắt được) hiện phía trên, chạm là qua, tự đóng sau 4,2 s (1,7 s khi chạy trốn). Cũng ghi vào chat. Client tự so cấp trước/sau trận vì server không gửi sự kiện lên cấp.
- **Nền combat:** nạp `public/battle/battle-bg-<key>.png` (`forest`, `deep_forest`, `gate`, `city`, `hall`) nếu có; chưa có thì dùng nền thế giới làm mờ. Prompt + ảnh mẫu để gửi GPT: `battle-bg/PROMPTS.md`, `battle-bg/refs/`.
- **HUD trái:** hai thẻ cùng một ngôn ngữ khung (thẻ pet, thẻ người chơi), nhãn HP/MP/EXP tách khỏi thanh (chữ ≥ 11 px), HP dưới 25% nháy, chạm chân dung mở menu Linh thú.
- **Chat:** chỉ còn 3 tab đang có nội dung (Tất cả, Hệ thống, Khu vực); khung xanh nhạt (`ui/chat-panel-light.png`, tô lại từ `chat-panel.png`, ruột xanh nhạt, viền vàng giữ nguyên) và chữ tối như game gốc.
- Chưa làm: hàng chờ lượt, icon trạng thái (còn chữ), âm thanh, hiệu ứng kỹ năng, Lv quái (cần server): xem DEBT D13.

## Đợt 5 (2026-10-22): 1 pet đấu 2–3 quái cùng loài
Server sinh 2–3 quái giống nhau (40%/60%, `rules.encounter_weights`), nhận `target_id`, thưởng cộng theo từng quái. Client: đội hình so le, chọn mục tiêu (kim cương cyan), hậu tố A/B/C, bố cục dọc. Chi tiết, cờ xung đột P02-R07 và vấn đề cân bằng: `COMBAT-HUD-SPEC.md`.
