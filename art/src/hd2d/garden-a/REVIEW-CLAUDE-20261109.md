# garden-a — Claude review 2026-11-09

Kết quả: 25/30 duyệt (`approved:true`, status `approved_claude_20261109`), 5 chờ vẽ lại (Đơn 13c).
Đo trực tiếp từ final.png hiện hành; hash final/raw của 30 asset khớp manifest. `tools/check_hd2d_art.sh` không quét garden-a nên không có chứng nhận từ cổng này.

## Chờ vẽ lại (5)
| Asset | Lỗi |
|---|---|
| gd-trunk-seg-01 | Hàng đầu/cuối khác 356/384 px (hash ec5aee7d… vs ea2dffae…), alpha 284 vs 384 px, mép phải nhảy bậc ~140 px khi ghép 3 bản |
| gd-trunk-seg-02 | 259/384 px khác (hash ad7541a8… vs 2751fb44…), vạch nối ở zoom 2x, hốc cây lặp nhịp |
| gd-seal-strip, gd-seal-strip-lit | Lề dưới 0 px (136 hàng cuối đặc kín); qa.json ghi lề 15 px sai với file |
| gd-pillar-vein-01 | 1 màu (<33) |

## Duyệt kèm ghi chú (4)
- gd-wall-soil-02: S 0.805 > wall-01 0.756 (brief: ít bão hòa hơn)
- gd-wall-soil-03: sáng hơn wall-01 (luminance 99.9 vs 77.5) — engine tối dần theo màn
- gd-roots-hang-02/03: đầu gắn hẹp 14–21 px (brief: đầu trên to)

## Duyệt (21)
wall-soil-01, ledge-mid-01 (42 màu), ledge-mid-02, ledge-cap-l/r, trunk-join-01..03, pillar-01, pillar-02, pillar-vein-02 (0 px ngoài mask), lantern-unlit/lit (mask bằng nhau), roots-hang-01/04, decor-01..06.

## Hygiene cần agent sửa
- qa.json seal-strip: bbox y 15–145 (thật: 20–159); trunk-seg-02: lề [1,64,1,64] (thật: 23,0,57,0); roots-hang-01: attachment_top_row_opaque_pixels 0 (thật: 75).
- review.md còn dòng cũ mâu thuẫn: ledge-mid-01 "48 màu"/hash ad06affe…; seal-strip-lit "12618 màu"; trunk-seg-02 "exact True".


## Đơn 13c — redraw candidates (2026-11-09)

Codex đã tạo `raw-03.png` và thay `final.png` cho 5 asset, cập nhật manifest/contact sheet/3x previews. Tất cả vẫn `approved:false`, `needs_claude_review`. Đo mới nhất:

- trunk-seg-01: 46 màu, alpha nhị phân; hàng đầu/cuối còn lệch 1 px.
- trunk-seg-02: 46 màu, alpha nhị phân; hàng đầu/cuối còn lệch 94 px.
- seal-strip/lit: 46/45 màu, alpha profile cột trái/phải bằng nhau từng bản; cặp mask khác 514 px.
- pillar-vein-01: 35 màu, 0 px ngoài mask pillar-01; coverage 12.43% (brief 5–8%).

Đây là candidate để Claude kiểm tra, chưa được coi là hoàn tất/được duyệt. Handoff prompt: `.ai/design/gpt-redo/13c-garden-a-claude-review-prompt.md`.

## Vòng 2 (Đơn 13c) — 0/5 duyệt
| Asset | Kết quả | Số đo |
|---|---|---|
| gd-trunk-seg-01 | Chờ owner | 46 màu, alpha nhị phân; 8/8 cặp hàng dải (0–7 vs 504–511) bằng nhau trên pixel hiển thị; hash chặt lệch 1 pixel alpha=0 (x=313); preview ghép 3 bản liền, dải đai rễ đọc như vòng rễ |
| gd-trunk-seg-02 | REDO | 46 màu; 93 px hàng đầu/cuối khác (max 6); dải không phẳng (5 màu); silhouette dải 0–303 ≠ 01 (0–312); ghép 01/02 bậc ~30 px mép phải |
| gd-seal-strip | REDO | 46 màu, lề 15/16 đạt; mép trái/phải có dải tối ~3–5 px → vạch nối thấy rõ khi lặp |
| gd-seal-strip-lit | REDO | 45 màu; mask lệch unlit 514 px; 50.9k pixel đá khác nhẹ ngoài rune; cùng vạch mép |
| gd-pillar-vein-01 | REDO | 35 màu, 0 px ngoài mask đạt; phủ 12.43% (brief 5–8%); nét dày giống tia sét, không bám rễ |


## Đơn 13d — kết quả candidate (2026-11-09)

Owner đã chọn A: chuẩn hóa RGB ẩn dưới alpha=0 cho trunk-01; so sánh hiển thị bỏ qua RGB trong suốt. Owner cũng chấp thuận thay `gd-seal-strip-lit` bằng overlay `gd-seal-rune-glow`. Không commit.

- **gd-trunk-seg-01:** owner-approved theo rule RGB ẩn. Chỉ RGB của pixel alpha=0 được đặt về đen; pixel nhìn thấy giữ nguyên.
- **gd-trunk-seg-02:** REDO. Candidate raw-04 sau resize/palette có 806 sai khác ở 8 cặp hàng; x span đầu/cuối là 0–300/301, yêu cầu 0–312. Không promote.
- **gd-seal-strip:** candidate raw-04 được crop/resize/palette, 44 màu, alpha nhị phân, lề trên/dưới 22/18 px; profile alpha cột đầu/cuối trùng chính xác, chênh RGB trung bình 3.835. Preview 3× nhìn liên tục; cần Claude xác nhận hình ảnh.
- **gd-seal-rune-glow:** asset overlay mới, 13 màu, 13,013 pixel rune đã key, mask alpha hai mép trùng; output không chứa pixel ngoài vùng key. Cần Claude xác nhận pixel được key chỉ thuộc rune. `gd-seal-strip-lit` cũ được giữ lại và đánh dấu superseded.
- **gd-pillar-vein-01:** 33 màu; binary alpha; coverage 6.481%; 0 px ngoài mask pillar-01; Jaccard với vein-02 0.0356, Pearson 0.0357; mechanical checks pass, cần visual review.

**Tình trạng:** 1 asset được owner duyệt; 3 candidate cơ khí sẵn sàng nghiệm thu; trunk-02 chưa đạt và cần vẽ lại. Vì vậy vòng này chưa hoàn tất 100%. Candidate files, QA, 3× repeats, 4× views và contact sheet đã cập nhật.


Đính chính Đơn 13d trunk-02: đã thử thêm `raw-05.png`; vẫn không đạt. Sau resize/palette, 702 sai khác trong các cặp hàng biên; x-span đầu/cuối [[0, 296], [0, 295]]. Không promote.

## Vòng 3 (Đơn 13d) — 4/5 duyệt
| Asset | Kết quả | Số đo |
|---|---|---|
| gd-trunk-seg-01 | PASS | Hash chặt hàng 0 = hàng 511 (a352500687edeabc); 8/8 cặp hàng dải bằng nhau; dải một màu (79,21,19); x 0–312; 46 màu; 0 pixel alpha=0 còn RGB; ghép 3 bản liền |
| gd-trunk-seg-02 | REDO | final không đổi: 94 px hàng đầu/cuối khác; dải 5 màu; x 0–303; ghép xen 01-02-01 bậc mép phải |
| gd-seal-strip | PASS | 44 màu; lề 22/18; hết dải tối mép (lum 80.7 vs 76.7); ghép ngang liền, rune và gạch nối đúng |
| gd-seal-rune-glow | PASS\* | 13 màu; 0 px ngoài vùng đặc seal; 13 mảng nhỏ (166 px) lẻ ngoài rune |
| gd-pillar-vein-01 | PASS | 33 màu; phủ 6.48%; 0 px ngoài mask; tương quan mask 0.036 |
gd-seal-strip-lit đã bị thay bằng gd-seal-rune-glow, không dùng nữa.


## Quyết định cuối — đóng trunk-02 theo lựa chọn owner (2026-11-09)

Owner chọn phương án 1: chỉ dùng `gd-trunk-seg-01` làm biến thể thân. Không tiếp tục chỉnh sửa có mặt nạ vì image_gen hiện không hỗ trợ mask/inpaint. `gd-trunk-seg-02` đã được gỡ khỏi danh sách active trong manifest; toàn bộ thư mục và các candidate được giữ lại để audit, không được load.

**Trạng thái hiện hành: 29/29 asset active đã duyệt.** Manifest `approved=true`; trunk-02 không còn là blocker vì đã retire theo quyết định owner, không phải vì asset đã đạt tiêu chí seam.
