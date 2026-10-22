# Đánh giá phong cách HD-2D (Octopath Traveler) – v1.0.1 đợt 3

Thang: ✔ đạt · ◐ một phần · ✘ chưa có. Nguồn so sánh: đặc trưng HD-2D của Octopath (sprite pixel đặt trong cảnh 3D, tilt-shift, bloom, ánh sáng/màu theo thời điểm, chiều sâu nhiều lớp).

| Yếu tố | Hiện trạng | Việc còn lại |
|---|---|---|
| Sprite pixel trong không gian 3D | ✔ Sprite billboard nghiêng −0.42 rad, camera pitch 0.66, FOV 24 (nhìn xa, ít méo). | – |
| Tilt-shift / dải nét giữa | ✔ Mờ dải trên/dưới 8 điểm (Cao 1.0, Trung bình 0.6). | Chưa đo trên GPU thật. |
| Bloom ở vùng sáng | ✔ Cao: UnrealBloom nửa độ phân giải, mạnh hơn về đêm. | D4: đo iPhone/Safari. |
| Phối màu theo giờ | ✔ Đợt 3: tách tông (bóng tối ngả xanh tím, vùng sáng ngả cam), tương phản và tối góc tăng về đêm; bình minh hồng, giờ vàng cam, chạng vạng tím, đêm xanh sâu. Sảnh trong nhà ánh nến ấm cố định. | Tinh chỉnh bằng mắt trên màn thật. |
| Đèn điểm / quầng sáng | ◐ Quầng cộng sáng + tia nắng + hạt bụi là sprite cộng sáng, chưa phải ánh sáng thật. | D12: đèn điểm thật, bóng đổ theo giờ. |
| Chiều sâu nhiều lớp | ◐ Rừng có tán xa/thân giữa/bụi trước; sảnh có cột, cờ, chậu. Thành phố dựa vào mặt tiền. | Cây/tán gần camera mờ (depth-of-field thật) ở rừng. |
| Trận đấu cảnh ngang | ◐ Cảnh DOM: nền là cảnh thế giới làm mờ + tối góc, quái trái/đồng đội phải, bóng đất, lướt tới khi đánh, nhấp nháy khi trúng. Chưa phải sân khấu 3D riêng. | Nền trận riêng theo địa hình (GPT) và camera diorama trong engine: xem `GPT-REMAINING.md` mục Trận đấu. |
| Hoạt họa chiến đấu | ◐ Dùng hàng idle/attack/down của atlas; chưa có hiệu ứng kỹ năng (tia, hạt). | Sprite hiệu ứng kỹ năng theo hệ. |
| Chữ/UI | ✔ Khung vàng, thanh chỉ số khung riêng, số sát thương pixel. | Khung chat sáng như game gốc (xem GPT-REMAINING). |
| Nước, thời tiết | ✘ | D12. |

Kết luận: nền tảng HD-2D đã đủ ở mức "nhận ra phong cách" (tilt-shift + bloom + phối màu + viền nhiều lớp); chênh lệch lớn nhất so với Octopath là ánh sáng thật và sân khấu trận đấu riêng.
