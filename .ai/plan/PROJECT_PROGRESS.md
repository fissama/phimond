# Phimond — Tiến độ dự án

**Cập nhật:** 2026-10-12.
**Nguồn phạm vi/phụ thuộc:** [Master spec §5](PHIMOND_MASTER_SPEC.md#5-roadmap-và-phụ-thuộc).
**Điểm vào công việc:** [ACTIVE.md](../ACTIVE.md).

## Hoàn tất có bằng chứng

| Phạm vi | Kết quả | Bằng chứng |
|---|---|---|
| P00 baseline | Đã đóng 2026-09-24, commit e66350b | [P00](phases/P00-baseline/README.md); latency budget dev FAILED, 50 CCU chưa được chứng nhận |
| P10 pet model design | Đã đóng 2026-09-30 | [Closure](phases/P10-pet-model/P10-closure.md); 152 species baseline (roster hiệu lực 160, xem bảng số liệu ở [ACTIVE.md](../ACTIVE.md)), 8 Race, D01–D46, 23 acceptance scenarios |
| P10 redraw art riêng | **152/152 DONE — 100%**, owner-approved 2026-10-11 | [Redraw closure](phases/P10-pet-model/P10-redraw-closure-20261011.md); nhóm 4★–5★ **48/48** |

## Trạng thái roadmap còn lại

Các trạng thái dưới đây theo tài liệu có trong workspace; chưa có closure không
đồng nghĩa một owner bên ngoài chưa làm việc. Không suy ra % implementation từ
số file hoặc số atlas. ID phase giữ nguyên, thứ tự theo master plan.

| Phase | Trạng thái / đầu ra tiếp theo |
|---|---|
| P11 stats | Scaffold NOT STARTED theo README; công thức, stat/role/Element assignment và O03/O04/O05/O08 |
| P12 world | OPEN. Stage 1 xong phần lớn (còn `review_detailed_scope`); Stage 2 đóng 2026-10-14; Stage 3: Three.js đã chọn (ADR-0001), chờ số đo iPhone; Stage 4–5 chưa có quyền. Chi tiết: `phases/P12-world/P12-closure-checklist.md` |
| P01 world slice | Chưa có closure; phụ thuộc P12, renderer/movement/collision/portal/web HUD |
| P13 skill | Chưa có closure; candidate V7 chờ owner nghiệm thu: 160 loài, 97 skill, 28 recipe candidate; pool/eligibility/Element chart/combat rules |
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

- [Selected manifest](phases/P10-pet-model/redraw-kit/owner-atlas-selection.json): 152 `owner_approved_done`, pin path + SHA-256.
- [Final inventory](phases/P10-pet-model/redraw-kit/completion-20261011/done.json): roster art đủ 152 species.
- [Mechanical evidence](phases/P10-pet-model/redraw-kit/completion-20261011/mechanical.json): 152/152 pass, 20 frame/atlas, RGBA 1124×1405.
- Kiểm tra metadata/hashes ngày 2026-10-12: 152 selected files khớp SHA và 152 bản duyệt khớp phiên bản.
- Bước tích hợp: routing bằng ID, lazy loading/cache, pivot và scale theo tier có ngoại lệ theo loài; idle/move loop, attack/cast/die one-shot; test battle layout và độ rõ ở kích thước game.
- Runtime catalog/save migration, công thức stat và luật Special còn theo phase sở hữu; art closure không đóng O01–O08 của P10.

**Không có % hoàn thiện toàn project được chứng nhận.** 100% chỉ áp dụng cho phạm vi redraw 152 species đã được chủ dự án nghiệm thu.
