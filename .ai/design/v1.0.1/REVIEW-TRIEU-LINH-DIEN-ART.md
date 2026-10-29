# Nhận xét bản vẽ lại Triệu Linh Điện (GPT, 2026-10-28) và nạp vào v1.0.0

Nguồn: `apps/game-web/art-src/hd2d/batch-02-octopath/summon-hall-redraw-20261028/` (chưa commit khi duyệt) và các ảnh `hd2d_summoning-hall-review-*`, `hd2d_review_pedestal_*` ở `apps/game-web/public/scenes/tex/`.
Duyệt bằng mắt trên bảng tổng hợp và trong game thật (`apps/client`, Chromium SwiftShader, 1280×720 và 430×932). Quyền duyệt asset do owner ủy cho Claude.

## Kết luận

Đạt, nạp vào. Cả bộ cùng một ngôn ngữ (pixel-art Octopath, ≤49 màu, viền tối, sáng từ trên-trái), ghép với sprite NPC/linh thú hiện có không lệch. Sảnh đổi từ gian gỗ tối sang **sân đá mở ban ngày nhìn ra thành phố**, đúng hướng của bản vẽ GPT và sáng hơn bản cũ rất nhiều.

## Từng nhóm

| Nhóm | Nhận xét | Dùng trong game |
|---|---|---|
| Hậu cảnh thành phố 1216×405 | Đẹp: tường thành có lỗ châu mai, mái ngói cam, lâu đài giữa, núi xa, mây. Không lặp ngang được (nền đặc, hai mép cắt thẳng). Mật độ điểm ảnh thấp hơn phần còn lại (kéo ra 33 px/ô so với 128 px/ô), nhưng ở vị trí xa trông như phối cảnh khí quyển nên chấp nhận. Trời xanh phẳng chưa bao giờ lọt vào khung hình vì camera cố định. | Mặt phẳng đứng sau sân thượng. |
| Sàn đá 512×512 (34 màu) | Gạch cát nứt tự nhiên, ấm, hợp cột và ngưỡng. Công cụ ghi `seamless_verified=false` nhưng trong cảnh không thấy đường nối. Lặp lại rõ ở 5×3 lần (cùng một vết nứt). | Sàn toàn sảnh và sàn ngoài rìa. Nên có thêm 1 biến thể để phá nhịp. |
| Cột đá (224×560) | Thân thon, đầu cột và chân cột vàng; sạch, không viền ma-gen-ta. | 5 cột hàng sau, 2 cột trong sảnh (ô `C`), 4+4 cột hai hông. |
| Xà ngang (1942×100) | Hoa văn vàng nối liền, khớp cột. | Nối đầu 5 cột hàng sau. |
| Ngưỡng cửa trái/phải (1029×267 mỗi nửa) | Bậc đá có hoa văn, hai nửa chừa đúng lối ra 2,92 ô, khớp cổng `hall_exit` (x 8–10). | Mép dưới sảnh. |
| 3 bệ thú (218×136, 212×156, 224×136) | Ba kiểu riêng (tròn viền vàng, bát giác có ba tháp, vuông vát) nên nhận ra từng bệ; nạp thay bệ cũ. | Bệ 1/2/3. |
| Vòng triệu hồi fx (4 khung 192) | Đẹp nhất bộ: vòng bạc-tím, ngọc vàng, lấp lánh đổi khung. Đặt nằm phẳng trên sàn đúng tâm ô xuất hiện, nhìn hợp với thẻ nhân vật hiện ra. | Thay hoa văn sàn cũ. |
| Bụi linh khí fx (4 khung) | Lửa vàng và đá xanh bay; dùng được, hơi rời rạc. | Bay trên vòng. |
| Bộ lễ vật (256×256 mỗi món) | Giá sách mở, quả cầu tinh tú, lư hương, cờ đỏ vàng, đèn treo, cửa kính màu: đều sạch và đồng bộ. Ảnh lư hương thực ra là **hai khung khói** của cùng một lư (ghép cạnh nhau), nên tách thành dải 2 khung hoạt hình. | Giá sách ở `K` trái, quả cầu ở `K` phải, lư hương ở `L`, cờ và đèn treo từ xà, kính màu dọc hai hông. |

## Không dùng / để lại

- **Thú trưng bày** (`showcase-pets/finish-01`: hoa, bọ cạp, kỳ lân, 192×192): đẹp nhưng trùng thiết kế với atlas P10 đang dùng ở trận và thẻ chọn starter. Đổi riêng ở sảnh sẽ lệch với phần còn lại, nên giữ atlas. Nếu owner muốn dùng, cần thay luôn atlas ba loài.
- **`spill-overlay.png`** (1024×1536 RGB, 231.102 màu, không alpha): không theo chuẩn palette, chưa đưa vào cảnh review. Bỏ qua, chờ GPT xuất lại (bảng màu ≤64, có alpha) nếu còn muốn dùng làm ánh sáng loang.
- `columns-redraw-01`, `scene-edges-preview.png`: bản phẳng cũ, GPT đã ghi là superseded.
- Các tệp `summon-pedestal-0N-active/dormant`, `summon-floor-emblem`, `hall-wall-*`, `hall-floor-*`, `hall-bookshelf`, `hall-torch` vẫn nằm trong `public/hd2d` nhưng sảnh không còn dùng (chưa xóa để không đụng sparse checkout).

## Việc đã làm trong client

- `tools/p01/install_hall_art.py` nạp ảnh + ghi `assets.json` (chỉ các id của sảnh). Lư hương được tách thành dải 2 khung.
- `scene.ts` theme `hall`: ánh sáng ban ngày; sàn mới + sân thượng sau hàng cột sâu ~2,5 ô rồi tới tường thành; hậu cảnh thành phố là mặt phẳng đứng; 5 cột + xà + 2 đèn treo + 2 cờ treo; cột và kính màu hai hông; ngưỡng cửa dưới; bệ mới; vòng triệu hồi và bụi linh khí động; `K`/`L`/`C` đổi thành giá sách/quả cầu, lư hương, cột (các ô chặn vẫn đúng như dữ liệu map P12, không đổi bố cục).
- `engine.ts`: `camBias` dịch tâm camera lên 1,5 ô khi ở sảnh để thấy xà và tường thành.
- `daylight.ts`: ánh sáng sảnh cố định ban ngày thay ánh nến.
- Kiểm: `tsc` sạch, vitest 24/24, Playwright chromium 11/11 (có test 3 ô nhân vật).

## Lô bổ sung 2026-10-29 (đã nạp)

Nguồn: `.../summon-hall-redraw-20261028/completion-20261029/summon-hall-extra-assets.zip` (6 PNG). Kiểm máy đạt (kích thước, màu, alpha nhị phân, không ma-gen-ta). Duyệt bằng mắt trong game:

| Asset | Nhận xét | Dùng |
|---|---|---|
| `stone-floor-b` 512×512 | Cùng gạch cát, bố cục khác hẳn bản A. GPT báo còn viền 2–8 px lấy từ bản A để hai mẫu nối nhau (nên chưa chứng minh "mọi viên gạch khác"); trong cảnh ghép A/B xen kẽ theo khối 4×4 ô không thấy đường nối, nhịp lặp đỡ hơn rõ. | Xen kẽ với A trên sàn sảnh. |
| `city-backdrop-wide` 2432×486 | Cùng hệ với bản cũ, rộng gấp đôi, lâu đài giữa, tường thành đáy thẳng. Mật độ điểm ảnh gấp đôi bản cũ (66 px/ô). | Thay nền thành phố. |
| `city-near-roofs` 2432×220 | Mái ngói cam và xanh, ống khói, tháp nhỏ; tối và ấm hơn nền xa nên đọc được là lớp gần. Dải lặp 1216 px hai lần. | Lớp thứ hai ngay trước nền, đáy chạm đỉnh tường thành. |
| `floor-light-1..3` 256×256 | Ba vệt sáng nghiêng (vàng, hồng đỏ, xanh) với hoa văn ô kính, mép dither. Tự nó giống mảnh pha lê đặc; dựng cộng sáng ở độ mờ 0,5 thì đọc là ánh sáng rơi xuống sàn. | 6 vệt trước các ô kính hai hông (bên phải lật gương). |

Còn nợ: bóng tiếp xúc (S22) và các mục S01–S27 khác trong `GPT-PROMPTS-OCTOPATH.md`.


## Lô viền hai bên (GPT, 2026-10-29)
- 3 ảnh nền magenta: lan can bên hông (2048×768), trụ đầu lan can (724×2172), ô cửa kính gắn tường (1122×1402). Đạt: cùng bảng màu/nét với lan can phía trước, vòm kính có khung đá dày; kích thước ngoài đúng quy cách nên `tools/p01/prep_hall_sides.py` cắt nền, thu về 512/128/256 px, ≤48 màu, alpha nhị phân.
- Lắp: xoay 90° quanh trục đứng để chạy dọc chiều sâu (tường 3D thật), 2 đoạn lan can + 3 trụ + 2 ô kính mỗi bên, bên phải đối xứng; thay hàng cột ngắn và ô kính lơ lửng cũ. Chỉ thấy rõ khi nhân vật đứng sát mép (camera bám người chơi).
- Còn lại: chưa có mảnh nối góc trước/sau và ngoại cảnh bên ngoài tường; nếu thấy trống khi màn rộng, thêm lô GPT sau.
