# P12 Stage 4 — Hướng dẫn chạy lại và đọc dữ liệu

Stage 4 (owner mở 2026-10-15) chỉ là **tài liệu và dữ liệu thiết kế**: không sửa runtime, game client hay nguồn APK. P12 vẫn OPEN. Thư mục này gồm thiết kế, các ma trận sinh tự động và script trích dữ liệu từ APK 3.2 (chỉ đọc).

## 1. Đọc gì trước

| File | Nội dung |
|---|---|
| [P12-S4-design.md](P12-S4-design.md) | Thiết kế chính: phạm vi 17 map, trụ teleport, cấp từng map, vùng an toàn và hồi sinh, quyết định của owner |
| [P12-S4-npc-roster.md](P12-S4-npc-roster.md) / `.json` | Roster đề xuất 106 NPC + 1 hòm thư trên 75 map (17 map phạm vi + 58 map của 11 vùng mở rộng) |
| [P12-S4-npc-matrix.md](P12-S4-npc-matrix.md) | 44 slot NPC gốc trong APK (vai trò gốc chỉ là suy đoán) |
| [P12-S4-portal-matrix.md](P12-S4-portal-matrix.md) / `portal-matrix.json` | 45 portal chạm phạm vi |
| `apk-extract/` | Dữ liệu thô trích từ APK: `npcs-raw.json`, `npcs.json` (đã lọc), `spawn-markers.json`, `map-scan.json` (quét 92 map) |

## 2. Yêu cầu

- Python 3.10 trở lên.
- Script trích APK cần `UnityPy==1.25.3` và `attrs>=23`:
  `python3 -m pip install "UnityPy==1.25.3" "attrs>=23"` (nên dùng venv). Repo đã có venv của `tools/assets` ở `tools/.cache/asset-venv` với UnityPy; dùng được nếu bạn muốn: `tools/.cache/asset-venv/bin/python <script>`.
- Nguồn **chỉ đọc** (không sửa, không copy vào repo):
  - `~/Downloads/Spirit Beast World 3.2.apk`
  - `~/Downloads/Phimond-P12-Review/normalized-code-registry.json` và `portal-geometry-draft.json` (đầu ra Stage 1, ngoài repo)

## 3. Chạy lại

Từ thư mục này (`.ai/plan/phases/P12-world/stage4`):

```bash
A="$HOME/Downloads/Spirit Beast World 3.2.apk"
R="$HOME/Downloads/Phimond-P12-Review"

# Trích từ APK (dùng python3 thường; không dùng -I vì sẽ ẩn gói cài ở user-site)
python3 apk-extract/02_extract_npcs.py "$A" "$R/portal-geometry-draft.json" apk-extract/npcs-raw.json   # ghi cả apk-extract/npcs.json (đã lọc)
python3 apk-extract/03_scan_all_maps.py "$A" "$R/portal-geometry-draft.json" apk-extract/map-scan.json
python3 apk-extract/04_extract_spawn_markers.py "$A" "$R/portal-geometry-draft.json" apk-extract/spawn-markers.json

# Sinh tài liệu và dữ liệu (không cần UnityPy)
python3 -I gen_portal_matrix.py "$R" .      # P12-S4-portal-matrix.md + portal-matrix.json
python3 -I gen_npc_matrix.py                # P12-S4-npc-matrix.md
python3 -I gen_npc_roster.py                # P12-S4-npc-roster.md + .json
```

Mỗi script trích APK mất khoảng nửa phút. Kết quả mong đợi khi chạy lại: `02` in 133 object trong AllNpc và lọc ra 44 NPC; `03` in 92 maps; `04` in 6 map; `gen_portal_matrix` in 45 portals; `gen_npc_roster` in 107 mục (106 NPC + hòm thư), 67 mới.

## 4. Sửa roster NPC

Dữ liệu thiết kế nằm ở `roster_data.py` (map, id, tên, hạng, vai trò, object nguồn hoặc `None` nếu NPC mới, ghi chú). Sửa file này rồi chạy lại `gen_npc_roster.py`. Script kiểm tra mọi slot NPC gốc đều được dùng (trừ 3 biến thể ẩn của người hướng dẫn ở Triệu Linh Điện và slot thừa ở Nông trại).

## 5. Giới hạn cần nhớ

- Script IL2CPP của game không có type tree nên **không đọc được tham số**: hội thoại, dịch vụ, danh tính và cấp quái không có trong dữ liệu.
- `TransEnemy` và điểm spawn đánh số là suy luận từ tên object. "0 quái" nghĩa là APK không có hai thứ đó trong map, chưa kiểm chứng bằng chạy game.
- Vai trò NPC gốc (`thaythuoc`, `TTTD`, `guild`…) chỉ là suy đoán từ tên prefab. Vai trò trong roster là thiết kế đề xuất.
- Tọa độ APK là đơn vị Unity của bản gốc, chỉ dùng làm bản phác; bản vẽ HD-2D và collision mới sẽ đặt lại.
- Chuỗi nhiệm vụ chính do phase quest quyết; bậc kỹ năng do P13; danh tính và cấp quái do P15/P10/P11.
