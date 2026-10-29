# Kế hoạch sửa giao diện ngoài trận (10 điểm nhận xét 2026-10-29)

Nguồn: nhận xét sau khi chụp bản `4c239b08` (màn ngang 1280×720 và màn dọc 430×932, mức Trung bình, ban ngày). Mọi sửa nằm ở `apps/client/src/ui/` (Hud.tsx, Overlays.tsx, PetArt.tsx, style.css, skin.ts) trừ khi ghi khác. Mỗi nhóm một commit, có ảnh trước/sau, `tsc` + e2e smoke chromium. Không đụng lưới đi, điểm dịch chuyển, luật server khi chưa được duyệt.

Quy ước kiểm cho cả kế hoạch: chụp lại bằng `dev ui tour` + `dev hud shot` ngang/dọc, so ảnh trước/sau; nút bấm ≥ 40 px trên màn dọc; chữ nội dung ≥ 12 px (nhãn phụ ≥ 11 px).

## Nhóm 1 — Sửa ngay bằng code, không cần asset mới (làm trước, 1 phiên)

| # | Điểm | Cách sửa | Tiêu chí đạt |
|---|---|---|---|
| 1 | Khung chat xanh nhạt lệch tông | Đổi nền sang tối ngả xanh mờ (`rgba(10,16,30,.78)`), viền vàng mảnh như `.hud-card`, chữ sáng; tab chat tối, tab chọn viền vàng. Giữ tự mờ khi rảnh. Dùng lại `chat-panel.png` nếu có bản tối, nếu không thì CSS thuần. Khi có `chat-frame.png` (N09) thì thay nền. | Sảnh không còn mảng sáng nhất màn hình; chữ đọc được trên cả rừng và thành phố. |
| 2 | Khối mục tiêu nhiệm vụ mờ | Nền tối `rgba(8,12,24,.72)`, viền trái vàng, tiêu đề vàng, dòng phụ `#e6e1d2`; giới hạn 2 dòng, ô to ra bằng chữ. | Đọc rõ trên nền sáng nhất (rừng nắng, sảnh). |
| 3 | Ảnh linh thú trong HUD quá nhỏ | `PetPortrait` thêm chế độ `bust`: phóng nền atlas 1,6–1,8× và lệch lên để lấy phần thân trên (dùng `bodyH/footPad` của `petArt`). Áp cho HUD, danh sách linh thú, chi tiết. | Con thú chiếm ≥ 70% đường kính vòng, thấy rõ đầu/mặt. |
| 4 | Chữ trong bảng quá nhỏ | Nâng nội dung bảng lên 13 px (nhãn phụ 11–12 px); kháng hệ chuyển thành lưới 2 cột có biểu tượng hệ (đã có `element_*.png`) thay cho một dòng chữ; thẻ (Lv, ★, hệ) cao hơn; nút trong bảng `min-height: 40px`; mô tả vật phẩm 12 px, thưởng nhiệm vụ dùng biểu tượng + số. | Không còn dòng chữ < 11 px trong bảng; không tràn dòng ở 360 px rộng. |
| 8 | Cài đặt như form web | Dùng thanh trượt cho âm thanh (0–100), chip chọn có biểu tượng bật rõ (`checkbox-on/off.png` đã có), nhóm theo tiêu đề nhỏ (Đồ họa / Âm thanh / Giao diện); nút khóa dùng chữ rõ hơn (đổi "MP đầy" thành màu xám sáng, không dùng độ mờ 40%). | Một màn không cần cuộn ở 1280×720; đổi cài đặt vẫn lưu qua tải lại (test hiện có). |
| 9 | Nút "Nói chuyện" bị bẻ dòng | Nhãn nút nhận kích thước chữ theo độ dài (tự co 15 → 12 px), `white-space: nowrap`; nút `Chọn` rộng thêm 14% ở màn dọc; nhãn dài hơn 8 ký tự dùng biểu tượng + chữ ngắn ("Nói chuyện" → "Nói"). | Mọi nhãn tương tác hiện trên một dòng ở 360–430 px. |

## Nhóm 2 — Cần quyết định hoặc đụng dữ liệu (làm sau khi bạn trả lời)

| # | Điểm | Phương án | Việc cần bạn quyết |
|---|---|---|---|
| 5 | Không đổi thứ tự / chọn con chính | **A (khuyên dùng):** thêm trường `party` (danh sách id, tối đa 3) lưu ở server, intent `pet.party_set`; client có màn "Đội hình" với nút ▲▼ hoặc kéo thả, chọn con chính, thêm/bỏ con khỏi đội. HUD và trận chỉ lấy theo `party`. **B:** client-only, lưu thứ tự trong localStorage (nhanh, nhưng không theo tài khoản, trận không biết). | Chọn A hay B. A cần sửa Go (`character`, `protocol`, test); container không chạy được Go 1.25 nên phải kiểm trên Mac. |
| 6 | Chi tiết linh thú thiếu tuổi và đồ | Dữ liệu hiện có: giới tính, sao, đã giám định, cường hóa, đời trước. **Tuổi** cần định nghĩa (số ngày từ lúc nở? cấp đời?) và **đồ mang** cần có hệ trang bị cho linh thú; cả hai chưa có trong `schema.ts`. Trước mắt hiện đủ những gì có (giới tính, sao, giám định, cường hóa, bố mẹ) và chừa hàng "Tuổi", "Đồ" ẩn sau cờ. | Bạn có hệ trang bị linh thú trong thiết kế P-sau không, "tuổi" nghĩa là gì. Nếu chưa có, để cho bản sau. |
| 10 | Hội thoại NPC là bảng giữa màn | **A:** giữ bảng giữa (hiện tại), chỉ làm to chân dung. **B:** khung thoại thấp ở đáy kiểu Octopath: chân dung lớn bên trái, tên NPC nhô lên, chữ gõ dần, lựa chọn xếp dọc bên phải; cảnh vẫn nhìn thấy. B cần `dialogue-frame.png` và `dialogue-nameplate.png` (N08). | Chọn A hay B. Mình khuyên B nhưng làm sau khi GPT giao N08. |

## Nhóm 3 — Cần asset từ GPT (đã có prompt trong `PLAN-OCTOPATH-V101.md` mục A4)

| # | Điểm | Asset | Việc mình làm khi có ảnh |
|---|---|---|---|
| 7 | Minimap nhỏ, khó đọc | N05 `minimap-frame.png`, N06 `minimap-markers.png` | Dựng minimap lớn hơn có khung trang trí, thu/phóng theo map, chấm: người chơi (mũi tên), NPC, cổng dịch chuyển, quái; bấm vào để mở bản đồ lớn. Trước đó: tạm tăng cỡ chấm tối thiểu 5 px, phóng khung lên 220 px ngang. |
| 1, 2, 4 (hoàn thiện) | Khung chung | N07 `panel-frame.png`, N09 `chat-frame.png`, N01/N02 tấm HUD | Thay nền CSS tạm bằng khung 9-slice của GPT; giữ nguyên bố cục đã sửa ở Nhóm 1. |
| 10 (nếu chọn B) | Khung thoại | N08 | Dựng khung thoại đáy. |

## Thứ tự và ước lượng
1. **Nhóm 1** (điểm 1, 2, 3, 4, 8, 9): một phiên, 3 commit (chat+mục tiêu, ảnh linh thú+chữ bảng, cài đặt+nút). Kiểm: chụp ngang/dọc, smoke.
2. **Điểm 7 tạm thời** (to hơn, chấm rõ hơn) cùng phiên 1 nếu còn thời gian; bản đẹp chờ N05–N06.
3. **Điểm 5** sau khi bạn chọn A/B; nếu A, kiểm Go trên Mac.
4. **Điểm 6, 10**: theo câu trả lời của bạn; làm cùng đợt nạp bộ A4.
5. Cập nhật `PLAYTEST-OCTOPATH-GAP.md` và chơi thử lại các màn ngoài trận sau mỗi nhóm.

## Rủi ro đã biết
- Các test e2e đi đường dài hết giờ chập chờn (không liên quan giao diện); không coi là hồi quy nếu chạy lại qua.
- Chụp bằng SwiftShader: màu và độ mờ có thể khác GPU thật; sau Nhóm 1 cần bạn xem trên Mac/iPhone.
- Đổi cỡ chữ có thể làm tràn trên màn 360 px: kiểm bằng chụp 360×740.
