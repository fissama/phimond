# REDRAW-world_tree-floor-extra-05

Prompt from ROADMAP-ART-TASKS-20261109.csv:

Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree-floor-extra-05` (floor) cho kit world_tree. Nội dung: rêu emerald sáng với phấn vàng thưa, 512×512/40 màu; nearest + no-dither finish; seam X=9.315/Y=10.120; corr cao nhất 0.861 với floor-03. Mosaic có ca. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 512×512 seamless, opaque, viền ngoài phẳng 8 px, texture riêng mỗi biến thể (tương quan chéo <0.9), nhìn từ trên xuống; 128 px = 1 đơn vị (tile 4×4 đv). Pivot: không có pivot (tile). 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: wrap x/y 2.5/3.6 cao, nghi seam; wrap x/y 2.512/3.596 >2.0. Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.

Errors to avoid:

wrap x/y 2.5/3.6 cao, nghi seam; wrap x/y 2.512/3.596 >2.0; baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID

References: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
Style anchors: art/src/hd2d/batch-01-octopath/dirt-floor-01/final.png; art/src/hd2d/batch-01-octopath/dirt-floor-02/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/batch-11-world_tree/world_tree-floor-extra-05/final.png

Raw source copied byte-for-byte. SHA256: `1ae9771f93e79e35ecd63d2d24c11f89584793203148e21685dc2ec749d0eac4`. Route: Codex built-in image_gen. Candidate is unregistered and awaits Claude review.
