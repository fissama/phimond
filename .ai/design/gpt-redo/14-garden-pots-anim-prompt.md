# Đơn 14 — Căn Mạch Linh Viên: 5 chậu có chuyển động (sprite atlas)

- Ngày: 2026-11-09. Dán master v2 + file này. Một phiên = MỘT chậu (hoặc pilot G1). 5 atlas.
- **Pilot trước:** vẽ G1 + duyệt pipeline (atlas, anim.json, ghép với cây pilot ở Đơn 15) rồi mới vẽ G2–G5.
- Định dạng theo chuẩn atlas linh thú (P10-redraw-plan.md): 4 cột × 5 hàng, mỗi hàng là một animation; hàng 1–2 lặp, hàng còn lại chạy một lần. Khác pet: ô 192×192.
- Thư mục: `art/src/hd2d/garden-b/pot-g1-tho-dao/` … (mỗi chậu một thư mục: raw-01.png, final.png, anim.json, prompt.md, review.md, qa.json, preview-anim.gif/strip).
- Engine lo (KHÔNG vẽ sẵn): tối dần theo màn, tint ánh sáng, aura biến dị, sáng/tối theo cổng.

## Hợp đồng atlas

- `final.png` RGBA 768×960; ô 192×192; 20 ô đều có nội dung, KHÔNG ô nào trùng ô khác.
- Mọi pixel alpha > 0 nằm trong [16, 176) theo cả x và y của ô (16 px trong suốt mỗi bên). Hiệu ứng cũng ở trong ô; không hiệu ứng nào vượt ô.
- Alpha nhị phân. Không antialias, không bloom, không blur, không glow nướng (tia sáng = cụm pixel).
- Màu: thân chậu 33–48 màu + riêng hiệu ứng ≤ 12 màu; tổng ≤ 60 màu mỗi atlas.
- Neo: tâm miệng chậu (nơi cây mọc) ở đúng (96, 112) của MỌI ô, sai số ≤ 2 px. Đáy chậu chạm y = 176 ở mọi ô (chậu đứng yên; chỉ có đất, hiệu ứng, chi tiết nhỏ chuyển động). Thân chậu rộng 112–144 px, rim ở y ≈ 100–116. Phần trên rim (y 16–96) dành cho hiệu ứng.
- Cây được vẽ riêng (Đơn 15) và engine đặt lên chậu tại neo (96,112), nên miệng chậu phải là đất/miệng trống, không có cây.
- Cùng một chậu trong cả 20 ô: cùng vật liệu, hoa văn, số chi tiết, silhouette, bảng màu.

## Hàng animation (mỗi hàng 4 khung)

| Hàng | Tên | Phát | Nội dung |
|---|---|---|---|
| 1 | idle | lặp, 3 fps | Chậu khô, chuyển động rất nhẹ theo vật liệu (xem bảng cấp). Khung 4 → 1 liền mạch |
| 2 | wet | lặp, 4 fps | Đất sẫm ẩm, bề mặt đất lấp lánh nhẹ, vài hạt nước nhỏ ở rim |
| 3 | water | một lần, 8 fps | Nước rơi xuống miệng chậu (không vẽ bình tưới) → bắn tung nhỏ → thấm xuống → đất sẫm lại; khung 4 trùng khung 1 của hàng wet |
| 4 | upgrade | một lần, 8 fps | Mảnh vỏ/ánh linh khí tụ lại quanh chậu → chớp một khung sáng bằng cụm pixel → hoàn chỉnh; khung 4 trùng khung 1 hàng idle |
| 5 | clear | một lần, 10 fps | Sau thu hoạch: bụi đất tơi bốc lên rồi lắng, đất trở lại trống; khung 4 trùng khung 1 hàng idle |

## 5 cấp chậu (một cấp = một phiên)

| Cấp | Tên | Vật liệu và hình | Chuyển động idle |
|---|---|---|---|
| G1 | Thổ Đào Bồn | Gốm nung thô, đắp tay, mẻ miệng, nâu cam đất | Vụn đất nhúc nhích 1 px, bụi nhỏ |
| G2 | Trùng Giáp Bồn | Gốm gia cố bằng các tấm giáp sâu bọ xếp lớp, nâu hổ phách ánh xanh rêu | Vài tấm giáp rung nhẹ, một tấm ánh lên rồi tắt |
| G3 | Căn Mộc Bồn | Thùng gỗ quấn đai rễ, một mầm lá nhỏ mọc bên hông | Mầm lá đung đưa, đai rễ co giãn 1 px |
| G4 | Linh Thạch Bồn | Chậu đá xám xanh khắc, dải rune hổ phách quanh thân | Rune sáng chạy dọc dải, 4 nhịp, bằng cụm pixel |
| G5 | Tinh Mạch Bồn | Vỏ đá tối khảm mạch tinh thể vàng nhạt, mảnh pha lê quanh rim | Ánh sáng chạy dọc mạch tinh thể; mảnh pha lê lóe |

Lưu ý: bảng màu họ ấm (nâu, cam, hổ phách, ngà). Màu nhấn xanh/tím theo màn do engine chiếu; không vẽ neon. Cấp cao có silhouette cầu kỳ hơn nhưng cùng cỡ 112–144 px để các cấp thay nhau được.

## anim.json (mỗi atlas)

{"cell":[192,192],"cols":4,"anchor":[96,112],"rows":[{"name":"idle","fps":3,"loop":true},{"name":"wet","fps":4,"loop":true},{"name":"water","fps":8,"loop":false},{"name":"upgrade","fps":8,"loop":false},{"name":"clear","fps":10,"loop":false}]}

## Prompt cho image_gen

```text
Bạn là art worker của Phimond (HD-2D Octopath, pixel art). Vẽ MỘT sprite atlas 4 cột × 5 hàng của một chậu cây dưới lòng đất, mỗi ô là một khung hoạt họa, theo chuẩn atlas linh thú. Cấp chậu: <G1..G5 — tên, vật liệu, chuyển động idle theo bảng>.
Ảnh tham chiếu đính kèm (thứ tự): (a) batch-01-octopath/exposed-roots, pebbles-01 final.png; (b) garden-a/gd-ledge-cap-l, gd-roots-hang-04, gd-decor-06 final.png (đã duyệt) → họ màu, outline; (c) DocDangNu/sprites.png và DaoThienDuong/sprites.png → CÁCH BỐ CỤC ATLAS 4×5, độ dày outline, đổ khối pixel-cluster, cách chia khung chuyển động. Ghi sha256 vào prompt.md.
Yêu cầu: nền #FF00FF phẳng, mỗi ô giữ một khoảng cách ≥ 16 px với mép ô, mọi hiệu ứng ở trong ô. Góc nhìn thẳng mặt trước, nhìn xuống nhẹ như linh thú. Tâm miệng chậu cố định tại (96,112) của ô 192×192 ở MỌI khung, đáy chạm y = 176. Miệng chậu để trống đất (cây vẽ riêng). Ánh sáng: key ấm từ trên-trái-trước. Không bóng đổ xuống đất, không sương, không chữ, không nhân vật, không glow/bloom.
20 khung hoạt họa: hàng 1 idle (lặp), hàng 2 wet (lặp), hàng 3 water (một lần), hàng 4 upgrade (một lần), hàng 5 clear (một lần), như bảng. Chuyển động nhỏ, rõ nhịp, đọc được ở kích thước 96 px. Mỗi khung khác nhau thật (không chép một khung 4 lần).
Hậu xử lý (code chỉ để cắt ô, khử nền, đưa về bảng màu, ghép đúng 768×960 bằng nearest-neighbor, kiểm). Không dùng code sinh hay vá hình.
```

## Nghiệm thu (Claude)

1. Cơ học: 768×960; 20 ô có nội dung và khác nhau; alpha nhị phân; mọi pixel trong [16,176); neo (96,112) ±2; đáy y=176; màu ≤ 60; báo bounds từng ô.
2. Chuyển động: render preview 4 hàng lặp và 3 hàng một lần; khung nối (water→wet, upgrade/clear→idle) liền mạch; không giật silhouette.
3. Hình: cùng chậu ở 20 khung; khác rõ giữa các cấp; đọc được ở 96 px; style khớp batch 00–09 và garden-a đã duyệt.
4. Ghép thử: đặt lên neo cùng cây pilot (Đơn 15) trong mock tầng 10 chậu một hàng.

## Bản sửa v2 (Claude review 2026-11-09, pot-g1-tho-dao REDO)

Lỗi pilot: chậu trôi trái 4 px (x 42→38) qua 4 cột ở mọi hàng; giữa các khung vẫn ~5300 px khác sau căn thẳng (đổ khối nhấp nháy); ba khung kết thúc không khớp khung đích; hàng wet không sẫm hơn idle (độ sáng đất 85.8 so với 85.0); upgrade chỉ là tia sáng.
Yêu cầu thêm:
1. Chậu ĐỨNG YÊN: bounding box x của thân chậu giống nhau ở cả 20 khung (±1 px). Không trôi theo cột.
2. Vẽ khung 1 hàng idle làm gốc; các khung khác chỉ đổi phần chuyển động (vụn đất, bụi, nước, tia sáng, đất trong miệng). Thân chậu giữ nguyên pixel. Sau căn thẳng, ≤ 5% pixel thân chậu khác giữa hai khung liền kề.
3. Khung nối: khung 4 hàng water giống khung 1 hàng wet, khung 4 hàng upgrade và clear giống khung 1 hàng idle, sai khác ≤ 1% pixel.
4. Hàng wet: đất trong miệng SẪM hơn rõ (độ sáng trung bình thấp hơn idle ≥ 20%), bề mặt bóng ẩm, vài hạt nước.
5. Hàng upgrade: mảnh vỏ/ánh linh khí bay vào quanh chậu, tụ lại, một khung sáng bằng cụm pixel, rồi chậu hoàn chỉnh. Không chỉ vài tia lấp lánh.
6. Chậu có thể có tính cách nhẹ (một chớp sáng như con mắt trong đất ở G4–G5), nhưng không có mặt như Linh Thảo.
