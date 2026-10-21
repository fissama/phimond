```text
Bạn là art worker của Phimond. Repo: /Users/phileanh/rust/phimond. Đọc AGENTS.md trước.

Batch 00–09 là do chính bạn vẽ và là chuẩn style. Batch 10 và Batch 11 (desert, windrock, tomb) do model khác vẽ và bị trả vì lệch style. Nhiệm vụ: vẽ lại để không thể phân biệt với batch 00–09. Bắt buộc dùng built-in image_gen để vẽ; cấm vẽ nội dung bằng code hay API trả phí; code chỉ để cắt sheet, khử nền #FF00FF, đưa về bảng màu, kiểm tra.

Hãy đọc kỹ theo thứ tự:
1. .ai/design/gpt-redo/README.md (thứ tự và hiện trạng)
2. .ai/design/gpt-redo/00-master-v2.md (luật chung: ảnh tham chiếu đính kèm thật kèm sha256, style DNA đo được, quy trình sheet ~6 vật, danh sách lỗi đã bị trả, cổng nghiệm thu)
3. .ai/design/gpt-redo/01-batch-10-redo.md (đợt đầu tiên)
Quy trình sản xuất cũ để dùng lại: apps/game-web/art-src/hd2d/batch-01-octopath/production.md và package.py.

VIỆC BẮT ĐẦU NGAY: Batch 10, CHẶNG A (3 tầng login sky/citadel/forest + foreground).
- Chuyển bản Gemini cũ sang apps/game-web/art-src/hd2d/batch-10-octopath/_gemini-rejected/ (không xóa, không dùng làm style).
- Mở và nhìn các ảnh style của batch 00–09 sát loại (contact-sheet batch-01, batch-02/03, batch-06) và hai anchor linh thú trước khi vẽ; đính kèm thật vào image_gen, ghi sha256 vào prompt.md.
- Mỗi asset một thư mục: raw-01.png (giữ nguyên), final.png, prompt.md, review.md, qa.json. Tự nhìn từng final (phóng 4×) trước khi ghi pass.
- Chạy `sh tools/check_hd2d_art.sh` (nếu chưa quét batch-10 thì chạy `python3 tools/hd2d_audit/art_gate.py --all`) và báo kết quả thật. Không sửa tools/hd2d_audit/*, gate_waivers.json hay check.sh. Không commit, không đụng runtime.
- Nộp xong chặng A: danh sách file, contact-sheet mới, kết quả check, và nêu 3 asset bạn tự thấy yếu nhất. Sau đó DỪNG chờ phản hồi; Claude sẽ duyệt bằng ảnh rồi mới sang chặng B (branding), C (loading), D (intro).

Sau Batch 10 sẽ là các kit: desert → windrock → tomb (file 02-kit-redo.md), rồi NPC batch-05 trùng sprite (04-batch-05-npc-redo.md). Không làm trước khi được giao.
```
