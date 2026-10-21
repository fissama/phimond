# Nghiệm thu thí điểm batch-11-tomb (10 asset) — 2026-10-15 23:55

**Kết luận: CHƯA ĐẠT. Tiến bộ lớn so với lần trước (đã là artwork thật), nhưng 3/10 đạt, 1/10 sửa nhỏ, 6/10 phải vẽ lại. Chưa mở 16 kit còn lại.**

## 1. Audit máy (audit.py + kiểm tra bổ sung)
10/10 đạt kiểm tra cơ học (RGBA, alpha nhị phân, 32–38 màu, lề, không hồng, không trùng hash, 128 px/đv). Khác hẳn lần trước (3–4 màu). Nhưng các chỉ số máy bỏ sót những lỗi dưới đây, vì vậy phải xem ảnh.

## 2. Kết quả từng asset (đã xem ảnh thật ở kích thước gốc)

| Asset | Kết quả | Lý do |
|---|---|---|
| `tomb-gravestone-01` | ĐẠT (xóa 13px lạc ở chân bia) | Bia vòm khắc thập tự, rêu, cỏ; đổ khối rõ, quay mặt trước |
| `tomb-gravestone-02` | ĐẠT (xóa 1px lạc) | Thập tự Celtic, dây leo; khác hẳn 01 về hình |
| `tomb-lantern-spirit` | ĐẠT | 4 khung khác nhau, cùng khung 85px, đèn lồng đồng + lõi ngọc lục, sắc nét |
| `tomb-sarcophagus-01` | SỬA | Hiệp sĩ nằm trên quan tài, đẹp. Nhưng có 3 mảnh lạc: vạch đứng cao 22px ở góc trái trên, vạch ngắn giữa trái, 2px; và một nét ký tên/vết ở góc dưới phải |
| `tomb-arch-gate` | VẼ LẠI | Nhìn xiên isometric 45° (mái, tháp, đá góc nhìn từ góc), không phải mặt trước billboard; còn 19px lạc. Gargoyle và đá đẹp, giữ ý tưởng |
| `tomb-portal-dormant` | VẼ LẠI | Cầu thang chéo isometric; mảnh tường 3.012px tách rời bên trái |
| `tomb-portal-active` | VẼ LẠI | Mảnh cột bị cắt lơ lửng ở góc trên trái (4.282px) và một mảnh nữa ở góc trên phải (435px), đều là phần thừa từ ô bên cạnh của sheet. Xoáy ngọc lục đẹp. Chiều rộng 202 so với dormant 190, vòm lệch ~7–10 px nên đổi trạng thái sẽ giật |
| `tomb-brick-floor` | VẼ LẠI | Viền mép tile tối hơn tâm (42,8 so với 54,0); ghép 3×3 hiện rõ khung lưới đậm. Họa tiết lớn lặp rõ, có đối xứng gương đường chữ thập |
| `tomb-graveyard-dirt` | VẼ LẠI | Làm liền mạch bằng cách LẬT GƯƠNG: ghép 3×3 hiện sọc đối xứng kiểu kính vạn hoa tại đường nối và chùm cỏ/xương lặp lại thấy rõ |
| `tomb-necropolis-wall-far` | VẼ LẠI | VẪN LÀ HÌNH SINH BẰNG CODE: tam giác, hàng chữ nhật làm lỗ châu mai, mặt trăng tròn phẳng, gradient. Không phải thành nghĩa địa. Còn 8 đơn vị bề rộng ở 128 px/đv (backdrop xa phải 64 px/đv, tức 16 đv hay 1024 px) |

## 3. Vì sao lỗi lọt qua QA của Gemini
- Tile "liền mạch" bằng lật gương: seam = 0 nhưng nhìn thấy ngay.
- Sheet cắt không sạch: mảnh lân cận còn sót; QA chỉ đếm vụn < 12px, không đếm mảnh lớn lạc.
- Backdrop không được vẽ bằng công cụ tạo ảnh.
- Phối cảnh không thống nhất: prop đứng nhìn thẳng, cổng nhìn xiên isometric.

## 4. Prompt gửi Gemini (dán nguyên)

```text
Thí điểm batch-11-tomb: Claude đã chạy audit và xem từng ảnh. Kết quả: 3/10 ĐẠT (gravestone-01, gravestone-02, lantern-spirit), 1/10 SỬA NHỎ (sarcophagus-01), 6/10 VẼ LẠI. Chất lượng prop đã đúng hướng, xin giữ mức này. CHƯA được làm 16 kit còn lại.

SỬA NHỎ (không vẽ lại, chỉ làm sạch):
- tomb-gravestone-01: xóa cụm 13 px lạc ở khoảng (x26–31, y203–205).
- tomb-gravestone-02: xóa 1 px lạc tại (45,208).
- tomb-sarcophagus-01: xóa vạch đứng ở góc trái trên (x14–15, y14–36), vạch giữa trái (x14–18, y123–131), 2 px tại (14,135–136), và nét ký tên/vết ở góc dưới phải. Sau khi xóa phải còn ĐÚNG 1 thành phần liên thông.

VẼ LẠI (từ đầu, bằng công cụ tạo ảnh):
1. tomb-arch-gate: vẽ nhìn MẶT TRƯỚC (billboard), thấy hơi mặt trên (~24°), KHÔNG nhìn xiên isometric 45°. Giữ ý: cổng vòm nghĩa địa, 3 gargoyle, tường đá có lỗ châu mai. Cửa vòm tối đen ở giữa. Không còn mảnh lạc.
2. tomb-portal-dormant và tomb-portal-active: cùng một cổng, cùng khung ảnh, cùng pivot, cùng vị trí vòm (độ lệch ≤ 1 px); chỉ khác ở lõi xoáy và rune phát sáng. Nhìn MẶT TRƯỚC (bậc thang đi xuống phía người xem, không chéo). Không còn mảnh tường/cột lơ lửng. Cả hai phải là đúng 1 thành phần liên thông (hoặc nếu có mảnh vỡ trang trí thì ghi rõ trong qa.json và để cách ≥ 8 px).
3. tomb-brick-floor: tile 512×512 liền mạch THẬT. Cấm lật gương/đối xứng để làm liền mạch. Mép tile phải sáng/tối giống tâm (chênh độ sáng trung bình mép–tâm ≤ 3). Ghép 3×3 không được thấy khung lưới, đường chữ thập, hoặc họa tiết lớn lặp rõ (đổi sang gạch nhỏ hơn, nhiều biến thể gạch, không có "ô to" nổi bật).
4. tomb-graveyard-dirt: như trên. Cấm lật gương. Các chi tiết nổi bật (chùm cỏ, xương) rải ngẫu nhiên, không lặp thành hàng. Ghép 3×3 không thấy sọc đối xứng.
5. tomb-necropolis-wall-far: VẼ bằng công cụ tạo ảnh, không dùng code. Một đường chân trời nghĩa địa: tường thành đá mục, tháp canh, bia mộ, cây khô, trăng, sương, 2–3 tầng chiều sâu (tối dần về xa). Kích thước 1024×384 hiển thị 16 đơn vị world (64 px/đơn vị) lặp được theo trục X (mép trái = mép phải, đo seam). ≥ 24 màu, nhị phân alpha.

BẮT BUỘC KHI NỘP LẠI:
- repeat-3x3.png cho mỗi tile, kèm 1 dòng trong review.md: "đã xem, không thấy lưới/gương/lặp rõ".
- Thêm vào qa.json: chênh độ sáng mép–tâm của tile; số thành phần liên thông và kích thước từng thành phần của prop; ghi rõ cách làm tile liền mạch (không dùng lật gương).
- Làm sạch sheet: sau khi cắt, giữ đúng 1 thành phần lớn nhất cho prop (hoặc liệt kê mảnh phụ có chủ đích). Mở từng final.png xem bằng mắt.
- Nộp lại CHỈ 6 asset vẽ lại + 3 asset đã sửa nhỏ (tổng 9; lantern giữ nguyên). Dừng và chờ nghiệm thu lần 2.
```

## 5. Quy trình tiếp
Nghiệm thu lần 2 kit Lăng Mộ → dựng thử 1 map Lăng Mộ trong engine (`tools/build-web-assets/` tương tự map rừng) → nếu ghép tốt mới mở 16 kit còn lại.

---

# Nghiệm thu lần 2 (2026-10-16 00:20) + dựng thử map `tomb_hd2d`

**Kết luận: 5/10 ĐẠT, 2/10 ĐẠT CÓ ĐIỀU KIỆN, 3/10 VẪN KHÔNG ĐẠT. Chưa mở 16 kit còn lại; nộp lần 3 chỉ 3 asset.**

## Audit lần 2
10/10 qua audit máy, mỗi prop đúng 1 thành phần liên thông (mảnh lạc đã sạch). Máy vẫn không bắt được các lỗi dưới (phải xem ảnh).

| Asset | Kết quả | Ghi chú |
|---|---|---|
| gravestone-01, gravestone-02, sarcophagus-01 | ĐẠT | Sạch mảnh lạc; trong engine đọc rõ, cùng phong cách |
| tomb-lantern-spirit | ĐẠT | 4 khung hoạt động trong engine (`frames:4`) |
| tomb-arch-gate | ĐẠT | Đã nhìn mặt trước, 1 khối, 3 gargoyle. Cửa tối trống, tạm chấp nhận |
| portal-dormant / portal-active | ĐẠT CÓ ĐIỀU KIỆN | Cặp khớp tuyệt đối (cùng mặt nạ alpha 35.166 px, cùng khung 216×276) nên đổi trạng thái không giật. Nhưng cầu thang vẫn chéo như isometric, lệch so với cổng vòm nhìn thẳng. Chấp nhận để dựng; sửa ở lượt sau |
| tomb-brick-floor | KHÔNG ĐẠT | Chênh seam max 9,8 (X) và 12,9 (Y), mép tối hơn tâm (38,7 so với 47,5). Trong engine thấy vệt dọc ở chỗ nối và các khối lớn lặp rõ. Gạch đọc được và đẹp, cần làm liền mạch thật |
| tomb-graveyard-dirt | KHÔNG ĐẠT | Hết lật gương, nhưng dùng dither ô cờ dày. Ở nền cận cảnh thành nhiễu moiré/ô vuông rất chói; bố cục chùm cỏ + xương lặp theo lưới |
| tomb-necropolis-wall-far | KHÔNG ĐẠT | Đã là tranh vẽ, nhưng sai chủ đề (màu be/ô-liu như sa mạc, không phải thành nghĩa địa ban đêm), có vệt/lỗi dọc ở giữa ảnh (x≈490–530, sai lệch màu 25), băng ngang xếp chồng và lật gương, vẫn 8 đv thay vì 16 đv |

## Dựng thử map `tomb_hd2d` trong engine
- Script: `tools/build-web-assets/build_hd2d_tomb_test.py` → `apps/game-web/public/scenes/tomb_hd2d.json` + texture `hd2d_tomb-*`. Xem: `scene.html?map=tomb_hd2d`. Không sửa mã engine.
- Ghép: nền đất, đường lát gạch, 12 bia mộ, 4 quan tài, cổng vòm, cổng dịch chuyển, 6 đèn lồng 4 khung, hạt bụi và đom đóm xanh.
- Kết quả: prop (bia, quan tài, đèn, cổng vòm) ghép tốt, đúng không khí nghĩa địa HD-2D và cùng tầm phong cách batch-01.
- Hạn chế quan sát được: (1) đường gạch lộ vết nối dọc; (2) nền đất cận cảnh nhiễu dither rất chói; (3) không có backdrop nên bầu trời trơ màu phẳng; (4) cổng dịch chuyển dormant nằm ở mép sau, nhìn chéo; (5) ranh giới đất–gạch cắt thẳng vì chưa có decal chuyển tiếp (`tomb-tile-edge-decal` chưa nộp trong thí điểm); (6) bản đã kiểm tra ở mức 24 prop, chưa đủ phủ kín như một map thật.

## Prompt lần 3 gửi Gemini (dán nguyên)

```text
Nghiệm thu lần 2 batch-11-tomb: 5 ĐẠT (gravestone-01, gravestone-02, sarcophagus-01, arch-gate, lantern-spirit), 2 ĐẠT CÓ ĐIỀU KIỆN (portal-dormant/active), 3 CHƯA ĐẠT. Hãy giữ nguyên 7 asset đã ổn, chỉ nộp lại 3 asset dưới đây (và tuỳ chọn 2 cổng, nếu sửa phải giữ cặp khớp mặt nạ alpha tuyệt đối).

1) tomb-brick-floor (512×512): giữ phong cách gạch hiện tại (đẹp) nhưng làm liền mạch THẬT. Đo seam lớn nhất (chênh max pixel mép trái/phải và trên/dưới) ≤ 3. Độ sáng trung bình viền 10 px so với vùng giữa chênh ≤ 3 (hiện 38,7 so với 47,5). Bỏ các khối lớn nổi bật (ô to giữa, thanh chữ thập đậm) để ghép 3×3 không thấy khối lặp.
2) tomb-graveyard-dirt (512×512): bỏ dither ô cờ dày (gây nhiễu moiré khi phóng cận cảnh); dùng cụm màu lớn 3–4 tông, mảng đất mềm, vài viên đá/xương/chùm cỏ nhỏ rải KHÔNG theo lưới. Ghép 3×3 không thấy hàng lặp. Seam ≤ 3.
3) tomb-necropolis-wall-far (1024×384, hiển thị 16 đơn vị world = 64 px/đv): vẽ lại đúng chủ đề thành nghĩa địa ban đêm: tường thành đá mục, tháp canh, bia mộ xa, cây khô, trăng, sương; xanh đen/xanh lục tối, tối dần về xa (2–3 tầng). Không dùng tông be/ô-liu sáng. Không có vệt hay lỗi dọc ở giữa ảnh; mép trái = mép phải (seam ≤ 3). Nhị phân alpha, ≥ 24 màu.

BỔ SUNG nộp thêm 1 asset để map không bị cắt thẳng: tomb-tile-edge-decal (decal chuyển đất → gạch, 512×512, cạnh trên là đất, cạnh dưới là gạch, ghép liền mạch theo trục X).

Quy tắc không đổi: không dùng code để vẽ nội dung, không lật gương để liền mạch, kèm repeat-3x3.png THẬT, review.md ghi đã xem, qa.json ghi seam max, chênh sáng mép–tâm, số thành phần liên thông. Không làm kit khác cho đến khi Claude nghiệm thu lần 3.
```
