# REDRAW-world_tree-edge-01

Prompt from ROADMAP-ART-TASKS-20261109.csv:

Vẽ asset HD-2D Octopath-Traveler pixel art `world_tree-edge-01` (edge) cho kit world_tree. Nội dung: dải chuyển rêu → vỏ cây 512×128/40 màu, alpha đục; art-gate seam X=10.586/limit 14. Repeat 3× không lộ mối nối lớn nhưng nhịp vỏ cây lặp và màu tối; c. Palette/style kit: Cành cây khổng lồ làm lối đi, lá to bằng mái nhà, quả thần phát sáng; xanh lục sáng + vàng kim. Kỹ thuật: 512×128 seamless hai đầu (mép trái/phải khớp), mép trên bất quy tắc, binary alpha. Pivot: pivot giữa-đáy, dải đặt giữa hai tile. 33–48 màu, outline tối cùng sắc, ánh sáng trên-trái, không baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID. Lỗi của bản cũ KHÔNG được lặp lại: Lộ đường cắt tại mốc 512 trong 3×1 thật (wx 3.5/4.1). Giữ chủng loại vật thể và bảng màu nhận diện của ảnh gốc map (đính kèm), diễn giải HD-2D, không sao chép pixel từ ảnh. Xuất 1 PNG final nền trong suốt (trừ floor/backdrop opaque) đúng kích thước.

Errors to avoid:

Lộ đường cắt tại mốc 512 trong 3×1 thật (wx 3.5/4.1); baked shadow/glow/text/magenta, lật gương hoặc đổi màu từ biến thể khác, decal chữ nhật, viền trắng (fringe), nền phẳng <28 màu, lưới/khe chữ thập giữa ô, cụm lặp đều theo ô, trùng họa tiết giữa các ID

References: .ai/design/map-checklists/refs/world_tree_gate.jpg; .ai/design/map-checklists/refs/world_tree_deep_woods.jpg; .ai/design/map-checklists/refs/world_tree_secret_chamber.jpg
Style anchors: art/src/hd2d/batch-01-octopath/edge-grass-dirt/final.png; art/src/hd2d/batch-02-octopath/city-garden-border/final.png; bản cũ lỗi (KHÔNG bắt chước): art/src/hd2d/batch-11-world_tree/world_tree-edge-01/final.png

Raw source copied byte-for-byte. SHA256: `e060d084bdebb22f5025bc5391d2286bd8801765f6209cc7600e43d6be30fed4`. Route: Codex built-in image_gen. Candidate is unregistered and awaits Claude review.
