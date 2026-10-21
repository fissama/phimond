# Prompt BỐ CỤC MAP HD-2D bám map gốc (APK/JAR) — dán cho Gemini, 2026-10-17

Dùng sau khi kit asset của vùng đó đã đạt (hoặc song song nếu Gemini tự vẽ asset kèm). Mỗi phiên làm **một map**, nộp rồi chờ Claude kiểm.
Đính kèm mỗi phiên: ảnh gốc `map-images/<map_id>.png`, brief `.ai/design/map-briefs/<kit>/<map_id>.md` và `.json` (sinh bằng `tools/build-web-assets/gen_hd2d_map_briefs.py`), `manifest.json` của kit.

```text
Bạn đang dựng BỐ CỤC một map HD-2D (Octopath Traveler) cho Phimond, dựa trên map gốc của APK/JAR. Bạn KHÔNG vẽ lại ảnh phẳng của map. Bạn dùng asset rời trong manifest của kit, đặt chúng thành layout.json. Claude sẽ dựng cảnh trong engine từ layout.json của bạn.

1. BÁM MAP GỐC (bắt buộc)
- Xem ảnh gốc trước. Ghi lại (trong layout.json, trường "reading") bố cục của nó: đường chân trời / dải đi được (walkable band), lối đi chính, các cụm vật lớn (nhà, cây, cột, hồ, vách) và thứ tự từ trái sang phải, vùng cổng ở hai đầu, vị trí NPC.
- Bố cục mới phải giữ: (a) hình dạng dải đi được và các lối rẽ; (b) thứ tự và vị trí tương đối của các landmark lớn (±10% chiều rộng ảnh); (c) bầu không khí và màu chủ đạo của map gốc; (d) loại vật thể chủ đạo (nếu gốc có nhà tre, đặt nhà tre theo phong cách kit; đừng thay bằng thứ khác).
- Đổi: chất liệu và độ chi tiết sang phong cách Octopath của kit; thêm trang trí; chỉnh vị trí vật trang trí cho hợp lý. Không thêm hoặc bớt landmark lớn, không đổi hướng đi của map.

2. NEO CỐ ĐỊNH — KHÔNG ĐƯỢC LÀM MẤT HOẶC CHẶN
Trong brief có bảng "anchors" với tọa độ px (CHÂN vật, ảnh gốc, 100 px = 1 đơn vị APK) và vùng cấm đặt vật (keepout) cho:
- door / arrival / pillar: cổng dịch chuyển do owner đã vẽ và duyệt trên map P12. Đặt đúng cổng/portal asset của kit tại px đó (pivot giữa-đáy chạm đúng điểm), cổng hướng thẳng mặt trước. Mỗi cổng có ít nhất 2 ô trống phía trước (keepout) để người chơi bước tới.
- npc: giữ đúng px nếu có. NPC chưa có tọa độ ("CẦN ĐẶT") thì bạn đề xuất: đứng trên dải đi được, cách cổng ≥ 220 px, gần một landmark hợp vai (thợ gần lò, thương nhân gần lều…), không đè lên lối đi chính, không cùng hàng với NPC khác (lệch ≥ 180 px). Ghi lý do trong "why".
- arrival có cờ "CẦN ĐẶT": đặt điểm đến của trụ/cổng tới trên dải đi được, cách cổng đối ứng ~1 đơn vị (~100 px) và không đè vật.
- spawn / trans_enemy (map có quái): giữ vùng trống rộng quanh các điểm này (keepout), không đặt vật cản cao quá 90 px trong bán kính 160 px.
Nếu thấy một neo bắt buộc phải dời (vì đè địa hình gốc, ngoài dải đi được…), đánh dấu "moved": true kèm "reason". Claude sẽ duyệt. Mặc định không dời.
Chiều trục Y của brief là giả định (đỉnh ảnh = ymax). Nếu khi đối chiếu bằng mắt thấy cổng không nằm đúng chỗ trên ảnh gốc, báo lỗi ở "reading.notes" thay vì tự sửa.

3. THÊM SINH ĐỘNG (bắt buộc đủ ngân sách trong brief: decor_budget_min)
- Ba tầng chiều sâu: (back) sau dải đi được: cây/đá/phế tích lớn, nhóm trang trí; (mid) trên dải đi được: landmark + trang trí chừa lối; (front) tiền cảnh: bụi, đá nhỏ, cỏ, vật trang trí thấp (< 90 px) ở rìa dưới ảnh, không che nhân vật.
- Nhịp điệu: không xếp hàng ngang đều; nhóm 2–4 vật theo cụm (1 vật lớn + 2 nhỏ), xen khoảng trống; mật độ tập trung quanh landmark và rìa dải đi được, thưa ở giữa lối đi.
- Mỗi vật đứng (từ cỡ vừa trở lên) kèm 1 decal bóng tiếp đất ngay dưới chân (asset shadow cỡ phù hợp). Mỗi chỗ đổi vật liệu sàn dùng decal chuyển tiếp mép mềm (asset edge/decal vẽ tay) thay vì ghép hai tile cạnh thẳng.
- Dùng đúng các loại sàn chủ đạo: 1 tile chủ đạo phủ cả map; tile phụ chỉ là vệt/mảng có decal viền mềm.
- Ánh sáng/FX: chỉ đề xuất trong "fx" (hạt, tia sáng, sương) tên hạt có sẵn trong engine: dust, leaf, pollen, ember, snow, spore, firefly. Không nướng vào asset.
- Nếu thiếu loại asset cần để sinh động (ví dụ cầu thiếu khe, vật đặc thù của map gốc), ghi vào "asset_requests": id đề xuất, mô tả, kích thước, số lượng. Claude sẽ gộp vào đợt vẽ kế.

4. QUY TẮC VỊ TRÍ HỢP LÝ
- Mọi vật đứng có px là CHÂN. Chân phải nằm trong dải đi được hoặc sát rìa của nó, trừ vật back.
- Vật cao > 190 px không được đặt trong vùng cấm hay trong lối đi chính (dải đi được ±60 px ở giữa).
- Nước, khe, vực: dùng asset khe/vực của kit; cầu phải bắc qua khe với hai mố ở hai bờ; không để cầu nằm trên nền liền.
- Tỉ lệ: nhân vật cao ~168 px (128 px/đơn vị). Cổng cao hơn nhân vật ít nhất 1.5 lần. Prop không vượt cỡ world của manifest quá 1.3×, không nhỏ hơn 0.7×.
- Không lật gương một asset khác cho "tạo biến thể"; dùng biến thể thật (đánh số -01/-02).
- Không dùng asset ngoài manifest kit (hoặc asset chung đã nghiệm thu mà brief chỉ rõ).

5. ĐỊNH DẠNG NỘP — một file layout.json cho map
{
 "map_id": "...", "kit": "...", "version": 1,
 "reading": { "walk_bands": [[x0,y0,x1,y1],...], "landmarks": [{"what":"...","px":[x,y]}], "notes": "..." },
 "anchors": [ {"id":"P:...","px":[x,y]}, {"id":"npc_id","px":[x,y],"why":"..."}, {"id":"...","px":[x,y],"moved":true,"reason":"..."} ],
 "floor": { "base": "tile-id", "patches": [ {"asset":"decal-id","px":[x,y],"scale":1.0} ] },
 "placements": [ {"asset":"asset-id","px":[x,y],"layer":"back|mid|front","scale":1.0,"sway":false,"why":"ngắn"} ],
 "backdrop": [ {"asset":"backdrop-id","layer":"far|mid|near"} ],
 "fx": [ {"type":"dust","where":"toàn map|px:[x0,y0,x1,y1]"} ],
 "asset_requests": [ {"id":"...","desc":"...","size_px":[w,h],"qty":1} ]
}
Tọa độ px là của ảnh gốc (chân vật). Claude đổi sang world của engine.

6. TỰ KIỂM TRƯỚC KHI NỘP (bắt buộc)
- Chạy `python3 tools/build-web-assets/validate_hd2d_map_layout.py layout.json` và sửa tới 0 lỗi. Báo kết quả.
- Tự dựng một ảnh phác phẳng (preview.png, chỉ để xem, không dùng làm asset) và đối chiếu với ảnh gốc: cổng đúng chỗ, NPC trên dải đi được, bố cục giữ thứ tự landmark.
- Nếu Claude chạy scene trong engine: mỗi vòng nộp thêm ảnh render 3 camera và ảnh zoom 2× vùng cổng và NPC. Bạn phải tự nhìn ảnh trước khi nói "đạt".

7. LỖI ĐÃ BỊ TRẢ LẠI (đừng lặp)
Decal hình chữ nhật cạnh cứng; vật xếp thành hàng ngang đều; sàn ghép mảng khác màu; cồn cát/boulder lệch màu so với sàn; cầu đặt lên nền liền không có khe; backdrop có vạch nối; báo "0 lỗi" nhưng ảnh render vẫn lỗi.
```

## Quy trình đề xuất
1. Chạy `python3 tools/build-web-assets/gen_hd2d_map_briefs.py` (đã chạy: 58 map, 173 neo, 57 neo "cần đặt"; 17 map của đấu trường/bang hội/Maya/địa lao/Sói–Cừu chưa có bounds trong portal package nên chưa có brief).
2. Gửi Gemini một map một lần với prompt này và brief; nhận `layout.json` + `preview.png`.
3. Claude chạy `validate_hd2d_map_layout.py`, dựng scene, duyệt bằng ảnh.
4. Sau khi layout duyệt, Claude viết bộ dựng scene (layout.json → scene JSON) một lần cho cả kit.
