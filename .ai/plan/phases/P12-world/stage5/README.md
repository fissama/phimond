# P12 Stage 5 — Validation và review đóng phase

Owner cấp quyền 2026-10-17. Stage 4 đã đóng cùng ngày. **P12 đóng 2026-10-17** sau owner exit review (master spec, P12 Exit).

## Chạy lại kiểm chứng

```
python3 -I .ai/plan/phases/P12-world/stage5/validate.py
```

Chỉ đọc dữ liệu Stage 4 và `review/`, in PASS/FAIL, ghi `validation-result.json`. Kết quả 2026-10-17: **17/17 PASS**.

## Bằng chứng theo yêu cầu

| Yêu cầu | Bằng chứng | Trạng thái |
|---|---|---|
| R01 world graph, portal, hồi phục | Đồ thị 102 liên kết đã duyệt; mọi map trong phạm vi đến được từ Triệu Linh Điện (Huyết Chiến Đài là map sự kiện hằng ngày giờ cố định, vào bằng nhiệm vụ phụ dịch chuyển ở Quảng Trường, không qua cổng) và có đường về Quảng Trường; mẫu 4 vùng nhiều tầng khớp quy tắc | Script PASS, owner đã duyệt |
| R02 phân loại map / NPC | Heal, shop và dịch vụ chỉ ở hub an toàn; 2 map hỗn hợp là ngoại lệ đã duyệt; roster 107 mục, 35/35 thẻ review đã duyệt | Script PASS, owner đã duyệt |
| R03 NPC, spawn, vai trò khám phá | Mọi map quái có điểm spawn (543 APK → 664 đề xuất, `stage4/P12-S4-spawn-plan.json`); danh tính, cấp, XP, drop hoãn có chủ | Script PASS, owner duyệt thẻ spawn |
| R04 template / instance | Điền Trang và Phòng thú cưng riêng từng người chơi; instance và map chung bang theo thẻ S4-INSTANCE đã duyệt; mọi map có nơi hồi sinh | Script PASS, owner đã duyệt |
| R05 route, readability, quay lại vùng cũ | Không map cụt; mọi map có đường hồi phục. Phần đọc hiểu thị giác và thiếu tài nguyên cần chơi thử, chưa có runtime | Owner tạm duyệt 2026-10-17: bản runtime thuộc P01 |
| R06 HD-2D, ràng buộc cho P01 | Stage 3: Three.js, iPhone 17 Pro Max Safari high 60 s: 60 / 59,85 FPS (ADR-0001); art direction mỗi 10 tầng đổi bố cục | Owner chấp nhận 2026-10-17: hiện chỉ đo được iPhone high; macOS Safari, medium, low chưa đo (đã ghi) |

## Chưa giải quyết, cần owner biết

- Không có mục critical nào đang mở trong dữ liệu thiết kế. Script không thay thế việc chơi thử: R05 và R06 chưa có bằng chứng từ client chạy thật, vì P12 không sửa runtime.
- Mục hoãn có chủ (owner đồng ý 2026-10-17, debate lại khi tới phase nhận): xem `P12-closure-checklist.md` §5 (danh tính và cấp quái, hệ số Mật Tầng, drop, race thứ hai U Linh Cổ Thành, logic Bia và Người Dẫn, art theo tầng, U7, social chat).
- Lệch giữa thiết kế và runtime hiện tại: `P12-closure-checklist.md` §4, việc sửa thuộc P01.
- Tên map, 21 điểm đến và vị trí Bia / Người Dẫn: owner đã duyệt.

## Việc để owner đóng phase

1. R05 (tạm duyệt, runtime ở P01) và R06 (chỉ đo được iPhone high): owner đã chấp nhận 2026-10-17.
2. Danh sách hoãn có chủ: owner chấp nhận 2026-10-17.
3. Ra lệnh đóng P12: owner đã ra lệnh 2026-10-17; `PROJECT_PROGRESS` và `ACTIVE.md` đã cập nhật.
