# Kit `beach` — Bãi biển châu báu

> **Quy tắc bắt buộc cho Codex** (xem README.md): dùng https://github.com/0x0funky/agent-sprite-forge (generate2dmap / generate2dsprite) với route image_gen tích hợp; cấm codeart2d, API trả phí, vẽ bằng code, lật gương; không commit; không sửa tools/hd2d_audit/*, gate_waivers.json, check.sh; mỗi asset phải tự nhìn ảnh trước khi ghi "vẽ xong"; chỉ Claude/owner đánh dấu "duyệt".

- Style/palette: Cát ấm/cát lạnh, biển lam, san hô, cọ
- Thư mục asset: `apps/game-web/art-src/hd2d/batch-03-octopath/`
- Số map: 5

## 1. Trạng thái asset hiện có

Tổng 61 · duyệt 57 · nháp 4 · khác 0

| Loại | Có | Cần tối thiểu | Ghi chú |
|---|---|---|---|
| floor | 6 | 8 | ⬜ thiếu 2 · tile sàn 512×512 seamless, mỗi biến thể là texture khác |
| edge | 0 | 3 | ⬜ thiếu 3 · dải chuyển tiếp 512×128 liền hai đầu |
| prop | 28 | 36 | ⬜ thiếu 8 · prop đứng, ≥2–3 biến thể thật/chủng loại |
| decal | 8 | 12 | ⬜ thiếu 4 · decal tiếp đất bất quy tắc, mép mềm |
| shadow | 0 | 4 | ⬜ thiếu 4 · bóng procedural alpha mềm (ngoại lệ) |
| backdrop | 5 | 3 | ✅ · far/mid/near, lặp ngang liền |
| portal | 1 | 2 | ⬜ thiếu 1 · cặp dormant/active cùng mask |
| marker | 1 | 1 | ✅ · điểm xuất hiện 4 khung |
| fx | 6 | 3 | ✅ · hạt/tia sáng sprite sheet |

### Danh sách asset

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ✅ duyệt | `sea-islands-far` | backdrop_far | [32.0, 6.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sea-islands-far/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `coastal-cliff-mid` | backdrop_mid | [16.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coastal-cliff-mid/prompt.md) |
| ✅ | ✅ duyệt | `fisher-hut` | backdrop_mid | [3.921875, 3.40625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/fisher-hut/prompt.md) |
| ✅ | ✅ duyệt | `lighthouse` | backdrop_mid | [2.0625, 4.8125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/lighthouse/prompt.md) |
| ✅ | ✅ duyệt | `ship-hull-backdrop` | backdrop_mid | [8.0, 3.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/ship-hull-backdrop/prompt.md) |
| ✅ | ✅ duyệt | `shell-clam` | decal | [0.671875, 0.515625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-clam/prompt.md) |
| ✅ | ✅ duyệt | `shell-conch` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-conch/prompt.md) |
| ✅ | ✅ duyệt | `shell-scallop` | decal | [0.640625, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-scallop/prompt.md) |
| ✅ | ✅ duyệt | `shell-spiral` | decal | [0.578125, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-spiral/prompt.md) |
| ✅ | ✅ duyệt | `starfish-coral` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-coral/prompt.md) |
| ✅ | ✅ duyệt | `starfish-ochre` | decal | [0.703125, 0.59375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-ochre/prompt.md) |
| ✅ | ✅ duyệt | `target-ring` | decal | [0.703125, 0.484375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/target-ring/prompt.md) |
| ✅ | ✅ duyệt | `touch-ring` | decal | [0.78125, 0.484375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/touch-ring/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `deep-sea-floor-tile` | floor | [4.0, 4.0] | — |
| ✅ | ✅ duyệt | `sand-dry-cool` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-cool/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-dry-warm` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-warm/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-seagrass` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-seagrass/prompt.md) |
| ✅ | ✅ duyệt | `sand-wet` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-wet/prompt.md) |
| ✅ | ✅ duyệt | `ship-deck-tile` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/ship-deck-tile/prompt.md) |
| ✅ | ✅ duyệt | `exit-arrow-down` | fx | [0.671875, 0.625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/exit-arrow-down/prompt.md) |
| ✅ | ✅ duyệt | `exit-arrow-left` | fx | [0.734375, 0.625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/exit-arrow-left/prompt.md) |
| ✅ | ✅ duyệt | `exit-arrow-right` | fx | [0.7421875, 0.625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/exit-arrow-right/prompt.md) |
| ✅ | ✅ duyệt | `exit-arrow-up` | fx | [0.6796875, 0.625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/exit-arrow-up/prompt.md) |
| ✅ | ✅ duyệt | `shore-foam` | fx | [2.0, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-foam/prompt.md) |
| ✅ | ✅ duyệt | `undersea-bubbles` | fx | [1.0, 1.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/undersea-bubbles/prompt.md) |
| ✅ | ✅ duyệt | `quest-complete` | icon | [0.9921875, 0.671875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/quest-complete/prompt.md) |
| ✅ | ✅ duyệt | `quest-new` | icon | [0.84375, 0.671875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/quest-new/prompt.md) |
| ✅ | ✅ duyệt | `talk-mark` | icon | [0.4609375, 0.3125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/talk-mark/prompt.md) |
| ✅ | ✅ duyệt | `storm-lantern` | light | [0.6640625, 1.125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/storm-lantern/prompt.md) |
| ✅ | ✅ duyệt | `nest-marker` | marker | [0.765625, 0.625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/nest-marker/prompt.md) |
| ✅ | ✅ duyệt | `teleport-pillar-high` | portal | [2.3125, 1.609375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/teleport-pillar-high/prompt.md) |
| ✅ | ✅ duyệt | `cannon` | prop | [1.265625, 1.296875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/cannon/prompt.md) |
| ✅ | ✅ duyệt | `coral-brain` | prop | [1.21875, 0.90625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coral-brain/prompt.md) |
| ✅ | ✅ duyệt | `coral-branching` | prop | [1.46875, 1.296875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coral-branching/prompt.md) |
| ✅ | ✅ duyệt | `coral-tube` | prop | [1.171875, 1.296875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coral-tube/prompt.md) |
| ✅ | ✅ duyệt | `driftwood` | prop | [2.03125, 0.90625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/driftwood/prompt.md) |
| ✅ | ✅ duyệt | `drying-net-rack` | prop | [2.53125, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/drying-net-rack/prompt.md) |
| ✅ | ✅ duyệt | `fishing-boat-01` | prop | [3.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/fishing-boat-01/prompt.md) |
| ✅ | ✅ duyệt | `fishing-boat-02` | prop | [4.578125, 1.6875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/fishing-boat-02/prompt.md) |
| ✅ | ✅ duyệt | `helm-wheel` | prop | [1.4296875, 1.609375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/helm-wheel/prompt.md) |
| ✅ | ✅ duyệt | `kelp` | prop | [1.21875, 1.84375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/kelp/prompt.md) |
| ✅ | ✅ duyệt | `mast-trunk` | prop | [2.046875, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/mast-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-canopy` | prop | [3.703125, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-trunk` | prop | [1.5625, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-canopy` | prop | [3.609375, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-trunk` | prop | [1.8125, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-canopy` | prop | [2.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-trunk` | prop | [1.09375, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-trunk/prompt.md) |
| ✅ | ✅ duyệt | `pier-deck-section` | prop | [2.796875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/pier-deck-section/prompt.md) |
| ✅ | ✅ duyệt | `pier-post` | prop | [1.0, 1.84375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/pier-post/prompt.md) |
| ✅ | ✅ duyệt | `prosperity-treasure-chest` | prop | [1.84375, 1.6875] | — |
| ✅ | ✅ duyệt | `rope-coil` | prop | [0.671875, 0.6875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/rope-coil/prompt.md) |
| ✅ | ✅ duyệt | `rum-barrel` | prop | [1.234375, 1.15625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/rum-barrel/prompt.md) |
| ✅ | ✅ duyệt | `seagrass` | prop | [1.234375, 0.984375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/seagrass/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-large` | prop | [3.171875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-large/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-medium` | prop | [1.421875, 1.140625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-medium/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-small` | prop | [1.125, 0.75] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-small/prompt.md) |
| ✅ | ✅ duyệt | `treasure-chest-closed` | prop | [1.53125, 1.28125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/treasure-chest-closed/prompt.md) |
| ✅ | ✅ duyệt | `treasure-chest-open` | prop | [1.59375, 1.546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/treasure-chest-open/prompt.md) |
| ✅ | ✅ duyệt | `pirate-flag` | prop_sway | [1.3828125, 1.453125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/pirate-flag/prompt.md) |
| ✅ | ✅ duyệt | `sail-cloth` | prop_sway | [2.1796875, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-04-octopath/sail-cloth/prompt.md) |

## 2. Prompt sheet chung cho kit

```text
[Dán Master v2: .ai/design/gpt-redo/00-master-v2.md]
Dùng agent-sprite-forge ($generate2dmap cho tile/prop, $generate2dsprite cho prop/decal/FX/marker). Route ảnh: image_gen tích hợp của Codex (kiểm `route_media.py resolve --kind image`). KHÔNG codeart2d, KHÔNG API, KHÔNG vẽ bằng code.
Kit: Bãi biển châu báu (beach). Style: Cát ấm/cát lạnh, biển lam, san hô, cọ. Style anchor: batch-01-octopath/contact-sheet.png + 2 sprites.png linh thú.
Mỗi lần gọi: 1 sheet ~6 vật trên nền #FF00FF, bố trí 2×3/3×2, cách nhau ≥48 px, không chạm mép. Giữ raw-01.png byte-identical. Cắt/khử nền/pixel finish bằng script forge. 33–48 màu, alpha nhị phân, lề ≥8 px, 128 px = 1 đơn vị (far 64), người = 1.31 đơn vị (cỡ tối đa vật nhỏ: tools/hd2d_audit/size_check.py).
Mỗi asset: thư mục raw-01/final/prompt.md/review.md/qa.json trong apps/game-web/art-src/hd2d/batch-11-beach/<id>/. Tự nhìn 4× nền tối/caro. Xong: `python3 tools/hd2d_audit/art_gate.py batch-11-beach` = 0 lỗi, contact-sheet mới hơn manifest.
```

## 3. Từng map

### `treasure_beach_fishermen_beach` — Bến Ngư Châu

![treasure_beach_fishermen_beach](refs/treasure_beach_fishermen_beach.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/treasure_beach_fishermen_beach.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/treasure_beach_fishermen_beach.png`, 2248×835 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/10-15/BaiBienKhoBau.unity`, 25 sprite ghép; brief: chưa có
- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.

Asset chính cho map này (rút từ kit):

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ✅ duyệt | `fisher-hut` | backdrop_mid | [3.921875, 3.40625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/fisher-hut/prompt.md) |
| ✅ | ✅ duyệt | `shell-clam` | decal | [0.671875, 0.515625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-clam/prompt.md) |
| ✅ | ✅ duyệt | `shell-conch` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-conch/prompt.md) |
| ✅ | ✅ duyệt | `shell-scallop` | decal | [0.640625, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-scallop/prompt.md) |
| ✅ | ✅ duyệt | `shell-spiral` | decal | [0.578125, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-spiral/prompt.md) |
| ✅ | ✅ duyệt | `sand-dry-cool` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-cool/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-dry-warm` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-warm/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-seagrass` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-seagrass/prompt.md) |
| ✅ | ✅ duyệt | `sand-wet` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-wet/prompt.md) |
| ✅ | ✅ duyệt | `shore-foam` | fx | [2.0, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-foam/prompt.md) |
| ✅ | ✅ duyệt | `driftwood` | prop | [2.03125, 0.90625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/driftwood/prompt.md) |
| ✅ | ✅ duyệt | `drying-net-rack` | prop | [2.53125, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/drying-net-rack/prompt.md) |
| ✅ | ✅ duyệt | `fishing-boat-01` | prop | [3.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/fishing-boat-01/prompt.md) |
| ✅ | ✅ duyệt | `fishing-boat-02` | prop | [4.578125, 1.6875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/fishing-boat-02/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-canopy` | prop | [3.703125, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-trunk` | prop | [1.5625, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-canopy` | prop | [3.609375, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-trunk` | prop | [1.8125, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-canopy` | prop | [2.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-trunk` | prop | [1.09375, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-trunk/prompt.md) |
| ✅ | ✅ duyệt | `pier-deck-section` | prop | [2.796875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/pier-deck-section/prompt.md) |
| ✅ | ✅ duyệt | `pier-post` | prop | [1.0, 1.84375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/pier-post/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-large` | prop | [3.171875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-large/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-medium` | prop | [1.421875, 1.140625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-medium/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-small` | prop | [1.125, 0.75] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-small/prompt.md) |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map treasure_beach_fishermen_beach (Bến Ngư Châu), kit beach.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/treasure_beach_fishermen_beach.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `treasure_beach_east_beach` — Bờ Đông Ngọc Bích

![treasure_beach_east_beach](refs/treasure_beach_east_beach.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/treasure_beach_east_beach.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/treasure_beach_east_beach.png`, 2421×822 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/10-15/BaiBienKhoBau.unity`, 22 sprite ghép; brief: chưa có
- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.

Asset chính cho map này (rút từ kit):

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ⏳ nháp, chờ duyệt | `coastal-cliff-mid` | backdrop_mid | [16.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coastal-cliff-mid/prompt.md) |
| ✅ | ✅ duyệt | `lighthouse` | backdrop_mid | [2.0625, 4.8125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/lighthouse/prompt.md) |
| ✅ | ✅ duyệt | `shell-clam` | decal | [0.671875, 0.515625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-clam/prompt.md) |
| ✅ | ✅ duyệt | `shell-conch` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-conch/prompt.md) |
| ✅ | ✅ duyệt | `shell-scallop` | decal | [0.640625, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-scallop/prompt.md) |
| ✅ | ✅ duyệt | `shell-spiral` | decal | [0.578125, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-spiral/prompt.md) |
| ✅ | ✅ duyệt | `starfish-coral` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-coral/prompt.md) |
| ✅ | ✅ duyệt | `starfish-ochre` | decal | [0.703125, 0.59375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-ochre/prompt.md) |
| ✅ | ✅ duyệt | `sand-dry-cool` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-cool/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-dry-warm` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-warm/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-seagrass` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-seagrass/prompt.md) |
| ✅ | ✅ duyệt | `sand-wet` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-wet/prompt.md) |
| ✅ | ✅ duyệt | `shore-foam` | fx | [2.0, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-foam/prompt.md) |
| ✅ | ✅ duyệt | `driftwood` | prop | [2.03125, 0.90625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/driftwood/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-canopy` | prop | [3.703125, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-trunk` | prop | [1.5625, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-canopy` | prop | [3.609375, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-trunk` | prop | [1.8125, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-canopy` | prop | [2.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-trunk` | prop | [1.09375, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-trunk/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-large` | prop | [3.171875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-large/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-medium` | prop | [1.421875, 1.140625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-medium/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-small` | prop | [1.125, 0.75] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-small/prompt.md) |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map treasure_beach_east_beach (Bờ Đông Ngọc Bích), kit beach.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/treasure_beach_east_beach.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `treasure_beach_west_beach` — Bờ Tây Hoàng Sa

![treasure_beach_west_beach](refs/treasure_beach_west_beach.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/treasure_beach_west_beach.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/treasure_beach_west_beach.png`, 2248×835 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/10-15/BaiBienKhoBau.unity`, 25 sprite ghép; brief: chưa có
- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.

Asset chính cho map này (rút từ kit):

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ⏳ nháp, chờ duyệt | `coastal-cliff-mid` | backdrop_mid | [16.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coastal-cliff-mid/prompt.md) |
| ✅ | ✅ duyệt | `shell-clam` | decal | [0.671875, 0.515625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-clam/prompt.md) |
| ✅ | ✅ duyệt | `shell-conch` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-conch/prompt.md) |
| ✅ | ✅ duyệt | `shell-scallop` | decal | [0.640625, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-scallop/prompt.md) |
| ✅ | ✅ duyệt | `shell-spiral` | decal | [0.578125, 0.5546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shell-spiral/prompt.md) |
| ✅ | ✅ duyệt | `starfish-coral` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-coral/prompt.md) |
| ✅ | ✅ duyệt | `starfish-ochre` | decal | [0.703125, 0.59375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-ochre/prompt.md) |
| ✅ | ✅ duyệt | `sand-dry-cool` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-cool/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-dry-warm` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-warm/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-seagrass` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-seagrass/prompt.md) |
| ✅ | ✅ duyệt | `sand-wet` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-wet/prompt.md) |
| ✅ | ✅ duyệt | `shore-foam` | fx | [2.0, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-foam/prompt.md) |
| ✅ | ✅ duyệt | `driftwood` | prop | [2.03125, 0.90625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/driftwood/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-canopy` | prop | [3.703125, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-trunk` | prop | [1.5625, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-canopy` | prop | [3.609375, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-trunk` | prop | [1.8125, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-canopy` | prop | [2.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-trunk` | prop | [1.09375, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-trunk/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-large` | prop | [3.171875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-large/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-medium` | prop | [1.421875, 1.140625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-medium/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-small` | prop | [1.125, 0.75] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-small/prompt.md) |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map treasure_beach_west_beach (Bờ Tây Hoàng Sa), kit beach.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/treasure_beach_west_beach.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `treasure_beach_deep_sea` — Vực Hải Lam

![treasure_beach_deep_sea](refs/treasure_beach_deep_sea.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/treasure_beach_deep_sea.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/treasure_beach_deep_sea.png`, 2248×825 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/10-15/BaiBienKhoBau.unity`, 25 sprite ghép; brief: chưa có
- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.

Asset chính cho map này (rút từ kit):

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ✅ duyệt | `sea-islands-far` | backdrop_far | [32.0, 6.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sea-islands-far/prompt.md) |
| ✅ | ✅ duyệt | `starfish-coral` | decal | [0.6875, 0.6328125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/starfish-coral/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `deep-sea-floor-tile` | floor | [4.0, 4.0] | — |
| ✅ | ⏳ nháp, chờ duyệt | `sand-seagrass` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-seagrass/prompt.md) |
| ✅ | ✅ duyệt | `undersea-bubbles` | fx | [1.0, 1.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/undersea-bubbles/prompt.md) |
| ✅ | ✅ duyệt | `coral-brain` | prop | [1.21875, 0.90625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coral-brain/prompt.md) |
| ✅ | ✅ duyệt | `coral-branching` | prop | [1.46875, 1.296875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coral-branching/prompt.md) |
| ✅ | ✅ duyệt | `coral-tube` | prop | [1.171875, 1.296875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/coral-tube/prompt.md) |
| ✅ | ✅ duyệt | `kelp` | prop | [1.21875, 1.84375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/kelp/prompt.md) |
| ✅ | ✅ duyệt | `seagrass` | prop | [1.234375, 0.984375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/seagrass/prompt.md) |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map treasure_beach_deep_sea (Vực Hải Lam), kit beach.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/treasure_beach_deep_sea.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```

### `treasure_beach_prosperity_island` — Đảo Phú Quý

![treasure_beach_prosperity_island](refs/treasure_beach_prosperity_island.jpg)

- Ảnh gốc (đối chiếu): `.ai/design/map-checklists/refs/treasure_beach_prosperity_island.jpg` (bản đầy đủ: `~/Downloads/Phimond-P12-Review/map-images/treasure_beach_prosperity_island.png`, 2248×835 px, 100 px = 1 đơn vị APK)
- Nguồn APK: scene `Assets/Scenes/Map/10-15/BaiBienKhoBau.unity`, 25 sprite ghép; brief: chưa có
- Brief điểm neo: **chưa có** (thiếu bounds P12). Codex đối chiếu ảnh gốc bằng mắt; Claude bổ sung brief trước khi dựng layout.

Asset chính cho map này (rút từ kit):

| Vẽ | Duyệt | id | loại | kích thước (world) | prompt/nguồn |
|---|---|---|---|---|---|
| ✅ | ✅ duyệt | `lighthouse` | backdrop_mid | [2.0625, 4.8125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/lighthouse/prompt.md) |
| ✅ | ✅ duyệt | `sand-dry-cool` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-cool/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-dry-warm` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-dry-warm/prompt.md) |
| ✅ | ⏳ nháp, chờ duyệt | `sand-seagrass` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-seagrass/prompt.md) |
| ✅ | ✅ duyệt | `sand-wet` | floor | [4.0, 4.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/sand-wet/prompt.md) |
| ✅ | ✅ duyệt | `shore-foam` | fx | [2.0, 2.0] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-foam/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-canopy` | prop | [3.703125, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-01-trunk` | prop | [1.5625, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-01-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-canopy` | prop | [3.609375, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-02-trunk` | prop | [1.8125, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-02-trunk/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-canopy` | prop | [2.96875, 2.078125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-canopy/prompt.md) |
| ✅ | ✅ duyệt | `palm-03-trunk` | prop | [1.09375, 2.9375] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/palm-03-trunk/prompt.md) |
| ✅ | ✅ duyệt | `prosperity-treasure-chest` | prop | [1.84375, 1.6875] | — |
| ✅ | ✅ duyệt | `shore-rock-large` | prop | [3.171875, 1.53125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-large/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-medium` | prop | [1.421875, 1.140625] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-medium/prompt.md) |
| ✅ | ✅ duyệt | `shore-rock-small` | prop | [1.125, 0.75] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/shore-rock-small/prompt.md) |
| ✅ | ✅ duyệt | `treasure-chest-closed` | prop | [1.53125, 1.28125] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/treasure-chest-closed/prompt.md) |
| ✅ | ✅ duyệt | `treasure-chest-open` | prop | [1.59375, 1.546875] | [prompt.md](../../../apps/game-web/art-src/hd2d/batch-03-octopath/treasure-chest-open/prompt.md) |

Prompt cho Codex:

```text
Dùng agent-sprite-forge (generate2dmap + generate2dsprite, route image_gen). Map treasure_beach_prosperity_island (Đảo Phú Quý), kit beach.
Mở và đính kèm thật ảnh gốc .ai/design/map-checklists/refs/treasure_beach_prosperity_island.jpg vào image_gen cùng 2–3 ảnh style batch 00–09 sát loại + 2 anchor linh thú; ghi sha256.
Rà các hàng chưa ✅ trong bảng; vẽ theo sheet 6 vật; landmark riêng: nhìn ảnh gốc, ghi tên vật vào bảng rồi vẽ (không giả là recovered APK nếu là diễn giải).
Xong: cập nhật cột "Vẽ" (✅ chỉ khi đã nhìn final 4×), chạy art_gate cho kit, KHÔNG tự đặt "Duyệt".
```
