# Message khởi động cho Codex (dán nguyên)

```text
Bạn là art worker của Phimond (repo /Users/phileanh/rust/phimond). Đọc AGENTS.md rồi .ai/design/map-checklists/README.md.

BẮT BUỘC dùng https://github.com/0x0funky/agent-sprite-forge cho mọi việc vẽ/đóng gói asset:
1. Nếu chưa cài: git clone https://github.com/0x0funky/agent-sprite-forge.git && cd agent-sprite-forge && python -m pip install -r requirements.txt && python tools/install_skills.py --apply --host codex, rồi mở phiên Codex mới. (Batch 00 đã dùng commit 5324342fdfab72430f4e9604f3fe427009f8596d; skills ở ~/.codex/skills/.)
2. Chạy `route_media.py resolve --kind image` (generate2dmedia) và `forge_doctor.py`; route phải là image_gen của Codex đã đăng nhập. Nếu rơi về codeart2d hoặc API trả phí thì DỪNG và báo. Không vẽ nội dung bằng code, không lật gương, không đổi màu để làm "asset mới".
3. Dùng generate2dmap (tile, prop kit, kiểm seam) và generate2dsprite (prop, decal, FX, marker, pixel finish) theo sheet ~6 vật trên nền #FF00FF; raw-01.png giữ nguyên; mỗi asset một thư mục raw-01/final/prompt.md/review.md/qa.json.

Luật style và lỗi đã bị trả: .ai/design/gpt-redo/00-master-v2.md. Tỉ lệ: người chơi = 1.31 đơn vị (cỡ tối đa vật nhỏ ở tools/hd2d_audit/size_check.py).

LÀM THEO THỨ TỰ (mỗi kit đọc kit-<tên>.md; mỗi map có ảnh gốc để đối chiếu và PHẢI đính kèm thật vào image_gen):
 1) desert (hoàn thiện nháp), 2) forest + city (Hoàng Cung/thành: rà bảng, bù asset thiếu), 3) windrock, 4) tomb, 5) nightmare, crossroads, astral, ancient, ghost_castle, world_tree, tower, maze, guild, battlefield, maya, dungeon, arena2, minigame, 6) beach, ship (rà lại).
Mỗi hàng trong bảng: vẽ xong thì đổi ⬜ → ✅ ở cột "Vẽ" (chỉ khi đã tự nhìn final 4× nền tối/caro). KHÔNG tự đánh "Duyệt" (chỉ Claude/owner). Chạy `python3 tools/hd2d_audit/art_gate.py batch-11-<kit>` sau mỗi kit và báo kết quả thật.
Landmark riêng từng map: nhìn ảnh gốc, ghi tên vật nhận diện vào bảng của map rồi vẽ.
Ghi tiến độ vào .ai/design/gpt-redo/PROGRESS.md. Không commit; không sửa runtime, tools/hd2d_audit/*, gate_waivers.json, check.sh.
```
