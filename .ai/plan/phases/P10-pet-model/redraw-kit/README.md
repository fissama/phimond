# Redraw kit — 152 species đã hoàn tất

**Trạng thái cập nhật 2026-10-12:** DONE 152/152 (100%), chủ dự án duyệt chốt 2026-10-11; nhóm 4★–5★ đạt 48/48.

- [Closure](../P10-redraw-closure-20261011.md)
- [Bản atlas được chọn và SHA-256](owner-atlas-selection.json)
- [Final inventory](completion-20261011/done.json)
- [Owner feedback theo phiên bản](owner-reviews.json)

Tích hợp runtime là bước riêng. Các batch/prompt bên dưới giữ làm lịch sử và hướng dẫn tái sử dụng; không phải hàng đợi redraw đang mở. Manifest dispatch cũ không thay thế final inventory.

## Kế hoạch dispatch ban đầu — 2026-10-05

**Goal:** bộ giao việc lặp lại được cho GPT-6.1 Sol, vẽ 150 species còn lại theo hai mẫu người dùng đã duyệt; giữ identity từ APK và kiểm chứng từng candidate.

**Architecture:** 30 batch × 5 loài; mỗi task xử lý tuần tự, mỗi loài một lần gọi image tool cho sheet 20 pose. Tách tạo hình → kiểm tra cơ học → review hình ảnh → người dùng duyệt → integration riêng.

**Tech:** built-in image generation, Python 3, Pillow trong `tools/.cache/asset-venv/bin/python`, checker/packer sẵn có, HTML preview cục bộ.

**Spec:** `../P10-redraw-plan.md`, roster `data/p10/species.json`, hai style anchors trong manifest. Đây là gói chuẩn bị dispatch theo yêu cầu mới; không mở lại P10 design hay kích hoạt artwork vào runtime.

## 1. Các lựa chọn đề xuất

| Điểm | Quyết định | Lý do |
|---|---|---|
| Đơn vị task | 5 species/task; 30 task | Dễ theo dõi lỗi, giới hạn context và retry |
| Đơn vị vẽ | 1 species/call, 20 pose | Không trộn identity của nhiều loài trong một sheet |
| Song song | Chạy batch 01 trước; sau khi duyệt, 2–3 task khác batch | Không trùng thư mục, dễ quan sát chất lượng |
| Identity | Giữ anatomy, palette, trang phục, vũ khí từ source | “Vẽ lại” không trở thành thiết kế một loài khác |
| Style | DocDangNu + DaoThienDuong đã duyệt | Thống nhất outline, shading và độ chi tiết |
| Retry | Tối đa 3 lần gọi image tool/loài trong brief | Tránh task tự sửa vô hạn; blocked có lý do để xử lý sau |
| Acceptance | Cơ học + reviewer độc lập + human | 20 ô khác pixel chưa chứng minh có animation tốt |

**Batch 01:** Nữ Vương Bạch Cốt, Ma Vương Hút Máu, Rồng Có Cánh, Cua Hắc Ám, Hoa Ăn Thịt Người. Có humanoid cầm đồ, rồng, thân rộng và thực vật. Toàn bộ redraw cũ ngoài hai anchors đã được người dùng yêu cầu xóa. Chỉ dùng assets APK gốc và hai anchors; không tái sử dụng redraw bị hủy.

Hai mẫu đã duyệt chỉ được loại khỏi danh sách redraw: `species_0037` (DocDangNu), `species_0150` (DaoThienDuong). **Style đã duyệt không đồng nghĩa production geometry đã đạt:** các reference hiện là 1122×1402. Output mới dùng 1124×1405 theo contract; việc chuẩn hóa hai anchors vào runtime là scope riêng.

## 2. Bắt đầu nhanh

Chạy từ `/Users/phileanh/rust/phimond`:

```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs
rtk proxy python3 tools/assets/p10_redraw_jobs.py list --batch 1
rtk proxy python3 tools/assets/p10_redraw_jobs.py prompt --batch 1
```

Mở task trong **cùng workspace**, chọn GPT-6.1 Sol, paste toàn bộ output `prompt`. Hoặc copy [batches/batch-01.md](batches/batch-01.md). Trên macOS có thể tự chạy:

```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py prompt --batch 1 | pbcopy
```

Đổi `--batch 1` thành 2…30 cho các batch sau. Mỗi task chỉ nhận một batch; không gửi cùng batch cho hai task cùng lúc. GPT-6.1 Sol điều phối/viết prompt; task phải có image-generation tool thực sự để tạo ảnh. Nếu thiếu tool, báo blocked; không tự chuyển sang API/CLI trả phí.

**Lưu ý workspace:** một số helper và art đang là file chưa commit của task khác. Kit kiểm tra được source ảnh nhưng không đảm bảo một checkout/worktree mới có các file này. Dùng workspace hiện tại hoặc chuyển một snapshot đã được owner kiểm tra; không `git add -A` để gom công việc của mọi người.

Không có lệnh trong kit tự chạy 150 lần gọi model. 150 sheet cần ít nhất 150 lần generate; với giới hạn 3/loài có thể đến 450 lần, chưa bao gồm xử lý blocked sau đó. Đây là giới hạn số lần gọi, không phải ước tính chi phí hay bảo đảm chất lượng.

## 3. File scope và đầu ra mỗi loài

`manifest.json` là danh sách dispatch cố định, không dùng làm bảng trạng thái cho nhiều worker cùng ghi. Input hash được pin; có drift phải kiểm tra nguyên nhân, không tự sửa hash để bỏ qua.

```text
apps/game-client/assets/pets/redraws/batches/20261005/species_NNNN/
  identity.md
  attempt-01/
    prompt.md
    inputs.json          # ordered paths + SHA256 + tool used
    raw.png              # original output, byte-identical
    layout.json          # only when packing is necessary
    packed.png           # optional; never overwrite raw
    packing.json         # packer's stdout if used
    mechanical.json
    preview/             # helper refuses existing directory
      preview.html
      sprites.png        # byte-identical candidate copy
      portrait-preview.png
      mechanical.json
    self-review.md
  attempt-02/             # if needed, retain failed attempt-01
  result.json
  independent-review.md  # separate reviewer, candidate SHA256 pinned
```

`result.json` example schema (worker fills actual values; never copy placeholders as evidence):

```json
{
  "species_id": "species_NNNN",
  "source_species_id": "APKSourceID",
  "status": "ready_for_review",
  "generation_calls": 1,
  "candidate_path": "relative/path/to/raw-or-packed.png",
  "candidate_sha256": "actual-sha256",
  "mechanical_status": "pass",
  "self_review_path": "relative/path/to/self-review.md",
  "preview_path": "relative/path/to/preview.html",
  "human_approved": false,
  "blockers": []
}
```

`queued` trong manifest chỉ là trạng thái ban đầu. Worker dùng `ready_for_review` hoặc `blocked`; reviewer ghi `pass`, `changes_requested` hoặc `unable_to_verify` vào review riêng. Chỉ người dùng quyết định accepted. Candidate đổi dù một pixel phải chạy check và review lại hash mới.

## 4. Hướng dẫn mỗi species

1. Kiểm tra input hashes, mở **bốn ảnh thật**: hai anchors, portrait gốc, atlas gốc. Atlas có thể chứa bia mộ; không coi bia mộ là anatomy của loài.
2. Viết identity card: đếm đầu/tay/chân/cánh/sừng, màu, mắt, vũ khí và tay cầm, trang phục, silhouette, locomotion, pivot. Nếu ảnh gốc mơ hồ, ghi rõ suy luận. Nếu không xác định được điểm nhận dạng quan trọng, mark blocked thay vì đoán từ tên.
3. Điền [image-prompt.md](image-prompt.md), attach đúng ảnh vào image tool; lưu prompt và input hashes. Reference theo thứ tự trong prompt.
4. Kiểm tra hình trước khi sửa kích thước: all 20 poses, vũ khí, anatomy, hướng hit, cast khác attack, down nằm thật. Dùng [repair-prompt.md](repair-prompt.md) khi cần; không dùng Python vẽ bù nét hoặc xóa alpha che lỗi.
5. Chạy checker. Sai bố cục thuần túy có thể dùng packer theo bước dưới; sai identity/animation cần sửa bằng image tool.
6. Export preview, play loop và one-shot ở 64/96/192px trên nền sáng/tối. Ghi self-review đủ 20 ô, dùng chỉ số **R1C1…R5C4** (checker JSON dùng row/column từ 0).
7. Lưu result. Chuyển reviewer độc lập bằng [review-prompt.md](review-prompt.md), sau đó đưa contact sheet + animation cho người dùng duyệt.

### Contract cơ học

- RGBA PNG, 1124×1405, 4 cột × 5 hàng, 281×281/ô.
- Toàn bộ alpha > 0 nằm trong tọa độ cục bộ `[22,259)`; effects cũng phải nằm trong ô.
- 20 ô có hình và khác pixel. Body thường cao 155–202px; thân rộng được nhỏ hơn.
- Hàng idle/move loop; attack/cast/hurt-down one-shot. Một camera cố định, mặc định toàn bộ20 pose nhìn trái; hướng tác động screen-left. Nếu sprite gốc frontal hoặc đối xứng (ví dụ Cua Hắc Ám), được giữ camera frontal xuyên suốt20 pose để bảo toàn nhận dạng; phải ghi exception trong review, không đổi góc giữa các ô. Timing preview là preset để quan sát, không phải combat timing.
- Không khai báo Element, skill mới hay stats từ màu/effect. Race, Star, class lấy manifest.

### Commands kiểm tra / đóng gói / preview

Thay `JOB` bằng output_dir của loài; đây là shell variable chỉ dẫn, không tên thật của thư mục:

```sh
JOB=apps/game-client/assets/pets/redraws/batches/20261005/species_0018
rtk proxy tools/.cache/asset-venv/bin/python tools/assets/check_p10_atlas.py "$JOB/attempt-01/raw.png" > "$JOB/attempt-01/mechanical.json"
```

Checker exit 0 mới được xem là pass. Không bỏ qua exit code do đã có file JSON. Nếu art tốt nhưng layout sai, tạo `layout.json` với **đúng 20 rectangles và pivots**, row-major:

```json
{
  "destination_pivot": [140, 237],
  "frames": [
    {"rect": [0, 0, 281, 281], "pivot": [140, 237]}
  ]
}
```

Đoạn trên chỉ minh họa schema **một frame**, không phải layout chạy được. Worker phải đo toàn bộ raw và điền 20 entries. `rect=[x,y,width,height]`; `pivot` là tọa độ trong rect. Không mặc định raw chia hết cho 4×5, không dùng 20 pivot chân giống nhau khi tư thế nằm/nhảy cần điểm neo khác. Packer yêu cầu giữ toàn bộ alpha nguồn, rectangles không chồng nhau; alpha tràn từ loài khác/ảnh hỏng phải regenerate.

```sh
rtk proxy tools/.cache/asset-venv/bin/python tools/assets/pack_p10_atlas.py --source "$JOB/attempt-01/raw.png" --layout "$JOB/attempt-01/layout.json" --output "$JOB/attempt-01/packed.png" > "$JOB/attempt-01/packing.json"
rtk proxy tools/.cache/asset-venv/bin/python tools/assets/check_p10_atlas.py "$JOB/attempt-01/packed.png" > "$JOB/attempt-01/mechanical.json"
rtk proxy tools/.cache/asset-venv/bin/python tools/assets/preview_p10_redraw.py --atlas "$JOB/attempt-01/packed.png" --out "$JOB/attempt-01/preview"
```

Nếu raw đã pass, preview `raw.png` trực tiếp. Packer dùng chung một tỷ lệ nearest-neighbor; không sửa chất lượng nét, anatomy hay chuyển động. Preview là HTML standalone nhúng PNG, mở trong browser không cần server. `portrait-preview.png` là crop idle ô đầu; **chưa phải portrait UI đã nghiệm thu**. Kit không tạo/ghi đè production `frames.tres`.

## 5. Checklist triển khai và review

- [x] Pin danh sách 150 canonical IDs, loại đúng 2 anchors; chia 30×5 không trùng.
- [x] Tạo prompt worker/image/repair/reviewer, script preflight và preview.
- [ ] Người dùng chạy batch 01, review trước khi scale.
- [ ] Điều chỉnh prompt chung nếu batch đầu có lỗi lặp lại; regenerate batch briefs bằng renderer khi template thay đổi.
- [ ] Chạy các batch 02–30; mỗi worker ghi trạng thái riêng, không ghi shared manifest.
- [ ] Triage blocked sau mỗi batch; chỉ retry loài chưa đạt, giữ failed attempts.
- [ ] Reviewer kiểm đủ 150 candidate hashes; người dùng duyệt từng batch.
- [ ] Lập integration task riêng: portrait UI, SpriteFrames timings/mapping, runtime activation, Godot smoke, source provenance, commit phạm vi đã duyệt.

**Global constraints:** giữ nguyên 304 PNG nguồn APK, catalog/IDs, source manifest, hai anchors, code runtime và công việc đồng thời. Redraw cũ ngoài hai anchors đã được xóa theo yêu cầu người dùng. Không push/merge/deploy/restart trong art worker; đây cũng là phạm vi giới hạn của redraw contract hiện có.

**Review focus:** weapons không mất ở cast/down, silhouette không biến thành loài khác, đủ 20 pose có ý nghĩa, loop seam và pivot ổn, hit trái, FX không che cơ thể, outline không mờ ở 64px. Nếu chỉ xem contact sheet thì phải ghi animation chưa xác minh.

## 6. Kiểm tra bộ công cụ

```sh
rtk proxy python3 tools/assets/p10_redraw_jobs.py check-inputs
rtk proxy tools/.cache/asset-venv/bin/python -m unittest discover -s tools/assets -p test_p10_redraw_kit.py
```

Helper chỉ chuẩn bị việc và bằng chứng. Không tự đánh dấu bất kỳ loài nào đã được người dùng chấp thuận.
