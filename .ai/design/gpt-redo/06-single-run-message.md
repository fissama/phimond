```text
Bạn là art worker của Phimond. Repo: /Users/phileanh/rust/phimond. Đọc AGENTS.md trước.

BỐI CẢNH: Batch 00–09 do chính bạn vẽ và là chuẩn style. Batch 10 và Batch 11 (desert, windrock, tomb) do model khác vẽ và bị trả vì lệch style. Bạn vẽ lại TOÀN BỘ phần này để không thể phân biệt với batch 00–09. Mục tiêu cuối: bộ asset rời theo từng map của game gốc, để Claude cắt ghép dựng map HD-2D Octopath. Bắt buộc dùng built-in image_gen; cấm vẽ nội dung bằng code hay API trả phí; code chỉ để cắt sheet, khử nền #FF00FF, đưa về bảng màu, kiểm tra.

ĐỌC TRƯỚC (theo thứ tự): .ai/design/gpt-redo/README.md, 00-master-v2.md (luật chung: tham chiếu đính kèm thật + sha256, style DNA, quy trình sheet, lỗi đã bị trả, cổng nghiệm thu), rồi từng file đợt khi tới lượt: 01-batch-10-redo.md, 02-kit-redo.md, 04-batch-05-npc-redo.md. Quy trình sản xuất cũ: apps/game-web/art-src/hd2d/batch-01-octopath/production.md và package.py.

CHẠY MỘT MẠCH THEO THỨ TỰ, KHÔNG DỪNG CHỜ DUYỆT GIỮA CÁC MỤC (trừ khi bị chặn thật):
 1. Batch 10: sửa nhẹ tầng forest (giảm cụm lá lặp, ≥ 2 kiểu cụm) và foreground (bớt hoa hai bên), rồi làm tiếp chặng B (branding), C (loading), D (intro).
 2. Kit desert (batch-11-desert), theo 02-kit-redo.md: toàn bộ 4 chặng. Bản Gemini cũ chuyển vào _gemini/ trong thư mục kit, không xóa, không dùng làm style.
 3. Kit windrock (batch-11-windrock).
 4. Kit tomb (batch-11-tomb), đủ cho 9 map.
 5. NPC batch-05 trùng sprite (04-batch-05-npc-redo.md).
 6. Các kit còn lại theo thứ tự: nightmare, crossroads, astral, ancient, ghost_castle, world_tree, tower, maze, guild, battlefield, maya, dungeon, arena2, minigame. Bảng map/mảnh tối thiểu từng kit: Phần C của .ai/design/hd2d-maps-75-gemini-prompt.md. Với MỖI kit, mở ảnh gốc của mọi map thuộc kit (Downloads/Phimond-P12-Review/map-images/<map_id>.png) và vẽ landmark đặc trưng từng map.

TIẾN ĐỘ VÀ TIẾP TỤC: sau mỗi mục/chặng cập nhật .ai/design/gpt-redo/PROGRESS.md (mục nào xong, asset nào còn, kết quả check, 3 asset yếu nhất, việc đang dở). Nếu hết hạn mức hay phiên bị ngắt, phiên sau đọc PROGRESS.md và làm tiếp đúng chỗ dở, không vẽ lại cái đã xong.

CHẤT LƯỢNG KHÔNG ĐƯỢC HẠ ĐỂ ĐI NHANH: mỗi asset tự nhìn (phóng 4×) trước khi ghi pass; vẽ lại bằng image_gen nếu hỏng, không vá bằng code; không hai asset cùng hình khác màu, không hai tile cùng texture; mỗi kit chạy `python3 tools/hd2d_audit/art_gate.py <batch>` (hoặc `sh tools/check_hd2d_art.sh`) và báo kết quả thật; không sửa tools/hd2d_audit/*, gate_waivers.json hay check.sh. Mỗi kit xong có contact-sheet MỚI hơn manifest. Không commit, không đụng runtime/scene.

KHI NÀO ĐƯỢC DỪNG VÀ HỎI: chỉ khi thiếu ảnh gốc/công cụ, hoặc gate báo lỗi bạn không thể sửa bằng cách vẽ lại. Ngoài ra, cứ tiếp tục. Khi xong mỗi kit, ghi một dòng vào PROGRESS.md để Claude duyệt ảnh song song; nếu Claude trả lại, sửa theo nhận xét rồi quay lại mạch chính.
```
