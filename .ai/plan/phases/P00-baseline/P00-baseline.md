# P00 baseline — 2026-09-23

Workspace không có `.git`; dùng source restore archive thay Git worktree trong lần này. Archive `evidence/source-before-p00.tgz` SHA256 `7280d081a5dc6eb27f92daeefba6e591729c7c52104726f23c7f20c2f33b85ed`, không chứa `.env`, asset nguồn hoặc caches Godot/Node. Restore vào folder riêng và diff trước khi chọn file; không giải nén đè toàn workspace hoặc restore DB bằng archive code.

Runtime: Go 1.27.0 darwin/arm64, Node v24.11.0, Godot 4.7.2; native OpenGL compatibility trên Apple M3 Pro. Logical viewport 960×640, window override 1152×768. Máy test/generator/server cùng local Mac; DB remote Aiven `phimond_reconstruction`. Server release vCPU/RAM/region chưa được chọn.

Entry: `apps/game-client/project.godot` → `scenes/LoginScreen.tscn`; autoload `PhimondClient.gd`; MainMap/BattleScene dùng `reference_game.gd`, `classic_hud.gd`, `room.gd`. `MainMap.gd`/`BattleScene.gd` cũ không là renderer active.

Commands từ project root:

```sh
rtk proxy sh tools/check.sh
rtk proxy sh tools/server.sh
rtk proxy apps/game-client/.tools/Godot.app/Contents/MacOS/Godot --path apps/game-client
```

Fast check gồm Go race/vet, Godot active offline checks, load-harness unit tests, web tests/typecheck. Override `GODOT_BIN` nếu runtime ở nơi khác. Live scripts tạo account và dùng MySQL, phải chạy riêng với `GAME_API_URL` trỏ test server đã xác minh DB.

Trong lượt này dùng server riêng 8091 (event bridge) và 8092 (thêm metrics), không restart phiên 8090 đang có. Không chạy migration hoặc đổi schema/ruleset.

Baseline `tools/check.sh`: Go race tests qua; vet fail tại bốn unkeyed `ActiveStatus/Buff` literals. Đã chuyển named fields, không đổi giá trị. Baseline fixture room dựa trên private history/events nên không được dùng làm live proof; đã thay public batches.

Tài khoản load: `p00_…`, manifest cạnh report chỉ chứa username/ID/profile, không credentials. Test UI cũ dùng `ref_…`/`contact_…`; không xóa hàng loạt theo prefix. Chưa chạy cleanup. Mọi account người dùng hiện có giữ nguyên.

Ảnh trong `evidence/screens/` là render fixture sau sửa, không bằng chứng progression hay screenshot before. Native ảnh `native-*.png` là test account thật. Baseline đầu phase còn dựa trên code + evidence lịch sử trong master; không tuyên bố đã làm playthrough trước mọi edit.
