# Đối chiếu APK và video — Phimond, 17/09/2026

Đây là đợt khôi phục và tích hợp asset đầu tiên, **chưa phải bản sao 100%**. Tạm dùng asset 3.2 làm nguồn tích hợp và video làm nguồn đối chiếu hình ảnh, trong khi chờ chọn phiên bản ưu tiên. Không chạy APK, không gọi dịch vụ của APK, không chuyển dữ liệu người dùng sang hệ thống khác.

## Dữ liệu đọc được

| Nguồn | Texture2D | Sprite | AnimationClip | Scene khai báo |
|---|---:|---:|---:|---:|
| Spirit Beast World 3.2.apk | 1.313 | 1.347 | 780 | 25 |
| Spirit Beast World 8.4.xapk | 1.314 | 1.347 | 780 | 25 |

- Mỗi bản có ba Font Texture không chứa ảnh có thể xuất bằng bộ giải mã hiện tại. Các lỗi được ghi trong inventory, không tính là xuất thành công.
- 3.2 xuất thành công 5.355 đối tượng thuộc các loại đã chọn; 8.4 xuất 4.280. Đây không phải số lượng asset gameplay độc lập: có texture/sprite trùng dữ liệu và metadata script.
- Sau xuất PNG: 1.208 texture duy nhất trong mỗi bản, 1.205 texture có nội dung giống hệt giữa hai bản.
- XAPK 8.4 khai báo package `com.HCGame.SpiritBeastWorld`, versionCode 37. Tên file/version không chứng minh đây là cùng bản lịch sử xuất hiện trong video.
- Đã dựng ảnh tham chiếu của 101 nhóm cảnh bằng hierarchy, tọa độ, scale, pivot, flip, màu và thứ tự sprite. Bộ ghép bỏ qua 15 sprite dùng rotation/draw mode chưa hỗ trợ; không phải trình mô phỏng Unity đầy đủ.
- Đã truy liên kết AnimatorController để lấy chuỗi sprite cho 155 actor. Thời lượng clip được đọc, nhưng preview chia đều thời gian giữa các frame; chưa giải mã lịch keyframe nén đầy đủ.
- Không thấy đối tượng AudioClip trong bundle đã đọc; chưa có bộ âm thanh xác minh được.
- Cấu trúc MonoBehaviour tùy biến bị thiếu type tree; thử đọc trả về số byte không khớp. Chưa khôi phục được đầy đủ cấu hình gameplay hoặc logic IL2CPP. Không suy ra công thức server từ tên class.

Inventory có hash nguồn và scene: [reference/inventory.json](reference/inventory.json).

## Quan sát video

Video H.264 1280×720, 30 fps, dài 273,286 giây. Mốc dưới đây là mốc lấy mẫu; không phải ranh giới chính xác của từng cảnh.

| Mốc | Bằng chứng nhìn thấy | Giới hạn |
|---|---|---|
| 00:00–00:30 | Đoạn giới thiệu, giao diện khác nhau và màn hình tải | Không dùng montage để suy luận một bộ luật duy nhất |
| 00:45–01:30 | Cổng cung điện, nhân vật/thú pixel, thanh trạng thái, cụm nút tròn, bảng chat dưới cùng | Chưa biết tọa độ/collision gốc |
| 01:45–02:15 | Danh sách/menu thú, thao tác lựa chọn và menu tương tác | Không thấy toàn bộ hệ thống lai tạo |
| 03:00–03:30 | Khu vực hang, nhiều thực thể, menu kỹ năng | Chưa đủ kết luận mô hình thời gian/turn của chiến đấu |
| 03:30 | Tooltip kỹ năng nước ghi sát thương 44 lên tất cả địch; danh sách có giá trị MP 12 và 43 | Một giá trị hiển thị không xác minh công thức sát thương |
| 03:45–04:15 | Quảng trường và bãi biển với sóng, thực thể và HUD | Chưa có đầy đủ bản đồ, nhiệm vụ và tiến trình |

[Bảng hình video](reference/video-overview.jpg) · [Khung 03:30](reference/video-0210.png) · [Cảnh ghép từ APK](reference/rooms-overview.jpg).

## Đã tích hợp vào Phimond

- Năm nền cảnh: quảng trường QTTP, rừng Map2, bãi biển BaiBien, nông trại NongTrai, đấu trường DauTruong. Đây là ánh xạ sang năm map hiện có; chưa thay topology/điều kiện mở map bằng dữ liệu gốc.
- Sprite nhân vật Boy với idle/run, mười thú đã ánh xạ theo tên actor và hình ảnh. Bốn loài tiến hóa riêng của Phimond chưa có ánh xạ xác minh, không tự gán sprite thú khác.
- Hiển thị thú đang đồng hành và các đơn vị trong trận, thanh HP; hình thú trong bảng thông tin và website đồng hành.
- Khung panel lấy từ APK và tông xanh–vàng. Bố cục desktop hiện có vẫn khác HUD/video; chưa dựng đủ D-pad, toàn bộ menu hay chat MMO.
- 133 file được nhập cho game/web; nguồn và SHA-256 ghi trong `apps/game-client/assets/reference/provenance.json`.

Ảnh chạy thật với dữ liệu fixture: [phimond-first-integration.png](reference/phimond-first-integration.png).

## Cần giải quyết để tiến gần bản tham chiếu

1. Chốt video, 3.2 hay 8.4 làm bản chuẩn khi chúng khác nhau.
2. Khôi phục layout HUD, font, menu, NPC, hiệu ứng và keyframe timing, đối chiếu từng màn ở cùng độ phân giải.
3. Khôi phục topology/collision/portal, bảng thú/kỹ năng/vật phẩm/nhiệm vụ theo đúng bản chuẩn.
4. Thu thập bằng chứng cho chiến đấu, bắt thú, tăng trưởng, lai tạo, rơi đồ, kinh tế; giữ mọi công thức hiện tại ở trạng thái reconstructed cho đến khi xác minh.
5. Triển khai các hệ thống MMO còn thiếu và xử lý lỗi timeout/session đã ghi ở báo cáo kiểm thử. Asset mới không sửa lỗi đó.

## Tái tạo kết quả

Chạy từ thư mục gốc. Môi trường Python dùng UnityPy 1.25.3, Pillow 12.3.0; cache không đưa vào source control.

```sh
uv venv tools/.cache/asset-venv
uv pip install --python tools/.cache/asset-venv/bin/python UnityPy==1.25.3 Pillow==12.3.0
tools/.cache/asset-venv/bin/python tools/assets/extract_unity.py '/path/Spirit Beast World 3.2.apk' tools/.cache/reference/apk-3.2
tools/.cache/asset-venv/bin/python tools/assets/extract_unity.py '/path/Spirit Beast World 8.4.xapk' tools/.cache/reference/apk-8.4
tools/.cache/asset-venv/bin/python tools/assets/compose_rooms.py '/path/Spirit Beast World 3.2.apk' tools/.cache/reference/rooms
tools/.cache/asset-venv/bin/python tools/assets/export_actors.py '/path/Spirit Beast World 3.2.apk' tools/.cache/reference/actors
python3 tools/assets/import_selected.py
```

## Kiểm tra sau tích hợp

- Godot reference smoke: năm cảnh, frame animation, ánh xạ thú và trường hợp thiếu asset — PASS.
- Godot fixture smoke: sáu panel, trận đấu, lineage, lỗi và revision — PASS; đã chạy native và kiểm tra ảnh.
- Godot live smoke: đăng ký, WS, NPC/shop/heal, di chuyển/cổng, nhiệm vụ, battle defend/reconnect/flee, logout/login và phục hồi dữ liệu — PASS.
- Next.js TypeScript — PASS. Browser xác nhận ảnh Moss Snail tải thành công, kích thước nguồn 44×42.
- Không xác nhận parity 100%, tính đúng của mọi scene ghép, toàn bộ animation hay công thức server.
