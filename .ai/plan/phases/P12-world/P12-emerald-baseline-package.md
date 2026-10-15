> Nguồn Stage 1 (ngoài repo, chỉ đọc): `~/Downloads/Phimond-P12-Review/` (inventory, `recovered-portals.json`, `portal-geometry-draft.json`, `reviews.json` = bản ghi duyệt của owner). Repo chỉ giữ tài liệu thiết kế và tóm tắt.

# Gói baseline Emerald Forest (DRAFT chờ owner duyệt)

Ngày: 2026-10-14. Nguồn chính: APK **3.2** (owner đã duyệt làm nguồn chính). Mức bằng chứng: tọa độ portal và bounds là **ước lượng tĩnh từ sprite** (`UNIQUE_VISUAL_BOUNDS_CANDIDATE`), chưa chứng nhận runtime. Gói này không phải P12 closure và không mở Stage 3.

## 1. Danh tính và phạm vi
- **Emerald Forest = `RungBiBo`** (scene `Map/1-10/RungBiBo`, khoảng cấp **Lv1–10**), gồm 2 submap: `emerald_forest_main_woods` (Rừng BiBo, đầu xa), `emerald_forest_deep_woods` (Rừng sâu, phía thành).
- **Cảnh đầu tiên của luồng người chơi mới: Sảnh vẫy gọi** (`summoning_hall_main_hall`). Sau khi đăng ký và đăng nhập lần đầu, người chơi chọn **pet 1★ khởi đầu** tại đây. Sau đó có **quest** dẫn sang Emerald Forest (owner, 2026-10-14).
- **Cảnh render/benchmark: Emerald (cả hai submap).** Khi dùng trụ teleport từ thành, điểm đến là `emerald_forest_deep_woods` cạnh cửa về (đầu map lớn theo quy tắc trụ). Khi đi từ Sảnh vẫy gọi, người chơi vào `emerald_forest_main_woods` qua `Door` như APK.
- **Scope chi tiết (cập nhật):** 15 ứng viên Stage 1 **+ `middle_corridor_main_hall` (Tàu cướp biển?)** vì là đầu mối vùng Lv40+. Chờ owner duyệt danh sách chính xác.

## 2. Bounds (đơn vị thế giới, ước lượng tĩnh)
| Map | Bounds |
|---|---|
| `summoning_hall_main_hall` | x -9.3→15.9, y -3.2→5.2 |
| `emerald_forest_main_woods` | x -2.0→20.7, y -3.4→5.3 |
| `emerald_forest_deep_woods` | x 32.5→60.3, y -3.1→5.4 |
| `city_palace_gate` | x 23.3→45.9, y -3.6→4.8 |
| `city_square` | x -14.4→11.1, y -4.4→4.2 |

## 3. Portal liên quan (3.2, hướng đi có hướng)
| Từ → Đến | Cửa | xy (ước lượng) | Raw record |
|---|---|---|---|
| `summoning_hall_main_hall` → `emerald_forest_main_woods` | Door | (14.6, -0.3) | `3.2:level2:loadscene:306` |
| `city_palace_gate` → `city_square` | Door (1) | (24.9, -1.2) | `3.2:level3:loadscene:1140` |
| `city_square` → `city_palace_gate` | Door | (9.9, -0.9) | `3.2:level3:loadscene:1144` |
| `emerald_forest_deep_woods` → `emerald_forest_main_woods` | Door 1 | (35.6, 0.5) | `3.2:level4:loadscene:388` |
| `emerald_forest_main_woods` → `emerald_forest_deep_woods` | Door | (19.3, 0.4) | `3.2:level4:loadscene:389` |
| `emerald_forest_deep_woods` → `city_palace_gate` | Door 2 | (58.4, 0.5) | `3.2:level4:loadscene:390` |

8.4: số portal và payload LoadScene **không khác** 3.2 (`version-comparison.json`); ý nghĩa tương đương chưa chứng minh.

## 4. Sơ đồ có hướng (trước → sau owner bổ sung)
**Luồng người chơi mới (owner):** Đăng ký → Đăng nhập lần đầu → Sảnh vẫy gọi (chọn pet 1★) → quest → Rừng BiBo → Rừng sâu → Cổng Hoàng cung.
**Đã có trong APK (cửa):**
```
Sảnh vẫy gọi ──→ Rừng BiBo ⇄ Rừng sâu ──→ Cổng Hoàng cung
Cổng Hoàng cung ⇄ Quảng trường · Chợ · Cung điện Hoàng gia
```
**Owner bổ sung (trụ teleport, chưa có trong APK):**
```
Quảng trường ══trụ══→ Rừng sâu (cạnh cửa về) · các vùng Lv1–40 · Nông trại · Tàu cướp biển (Lv40+)
Rừng sâu ──Door 2──→ Cổng Hoàng cung  (đường về / recovery)
```
Không ép cửa một chiều thành hai chiều. Chiều vào từ thành là trụ, chiều ra là cửa.

## 5. Quy tắc trụ teleport (owner)
- Chỉ hiện vùng đủ cấp người chơi; Tàu cướp biển tối thiểu Lv40; Rừng BiBo hiện từ Lv1.
- Điểm đến: **cạnh điểm quay về ở đầu map lớn**, cách cửa **khoảng 1 đơn vị** về phía trong map để liền mạch (owner chốt). Với Emerald: Rừng sâu, cạnh `Door 2` (x≈58,4, nên xuất hiện khoảng x≈57,4).
- Người chơi **dưới Lv10 vẫn được đi qua** cửa Rừng sâu → Cổng Hoàng cung; trụ ở thành đưa họ quay lại Emerald khi cần (owner chốt).

## 6. Điểm chưa xác minh (chặn hoặc cần duyệt)
| # | Điểm | Ảnh hưởng | Cách giải |
|---|---|---|---|
| U1 | **ĐÃ CHỐT 2026-10-14:** trụ đá teleport đặt trên bệ phép hình thoi xanh ngọc ở phía dưới bên phải Quảng Trường Thạch Trụ (`city_square`). Bệ đã có sẵn trong nền APK, trụ chưa gắn. Tọa độ xấp xỉ trên ảnh gốc 2543×853: tâm khoảng (2060, 590), phạm vi khoảng x 1870–2250, y 490–690 | Arrival từ thành | Owner xác nhận bệ; tọa độ chính xác và quy đổi sang đơn vị thế giới làm ở Stage 2 |
| U2 | ~~Offset điểm xuất hiện~~ | **ĐÃ CHỐT: ≈1 đơn vị** (owner 2026-10-14); cần kiểm tra không rơi vào vùng collision khi có dữ liệu | — | **Stage 2:** gốc APK dùng điểm xuất hiện cách cửa đối ứng 1,3–2,3 đơn vị (trung vị toàn bản đồ 1,89); xem R-S2-1 (owner duyệt: giữ 1 đơn vị, cửa chỉ kích hoạt sau khi rời vùng kích hoạt). Sảnh vẫy gọi → Rừng BiBo: xuất hiện ngay mép cửa vào, mép trái Rừng BiBo (R-S2-2, owner duyệt).
| U3 | **ĐÃ CHỐT HƯỚNG 2026-10-14:** không khôi phục va chạm gốc. Dựng va chạm mới cho bản vẽ HD-2D, lấy ảnh 2D gốc làm bản phác (vị trí tương đối của cổng, bệ, lối đi). Bản thử Emerald dùng lớp vùng đi được tối giản vẽ tay trên ảnh HD-2D | Traversal | Thuộc lớp Logical (D25). Hoàn thiện ở Stage 4; bản thử ở Stage 3. Q-P12-01 (tái dựng từ APK) không còn bắt buộc |
| U4 | ~~`level_field_raw = 10`~~ | **ĐÃ CHỐT: không chặn**, dưới Lv10 vẫn đi qua được (owner). Giá trị 10 trong APK chưa rõ nghĩa; không dùng làm luật | — |
| U5 | **ĐÃ CHỐT 2026-10-14:** HanhLang (`middle_corridor_main_hall`) = Tàu cướp biển; trụ teleport trên tàu là lối ra tới 6 vùng cao, về thành và Nông trại | Scope và đường Lv40+ | Owner xác nhận |
| U6 | **ĐÃ CHỐT 2026-10-14:** tên submap Emerald theo owner: `emerald_forest_main_woods` = Bìa Rừng Lục Bảo; `emerald_forest_deep_woods` = Rừng Sâu Lục Bảo. Sảnh vẫy gọi đề xuất **Triệu Linh Điện** | Hiển thị UI | Bảng đầy đủ: `P12-world-names-master.md` |
| U7 | NPC, spawn, monster của Emerald | Không chặn prototype render/traversal | Owner phase khác (P15/P19) |
| U8 | **ĐÃ CHỐT 2026-10-14 (cập nhật):** chuỗi nhiệm vụ đầu: nói chuyện với người hướng dẫn → chọn pet → mở khóa điểm dịch chuyển tới Emerald Forest. Điểm dịch chuyển khóa trước đó. Sau khi qua, **không dịch chuyển ngược lại Sảnh vẫy gọi** (một chiều) | Truy cập, onboarding | Logic quest thuộc P04; P12 ghi trạng thái: locked → unlocked sau khi chọn pet, cạnh Sảnh→Emerald là một chiều. Chi tiết: lối ra là điểm dịch chuyển (không phải Door); xác nhận Stage 2 |
| U9 | **ĐÃ CHỐT 2026-10-14:** 3 pet 1★ khởi đầu, 3 race khác nhau: Xương Rồng `species_0021` (plant), Bọ Cạp Sa Mạc `species_0109` (insect), Ưng Đỏ `species_0071` (beast) | Cảnh Sảnh vẫy gọi | Atlas đủ 20/20 ô, 0 issue; ô typical 11/20, 15/20, 15/20. UI chọn thuộc P03/P04; chỉ số khởi đầu thuộc P10/P11 |
| U10 | **ĐÃ CHỐT HƯỚNG 2026-10-14:** Sảnh vẫy gọi có 3 bệ đá, mỗi bệ một thần thú Special 5★ của race tương ứng, đại diện cho pet 1★ cùng race. Người chơi chọn bệ, nói chuyện, đồng ý thì nhận pet 1★ tương ứng ở Lv1. **Thần thú:** Linh Tiên Hoa Hương `species_0144` (plant, owner chọn), Đại Vương Bọ Cạp `species_0151` (insect), Thú Vàng Một Sừng `species_0149` (beast) — **owner duyệt cả 3 thần thú 2026-10-15**. **Bố cục đã chốt:** người chơi xuất hiện ở cửa vào; 3 bệ đá xếp hình cung phía trước; người hướng dẫn đứng giữa; điểm dịch chuyển (khóa) ở phía sau. **Còn mở:** tọa độ cụ thể (Stage 2) | Safe arrival của map đầu tiên | Thần thú chỉ là mô hình trưng bày, không nhận được; logic nói chuyện/nhận pet thuộc P04. Tọa độ: owner mô tả hoặc Stage 2 |

## 7. Duyệt từng phần (partial approval cho phép)
Owner (2026-10-14): các mục đã chốt qua chat được coi là duyệt; **còn lại chỉ 2 thần thú đề xuất** (Đại Vương Bọ Cạp, Thú Vàng Một Sừng).
- [x] Danh tính và phạm vi (mục 1) — owner duyệt 2026-10-14
- [x] Bounds (mục 2) — owner duyệt 2026-10-14
- [x] Portal và sơ đồ (mục 3–4) — owner duyệt 2026-10-14
- [x] Quy tắc trụ (mục 5) — owner duyệt 2026-10-14
- [x] Chấp nhận U7 là unresolved/deferred có điều kiện (U3 đã chốt hướng) (U2, U4, U5, U6, U8–U10 đã chốt hướng)
