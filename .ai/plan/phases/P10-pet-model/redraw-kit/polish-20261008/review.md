# P10 polish candidates — 2026-10-08

Owner: chọn A cho Ma Vương Hút Máu; yêu cầu review/sửa cả hai anchor.

Built-in image_gen: 6 lần gọi, gồm các vòng sửa có vấn đề cụ thể. Prompt và input hashes nằm trong generation-calls.json và inputs.json từng attempt. Không dùng MiniMax.

PASS: 305 original PNG/manifest Git objects unchanged; hai historical anchor unchanged.

Ba candidate đều mechanical PASS: RGBA,1124×1405,20 distinct occupied frames, safe alpha containment. Source rectangles/pivots và common NN scale nằm trong layout/pack-report. Không xóa alpha hoặc repaint bằng Python.

Static visual review: đã xem đủ20 frame của từng candidate trên nền sáng; Ma Vương giữ một đao trong cast, impact tail gọn; Đảo có collapse; Độc có blink và plant wilt/bud. Có faint alpha artifacts trong raw; không tự erase. Cần review độ đọc 64/96px và loop/pivot bằng playback. Không khẳng định hoàn mĩ hoặc đã được owner duyệt.

## Candidates

### Độc Đằng Nữ

Vẽ sửa mắt/biểu cảm và pose cast; đóng atlas chuẩn. Cần kiểm tra playback và độ đọc khi scale.

- Candidate: apps/game-client/assets/pets/redraws/polish-20261008/species_0037/attempt-02/packed.png
- SHA256: a5a2eb7bbc7b69ff107f65974758f9a12d7a6824619552d38faf621472a73f02
- Opaque idle height: 166px (không phải scale gameplay)
- Preview: apps/game-client/assets/pets/redraws/polish-20261008/species_0037/attempt-02/preview/preview.html

### Ma Vương Hút Máu

Hướng A nặng/hung dữ: mặt rõ, lấy đà chém mạnh, cast gầm với đao giữ nguyên, đuôi pose impact gọn.

- Candidate: apps/game-client/assets/pets/redraws/polish-20261008/species_0146/attempt-04/packed.png
- SHA256: e801c3d364f919509c84af935c9e15fbe8b2be127fcaf980c03bde9cb7a47114
- Opaque idle height: 168px (không phải scale gameplay)
- Preview: apps/game-client/assets/pets/redraws/polish-20261008/species_0146/attempt-04/preview/preview.html

### Đảo Thiên Đường

Sửa hàng hurt/down để hai pose cuối thực sự nằm gục; giữ đầu đỏ, cánh xanh và crest tím.

- Candidate: apps/game-client/assets/pets/redraws/polish-20261008/species_0150/packed-v2.png
- SHA256: 4e4ed7a3c2b1d7a9679dea43a3045880082c5b27c5d3c74b9e8172ff8401cad2
- Opaque idle height: 160px (không phải scale gameplay)
- Preview: apps/game-client/assets/pets/redraws/polish-20261008/species_0150/preview-v2/preview.html

## Còn lại

Owner duyệt art và playback. Sau đó mới cân nhắc selection/activation. Tiếp tục debate các loài late-game khác theo review48 loài; chưa triển khai runtime sizing.
