> Nguồn Stage 1 (ngoài repo, chỉ đọc): `~/Downloads/Phimond-P12-Review/` (inventory, `recovered-portals.json`, `portal-geometry-draft.json`, `reviews.json` = bản ghi duyệt của owner). Repo chỉ giữ tài liệu thiết kế và tóm tắt.

# Phát hiện: luồng Thành phố → Vùng ngoài (APK 3.2)

Ngày: 2026-10-14. Nguồn: `recovered-portals.json` (Stage 1) + chuỗi trong `global-metadata.dat` của APK 3.2 (đọc tĩnh, không chạy game). Đính chính sơ đồ nối trước đó của agent: thiếu cạnh Quảng trường → Rừng BiBo **không phải lỗi riêng của Emerald**.

## Quan sát có bằng chứng
1. Trong 157 bản ghi LoadScene, 21 bản ghi kiểu NEXTSCENE (đổi scene): chỉ có `SanhVayGoi → RungBiBo`, mỗi vùng ngoài `Door 2 → QTTP` (thành) hoặc `→ HanhLang` (6 vùng cao), và các map phụ (Guild, Maya, SoiCuu…) `→ QTTP`. **Không có NEXTSCENE nào từ QTTP đi ra vùng ngoài.**
2. `RungBiBo Door 2 → QTTP idx 1` (Cổng Hoàng cung) có `level_field_raw = 10`; các cửa về thành khác có giá trị 0. Ý nghĩa chưa xác minh.
3. Thư mục scene theo khoảng cấp: `Map/1-10/RungBiBo`, `10-15/BaiBienKhoBau`, `15-20/SaMac`, `20-25/MomDaGio`, `25-30/DaoAcMong`, `30-35/LangMo`, `35-40/GiaoDiem`.
4. Metadata chứa một danh sách vùng với nhãn hiển thị và khoảng cấp, theo thứ tự: Nông trại · Rừng BiBo (Lv1–10) · Bãi biển kho báu (10–15) · Sa mạc Baren (15–20) · Mỏm Đá Gió (20–25) · Đảo ác mộng (25–30) · Lăng mộ các vị thần (30–35) · Giao điểm Tunnel (35–40) · **Tàu cướp biển** · Thời gian và không gian (40–45) · Di tích cổ (45–50) · Lâu đài ma (50–100) · Cây thế giới (50–100) · Tháp chim (100–140) · Mê thành bất tử (130–170) · Quảng trường thành phố. Cùng khối có hằng số `NONGTRAI, RUNGBIBO, BAIBIENKHOBAU, SAMACRARREN, MOMDAGIO, DAOACMONG, LANGMOCACVITHAN, GIAODIEMTUNNEL, TAUCUOPBIEN, TINHKHONG, DITICHCO, LAUDAIMA, CAYTHEGIOI, THAPCHIM, METHANHBATTU`.
5. Có nhãn "Điện thờ Maya" ngay sau Đảo ác mộng (Lv25–30).

## Suy luận (chưa xác minh runtime)
- Đường chơi mới: Sảnh vẫy gọi → Rừng BiBo → Rừng sâu → Cổng Hoàng cung (thành).
- Từ thành ra các vùng: nhiều khả năng qua **bảng chọn vùng theo cấp độ** (UI), không phải cửa vật lý. Chưa tìm thấy mã gọi nó.
- Cạnh thiếu trong sơ đồ nối là một lớp truyền tống chưa mô hình hóa, không phải portal bị bỏ sót.

## Khoảng trống mới
- **Tàu cướp biển** có hằng số và nhãn UI nhưng **không có scene** trong 92 map của 3.2/8.4.
- Hành lang tầng giữa nhận cửa từ 6 vùng cao, nhưng không có cửa ra dạng LoadScene.
- Chưa biết điều kiện cấp độ, vé/phiếu, hay ai/đâu mở bảng chọn vùng. Cần xác minh trong Stage 2 hoặc bạn mô tả.


## Cập nhật 2026-10-14 — owner mô tả (nguồn: owner, chưa đối chiếu runtime APK)
- Ở **Quảng trường thành phố** có **trụ đá teleport** tới các map sơ cấp và tới map **Tàu cướp biển**.
- Ở **Tàu cướp biển** có một trụ teleport tới các map **trung cấp và cao cấp**, và một đường **quay lại Quảng trường**.

### Suy luận của agent — **owner xác nhận ĐÚNG 2026-10-14 (U5)**
- Scene **HanhLang ("Hành lang tầng giữa") chính là Tàu cướp biển (tên mới: Hải Tặc Hào)**: 6 vùng cao đều có `Door 2 → HanhLang`; HanhLang không có cửa ra dạng LoadScene (đúng với việc đi ra bằng trụ teleport); ảnh scene có đại bác, thùng gỗ, cờ hiệu và giá vũ khí; và `TAUCUOPBIEN` có hằng số UI nhưng không có scene riêng nào trong 92 map.
- Do đã xác nhận, khoảng trống "Tàu cướp biển không có scene" và "Hành lang không có cửa ra" được giải quyết cùng lúc.
- Vùng trung cấp (Lv20–40) có `Door 2 → QTTP` (về thành), trong khi vùng cao (Lv40+) có `Door 2 → HanhLang` (về tàu). Vào bằng trụ, ra bằng cửa: bất đối xứng.


## Quyết định của owner 2026-10-14 (chiều) — hợp đồng trụ teleport (DRAFT)
Nguồn: owner mô tả. Mức bằng chứng APK ghi riêng ở từng dòng.

| Mục | Quyết định | Đối chiếu APK 3.2 |
|---|---|---|
| Trụ ở Quảng trường (`city_square`) | Đi tới **mọi vùng Lv1–40**: Rừng BiBo, Bãi biển kho báu, Sa mạc Baren, Mỏm Đá Gió, Đảo ác mộng, Lăng mộ các vị thần, Giao điểm Tunnel; cộng **Nông trại** và **Tàu cướp biển** | Khoảng cấp lấy từ nhãn UI trong metadata (thứ tự khớp). Vị trí trụ trong scene: **chưa tìm thấy** (không phải LoadScene) |
| Trụ ở Tàu cướp biển | Đi tới các vùng cao: Thời không (40–45), Di tích cổ (45–50), Lâu đài ma, Cây thế giới, Tháp chim, Mê thành bất tử; cộng **Nông trại**; có đường **quay lại Quảng trường** | 6 vùng cao đều `Door 2 → HanhLang`. Chưa xác nhận HanhLang = Tàu cướp biển |
| Hiển thị | Chỉ hiện vùng **đủ cấp người chơi** (so với mức tối thiểu của nhãn khoảng cấp). **Tàu cướp biển: tối thiểu Lv40** | Nhãn khoảng cấp có trong APK; quy tắc hiện/ẩn là owner quyết, chưa kiểm chứng |
| Nông trại | Vào bằng trụ, ở cả hai trụ (thành và tàu) | `NONGTRAI` là hằng số đầu bảng vùng; scene Farm ở `city_farm` |
| Điểm đến | **Cạnh điểm quay về, ở đầu mỗi map lớn** | Dữ liệu khớp: mọi vùng đều có `Door 2` về thành/tàu nằm sát mép trong của submap đầu (cách biên khoảng 1–2 đơn vị). Ngoại lệ: **Rừng BiBo** có `Door 2` ở **Rừng sâu** (x=58.4, biên phải 60.3), nên điểm đến từ trụ là **Rừng sâu**, không phải Rừng BiBo |

### Hệ quả cho prototype Emerald
- Từ trụ, người chơi xuất hiện ở **`emerald_forest_deep_woods`** cạnh cửa về Cổng Hoàng cung, rồi đi sang Rừng BiBo qua `Door 1` (x=35.6).
- Đường chơi mới vẫn là Sảnh vẫy gọi → Rừng BiBo → Rừng sâu → Cổng Hoàng cung.
- Còn thiếu để duyệt baseline: vị trí trụ trong `city_square`, offset điểm đến chính xác, collision. APK chưa cho; cần Stage 2 hoặc bạn mô tả.


## Bổ sung 2026-10-14 (chiều muộn)
- Điểm đến sau teleport cách cửa về **khoảng 1 đơn vị** về phía trong map (owner).
- Dưới Lv10 vẫn đi qua được cửa Rừng sâu → Cổng Hoàng cung; trụ ở thành đưa về Emerald khi cần (owner).
- Luồng người chơi mới: đăng ký/đăng nhập → **Sảnh vẫy gọi** (chọn pet 1★) → quest → Emerald. Chi tiết ở [P12-emerald-baseline-package.md](P12-emerald-baseline-package.md).
