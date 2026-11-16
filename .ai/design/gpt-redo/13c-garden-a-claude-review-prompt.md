# Claude handoff — nghiệm thu 5 asset garden-a (Đơn 13c)

Bạn là reviewer art của Phimond. Hãy nghiệm thu **5 asset pending** trong `art/src/hd2d/garden-a/` sau khi Codex đã vẽ lại bằng built-in image_gen. Không sửa file, không tạo ảnh. Đây là review để phản hồi đạt/không đạt và ghi rõ vị trí/lý do.

## Phạm vi

Chỉ review: `gd-trunk-seg-01`, `gd-trunk-seg-02`, `gd-seal-strip`, `gd-seal-strip-lit`, `gd-pillar-vein-01`. 25 asset còn lại giữ nguyên. Bối cảnh HD-2D Octopath pixel art: 33–48 màu/asset, alpha nhị phân, outline cùng sắc vật thể, không blur/glow/fog/chữ vẽ sẵn.

## File cần đọc

- `art/src/hd2d/garden-a/contact-sheet.png`
- Mỗi asset: `final.png`, `qa.json`, `review.md`, `prompt.md`
- Ghép dọc: `gd-trunk-seg-01/preview-3x-vertical.png`, `gd-trunk-seg-02/preview-3x-vertical.png`
- Ghép ngang: `gd-seal-strip/preview-3x-horizontal.png`, `gd-seal-strip-lit/preview-3x-horizontal.png`
- Brief: `.ai/design/gpt-redo/13c-garden-a-redraw-prompt.md`
- Manifest: `art/src/hd2d/garden-a/manifest.json`

## Tiêu chí và số đo hiện tại

- **Trunk 01/02, 384×512:** 40–48 màu, binary alpha, dải đai rễ ở trên/dưới, ruột hai bản khác rõ. Hash hàng đầu/cuối và số pixel khác nhau nằm trong `qa.json`. Candidate 01 lệch 1 px giữa hàng đầu/cuối; candidate 02 lệch 94 px. Vì vậy đừng coi seamless chỉ dựa trên preview; xác nhận trực tiếp ghép 3 bản.
- **Seal unlit/lit, 512×160:** 40–48 màu, rune chạy giữa, không dây leo/lá, lặp ngang. Alpha profile cột trái/phải hiện bằng nhau trong từng file. Cặp mask hiện còn khác 514 pixel; RGB toàn ảnh khác 67,405 pixel. Profile alpha hai mép giống nhau, nhưng RGB mép trái/phải vẫn lệch lần lượt 102 px (unlit) và 81 px (lit), thấy vạch nối trong preview 3x. Xác định rune có phải vùng khác duy nhất không và tile có liền mạch thị giác không. Lit chỉ được đổi rune sang ngà; không glow.
- **Vein-01, 160×340:** cần 33–48 màu, phủ 5–8% mask pillar-01, 0 px ngoài mask, không halo/blur. Candidate hiện có 35 màu, 0 px ngoài mask, coverage 12.43% (quá dày so với brief); nhận xét xem hình ảnh có đủ bám theo đường xoắn pillar không.

## Cách phản hồi

Với từng asset, ghi `PASS` hoặc `REDO`, nêu lý do cụ thể và trỏ tới phép đo/ảnh. Với trunk, bắt buộc kiểm seam ghép ba lần; với seal pair, kiểm cả mask và pixel ngoài rune; với vein, kiểm 0 px ngoài mask, màu, coverage và độ bám silhouette. Cuối cùng ghi tổng số pass/redo và 3 asset yếu nhất. Không đánh dấu duyệt manifest nếu một tiêu chí cứng còn fail.
