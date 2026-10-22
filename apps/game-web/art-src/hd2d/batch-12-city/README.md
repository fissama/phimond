# batch-12-city — đồ thành phố (đơn 10, ChatGPT web)

Nguồn: ảnh owner nộp ở `_intake/don10-web-r1..r3/`. Cắt bằng:

```bash
python3 tools/p01/cut_city_batch12.py          # cắt lại toàn bộ, ghi manifest.json + contact-sheet.png
python3 tools/p01/cut_city_batch12.py --debug  # in vùng tìm được trên từng sheet (khi GPT đổi bố cục)
python3 tools/p01/sync_client_assets.py        # chép sang apps/client/public/hd2d (cờ provisional)
```

Tất cả `approved: false` → client dùng với cờ `provisional` tới khi owner duyệt trong game.

| Nhóm | Asset | Nguồn |
|---|---|---|
| Mặt tiền (tĩnh) | city-facade-inn/bakery/exchange/warehouse/belltower/corner | r1 sheet 2A/2B |
| Mảnh nối (tĩnh) | city-alley-arch, city-pillar-drainpipe, city-wall-flowerbox, city-iron-fence | r1 sheet 6 |
| Dải mái lớp giữa | city-roofline-mid (lặp ngang) | r1 sheet 7 |
| Đồ phố | city-hanging-sign*, city-bunting*, city-topiary*, city-sacks, city-vendor-cart | r1 sheet 3 (* lắc nhẹ) |
| Đồ phố động | city-lion-fountain (3 khung nước) | r3 lần 11 |
| Hoàng Môn | palace-guard-booth, palace-long-planter, palace-crenel-wall, palace-lion-r/l | r2 sheet 8 v2 |
| Hoàng Môn động | palace-flagpole (3 khung, chạy 1-2-3-2) | r3 lần 10 |
| Động vật | animal-pigeon-peck / -fly (2 khung), animal-cat (3 khung) | r3 lần 8–9 |
| Động vật (engine làm động) | animal-dog (thở), animal-butterflies (vỗ cánh/bay vòng), animal-crow (nhảy) | r1 sheet 5 |
| Decal | decal-cracks/drain/puddle/petals/hopscotch/ruts | r3 lần 1 |
| Người đi đường | walker-boy/girl/elder/baker/guard/traveller: final = đứng, run = 2 tư thế bước (quay phải, engine lật khi đi trái) | r3 lần 2–7 |

Ghi chú chất lượng (để owner quyết khi duyệt):
- Dáng đi: GPT vẽ hai tư thế bước giống nhau (cùng chân trước), nên chu kỳ là "đứng ↔ bước" kèm nhún. Đủ dùng ở cỡ 168 px; muốn mượt hơn thì nhờ vẽ thêm tư thế "chân kia trước".
- walker-baker: tư thế 3 đổi giỏ sang tay kia → chỉ dùng tư thế 2.
- Decal phấn/vệt bánh xe: đã khử ánh hồng do nền magenta, còn sót rất nhẹ ở viền.
