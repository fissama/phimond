# P19 — Hệ thống vật phẩm và hòm thư: scope (bản nháp để owner duyệt)

Ngày: 2026-11-05. Trạng thái: **DRAFT, chưa có code**. Nguồn yêu cầu: `PHIMOND_MASTER_SPEC.md` §P19 (R01–R06, R03a, R03b).

## 1. Hiện trạng trong repo (đã đối chiếu)

| Hạng mục | Hiện có | Thiếu so với P19 |
|---|---|---|
| Catalog | `data/items/items.json` (runtime): `capture_seal`, `potion`, `ether`, `synthesis_soul`, `blessing_leaf` với `kind/price/power`. `data/p10/items.json` chỉ là hồ sơ authoring (`authoring_only_not_runtime`, các trường `item_kind, effect, cost, stack_limit, binding, assets` còn unresolved) | Rarity, mô tả, icon, stack, binding, điều kiện dùng, EXP share, bản vẽ, trang bị |
| Inventory | `Character.Inventory map[string]int` trong blob `characters.state`; package `internal/inventory` chỉ là README | Capacity, stack, ownership theo instance, idempotency |
| Nguồn nhận | Mua ở shop (`shop.buy`), thưởng quest (`quest.claim`), khởi đầu cố định | Drop quái theo map/độ hiếm, event, admin grant |
| Nguồn tiêu | `item.use` (heal/mp ngoài trận), dùng trong trận, `capture_seal`, `synthesis_soul`/`blessing_leaf` ở dung hợp | Bán/bỏ, EXP share, công thức |
| Hòm thư | `internal/mail` chỉ là README "TBD" | Toàn bộ |
| Client | Túi/shop dựng trên 5 loại hiện có | Hiển thị rarity, stack, thư |

## 2. Phạm vi đề xuất

**P19a — Nền item (an toàn cho save hiện có)**
- Schema catalog v2 (id, tên, mô tả, icon, rarity, stack_limit, kind, effect, binding, sell_price). Giữ id cũ; `Inventory map[string]int` giữ nguyên định dạng để save của người chơi thật không phải chuyển đổi.
- Validator content: id duy nhất, tham chiếu hợp lệ, icon tồn tại.
- Capacity túi + hành vi khi đầy (chờ P19c).

**P19b — Nguồn/tiêu**
- Drop table theo quái/map/độ hiếm (data JSON); loại hẳn công thức 5★ khỏi mọi drop (R02).
- Bán/bỏ theo kind; log sinks/sources gold.
- `item.use` mở rộng bằng bảng effect thay vì `kind` cứng.

**P19c — Hòm thư hệ thống (R03a/R03b/R05)**
- Bảng `mail` (migration 004): người nhận, nguồn/lý do, phần đính kèm (item/pet snapshot), hạn, trạng thái nhận, khoá idempotency.
- Nhận đúng một lần, retry/reconnect không nhân đôi; túi/kho đầy thì thư giữ lại.
- Admin/event grant tối thiểu (cần back office, xem rủi ro).
- Không có thư giữa người chơi.

**P19d — EXP share (R04)**: chỉ thiết kế và chốt luật, hiện thực khi có P02/P15 (chưa có combat 1v3 thật).

**Ngoài scope P19:** trang bị (P14), bản vẽ/công thức 5★ (P20), auction (P08).

## 3. Quyết định cần owner chốt

1. Capacity túi: theo số loại, tổng số, hay không giới hạn ở bản đầu?
2. Binding mặc định: item nhận từ quái/shop có trade được không (trade chưa có tới P08)?
3. Hạn lưu thư: bao nhiêu ngày, hay vĩnh viễn ở bản đầu?
4. EXP share: item trang bị hay tiêu hao? (chỉ cần chọn hướng, chưa cần số)
5. Admin grant cần back office trước, hay làm công cụ CLI tối thiểu phía server?
6. Drop: có thêm item mới (nguyên liệu) hay chỉ dùng 5 loại hiện có ở P19b?

## 4. Rủi ro

- **Save người chơi thật**: không đổi dạng `Inventory`; thêm trường mới phải có mặc định đọc được từ blob cũ; có test nạp save v1.0.0.
- **Nhân đôi/mất đồ** ở thư và drop: mọi nhận thưởng đi qua một giao dịch + khoá idempotency; test retry.
- **Máy chủ Go chưa build được trong môi trường này**: kiểm thử server dựa vào CI/máy owner.
- **Back office chưa có**: admin grant thiếu giao diện, cần quyết định thứ tự.
- Số liệu catalog hiện là "reconstructed", cần P15 đo balance.

## 5. Thứ tự đề xuất

P19a → P19b → P19c; mỗi bước một commit nhỏ, ra cùng bản `1.0.z`/`1.1.0` khi sẵn sàng, không push khi chưa có lệnh.
