# Đánh giá Nghệ thuật & Nghiệm thu Kit Hoang Mạc (batch-11-desert) — Kết Luận & Hoàn Thiện Triệt Để (Round 6)

## 1. Kết Luận Nghiệm Thu & Mốc Chuẩn (2026-10-17)

- **Trạng thái**: **ĐẠT CÓ ĐIỀU KIỆN (Chốt làm mốc chuẩn cho toàn bộ 17 kit)**.
- **Audit**: 85 asset, 0 cảnh báo, 0 trùng hash, sha256 và kích thước đĩa khớp 100% manifest.
- **Ảnh kiểm tra thực tế (3 camera + Zoom 2×)**:
  - `desert_cam_015.png`: Cổng đá vòm, bậc thang sa thạch, phế tích tường, lều du mục, cồn cát chân thoải tự nhiên.
  - `desert_cam_050.png`: Khe nứt vực thẳm tiền cảnh, lều lớn, bếp than, xương sọ quái khổng lồ, gạch chìm dưới cột không còn mép vuông.
  - `desert_cam_085.png`: Nhân sư bóc trọn vẹn hông/đuôi không còn hộp đáy/mép cắt; cồn cát `sand-dune-medium` vuốt nhọn tự nhiên cả 2 đầu (hết 2 vạch cắt đứng x≈305 và x≈545); đĩa spawn tròn hoàn hảo không còn đế vuông.
  - `desert_transition_zoom_2x.png`: Vùng tiếp giáp sàn cát và decal gạch/vết chân/vệt gió loang tự nhiên, triệt tiêu mọi cạnh cắt ngang 74px.

---

## 2. Chi Tiết Khắc Phục Triệt Để Round 6

| # | Hạng mục tồn đọng | Phản hồi của Reviewer | Xử lý Round 6 |
|---|---|---|---|
| **1** | `sand-dune-medium` | Hai cạnh dọc cắt vuông x≈305 và x≈545, lộ vùng sáng chữ nhật. | Trích xuất tươi từ sheet gốc với khung mở rộng $[520, 580 \to 1005, 900]$. Giữ trọn đường dốc tự nhiên bắt đầu từ 1 px (bên trái) và vuốt về 6 px (bên phải). Bỏ việc cắt cụt dải taper theo component. Triệt tiêu hoàn toàn 2 vách đứng và vùng sáng chữ nhật. |
| **2** | Đế nhân sư (`desert-sphinx-ruin`) | Đế hình chữ nhật nhạt bên phải và quanh móng. | Trích xuất tươi từ sheet mở rộng $[600, 480 \to 1024, 765]$, giữ trọn vẹn phần thân/đuôi vuốt tự nhiên về 0 tại $x=403$ (khắc phục vết cắt 115 px ở $x=960$). Tách sạch mảng nền hình chữ nhật xung quanh. |
| **3** | Đĩa spawn (`ancient-rune-faded`) | Đế hình chữ nhật nhạt bao quanh đĩa tròn. | Áp dụng mặt nạ hình tròn chuẩn bán kính $r \le 114\text{ px}$, cắt bỏ hoàn toàn 4.925 pixel của khung chữ nhật bao ngoài. Đĩa phù văn tròn tuyệt đối. |
| **4** | Decal `wind-sand-01/02` | Cạnh đáy bị cắt phẳng ngang, vệt tối hơn sàn. | Cắt gọt và vuốt nhọn tự nhiên hình trăng khuyết/hình thoi hai đầu (taper về 0 ở cả đỉnh và đáy), xóa bỏ đường cắt ngang 74 px và vạch khung thừa ở mép trái. |
| **5** | Gạch dưới cột (`sunken-bricks` & `sandstone-rubble`) | Bị cắt phẳng ngang ở đáy (cam 0.5 & 0.15). | Xói mòn chu vi theo đường zíc-zắc gồ ghề của từng viên đá lát chìm, không còn cạnh bao hình chữ nhật. |
| **6** | 6 `desert-shadow-*` | Quá đen đặc, dither toàn hạt nhiễu (370–2.903 components). | Chuyển sang dạng **procedural gradient mềm** (màu nâu ấm trung tính `#68482A`, alpha xuyên tâm từ 43% ở tâm giảm dần đều êm ái ra 0 ở viền). Không dither hạt, gắn vật xuống sàn tự nhiên. |
| **7** | `contact-sheet.png` | Chưa được cập nhật ở vòng trước. | Đã kết xuất lại toàn bộ 85 asset mới nhất vào `contact-sheet.png`. |

---

## 3. Quy Tắc Bắt Buộc Đã Thống Nhất Cho Núi Phong Thạch & Lăng Mộ

1. **Bóng đổ (Shadows)**: Cho phép tạo bằng procedural gradient mềm (radial smooth alpha fade), cấm dùng 1-bit dither Bayer toàn hạt làm vỡ vụn.
2. **Decal chuyển tiếp (Edge & Transition Decals)**: **CẤM LÀM BẰNG CODE TOÁN HỌC**. Bắt buộc phải vẽ bằng công cụ tạo ảnh như các asset khác để giữ hình thái tự nhiên hữu cơ.
3. **Quy trình nghiệm thu bắt buộc**: Mỗi kit khi hoàn thành phải tự render scene và nộp đủ:
   - **Ảnh render 3 camera** (0.15, 0.50, 0.85).
   - **Ảnh zoom 2× vùng chuyển tiếp sàn/decal** để kiểm tra mép cắt và độ hòa trộn trước khi báo cáo.
