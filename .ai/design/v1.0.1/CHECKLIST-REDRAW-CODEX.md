# Checklist redraw cho codex (v1.0.0 → v1.0.1)

Cập nhật: 2026-10-23, sau khi duyệt lô `apps/game-web/art-src/hd2d/p01-release-art-20261023/` và rà tiền cảnh/hậu cảnh 5 map.
Quy cách ảnh, prompt mẫu, cách nạp: xem `ASSETS-REDRAW-v1.0.0.md` (mục "Quy ước chung").

## Cách dùng

Codex tích **ô "Đã vẽ"** khi bỏ file vào `delivery/` (kèm `.prompt.md`, `.qa.json`). Claude duyệt bằng mắt (ảnh động/ảnh phóng 4×, kiểm viền ma-gen-ta, chân, số khung) rồi tích **ô "Duyệt"**. Chỉ file đã duyệt mới được nạp vào `apps/client/public/`.

Ký hiệu: `[ ]` chưa · `[x]` xong · `[!]` có lỗi cần sửa (xem cột Ghi chú) · `[✗]` bị loại, vẽ lại.

## A. Chuyển động (ưu tiên 1: đang gây cảm giác "lướt")

| ID | Asset | Khung | Đã vẽ | Duyệt | Ghi chú |
|---|---|---|---|---|---|
| R01 | `player-male.run.png` | 8 | [x] | [✗] | Chân trụ vẫn nghiêng một bên ở cả hai nửa chu kỳ; có điểm ảnh rác khung 3, 7. Khung 1 và 5 phải là hai chân đối nhau. |
| R02 | `player-female.run.png` | 8 | [x] | [✗] | Như R01; điểm ảnh rác khung 2, 7, 8. |
| R03 | `player-male.run-down.png` | 8 | [x] | [✗] | Các khung gần như giống nhau, không thấy đổi chân. |
| R04 | `player-female.run-down.png` | 8 | [x] | [✗] | Như R03. |
| R05 | `player-male.run-up.png` | 8 | [x] | [✗] | Như R03. |
| R06 | `player-female.run-up.png` | 8 | [x] | [✗] | Như R03; chênh chiều cao thân > 6 px. |
| R07–R12 | `walker-{baker,elder,boy,girl,guard,traveller}.run.png` | 8 | [ ] | [ ] | Hiện 2 khung. Baker, elder đã có nguồn 8 tư thế nhưng còn lỗi nửa chu kỳ; chờ sửa R01. |
| R13–R24 | `walker-<tên>.run-down.png`, `.run-up.png` (×6) | 8 | [ ] | [ ] | Tối thiểu baker, boy, girl trước. |
| R25–R31 | Idle NPC: `npc-{summoner_mira,bia_free,bia_skill,sq_pillar,sq_skill,sq_exchange,sq_warehouse}.idle.png` | 4 | [x] | [x]* | *Duyệt có điều kiện: hình đẹp nhưng 4 khung gần như giống hệt, chỉ như thở rất nhẹ. Muốn sinh động hơn thì thêm đổi trọng tâm/vung tay ở khung 2–3. **Chưa nạp**: tool `sync_client_assets.py --merge` chưa xử lý ghi đè dải idle (việc của Claude). |

## B. Bố cục thành phố và hậu cảnh (mới, từ rà soát map)

Lý do: cổng vòm Hoàng Môn, ngõ và khe giữa các mặt tiền nhìn xuyên ra nền trống. Claude đã dựng tạm bằng code (tường hậu canvas, tường thành kéo giãn); các ảnh dưới đây thay phần tạm.

| ID | Asset | Kích thước | Đã vẽ | Duyệt | Ghi chú |
|---|---|---|---|---|---|
| R32 | `city-backwall-brick.png`: tường hậu phố, gạch sẫm, lặp ngang liền mạch, tối dần về chân | 512×384 | [ ] | [ ] | Nhìn thấy qua ngõ vòm và khe giữa nhà ở Quảng Trường. Nền đặc, không ma-gen-ta nếu lặp ngang. |
| R33 | `palace-gate-passage.png`: nhìn xuyên cổng vòm Hoàng Môn vào sân trong (bậc đá, ánh sáng cuối lối, tường tối hai bên) | 384×420 | [ ] | [ ] | Đặt sau lỗ vòm của `palace-gate`. Hiện lỗ vòm chỉ thấy bức tường phẳng. |
| R34 | `palace-wall-fill.png`: đoạn tường thành lặp liền mạch có lỗ châu mai và gờ đá, để lấp khe giữa các khối | 512×320 | [ ] | [ ] | Hiện kéo giãn `palace-wall-section` (méo). |
| R35 | `city-roofline-gate.png`: dải mái và tháp lâu đài xa phía sau tường Hoàng Môn | 2048×384 | [ ] | [ ] | Ở Hoàng Môn người chơi chỉ thấy tường; cần nóc/tháp phía sau để có chiều sâu. |
| R36 | `forest-exit-arch.png`: lối ra rừng đánh dấu rõ (hai thân cây nghiêng ôm lối, đường đất sáng hơn) | 384×384 | [ ] | [ ] | Cổng Rừng Sâu → Hoàng Môn bị tán cây lớn che. Có `forest-portal-arch` cũ nhưng không nổi. |
| R37 | `forest-fg-low-bush.png`: 3 biến thể bụi/dương xỉ thấp phía trước camera | 3×256×192 | [ ] | [ ] | Thay hàng cây lớn tiền cảnh (đã đổi bằng code thành bụi nhỏ). |

## C. Giao diện, chân dung, hiệu ứng, nền (lô codex 2026-10-23)

| ID | Asset | Đã vẽ | Duyệt | Ghi chú |
|---|---|---|---|---|
| R40–R44 | `battle-bg-{forest,deep_forest,gate,city,hall}.png` | [x] | [x] | Đã nằm trong `apps/client/public/battle/` (chưa commit). Chụp thử trận rừng đẹp. |
| R45 | Chân dung NPC 19 ảnh `portrait-*.png` | [x] | [x]* | *13 ảnh đã xem trên bảng tổng hợp đều đạt. 6 ảnh chưa xem được: `bia_free`, `gate_guild`, `sq_exchange`, `sq_mailbox`, `sq_skill`, `sq_warehouse` (không có trong bảng tổng hợp của codex), cần xem. |
| R46–R47 | `slot-male.png`, `slot-female.png` | [x] | [x] | Dùng cho màn Chọn nhân vật. |
| R48–R50 | `starter-{tien_chuong,sa_hat,xich_ung}.png` | [x] | [x] | |
| R51 | `fx-summon.png` (6 khung 192×384) | [x] | [x] | Thay hiệu ứng tạm bằng code khi vào sảnh. |
| R52 | `foe-ring.png` (4 khung) | [x] | [x] | |
| R53 | `fx-fire`, `fx-water`, `fx-earth` | [x] | [x] | |
| R54 | `fx-beast`, `fx-insect`, `fx-plant` | [x] | [!] | Một vài khung chỉ có mảnh vụn rời (khung 3–5), xem lại bằng ảnh động. Vẫn dùng được nếu bỏ khung rác. |
| R55 | `ui-bottombar`, `ui-chat`, `ui-menu`, `ui-objective` | [x] | [x] | |
| R56 | `ui-minimap.png` | [x] | [!] | Viền hồng ma-gen-ta còn sót bên trong khung; cần khử. |
| R57 | Gạch/đá/thảm: `city-border-curve`, `city-brick-cobble-edge`, `city-carpet-cap-{round,square}`, `city-plinth-round`, `city-stone-step-edge` | [x] | [x] | Chưa dùng trong map; sẽ gắn khi dựng lại Hoàng Môn đợt sau. |
| R58 | `path-transition-01…12` | [x] | [x] | Có chữ Y, ngã tư, đường cong. Chưa nạp. |

## D. Còn lại từ danh sách cũ (`GPT-REMAINING.md`)

| ID | Asset | Đã vẽ | Duyệt |
|---|---|---|---|
| R60 | Bóng tiếp xúc (tròn nhỏ/lớn, chữ nhật, dài theo tán) | [ ] | [ ] |
| R61 | Mảnh nối mặt tiền nhà (ngõ, ống máng, cột) | [ ] | [ ] |
| R62 | Khung thanh chỉ số có nhãn (HP/MP/EXP), tách nhãn khỏi thanh | [ ] | [ ] |

## Thứ tự đề nghị

1. R01–R06 (gốc của chuyện "lướt"), rồi R07–R24.
2. R33, R32, R34 (hậu cảnh thành phố), R35, R36.
3. Sửa R54, R56; xem 7 chân dung còn lại ở R45.
4. R37, R60–R62.
