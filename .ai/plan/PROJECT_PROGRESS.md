# Phimond — Tiến độ dự án

**Cập nhật:** 2026-10-21 (P10redrawart).
**Nguồn phạm vi/phụ thuộc:** [Master spec §5](PHIMOND_MASTER_SPEC.md#5-roadmap-và-phụ-thuộc).
**Điểm vào công việc:** [ACTIVE.md](../ACTIVE.md).

## Hoàn tất có bằng chứng

| Phạm vi | Kết quả | Bằng chứng |
|---|---|---|
| P00 baseline | Đã đóng 2026-09-24, commit e66350b | [P00](phases/P00-baseline/README.md); latency budget dev FAILED, 50 CCU chưa được chứng nhận |
| P13 skill design | Đã đóng 2026-10-20 | [Closure](phases/P13-skills/P13-closure.md); V7.1 hash 57c07796…; chi phí vàng/pacing thuộc P15/P19 |
| P10 pet model design | Đã đóng 2026-09-30 | [Closure](phases/P10-pet-model/P10-closure.md); 152 species baseline (roster hiệu lực 160, xem bảng số liệu ở [ACTIVE.md](../ACTIVE.md)), 8 Race, D01–D46, 23 acceptance scenarios |
| P10 redraw art riêng | **160/160 CLOSED —100%art**, owner-approved2026-10-21 | [160-art closure](phases/P10-pet-model/P10-redraw-closure-160-20261021.md); nhóm4★–5★ **56/56** |

## Trạng thái roadmap còn lại

Các trạng thái dưới đây theo tài liệu có trong workspace; chưa có closure không
đồng nghĩa một owner bên ngoài chưa làm việc. Không suy ra % implementation từ
số file hoặc số atlas. ID phase giữ nguyên, thứ tự theo master plan.

| Phase | Trạng thái / đầu ra tiếp theo |
|---|---|
| P11 stats | Scaffold NOT STARTED theo README; công thức, stat/role/Element assignment và O03/O04/O05/O08 |
| P12 world | **ĐÓNG 2026-10-17** (owner exit review). Stage 2 đóng 2026-10-14; Stage 3 đóng 2026-10-16 (Three.js, ADR-0001; iPhone high ~60 FPS); Stage 4 và 5 đóng 2026-10-17 (validate.py 17/17, 12 mục hoãn có chủ, R05 tạm duyệt, R06 chỉ đo iPhone high). Chi tiết: `phases/P12-world/P12-closure-checklist.md` |
| P01 world slice | Chưa có closure; phụ thuộc P12, renderer/movement/collision/portal/web HUD |
| P19 items | Chưa có closure; item foundation, mailbox, EXP share |
| P02 PvE | Chưa có closure; battle 1v3 và render animation/effect thật |
| P14 equipment | Chưa có closure; trang bị và ngân sách sức mạnh |
| P15 training | Chưa có closure; EXP, level vùng, pacing |
| P20 recipe | Chưa có closure; công thức theo species và nguồn học (P13 đề xuất 28 recipe candidate; 17 recipe APK chỉ là bằng chứng) |
| P03 pet UI | Chưa có closure; quản lý pet/inventory/appraisal |
| P16 breeding | Chưa có closure; fusion/reinforcement/egg/hatch/restoration |
| P04 onboarding | Chưa có closure; quest và core loop |
| P05 solo alpha | Chưa nghiệm thu M1; polish/HD-2D/web/device/playtest |
| P06 shared world | Chưa nghiệm thu 50 CCU |
| P07 party/PvP | Chưa nghiệm thu M2 |
| P08 economy | Nhánh M3 tùy chọn; chưa có closure |
| P17 campaign | Chưa có closure |
| P09 release | Chưa nghiệm thu M4 |
| P18 side stories | Sau baseline phát hành; chưa có closure |

## Atlas sẵn sàng bàn giao, tích hợp chưa nghiệm thu

- [Selected160manifest](phases/P10-pet-model/redraw-kit/owner-atlas-selection-160.json):160 `owner_approved_done`, pin path + SHA-256.
- [Final inventory](phases/P10-pet-model/redraw-kit/completion-20261021/done.json): roster art đủ160species.
- [Mechanical evidence](phases/P10-pet-model/redraw-kit/completion-20261021/mechanical.json):160/160pass, 20 frame/atlas, RGBA 1124×1405.
- Kiểm tra2026-10-21:160selectedpath/hash khớp,304sourcePNG giữ nguyên;68unit testsPASS.0147 được duyệt là PNG+registeredprofile, không phải native170px/drop-inatlas.
- Bước tích hợp: routing bằng ID, lazy loading/cache, pivot và scale theo tier có ngoại lệ theo loài; idle/move loop, attack/cast/die one-shot; test battle layout và độ rõ ở kích thước game.
- Runtime catalog/save migration, công thức stat và luật Special còn theo phase sở hữu; art closure không đóng O01–O08 của P10.

**Không có % hoàn thiện toàn project được chứng nhận.** 100% chỉ áp dụng cho phạm vi redraw160species đã được chủ dự án nghiệm thu.
