# GPT redo từ Batch 10 — thứ tự và hiện trạng (2026-10-19)

Dán theo thứ tự: `00-master-v2.md` (mọi phiên) + MỘT trong `01`, `02`, `03`.

| Batch | Người vẽ | Hiện trạng | Việc |
|---|---|---|---|
| 00–06 | GPT | chuẩn style (batch-01 rừng là mẫu: 32–48 màu, alpha nhị phân) | giữ |
| 07–09 (UI/icon/FX) | GPT | audit cảnh báo COLORS và SEMI_ALPHA (icon alpha mềm trung vị ~0.36) | owner quyết: chấp nhận (waiver) hay GPT làm lại icon alpha nhị phân |
| 05 (NPC) | GPT | có sprite NPC trùng nhau (cần owner xác nhận khi xem contact-sheet) | tùy chọn: vẽ lại phần trùng, kèm roster 54 NPC |
| 10 | Gemini | sơn dầu, nhiều màu, chữ nướng | LÀM LẠI: `01-batch-10-redo.md` |
| 11 desert | Gemini | bố cục đạt có điều kiện, art phẳng hơn GPT | vẽ lại: `02-kit-redo.md` (kit 1) |
| 11 windrock | Gemini | bị trả (40 lỗi gate) | vẽ lại: kit 2 |
| 11 tomb | Gemini | thí điểm 11 asset | vẽ đủ kit: kit 3 |
| 14 kit còn lại | chưa vẽ | — | sau khi 3 kit đầu đạt |
| Bố cục map | Gemini/GPT | benchmark: `map-layouts/desert/desert_entrance` | `03-map-layout-gpt.md` |

Quy trình: GPT nộp theo chặng → Claude chạy `tools/check_hd2d_art.sh` + xem ảnh → dựng cảnh → báo kết quả. Cổng hiện quét `batch-11-*`; muốn gồm batch-10 chạy `art_gate.py --all` (Claude chỉnh).
