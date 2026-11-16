# Roadmap tổng + prompt giao ChatGPT (2026-11-09)

Nguồn: `ROADMAP-ART-TASKS-20261109.csv` (672 task), `ROADMAP-ART-92MAPS-20261109.md`, `REVIEW-CLAUDE-20261109-HANDOFF.md`.

## 1. Roadmap tổng

Khối lượng vẽ: **514 ảnh** = 417 NEW + 97 REDRAW (+ 48 FIX đóng gói, 10 REVIEW, 8 BRIEF, 92 SCENE proof không phải vẽ).

| Chặng | Milestone | Việc | Số task | Ai làm |
|---|---|---|---:|---|
| 0 | M0 | Sửa sha/lề/provenance + xem lại CHƯA_XEM | 58 | Codex/Claude (không cần ChatGPT vẽ) |
| 1 | M1 | World Tree (5) + Garden (5) vẽ lại | 10 | ChatGPT — **bắt đầu ở đây** |
| 2 | M2 | Sửa lỗi kit đã có: sàn/edge/backdrop/decal/prop (crossroads, nightmare, tomb, windrock, desert, ghost, astral, ancient, P01, batch-12) | 88 | ChatGPT |
| 3 | M3 | Landmark thiếu: desert 6, forest 2, ship 1 (xem ảnh gốc chọn vật) | 9 | ChatGPT |
| 4–11 | M4…M11 | 8 kit mới theo thứ tự tower → maze → guild → battlefield → maya → dungeon → arena2 → minigame; mỗi kit mở bằng `BRIEF-<kit>` (viết lại danh sách theo ảnh gốc) | 51/51/60/51/50/48/45/59 | Claude viết BRIEF, ChatGPT vẽ |
| 12 | M12 | Scene proof 92 map | 92 | Dựng + Claude xem |

Mỗi chặng đóng khi: gate pass → Claude xem 4× + lát thật → verdict DUYỆT trong ASSET-VERDICTS. Không mở chặng sau khi chặng trước còn VẼ_LẠI.

Lưu ý thật: **không prompt nào ép được ChatGPT "không dừng" qua 514 ảnh trong một lượt** (giới hạn độ dài chat, số ảnh/lượt, quota). Cách bền là giao theo **lô nhỏ + sổ cái (ledger)** để lần sau ChatGPT biết còn thiếu gì và không được tuyên bố xong sớm. Prompt dưới đây làm đúng việc đó.

## 2. PROMPT CHÍNH (dán 1 lần ở đầu mỗi chat mới)

```
Bạn là họa sĩ pixel-art HD-2D (kiểu Octopath Traveler) cho game web Phimond. Nhiệm vụ: hoàn thành TOÀN BỘ danh sách asset trong file CSV đính kèm (ROADMAP-ART-TASKS-20261109.csv), theo thứ tự cột `order`/`milestone`. Bạn KHÔNG ĐƯỢC dừng, KHÔNG ĐƯỢC tuyên bố "xong" cho tới khi sổ cái (LEDGER) cho thấy MỌI task thuộc phạm vi hiện hành đều ở trạng thái SUBMITTED có ảnh thật. Dừng sớm, tóm tắt thay vì vẽ, hoặc nói "các asset còn lại tương tự" đều bị coi là THẤT BẠI.

LUẬT CỨNG (từ owner):
1. Mỗi asset = 1 ảnh PNG thật do bạn tự tạo bằng công cụ tạo ảnh. CẤM vẽ bằng code (canvas/PIL/SVG), CẤM lật gương, CẤM đổi màu một asset khác để thành asset mới, CẤM tái dùng ảnh cũ.
2. Làm theo đúng cột `prompt`, `size_scale_pivot`, `errors_to_avoid` của từng dòng CSV. 128 px = 1 đơn vị thế giới (backdrop 64 px). 33–48 màu, alpha nhị phân, lề alpha ≥ 8 px (trừ floor/edge/backdrop), không bóng/glow/chữ/magenta nướng. Sàn 512×512 seamless, viền phẳng 8 px, mỗi biến thể texture khác nhau; edge 512×128 liền hai đầu; backdrop 1280×384 lặp ngang.
3. Ảnh gốc map tôi đính kèm trong từng lượt là nguồn sự thật về CHỦNG LOẠI vật thể và BẢNG MÀU. Nếu `prompt` mâu thuẫn ảnh gốc thì theo ảnh gốc và ghi rõ quyết định.
4. Ảnh "style anchor" đính kèm chỉ để khớp phong cách. Ảnh "bản cũ lỗi" chỉ để TRÁNH lỗi, không bắt chước.
5. Không được tự duyệt. Bạn chỉ SUBMIT; Claude/owner mới là người duyệt.
6. Không biết/không làm được thì ghi BLOCKED kèm lý do cụ thể; không được thay bằng asset khác.

GIAO THỨC MỖI LƯỢT:
- Tôi gửi 1 LÔ (≤ 6 asset) kèm ảnh. Bạn vẽ ĐỦ cả lô, từng ảnh một, rồi tự kiểm theo bảng dưới cho từng ảnh trước khi nộp. Ảnh nào trượt kiểm thì vẽ lại ngay trong lượt (tối đa 3 lần/asset).
- Bảng tự kiểm (trả lời CÓ/KHÔNG cho từng ảnh): đúng kích thước? nền trong suốt/opaque đúng loại? không viền trắng, không glow/bóng nướng? số màu có vẻ 33–48 (không phẳng)? sàn: lát 3×3 không thấy lưới/khe/cụm lặp? edge/backdrop: lát 3×1 không đường cắt, không cụm lặp đều, không đối xứng gương? portal: dormant/active cùng mask? đúng chủng loại vật thể theo ảnh gốc? KHÔNG lỗi nào trong `errors_to_avoid`?
- Cuối MỖI lượt bạn phải in LEDGER dạng bảng: task_id | trạng thái (SUBMITTED / REDO / BLOCKED / PENDING) | số lần vẽ | ghi chú lỗi còn nghi. Mọi task chưa nộp phải nằm ở PENDING — không được bỏ sót, không được gộp.
- Sau LEDGER in dòng: "CÒN LẠI: <n> task. LÔ KẾ TIẾP: <task_id đầu tiên chưa nộp>. Hãy gửi 'tiếp' kèm ảnh." Nếu CÒN LẠI > 0 thì TUYỆT ĐỐI không nói hoàn thành.
- Khi tôi gõ "tiếp", bạn lấy các task PENDING theo thứ tự và tiếp tục ngay, không hỏi lại, không tóm tắt lại luật.
- Chỉ khi LEDGER có 0 PENDING, 0 REDO, 0 BLOCKED thì in đúng dòng: "HOÀN TẤT 100% PHẠM VI: <milestone>" và dừng.

Xác nhận bằng đúng 1 câu: "Đã hiểu, sẵn sàng nhận lô đầu." rồi chờ lô.
```

## 3. Mẫu gửi MỖI LÔ (gửi kèm ảnh trực tiếp, KHÔNG zip)

```
LÔ <số> — milestone <Mx>, batch <tên batch>. Vẽ ĐỦ <n> asset sau, theo CSV (đã đính kèm ở đầu chat):
<danh sách task_id>
Ảnh đính kèm lượt này:
- Ảnh gốc map: <reference_attach của các task>
- Style anchor (đã duyệt): <style_anchor_attach>
- Bản cũ lỗi (chỉ để tránh lỗi): <nếu REDRAW>
Dán thêm vào prompt từng asset phần "errors_to_avoid" của dòng CSV nếu đây là lần vẽ lại.
Nhắc: nộp đủ <n> ảnh, tự kiểm từng ảnh, in LEDGER, ghi CÒN LẠI.
```

## 4. Lô đầu tiên (M1 — World Tree), dán sau prompt chính

Task: `NEW-world_tree-edge-03`, `REDRAW-world_tree-edge-01`, `REDRAW-world_tree-edge-02`, `REDRAW-world_tree-floor-extra-05`, `REDRAW-world_tree_gate-landmark-01`.
Prompt từng asset: ROADMAP-ART-92MAPS-20261109.md §4 (copy khối code của từng task). Ảnh gốc: `refs/world_tree_gate.jpg`, `world_tree_deep_woods.jpg`, `world_tree_secret_chamber.jpg` + anchor ghi trong từng task. Lưu ý edge-03: 16 lần trước đều bị bác (seam/cadence/magenta) — nhấn mạnh "không cụm lặp trong 1 tile, không đối xứng, hai đầu khớp".
Lô 2: 5 asset Garden (`REDRAW-gd-trunk-seg-01/02`, `gd-seal-strip`, `gd-seal-strip-lit`, `gd-pillar-vein-01`) kèm `garden-a/REVIEW-CLAUDE-20261109.md` làm ngữ cảnh.

## 5. Sau mỗi lô

1. Lưu ảnh vào output path trong CSV; chạy `python3 tools/hd2d_audit/art_gate.py batch-11-<kit>`.
2. Đưa lại cho Claude xem 4× + lát thật; Claude ghi verdict.
3. Asset trượt → dán `errors_to_avoid` + lỗi cụ thể Claude nêu, bảo ChatGPT vẽ lại đúng asset đó ở lượt sau.
4. Hết chặng mới sang chặng kế. Kit mới (M4+): chạy `BRIEF-<kit>` với Claude trước khi giao ChatGPT, vì brief plan của 6/8 kit sai chủ đề so với ảnh gốc.
