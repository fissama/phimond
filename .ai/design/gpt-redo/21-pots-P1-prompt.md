# Prompt P1 — 5 chậu (G1 kiểu 2, G2 x2, G3 x2)
Copy khối dưới gửi Codex. Pilot chậu G1 Thổ Đào Bồn đã duyệt (garden-b/pot-g1-tho-dao) là chuẩn.

```
NHIỆM VỤ: Vẽ và đóng gói 5 atlas chậu cho khu vườn ngầm (garden-b): pot-g1b-thung-tre, pot-g2a-gao-dua, pot-g2b-truc-dong, pot-g3a-can-moc, pot-g3b-sanh-nau. KHÔNG ĐƯỢC DỪNG GIỮA CHỪNG: làm tuần tự từng chậu; chỉ báo xong khi cả 5 atlas qua đủ cổng của Đơn 16, hoặc có số đo chứng minh bất khả sau khi đã làm đúng Đơn 16. Không hỏi lại, tự quyết trong phạm vi tài liệu.

ĐỌC TRƯỚC: .ai/design/gpt-redo/16-garden-atlas-pipeline-v3.md, 14-garden-pots-anim-prompt.md (hợp đồng chậu, 5 hàng idle/wet/water/upgrade/clear), và pilot đã duyệt garden-b/pot-g1-tho-dao (final.png, anim.json, prompt.md, review.md).

CHUNG: Dùng ĐÚNG pipeline pilot: image_gen vẽ sheet nền #FF00FF -> tools/pack_atlas.py -> tools/measure_atlas.py (nhánh chậu). Không sửa pixel tay, không đổi tiêu chí, không tự đặt approved:true. Atlas 768x960 RGBA, 4x5 ô 192, đáy chậu y=175, tâm x=96, miệng chậu ellipse nằm quanh y≈112 để cây cắm vào pivot (96,112). Hàng: idle (lặp), wet (lặp, đất trong miệng SẪM hơn idle >=15% độ sáng, có bóng nước), water (một lần), upgrade (một lần, hiệu ứng nâng cấp rõ), clear (một lần, dọn đất/cây). Thân chậu đứng yên (IoU liền kề >=0.95, khung nối >=0.93). Chậu không có mặt. Tổng <=60 màu, alpha nhị phân, viền cùng tông, không glow/bóng/chữ baked. Bề ngang chậu <=158 px, cao thân <=100 px để cây không bị che. Đổi hẳn chất liệu giữa các chậu (không chỉ đổi màu), silhouette đọc được khi thu nhỏ, màu không bão hòa quá mức (tránh cam neon như lần pilot).

CÁC CHẬU:
1. pot-g1b-thung-tre — Thúng Tre Bồn (hạng G1): chiếc thúng/rổ tre đan nan đan chéo màu vàng tre, lót lá chuối ở miệng, đất nâu trong. Ấm, mộc mạc. Hiệu ứng water: nước thấm làm nan sẫm lại; upgrade: nan sáng lên, vài sợi tre mới nảy; clear: lá chuối cuộn lại.
2. pot-g2a-gao-dua — Gáo Dừa Bồn (hạng G2): nửa vỏ dừa nâu xơ, mặt cắt tròn, miệng viền nâu đậm, ba chân gỗ nhỏ. Đất đen mịn. water: giọt nước chảy xuống xơ dừa; upgrade: xơ dừa chải mượt, thêm vòng khắc; clear: nắp đất bật.
3. pot-g2b-truc-dong — Trúc Đồng Bồn (hạng G2): bó 3–4 ống tre đứng buộc dây, đốt tre rõ, miệng ống nhiều tầng. Xanh vàng nhạt. water: nước dâng trong ống; upgrade: măng non nhú ở chân; clear: đốt tre rung.
4. pot-g3a-can-moc — Căn Mộc Bồn (hạng G3): gốc cây rỗng, vỏ nâu sẫm, rễ nổi ở chân, rêu xanh ở viền. water: rêu tươi lên; upgrade: rễ cuộn, nụ nấm nhỏ; clear: rễ co lại.
5. pot-g3b-sanh-nau — Sành Nâu Bồn (hạng G3): lu sành men nâu có vân men chảy, miệng loe, nắp quai nhỏ. water: men sẫm lại, nước đọng; upgrade: men bóng hơn, đường chỉ vàng; clear: nắp lật.

LẶP TỰ SỬA: pack -> measure -> chỉ vẽ lại phần khung fail -> pack -> measure, cho tới khi mọi atlas qua 100% cổng. Mỗi vòng ghi vào review.md bảng cổng kèm số đo. Mỗi chậu tối đa 8 lượt ImageGen; hết lượt mà còn fail thì ghi số đo cụ thể và đề xuất, KHÔNG nới ngưỡng.

GIAO: cho mỗi chậu: final.png, anim.json, prompt.md, review.md, qa.json, preview từng hàng PNG/GIF, ảnh 4x có lưới pivot; cập nhật garden-b/manifest.json (status ready_for_claude_review, approved:false) và contact-sheet.png. Báo cuối: bảng atlas x cổng (số đo), file đã tạo/sửa, điểm sát ngưỡng.
```
