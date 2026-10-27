# Phimond: khóa art và dùng Sprite Forge cho sprite 2D

Ngày: 2026-10-23. Scope: artwork, prompt, metadata và QA. Không sửa game code.

## Chỉ đạo đã chốt với owner

Vẽ asset 2D và từng tư thế chuyển động thành PNG. Không tạo video. Khung nhân vật192×192, dải8khung1536×192, pivot96,184, alpha nhị phân, ≤64màu; đồng bộ trang phục và kích thước với idle đã có. Không dùng video/rig/interpolation để thay cho tư thế được vẽ. Code chỉ làm việc cắt, key nền, palette, căn khung và kiểm tra.

Các mẫu ảnh đã xem lại: snapshot22/10 của cả5map trong `apps/game-web/art-src/hd2d/p01-release-art-20261022/before/`, city kit đã duyệt trong `.ai/design/gpt-redo/refs-v1.0.1-city/approved-city-kit.png`, các idle đang dùng trong `apps/client/public/hd2d/`. Snapshot là tài liệu tham chiếu art, không phải xác nhận bố cục runtime mới nhất.

## Ngôn ngữ hình ảnh cần giữ

- Sprite dựng đứng trên mặt sàn nhìn chéo. Nhân vật/đạo cụ tách PNG; chiều sâu đến từ lớp cảnh, che khuất và ánh sáng trong game.
- Người: nét pixel rõ, tỷ lệ đầu/thân và trang phục bám idle hiện có. Nam tóc xanh/navy-gold/redlining; nữ tóc đỏ cam, corset nâu, tay áo ngà, áo/váy gỉ đỏ. Không đổi nhân vật khi đổi hướng.
- Rừng: olive/vàng lá, bóng xanh lục lạnh, vỏ cây nâu già; không xanh neon. Bụi thấp phải nhường tầm nhìn đường đi và lối ra.
- Thành phố: đá ngà/ochre, mái đất nung, kim loại vàng cũ, gỗ nâu; hậu cảnh bớt tương phản. Mảnh nối phải tiếp tục vật liệu, tỷ lệ viên đá và gờ của facade hiện có.
- UI: vàng cũ, ngà và xanh navy; nhãn tách khỏi thanh, tâm khung rỗng, không còn viền ma-gen-ta.
- Vật đang cầm là một phần identity: baker có giỏ, girl có táo, elder có gậy, guard có giáo, traveller có ba lô/cuộn chăn/bình/gậy. Kiểm từng khung, không chỉ khuôn mặt.
- Boy/girl phải giữ tầm vóc idle128/124px trong cùng cell192; kéo tất cả lên168 sẽ làm nhân vật phóng to khi bắt đầu đi. Hero168px; baker164px, elder158px theo master đang chạy.

Chuẩn chi tiết: `.ai/design/gpt-redo/00-master-v2.md`. Batch00–09 là nguồn style, không lấy các batch bị trả làm chuẩn.

## Phần Sprite Forge đã nghiên cứu và dùng thật

Repo: https://github.com/0x0funky/agent-sprite-forge, commit `5324342fdfab72430f4e9604f3fe427009f8596d`, v0.4.0. Bản clone nghiên cứu ở `/tmp/phimond-agent-sprite-forge-research`. Các script đã cài trong4skill generate2dmap/generate2dsprite/video2dsprite/generate2dmedia khớp bản clone; không cài lại global.

Chỉ dùng phần áp dụng cho PNG: guide tư thế, `sheet_qc.py frames`, `scale_frames.py`, matte/palette và reviewer. Quy trình riêng Phimond:

1. Khóa reference idle, trang phục và vật cầm. Chốt chu kỳ hai chân trước khi nhân rộng.
2. Vẽ tư thế bằng built-in image_gen. Khi sinh cả sheet lặp chân, sửa từng keypose từ cùng một mẫu, không sao chép/lật nửa chu kỳ.
3. Cắt theo lưới thực của ảnh trả về; không giả định model tuân thủ số hàng. Chỉ bỏ gutter đã xác nhận trống, không cắt vào chân/giáo/tóc.
4. Một scale chung cho cả action; palette chung; alpha nhị phân. Không co giãn từng người để che lỗi hình học.
5. `scale_frames.py --scale-from 1 --resampler nearest --root-lock torso-x --canvas 192,192 --anchor-px 96,184`: dịch pixel nguyên, không tạo tư thế. Giữ hồ sơ trước/sau và kiểm không cắt mép.
6. `sheet_qc.py frames --cycle walk` cho dải ngang; không áp suy luận near/far theo chiều ngang vào dải xuống/lên. Đọc head-scale, drift, seam và half-cycle; không chỉ kiểm hash khung trùng.
7. Xem PNG, GIF phóng4× và so idle ở kích thước game. Các số không chứng minh anatomy, trang phục hay bước chân đúng. Claude duyệt cuối cùng.

## Kết quả và giới hạn phải giữ khi bàn giao

- Audit cũ ở `p01-release-art-20261023/forge-audit/`: 23dải,21warn và2fail trong snapshot ban đầu; xem JSON cụ thể thay vì suy kết quả từ exitcode. Số lượng trạng thái được cập nhật ở các summary mới, không dùng snapshot cũ để duyệt phiên bản mới.
- Các lần căn mới lưu riêng theo SHA trong `forge-registration-v2/`. Cảnh báo và đường dẫn report được chép vào `.qa.json` từng ảnh; không đổi ngưỡng để làm đẹp báo cáo.
- Auto near/far suy từ độ sáng chân có thể không nhận diện được giày cùng màu hoặc bị áo che. `needs-visual-review` không phải pass chuyển động.
- Canonical `art_gate.py` hiện quét batch toàn repo và lỗi `KeyError: file` khi gặp manifest override cũ. Không sửa gate/waiver. Dùng nguyên `tools/hd2d_audit/audit.py` trên manifest lô này ở root cách ly:110asset,0issue về file/size/margin/palette/alpha/density/seam. Đây không thay thế gate toàn repo hoặc duyệt chuyển động.
- Chưa công bố v1.0.1 đạt release; chưa nạp các bản chưa duyệt. Giữ kết quả duyệt Claude trong checklist, tách khỏi trạng thái cơ học.

Sổ ảnh riêng kèm prompt: `apps/game-web/art-src/hd2d/p01-release-art-20261023/DELIVERY-BOOK.md`.
