# P12 Stage 4 — Thiết kế chi tiết, phạm vi 17 map (bản nháp 2026-10-15)

Quyền: owner mở Stage 4 ngày 2026-10-15, **chỉ tài liệu/dữ liệu thiết kế**; không sửa runtime, game client hay nguồn. P12 vẫn OPEN. Tên map = tên owner ([names master](../P12-world-names-master.md)).

## 1. Phạm vi (17 map)

| ID code | Tên owner | Nhóm |
|---|---|---|
| `summoning_hall_main_hall` | Triệu Linh Điện | Khởi đầu |
| `emerald_forest_main_woods` / `emerald_forest_deep_woods` | Bìa Rừng Lục Bảo / Rừng Sâu Lục Bảo | Emerald |
| `city_square` | Quảng Trường Thạch Trụ | Thành |
| `city_market` | Thương Phố | Thành |
| `city_palace_gate` | Hoàng Môn | Thành |
| `city_royal_palace` | Vương Cung | Thành |
| `city_activity_hall` | Vạn Sự Hội Sảnh | Thành |
| `city_pet_room` (**CanPhong**) | Phòng thú cưng | Thành |
| `city_farm` | Điền Trang Lục Dã | Thành |
| `city_deathmatch_arena` | Huyết Chiến Đài | Thành |
| `treasure_beach_{fishermen,east,west}_beach`, `_deep_sea`, `_prosperity_island` | Bến Ngư Châu, Bờ Đông Ngọc Bích, Bờ Tây Hoàng Sa, Vực Hải Lam, Đảo Phú Quý | Bãi biển |
| `middle_corridor_main_hall` | Hải Tặc Hào | Trụ Lv40+ |

## 2. Ma trận portal (đã sinh)

- Dữ liệu: [portal-matrix.json](portal-matrix.json), bảng đọc được: [P12-S4-portal-matrix.md](P12-S4-portal-matrix.md). Sinh lại bằng `gen_portal_matrix.py` (chỉ đọc `~/Downloads/Phimond-P12-Review`). 45 portal APK chạm phạm vi.
- Nguồn là cấu hình APK (3.2 và 8.4 trùng 157/157 portal); **runtime chưa kiểm chứng** (R-S2-1…5 vẫn áp dụng).

### Đồ thị cửa APK (nội bộ phạm vi)
```
Triệu Linh Điện ──► Bìa Rừng Lục Bảo ◄──► Rừng Sâu Lục Bảo ──► Hoàng Môn      (một chiều ra thành)
Quảng Trường ◄──► Hoàng Môn ◄──► Thương Phố ◄──► Quảng Trường
Hoàng Môn ◄──► Vương Cung ◄──► Vạn Sự Hội Sảnh
Điền Trang ◄──► Phòng thú cưng ;  Điền Trang ──► Quảng Trường (một chiều)
Bến Ngư Châu ◄──► Bờ Đông / Bờ Tây / Vực Hải ;  Bờ Tây ◄──► Đảo Phú Quý ;  Bờ Đông ──► Quảng Trường (một chiều)
Huyết Chiến Đài ──► Quảng Trường (một chiều)
Hải Tặc Hào: 0 cửa ra; 6 vùng cao có cửa về Hải Tặc Hào
```

### Phát hiện (khớp mô hình trụ teleport đã chốt)
1. **Quảng Trường không có cửa tới Điền Trang, Huyết Chiến Đài, Bãi biển, Emerald**, nhưng 16 map khác có cửa *về* Quảng Trường → vào bằng trụ, ra bằng cửa.
2. **Điền Trang chỉ có cửa vào từ Phòng thú cưng** và Huyết Chiến Đài không có cửa vào → hai nơi này vào bằng trụ/hàng đợi.
3. **Hải Tặc Hào không có cửa ra** → trụ trên tàu là lối ra duy nhất (đã chốt U5).
4. **Rừng Sâu Lục Bảo → Hoàng Môn** theo APK. **Owner chốt 2026-10-15 (Q1):** Hoàng Môn chỉ dùng cho lần đầu, theo yêu cầu nhiệm vụ; các lần sau lối ra này đưa về Quảng Trường Thạch Trụ.
5. **Bờ Đông Ngọc Bích** (bãi quái) có cửa về Quảng Trường và cửa tới Bến Ngư Châu. **Owner chốt (Q2):** trụ đưa người chơi tới Bờ Đông, từ đó đi tiếp vào Bến Ngư Châu.

## 3. Ma trận trụ teleport (quyết định owner)

| Trụ | Đích | Điều kiện |
|---|---|---|
| Quảng Trường Thạch Trụ (U1: bệ phép xanh ngọc, dưới-phải) | Vùng sơ cấp Lv1–40 (bảng §4), Điền Trang, Hải Tặc Hào | Menu chỉ hiện vùng đủ cấp / bậc đấu trường (runtime đã có menu) |
| Hải Tặc Hào | 6 vùng cao Lv40+, Điền Trang, Quảng Trường | — |
| Triệu Linh Điện (khóa) | Bìa Rừng Lục Bảo, **một chiều**, không quay lại | Mở sau khi nhận pet + nhiệm vụ đầu (U8) |

Điểm đến của trụ với Bãi biển là **Bờ Đông Ngọc Bích**. Quy tắc chung: điểm xuất hiện cách cửa đối ứng ≈1 đơn vị + guard chống kích hoạt lại cửa; không chặn cấp ở Emerald (U4).

## 4. Phân cấp vùng và spawn

### 4.1 Nguồn cấp (bằng chứng APK)
Tên thư mục scene trong APK 3.2 ghi dải cấp từng vùng: `Map/1-10/RungBiBo`, `10-15/BaiBienKhoBau`, `15-20/SaMac`, `20-25/MomDaGio`, `25-30/DaoAcMong`, `30-35/LangMo`, `35-40/GiaoDiem`. Sáu vùng cao (Tinh Không, Di Tích Cổ, Lâu Đài Ma, Cây Thế Giới, Tháp Chim, Mê Thành) không có dải trong đường dẫn; owner đã chốt là Lv40+.

### 4.2 Cấp từng map (**owner duyệt 2026-10-15**)
Chia đều trong dải của vùng; map hub an toàn không có quái. Số cấp quái cuối cùng thuộc P15, đây là cấp vào vùng + dải quái dự kiến để làm menu trụ.

| Map | Vai trò | Cấp quái đề xuất | Cấp tối thiểu hiện trên menu trụ |
|---|---|---|---|
| Bìa Rừng Lục Bảo | map khởi đầu: NPC và quái trộn lẫn, **không có vùng an toàn** (owner 2026-10-15) | 1–5 | 1 |
| Rừng Sâu Lục Bảo | bãi quái (6 điểm spawn) | 5–10 | 1 (không chặn, U4) |
| Bờ Đông Ngọc Bích | bãi quái, cửa vào của vùng (15 điểm) | 10–12 | 10 |
| Bến Ngư Châu | hub an toàn (Shop, Skill, 2 NPC) | — | 10 |
| Bờ Tây Hoàng Sa | bãi quái (10 điểm) | 12–13 | 10 |
| Vực Hải Lam | bãi quái (10 điểm) | 13–14 | 10 |
| Đảo Phú Quý | bãi quái sâu nhất (10 điểm) | 14–15 | 10 |
| Sa Mạc / Mỏm Đá Gió / Đảo Ác Mộng / Lăng Mộ / Giao Điểm | ngoài 17 map, theo dải APK | 15–20 / 20–25 / 25–30 / 30–35 / 35–40 | 15 / 20 / 25 / 30 / 35 |
| 6 vùng cao qua Hải Tặc Hào | ngoài 17 map | Lv40+ (chia bậc ở Stage 4 sau) | 40 |

Lưu ý: map mới hiện trong menu khi đủ cấp tối thiểu, nhưng không chặn người chơi cấp thấp đi vào bằng đường khác (quy tắc U4).

### 4.3 Điểm spawn đọc từ APK
Dữ liệu: [apk-extract/spawn-markers.json](apk-extract/spawn-markers.json). Mỗi map quái có 1 trigger `TransEnemy` và các điểm đánh số (marker): Bìa Rừng 0, Rừng Sâu 6, Bờ Đông 15, Vực Hải Lam 10, Bờ Tây 10, Đảo Phú Quý 10; Bến Ngư Châu, thành và Hải Tặc Hào không có. **Danh tính, số lượng, cấp quái không đọc được** (container `AllEnemy` rỗng; tham số nằm trong script IL2CPP không có type tree). Danh tính quái phải lấy từ thiết kế Phimond (P10/P11 + P15), không từ APK.

## 5. Các ma trận còn lại

| Ma trận | Trạng thái | Ghi chú |
|---|---|---|
| Portal | **Xong (nháp)** | [P12-S4-portal-matrix.md](P12-S4-portal-matrix.md) |
| Trụ / access | **Xong (nháp)** | §3, §4.2 |
| NPC / dịch vụ | **Roster đề xuất đủ (chờ duyệt)** | [P12-S4-npc-roster.md](P12-S4-npc-roster.md): 52 NPC + 1 hòm thư (40 gắn vị trí gốc, 12 mới + hòm thư) phủ chính tuyến, tự do, hồi máu, học kỹ năng, cửa hàng, dịch vụ pet. Bảng nguồn thô: [P12-S4-npc-matrix.md](P12-S4-npc-matrix.md) (44 slot APK; vai trò gốc chỉ là suy đoán) |
| Spawn / vùng quái | **Có điểm spawn, thiếu danh tính** | §4.3; danh tính quái do P15/P10/P11 quyết |
| Recovery / safe arrival | **Quy tắc đã chốt (§7)** | Chết/kẹt → vùng an toàn của map lớn hiện tại |
| Template / instance / ownership | **Một phần** | **Điền Trang Lục Dã và Phòng thú cưng: map riêng từng người chơi** (owner 2026-10-15). Huyết Chiến Đài và phòng Sói–Cừu cần instance; chưa có bằng chứng APK |

Cách tái tạo dữ liệu APK: `apk-extract/01_dump_scenes.py`, `02_extract_npcs.py` (cần `UnityPy==1.25.3`, đọc `~/Downloads/Spirit Beast World 3.2.apk` và thư mục `Phimond-P12-Review`; chỉ đọc; chỉnh `~` cho khớp máy).

## 6. Câu hỏi còn mở cho owner
- Không còn câu hỏi mở về vùng an toàn.

## Đã chốt 2026-10-15
- Q1: Rừng Sâu → Hoàng Môn chỉ lần đầu theo nhiệm vụ; sau đó về Quảng Trường.
- Q2: trụ tới Bờ Đông Ngọc Bích (bãi quái), rồi có lối vào Bến Ngư Châu.
- Q4: owner cho đọc APK 3.2 (chỉ đọc); đã trích NPC và spawn.
- Q3: owner duyệt bảng cấp vùng §4.2.
- Q5: roster đủ chính tuyến, tự do, hồi máu, học kỹ năng, dịch vụ (§5). Kỹ năng: một thầy chung mỗi điểm dạy, không chia theo race. Nông trại ngoài chỉ có 1 NPC gửi/rút pet; giám định, cường hóa, lai tạo, ấp ở Phòng thú cưng.
- Q8: Bìa Rừng giữ như cũ (map khởi đầu, NPC và quái trộn, không có vùng an toàn). Các map quái phía sau vẫn có NPC làm nhiệm vụ.
- Q6: giữ 6 NPC ở Hải Tặc Hào.
- Q7: chết/kẹt → vùng an toàn của map lớn; mỗi map lớn có 1 map nhỏ là vùng an toàn, ngoại lệ Emerald (§7).

## 7. Vùng an toàn và hồi sinh

### 7.1 Quy tắc (owner 2026-10-15)
Mỗi map lớn (vùng) có **đúng 1 map nhỏ là vùng an toàn**, **trừ Emerald** (map khởi đầu): không quái hoang, có NPC hồi máu, thường có cửa hàng và học kỹ năng. Khi chết hoặc kẹt, người chơi hồi sinh/được đưa về vùng an toàn của map lớn hiện tại. Phạt chết, chi phí, cooldown thuộc phase khác (P15/P09), không quyết ở đây.

### 7.2 Vùng an toàn theo map lớn (đã đối chiếu APK 3.2)
Cách xác định: quét mọi map trong APK ([apk-extract/map-scan.json](apk-extract/map-scan.json), script `03_scan_all_maps.py`). Map có trigger `TransEnemy` hoặc điểm spawn đánh số là map có quái; map không có cả hai mà có NPC là hub an toàn. Mẫu hình nhất quán: map đầu tiên của mỗi vùng là hub (0 quái, 2–4 NPC, 3–4 cửa), trừ Emerald và Đảo Ác Mộng.

| Map lớn | Vùng an toàn | Quái / NPC trong APK | Kết luận |
|---|---|---|---|
| Thành phố (8 map) | Quảng Trường Thạch Trụ | cả 8 map: 0 quái | Khớp; cả thành là an toàn |
| **Emerald** | **Không có** (map khởi đầu, NPC và quái trộn). Chết/kẹt → Bìa Rừng | Bìa Rừng: có trigger quái + 4 NPC | APK khớp ý owner |
| Bãi biển | Bến Ngư Châu | 0 quái, 4 NPC | Khớp |
| Hải Tặc Hào | chính nó | 0 quái, 6 NPC | Khớp |
| Triệu Linh Điện | chính nó (dùng một lần) | 0 quái | Khớp |
| Sa mạc | **Sa Thạch Cổ Thành** (`desert_shicheng_ruins`) | 0 quái, 4 NPC, 3 cửa | **Sửa đề xuất cũ.** Bộ Lạc Hồ Lô và Cửa Ngõ Hoàng Mạc đều có quái |
| Mỏm Đá Gió | **Trại Phong Thạch** (`windrock_mountain_camp`) | 0 quái, 4 NPC | Xác nhận |
| Đảo Ác Mộng | **Không có** (giống Emerald). Trại Tàn Sinh (`nightmare_island_survivor_camp`) giữ trộn lẫn NPC và quái; chết/kẹt → Trại Tàn Sinh | Trại Tàn Sinh: có quái (5 điểm) + 3 NPC; 5 map còn lại đều có quái | **Owner chốt 2026-10-15** |
| Lăng Mộ | **Trạm Canh Lăng** (`tomb_region_camp`) | 0 quái, 4 NPC | Xác nhận |
| Giao Điểm | **Cổng Địa Đạo Lam Dạ** (`crossroads_unnamed_area_01`) | 0 quái, 2 NPC, 3 cửa | Xác nhận (trước là đoán) |
| Tinh Không | **Tử Vân Lâm** (`astral_realm_unnamed_area_01`) | 0 quái, 2 NPC, 4 cửa | **Sửa.** Cửa lên tàu ở Thời Không Liệt Khích (0 quái, 0 NPC, chỉ là điểm chuyển tiếp) |
| Di Tích Cổ | **Tiền Sảnh Ngọc Lục** (`ancient_ruins_unnamed_area_01`) | 0 quái, 2 NPC | Xác nhận |
| Lâu Đài Ma | **Cổng U Lâu** (`ghost_castle_gate`) | 0 quái, 2 NPC | Xác nhận |
| Cây Thế Giới | **Thế Thụ Môn** (`world_tree_gate`) | 0 quái, 2 NPC | Xác nhận |
| Tháp Chim | **Điểu Tháp** (`tower_region_main_tower`) | 0 quái, 2 NPC | Xác nhận |
| Mê Thành | **Mê Thành Bất Tử** (`immortal_maze_main_maze`) | 0 quái, 2 NPC | Xác nhận |
| Bang hội | Thành Lũy Bang Hội (cả 6 map: 0 quái) | — | Khớp |
| Sói–Cừu | Sảnh Chờ Sói–Cừu (0 quái, 0 NPC) | — | Dùng sảnh chờ |
| Maya, Ngục ngầm | Không có (một tầng, có trigger quái) | — | Về Quảng Trường |
| Đấu trường PK/đội, chiến trường bang | Không có trigger quái (đấu người) | — | Về Quảng Trường hoặc sảnh hoạt động |

Giới hạn: tên `TransEnemy` và điểm spawn đánh số là suy luận từ tên object; script IL2CPP không đọc được tham số. Kết luận "0 quái" nghĩa là APK không có trigger/điểm spawn trong map đó, chưa kiểm chứng bằng chạy game. Các vùng ngoài phạm vi 17 map vẫn cần thêm NPC hồi máu khi thiết kế (hub APK có 2–4 NPC, chưa biết vai trò).

### 7.3 Hệ quả cho phạm vi 17 map
- Trụ teleport vẫn đưa người chơi vào bãi quái (Bờ Đông); Rinka có trại nghỉ để hồi máu ngay, nhưng điểm hồi sinh khi chết là Bến Ngư Châu.
- Map quái ở các vùng khác vẫn có NPC làm nhiệm vụ (roster đã có).
- Chết ở Rừng Sâu → Bìa Rừng (đề xuất, Q12).
- Cổng Hoàng Môn, Vương Cung, Thương Phố... thuộc Thành phố nên chết ở đó (nếu có) → Quảng Trường.
- Q12: chết/kẹt ở Emerald → hồi sinh ở Bìa Rừng.
- Q13: ấp trứng ở lại Phòng thú cưng. Nông trại và Phòng thú cưng là map riêng của từng người chơi (không dùng chung).
- Q14: bậc kỹ năng từng thầy do P13 quyết.
- Chuỗi nhiệm vụ chính do phase quest quyết; P12 chỉ soạn NPC.
- Đảo Ác Mộng: giữ Trại Tàn Sinh trộn lẫn như Bìa Rừng, không có vùng an toàn; chết/kẹt → Trại Tàn Sinh. Vùng an toàn của các vùng ngoài phạm vi đã đối chiếu APK (§7.2).

## 8. Quy tắc NPC theo loại map (owner, web review 2026-10-15)

- NPC hồi máu và cửa hàng chỉ ở map an toàn. Map có bãi quái chỉ có NPC nhiệm vụ phụ (hạng tự do). Ngoại lệ: 2 map hỗn hợp (Bìa Rừng Lục Bảo, Đảo Ác Mộng).
- Triệu Linh Điện chính là Sảnh vẫy gọi (`SanhVayGoi`, luồng người chơi mới). Owner đã xác nhận và yêu cầu hoàn lại vai trò ban đầu của Mira: NPC chính tuyến, hướng dẫn chọn bệ và nhận pet 1★ (đảo lại nhận xét trước đó cho map này là map sự kiện).
- Quảng Trường thêm: Chủ Sàn Giao Dịch Ketra, Thủ Kho Odan (kho đồ) và Hòm Thư Thạch Trụ (vật thể cạnh Thủ Kho).
- Hải Tặc Hào thêm Thợ Rèn Tàu Harlo.
- Hệ quả cần lưu ý: Rừng Sâu, Bờ Đông, Bờ Tây, Vực Hải Lam, Đảo Phú Quý không còn hồi máu tại chỗ; người chơi về Bến Ngư Châu hoặc hồi sinh theo §7. Bước nhiệm vụ chính đi Hoàng Môn không còn ở Rừng Sâu; phase quest đặt NPC.

## 9. Mở rộng roster sang 58 map ngoài phạm vi (owner 2026-10-15)

Owner yêu cầu thêm NPC cho Sa Mạc, Mỏm Đá Gió, Đảo Ác Mộng, Lăng Mộ, Giao Điểm và 6 vùng cao Lv40+ (Tinh Không, Di Tích Cổ, Lâu Đài Ma, Cây Thế Giới, Tháp Chim, Mê Thành): 11 vùng, 58 map, **54 NPC mới**.

- Số NPC mỗi map bằng số slot NPC của APK 3.2 (`apk-extract/map-scan.json`); vị trí chưa trích, đặt khi vẽ HD-2D.
- Hub an toàn (map đầu của vùng): trưởng hub (nhiệm vụ vùng + hồi máu), cửa hàng, dạy kỹ năng, NPC phụ. Hub 2 NPC: trưởng hub + một NPC cửa hàng/kỹ năng.
- Trại Tàn Sinh (map hỗn hợp): 3 NPC, được hồi máu và cửa hàng.
- Map quái: chỉ NPC nhiệm vụ phụ. Map không có slot NPC trong APK (ví dụ Thời Không Liệt Khích, các map cụt) giữ trống.
- Dữ liệu: `roster_outer.py`; `gen_npc_roster.py` gộp với `roster_data.py`. Portal của các map này vẫn ngoài ma trận chi tiết (xem §7.2 cho vùng an toàn).
