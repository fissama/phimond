# P00 reference ledger

Nguồn chính: video Pokezoo 4:33 theo [audit đầy đủ](../../../../docs/research/VIDEO_UI_AUDIT_2026-09-23.md). Timestamp kế thừa audit đã xem, không phải một lượt scrub mới. Người review hiện tại: Codex, đối chiếu render active. Nguồn blue/gold sustained client; không trộn montage brown HUD.

| Screen | Video | Mapping / evidence | Nhãn và gap |
|---|---|---|---|
| Login | Không thấy username/password | `evidence/screens/login.png`, source HUD frames | adapted; không nhận là login gốc |
| World | 00:39–01:05; 03:03–03:11 | `evidence/screens/world.png`, native-contact; reference/rooms + actors | reconstructed map topology; rừng còn seam/mảng màu P01/P05 |
| NPC | 01:13–01:16 | `evidence/screens/npc.png`, upper strip + compact options | observed layout, translated content reconstructed |
| Combat | 03:12–03:28 | `evidence/screens/battle.png`, native-battle/after-attack | observed command flow; current animation timing reconstructed |
| Pet | 01:50–02:12 | `evidence/screens/companions.png`, reference actors | observed visual family; domain/stat mapping P03 |
| Inventory | 01:39–01:47 | `evidence/screens/inventory.png` | observed 6×4 grid; capacity/equipment chưa hoàn thiện |
| Quest | 01:18–01:20 | `evidence/screens/quests.png` | observed panel structure; quest data reconstruction |
| Synthesis | Quảng cáo 00:25, không có full UI | `evidence/screens/ranch.png` | actual UI unknown; không suy chính xác từ quảng cáo |

Actor art contract: `apps/game-client/assets/reference/actors/`, `scripts/reference_art.gd` và các manifest source là chuẩn nhận diện hiện tại. `evidence/asset-hashes.txt` khóa bytes của actor/HUD/map manifests và assets curated. Không sửa source art trong P00. 10 mapped species; các species chưa map vẫn là debt, không lấy placeholder làm bằng chứng fidelity. Bộ ảnh `evidence/actors/` ghi trainer + 10 loài, từng action có frame đầu/giữa/lật hướng; `actor_design_audit.gd` dùng chính renderer source textures. Toàn bộ frame/timing/pivot theo từng loài vẫn cần audit P02, không suy atlas mẫu thành animation đã hoàn hảo.

Đồ họa hiện tại chỉ là POC. Cải thiện readability/animation/anchor được phép nhưng không đổi silhouette, tỷ lệ, bảng màu nhận diện hoặc phong cách raster nhân vật/quái vật. Nguồn APK3.2/8.4 cần giữ provenance riêng trong manifests hiện có.
