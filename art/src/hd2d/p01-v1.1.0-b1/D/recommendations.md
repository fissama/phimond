# Đơn 11 — Nhóm D: rà soát phần còn thiếu (đề xuất chờ Claude duyệt)

Đã xem ảnh gốc `~/Downloads/Phimond-P12-Review/map-images/city_market.png`, `city_activity_hall.png`, `city_pet_room.png`; đối chiếu asset trong `batch-02-octopath` và `batch-12-city`.

- **Thương Phố:** kit hiện có `awning-red/green/blue`, `market-produce`, `market-cloth`, `market-weapons`, `city-vendor-cart`, facade cửa hàng/inn/exchange/warehouse, `city-hanging-sign`, `city-alley-arch`, roofline, pavers và props môi trường. Ảnh map được các nhóm này bao phủ; chưa thấy prop/tile bắt buộc nào thiếu rõ ràng.
- **Vạn Sự Hội Sảnh:** `hall-wall-stone`, `hall-wall-timber`, `palace-column`, `hall-floor-stone/wood`, `hall-counter`, `hall-bookshelf`, `hall-quest-board`, exit open/closed, torch/candle hiện có thể dựng các bề mặt và đồ nội thất nhìn thấy trong ảnh. Chưa thấy thiếu asset bắt buộc.
- **Phòng thú cưng:** `pet-nest-shelter`, `pet-nest-straw`, `pet-nest-blanket`, `barrel`, `farm-trough`, `hall-floor-wood` hiện có thể dựng chuồng, ổ, thùng và sàn. Ảnh map còn có các chén nhỏ đặt trước ổ; kit chưa có chén riêng. Claude đã duyệt bổ sung prop này. Đã vẽ 2 biến thể riêng `pet-feed-bowl-food` và `pet-feed-bowl-water` trong thư mục D, mỗi file 64×64, palette 37–38 màu, alpha nhị phân, lề 8 px, không bóng đổ. Trạng thái vẫn `approved=false`, `needs_claude_review`.

Đã hoàn tất phần chén theo phê duyệt của Claude; các thiếu hụt khác không đổi so với rà soát trước.
