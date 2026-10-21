# Checklist giao GPT — sửa atlas pet 4★/5★ bị nhỏ

Ngày: 2026-10-20. Trạng thái: checklist để thực hiện; chưa vẽ hoặc chọn candidate trong tài liệu này.

**Mục tiêu:** pet to, rõ, đúng thiết kế hiện tại; lấy **Linh Tiên Hoa Hương, species_0144** làm chuẩn cảm quan humanoid. GPT tự so sánh và sửa liên tục từng loài cho đến khi đạt các cổng kiểm tra bên dưới. Chủ game duyệt bản cuối trước khi thay selection hoặc kích hoạt runtime.

**Cách thực hiện:** làm tuần tự từng loài bằng workflow `superpowers:executing-plans`; mỗi loài có candidate phiên bản mới, bằng chứng so sánh và review riêng. Không cần tạo thêm agent để bắt đầu. Nếu áp dụng reviewer độc lập theo contract, chỉ giao đọc candidate đúng hash sau khi bản tự review đã đạt.

## 1. Đọc và khóa nguồn trước khi vẽ

- [ ] Đọc `AGENTS.md` và `.ai/plan/phases/P10-pet-model/P10-redraw-plan.md`, gồm các phần bổ sung phía cuối: hướng dẫn mới ghi đè các quy định cũ bị thay thế.
- [ ] Đọc `size-audit-20261019/review.md`, `measurements.json` và 7 ảnh `contact-01.jpg` → `contact-07.jpg` trong cùng thư mục với checklist này.
- [ ] Lấy đúng bản đã chọn từ `redraw-kit/owner-atlas-selection.json` cho 152 loài; 8 loài mới lấy `extension-20261013/art-manifest.json`. Không chọn attempt theo tên thư mục lớn nhất.
- [ ] Ghi đường dẫn + SHA-256 bản trước khi sửa. Không ghi đè file gốc, không thay trạng thái đã duyệt bằng candidate chưa duyệt.
- [ ] Xem trực tiếp atlas cũ đủ 20 frame, ảnh nhận diện APK/JAR nếu có và các nhận xét riêng của chủ game. Tám loài mới là **Phimond-authored**; không gán provenance APK/JAR cho chúng.
- [ ] Mở chuẩn `apps/game-client/assets/pets/redraws/owner-feedback-20261009/species_0144/attempt-01/packed.png`; SHA-256 `63efbba22985c5e938be71bcfb2aebbc9db3ec1b9d12bd8d38c5a5ce5d666dd4`. Không sửa chuẩn.
- [ ] Nhớ chuẩn có idle đầu **164px**, trung bình 4 idle **162.75px** ở alpha ≥128. Đây là bbox silhouette gồm hoa/cánh, không phải chiều cao anatomy người thuần.

## 2. Quy tắc sửa size và thiết kế

- [ ] Giữ nhận diện, anatomy, tuổi/gương mặt, tóc, vũ khí, số tay/chân/cánh/sừng, palette và phong cách pixel đã duyệt. Sửa size/nét không phải thiết kế lại nhân vật.
- [ ] Nhìn nguyên nhân từng loài: hình vẽ chiếm ít pixel; runtime scale nhỏ; hay cả hai. Nhỏ trong game không tự chứng minh cần redraw.
- [ ] Với hình nguồn đã đủ rõ: thử bản đóng gói lớn hơn bằng **một scale đồng đều cho toàn bộ 20 frame**, nearest-neighbor, giữ pivot và đủ safe area. Ghi đây là repack, không gọi là redraw tăng chi tiết.
- [ ] Với hình nguồn thiếu chi tiết khi lớn lên: vẽ lại ở độ chi tiết phù hợp, không dùng upscale/blur/sharpen để giả chi tiết mới. Dùng công cụ sinh/chỉnh ảnh và đọc skill tương ứng trước khi vẽ; giữ raw output.
- [ ] Humanoid: thử silhouette idle quanh **155–180px** trong cell 281px, lấy Linh Tiên làm đối chiếu. Đây là mục tiêu thử, không ép anatomy hoặc thêm FX để đạt số.
- [ ] Thú bốn chân/rồng bò thấp/côn trùng bò ngang: xét **chiều dài, bề ngang và khối thân**, không ép đứng cao như humanoid. Ghi rõ ngoại lệ khi chiều cao thấp hơn mục tiêu nhưng khối đã rõ.
- [ ] Rồng/cự thú phải có cảm giác lớn hơn người khi đặt trong scene. Có thể dùng scale hiển thị riêng; khoảng 1.25–1.6× về cảm quan khối chỉ là phạm vi thử, chưa phải thông số runtime đã duyệt.
- [ ] Không làm rồng to bằng cách kéo giãn ảnh một trục. Không auto-fit từng frame làm nhân vật phồng/xẹp khi chạy/đánh.
- [ ] Không lấy đầu cánh, sừng, đao, aura hay hạt sáng làm thước thân. Ghi riêng bbox silhouette và nhận xét khối anatomy bằng mắt.
- [ ] Pet 5★ có FX phong phú và Special có điểm nhấn riêng; FX không che mặt/thân và không được dùng để che việc pet còn mini.
- [ ] Giữ hướng gốc **sang trái** theo các atlas hiện tại và yêu cầu mới của chủ game; cú đánh/skill nhất quán với hướng đối thủ. Quy tắc screen-right cũ trong contract không dùng để lật hàng loạt bản trái đã duyệt.
- [ ] Giữ các chi tiết đã chốt: Bọ Cạp càng nhiều lớp sắc nhọn, lớn và hình người nam trung niên; Thần Đèn mũi đèn bên trái, đuôi uốn nối vào mũi đèn; Ma Chủ trẻ shonen khoảng 20 tuổi, tóc gọn trắng ánh tím và mắt lạnh; Long Thần giữ yêu cầu cánh đã duyệt gần nhất.

## 3. Contract atlas bắt buộc cho mọi candidate

- [ ] PNG RGBA trong suốt **1124×1405**, **4 cột × 5 hàng**, cell **281×281**, 20 frame có nội dung và khác nhau.
- [ ] Mọi pixel alpha >0 nằm trong cell-local **x/y [22,259)**, kể cả FX mờ. Không cắt bộ phận/hiệu ứng hoặc xóa alpha để vượt gate.
- [ ] Hàng 1 idle: 4 frame khác nhau, loop 4→1 êm.
- [ ] Hàng 2 movement: 4 pose locomotion, loop 4→1 êm; không chỉ dịch chuyển một hình tĩnh.
- [ ] Hàng 3 basic attack: chuẩn bị → lấy đà → impact → thu thế; one-shot.
- [ ] Hàng 4 skill: tụ → tạo hình → phóng/thi triển → tan; one-shot, đúng signature/thiết kế loài.
- [ ] Hàng 5 hurt/down: trúng đòn → yếu → ngã → **fully down**; one-shot và giữ frame cuối.
- [ ] Chỉ idle/movement loop. Đầu, mặt, tóc, màu, vũ khí/phụ kiện không đổi giữa frame; không mất/thêm chi hoặc lật ngẫu nhiên.
- [ ] Outline và pixel clusters rõ; không AA, blur, bloom, glow trùm thân, nền, chữ hoặc watermark. Không nén mất chi tiết.
- [ ] Khi pack: giữ đủ 20 source rectangles, source image, transform/pivot và common scale. Không thay pixel art bằng code tự vẽ.

## 4. Vòng lặp bắt buộc cho từng loài

### A. Chẩn đoán và candidate

- [ ] Chụp trước sửa: idle và 4 hàng còn lại, thông số H/W, trạng thái approval và hash.
- [ ] Viết 2–4 lỗi cụ thể cần sửa: ví dụ thân nhỏ, mắt mất nét, vũ khí dính thân. Ghi phương án repack/redraw/scale-only và lý do.
- [ ] Tạo candidate dưới `apps/game-client/assets/pets/redraws/size-remedy-20261020/<species_id>/attempt-XX/`; giữ nguyên các attempt trước.
- [ ] Ghi `prompt.md`, raw image, `packed.png`, `metadata.json` và SHA-256. Nếu chỉ cần runtime scale, ghi `scale_only_review` thay vì tạo redraw không cần thiết.

### B. So sánh công bằng

- [ ] Xuất triptych **bản cũ / bản mới / Linh Tiên**: cell hiển thị cố định **96px và 192px**, cùng nền/zoom, không auto-fit từng card.
- [ ] Thêm crop **281px native** để soi pixel; không dùng ảnh zoom lớn làm bằng chứng duy nhất cho độ rõ trong game.
- [ ] Xuất đủ 20 frame trên contact sheet và preview playback 5 hàng; idle/movement loop, 3 hàng còn lại one-shot/hold đúng nghĩa.
- [ ] So silhouette không FX và frame có FX bằng mắt; không xóa FX khỏi ảnh thật để tạo số đo đẹp. Bbox alpha không phải body mask.
- [ ] Ghi rõ phần nào nhỏ hơn/lớn hơn chuẩn là do anatomy, không dùng một tỷ lệ H duy nhất để phán mọi loài.
- [ ] Nếu mô phỏng cỡ hiển thị lớn hơn người: ghi rõ scale đề xuất và nhãn **preview**, không gọi là gameplay đã chạy thật.

### C. Tự review và sửa tiếp

- [ ] Review toàn bộ 20 frame theo 6 mục: size/khối, nét/mặt, anatomy/identity, pivot, hướng/animation, FX/containment.
- [ ] Mỗi lỗi phải có `species_id`, hash, hàng/frame, biểu hiện cụ thể, mức độ, cách sửa. Không nhận xét chung “chưa đẹp”.
- [ ] Nếu bất kỳ mục bắt buộc nào fail: tạo attempt kế tiếp, kiểm tra lại tất cả 20 frame và lặp B→C. Không chỉ soi frame vừa sửa.
- [ ] Bản mới không được tệ hơn bản cũ ở motion, mặt, anatomy, màu hay độ rõ; nếu regress thì giữ bản tốt nhất và sửa tiếp từ đó.
- [ ] Không dừng chỉ vì đã đủ số vòng hoặc mechanical PASS. Nếu công cụ lỗi/hết quota/không truy cập được nguồn: ghi `blocked` và lỗi thật, không đánh dấu đạt.
- [ ] Khi mọi mục đạt: ghi **self_review_pass_pending_owner**, chuyển loài tiếp theo. Review độc lập theo contract trước khi đề xuất selection; chủ game giữ quyền duyệt thẩm mỹ cuối.

## 5. Chốt cả batch và điều kiện dừng

- [ ] Tất cả 32 loài được sàng lọc đều có kết quả riêng: candidate đạt, scale-only có bằng chứng, hoặc ngoại lệ anatomy có giải thích. Không tự gộp tất cả thành “đã vẽ lại”.
- [ ] Đối chiếu lại cả **56 loài** cạnh chuẩn, bao gồm 24 loài đối chứng, để tránh sửa một nhóm thành quá to hoặc lệch mật độ pixel.
- [ ] Với 24 loài đối chứng: chỉ mở thêm redraw nếu phát hiện lỗi cụ thể; ghi ID và lý do vào batch thay vì sửa ngầm.
- [ ] Kiểm tra hash toàn bộ art ngoài scope không đổi; không sửa stable IDs, registry/provenance, stats, skill rules hoặc source APK/JAR.
- [ ] 5 candidate mới 0153/0155/0157/0159/0160 vẫn giữ trạng thái chờ owner nếu chưa có phê duyệt mới. Không suy diễn “size đạt” thành “owner duyệt”.
- [ ] Deliver: trang review, before/after 96/192px, 20-frame sheet, playback, measurements, prompt/raw/packing provenance, hash và báo cáo lỗi đã sửa/còn tồn.
- [ ] **Art review hoàn tất** chỉ khi toàn bộ mục bắt buộc đạt, không còn lỗi size/nét chưa xử lý và có disposition từng loài. Không đồng nghĩa runtime/gameplay hoàn tất.
- [ ] **Runtime nghiệm thu riêng:** scene đúng atlas mapping, Linh Tiên + player cạnh pet, world và battle camera thật, test 20 frame, UI hẹp/1v3, full-res/low-tier và texture budget. Nếu chưa có scene thì ghi chưa nghiệm thu in-game.
- [ ] Không activate runtime, thay owner selection, push/merge, restart server hay đụng DB trong checklist art này. Candidate đúng hash vẫn chờ chủ game duyệt theo contract.

## 6. Mẫu báo cáo mỗi vòng

```text
Species: <stable_id + tên>
Before: <path + sha256 + approval>
Attempt: <path + sha256>
Action: repack / redraw / scale-only / anatomy exception
Size: old H×W -> new H×W; comparison cell 96/192px
Body review: <khối anatomy, FX ảnh hưởng phép đo thế nào>
Frame review: idle / move / attack / skill / down + chỉ rõ frame lỗi
Fixed: <lỗi đã sửa và ảnh chứng minh>
Remaining: <lỗi còn lại hoặc none>
Mechanical: PASS/FAIL + report path
Visual: PASS/FAIL + comparison/playback paths
Decision: retry / blocked / self_review_pass_pending_owner
Runtime: not activated; in-game verification pending nếu chưa test thật
```

## 7. Prompt có thể giao thẳng cho GPT

> Thực hiện checklist `.ai/plan/phases/P10-pet-model/size-audit-20261019/REDRAW_CHECKLIST_20261020.md` trong project `/Users/phileanh/rust/phimond`. Đọc contract và audit được dẫn trong checklist trước. Làm từng loài, ưu tiên batch A rồi B; tạo bản mới giữ thiết kế/palette/anatomy đã duyệt. Lấy species_0144 Linh Tiên Hoa Hương làm chuẩn người. Với nguồn đủ nét chỉ cần repack/scale, ghi đúng loại xử lý; nguồn thiếu chi tiết thì redraw. Không ép thú bốn chân cao bằng humanoid. Sau mỗi attempt tự so bản cũ/mới/chuẩn tại cùng cell 96/192px, soi 20 frame và playback 5 hàng, nhận xét lỗi cụ thể rồi sửa tiếp cho đến khi không còn lỗi bắt buộc. Sau cùng so lại đủ 56 loài, báo cáo từng loài và trạng thái thật. Không overwrite art cũ, không tự phê duyệt candidate hay kích hoạt runtime. Nếu bị chặn bởi công cụ thì báo rõ, không giả hoàn tất. Bắt đầu bằng loài đầu tiên trong batch A.

## 8. Danh sách thực hiện từ audit 2026-10-19

Chiều cao dưới đây là **trung bình bbox alpha ≥128 của 4 idle**, không phải số pixel thân thuần. Batch A gồm 13 loài dưới 100px; batch B là 19 loài còn lại dưới 80% chuẩn. Các mức này chỉ là ưu tiên sàng lọc, không phải phán quyết bắt buộc redraw.

### Batch A — 13 nguồn rất nhỏ, xử lý trước

- [ ] **species_0138 — Thú Lớn Dung Nham (4★)**: 63.5×60.5px; H/chuẩn 0.39. Nhỏ nhất nhóm, 63.5px; ưu tiên thử tăng lớn và QA nguồn, có thể cần redraw nếu thiếu nét.
- [ ] **species_0141 — Totem Thượng Cổ (5★)**: 66.0×55.5px; H/chuẩn 0.41. 66px, họa tiết quá li ti; nhóm ưu tiên QA nguồn sau tăng size.
- [ ] **species_0147 — Người Tuyết Viễn Cổ (5★)**: 70.25×92.5px; H/chuẩn 0.43. 70.25px, cự thú đang thành mini; ưu tiên lớn hơn người và QA mặt/tay.
- [ ] **species_0068 — Thanh Long (4★)**: 79.25×80.5px; H/chuẩn 0.49. Thanh Long rất nhỏ; ưu tiên tăng khối rồng và QA lại chi tiết nguồn.
- [ ] **species_0037 — Độc Đằng Nữ (5★)**: 81.5×85.5px; H/chuẩn 0.50. Rất nhỏ ở ô chung; chi tiết mặt/thân dễ mất, cần thử tăng cỡ và QA nguồn.
- [ ] **species_0086 — Gấu Trúc Ma Pháp (4★)**: 89.0×95.0px; H/chuẩn 0.55. Dáng chibi hợp thiết kế nhưng quá nhỏ tại cùng ô; tăng vừa, giữ anatomy.
- [ ] **species_0087 — Bạch Hổ (4★)**: 90.25×146.5px; H/chuẩn 0.56. Thú bốn chân thấp là đúng; căn chiều dài/thân, không ép chiều cao bằng người.
- [ ] **species_0139 — Huyền Vũ (4★)**: 91.5×115.0px; H/chuẩn 0.56. Dáng bốn chân thấp; tăng khối/chiều dài, không ép cao như humanoid.
- [ ] **species_0084 — Tinh Tinh Rock (4★)**: 94.75×94.0px; H/chuẩn 0.58. Khỉ thấp nhưng khối nhỏ; scale theo thú to, không ép cao như người.
- [ ] **species_0124 — Trùng Bất Tử Địa Huyệt (5★)**: 96.0×141.5px; H/chuẩn 0.59. Thấp vì anatomy bò ngang; căn bề ngang/thân, QA chân ở cỡ đích.
- [ ] **species_0017 — Rồng Xương Băng (5★)**: 96.25×125.25px; H/chuẩn 0.59. Rồng xương nhỏ cả chiều cao lẫn bề ngang; cần lớn hơn người về tổng khối.
- [ ] **species_0154 — Thiết Giáp Long (5★)**: 96.5×131.0px; H/chuẩn 0.59. Rồng thấp/bò ngang; tăng khối/chiều dài, không ép đứng cao như humanoid; giữ bản duyệt.
- [ ] **species_0069 — Trụy Thiên Sứ (5★)**: 97.5×86.5px; H/chuẩn 0.60. Humanoid/cánh nhỏ; tăng cỡ để mặt và vũ khí dễ đọc.

### Batch B — 19 loài cần trial size và sửa tiếp

- [ ] **species_0067 — Ma Vương Địa Ngục (4★)**: 100.0×68.0px; H/chuẩn 0.61. Người và vũ khí nhỏ, mặt ít pixel; ưu tiên kiểm tra nguồn ở cỡ lớn.
- [ ] **species_0085 — Đại Tuyết Quái (4★)**: 101.75×94.5px; H/chuẩn 0.62. Yeti cần to hơn người về khối; nguồn hiện nhỏ, QA mặt/tay khi tăng.
- [ ] **species_0015 — Tử Thần (4★)**: 103.75×94.5px; H/chuẩn 0.64. Dáng người/lưỡi hái nhỏ; tăng hiển thị, kiểm tra mặt và vũ khí ở cỡ đích.
- [ ] **species_0107 — Đại Bàng Vàng (5★)**: 104.0×113.5px; H/chuẩn 0.64. Chim nhỏ khi đứng cạnh chuẩn; tăng size, QA đầu và mỏ.
- [ ] **species_0137 — Ma Gương Thủy Tinh (4★)**: 104.5×93.0px; H/chuẩn 0.64. Gương/chi nhỏ; tăng vừa, kiểm tra mặt gương trên nền tối.
- [ ] **species_0156 — Đao Ma Huyết Giáp (5★)**: 112.0×131.5px; H/chuẩn 0.69. Thân/đao bị lửa lấn; tăng cỡ và QA readability; giữ bản duyệt.
- [ ] **species_0051 — Long Vương Hắc Ám (4★)**: 113.25×135.5px; H/chuẩn 0.70. Rồng tối tương đối nhỏ và tối; tăng size rồi kiểm tra tương phản trên nền map.
- [ ] **species_0122 — Trùng Hốt Lỗ (4★)**: 114.25×104.5px; H/chuẩn 0.70. Dáng đứng nhỏ hơn chuẩn; tăng vừa để đọc rõ mặt và tay.
- [ ] **species_0145 — Cây Cự Linh (5★)**: 116.25×135.25px; H/chuẩn 0.71. Cự linh nhỏ so tên/khối dự kiến; tăng hiển thị, giữ nguyên nguồn duyệt.
- [ ] **species_0126 — Trùng Mẫu Mào Vàng (5★)**: 117.0×105.0px; H/chuẩn 0.72. Thân humanoid trên bụng côn trùng nhỏ; tăng size để đọc mặt.
- [ ] **species_0016 — Pharaon (4★)**: 118.5×84.0px; H/chuẩn 0.73. Pharaon thấp hơn chuẩn người; ưu tiên scale, giữ tỷ lệ người thanh mảnh.
- [ ] **species_0038 — Tinh Linh Bách Hoa (5★)**: 120.0×110.0px; H/chuẩn 0.74. Tiên dáng người nhỏ hơn chuẩn; tăng hiển thị, không dùng cánh/hoa làm thước thân.
- [ ] **species_0140 — Nhân Sư (5★)**: 122.75×132.0px; H/chuẩn 0.75. Nhân Sư nên nặng và rộng hơn người; scale theo thân/sải chân.
- [ ] **species_0148 — Ngựa Bùn Cỏ (5★)**: 123.75×94.5px; H/chuẩn 0.76. Thiết kế chibi, không đổi anatomy; tăng vừa, tránh thành pet mini.
- [ ] **species_0106 — Chim Cú Địa Ngục (5★)**: 125.25×134.0px; H/chuẩn 0.77. Cú lớn cần tăng khối; so thân riêng khỏi cánh.
- [ ] **species_0035 — Trưởng Lão Người Cây (4★)**: 126.0×121.5px; H/chuẩn 0.77. Người cây cần khối lớn và tay/cành rõ hơn; thử scale trước.
- [ ] **species_0036 — Hoa ăn Thịt Người Ba Đầu (4★)**: 127.25×127.5px; H/chuẩn 0.78. Ba đầu đọc được; scale đều, không bắt cây bò ngang cao bằng humanoid.
- [ ] **species_0103 — Chim Đại Phì (4★)**: 127.75×128.0px; H/chuẩn 0.79. Dáng tròn đọc rõ; tăng vừa theo khối, giữ thiết kế chim.
- [ ] **species_0020 — Thủ Lĩnh Hắc Ám (5★)**: 128.75×147.0px; H/chuẩn 0.79. Kỵ sĩ/thú cưỡi nên có tổng khối lớn hơn humanoid, không chỉ tăng chiều cao.

### Batch C — 24 đối chứng, bắt buộc so lại cuối batch

| ID | Loài | Sao | Idle H×W | Trọng tâm đối chiếu |
|---|---|---:|---:|---|
| species_0018 | Nữ Vương Bạch Cốt | 5 | 145.25×115.0 | Silhouette rõ; tăng nhẹ theo chuẩn người, tránh tính cánh là thân. |
| species_0019 | Nữ Đế Minh Giới | 5 | 139.0×125.0 | Silhouette rõ; scale nhẹ, đo thân riêng khỏi quả cầu phép. |
| species_0050 | Hải Long Ba Đầu | 4 | 136.25×172.0 | Ba đầu và bề ngang khá rõ; đề xuất khối rồng lớn hơn người. |
| species_0052 | Thánh Rồng Thái Cổ | 5 | 143.75×138.5 | Nguồn khá rõ; tăng profile rồng, không cần mặc định vẽ lại. |
| species_0066 | Đại Ác Ma | 4 | 131.0×103.5 | Ác ma khá rõ; căn lại theo chuẩn người/cơ thể, không theo sải cánh. |
| species_0088 | Sói Xích Viêm | 5 | 138.5×144.0 | Khối thú khá rõ; tăng vừa theo vai/lưng, loại lửa khỏi phép đo thân. |
| species_0104 | Chim Đa Đa | 4 | 168.25×151.5 | Size nguồn gần chuẩn; không cần phóng đồng loạt chỉ vì 4 sao. |
| species_0105 | Chu Tước | 4 | 153.0×146.0 | Silhouette tốt; profile chim lớn, chừa chỗ đuôi/lửa. |
| species_0123 | Trùng Gai Nhọn | 4 | 154.75×138.5 | Nguồn tương đối rõ; ưu tiên scale/context, chừa khoảng cho gai. |
| species_0125 | Nhện Phu Nhân | 5 | 162.75×129.0 | Nguồn gần chuẩn, rõ; không cần vẽ lại vì size. |
| species_0142 | Thần Tướng Cự Ma | 5 | 142.25×142.0 | Khối lớn rõ; profile cự thú, đừng ép cùng cao với pet nhỏ. |
| species_0143 | Thần Đèn | 5 | 139.25×126.0 | Djinn khá rõ; tăng nhẹ theo thân + đèn, giữ nối đuôi và mũi đèn. |
| species_0144 | Linh Tiên Hoa Hương | 5 | 162.75×165.5 | Chuẩn size humanoid do chủ game chọn; giữ nguyên PNG. |
| species_0146 | Ma Vương Hút Máu | 5 | 140.5×156.25 | Nguồn khá rõ; scale theo thân, không lấy đao/cánh làm chiều cao người. |
| species_0149 | Thú Vàng Một Sừng | 5 | 131.25×164.5 | Bốn chân/sừng rõ; giữ thấp hơn người ở vai nhưng đủ dài và to. |
| species_0150 | Đảo Thiên Đường | 5 | 155.0×161.0 | Nguồn rõ; scale theo chim và chừa đuôi, không cần redraw size. |
| species_0151 | Đại Vương Bọ Cạp | 5 | 160.25×164.0 | Khối/càng rõ; profile lớn và rộng, giữ art đã duyệt. |
| species_0152 | Chim Ái Thần | 5 | 136.5×174.0 | Cánh rộng nhưng người nhỏ hơn bbox; scale theo thân humanoid, chừa cánh. |
| species_0153 | Hươu Rêu Nguyệt | 5 | 166.25×134.5 | Nguồn mới đã gần chuẩn ô; cần profile thú bốn chân khi runtime được duyệt. |
| species_0155 | Tinh Vân Long | 5 | 160.25×185.25 | Nguồn mới rõ và rộng; profile rồng lớn hơn người, chưa kích hoạt runtime. |
| species_0157 | Ma Nhãn Hư Không | 5 | 160.0×166.75 | Nguồn mới gần chuẩn; căn lõi/mắt riêng khỏi xúc tu/FX, không cần cố lớn như rồng. |
| species_0158 | Hộ Vệ Thạch Linh | 5 | 142.25×137.75 | Khối rõ; profile golem lớn hơn người, giữ bản duyệt. |
| species_0159 | Long Thần Song Ấn | 5 | 169.5×167.25 | Nguồn mới gần chuẩn; profile Special rồng lớn, chừa hai cánh và ấn. |
| species_0160 | Ma Chủ Song Cực | 5 | 167.75×155.75 | Nguồn mới gần chuẩn người; giữ tỷ lệ shonen, FX không quyết định size thân. |

## 9. Tự kiểm checklist trước khi giao

- [x] Danh sách đủ 56 ID duy nhất, 13 + 19 + 24; không thiếu 8 loài mới.
- [x] Có baseline, geometry, animation, hướng, provenance, bảo toàn approval và runtime gate riêng.
- [x] Có quy trình retry và điều kiện dừng dựa trên lỗi, không dựa vào số attempt.
- [x] Có so cùng tỷ lệ, tránh lấy FX/bbox thay anatomy hoặc ép rồng bò thấp thành humanoid.
- [x] Chỉ soạn tài liệu ở lượt này; mọi checkbox thực thi và acceptance vẫn để trống.
