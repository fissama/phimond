# P10 — Danh sách chuẩn 152 loài từ APK 8.4

Status: **baseline đã được chủ dự án chấp nhận ngày 2026-09-28**.

Dữ liệu máy đọc: [roster_apk84.json](../../../../data/pets/roster_apk84.json). Giữ nguyên ID, tên, mô tả, race và sao từ catalog nguồn. Danh sách này không tự suy ra Element/stat/skill/drop và không có nghĩa tất cả loài đều đã được bật trong gameplay hiện tại.

135 loài thường + 17 thần thú. Phân bố sao tính cả thần thú: **50 / 30 / 24 / 21 / 27**.

| Race | 1★ | 2★ | 3★ | 4★ thường | 4★ thần | 5★ thường | 5★ thần | Tổng |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sâu / Insect | 7 | 4 | 3 | 2 | 0 | 2 | 2 | 20 |
| Linh Thể / Spirit | 5 | 2 | 3 | 2 | 1 | 2 | 2 | 17 |
| Chim / Bird | 7 | 4 | 3 | 2 | 1 | 2 | 2 | 21 |
| Ác Ma / Demon | 6 | 4 | 3 | 2 | 1 | 1 | 1 | 18 |
| Dã Thú / Beast | 7 | 4 | 3 | 3 | 1 | 2 | 2 | 22 |
| Thực Vật / Plant | 7 | 4 | 3 | 2 | 0 | 2 | 2 | 20 |
| Bất Tử / Undead | 7 | 4 | 3 | 2 | 0 | 2 | 2 | 20 |
| Rồng / Dragon | 4 | 4 | 3 | 2 | 0 | 1 | 0 | 14 |

## 17 công thức thần thú có trong catalog

Giữ thứ tự `Chinh`/`Phu` của nguồn. Bảng chưa chứng minh có thể đảo nguyên liệu hay xác nhận cost, Plus, tỷ lệ thành công và điều kiện phía server.

| Đích | Race | Sao | Chính | Phụ | Hồn theo catalog vật phẩm |
|---|---|---:|---|---|---|
| Nữ Đế Minh Giới | Bất Tử / Undead | 5 | Nữ Vương Bạch Cốt | Tinh Linh Bách Hoa | `KetHopTT5S` |
| Thủ Lĩnh Hắc Ám | Bất Tử / Undead | 5 | Rồng Xương Băng | Đại Bàng Vàng | `KetHopTT5S` |
| Thanh Long | Ác Ma / Demon | 4 | Đại Ác Ma | Gấu Trúc Ma Pháp | `KetHopTT4S` |
| Bạch Hổ | Dã Thú / Beast | 4 | Tinh Tinh Rock | Trùng Gai Nhọn | `KetHopTT4S` |
| Chu Tước | Chim / Bird | 4 | Chim Đại Phì | Ma Gương Thủy Tinh | `KetHopTT4S` |
| Trùng Mẫu Mào Vàng | Sâu / Insect | 5 | Nhện Phu Nhân | Totem Thượng Cổ | `KetHopTT5S` |
| Huyền Vũ | Linh Thể / Spirit | 4 | Thú Lớn Dung Nham | Đại Tuyết Quái | `KetHopTT4S` |
| Thần Tướng Cự Ma | Linh Thể / Spirit | 5 | Nhân Sư | Người Tuyết Viễn Cổ | `KetHopTT5S` |
| Thần Đèn | Linh Thể / Spirit | 5 | Totem Thượng Cổ | Nữ Vương Bạch Cốt | `KetHopTT5S` |
| Linh Tiên Hoa Hương | Thực Vật / Plant | 5 | Độc Đằng Nữ | Trùng Bất Tử Địa Huyệt | `KetHopTT5S` |
| Cây Cự Linh | Thực Vật / Plant | 5 | Tinh Linh Bách Hoa | Sói Xích Viêm | `KetHopTT5S` |
| Ma Vương Hút Máu | Ác Ma / Demon | 5 | Trụy Thiên Sứ | Nhân Sư | `KetHopTT5S` |
| Ngựa Bùn Cỏ | Dã Thú / Beast | 5 | Sói Xích Viêm | Chim Cú Địa Ngục | `KetHopTT5S` |
| Thú Vàng Một Sừng | Dã Thú / Beast | 5 | Người Tuyết Viễn Cổ | Nhân Sư | `KetHopTT5S` |
| Đảo Thiên Đường | Chim / Bird | 5 | Chim Cú Địa Ngục | Nhện Phu Nhân | `KetHopTT5S` |
| Đại Vương Bọ Cạp | Sâu / Insect | 5 | Trùng Bất Tử Địa Huyệt | Độc Đằng Nữ | `KetHopTT5S` |
| Chim Ái Thần | Chim / Bird | 5 | Đại Bàng Vàng | Rồng Xương Băng | `KetHopTT5S` |

## Sâu / Insect

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Bọ Cánh Cứng Răng Kiếm · `BoCanhCungRangKiem` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BoCanhCungRangKiem/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BoCanhCungRangKiem/frames.tres) |
| Bọ Cạp Sa Mạc · `BoCapSaMac` | 1 | Thường | Bọ cạp đỏ , thường sử dụng ma pháp hệ đất , xuất hiện ở sa mạc Hoang vu.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BoCapSaMac/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BoCapSaMac/frames.tres) |
| Bọ Ngựa Móng Sắt · `BoNguaMongSat` | 1 | Thường | Bọ Ngựa móng sắt có sức phong ngự vật lý , xuất hiện lần ở San Mang Ma | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BoNguaMongSat/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BoNguaMongSat/frames.tres) |
| Nhện Độc · `NhenDoc` | 1 | Thường | Đỉnh núi Phong Nham xuất hiện loài nhện núi ,mình lớn ,móng vuốt nhỏ  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NhenDoc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NhenDoc/frames.tres) |
| Ốc Sên Hoa · `OcSenHoa` | 1 | Thường | Ốc sên nhỏ đáng yêu , sức phong ngự vật lý rất cao , xuất hiện ở rừng sâu bích ba.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/OcSenHoa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/OcSenHoa/frames.tres) |
| Ong Giết Người · `OngGietNguoi` | 1 | Thường | Loài ong hung ác ,có nọc độc mạnh , xuất hiện ở sa mạc Hoang vu | [Ảnh](../../../../apps/game-client/assets/pets/apk84/OngGietNguoi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/OngGietNguoi/frames.tres) |
| Thiên Ngưu · `ThienNguu` | 1 | Thường | ‌Poke ra tay cần bằng nhanh ,có khả năng công kích nhóm ma pháp và vật lý , còn có khả năng kháng tính tối tốt.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThienNguu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThienNguu/frames.tres) |
| Bướm Hoa Vũ · `BuomHoaVu` | 2 | Thường | ‌Hp và Trí tuệ trưởng thành cực tốt,poke ma pháp .Có khả năng trị liệu nhóm và ít kỹ năng phụ trợ.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BuomHoaVu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BuomHoaVu/frames.tres) |
| Châu Chấu Móng Lớn · `ChauChauMongLon` | 2 | Thường | Trí tuệ và phòng ngự vô cùng lý tưởng , ngoài ra tấn công pháp thuật cá thể còn có tấn công nọc độc.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChauChauMongLon/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChauChauMongLon/frames.tres) |
| Giun Đất Móng Sắt · `GiunDatMongSat` | 2 | Thường | Thường ở dưới đất , công kích và hp cao , giỏi tấn công nhóm ,có khả năng giám thấp ngưỡng Hp của địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/GiunDatMongSat/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/GiunDatMongSat/frames.tres) |
| Thú Một Sừng Vỏ Cứng · `ThuMotSungVoCung` | 2 | Thường | Mọi phương diện phát triển cân bằng ,poke ma pháp ,có kỹ năng công kích ma pháp nhóm và tự tăng Hp.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuMotSungVoCung/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuMotSungVoCung/frames.tres) |
| Cua Ký Sinh · `CuaKySinh` | 3 | Thường | ‌Hp và phòng ngự trưởng thành cực tốt, poke vật lý ,có kỹ năng công kích ma pháp kẻ địch và giảm Hp kẻ địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/CuaKySinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/CuaKySinh/frames.tres) |
| Hải Mã Bong Bóng · `HaiMaBongBong` | 3 | Thường | Hp khá tốt , poke ma pháp bổ trợ cho kỹ năng giảm hp của địch ,nâng cao kháng tính đất của mình.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HaiMaBongBong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HaiMaBongBong/frames.tres) |
| Tôm Hùm Răng Cưa · `TomHumRangCua` | 3 | Thường | Công kích vật lý trưởng thành khá tốt , có kỹ năng làm sạch lời nguyền và nâng cao ngưỡng hp của đồng đội.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TomHumRangCua/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TomHumRangCua/frames.tres) |
| Trùng Gai Nhọn · `TrungGaiNhon` | 4 | Thường | Sức mạnh và Hp trưởng thành khá cao ,là poke vật lý ,có khả năng hoá đá đối phương. Có kỹ năng tăng Hp đồng đội.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TrungGaiNhon/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TrungGaiNhon/frames.tres) |
| Trùng Hốt Lỗ · `TrungHotLo` | 4 | Thường | Hp và trí tuệ trưởng thành khá cao ,là Poke ma pháp ngoài ra khả năng làm phân tán còn có kỹ năng vận xui.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TrungHotLo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TrungHotLo/frames.tres) |
| Nhện Phu Nhân · `NhenPhuNhan` | 5 | Thường | Hp trưởng thành cực cao , dưới ảnh hưởng của ma pháp Thánh Linh từ loài bướm bình thường , trở thành poke trí tuệ.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NhenPhuNhan/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NhenPhuNhan/frames.tres) |
| Trùng Bất Tử Địa Huyệt · `TrungBatTuDiaHuyet` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TrungBatTuDiaHuyet/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TrungBatTuDiaHuyet/frames.tres) |
| Đại Vương Bọ Cạp · `DaiVuongBoCap` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaiVuongBoCap/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaiVuongBoCap/frames.tres) |
| Trùng Mẫu Mào Vàng · `TrungMauMaoVang` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TrungMauMaoVang/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TrungMauMaoVang/frames.tres) |

## Linh Thể / Spirit

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Chong Chóng Gió · `ChongChongGio` | 1 | Thường | ‌Hp và Trí tuệ trưởng thành khá cao,poke ma pháp mang sát thương quần thể là trò chơi tủ của nó.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChongChongGio/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChongChongGio/frames.tres) |
| Đá Mặt Quỷ · `DaMatQuy` | 1 | Thường | Có khả năng phòng ngự và Hp  khá cao ,kháng tính hoá đá của đối phương khá cao.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaMatQuy/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaMatQuy/frames.tres) |
| Hư Không Hắc Ám · `HuKhongHacAm` | 1 | Thường | Hành giả trên Không ,là poke khả năng ma pháp và tốc độ, nhưng khả năng tấn công lại thấp.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HuKhongHacAm/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HuKhongHacAm/frames.tres) |
| Quái Vật Nham Thạch · `QuaiVatNhamThach` | 1 | Thường | ‌Hp , phòng ngự , công kích trưởng thành cực tốt , Poke vật lý kháng tính khá nhiều .  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/QuaiVatNhamThach/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/QuaiVatNhamThach/frames.tres) |
| Quái Vật Rương Báu · `QuaiVatRuongBau` | 1 | Thường | Công kích và phòng ngự trưởng thành khá cao , đồng thời là poke vật lý có kỹ năng trị liệu kèm kháng tính vận xui khá tốt  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/QuaiVatRuongBau/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/QuaiVatRuongBau/frames.tres) |
| Ma Kiếm · `MaKiem` | 2 | Thường | Công kích trưởng thành cực tốt ,poke vật lý có kỹ năng nâng Hp.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaKiem/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaKiem/frames.tres) |
| Sách Ma Pháp · `SachMaPhap` | 2 | Thường | Phòng ngự ,trí tuệ ,Hp trưởng thành cực tốt , poke ma pháp có kỹ năng trị liệu cá thể.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/SachMaPhap/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/SachMaPhap/frames.tres) |
| Chiến Sĩ Bù Nhìn · `ChienSiBuNhin` | 3 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChienSiBuNhin/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChienSiBuNhin/frames.tres) |
| Con Rối Gạch Đá · `ConRoiGachDa` | 3 | Thường | Công kích và Hp trưởng thành khá cao ,là poke vật lý . Vững vàng như một bức tường đá , có kỹ năng làm yếu đối thủ.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ConRoiGachDa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ConRoiGachDa/frames.tres) |
| Thằng Hề Hộp · `ThangHeHop` | 3 | Thường | Ðồ dùng đe doạ trẻ con vào dịp Halloween , Một poke có Hp ,trí từ , phòng ngự trưởng thành cực tốt, có kỹ năng ma pháp mạnh.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThangHeHop/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThangHeHop/frames.tres) |
| Ma Gương Thủy Tinh · `MaGuongThuyTinh` | 4 | Thường | Trí tuệ trưởng thành cực tốt ,poke ma pháp , có kỹ năng vận xui lên địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaGuongThuyTinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaGuongThuyTinh/frames.tres) |
| Thú Lớn Dung Nham · `ThuLonDungNham` | 4 | Thường | Sức Mạnh trưởng thành cực tốt , poke vật lý có kỹ năng giảm công kích ma pháp của toàn bộ kẻ địch  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuLonDungNham/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuLonDungNham/frames.tres) |
| Huyền Vũ · `HuyenVu` | 4 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HuyenVu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HuyenVu/frames.tres) |
| Nhân Sư · `NhanSu` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NhanSu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NhanSu/frames.tres) |
| Totem Thượng Cổ · `TotemThuongCo` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TotemThuongCo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TotemThuongCo/frames.tres) |
| Thần Đèn · `ThanDen` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThanDen/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThanDen/frames.tres) |
| Thần Tướng Cự Ma · `ThanTuongCuMa` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThanTuongCuMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThanTuongCuMa/frames.tres) |

## Chim / Bird

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Chim Chào Mào · `ChimChaoMao` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimChaoMao/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimChaoMao/frames.tres) |
| Chim Cú · `ChimCu` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimCu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimCu/frames.tres) |
| Chim Ong · `ChimOng` | 1 | Thường | Poke có độ trưởng thành công kích cao ,khả năng công kích có kỹ năng trị liệu cá thể.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimOng/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimOng/frames.tres) |
| Chim Sấm · `ChimSam` | 1 | Thường | ‌Poke thiên về vật lý có khả năng phòng ngự cao ,có sức mạnh công kích nhóm.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimSam/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimSam/frames.tres) |
| Dơi · `Doi` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/Doi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/Doi/frames.tres) |
| Ưng Trọc · `UngTroc` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/UngTroc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/UngTroc/frames.tres) |
| Ưng Trọc Ma · `UngTrocMa` | 1 | Thường | Là thú săn bẩm sinh ,nó có tốc độ và khả năng công kích cực nhanh , ngoài ra còn có kỹ năng trị liệu cá thể.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/UngTrocMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/UngTrocMa/frames.tres) |
| Dơi Một Mắt · `DoiMotMat` | 2 | Thường | ‌Poke ma pháp Hp trưởng thành cao , ngoài ma pháp công kích còn có kỹ năng giảm tốc độ của kẻ địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DoiMotMat/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DoiMotMat/frames.tres) |
| Nữ Yêu Minh Ưng · `NuYeuMinhUng` | 2 | Thường | ‌Poke ma pháp trưởng thành đồng đều ,có vẻ bề ngoài khác với một số loài chim 1 sao.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NuYeuMinhUng/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NuYeuMinhUng/frames.tres) |
| Quạ Nghĩa Trang · `QuaNghiaTrang` | 2 | Thường | Công kích và phòng ngự trưởng thành khá cao poke vật lý có kỹ năng nâng cao tốc độ và kháng tính gió.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/QuaNghiaTrang/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/QuaNghiaTrang/frames.tres) |
| Tê Điểu · `TeDieu` | 2 | Thường | Công kích vật lý trưởng thành cực tốt ,poke vật lý có kỹ năng kháng tính gió của bản thân.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TeDieu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TeDieu/frames.tres) |
| Đại Bàng Sư Tử · `DaiBangSuTu` | 3 | Thường | Công kích trưởng thành cực tốt , poke vật lý có kỹ năng làm sạch nhà khí và giảm tốc độ kẻ địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaiBangSuTu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaiBangSuTu/frames.tres) |
| Ưng Hồng Vũ · `UngHongVu` | 3 | Thường | Ưng Hồng vũ Trưởng thành cân bằng , poke ma pháp ,kỹ năng công kích ma pháp tốc kẻ địch ,nâng tốc bản thân.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/UngHongVu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/UngHongVu/frames.tres) |
| Vẹt Độc Vuốt · `VetDocVuot` | 3 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/VetDocVuot/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/VetDocVuot/frames.tres) |
| Chim Đa Đa · `ChimDaDa` | 4 | Thường | Công kích trưởng thành cao ,poke vật lý nâng cao tốc toàn phương diện , ngoài ra ,có thể giải trừ hiệu quả trâm mặc cá thể.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimDaDa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimDaDa/frames.tres) |
| Chim Đại Phì · `ChimDaiPhi` | 4 | Thường | Trí tuệ trưởng thành khá cao ,poke ma pháp ngoài ra khả năng giảm tốc độ toàn thể ,còn có kỹ năng ngủ say .  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimDaiPhi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimDaiPhi/frames.tres) |
| Chu Tước · `ChuTuoc` | 4 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChuTuoc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChuTuoc/frames.tres) |
| Chim Cú Địa Ngục · `ChimCuDiaNguc` | 5 | Thường | ‌Poke ma pháp có sự nhanh nhẹn cao nhất ,có kỹ năng công kích giảm tốc kẻ địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimCuDiaNguc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimCuDiaNguc/frames.tres) |
| Đại Bàng Vàng · `DaiBangVang` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaiBangVang/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaiBangVang/frames.tres) |
| Chim Ái Thần · `ChimAiThan` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChimAiThan/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChimAiThan/frames.tres) |
| Đảo Thiên Đường · `DaoThienDuong` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaoThienDuong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaoThienDuong/frames.tres) |

## Ác Ma / Demon

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Báo Địa Ngục · `BaoDiaNguc` | 1 | Thường | Ðiểm đảng sợ của chúng là rất nhanh, ngoài ra cũng là poke ma võ song thần.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BaoDiaNguc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BaoDiaNguc/frames.tres) |
| Chó Săn Ác Ma · `ChoSanAcMa` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChoSanAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChoSanAcMa/frames.tres) |
| Ma Móng Rồng · `MaMongRong` | 1 | Thường | Hp và phòng ngự Khá tốt , công kích vật lý đa dạng ,giúp chúng giành nhiều phần thắng.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaMongRong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaMongRong/frames.tres) |
| Mắt Ác Ma · `MatAcMa` | 1 | Thường |  Trí tuệ và tinh thần trưởng thành cao ,có kỹ năng trị liệu kèm ,bù đắp cho khả năng phòng ngự Hp kém.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MatAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MatAcMa/frames.tres) |
| Tiểu Ác Ma · `TieuAcMa` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TieuAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TieuAcMa/frames.tres) |
| Yêu Tinh Biển · `YeuTinhBien` | 1 | Thường | Ác ma ẩn trong biển sâu ,công kích nhanh là đặc điểm của chúng , ngoài ra còn nắm bắt ma pháp trị liệu .  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/YeuTinhBien/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/YeuTinhBien/frames.tres) |
| Lợn Ác Ma · `LonAcMa` | 2 | Thường | Là một Poke ma pháp ,mọi thuộc tính trưởng thành  đồng đều, Nhưng đừng xem thường nó , nếu không sẽ ăn quả khổ đấy!  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/LonAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/LonAcMa/frames.tres) |
| Ma Thú Địa Ngục · `MaThuDiaNguc` | 2 | Thường | Tuy công kích trưởng thành hơi thấp ,nhưng bù lại Hp và phòng ngự cao ,lợi dụng kỹ năng phản kích tấn công kẻ địch. | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaThuDiaNguc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaThuDiaNguc/frames.tres) |
| Quái Vật Đầu Dê · `QuaiVatDauDe` | 2 | Thường | Hp ,Trí tuệ ,tinh thần, phòng ngự trưởng thành khá tốt,poke thuộc hệ ma pháp có khả năng giảm công kích vật lý của pet đối phương.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/QuaiVatDauDe/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/QuaiVatDauDe/frames.tres) |
| Tướng Chiến Ma Rồng · `TuongChienMaRong` | 2 | Thường | Là chiến sĩ ác ma ,nó có sức mạnh ,Hp , phòng ngự cao , đồng thời có thể tự nâng khả năng công kích vật lý của mình.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TuongChienMaRong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TuongChienMaRong/frames.tres) |
| Ma Muội · `MaMuoi` | 3 | Thường | Là một yêu tinh ma giới có năng lực đồng đều  , chúng có thể sử dụng vũ đạo cầm cố và giảm công kích của mục tiêu .  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaMuoi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaMuoi/frames.tres) |
| Ma Tướng Địa Ngục · `MaTuongDiaNguc` | 3 | Thường | Sức Mạnh ,Hp trưởng thành cao , nhưng tốc độ lại thấp .Có khả năng nâng cao công kích cho bản thân.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaTuongDiaNguc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaTuongDiaNguc/frames.tres) |
| Thầy Bói Ác Ma · `ThayBoiAcMa` | 3 | Thường | Giống các thầy ma khác thì có thể , nhưng  trí tuệ trưởng thành cao khiến nó có khả năng công kích ma pháp rất cao.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThayBoiAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThayBoiAcMa/frames.tres) |
| Đại Ác Ma · `DaiAcMa` | 4 | Thường | So với Ma vương địa ngục thì Đại ác ma khác lại dùng ma pháp để mà dày vò đối phương ,có ma pháp chúc phúc tự do ,và giảm sức công kích của mục tiêu.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaiAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaiAcMa/frames.tres) |
| Ma Vương Địa Ngục · `MaVuongDiaNguc` | 4 | Thường | Ma vương trên chiến trường không có chút lòng thương hại ,khả năng công kích cực mạnh và sức sống ngoan cường là ác mộng của vô số kẻ địch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaVuongDiaNguc/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaVuongDiaNguc/frames.tres) |
| Thanh Long · `ThanhLong` | 4 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThanhLong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThanhLong/frames.tres) |
| Trụy Thiên Sứ · `TruyThienSu` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TruyThienSu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TruyThienSu/frames.tres) |
| Ma Vương Hút Máu · `MaVuongHutMau` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaVuongHutMau/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaVuongHutMau/frames.tres) |

## Dã Thú / Beast

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Ma Cây · `MaCay` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaCay/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaCay/frames.tres) |
| Rùa Phú Quý · `RuaPhuQuy` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RuaPhuQuy/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RuaPhuQuy/frames.tres) |
| Sói Ngớ Ngẩn · `SoiNgoNgan` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/SoiNgoNgan/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/SoiNgoNgan/frames.tres) |
| Tê Tê Vàng · `TeTeVang` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TeTeVang/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TeTeVang/frames.tres) |
| Thú Móng Lớn · `ThuMongLon` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuMongLon/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuMongLon/frames.tres) |
| Thú Răng Kiếm · `ThuRangKiem` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuRangKiem/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuRangKiem/frames.tres) |
| Ưng Đỏ · `UngDo` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/UngDo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/UngDo/frames.tres) |
| Dương Dương Dương · `DuongDuongDuong` | 2 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DuongDuongDuong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DuongDuongDuong/frames.tres) |
| Gấu Vết Dao · `GauVetDao` | 2 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/GauVetDao/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/GauVetDao/frames.tres) |
| Mực Hắc Ám · `MucHacAm` | 2 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MucHacAm/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MucHacAm/frames.tres) |
| Thiên Nga Cực Địa · `ThienNgaCucDia` | 2 | Thường | Công kích vật lý và phòng ngự khá cao, có nhiều kỹ năng tăng ích ‌  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThienNgaCucDia/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThienNgaCucDia/frames.tres) |
| Cáo Chín Đuôi · `CaoChinDuoi` | 3 | Thường | Poke trí tuệ trưởng thành cực tốt,poke ma pháp ,có kỹ năng nâng cao ngưỡng Mp  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/CaoChinDuoi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/CaoChinDuoi/frames.tres) |
| Rùa Nham Thạch · `RuaNhamThach` | 3 | Thường | HP và Phòng Ngự trưởng thành khá cao,Là poke vật lý ,có kĩ năng tăng ích nhóm.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RuaNhamThach/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RuaNhamThach/frames.tres) |
| Voi Tai To · `VoiTaiTo` | 3 | Thường | Công kích và HP trưởng thành khá cao ,là poke vật lý , cơ thể lớn cho cảm giác an toàn.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/VoiTaiTo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/VoiTaiTo/frames.tres) |
| Đại Tuyết Quái · `DaiTuyetQuai` | 4 | Thường | Poke có sức mạnh trưởng thành cao ,có hiệu quả làm mù, đồng thời có khả năng phản kích đối phương nhất định.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DaiTuyetQuai/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DaiTuyetQuai/frames.tres) |
| Gấu Trúc Ma Pháp · `GauTrucMaPhap` | 4 | Thường | Trí tuệ trưởng thành cao , Poke ma pháp sinh vật đến từ phương Đông cực ít trên Đại Lục.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/GauTrucMaPhap/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/GauTrucMaPhap/frames.tres) |
| Tinh Tinh Rock · `TinhTinhRock` | 4 | Thường | HP trưởng thành rất cao,poke vật lý có thể trói buộc đối phương  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TinhTinhRock/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TinhTinhRock/frames.tres) |
| Bạch Hổ · `BachHo` | 4 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BachHo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BachHo/frames.tres) |
| Người Tuyết Viễn Cổ · `NguoiTuyetVienCo` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NguoiTuyetVienCo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NguoiTuyetVienCo/frames.tres) |
| Sói Xích Viêm · `SoiXichViem` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/SoiXichViem/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/SoiXichViem/frames.tres) |
| Ngựa Bùn Cỏ · `NguaBunCo` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NguaBunCo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NguaBunCo/frames.tres) |
| Thú Vàng Một Sừng · `ThuVangMotSung` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuVangMotSung/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuVangMotSung/frames.tres) |

## Thực Vật / Plant

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Gỗ Quỷ · `GoQuy` | 1 | Thường | Nhỏ bé nhưng rất mạnh mẽ,Sức mạnh,Hp khá cao | [Ảnh](../../../../apps/game-client/assets/pets/apk84/GoQuy/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/GoQuy/frames.tres) |
| Hải Quỳ · `HaiQuy` | 1 | Thường | Sát thủ ẩn mình trong biển ,kỹ năng ,trí tuệ nhóm cao.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HaiQuy/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HaiQuy/frames.tres) |
| Nấm Hoa · `NamHoa` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NamHoa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NamHoa/frames.tres) |
| Quả Mặt Quỷ · `QuaMatQuy` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/QuaMatQuy/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/QuaMatQuy/frames.tres) |
| Tinh Tinh Xanh · `TinhTinhXanh` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TinhTinhXanh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TinhTinhXanh/frames.tres) |
| Xương Rồng · `XuongRong` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/XuongRong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/XuongRong/frames.tres) |
| Yêu Tinh Hoa · `YeuTinhHoa` | 1 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/YeuTinhHoa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/YeuTinhHoa/frames.tres) |
| Hoa Ăn Thịt Người · `HoaAnThitNguoi` | 2 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HoaAnThitNguoi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HoaAnThitNguoi/frames.tres) |
| Thủy Linh · `ThuyLinh` | 2 | Thường | Hp và phòng ngư trưởng thành khá cao ,là một poke ma pháp ,có kỹ năng nâng thuộc tính kháng ánh sáng và kỹ năng trị liệu cho nhóm.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuyLinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuyLinh/frames.tres) |
| Trúc Địa Linh · `TrucDiaLinh` | 2 | Thường | Một cây trúc ở các ngôi mộ , Trưởng thành cân bằng ,Là một Poke vật lý ,có khả năng phòng ngự vật lý và trị liệu cao.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TrucDiaLinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TrucDiaLinh/frames.tres) |
| Yêu Tinh Dứa · `YeuTinhDua` | 2 | Thường | Công kích vật lý và phòng ngự trưởng thành khá cao ,là poke vật lý ,có khả năng sát thương liên tục lên mục tiêu.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/YeuTinhDua/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/YeuTinhDua/frames.tres) |
| Bí Đỏ Quỷ Quái · `BiDoQuyQuai` | 3 | Thường |  Phòng Ngự trưởng thành cực tốt ,poke vật lý có khả năng kháng ánh sáng và cầm cố.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/BiDoQuyQuai/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/BiDoQuyQuai/frames.tres) |
| Hoa Hướng Dương · `HoaHuongDuong` | 3 | Thường |  Trí tuệ trưởng thành cực tốt , Poke ma pháp ,có kỹ năng sám hối và làm vỡ vỏ nhóm   | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HoaHuongDuong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HoaHuongDuong/frames.tres) |
| Hoa Môi · `HoaMoi` | 3 | Thường |  Sức Mạnh và phòng ngự trưởng thành khá cao , là một Poke vật lý , Có khả năng kháng chiêu thức vũ đạo.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HoaMoi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HoaMoi/frames.tres) |
| Hoa ăn Thịt Người Ba Đầu · `HoaAnThitNguoiBaDau` | 4 | Thường | Công kích và phòng ngự trưởng thành cao ,duy trì khả năng phòng ngự Hệ Thực vật , đồng thời có khả năng công kích vật lý cao.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HoaAnThitNguoiBaDau/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HoaAnThitNguoiBaDau/frames.tres) |
| Trưởng Lão Người Cây · `TruongLaoNguoiCay` | 4 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TruongLaoNguoiCay/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TruongLaoNguoiCay/frames.tres) |
| Độc Đằng Nữ · `DocDangNu` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/DocDangNu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/DocDangNu/frames.tres) |
| Tinh Linh Bách Hoa · `TinhLinhBachHoa` | 5 | Thường | Là một poke có thể nói là tinh linh của loài hoa ,Có phòng ngự trưởng thành Cao nhất , Sử dụng kỹ năng Ma Pháp Trị Liệu mạnh nhất cho nhóm.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TinhLinhBachHoa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TinhLinhBachHoa/frames.tres) |
| Cây Cự Linh · `CayCuLinh` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/CayCuLinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/CayCuLinh/frames.tres) |
| Linh Tiên Hoa Hương · `LinhTienHoaHuong` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/LinhTienHoaHuong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/LinhTienHoaHuong/frames.tres) |

## Bất Tử / Undead

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Chiến Sĩ Đầu Lâu · `ChienSiDauLau` | 1 | Thường | Hp và phòng ngự trưởng thành khá cao , là poke vật lý , có kỹ năng trị liệu cá thể. | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChienSiDauLau/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChienSiDauLau/frames.tres) |
| Chó Ác Ma  · `ChoAcMa` | 1 | Thường | Dù biến thành xác chết nhưng chúng vẫn háu chiến , Sức Mạnh công kích mạnh ,khả năng di chuyển nhanh.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ChoAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ChoAcMa/frames.tres) |
| Cua Hắc Ám · `CuaHacAm` | 1 | Thường | Hp và công kích vật lý trưởng thành khá cao là poke vật lý ,kháng tính khá nhiều. | [Ảnh](../../../../apps/game-client/assets/pets/apk84/CuaHacAm/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/CuaHacAm/frames.tres) |
| Nhện Vong Linh · `NhenVongLinh` | 1 | Thường | Công kích và phòng ngự cực tốt ,poke vật lý. | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NhenVongLinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NhenVongLinh/frames.tres) |
| U Linh · `ULinh` | 1 | Thường | Tri tuệ và hp trưởng thành cực tốt | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ULinh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ULinh/frames.tres) |
| Xác Chết Ác Ma · `XacChetAcMa` | 1 | Thường | Phòng ngự và Hp khá cao , nhưng tấn công và tốc độ lại thấp.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/XacChetAcMa/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/XacChetAcMa/frames.tres) |
| Xác Ướp · `XacUop` | 1 | Thường | Trí tuệ và phòng ngự trưởng thành khá cao, là Poke ma pháp ,kháng tính hỗn loạn của địch rất nổi bật .  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/XacUop/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/XacUop/frames.tres) |
| Cá Xương · `CaXuong` | 2 | Thường | Tấn công, phòng ngự , HP trưởng thành đều cao ,có kỹ năng công kích vật lý.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/CaXuong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/CaXuong/frames.tres) |
| Kẻ Đồ Tể · `KeDoTe` | 2 | Thường | Công kích và phòng ngự trưởng thành khá cao,Là poke vật lý .phản đòn là một trong những thủ đoạn tấn công của chúng  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/KeDoTe/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/KeDoTe/frames.tres) |
| Lửa Yêu · `LuaYeu` | 2 | Thường | Hp và trí tuệ trưởng thành cực tốt ,poke ma pháp , có kỹ năng trị liệu cá thể.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/LuaYeu/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/LuaYeu/frames.tres) |
| Xác Chết Vuốt Sắc · `XacChetVuotSac` | 2 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/XacChetVuotSac/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/XacChetVuotSac/frames.tres) |
| Ma Ảnh · `MaAnh` | 3 | Thường | Công kích trưởng thành cực tốt ,poke vật lý có kỹ năng làm sạch lời chú.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/MaAnh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/MaAnh/frames.tres) |
| Tinh Tinh Xanh Ma Giới · `TinhTinhXanhMaGioi` | 3 | Thường | Trí tuệ trưởng thành khá cao , là poke ma pháp , tấn công và bổ trợ đa diện. p | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TinhTinhXanhMaGioi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TinhTinhXanhMaGioi/frames.tres) |
| Xác Chết Nửa Người · `XacChetNuaNguoi` | 3 | Thường | Phòng Ngự và Hp trưởng thành khá cao , Là poke vật lý có khả năng cấm cố lời nguyền.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/XacChetNuaNguoi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/XacChetNuaNguoi/frames.tres) |
| Pharaon · `Pharaon` | 4 | Thường | Một kẻ sử dụng ma pháp bẩm sinh .Trí tuệ trưởng thành cực tốt ,poke ma pháp ,có kỹ năng làm đôi thủ hỗn loan.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/Pharaon/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/Pharaon/frames.tres) |
| Tử Thần · `TuThan` | 4 | Thường | Công kích trưởng thành cực tốt,là poke nắm giữ sự sống và cái chết của thế giới ,kỹ năng tốt nhất là giải trừ hoá thạch.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TuThan/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TuThan/frames.tres) |
| Nữ Vương Bạch Cốt · `NuVuongBachCot` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NuVuongBachCot/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NuVuongBachCot/frames.tres) |
| Rồng Xương Băng · `RongXuongBang` | 5 | Thường | Hp , tấn công , phòng ngự trưởng thành cân bằng , Poke vật lý ,có kỹ năng công kích vật lý mạnh nhất là đặc điểm của chúng.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongXuongBang/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongXuongBang/frames.tres) |
| Nữ Đế Minh Giới · `NuDeMinhGioi` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NuDeMinhGioi/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NuDeMinhGioi/frames.tres) |
| Thủ Lĩnh Hắc Ám · `ThuLinhHacAm` | 5 | Thần thú | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThuLinhHacAm/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThuLinhHacAm/frames.tres) |

## Rồng / Dragon

| Loài / ID | Sao | Loại | Mô tả nguyên bản | Asset |
|---|---:|---|---|---|
| Rắn Xương Trắng · `RanXuongTrang` | 1 | Thường | Có trí tuệ, Hp trưởng thành cao , phòng ngự khá cao . Điều này quyết định vị trí của chúng trên chiến trường.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RanXuongTrang/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RanXuongTrang/frames.tres) |
| Rồng Có Cánh · `RongCoCanh` | 1 | Thường | Có sức mạnh nhanh nhẹn trưởng thành cao ,là poke vật lý ,có kỹ năng tấn công nhanh khiến khả năng tự phòng thủ thấp.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongCoCanh/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongCoCanh/frames.tres) |
| Rồng Mào Đỏ · `RongMaoDo` | 1 | Thường | Rồng màu đỏ tự hào nhất là sức mạnh trưởng thành cao nhất , chúng súng bái sức mạnh tấn công , nên rất ít dùng đầu óc suy nghĩ vấn đề.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongMaoDo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongMaoDo/frames.tres) |
| Tiểu Ma Long · `TieuMaLong` | 1 | Thường | Trưởng thành cân bằng ,mọi loại đều biết , công kích vật lý vừa ma pháp ,còn trị liệu thì hơi biết.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/TieuMaLong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/TieuMaLong/frames.tres) |
| Giáp Long Răng Nhọn · `GiapLongRangNhon` | 2 | Thường | Tri tuệ phòng ngự tốt ,tăng cường kỹ năng công kích bản thân giúp chúng trở nên thiên chiến.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/GiapLongRangNhon/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/GiapLongRangNhon/frames.tres) |
| Nham Long · `NhamLong` | 2 | Thường | Tuy  có sức phong ngự và Hp trưởng thành cao , nhưng chúng thích sử dụng ma pháp tấn công địch , lúc rảnh rỗi chúng cũng học một ít ma pháp.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/NhamLong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/NhamLong/frames.tres) |
| Rồng Cổ Dài · `RongCoDai` | 2 | Thường | Hp trưởng thành cao , sức mạnh và phòng ngự trưởng thành tốt , có kỹ năng làm yếu , thường khiến đối thủ bị tấn công bất ngờ  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongCoDai/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongCoDai/frames.tres) |
| Rồng Vuốt Xương · `RongVuotXuong` | 2 | Thường | Rồng Vuốt Xương là sát thủ đích thực ,khả năng làm vỡ vỏ ,phản kích đều là kỹ năng khiến đối thủ đau đầu.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongVuotXuong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongVuotXuong/frames.tres) |
| Rồng Phỉ Thúy · `RongPhiThuy` | 3 | Thường | Độ Trưởng thành Hp cao , lực công kích bình thường nhưng có nhiều kỹ năng giảm năng lực kẻ thù.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongPhiThuy/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongPhiThuy/frames.tres) |
| Rồng Sấm · `RongSam` | 3 | Thường | Trí tuệ trưởng thành cao ,Thủ đoạn công kích ma pháp đa dạng khiến đối thủ đau đầu.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/RongSam/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/RongSam/frames.tres) |
| Viêm Long · `ViemLong` | 3 | Thường | Viêm Long sức mạnh trưởng thành cao đồng thời còn nhiều kỹ năng chiến đấu chi viện bổ trợ.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ViemLong/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ViemLong/frames.tres) |
| Hải Long Ba Đầu · `HaiLongBaDau` | 4 | Thường | Trí tuệ trưởng thành cao , kỹ năng ma pháp đa dạng , nhưng phòng ngự kém . Tuy vậy kỹ năng khống chế đa dạng hoàn toàn có thể đưa cuộc chiến theo hướng nó.  | [Ảnh](../../../../apps/game-client/assets/pets/apk84/HaiLongBaDau/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/HaiLongBaDau/frames.tres) |
| Long Vương Hắc Ám · `LongVuongHacAm` | 4 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/LongVuongHacAm/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/LongVuongHacAm/frames.tres) |
| Thánh Rồng Thái Cổ · `ThanhRongThaiCo` | 5 | Thường | Nguồn để trống | [Ảnh](../../../../apps/game-client/assets/pets/apk84/ThanhRongThaiCo/portrait.png) · [Animation](../../../../apps/game-client/assets/pets/apk84/ThanhRongThaiCo/frames.tres) |

## Kiểm chứng nguồn

Nguồn: `Spirit Beast World 8.4 (1).xapk`; SHA-256 `b8e02a75e49d5d02703a0b05ec52b450cdfaf69d544f04df2f4a2a465199a18e`. DataPoke ở `sharedassets0.assets:739`, 152 bản ghi/24.412 byte. Schema và enum được giải mã từ IL2CPP metadata v31. Tất cả portrait hợp lệ; 152 actor, 760 clip và 1.241 frame keyframe có thời điểm đổi frame giải mã trực tiếp.

Một typo prefab được ánh xạ có chủ đích: `QuaiVatNhamThach` → `QUAIVATNHAMTHAC`. Tên actor còn lại khớp duy nhất sau khi bỏ khác biệt chữ hoa/thường. Godot importer không sao chép các transition của Unity Animator.
