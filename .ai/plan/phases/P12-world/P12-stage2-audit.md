# P12 Stage 2 — Audit sâu Emerald + tuyến thành / hub / recovery

Ngày: 2026-10-14. Phạm vi: owner cấp quyền Stage 2 (chat 2026-10-14 16:12). Chỉ **đọc** APK 3.2, XAPK 8.4, JAR và đầu ra Stage 1 trong Downloads; chỉ ghi vào `.ai`. Không sửa runtime, không tái dựng va chạm (U3 đã chuyển sang dựng mới cho HD-2D). Mức bằng chứng: **cấu hình khai báo thu hồi từ asset tĩnh; hành vi runtime chưa kiểm chứng** (`semantic_status = DECLARED_CONFIGURATION_RECOVERED_RUNTIME_BEHAVIOUR_UNVERIFIED`). Báo cáo này không phải P12 closure.

**Owner duyệt 2026-10-14 16:42:** (1) giữ điểm xuất hiện 1 đơn vị + cửa chỉ kích hoạt sau khi người chơi rời vùng kích hoạt (R-S2-1); (2) Sảnh vẫy gọi → Rừng BiBo: người chơi xuất hiện ngay mép cửa vào ở mép trái Rừng BiBo (R-S2-2); (3) vị trí bệ phép U1 đúng; (4) vector cửa = điểm xuất hiện được dùng làm cơ sở thiết kế, kiểm thử ở Stage 3. **Stage 2 coi như đóng; chưa mở Stage 3.**

## 1. Kết quả chính
1. **Danh tính và chuỗi liên kết Emerald khớp qua cả hai phiên bản.** 6 bản ghi LoadScene liên quan (mục 2) có payload giống nhau ở 3.2 và 8.4 (`version-comparison.json`). Tên scene đích là `RungBiBo` cho cả hai submap và `QTTP` cho cổng thành.
2. **Phát hiện mới: trường `vector_raw` của mỗi cửa hoạt động như toạ độ xuất hiện ở map đích.** Trên 130 cửa có vector khác 0 và map đích xác định được: **122/130 (94 %) nằm trong bounds map đích**; 8 ngoại lệ đều là các map "Rừng sâu" dùng chung một mẫu (vector 17.0 sao chép từ mẫu, ngoài bounds của cổng đích). Khoảng cách từ điểm xuất hiện tới cửa đối ứng trên map đích (128 cặp): **trung vị 1,89 đơn vị**, 82/128 nằm trong 1–2,5 đơn vị. Đây là suy luận từ hình học, chưa phải bằng chứng runtime.
3. **Điểm xuất hiện gốc của chuỗi Emerald:**
   | Cửa | Vector (x, y) | Map đích | Cách cửa đối ứng |
   |---|---|---|---|
   | Rừng BiBo → Rừng sâu (`Door`, 389) | (37,30; 0,92) | `emerald_forest_deep_woods` | 1,68 từ Door 1 (x 35,62) |
   | Rừng sâu → Rừng BiBo (`Door 1`, 388) | (17,0; 1,0) | `emerald_forest_main_woods` | 2,31 từ Door (x 19,31) |
   | Rừng sâu → Cổng Hoàng cung (`Door 2`, 390, NEXTSCENE, level_field 10) | (27,0; 0) | `city_palace_gate` | 2,1 từ cửa tới Quảng trường (x 24,9); **không có cửa tới Emerald** |
   | Sảnh vẫy gọi → Rừng BiBo (306, NEXTSCENE) | (0, 0, 0) | `emerald_forest_main_woods` | vector 0 = chưa khai báo điểm xuất hiện; cần quy tắc mặc định (U10) |
   | Cổng Hoàng cung → Quảng trường (1140 / 1144) | (8,55; 0) / (27,0; 0) | `city_square` / `city_palace_gate` | 1,34 / 2,1 |
4. **Xác nhận mô hình trụ teleport.** Palace Gate **không có cửa nào dẫn tới Emerald** (phù hợp lời owner): thành → vùng ngoài chỉ qua trụ; Door 2 là đường về/recovery một chiều. Sáu vùng trung cấp (Bãi biển, Sa mạc, Mỏm đá gió, Đảo ác mộng, Lăng mộ, Giao điểm) đều có `Door 2 → city_square` (đường về thành).
5. **Sảnh vẫy gọi → Emerald một chiều.** Không tồn tại bản ghi Rừng BiBo → Sảnh vẫy gọi (đúng quyết định "không quay lại sảnh").

## 2. Bounds và vị trí cửa (đơn vị thế giới, ước lượng tĩnh)
| Map | Bounds x | Cửa (x) → đích | Cách mép |
|---|---|---|---|
| Rừng BiBo | -1,98→20,74 | 19,31 → Rừng sâu | 1,43 |
| Rừng sâu | 32,54→60,32 | 35,62 → Rừng BiBo (cách mép trái 3,08); 58,40 (Door 2) → Cổng Hoàng cung | 3,08 / 1,92 |
| Cổng Hoàng cung | 23,33→45,87 | 24,90 → Quảng trường; 44,63 → Chợ; 34,47 → Cung điện | 1,57 / 1,24 / 11,14 |
| Quảng trường | -14,36→11,07 | 9,89 → Cổng Hoàng cung; -13,12 → Chợ | 1,18 / 1,24 |

Các cửa nằm cách mép 1–2 đơn vị, tức đầu mút của map, đúng mô hình "điểm về ở đầu map lớn". Riêng cửa Rừng sâu → Rừng BiBo (Door 1) cách mép trái 3,08, không nằm sát mép.

## 3. U1 — vị trí bệ phép trong Quảng trường
Owner đánh dấu bệ phép hình thoi xanh ngọc ở phía dưới bên phải ảnh nền `city_square` (2543×853, 100 px/đơn vị, gốc ảnh = (min x, max y) của bounds). Quy đổi: tâm ≈ (2060, 590) px → **thế giới ≈ (6,2; -1,7)**, phạm vi x 4,3→8,1, y -0,7→-2,7. Cách cửa Quảng trường → Cổng Hoàng cung (9,89; -0,95) khoảng 3,8 đơn vị. Độ chính xác: theo ước lượng bằng mắt trên ảnh; cần chốt bằng công cụ đánh dấu trước khi dùng cho Stage 3.

## 4. JAR gốc (`Pokezoo 100.jar`)
- JAR chỉ chứa **5 gói khu vực**: `area5` Nông trường Poke, `area6` Trạm kiểm soát người mới (Sảnh Vẫy Gọi), `area19` Chợ, `area33` Quảng trường (Đế đô Sevilla), `area34` Cổng Hoàng Cung. **Không có Emerald/Rừng BiBo**, nên JAR không đối chiếu được danh tính Emerald.
- JAR xác nhận chuỗi thành tương đương APK: Sảnh Vẫy Gọi, Quảng trường, Cổng Hoàng Cung, Chợ, Nông trường. Sảnh Vẫy Gọi trong JAR gồm **4 phòng 52×15 ô cộng 1 "Phòng nghỉ" 25×15 ô**, trong khi APK chỉ có một scene `SanhVayGoi`. Có thể bản gốc chia sảnh thành nhiều phòng; chưa giải mã được ý nghĩa header (`EMBEDDED_MAP_RESOURCE_AND_TITLE_RECOVERED_ROUTING_AND_HEADER_SEMANTICS_UNRESOLVED`).
- Định dạng `.pkg` là nhị phân tuỳ biến (chuỗi UTF + số nguyên + tên PNG); **chưa giải mã** bảng cửa/va chạm. Không cần cho hướng HD-2D hiện tại; chỉ làm nếu owner muốn đối chiếu bố cục sảnh.

## 5. Rủi ro / vấn đề phát hiện
| # | Vấn đề | Ảnh hưởng | Đề xuất |
|---|---|---|---|
| R-S2-1 (**đã duyệt**) | **Xuất hiện cách cửa về chỉ 1 đơn vị có thể kích hoạt lại cửa ngay** (bán kính kích hoạt cửa chưa biết). Gốc APK dùng trung vị 1,9 (1,3–2,3 trong chuỗi Emerald) | Người chơi qua trụ có thể bị đẩy ngược Cổng Hoàng cung | Giữ owner chốt ≈1 đơn vị nhưng thêm quy tắc: cửa không kích hoạt tới khi người chơi rời vùng kích hoạt (hoặc kích hoạt bằng thao tác); kiểm thử ở Stage 3 |
| R-S2-2 (**đã duyệt**) | Vector (0,0,0) cho Sảnh vẫy gọi → Rừng BiBo (27/157 bản ghi có vector 0) | Chưa có điểm xuất hiện gốc | Xuất hiện ngay mép cửa vào ở mép trái Rừng BiBo (x ≈ -1), chốt khi dựng cảnh |
| R-S2-3 | `level_field_raw = 10` chỉ có ở Door 2 (Rừng sâu → Cổng Hoàng cung) | Ý nghĩa chưa rõ | Owner đã chốt không chặn; ghi nhận, không dùng làm luật |
| R-S2-4 | 8 cửa của các map "Rừng sâu" mẫu chung có vector 17,0 ngoài bounds | Dữ liệu mẫu sao chép | Không ảnh hưởng Emerald; xử lý khi tới Stage 4 cho vùng cao |
| R-S2-5 | Tọa độ bệ phép U1 ước lượng bằng mắt | Sai số vài chục px | Owner/Stage 3 chốt chính xác |

## 6. Trạng thái các điểm chưa xác minh
| U | Trạng thái sau Stage 2 |
|---|---|
| U1 | Owner xác nhận vị trí bệ; tọa độ thế giới ước lượng (6,2; -1,7) |
| U2 | Giữ ≈1 đơn vị (owner); gốc APK 1,3–2,3; thêm R-S2-1 |
| U3 | Va chạm mới cho HD-2D; không cần tái dựng |
| U4 | Không chặn (owner) |
| U5 | HanhLang = Tàu cướp biển (owner) |
| U7 | Thuộc P15/P19; không chặn prototype |
| U8–U10 | Đã chốt hướng |
| Mới | R-S2-1 đến R-S2-5 ở trên |

## 7. Điều chưa làm
- Không chạy client/server, không kiểm chứng runtime của cửa/spawn.
- Không giải mã `.pkg` của JAR.
- Không xác minh `Door 2 NEXTSCENE` có tải khác `NEXTMAP` hay không (hai chế độ tải khác nhau).
- Chưa audit 6 vùng cao (ngoài scope Stage 2 Emerald); chờ Stage 4.

## 8. Gate để sang Stage 3
- Owner duyệt báo cáo này và các tên/pet đang chờ (xem README).
- Owner cấp quyền Stage 3 riêng (Golden Scene và benchmark Godot Web vs Three.js).
