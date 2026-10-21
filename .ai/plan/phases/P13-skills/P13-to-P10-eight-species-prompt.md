# Prompt chuyển về P10 — mở rộng roster và art từ 152 lên 160

Copy phần dưới sang task P10. Đây là yêu cầu mở rộng P10, không phải handoff đóng P13.

---

Hãy thực hiện P10 extension cho **8 species authored mới: 6 Normal 5★ và 2 Special Hybrid 5★**, nâng danh sách hiệu lực từ 152 lên 160. Chủ dự án đã yêu cầu bổ sung tám loài này để đủ lựa chọn vật lý/phép và đường dung hợp; P13 vẫn đang nghiệm thu design, không coi toàn phase đã được duyệt.

Đọc AGENTS.md, `.ai/plan/phases/P10-pet-model/P10-redraw-plan.md`, `redraw-kit/owner-atlas-selection.json`, closure P10 và `.ai/plan/phases/P13-skills/P13-owner-feedback-v7.md` trước khi làm. Catalog numeric/role/MP candidate nằm tại `P13-candidate-species-catalog-160.json`; danh mục pool/signature/recipe ở `roster-review-package.json`, revision `P13-candidate-v7-20261013`. Không tự đổi role/hệ/class của tám loài để khớp hình vẽ.

**Danh sách cần đăng ký và vẽ** — tên/hệ là design candidate, ID dưới đây là proposal ID để đối chiếu, chưa phải stable ID P10:

1. **P13-NEW-01 — Nguyệt Đài Lộc**: race `beast`, Normal 5★, primary `magic_dps`, hệ `earth`. Hươu thanh mảnh bốn chân; một cặp gạc phân nhánh phủ rêu và mầm lá nhỏ, một đuôi ngắn. Lông nâu đất, rêu xanh ngọc, điểm sáng hổ phách gọn quanh gạc. Nhận diện phép bằng gạc/lõi sáng; tránh dáng ngựa, sừng đơn hoặc silhouette trùng Vân Mao Đà/Kim Kỳ Lân. Basic dùng gạc/chân trước; skill Địa gom hạt sáng rồi phóng một đợt năng lượng đất gọn. Hồi phục phụ trong brief không tự gán thêm role Support ngoài catalog candidate.

2. **P13-NEW-02 — Thiết Giáp Long**: race `dragon`, Normal 5★, primary `physical_dps`, hệ `earth`. Rồng bốn chân thấp và chắc, giáp đá xám sẫm/nâu sắt, bụng đất vàng, đuôi chùy một đầu; gai giáp có số lượng/vị trí ổn định. Khác rồng mảnh dùng phép, không đổi thành chim/rồng bay chỉ vì hiệu ứng. Basic vung đuôi hoặc húc; skill vật lý là cú đập/quét có mảnh đá nhỏ. Giáp thể hiện phòng thủ bản thân, không tự thêm role Tank hoặc cơ chế miễn nhiễm.

3. **P13-NEW-03 — Tinh Vân Long**: race `dragon`, Normal 5★, primary `magic_dps`, hệ `light`. Rồng dáng mảnh, hai cánh/vây lớn gọn, hai sừng, một đuôi dài; vảy xanh đêm, viền ngà, họa tiết sao vàng nhạt và lõi sáng ở ngực. Giữ các chi rõ khi thu nhỏ; không biến thành quầng sáng mất thân. Basic dùng vuốt; skill gom các điểm sáng thành một luồng Quang hướng đối thủ, tránh phủ kín sprite. Phải khác Thái Cổ Thánh Long và Special Long Thần Song Ấn.

4. **P13-NEW-04 — Đao Ma Huyết Giáp**: race `demon`, Normal 5★, primary `physical_dps`, hệ `fire`. Ác ma hai chân, vai rộng, hai sừng ngắn, mặc giáp đen nứt đỏ than; cầm **một đao lớn**, không tăng số vũ khí giữa frame. Màu đen/xám sắt với đỏ gạch và cam ít; không vẽ máu me. Basic chém đao; skill quét đao với vệt Hỏa ngắn và bụi va chạm. Nhận diện chiến binh vật lý, khác caster mắt bay và Huyết Ma Vương.

5. **P13-NEW-05 — Ma Nhãn Hư Không**: race `demon`, Normal 5★, primary `magic_dps`, hệ `dark`. Một mắt trung tâm lớn nằm trong thân/rèm bóng tối nhỏ, vòng ấn tím tối và ba mảnh rune gọn; cố định số mắt/rune/phụ kiện trong atlas. Di chuyển lơ lửng nhưng vẫn có silhouette và điểm neo rõ. Màu tím than, xanh đen, pupil hồng tím gọn. Basic va/chạm hoặc quất tua ngắn; skill tụ ấn rồi phóng xung Âm từ mắt. Không vẽ toàn thân glow/blur, không tạo thêm mắt ở frame tấn công. Loài này là bố mẹ phép cho Nữ Đế và Huyết Ma Vương trong candidate P13.

6. **P13-NEW-06 — Hộ Vệ Thạch Linh**: race `spirit`, Normal 5★, primary `physical_dps`, hệ `earth`. Linh thể đá hai chân, hai cánh tay với nắm đấm lớn, đầu/lõi nhỏ, các khối đá có đường ráp nhất quán. Đá xám nâu, lõi xanh ngọc nhỏ; mặt rõ, không sao chép Nhân Sư hay Cự Ma. Basic đấm thẳng; skill đập/quét đất vật lý, bụi đá gọn. Khi down phải sụp nằm/hạ khối thân hoàn toàn, không chỉ đứng choáng. Thể hiện phòng thủ bằng tư thế, không tự thêm role Tank ngoài catalog.

7. **P13-SPECIAL-01 — Long Thần Song Ấn**: race `dragon`, Special 5★, `hybrid / support`, hệ `light`. Rồng bốn chân uy nghi, hai sừng, hai cánh gọn, một đuôi; hai cụm giáp ngà/xanh ngọc và dấu ấn Quang màu vàng nhạt. Vuốt/cơ bắp thể hiện vật lý, lõi/ấn thể hiện phép; trang trọng hơn Normal, khác Thanh Long và Tinh Vân Long. Basic dùng vuốt. Row skill thể hiện **Long Thần · Song ấn**: một cú vuốt Quang, sau đó hai dấu ấn gọn sáng ở thân. Luật P13: 1.35×ATK Quang, hit mới tự tăng MAG 20% trong 2 vòng; 28MP/CD3/Lv40, rank1, không kế thừa, chiếm một slot. Không minh họa thành hai action hoặc cộng ATK+MAG trong một hit. Recipe: Thái Cổ Thánh Long + Nhân Sư → Long Thần Song Ấn.

8. **P13-SPECIAL-02 — Ma Chủ Song Cực**: race `demon`, Special 5★, `hybrid / disruptor`, hệ `dark`. Ác ma hai chân, hai sừng, thân giáp chắc; một tay cầm một vũ khí, tay còn lại tạo một ấn phép. Giáp tím than/đen, điểm nhấn xanh lạnh và tím hồng; phân biệt tay vật lý và tay phép bằng hình khối, không bằng full-body glow. Basic dùng vũ khí. Row skill thể hiện **Ma Chủ · Nghịch ấn**: tay phép tụ ấn rồi phóng một xung Âm ngắn. Luật P13: 1.35×MAG Âm; sau hit, 70% base chance giảm ATK địch 20% trong 2 vòng, qua SR, cleanse được; 28MP/CD3/Lv40, rank1, không kế thừa, chiếm một slot. Recipe: Đọa Thiên Sứ + Nhân Sư → Ma Chủ Song Cực.

**Đăng ký roster/provenance:**

- Bổ sung stable IDs bằng cơ chế registry hiện có; có thể đề xuất `species_0153`…`species_0160` theo thứ tự trên **chỉ sau khi kiểm tra chúng chưa được cấp**. Trả lại bảng ánh xạ proposal ID → stable ID cho P13 cập nhật owner/signature/pool/recipe references.
- Giữ nguyên 152 stable IDs, metadata nguồn và hash asset APK/JAR. Tám loài mới có provenance Phimond-authored, không giả source enum/path/hash hoặc tuyên bố recovered từ APK. Nếu file 152 hiện tại là snapshot nguồn frozen, giữ snapshot ấy và tạo lớp catalog hiệu lực 160 có namespace authored rõ ràng; cập nhật list/review UI/registry dẫn xuất cho đúng 160.
- Sáu loài đầu là Normal 5★; hai loài cuối Special 5★, không phải 6★. Hai Normal cùng bậc ghép thành Special cùng bậc. P13 có 28 recipe candidate; không tự khôi phục recipe APK vì tiện schema, không bật runtime dung hợp hay chỉnh công thức P11 trong task art/list.

**Art contract:** dùng style của 152 atlas đã owner duyệt trong owner-atlas-selection, không lấy failed/rejected candidates làm anchor. Mỗi loài một PNG RGBA trong suốt **1124×1405**, **4 cột × 5 hàng**, cell **281×281**, **20 frame khác nhau**. Mọi pixel alpha>0 nằm trong tọa độ cell-local **[22,259)** cả x/y. Row 1 idle loop, row 2 movement loop, row 3 basic attack one-shot, row 4 skill one-shot, row 5 hurt→fully down one-shot. Impact ưu tiên hướng phải; anatomy/vũ khí/phụ kiện/pivot/palette nhất quán. Pixel clusters rõ, outline tối có màu, không AA/blur/bloom/text/watermark/background. Special có presence nổi bật nhưng vẫn đúng containment, tỷ lệ hiển thị theo contract P10 đã cập nhật. Với Normal, row skill thể hiện hướng chiến đấu chính, không tự gắn skill độc quyền.

Preserve raw generations và lịch sử/hash từng candidate. Chạy kiểm tra geometry/alpha/20-frame distinctness, review animation/identity ở game scale, cập nhật art manifest và browser review để mình duyệt 8 loài. Không thay 152 atlas đã duyệt để làm đủ count. Báo đầy đủ 160 effective records, 8 mapping mới, art paths/hashes và các mục còn chờ owner; không gọi art mới đã được duyệt chỉ vì mechanical tests pass.
