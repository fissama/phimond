# Hoàng thành / Thành phố — bổ sung 2026-10-28

Ba gói ứng viên được vẽ bằng built-in Codex ImageGen theo các prompt trong từng thư mục, sau đó xử lý bằng Sprite Forge `generate2dsprite.py process`. Art gốc và reference hashes nằm cạnh gói tương ứng. Đây là đề xuất sáng tạo theo ảnh tham khảo, không phải asset khôi phục từ APK.

| Gói | Nội dung | Kết quả Forge | Đánh giá bằng mắt | Trạng thái |
|---|---|---|---|---|
| `npcs/` | 6 NPC Hoàng thành: tiểu quan đưa thư, nữ vệ binh, thợ đài phun nước, người bán hoa, trẻ chơi vòng, nhạc công lớn tuổi | Strict process QC pass; palette build/apply pass, 48 màu + alpha nhị phân; raw spill WARN `safe_frame` ở 6/6 ô | Đã mở từng final; dáng/đạo cụ phân biệt. Mỗi final dùng 44–48 màu hữu hình, 192×192 | Chờ owner duyệt; chưa vào roster/runtime |
| `fx/` | 4 frame cánh hoa bay lượn ở quảng trường | Strict process QC pass; palette build/apply pass, 48 màu + alpha nhị phân; raw spill pass | Đã mở từng final; các frame thay đổi vị trí/hướng. 47–48 màu hữu hình, 192×192 | Chờ owner duyệt; chưa vào kit manifest |
| `props/` | kiosk bản đồ, chuông đồng trên bệ, cân chợ, hộp đàn, cọc dây xếp hàng, bồn hoa | Strict process QC pass; palette build/apply pass, 48 màu + alpha nhị phân; raw spill WARN `safe_frame` ở 6/6 ô | Đã mở từng final; vật tách rõ. Mỗi final dùng 33–47 màu hữu hình, 192×192 | Chờ owner duyệt; lưu ý model thay chuông cầm tay thành chuông treo trên bệ |

Ảnh xem nhanh:

- NPC: `npcs/forge-01/sheet-transparent.png`
- FX: `fx/forge-01/sheet-transparent.png`
- Props: `props/forge-01/sheet-transparent.png`

Mọi gói giữ `approved=false` cho tới khi owner xem và duyệt. Chưa sửa `batch-12-city/manifest.json`, checklist kit, runtime, scene hay cờ provisional. Không có test server/client chạy vì đây là asset-only review bundle.

Raw spill report: NPC `npcs/spill-01/sheet-qc.json`, FX `fx/spill-01/sheet-qc.json`, props `props/spill-01/sheet-qc.json`. `cross_cell_components`, `cross_cell_visible`, `sheet_edge`, `empty_cells`, và `boundary_band` đều pass trên cả ba sheet. Cảnh báo duy nhất là khoảng lề raw nhỏ hơn khuyến nghị 15%; các final đã được Forge đăng ký vào canvas 192×192 và không chạm mép output.

Final file order:

- NPC `npc-1.png` đến `npc-6.png`: page, nữ vệ binh, thợ đài phun, người bán hoa, trẻ chơi vòng, nhạc công.
- FX `fx-1.png` đến `fx-4.png`: chu kỳ cánh hoa bay.
- Props `sheet-1.png` đến `sheet-6.png`: kiosk bản đồ, chuông bệ, cân chợ, hộp đàn, cọc dây, bồn hoa.
