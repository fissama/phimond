# GPT redo từ Batch 10 — thứ tự và hiện trạng (2026-10-19)

Dán theo thứ tự: `00-master-v2.md` (mọi phiên) + MỘT trong `01`, `02`, `03`.

| Batch | Người vẽ | Hiện trạng | Việc |
|---|---|---|---|
| 00–06 | GPT | chuẩn style (batch-01 rừng là mẫu: 32–48 màu, alpha nhị phân) | giữ |
| 07–09 (UI/icon/FX) | GPT | audit cảnh báo COLORS và SEMI_ALPHA (icon alpha mềm trung vị ~0.36) | owner quyết: chấp nhận (waiver) hay GPT làm lại icon alpha nhị phân |
| 05 (NPC) | GPT | có sprite NPC trùng nhau (cần owner xác nhận khi xem contact-sheet) | tùy chọn: vẽ lại phần trùng, kèm roster 54 NPC |
| 10 | Gemini | sơn dầu, nhiều màu, chữ nướng | LÀM LẠI: `01-batch-10-redo.md` |
| 11 desert | GPT | 98 asset, gate sạch; dùng dựng thử, chưa duyệt. Backdrop chưa được Claude xem bằng mắt | xử lý boulder/backdrop-far theo review; xem [`kit-desert.md`](../map-checklists/kit-desert.md) |
| 11 windrock | GPT | 79 asset (9 floor, 36 prop, 3 backdrop, 16 decal, 6 shadow, 1 marker, 6 FX, 2 portal), 0 duyệt; còn edge-01..03 | tiếp tục theo [`kit-windrock.md`](../map-checklists/kit-windrock.md); bảng 74 dòng vẫn là inventory Gemini |
| 11 nightmare | GPT | 67 asset, 0 duyệt; floor repeat lộ lưới; edge-02/03 và far backdrop bị loại theo log Codex; backdrop chưa được Claude xem | redraw blocker và xử lý 4 landmark-02 theo [`kit-nightmare.md`](../map-checklists/kit-nightmare.md) |
| 11 crossroads | GPT | 59 asset, 0 duyệt; floor repeat pattern còn rõ; thiếu 3 edge và backdrop-far đạt yêu cầu theo log Codex; backdrop chưa được Claude xem | tiếp tục theo [`kit-crossroads.md`](../map-checklists/kit-crossroads.md) |
| 11 tomb | GPT | 76 candidate assets, 0 approved; gate sạch; đã redraw portal/backdrops/FX và map foliage; landmark rows dùng prop chung | Claude/owner review và composite scene theo [`kit-tomb.md`](../map-checklists/kit-tomb.md) |
| 11 ancient | GPT | 55 candidate assets, 0 approved; latest gate 525 assets / 0 errors / 0 warnings; all drawn checklist rows complete; map-scale composite and owner visual review pending | tiếp tục sang kit kế tiếp; review theo [`kit-ancient.md`](../map-checklists/kit-ancient.md) |
| Các kit còn lại | chưa vẽ | — | theo hàng đợi [`REDRAW-QUEUE-20261024.md`](../map-checklists/REDRAW-QUEUE-20261024.md) và checklist 21 kit |
| Bố cục map | Gemini/GPT | benchmark: `map-layouts/desert/desert_entrance` | `03-map-layout-gpt.md` |

Quy trình: GPT nộp theo chặng → Claude chạy `tools/check_hd2d_art.sh` + xem ảnh → dựng cảnh → báo kết quả. Cổng hiện quét `batch-11-*`; muốn gồm batch-10 chạy `art_gate.py --all` (Claude chỉnh).


World Tree 2026-11-05: 48 candidates, 0 owner approvals; FX-01..03 and floor-extra-01..04 are candidates. One floor extra, three edges, far-backdrop checklist reconciliation and map-scale compositions remain. See `PROGRESS.md` and `.ai/design/map-checklists/kit-world_tree.md`.
