# P10 Late-Game Sprite Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for sequential execution. Work one species at a time in this task; do not start the next art candidate before recording the current species disposition and progress report.

**Goal:** Hoàn thiện lần lượt 48 sprite atlas 4★/5★, báo tỷ lệ sau mỗi loài đạt QA mà không nhầm với quyền kích hoạt runtime.

**Architecture:** Mỗi species là một đơn vị độc lập, có APK source bất biến, raw imagegen phiên bản hóa, atlas đóng NN, bằng chứng kiểm tra và một `result.json`. Thứ tự ưu tiên nằm trong bảng dưới; tracker đếm các loài qua QA, không đếm số lần generate hay chỉ geometry pass.

**Tech Stack:** Built-in image_gen, Python/Pillow NN packing, `tools/assets/check_p10_atlas.py`, `tools/assets/preview_p10_redraw.py`, Godot/browser preview ở 64/96 px.

**Spec:** `.ai/plan/phases/P10-pet-model/P10-redraw-plan.md`; review từng loài `.ai/plan/phases/P10-pet-model/redraw-kit/review-20261008/review.md`; snapshot trước thực hiện `.ai/plan/phases/P10-pet-model/redraw-kit/polish-20261008/status-20261008.md`.

## Global Constraints

- Roster đúng 48: 4★ = 17 thường + 4 Special; 5★ = 14 thường + 13 Special. ID trong `data/p10/species.json` bất biến.
- Chỉ APK của cùng loài ở `apps/game-client/assets/pets/apk84/<source_species_id>/` được đưa vào generation references. Không dùng bất kỳ atlas redraw nào làm reference, kể cả cùng loài hoặc hai anchor cũ. Giữ source bytes và hash.
- Owner refinement 2026-10-09: giữ triết lí/tính cách và đặc điểm nhận diện gốc, thiết kế lại hình khối và khuôn mặt; không chỉ làm sắc ảnh cũ. Đánh giá mặt riêng ở raw và size chơi thật: hướng mắt, chân mày, mõm/hàm hoặc cằm/miệng, biểu cảm, độ nhất quán qua 20 pose. Xem `owner-art-direction-20261009.md`.
- Cast phải có hiệu ứng phép đọc rõ ở size thân thử battle: tụ → phát → tan, hình khối/màu theo triết lí loài; không chỉ đổi động tác tay hoặc glow gần như vô hình. Giữ mặt rõ, FX gọn có tương phản, không sương mờ/tràn ô. Không suy diễn thêm gameplay hay element từ FX. Rà lại cả các candidate cũ theo tiêu chí này trước final QA.
- Dùng built-in imagegen, không MiniMax hay script tự vẽ sprite. Lưu raw, prompt, reference hash và rejected attempts; không xóa alpha hoặc crop phần hình để giả pass.
- Atlas RGBA 1124×1405, 4×5 cell 281×281, 20 frame có hình và khác nhau; mọi alpha > 0 nằm trong local [22,259). Pack NN với một scale/pivot nhất quán.
- Idle và Move loop 4→1; Attack, Cast, Hurt/Down one-shot. Row Move phải có chuyển động thật theo giải phẫu loài. Row Down cuối phải gục. Camera, anatomy, trang bị, palette ổn định.
- Size A đã chốt là **cảm giác hiện diện trong battle**: 4★ lớn hơn nhẹ so với 1–3★; 5★ lớn rõ hơn; Special 5★ có ngoại lệ theo loài. Không giãn x/y khác nhau và không coi bản demo scale là runtime config.
- Không thay gameplay code, APK source, DB, server 8090 hay runtime routing trong vòng art này. Không push/merge để công bố candidate chưa duyệt.

## Review Focus

1. Raw chứa pose hoặc FX chồng sang ô kế: phải vẽ lại, vì pack có thể pass geometry trong khi nhân vật bị cắt.
2. Move bốn frame khác nhau về pixel nhưng lặp cùng chân trụ: xem loop thực ở 64/96 px và xác nhận pha trái/phải hoặc cánh/hover.
3. Vũ khí, đầu, tay, đuôi hoặc số đầu thay đổi giữa Attack/Cast/Down: đối chiếu cả 20 frame với APK.
4. Hiệu ứng/alpha noise làm nhân vật mờ hoặc át mặt trên nền sáng/tối: sửa nguồn, không xóa alpha để hợp thức hóa.
5. Atlas đúng 281 px nhưng thân quá nhỏ, nhảy pivot hoặc va UI battle: thử size A trên màn battle trước khi đề xuất chốt scale.

## Một species được tính là “QA xong” khi nào?

- [ ] Khóa nhận diện nguồn: anatomy, số đầu/chân/tay/cánh, vật cầm, palette và camera đã so với portrait + sprites gốc.
- [ ] Xem **raw** ở độ phân giải gốc; mỗi pose/FX đủ hình, không tràn hoặc bị chia qua biên ô nguồn. Nếu ảnh sinh lỗi, vẽ lại. Không dùng pack để che lỗi.
- [ ] Lưu raw/prompt/inputs theo phiên bản; pack NN toàn bộ 20 pose bằng cùng scale/pivot, giữ nguyên raw và record hash/layout.
- [ ] `check_p10_atlas.py` pass: RGBA, 1124×1405, 20 frame có hình/khác nhau và alpha trong [22,259).
- [ ] Xem 20 frame riêng + playback Idle/Move 4→1 trên nền sáng/tối tại 64/96 px; Move đúng dáng loài, không nhảy scale/pivot.
- [ ] Xem one-shot Attack/Cast/Hurt: động tác cơ thể khác nhau, vật cầm xuyên suốt, hai pose Down cuối thực sự gục.
- [ ] So tại kích thước thử battle theo quyết định size A: mặt và chi tiết chính đọc được, không đè tên/HP/selection ring.
- [ ] Review độc lập trên **đúng SHA của atlas** và ghi `result.json` với bằng chứng, lỗi còn lại. Chỉ trạng thái `qa_passed` sau tám kiểm tra này mới tăng %.

`owner_approved` là bước sau khi bạn duyệt; QA pass không tự kích hoạt game. Nếu bạn từ chối bản đã QA pass, đổi về `repair_required` và tính lại %.

**Công thức:** `QA hoàn thiện = số species trạng thái qa_passed hoặc owner_approved / 48 × 100`, làm tròn 2 chữ số. Bắt đầu **0/48 = 0.00%**. Sau loài đầu: **1/48 = 2.08%**; sau 3 loài: **3/48 = 6.25%**; sau 27 loài: **27/48 = 56.25%**; cuối: **48/48 = 100.00%**. Báo riêng số owner đã duyệt, hiện 0/48 theo metadata, không gộp vào % QA.

## Thứ tự thực hiện — đúng một species đang active

| # | ID | Loài | Tier | Điểm xuất phát | Điểm cần chốt |
|---:|---|---|---|---|---|
| 1 | species_0146 | Ma Vương Hút Máu | 5★ Special | Move lỗi | Sửa Move bước ngắn có đổi chân trụ; giữ 16 frame còn lại. |
| 2 | species_0037 | Độc Đằng Nữ | 5★ | Bản chọn chờ duyệt | Kiểm tra blink, cast, pivot, năm hàng ở 64/96 px. |
| 3 | species_0150 | Đảo Thiên Đường | 5★ Special | Bản chọn chờ duyệt | Kiểm tra 2 pose down cuối gục rõ và giữ màu nguồn. |
| 4 | species_0142 | Thần Tướng Cự Ma | 5★ Special | Atlas mới chưa duyệt | Giữ đầu, khiên và khối giáp đọc rõ; xem source-grid R3. |
| 5 | species_0020 | Thủ Lĩnh Hắc Ám | 5★ Special | Atlas mới chưa duyệt | Tách đầu kỵ sĩ, thú cưỡi và kiếm; nhịp bước thú cưỡi. |
| 6 | species_0126 | Trùng Mẫu Mào Vàng | 5★ Special | Atlas mới chưa duyệt | Mặt nữ vương rõ trước mào/bụng; nhịp chân và cast. |
| 7 | species_0019 | Nữ Đế Minh Giới | 5★ Special | Atlas mới chưa duyệt | Tách mặt khỏi tóc/trang sức; cast có tay và thân. |
| 8 | species_0151 | Đại Vương Bọ Cạp | 5★ Special | Atlas mới chưa duyệt | Tách mặt, bụng, khớp càng/đuôi; giữ một ngòi. |
| 9 | species_0149 | Thú Vàng Một Sừng | 5★ Special | Atlas mới chưa duyệt | Tách mặt/ngực/chân vàng; dáng kiêu hãnh, không thêm giáp. |
| 10 | species_0152 | Chim Ái Thần | 5★ Special | Atlas mới chưa duyệt | Mắt và tay rõ; bỏ noise/glow ngoài silhouette. |
| 11 | species_0145 | Cây Cự Linh | 5★ Special | Atlas mới chưa duyệt | Giữ đúng hai trụ gỗ; phân lớp mắt/gỗ/lá. |
| 12 | species_0143 | Thần Đèn | 5★ Special | Atlas cũ | Giữ một đèn; gom highlight da xanh, diễn mắt/tay. |
| 13 | species_0144 | Linh Tiên Hoa Hương | 5★ Special | Atlas cũ | Mặt không chìm dưới cánh hoa; giữ dáng dịu. |
| 14 | species_0148 | Ngựa Bùn Cỏ | 5★ Special | Atlas cũ | Giữ vẻ dễ thương; mắt, lông, chân và nhịp nhún. |
| 15 | species_0052 | Thánh Rồng Thái Cổ | 5★ | Atlas cũ | Mặt/ngực/cánh khí chất thái cổ; tăng hiện diện theo tier. |
| 16 | species_0069 | Trụy Thiên Sứ | 5★ | Atlas cũ | Mặt/ngực/kiếm đỏ rõ; phân lớp lông cánh. |
| 17 | species_0017 | Rồng Xương Băng | 5★ | Mở lại theo owner | Rồng undead bốn chân, thân xương dài; hai cánh có khớp đập để bay; lõi đỏ trong lồng ngực. Xương ngà, màng nâu theo APK. |
| 18 | species_0124 | Trùng Bất Tử Địa Huyệt | 5★ | Đang review | Hàm tách khỏi chân; kiểm tra cánh có nhịp đập và chức năng bay, không chỉ trang trí. |
| 19 | species_0125 | Nhện Phu Nhân | 5★ | Mở lại theo owner | Côn trùng hình người nữ tính/quyến rũ như Mantis; mặt mềm có nét người, râu cảm giác; cánh bướm có nhịp bay. Không tiên nữ thường hoặc mặt côn trùng dữ. |
| 20 | species_0141 | Totem Thượng Cổ | 5★ | Sửa theo owner | Phiến đá cổ bám bùn, hai tay và không có chân; mặt nghiêm ngầu, ánh sáng huyền bí nhẹ, di chuyển tâm linh lơ lửng. |
| 21 | species_0147 | Người Tuyết Viễn Cổ | 5★ | Đang redraw | Lông/ngà/vai rõ; cầm chùy/gậy đầu nhọn xương hoặc băng, không phải rìu; kiểm tra tay bám cán và bước chân luân phiên. |
| 22 | species_0018 | Nữ Vương Bạch Cốt | 5★ | Atlas cũ | Một rìu/hai tay xuyên suốt; down và cast không mất rìu. |
| 23 | species_0038 | Tinh Linh Bách Hoa | 5★ | Atlas cũ | Mặt/cánh xanh/tay giữ gậy; Move có nhịp cánh. |
| 24 | species_0088 | Sói Xích Viêm | 5★ | Atlas cũ | Phân biệt bờm lửa với lông; body phản ứng hit. |
| 25 | species_0106 | Chim Cú Địa Ngục | 5★ | Atlas cũ | Mắt/mỏ/cổ rõ; cánh tím bớt bóng mượt. |
| 26 | species_0107 | Đại Bàng Vàng | 5★ | Atlas cũ | Mỏ, móng, gốc cánh chắc; giữ hình chim APK. |
| 27 | species_0140 | Nhân Sư | 5★ | Atlas cũ | Mặt và mắt tách mũ/giáp; dáng trang nghiêm. |
| 28 | species_0068 | Thanh Long | 4★ Special | Atlas cũ | Thân rồng dài ưu tiên chiều rộng; râu/sừng/bờm rõ. |
| 29 | species_0087 | Bạch Hổ | 4★ Special | Atlas cũ | Thân ngang, mắt và sọc rõ; giữ giáp vàng. |
| 30 | species_0105 | Chu Tước | 4★ Special | Ảnh thô | Đuôi cuộn và mỏ/mắt rõ; khác Đảo Thiên Đường. |
| 31 | species_0139 | Huyền Vũ | 4★ Special | Atlas cũ | Phân lớp mai/cổ/chân; giữ màu đỏ tím APK. |
| 32 | species_0015 | Tử Thần | 4★ | Cần sửa | Giữ một lưỡi hái đỏ; sprite nguồn không bị cắt qua ô. |
| 33 | species_0035 | Trưởng Lão Người Cây | 4★ | Cần sửa | Mắt/râu/miệng gỗ rõ; gậy và FX không tràn ô. |
| 34 | species_0050 | Hải Long Ba Đầu | 4★ | Cần sửa | Đúng HAI đầu theo APK; đầu/cổ và nước không tràn ô. |
| 35 | species_0122 | Trùng Hốt Lỗ | 4★ | Atlas cũ | Xác minh mắt trắng; tách bụng, xúc tu, mặt. |
| 36 | species_0016 | Pharaon | 4★ | Ảnh thô | Phân biệt vải/giáp, nhịp gậy và đầu. |
| 37 | species_0036 | Hoa ăn Thịt Người Ba Đầu | 4★ | Atlas cũ | Đúng ba đầu; cổ lệch nhịp và không dính khối. |
| 38 | species_0051 | Long Vương Hắc Ám | 4★ | Ảnh thô | Mắt/hàm rõ, bớt chấm vảy; thở nặng. |
| 39 | species_0066 | Đại Ác Ma | 4★ | Ảnh thô | Tay tách thân đỏ, tránh highlight vàng át mắt. |
| 40 | species_0067 | Ma Vương Địa Ngục | 4★ | Ảnh thô | Mặt/sừng/ngực làm điểm nhấn; giáp vàng phụ trợ. |
| 41 | species_0084 | Tinh Tinh Rock | 4★ | Ảnh thô | Giữ nét hài hước, nắm đấm có trọng lượng. |
| 42 | species_0085 | Đại Tuyết Quái | 4★ | Ảnh thô | Giữ hoa và vẻ hiền; mặt tách lông trắng. |
| 43 | species_0086 | Gấu Trúc Ma Pháp | 4★ | Ảnh thô | Mắt/miệng rõ; cast bằng tay/thân. |
| 44 | species_0103 | Chim Đại Phì | 4★ | Ảnh thô | Giữ chim tròn, mắt/cá tính; lớp lông lớn. |
| 45 | species_0104 | Chim Đa Đa | 4★ | Ảnh thô | Mắt tách mào; cánh tách đuôi. |
| 46 | species_0123 | Trùng Gai Nhọn | 4★ | Atlas cũ | Chân tách khỏi gai dưới, giảm chấm sáng. |
| 47 | species_0137 | Ma Gương Thủy Tinh | 4★ | Atlas cũ | Xương tay/chân rõ; giữ gương đỏ không thêm mặt người. |
| 48 | species_0138 | Thú Lớn Dung Nham | 4★ | Atlas cũ | Mắt/khe nham nổi; thân nặng khi đánh. |

**A (1–3):** Giải quyết phản hồi Move 0146 trước, sau đó hoàn thiện hai anchor đã được vẽ lại. **B (4–14):** Special 5★ còn lại. **C (15–27):** 5★ thường. **D (28–31):** bốn Special 4★. **E (32–48):** 4★ thường, bắt đầu với bốn bản từng được ưu tiên sửa.

## Quy trình thực hiện cho từng dòng

1. Đọc record `data/p10/species.json`, hai ảnh APK gốc của đúng loài, atlas cũ của chính loài đó và nhận xét trong review. Ghi brief ngắn: nhận diện giữ, tính cách, điểm nhấn ở gameplay size, chất liệu, Attack/Cast, tỷ lệ/pivot.
2. Mở APK reference bằng `view_image`. Sinh bản thiết kế mới bằng built-in imagegen, chỉ đưa APK của chính loài vào references. Có thể xem raw cũ để chẩn đoán nhưng không đưa redraw vào generation references. Tạo thư mục attempt mới dưới `apps/game-client/assets/pets/redraws/polish-20261008/` theo ID trong bảng và số attempt tăng dần; lưu `prompt.txt`, `inputs.json`, `raw.png` trong đó.
3. Duyệt native raw trước pack. Nếu pose thiếu bộ phận, số vật cầm sai, layout chồng ô hoặc nền không trong suốt, ghi `repair_required` và sửa ảnh sinh. Sau hai lần sửa cùng lỗi mà chưa tiến bộ, lưu bằng chứng blocker, chuyển sang species kế tiếp; quay lại blocker trước khi công bố 100%.
4. Khi raw nguyên vẹn, tạo `layout.json` với 20 source rectangles/pivots thực, không suy đoán từ grid nếu hình bị lệch. Chạy pack NN bằng `tools/assets/pack_p10_atlas.py`; lưu `packing.json`, `packed.png` và raw SHA.
5. Chạy `tools/assets/check_p10_atlas.py` và export `tools/assets/preview_p10_redraw.py`. Chạy playback thực trên preview; lưu ảnh/GIF chẩn đoán và ghi rõ preset timing chỉ phục vụ review.
6. So bản mới với APK và atlas cũ trên nền sáng/tối, 64/96 px và scene battle thử. Một reviewer đọc đúng SHA, ghi `review.md` với các gate đạt/chưa đạt; cập nhật `result.json`.
7. Nếu cả tám gate đạt, đặt `qa_passed`, cập nhật tracker và **báo ngay sau loài đó**, rồi sang dòng kế. Nếu lỗi, `repair_required` không tăng %. Không đợi owner duyệt để tiếp tục loài độc lập; chờ owner duyệt trước runtime activation.

Lệnh kiểm tra hiện có cho species 0146 (geometry pass của bản này **không** chứng minh Move đạt):

```sh
rtk proxy tools/.cache/asset-venv/bin/python -B tools/assets/check_p10_atlas.py apps/game-client/assets/pets/redraws/polish-20261008/species_0146/attempt-04/packed.png
```

Khi vẽ lại, dùng `pack_p10_atlas.py --source --layout --output` và `preview_p10_redraw.py --atlas --out` theo CLI đã ghi trong hai script. Cả output atlas và preview directory phải là đường dẫn **mới** của attempt đang làm; hai tool không ghi đè.

**Mẫu báo sau mỗi species:**

> `#<thứ tự> <species_id> — <tên>: QA PASS/CHƯA ĐẠT. Tiến độ art: <k>/48 = <p>%. Owner duyệt: <a>/48. Đã kiểm tra: source identity, 20 frame, loop Move/Idle 64/96 px, Attack/Cast/Down, geometry, battle size. Atlas SHA: <hash>. Còn lỗi: <nếu có>. Preview: <link>.`

Nếu species chưa đạt, báo nguyên nhân và % giữ nguyên. Nếu owner yêu cầu sửa sau PASS, giảm `k` và báo lại % mới; không để số cũ tiếp tục xuất hiện trong gallery.

## Theo dõi và giới hạn

- Lưu một tracker `.ai/plan/phases/P10-pet-model/redraw-kit/polish-20261008/progress.json` với `total:48`, `qa_passed_ids`, `owner_approved_ids`, `blocked_ids`, `active_species_id`, `last_reported_percent`. Không suy tiến độ từ việc file `raw.png` hay `packed.png` tồn tại.
- Sau mỗi species, refresh gallery/report từ đúng `result.json`; gallery phải hiển thị badge `repair_required`, `qa_passed` hoặc `owner_approved` và SHA. Không route sprite vào runtime nếu chỉ QA pass.
- Tất cả blocker được giải quyết trước khi nói 48/48. Sau 48 QA pass, xin duyệt các bản chưa được owner chốt; sau owner approval mới cân nhắc kích hoạt và kiểm tra runtime theo phase riêng.
