# Five PNG atlas candidates — 2026-10-15

Đã vẽ và đóng gói 5 atlas PNG thực tế theo các master mới. Đây là bản để xem và góp ý, **chưa đạt strict visual acceptance và chưa được chọn vào runtime**. Không dùng nguồn video.

Mỗi atlas: RGBA 1124×1405, 4 cột × 5 hàng, 20 frame khác nhau; alpha trong cell-local [22,259). Hàng 1–2 lặp; hàng 3–5 phát một lần và giữ frame cuối.

| Loài | Bản | PNG |
|---|---|---|
| Hươu Rêu Nguyệt | attempt-11 | [PNG](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0153/attempt-11/packed.png) |
| Tinh Vân Long | attempt-13 | [PNG](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0155/attempt-13/packed.png) |
| Ma Nhãn Hư Không | attempt-11 | [PNG](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0157/attempt-11/packed.png) |
| Long Thần Song Ấn | attempt-15 | [PNG](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0159/attempt-15/packed.png) |
| Ma Chủ Song Cực | attempt-15 | [PNG](/Users/phileanh/rust/phimond/apps/game-client/assets/pets/redraws/extension-20261013/species_0160/attempt-15/packed.png) |

## Kiểm tra

- 5/5 atlas đạt kiểm tra cơ học; 20 vùng nguồn phủ toàn bộ ảnh, không xóa alpha để làm sạch giả.
- 33 asset unit tests passed; roster check PASS: 160 authoring records, 152 frozen, 8 authored, không kích hoạt runtime.
- Independent reviewer kiểm tra hash chính xác, raw/packed, 64/96px và playback của từng hàng.
- Giữ nguyên 152 atlas đã chọn, 919 file nguồn/tài sản đóng băng và 3 atlas extension đã duyệt.

## Chưa đạt / cần duyệt

- Hươu: frame lấy đà R3C2 vẫn có vệt FX của frame impact ở mép phải; chưa đạt gate không lẫn fragment. Bản sửa native tiếp theo khiến thân quá nhỏ nên không chọn làm bản xem chính.
- Ma Nhãn: cổng phép hình thoi dễ trông như mắt phụ; xúc tu chồng lấp.
- Long Thần: cần duyệt cánh mới; thứ tự vuốt rồi sáng hai ấn chưa đủ rõ trong aura.
- Ma Chủ: thân nhỏ khi xem 64px; cần duyệt khác biệt skill với đòn thường.
- Tất cả: owner cần xem độ mượt 4 frame và mật độ glow/chất pixel. Mechanical PASS không phải art approval.

## Xem thử

[Review atlas](http://127.0.0.1:8125/#species_0159). Lọc nguồn “8 loài Phimond-authored mới” và duyệt “Bản sửa mới · chờ duyệt” để thấy đúng 5 bản.

Review server PID: 90896, port 8125, log `/tmp/p10-extension-review.log`. Health160 và hash live khớp cả 5 atlas. Game server và DB không đổi trong scope art.

Evidence: [independent review](independent-review.md), [verification](verification.json), [live hashes](live-review-verification.json), [preservation](preservation.json).

Không push/merge/deploy. Các bản lỗi và raw vẫn được giữ để đối chiếu.
