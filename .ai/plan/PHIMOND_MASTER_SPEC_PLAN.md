# Phimond — Master Gameplay Spec & Phase Plan

**Ngày baseline:** 2026-09-23  
**Trạng thái:** Draft v5 — chốt training/combat và bổ sung items/công thức pet ngày 2026-09-23; để chia sprint; chưa phải implementation plan và chưa cấp phép tự triển khai toàn bộ roadmap.  
**Mục tiêu:** Phát triển bản reconstruction hiện tại thành một game nuôi linh thú có vòng chơi hoàn chỉnh, điều khiển rõ ràng, combat có phản hồi tốt và phong cách gần client gốc; đạt trải nghiệm online nhiều người chơi với tối thiểu 50 người chơi hoạt động đồng thời trên cấu hình triển khai được kiểm chứng.  
**Stack hiện tại:** Godot 4, Go, MySQL, Next.js companion.  
**Nguồn trình bày chính:** video Pokezoo 4:33 đã được người dùng xác nhận; APK 3.2/8.4 cung cấp asset nhưng có khác biệt phiên bản.

## 1. Cách sử dụng tài liệu

**Cập nhật thực thi 2026-09-23:** Đã triển khai nền tảng P00: public combat event/presentation, reconnect no-replay, validation, checks và metrics/load harness. Xem [P00 verification](phases/P00-baseline/P00-verification.md). Các nhận định baseline ban đầu bên dưới được giữ làm lịch sử; kết quả sửa và bằng chứng mới nằm trong báo cáo P00. Tải 10 account hoàn tất nhưng combat p95 1659ms vượt budget; chưa đạt gate online 50 CCU. Các phase sau vẫn cần lập/duyệt phạm vi trước triển khai.

Đây là tài liệu cấp sản phẩm và phase. Mỗi phase mô tả kết quả người chơi cần nhận được, phạm vi lớn, phụ thuộc và exit gate. Các sprint bên dưới chỉ là **cách chia đề xuất**, chưa chốt thời lượng, nhân lực hoặc giải pháp kỹ thuật.

Quy trình: **master spec → phase scope → sprint spec → sprint implementation plan → implement → verify → cập nhật evidence**.

- Mỗi sprint chọn một kết quả chơi được xuyên suốt client/server/data; tránh sprint chỉ “xong backend” nhưng chưa ai dùng được.
- Mỗi requirement có ID ổn định dạng `P02-R03`; sprint dẫn chiếu ID thay vì sao chép toàn bộ master plan.
- Mỗi sprint có implementation plan riêng sau khi khảo sát lại code ở thời điểm bắt đầu. Không coi tên file/hàm hiện tại là thiết kế bắt buộc vĩnh viễn.
- Chỉ đánh dấu phase hoàn thành khi exit gate có bằng chứng; số lượng file/code/test không thay thế kết quả gameplay.
- Thay đổi mục tiêu, economy, schema hoặc lịch sử game phải cập nhật decision log của sprint và master spec.
- Dùng [template sprint](SPRINT_SPEC_TEMPLATE.md) để tách việc. Không bắt đầu thực thi các phase chỉ vì tài liệu này đã được tạo.

## 2. Product contract

### Vòng chơi mục tiêu

Đăng nhập → hiểu nhiệm vụ đầu tiên → khám phá → gặp đúng quái → chiến đấu hoặc bắt → nhận kết quả rõ ràng → xem/đổi/hồi phục/huấn luyện pet → hoàn thành nhiệm vụ → mở vùng mới → luyện hai pet bố mẹ tới điều kiện cấp đã chốt → chọn dung hợp nâng sao hoặc dung hợp bổ trợ → nhận trứng theo nhánh đã chọn → ấp/nở → nhìn thấy con và phả hệ → tiếp tục xây đội mạnh hơn.

Một bản solo alpha được coi là có giá trị khi người chơi mới hoàn thành vòng trên qua UI thật, không cần chỉnh database, gọi lệnh debug hay người phát triển giải thích từng nút.

### Phạm vi bổ sung đã yêu cầu ngày 2026-09-23

- Thiết kế lại pet theo **8 hệ và 5 cấp sao (1★–5★) trước**. **Đã xác nhận:** 8 hệ tộc gắn với 8 hệ skill tương khắc; có một số skill dùng chung cho cả 8 hệ; mỗi hệ có nhánh skill vật lý và phép riêng. Tên/ánh xạ cụ thể và bảng tương tác chốt tại P10/P13.
- **Hai nhánh dung hợp:** (1) hai pet cùng sao lên đúng bậc sao tiếp theo khi có hình ảnh pet đầu ra, ít nhất một bố mẹ thuộc hệ tộc đầu ra; (2) dung hợp bổ trợ cho pet chính trở về trứng level 0, giữ pet chính và tăng cường chỉ số/độ cộng. Pet phụ trong nhánh bổ trợ cũng bắt buộc cùng sao; **cả hai nhánh tiêu cả hai pet, giữ bố mẹ trong phả hệ**; không tự mở 6★.
- **Ngưỡng dung hợp lv20** là đủ; luyện cấp cao hơn làm tăng chỉ số theo cấp của bố mẹ, từ đó tạo trứng có chỉ số tốt hơn so với bố mẹ chỉ vừa đạt ngưỡng, khi các yếu tố khác tương đương. Công thức kế thừa và ảnh hưởng riêng của từng bố mẹ chưa chốt.
- **Level cap gốc:** 1★ lv60, 2★ lv70, 3★ lv80, 4★ lv90, 5★ lv100. Pet có độ cộng từ +00 tới +99; cap hiệu lực = cap gốc theo sao + độ cộng, nên 5★ +99 đạt tối đa lv199. Độ cộng khác level hiện tại, sao và số thế hệ; **chỉ mở level cap, không trực tiếp cộng stat**. Cùng level và điều kiện so sánh phù hợp, bậc sao cao có nền chỉ số/tăng trưởng mạnh hơn; chênh level vẫn có ý nghĩa, ví dụ 1★ lv159 mạnh hơn 5★ lv1 về sức mạnh chỉ số, không phải cam kết thắng mọi matchup.
- Chuỗi `+00 với +00 → +03`, `+03 với +03 → +07` là **ví dụ brainstorm**, chưa phải công thức. Luật tăng + và cặp khác độ cộng còn cần thiết kế; **+99 không được cường hoá tiếp; nâng sao reset + về +00**. Không bắt buộc đạt +99 mới được nâng sao. Cả hai nhánh đều tạo trứng lv0, ấp nở thành pet lv1. **5★ +99 được đổi build nhưng không tăng chỉ số/cap**; đây là thao tác riêng, không mở lại cường hoá.
- **Mang tối đa 3 pet.** Pet nở lv1 phải luyện lại từ map level thấp; không thêm sân tập/cơ chế bù level riêng. Có vật phẩm chia EXP giữa pet mang theo, cho phép pet mạnh kéo pet yếu khi có item; không chia EXP miễn phí mặc định.
- **Combat đã chốt:** PvE solo pet đầu danh sách ra trận, chạm quái vào combat auto **1 pet vs 3 quái**; PvP **3 pet mỗi người đấu nhau**; party tối đa **3 người**, mỗi người góp **1 pet** khi đánh quái. Quyền đổi pet trong trận, bố trí/lượt PvP và số quái của encounter party cần phase sở hữu làm rõ; không lấy ba pet mang theo thành ba pet ra trận trong PvE solo.
- **Công thức pet:** vật phẩm có hình pet, dùng một lần để học công thức dùng lâu dài cho dung hợp/cường hoá. Độ hiếm theo sao; công thức 1★–4★ có nguồn rơi từ quái, 5★ **chỉ từ sự kiện hoặc admin gửi**, không rơi từ quái. Tách công thức đã học khỏi pet/vật liệu/chi phí phải tiêu mỗi lần dung hợp.
- Có phase riêng cho chỉ số; skill pet/quái và tương tác tăng cường/khắc chế/triệt tiêu; trang bị pet; map và liên kết; level quái theo map phục vụ luyện pet/max cấp; trang trại riêng từng tài khoản.
- Viết **một tuyến truyện chính gắn với map sau khi hoàn thiện các hệ thống trong phạm vi phát hành**; truyện phụ bổ sung sau. Trước đó chỉ giữ hook/ID quest và mục đích của vùng để tránh sửa topology, chưa viết cốt truyện chi tiết.
- Đây là cập nhật phase, outcome, dependency và exit gate. Chưa chọn bảng hệ, công thức chỉ số/XP/kế thừa/độ cộng, danh sách skill/trang bị, bản đồ cụ thể, nội dung truyện hoặc implementation của bất kỳ phase nào.
- Yêu cầu mới là định hướng sản phẩm ưu tiên khi khác reconstruction cũ; không coi đó là bằng chứng lịch sử. Code/data/save hiện tại giữ nguyên tới khi phase sở hữu có spec và phương án chuyển đổi.

### Nguyên tắc không thương lượng

1. Server quyết định vị trí hợp lệ, ownership, RNG, battle, chi phí, capture, progression và rewards. Client dự đoán chuyển động và trình bày kết quả; không tự tính kết quả gameplay.
2. Gameplay nằm trong Godot. Next.js phục vụ tài khoản, bách khoa, planner, journal/phả hệ; không tạo HUD gameplay thứ hai.
3. Video quyết định bố cục và flow khi có bằng chứng rõ. Giữ world viewport cố định, HUD ổn định, panel compact, raster/9-slice đúng tỷ lệ; không chuyển thành dashboard hoặc mobile gacha hiện đại.
4. Mỗi chi tiết fidelity có nhãn: **observed / inferred / reconstructed / unknown**. Không dùng “100%” hoặc % fidelity nếu chưa có thước đo và dữ liệu đủ.
5. Không đổi công thức gameplay chỉ để UI dễ triển khai. Chọn/chuyển ruleset là quyết định riêng, có kiểm thử và kế hoạch giữ save.
6. Chỉ dùng database riêng `phimond_reconstruction` và môi trường test được định danh. Không đụng schema/dữ liệu cũ `philandz`.
7. Các thao tác tiêu thụ pet/tài nguyên phải trình bày rõ điều kiện, đối tượng và hậu quả. Retry/reconnect không được double-spend hoặc nhận thưởng hai lần.
8. Chưa đưa real-money, thanh toán, quảng cáo hay auto-grinding không giám sát vào phạm vi mặc định.

### Chất lượng hình ảnh và thiết kế nhân vật/quái vật

**Quyết định của chủ dự án:** Đồ họa hiện tại chỉ được chấp nhận ở mức **POC**, chưa phải chất lượng cuối cùng để đưa tới player. Không dùng ảnh baseline hiện tại làm mức trần chất lượng hoặc bằng chứng đã đạt release.

**Giữ nguyên lối thiết kế đồ họa nhân vật và quái vật hiện tại:** silhouette, tỷ lệ cơ thể, nét tạo hình, bảng màu nhận diện và phong cách sprite/raster. Được hoàn thiện frame, animation, pivot, hướng nhìn, độ rõ, ánh sáng/hiệu ứng và độ nhất quán; không tự đổi sang realistic, 3D, chibi khác tỷ lệ hoặc vẽ lại làm mất nhận diện. Mọi đề xuất đổi art direction phải thành quyết định riêng của chủ dự án trước khi triển khai. Lưu bộ ảnh chuẩn của nhân vật/quái vật hiện tại tại P00 để so sánh xuyên các phase.

HUD, map, typography, icon, VFX, audio và chuyển cảnh cần tiếp tục hoàn thiện thành một trải nghiệm nhất quán. Polish không chỉ là trang trí: phải giúp đọc tình huống, chọn hành động và hiểu kết quả tốt hơn, đồng thời đáp ứng frame-time budget. P05 là mốc solo alpha được polish để chơi thử; P09 mới xét chất lượng cuối của bản phát hành đã chọn phạm vi.

### Online multiplayer và mục tiêu 50 CCU

**Yêu cầu sản phẩm đã chốt:** Phimond là game online nhiều người chơi. Bản phát hành phải phục vụ **ít nhất 50 người chơi hoạt động đồng thời (50 CCU)** trên một môi trường server/database được ghi rõ; không tính 50 socket đứng yên là đạt tải. Solo alpha chỉ là milestone kiểm chứng core loop, không thay thế mục tiêu multiplayer. P06 và gate 50 CCU là bắt buộc trước release; party/PvP cơ bản P07 đã được chọn, meta mở rộng P08 vẫn tùy nhánh.

Tối ưu xuyên suốt các phase: input/interpolation và render phía client; xử lý intent, broadcast/interest range và hàng đợi phía server; query/transaction/pool/checkpoint phía MySQL. Đo riêng client frame time, RTT, server receive→response-ready (bao gồm chờ queue/DB), thời gian commit và độ trễ cập nhật remote actor. Không giải quyết lag bằng cách bỏ validation, mất update bền vững hoặc thay đổi thiết kế nhân vật/quái vật.

**Ngân sách hiệu năng đề xuất để khóa tại P00:** 50 CCU, RTT ≤150ms, jitter ≤30ms, không chủ động gây mất mạng: server intent p95 ≤50ms/p99 ≤100ms; client send→authoritative ack p95 ≤250ms/p99 ≤400ms; remote movement state age p95 ≤250ms. Lệnh bị từ chối đúng luật không tính là lỗi hệ thống; timeout/lỗi nội bộ <0.1% request hợp lệ, không mất/nhân reward, pet hoặc tài nguyên. Input preview và frame pacing tuân thủ mục 7, kể cả có 50 actor trong cùng map. Các số này là acceptance dự kiến, **chưa phải kết quả đo hoặc cam kết không lag trên mọi mạng**; thay đổi budget phải ghi quyết định, không hạ gate chỉ để test qua.

**Bộ kiểm thử tải bắt buộc:**

- Ramp 1→10→25→50 account độc lập, đúng public protocol và cadence hợp lệ; soak 50 CCU ít nhất 2 giờ sau warmup. Lưu workload/script/seed, build, catalog, máy client, vCPU/RAM, region, cấu hình DB/pool và RTT. Load generator chạy riêng để không tranh CPU với server; ghi cả achieved request rate và số action/account/phút để phát hiện bot bị đứng.
- Chạy hai profile riêng: 50 người cùng map di chuyển/tương tác gây fan-out; và hỗn hợp 20 khám phá, 20 combat riêng, 10 thao tác pet/shop/quest. Bổ sung 50 trận PvE 1 pet vs 3 quái đồng thời để đo battle/persistence; profile party tối đa 3 người và PvP 3v3 phải bổ sung khi nghiệm thu P07. Dữ liệu tải 1v1 cũ chỉ là baseline lịch sử. Không chỉ benchmark API health hoặc idle connections.
- Cho 10/50 người reconnect trong khi 40 người còn lại chơi; kiểm tra retry/duplicate, đổi map đồng thời và slow consumer. Với RTT 300ms/jitter/mất kết nối, đánh giá phục hồi và tính đúng đắn riêng, không áp SLA của mạng ≤150ms.
- Stress 75 CCU ít nhất 15 phút để đo headroom và hành vi quá tải; chưa cam kết SLA 75 CCU. Có queue giới hạn, backpressure/rate limit và reconnect backoff; không để client chậm chặn cả map, DB pool cạn vô hạn hoặc broadcast không giới hạn.
- Theo dõi CPU/RAM/GC, queue depth, DB pool wait/slow queries/locks, commit/checkpoint lag, bytes/sec và fan-out. Mục tiêu headroom ở 50 CCU: CPU trung bình ≤70%, RAM đỉnh ≤80% giới hạn, không có queue/checkpoint backlog hoặc memory tăng không hồi phục trong soak. Đo overhead profiling riêng nếu có.
- Chạy client Godot thật trong khi load bots hoạt động để capture frame time và chơi world→combat→result→pet; bot pass không thay thế playtest cảm giác mượt. Review game design về mật độ quái, tranh encounter, chờ đợi và độ rõ màn hình đông người, đồng thời bảo toàn tạo hình nhân vật/quái vật.

Report tải thuộc evidence P06/P09, có percentile theo từng loại action/profile (không gộp che slow mutation), lỗi, tài nguyên, findings, tuning trước/sau và cách chạy lại. Chưa chốt cấu hình server/DB và chưa có report đạt thì chưa được ghi “hỗ trợ 50 CCU”.

### Review gameplay và game design bắt buộc ở mọi phase

Mỗi phase có requirement review riêng bên dưới, bao gồm ba task phải đưa vào sprint backlog:

1. **Đầu phase:** chơi lại flow liên quan và vòng chơi đã có; ghi friction, giả thuyết thiết kế, mục tiêu trải nghiệm và chỉ số cần đo trước khi sửa. Phân biệt lỗi triển khai với lựa chọn thiết kế chưa tốt và chi tiết nguồn chưa xác minh.
2. **Trong phase:** playtest sau mỗi lát cắt chơi được; review điều khiển, mức rõ ràng, lựa chọn có ý nghĩa, độ khó, nhịp độ, công sức/phần thưởng và đường phục hồi. Đề xuất tuning dựa trên quan sát; ghi rõ thay đổi mechanics nào cần quyết định ruleset. Tối ưu gameplay là cải thiện trải nghiệm và vòng chơi, không chỉ FPS/latency.
3. **Cuối phase:** chơi lại flow của phase cùng core loop bị ảnh hưởng; so sánh trước/sau, review game design và hình ảnh, kiểm tra giữ nguyên thiết kế nhân vật/quái vật. Kết luận **giữ / chỉnh / hoãn** cho từng finding, có lý do và evidence. Finding chặn outcome/exit gate phải được xử lý và chơi lại trước khi đóng phase; phần hoãn phải có owner, phase/sprint đích và lý do chấp nhận.

Deliverable: `Pxx-gameplay-gamedesign-review.md` trong folder của phase, dẫn chiếu build, scenario, người chơi/reviewer, capture/log, số đo, phản hồi định tính, quyết định tuning và task tiếp theo. Không coi test kỹ thuật qua hoặc danh sách feature hoàn thành là thay thế review. Phase không được đóng khi thiếu report và kết luận design review; phase không chọn triển khai được ghi rõ skipped cùng lý do, không đánh dấu verified.

## 3. Review baseline hiện tại

Review này gồm đọc code/data đang active, đối chiếu video audit và bằng chứng chơi thật của các lượt trước. **Không chạy lại toàn bộ game hoặc benchmark mới trong lượt lập kế hoạch này.** “Đã có” không đồng nghĩa “đã hoàn thiện”.

| Hệ thống | Trạng thái có bằng chứng | Khoảng trống cần xử lý | Phase chính |
|---|---|---|---|
| Account/session | Register/login, WS, reconnect và MySQL đã được thử thật | Trải nghiệm logout/đổi tài khoản, lỗi kết nối, phục hồi phiên và build cài đặt còn cần review đầy đủ | P00, P05, P09 |
| Di chuyển | X/Y, bốn hướng, preview/reconcile, cadence đã sửa | Chưa có walkable/collision map; đường đi tới mục tiêu đơn giản; NPC/portal server còn xét X | P01 |
| Gặp quái | Contact theo `wild_spawns`, đúng species, kiểm tra proximity, chống đứng yên tái kích hoạt | Vị trí sinh ra từ công thức; chưa có spawn lifecycle hay population dùng chung | P01, P06 |
| Combat | Một pet vs một enemy, attack/skill/item/defend/capture/auto/flee, giữ battle khi reconnect | Event presentation không nối đúng wire; result flow, status/target UX, timing cần làm chắc | P00, P02 |
| Sprite hướng | Đã sửa nhìn vào tâm và giữ anchor khi lật; đã xem render fixture | Chưa kiểm tra mọi loài/action/pivot trong live combat | P02, P05 |
| Pet | Instance, quality/growth/resistance, appraise, activate, learn, release có domain | UI chưa biểu diễn đủ dữ liệu thật; cần thiết kế lại hệ/sao/stat và quản lý trang bị | P10, P11, P14, P03 |
| Synthesis/strengthen | Rules, costs, retired parents, inheritance, lineage có backend; UI có chọn và xác nhận | Chưa có vòng cùng sao → trứng → nở theo yêu cầu mới; chưa chứng minh pacing từ account sạch | P16, P15, P03, P04 |
| Inventory/shop | Count, purchase, battle consumables, grid 6×4 | Chưa có bag capacity/equipment/storage thực; icon mapping và ngữ nghĩa số lượng còn thiếu | P03 |
| Quest/progression | Bốn quest, arena I, beach gate | Thiếu world graph/level vùng đầy đủ, nhịp luyện hai bố mẹ và tuyến truyện chính | P12, P15, P04, P17 |
| Visual/audio | Source HUD/panels, 5 map composites, 10 loài có source mapping | Cảnh rừng còn mảng ghép/layer thiếu tự nhiên; 4 loài chưa map art; icon, VFX, audio, font cần đối chiếu | P01–P05 |
| Multiplayer | Account qua server và persistence đã có | Chưa có presence, party, friends/chat/guild/PvP hoạt động; package tên tương ứng chủ yếu là scaffold | P06–P08 |
| Companion web | Encyclopedia, recipes, journal/lineage từng có bằng chứng integration | Chưa tái kiểm tra sau các lần refactor gần đây; phải đồng bộ catalog/API version | P03, P05 |
| Release/ops | Local server, tests và migration riêng | Chưa đạt production MMO: load/soak, restore, observability, rollout, đóng gói | P09 |

**Catalog kiểm đếm hiện tại:** 14 species, 29 skills, 6 recipes, 5 maps, 4 quests, 5 items. Số lượng này chỉ mô tả vertical slice, không phải mục tiêu hoàn thiện bản gốc.

### Findings ưu tiên từ code hiện tại

| ID | Finding và bằng chứng | Hậu quả / hướng xử lý |
|---|---|---|
| F01 — cao | `transport/server.go` gửi `data.events`; `character/engine.go::Snapshot` loại `battle.events`; `PhimondClient.gd` phát `events_received`, nhưng `reference_game.gd` chưa nối signal này vào renderer, còn `room.gd` đọc `next.events` | HP/log có thể đúng trong khi hit/VFX/floating numbers không chạy ở live. P00 sửa contract/integration; P02 làm presentation. Không coi fixture có `battle.events` là bằng chứng live. |
| F02 — cao | `room.gd` đọc `character.history`; domain lưu `battle_history` và public snapshot loại trường đó | Không dựa vào history trong snapshot để giữ animation/result cuối trận. Cần battle-completed presentation payload hoặc trạng thái kết thúc cục bộ từ event hợp lệ. Không lộ RNG/pet internals để chữa lỗi UI. |
| F03 — cao | `apply.go` và `helpers.go` dùng khoảng cách X cho NPC/portal; client dùng X/Y; contact quái đã kiểm tra cả hai trục | Flow “đứng xa vẫn giao dịch” hoặc “client nghĩ gần nhưng server khác” không nhất quán. P01 thống nhất tọa độ/proximity và save compatibility. |
| F04 — vừa | Pet UI tìm một số field như `strength/vitality/agility/intelligence` trực tiếp trên pet; domain có quality/growth và bộ derived stats riêng | Thiếu chỉ số hoặc nhãn gây hiểu nhầm. P03 lập mapping schema→label→nguồn; không bịa số để lấp UI. |
| F05 — vừa | `reference_art.gd` crop map bằng số cố định, trim từng frame, duration phân đều; một số evolved species không có mapping | Layer/pivot/camera/animation và pet không có hình là fidelity gap. P01/P02/P05 xử lý bằng manifest và reference. |
| F06 — vừa | UI combat chọn mục tiêu nhưng intent hiện chỉ có choice/skill/item; server combat hard-code một đối thủ | Baseline lịch sử chỉ hợp lệ 1v1. P02 cần contract actor/target và validation cho PvE 1v3; P07 tiếp tục cho party/PvP nhiều owner. |
| F07 — vừa | `docs/STATUS.md`, `GAMEPLAY.md`, README cũ còn mô tả horizontal-only, procedural art hoặc đường dẫn `internal/game`; có nhiều script client cũ | P00 chuẩn hóa đường chạy/checks/docs và lưu trữ legacy rõ ràng. Tên package không chứng minh feature đã có. Workspace hiện không có `.git`. |

Các finding trên là review kỹ thuật; không sửa production code trong lượt viết master plan này.

## 4. Kiến trúc và khu vực thay đổi

| Khu vực hiện có | Trách nhiệm giữ lại | Lưu ý khi chia sprint |
|---|---|---|
| `apps/game-client/scripts/reference_game.gd` | Flow UI, input, navigation, intent dispatch | Tách controller theo nhu cầu của sprint; tránh thêm toàn bộ MMO vào một file |
| `classic_hud.gd`, `reference_menus.gd`, `styles/` | Source visual components và menu dữ liệu | Một theme/token/layout source; acceptance bằng screenshot lẫn interaction |
| `room.gd`, `reference_art.gd`, `assets/reference/` | World/combat render, sprite/cache | Tách world model, animation/event playback khi P01/P02 cần; giữ anchor và asset provenance |
| `PhimondClient.gd`, `packages/protocol/` | Auth, snapshot/events, request lifecycle | Version contract; idempotency; kết quả cuối và lỗi thuộc request nào phải rõ |
| `apps/game-server/internal/character/` | Aggregate/Engine và gameplay hiện tại | Chỉ extract domain khi một feature cần ranh giới rõ; không rewrite toàn bộ trước khi sửa gameplay |
| `content/`, `data/` | Catalog, rules và validation | Stable IDs; provenance/version; validate cross references; kế hoạch giữ save khi đổi catalog |
| `transport/`, `persistence/`, `migrations/` | Server authority, transaction, checkpoint, recovery | Giữ phân biệt movement tạm thời và durable action; multi-character transaction là thiết kế mới ở P08 |
| `apps/web/` | Companion/read views | Không là lối tắt bắt buộc để hoàn thành core loop trong Godot |

## 5. Roadmap và phụ thuộc

**ID là định danh ổn định, không phải thứ tự thực hiện.** Giữ P00–P18 và requirement IDs đã có; thêm P19 (items), P20 (công thức pet). Bảng và mô tả phase cùng thứ tự; không đổi hồ sơ/evidence P00 hay coi roadmap đã triển khai.

| Thứ tự | Phase | Kết quả lớn | Phụ thuộc trước exit | Milestone |
|---|---|---|---|---|
| 1 | P00 | Baseline và integration đáng tin | Không | Nền kiểm chứng |
| 2 | P10 | Pet, 8 hệ tộc, sao, level và 3 slot mang theo | P00 | Pet design baseline |
| 3 | P11 | Chỉ số, tăng trưởng và kế thừa | P10 | Stat design baseline |
| 4 | P12 | World graph, loại map, quái/NPC và farm riêng | P10 | World design baseline |
| 5 | P01 | Di chuyển, collision, portal, encounter lifecycle | P00, P12 | World slice |
| 6 | P13 | Skill pet/quái và tương tác giữa các hệ | P10, P11 | Combat rules design |
| 7 | P19 | Hệ thống items, nguồn nhận/dùng và EXP share | P10, P11, P12, P13 | Item foundation |
| 8 | P02 | PvE auto: pet đầu vs 3 quái | P01, P11, P13, P19 | Core combat |
| 9 | P14 | Trang bị pet và ngân sách sức mạnh | P11, P13, P19, P02 | Equipment loop |
| 10 | P15 | Level vùng, luyện lại từ đầu, EXP share bằng item | P12, P02, P14, P19 | Training progression |
| 11 | P20 | Bản vẽ pet, học công thức lâu dài, nguồn 1★–5★ | P10, P12, P19, P15 | Recipe progression |
| 12 | P03 | Quản lý 3 pet, inventory, appraisal và chuẩn bị bố mẹ | P10, P11, P13, P14, P15, P19, P20 | Pet management |
| 13 | P16 | Farm, dung hợp/cường hoá theo công thức, ấp/nở | P01, P03, P10, P12, P15, P20 | Breeding loop |
| 14 | P04 | Onboarding, quest và cân bằng core loop | P01, P02, P03, P15, P16, P20 | Full solo loop |
| 15 | P05 | Fidelity, UX, đóng gói và solo playtest | P04; tích hợp P10–P16, P19, P20 | **M1: Solo alpha** |
| 16 | P06 | Shared world, social nền tảng và 50 CCU | P01, P05, P12, P16 | Online world alpha |
| 17 | P07 | Party tối đa 3 người và PvP 3 pet mỗi bên | P02, P03, P06, P13, P19 | **M2: Co-op/PvP cơ bản**, đã chọn |
| 18 | P08 | Economy liên người chơi và meta theo nhánh | P03, P06, P14, P16, P19, P20; ranking cần P07 | **M3: Extended MMO**, tùy chọn |
| 19 | P17 | Một cốt truyện chính xuyên các map | P04, P05, P06, P07; P08 nếu thuộc release | Main campaign |
| 20 | P09 | Kiểm định build có truyện chính và vận hành | P05, P06, P07, P17 + nhánh release đã chọn | **M4: Release candidate** |
| 21 | P18 | Truyện phụ và mở rộng thế giới | P17, baseline phát hành P09 | Content expansion |

P19 đặt trước combat/trang bị/training để chốt item dùng và EXP share. P20 dùng nền item, hệ pet và nguồn vùng đã thiết kế, đặt trước P03/P16 để có flow học công thức trước dung hợp. Bản vẽ/hình pet và asset đích phải được đối chiếu từ P20, không đợi P05 mới phát hiện không thể nâng sao.

P02 chịu trách nhiệm multi-target PvE 1v3; P07 mở rộng sang nhiều chủ sở hữu/party và PvP 3v3. P03 hoàn thiện quản lý roster, nhưng P02 phải có chọn/sắp pet đầu tối thiểu để chơi được. P19 cung cấp nền item; P15 kiểm chứng phân EXP với combat thật, không tạo vòng dependency ngược. P20 cung cấp học/quyền công thức; P16 kiểm chứng tái sử dụng qua các lần dung hợp thật. Cấp/nhận công thức 5★ tối thiểu nằm ở P19/P20, không phụ thuộc auction/mail đầy đủ P08.

Các phase thiết kế có gate bằng tài liệu được review; phase tích hợp có gate bằng trải nghiệm chơi được. Review game design mục 2 vẫn bắt buộc. Master plan chỉ ghi phạm vi/flow/decision/gate; chưa tạo implementation plan, công thức số hoặc code trong lượt này. Fidelity, save compatibility và hiệu năng đi xuyên phase. P09 chuẩn bị metrics/backup từ P00 nhưng gate release sau P17; truyện phụ P18 làm sau, P08 meta không chặn nếu không chọn.

### 5.1. Review so với video/game gốc và phần cần cải thiện

Lượt review này đã đọc audit timeline và xem lại [bảng khung hình trích video](../../docs/research/reference/video-overview.jpg), không phát/xem lại toàn bộ video. Nguồn hình chỉ chứng minh nội dung nhìn thấy; không khôi phục được công thức từ montage.

| Bằng chứng tham chiếu | Khoảng trống của v3 | Xử lý trong v4 |
|---|---|---|
| City/NPC ở khoảng 00:45–01:30, hang/skill 03:00–03:30, quảng trường/bãi biển 03:45–04:15 theo audit | P01 chủ yếu nói di chuyển, chưa thiết kế world graph/loại map | P12 tách map an toàn, vùng quái, farm riêng; P15 nối vùng với training |
| Menu pet/thuộc tính khoảng 01:45–02:15 | P03 gom UI, stats, skill, breeding thành một phase | P10/P11/P13 thiết kế riêng rồi tích hợp P03 |
| Tooltip skill nước ở 03:30 có mô tả đánh nhiều địch | P02 1v1 chưa chứng minh group skill hoặc synergy | P13 chốt rules; P02 kiểm chứng PvE 1v3, P07 kiểm chứng party/PvP; không suy ra type chart từ tooltip |
| Tab trang bị pet có ở 01:58–01:59; farm riêng/synthesis/ấp trứng chưa có flow được xác minh | V4 trước review này ghi nhầm equipment là chưa thấy; chưa biết đầy đủ slot/stat rules | P14 đối chiếu tab trang bị; P16 vẫn cần thiết kế lifecycle trứng/farm owner, không gắn nhãn luật gốc |
| Video không thể hiện trọn chiến dịch hoặc toàn bộ tuyến map | P04 onboarding chưa thay thế cốt truyện | P17 một tuyến chính, P18 truyện phụ sau |

Đã mở lại [hướng dẫn người chơi ngày 19/05/2010](https://m.ali213.net/gonglue/100519/11194.html): bài mô tả pet 1–5 sao, bố mẹ cùng sao với thêm điều kiện level/chủng tộc/giới tính, và cap level liên quan sao. Đây là nguồn người chơi theo phiên bản, **không chứng minh “phải max cấp” hoặc mọi cặp cùng sao đều tăng đúng một sao**. [Hướng dẫn skill ngày 08/09/2010](https://m.ali213.net/gonglue/100908/10529.html) và [fidelity ledger](../../docs/research/fidelity.md) là nguồn đối chiếu family/status; không đủ để khẳng định một ma trận 8 nguyên tố gốc. Lần mở lại trang catalog Bahamut bị lỗi, nên không bổ sung claim mới từ trang đó.

**Các hướng cân nhắc khi vào phase thiết kế:**

- Pet/hệ: chủ dự án đã chốt 8 hệ tộc gắn với 8 hệ skill, mỗi hệ có vật lý/phép, cộng một nhóm skill chung. Tách định danh tộc, family skill và cá thể để mô tả ánh xạ/di truyền rõ; nhóm skill chung không phải hệ tộc thứ chín. Không mặc định mọi pet được học mọi skill khác hệ.
- Training đã chốt: lv20 đủ điều kiện, luyện cao hơn cho trứng có chỉ số tốt hơn. P15 phải so sánh dung hợp sớm với luyện lâu, tính cả hai bố mẹ và nhiều thế hệ; không biến max cấp thành điều kiện bắt buộc ngầm.
- Nếu chọn +1 sao và tiêu cả hai bố mẹ, một pet 5★ cần tối thiểu 16 pet 1★ và 15 lần dung hợp từ đầu, chưa tính thất bại/recipe/material/XP. Đây là phép đếm theo giả định thiết kế, không phải dữ liệu lịch sử. Không dùng thời gian “first synthesis” làm thước đo duy nhất.
- Tương tác hệ: ưu tiên một bộ tương tác nhỏ, dễ đọc và có counterplay trước khi mở rộng. Status/kháng và learned-skill inheritance giúp tạo bản sắc riêng; không cần bê nguyên bảng khắc hệ Pokémon.
- Các phần dễ thiếu đã gắn owner: bắt/appraise/chọn giống (P03), kho và vòng đời trứng (P16), đường hồi phục/ngân sách XP-vàng-vật liệu/boss-arena gates (P15/P04), đồng bộ bách khoa/planner (P03/P16/P05), công cụ kiểm tra content và migration (P04/P09). Không thêm crafting, housing hoặc daily mặc định; PvP cơ bản 3v3 đã được chọn ở P07, ranking vẫn tùy chọn.
- Mốc truyện: chỉ dành hook vùng/NPC từ P12/P04, viết tuyến chính ở P17 sau hệ thống để đúng yêu cầu. P09 vẫn phải chạy sau truyện vì quest/reward/save mới cũng cần kiểm định.

### 5.2. Nghiên cứu bổ sung và quyết định sau review

**Trạng thái:** Đã nhận lựa chọn của chủ dự án; bảng dưới thay thế khuyến nghị cũ. Roadmap có 21 phase sau khi thêm P19/P20. Đề xuất bị từ chối không được đưa lại vào implementation plan như scope mặc định. Lượt này đọc lại video audit, xem contact sheet 01:52–02:07 và tìm nguồn trên web; không xem lại toàn bộ video. Đã sửa nhận xét sai về trang bị: có tab ở 01:58–01:59, chỉ luật chi tiết còn chưa rõ.

**Nguồn và giới hạn:**

- [Video Pokezoo](https://www.youtube.com/watch?v=FXJtLBPoGgo) qua [audit có timestamp](../../docs/research/VIDEO_UI_AUDIT_2026-09-23.md): tab stat/resistance/equipment/skill, party, đánh nhiều mục tiêu và auto trong trận có bằng chứng. Không suy ra quy mô đội, công thức damage hoặc auto farm offline.
- [Hướng dẫn skill 08/09/2010](https://m.ali213.net/gonglue/100908/10529.html): mô tả các hệ có hiệu ứng trạng thái/giải trạng thái, buff/debuff riêng và con lai có thể kế thừa skill đặc thù của bố mẹ khác hệ. Là lời người chơi theo phiên bản, chưa xác minh bộ 8 hệ mới.
- [Hướng dẫn synthesis 22/12/2010](https://m.ali213.net/gonglue/101222/9961.html): mô tả học công thức dùng lâu dài, tra công thức tại ranch, nguồn công thức khác nhau theo sao. Tham khảo vòng khám phá→công thức→lai, không sao chép điều kiện thương mại của bản đó.
- [Hướng dẫn chọn/luyện pet 05/08/2010](https://m.ali213.net/gonglue/100805/10818.html): nhấn mạnh chọn bố mẹ theo hướng vật lý/phép, chuẩn bị skill và tuyến luyện pet. Không lấy thời gian hoặc số liệu của bài làm balance hiện tại.
- [Monster Sanctuary — giới thiệu của nhà phát hành](https://store.steampowered.com/app/814370/Monster_Sanctuary/?l=english): skill tree, khả năng riêng từng loài và pet giúp khám phá môi trường. Chỉ tham khảo giá trị lựa chọn build/khám phá, không chuyển Phimond sang platformer.
- [Siralim Ultimate 2.0 — ghi chú nhà phát triển](https://www.thylacinestudios.com/blog/siralim-ultimate-2-0-patch-notes): cải thiện UI fusion, xem trước hình dung hợp, đánh dấu yêu thích, điều kiện macro và tùy chọn giảm chờ hiệu ứng. Tham khảo khả năng đọc kết quả và giảm thao tác lặp, không lấy độ phức tạp/số lượng content làm mục tiêu.

| Đề xuất cũ | Quyết định hiện tại | Owner |
|---|---|---|
| Q01 — trợ giúp luyện lại | Không chọn sân tập/bù level. Pet nở lv1 farm lại ở map thấp; mang tối đa 3 pet và có item EXP share để pet mạnh kéo pet yếu | P19, P15, P03 |
| Q02 — combat/party | Đã chốt PvE pet đầu 1v3 auto; PvP 3 pet/người; party tối đa 3 người, mỗi người 1 pet | P02, P07 |
| Q03 — công thức/coverage | Chọn học một lần dùng lâu dài, hiếm theo sao; 1★–4★ rơi từ quái, 5★ chỉ event/admin; thêm phase công thức riêng | P20 |
| Q04 — bản sắc loài/kế thừa skill | Chấp nhận để brainstorm sâu tại phase, ghi checklist bắt buộc cho spec/implementation plan tương lai; chưa chốt luật kế thừa khác hệ | P10, P13, P16 |
| Q05/Q06 — so sánh/khóa/preview/planner nâng cao | Không mở rộng theo đề xuất; làm rõ cơ chế dung hợp/cường hoá tại phase sở hữu. Giữ thông tin điều kiện/chi phí/tiêu pet tối thiểu của product contract | P03, P16 |
| Q07 — boss/endgame thử build mới | Không chọn; không thêm track thử thách/endgame riêng. Arena/progression có từ trước vẫn theo scope cũ | Không tạo phase |
| Q09 — pet mở lối/khám phá phụ | Không chọn | Không tạo phase |
| Q08/Q10 — QoL auto/sân thử build mở rộng | Chỉ giữ auto combat và đổi build 5★ +99 đã chốt; không tự thêm macro nâng cao, sân tập hoặc respec sớm | P02, P13, P16 |

Không dùng phần nghiên cứu nguồn làm bằng chứng rằng mọi đề xuất đã được chọn. Chi tiết cơ chế công thức xem P20; các luật sản phẩm mới ưu tiên hơn reference lịch sử.

## 6. Phase specifications

### P00 — Khóa baseline và sửa đường dữ liệu cốt lõi

**Outcome:** Cùng một build, cùng một flow test, mọi người biết tính năng nào thực sự chạy và đâu là dữ liệu mô phỏng.

- **P00-R01:** Ghi nhận baseline version, entry scene, server command, catalog/ruleset và bộ test active; thiết lập quản lý phiên bản/restore point trước sprint code tiếp theo. Không xóa legacy chỉ vì tên giống.
- **P00-R02:** Sửa F01/F02: thống nhất snapshot/event/completed battle contract; mỗi event có đủ context để render một lần, kể cả action kết thúc trận. Không dựa vào field đã bị public serializer loại bỏ.
- **P00-R03:** Chuẩn hóa asset/reference ledger: mỗi screen có timestamp, screenshot, mapping, phần chưa biết và người kiểm tra. Chọn sustained blue/gold client làm baseline presentation.
- **P00-R04:** Baseline performance và fault matrix: input→preview, request→ack, frame cadence, asset warmup, disconnect/timeout; phân biệt FPS với độ trễ DB/network. Chốt workload, cấu hình thử và performance budget 50 CCU tại mục 2; chuẩn bị harness/metrics từ đầu để mỗi phase có thể đo regression.
- **P00-R05:** Đồng bộ docs/check scripts với active client; test accounts dễ nhận biết và có chính sách dọn riêng, không mất account người dùng.

- **P00-R06:** **Task review gameplay & game design bắt buộc:** Review vòng chơi đang có từ login đến encounter/combat/pet; tách bug kỹ thuật, friction và khoảng trống game design. Chốt baseline đo gameplay, danh sách POC visual debt và bộ ảnh chuẩn giữ thiết kế nhân vật/quái vật. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 baseline + canonical checks; S02 live combat event bridge + terminal result; S03 fault/performance/reference baseline nếu không thể gộp mà vẫn review được.

**Exit gate:** Live battle thực sự hiển thị ít nhất damage/heal/miss/status và kết quả cuối; reconnect không replay effect/reward; fixtures dùng public wire shape; docs không còn gọi script cũ là bằng chứng active. Có report lỗi còn mở theo severity.

**Ngoài scope:** Thêm vùng, loài, party hoặc đổi công thức damage.

### P10 — Thiết kế lại pet: 8 hệ, 5 sao và level

**Outcome:** Có một mô hình pet thống nhất để các phase stat, skill, map, training và dung hợp cùng sử dụng.

- **P10-R01:** Thiết kế **8 hệ tộc gắn với 8 hệ skill tương khắc** theo xác nhận của chủ dự án; chốt tên/định danh, ánh xạ và vai trò từ 8 race hiện có. Phân biệt species/cá thể với tộc/family skill; skill chung không tạo hệ thứ chín. Đối chiếu lịch sử và ghi rõ phần thiết kế mới.
- **P10-R02:** Giữ 1★–5★ với cap gốc lần lượt 60/70/80/90/100; cap hiệu lực bằng cap gốc cộng độ cộng +00…+99 (5★ +99 = lv199). Phân biệt sao, level/XP hiện tại, độ cộng và generation; tăng cap không tự cấp thêm level hay trực tiếp tăng stat. Sao quyết định nền stat/growth, level quyết định phần tăng trưởng đã luyện; kiểm chứng sao cao ưu thế khi cùng level và 1★ lv159 mạnh hơn 5★ lv1 về chỉ số. Công thức tăng độ cộng còn brainstorm, không tự mở thêm sao.
- **P10-R03:** Thiết kế hai nhánh P16: nâng đúng một sao từ hai pet cùng sao, có hình ảnh pet đích và ít nhất một bố mẹ cùng hệ tộc đích; bổ trợ giữ pet chính, về trứng level 0 và tăng chỉ số/độ cộng. Nâng sao reset độ cộng về +00; cả hai nhánh ra trứng lv0 và nở pet lv1. +99 chặn cường hoá, chỉ còn nhánh nâng sao nếu hợp lệ; 5★ không lên 6★, chỉ bổ trợ khi chưa +99. 5★ +99 được đổi build không tăng chỉ số/cap; phạm vi/chi phí của thao tác riêng này chốt ở P13/P16, không cho đi vòng để mở lại cường hoá. Phân biệt với strengthening hiện có; chốt chuyển đổi thay vì mặc định tái sử dụng nguyên luật donor cũ.
- **P10-R04:** Review bản thiết kế và ảnh hưởng tới species/cá thể/save/recipe/planner đang có; giữ vai trò individual variance, learned-skill inheritance và phả hệ qua nhiều thế hệ.

**Exit gate:** Có bản thiết kế được review, glossary thống nhất, quyết định về 8 hệ/5 sao/level và các ràng buộc liên phase; các luật chưa chọn có owner/gate. Chưa yêu cầu code hay bộ content đầy đủ.

### P11 — Hệ thống chỉ số pet và quái

**Outcome:** Người chơi hiểu sức mạnh pet đến từ đâu và có lý do giữ, luyện hoặc chọn một cá thể làm bố mẹ.

- **P11-R01:** Thiết kế bộ chỉ số gốc/derived, HP/MP, công/thủ vật lý và phép, tốc độ, chí mạng/chính xác/né nếu chọn; không thêm stat chỉ vì game khác có.
- **P11-R02:** Phân biệt base species, quality/potential cá thể, growth, level, sao, resistance/status resistance, buff và trang bị. Kế thừa phải phản ánh phần chỉ số tăng do level của bố mẹ: cùng các yếu tố khác, bố mẹ luyện cao hơn lv20 cho trứng tốt hơn. Chốt phần đóng góp của level/base/growth/inheritance cũ để tránh cộng lặp qua thế hệ; tránh cộng buff/trang bị tạm thời vào di truyền. Độ cộng +xx chỉ tăng cap; lợi ích stat đến từ luyện level và kế thừa được tính riêng. Thiết kế phải duy trì ưu thế chỉ số của sao cao khi cùng level, đồng thời giữ giá trị chênh level lớn; đánh giá theo vai trò/budget, không biến thành mọi stat của mọi loài đều xếp hạng tuyệt đối.
- **P11-R03:** Pet sở hữu và quái ngoài map dùng quy tắc chỉ số nhất quán, có ngoại lệ boss được khai báo; appraisal và UI giải thích phần ẩn/hiện.
- **P11-R04:** Review vai trò/build, tốc độ tăng sức mạnh qua thế hệ và ngân sách cho P13/P14; đánh giá trần kế thừa theo sao và cách chuyển phần kế thừa khi nâng sao, không coi reset +00 là tự xóa hoặc tự nhân chỉ số di truyền; yêu cầu mô phỏng kiểm chứng khi triển khai, không khóa công thức số trong master plan.

**Exit gate:** Bộ stat và nguồn đóng góp/di truyền rõ, có kịch bản so sánh cá thể cùng loài/cùng sao/khác level được review, không khiến mọi pet cùng loài trở nên giống nhau.

### P12 — Thiết kế thế giới, liên kết và loại bản đồ

**Outcome:** Mỗi map có vai trò trong hành trình, đường đi/đường về và nội dung NPC/quái được xác định.

- **P12-R01:** World graph và liên kết portal, điểm đến an toàn, tuyến chính/nhánh, điều kiện mở vùng và đường hồi phục; phân biệt topology gameplay với ảnh nền APK.
- **P12-R02:** Phân loại thành phố/làng/hub NPC an toàn không có quái hoang; map dã ngoại có quái; trang trại riêng từng tài khoản; arena/challenge riêng nếu cần. Ngoại lệ combat ở hub phải được thiết kế riêng, không sinh quái từ pool mặc định.
- **P12-R03:** Mỗi vùng có NPC/dịch vụ, roster quái, phân bố/khu spawn và vai trò khám phá; level/XP cụ thể thuộc P15, lifecycle thuộc P01. Phân biệt quái chiến đấu với pet follower/trưng bày.
- **P12-R04:** Phân biệt map template và instance: public world, private farm theo owner; điểm vào/ra, quyền truy cập và tính bền vững. P06 hiện thực presence; không chờ P06 mới phát hiện farm dùng chung sai owner.
- **P12-R05:** Review route, readability, trở lại vùng cũ và thiếu tài nguyên; dành hook cho truyện P17, chưa viết truyện hoặc chốt toàn bộ số lượng map.

**Exit gate:** World graph, ma trận loại map/NPC/quái/quyền truy cập và tuyến mở vùng được review; không có portal cụt ngoài chủ ý, farm lẫn account hoặc mặc định quái xuất hiện ở khu an toàn.

### P01 — World traversal, collision và encounter lifecycle

**Outcome:** Người chơi đi tới đâu nhìn thấy đúng vị trí, tương tác đúng vật thể và không bị mắc kẹt/vào trận ngoài ý muốn.

- **P01-R01:** Một mô hình tọa độ X/Y giữa map, renderer, NPC, portal, spawn; bounds và safe arrival hợp lệ khi qua cổng, reconnect, đổi content.
- **P01-R02:** Walkable/collision dữ liệu theo map, camera/framing/layer đúng; sửa các mảng ghép rừng và seam thấy trong playtest. Không suy ra collision từ một ảnh nền rồi coi là dữ liệu lịch sử chính xác.
- **P01-R03:** Giữ phím/D-pad mượt; release/focus loss/menu/battle dừng đúng; click-to-approach đi đường hợp lệ, bị chặn thì dừng và giải thích. Nội suy không teleport hoặc xuyên vật cản được server chặn.
- **P01-R04:** NPC/portal proximity hai chiều và điều kiện sử dụng thống nhất; phản hồi bị khóa map/NPC ngoài tầm rõ ràng.
- **P01-R05:** Chốt spawn lifecycle cho solo: contact, target identity, active battle, defeat/capture/flee, cooldown/respawn, reconnect. Phân biệt private encounter với shared spawn; chưa giả lập tranh quái multiplayer.

- **P01-R06:** **Task review gameplay & game design bắt buộc:** Review cảm giác di chuyển, đường đi, khả năng đọc map, mật độ gặp quái, contact/cooldown và nhịp khám phá. Đo thao tác hụt, mắc kẹt và encounter ngoài ý muốn; chỉnh để di chuyển/gặp quái tự nhiên, kiểm tra silhouette nhân vật và quái vẫn rõ trên map. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 coordinate/proximity contract; S02 collision + navigation + camera; S03 spawn lifecycle và transition/recovery.

**Exit gate:** Chạy được một route city→forest→city→ranch bằng keyboard/D-pad/click; không xuyên chướng ngại/teleport; gặp đúng quái; rời trận không lặp vô hạn; vị trí khi reconnect khớp state hợp lệ. Playtest các góc map, cửa sổ đổi tỷ lệ và focus loss.

**Ngoài scope:** Shared-world ownership và party follow, thuộc P06/P07.

### P13 — Skill pet/quái và tương tác giữa các hệ

**Outcome:** Skill tạo lựa chọn chiến thuật thông qua phối hợp, khắc chế và xử lý trạng thái, giữ bản sắc nuôi/lai pet.

- **P13-R01:** Thiết kế **8 family skill gắn với 8 hệ tộc**, mỗi family có **nhánh vật lý và nhánh phép riêng**, cùng một số skill dùng chung cho cả 8 hệ. “Dùng chung” là phạm vi đủ điều kiện học, không tự cấp toàn bộ skill cho mọi pet. Chốt vai trò damage/support/control, học/nâng skill, slot và điều kiện sử dụng. Quái ngoài map dùng cấu trúc này với skill pool/hành vi theo loài/vùng/level; không chỉ tăng HP/damage.
- **P13-R02:** Phân biệt khắc chế sát thương/kháng, phối hợp tăng cường và triệt tiêu/giải trạng thái. Xác định thứ tự giải quyết, thời hạn, giới hạn cộng dồn và cách UI giải thích; tham khảo tư duy Pokémon, không sao chép toàn bộ type chart hay hệ số.
- **P13-R03:** Thiết kế single/group target cho PvE 1 pet vs 3 quái (P02), party tối đa 3 người mỗi người 1 pet, PvP 3 pet mỗi bên (P07). Không buộc tất cả người chơi tham gia party mới dùng được hệ skill cơ bản.
- **P13-R04:** Giữ khác biệt species skill pool với skill bố mẹ thực sự học; ràng buộc học/kế thừa skill chung, skill cùng hệ và skill khác hệ phối hợp P16, tránh một combo vừa tối ưu mọi map vừa triệt tiêu vai trò mọi hệ khác.
- **P13-R05:** Review ma trận tương tác và kịch bản counterplay; có kế hoạch kiểm chứng vòng lặp buff/control vô hạn và phản hồi chiến đấu, không liệt kê hàng trăm skill ở đây.

- **P13-R06:** **Ghi chú bắt buộc khi viết phase spec/implementation plan:** brainstorm bản sắc loài trong cùng tộc/sao (vai trò, growth, skill pool); phân biệt skill chung, bản địa và skill thực học kế thừa. So sánh phương án kế thừa khác hệ có giới hạn, số slot, skill vật lý/phép và giải trạng thái; giữ giá trị bố mẹ ngoài stat, tránh pet có mọi ưu điểm 8 hệ. Chủ dự án đã chọn nghiên cứu hướng này, chưa phê duyệt công thức/slot hay mọi skill đều được kế thừa. Kết luận design phải có trước task implementation liên quan, phối hợp P10/P16.

**Exit gate:** Thiết kế có đủ 8 family với hai nhánh vật lý/phép mỗi family, nhóm skill chung và ma trận tương tác được review; có tình huống minh họa tăng cường, tương khắc, triệt tiêu và trung tính. Mỗi tình huống ghi rõ solo PvE 1v3, party hay PvP 3v3; gate runtime lần lượt thuộc P02/P07.

### P19 — Hệ thống items và vật phẩm chia EXP

**Outcome:** Vật phẩm có loại, công dụng, nguồn nhận và quy tắc sử dụng nhất quán; phục vụ combat, training, trang bị và học công thức.

- **P19-R01:** Thiết kế catalog item theo chức năng: hồi HP/MP, bắt pet, nguyên liệu/chi phí dung hợp-ấp nếu được chọn, vật phẩm nhiệm vụ, EXP share, bản vẽ pet và trang bị tham chiếu P14. Mỗi item có ID, tên/mô tả, hình/icon, rarity, stack và điều kiện dùng; không tự thêm crafting/housing hoặc loại tiền mới.
- **P19-R02:** Nguồn nhận/tiêu: quái, shop, quest, event và admin grant theo allowlist từng loại. Thiết kế drop table theo quái/map và độ hiếm, kiểm soát gold/material sources-sinks. Công thức 5★ bị loại khỏi mọi drop quái kể cả boss/quái sự kiện; thưởng event trực tiếp hoặc admin gửi do P20 quy định.
- **P19-R03:** Inventory/kho có ownership, count/stack/capacity, trang bị/đang dùng/tiêu một lần; chốt bound/tradable/sell/discard theo loại trước triển khai. Intent dùng item bị từ chối vì sai điều kiện không mất đồ; kết quả gameplay thất bại như bắt pet hụt vẫn tiêu item theo luật đã chốt; retry/reconnect không dùng/nhận hai lần. Luật UI tích hợp ở P03, không cần thêm màn hình mới chỉ để chia phase.
- **P19-R04:** **EXP share là item bắt buộc trong thiết kế:** cho pet mạnh kéo pet yếu trong danh sách tối đa 3 pet. Chốt item trang bị hay kích hoạt/tiêu hao, phạm vi nhận EXP, tỷ lệ chia hay bonus, thời hạn/số lượt, pet gục/cap, thay roster giữa trận và party. Chưa chốt con số; không áp XP share miễn phí, không nâng thẳng pet mới nở lên level bố mẹ. P15 đo pacing qua combat thật.
- **P19-R05:** Event/admin gửi vật phẩm có người nhận, nguồn/lý do, quyền hạn và nhận một lần; xây flow cấp/nhận tối thiểu không phụ thuộc mail/auction P08. Chốt xử lý túi đầy và học công thức 5★ qua P20. Không gửi vật phẩm thật cho user trong lượt viết plan.
- **P19-R06:** Review gameplay/game design đầu-trong-cuối phase theo mục 2: hiểu công dụng, nguồn farm, chi phí, độ hiếm và lợi ích EXP share; xác định công thức/balance còn cần P15/P20 kiểm chứng, không coi catalog JSON là hoàn thành.

**Exit gate:** Thiết kế item/nguồn dùng được review; khi triển khai, nhận→xem→dùng/tiêu/lưu lại qua relog hoạt động, retry không nhân item, nguồn cấm bị chặn. Item EXP share có contract đủ cho P02/P15; gate chia EXP và kéo level cuối cùng thuộc P15. Trang bị và bản vẽ có liên kết đúng P14/P20.

**Ngoài scope:** Crafting, housing, auction/mail đầy đủ, tiền thật và auto farm offline.

### P02 — PvE auto: một pet đấu ba quái

**Outcome:** Chạm quái vào trận PvE auto với pet đầu danh sách đối đầu 3 quái; đọc rõ từng actor/target, kết quả và trạng thái auto.

- **P02-R01:** Command→skill/item→target→submit→resolution→next turn/result có state rõ; back/cancel/disabled/busy không gửi lệnh thừa. Auto PvE có chỉ báo, xử lý target chết và MP/item không đủ; quyền dừng/chuyển lệnh tay/capture cần chốt trong spec, không tự mở auto farm offline.
- **P02-R02:** Event playback dựa trên kết quả server: actor/target, hit/miss, damage/heal, status/buff, MP/item, capture, faint; cân chỉnh duration theo clip và reference, không tự đoán damage từ hiệu ứng.
- **P02-R03:** Kiểm tra tất cả mapped species/action: quay vào đối thủ, chân/shadow/HP/name/target marker cùng anchor; sprite attack không dịch sai hitbox; kết quả không biến mất trước effect cuối.
- **P02-R04:** Trình bày skill cost, học/chưa học, MP thiếu, item hết, seal/capture restrictions; không cho thao tác trông khả dụng rồi chỉ trả lỗi chung.
- **P02-R05:** Win/loss/flee/capture là bốn flow rõ, có reward/destination/recovery; pet gục vẫn có đường tiếp tục chơi. Resume battle khôi phục turn/resources/target state, không gửi lại action chưa rõ kết quả.

- **P02-R06:** **Task review gameplay & game design bắt buộc:** Review quyết định attack/skill/item/defend/capture/flee, nhịp chờ giữa lượt, feedback và khả năng hiểu thắng/thua. Đo thời gian trận, thời gian chờ, chọn nhầm và lỗi hiểu turn; tối ưu flow/timing, đề xuất balance riêng nếu cần; giữ tạo hình và hướng/pivot của mọi actor. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 command/result/reconnect flow; S02 animation, floating feedback và status; S03 auto/capture/edge cases + battle fidelity acceptance.

**Exit gate:** Chạm quái→auto pet đầu vs 3 quái, xử lý target đã chết/bị bắt và điều kiện kết thúc; chơi bằng UI thật đủ bốn kết quả; xem rõ hit/miss/heal/status trên wire thật; test duplicate request, stale turn, disconnect trước/sau ack và finishing blow. Không còn bug hướng/pivot ở bộ pet alpha.

- **P02-R07:** Người chơi mang tối đa 3 pet, pet đầu ra trận solo; encounter sinh 3 quái với identity riêng, server quyết định loài/level theo map. Single/group target, chết/bắt/chạy và kết thúc trận phải xử lý nhiều quái; chọn loài/bố trí/đổi pet giữa trận là decision của phase, không tự bật cả 3 pet người chơi. Kế hoạch giữ/resume battle 1v1 cũ phải rõ.

**Ngoài scope:** Party và PvP thuộc P07; auto farm không giám sát/offline chưa được chọn. Multi-target PvE thuộc chính P02.

### P14 — Hệ thống trang bị cho pet

**Outcome:** Trang bị tạo lựa chọn build bổ trợ pet, với flow nhận–xem–trang bị–tháo rõ ràng.

- **P14-R01:** Chốt loại/slot, điều kiện trang bị theo pet, nguồn nhận và ngân sách stat theo P11; scope đã yêu cầu; video có tab trang bị ở 01:58–01:59, nhưng chưa xác minh số slot, loại đồ và công thức bonus gốc.
- **P14-R02:** Quan hệ với inventory/storage, binding/trade, active/retired pet và lifecycle dung hợp: đồ phải được xử lý minh bạch khi tiêu bố mẹ; thiếu chỗ chứa có hành vi rõ.
- **P14-R03:** Hiển thị so sánh trước/sau; persist/reconnect nhất quán; không cộng trùng chỉ số hoặc tạo đồ qua tháo/lắp/retry. Luật kế thừa pet không mặc nhiên kế thừa bonus trang bị.
- **P14-R04:** Review giá trị build so với sao/level/quality/skill; cân bằng để trang bị không xóa động lực bắt và lai cá thể tốt. Crafting, nâng cấp đồ, set bonus không tự thuộc scope.

**Exit gate:** Luật trang bị được chốt và một vòng nhận–lắp–dùng trong trận–tháo–đăng nhập lại kiểm chứng được khi triển khai; có xử lý trang bị của bố mẹ trước dung hợp, không mất/nhân đồ.

### P15 — Level quái theo map và tiến trình luyện pet

**Outcome:** Người chơi biết luyện pet ở đâu, nuôi được hai bố mẹ đạt điều kiện và đưa pet con trở lại vòng chơi.

- **P15-R01:** Thiết kế dải level quái theo vùng/khu spawn, độ khó/skill, XP/drop, tuyến mở map/arena, phân biệt trainer level và pet level. Các khoảng level lịch sử là reference theo phiên bản, chưa là bảng cân bằng cuối.
- **P15-R02:** Áp ngưỡng lv20 đủ dung hợp và cap theo sao + độ cộng của P10. Luyện cao hơn cải thiện chỉ số trứng, không bắt buộc max cấp; so sánh hiệu quả thời gian giữa dung hợp sớm và luyện sâu trước dung hợp.
- **P15-R03:** Đo thời gian/công sức nuôi **hai** bố mẹ, nhiều thế hệ tới 5★, pet con level thấp và trở lại vùng cũ, các vòng bổ trợ giữ sao và đường luyện tới cap cao nhất lv199. Không mặc định phải tạo 199 map hoặc một map cho mỗi level. Pet nở lv1 phải farm lại từ các map thấp, không có sân tập/bù level riêng. Mang tối đa 3 pet; item EXP share theo P19 cho phép pet mạnh kéo pet yếu. Chốt tỷ lệ chia, đối tượng nhận, giới hạn chênh level và xử lý pet chạm cap khi thiết kế; không tự chia EXP khi thiếu item. Farm cá nhân không mặc nhiên sinh XP.
- **P15-R04:** Economy cơ bản gồm seal, hồi HP/MP, học skill, đồ, dung hợp và ấp; đường phục hồi khi hết tài nguyên/pet gục. Review nhịp grind, chênh level, phần thưởng boss/arena và lý do đi nhiều map thay vì một bãi tối ưu duy nhất.

**Exit gate:** Có tuyến luyện theo sao/level/map được review và playtest khi tích hợp, đo được thời gian tới hai bố mẹ đủ điều kiện; kiểm tra đi lại map thấp để farm từ lv1 và trường hợp kéo level bằng item EXP share; đo EXP khi không có/có item và tổng thưởng không bị nhân ngoài luật. P04 nghiệm thu lại toàn bộ từ account sạch.

### P20 — Bản vẽ pet, học công thức và nguồn thu thập theo sao

**Outcome:** Người chơi nhận bản vẽ có hình pet, dùng một lần để học công thức, rồi dùng công thức lâu dài cho các lần dung hợp/cường hoá đủ điều kiện.

- **P20-R01:** Tách ba khái niệm: **bản vẽ** là item có hình/định danh pet; **công thức đã học** là quyền dùng lâu dài; **lần dung hợp/cường hoá** là thao tác tiêu hai pet và chi phí riêng. Tiêu bản vẽ khi học thành công, không tiêu lại quyền công thức mỗi lần; một file ảnh đơn thuần không cấp quyền học.
- **P20-R02:** Độ hiếm tăng theo sao. Công thức 1★–4★ có thể rơi từ quái với nguồn phân theo vùng/loài/độ khó; tỷ lệ cụ thể chốt sau. Công thức 5★ **chỉ nhận qua thưởng sự kiện hoặc admin gửi**, không nằm trong drop table quái thường/boss/quái sự kiện. Không tự thêm quest/shop thường như nguồn 5★; quyền học không tự mở chỉ vì đã thấy pet trong bách khoa.
- **P20-R03:** Công thức liên kết loài/hình pet đích, bậc sao, nhánh áp dụng và điều kiện pet chính/phụ. Chốt quy ước sao nhãn theo pet đích, recipe riêng hay dùng chung cho nâng sao/bổ trợ, tiêu chí asset đầu ra đủ dùng; bảo đảm hai pet cùng sao và ít nhất một bố mẹ cùng hệ đích khi nâng sao theo P16.
- **P20-R04:** Học công thức từ item trong túi; lưu lâu dài và còn sau relog. Chốt phạm vi account/character, xử lý học trùng, trao đổi/binding và bản vẽ thừa. Khuyến nghị học trùng bị từ chối không tiêu item, nhưng quyết định này phải ghi trong phase spec. Chưa chọn market/trade như điều kiện bắt buộc để tiếp cận công thức.
- **P20-R05:** Nguồn event/admin 5★ có quyền cấp, người nhận, danh sách thưởng/điều kiện event và lịch sử nhận. Có thể nhận vật phẩm ở event rồi học sau; hết event không xóa công thức đã học. Chốt chuyển nhượng bản vẽ 5★ có được phép hay không trước economy P08; không mở kênh mua bán để lách nguồn chỉ event/admin.
- **P20-R06:** Danh mục công thức gắn world graph và coverage asset 8 hệ/1★–5★: chỉ rõ nhánh có thể làm, thiếu công thức, thiếu pet nguyên liệu hoặc thiếu asset. Giải thích người chơi cần học công thức nào; chưa làm planner/preview nâng cao bị từ chối. Ghi rõ 5★ là nội dung được phân phối có kiểm soát, không hứa farm quái thường sẽ nhận được. Trước chốt progression/truyện chính, xác định campaign có cần 5★ hay không và người chơi bỏ lỡ event tiếp cận nội dung ra sao; không tự mở nguồn drop/shop mới để giải quyết.
- **P20-R07:** Review đầu-trong-cuối phase theo mục 2: dễ hiểu sự khác nhau bản vẽ/quyền học/chi phí mỗi lần, động lực farm 1★–4★, tiếp cận event 5★ và nguy cơ nhánh không có đầu ra. P16 tích hợp quyền công thức vào hai thao tác thật.

**Luồng hướng dẫn ở mức thiết kế sản phẩm:**

1. **Thu thập:** đánh quái ở vùng phù hợp để nhận bản vẽ 1★–4★; nhận thưởng event/admin cho 5★. Vật phẩm nằm trong túi, có hình/tên pet và sao; chưa học thì chưa được dùng công thức.
2. **Học:** chọn bản vẽ → thao tác học → server kiểm tra quyền sở hữu/chưa học → tiêu một bản vẽ và ghi quyền công thức cùng một kết quả bền vững. Retry không tiêu thêm bản vẽ; xử lý đã học phải được chốt rõ.
3. **Tra cứu:** công thức đã học tồn tại trong danh mục dung hợp/cường hoá; giải thích pet đích, nhánh áp dụng và điều kiện. Không yêu cầu người chơi giữ thêm một bản vẽ trong túi.
4. **Sử dụng:** tại nơi dung hợp theo P16, chọn công thức/nhánh và hai pet hợp lệ tối thiểu lv20, cùng sao. Kiểm tra asset đích, hệ tộc, +99, chi phí và quyền dùng; công thức không thay thế điều kiện nguyên liệu.
5. **Nhận kết quả:** tiêu hai pet và chi phí theo P16 → trứng lv0 → ấp nở lv1; quyền công thức còn nguyên. Nâng sao reset +00; cường hoá giữ loài/sao và áp luật + đã chốt.
6. **Lặp lại:** chuẩn bị hai pet/chi phí mới để dùng lại công thức; không cần farm lại bản vẽ đó. Mất hai pet nguyên liệu không làm mất quyền công thức.

**Ví dụ minh hoạ convention cần chốt:** nếu nhãn sao bám pet đích, bản vẽ pet X 2★ dùng cho nhánh nâng hai pet 1★ thành X 2★; công thức bổ trợ X 2★ dùng hai pet 2★ với X làm pet chính. Bản vẽ 1★ vẫn có ý nghĩa cho cường hoá pet 1★, không tạo pet 0★. **Khuyến nghị để chốt ở phase:** một bản vẽ pet X mở quyền công thức của X, liệt kê những nhánh hợp lệ; tách điều kiện nâng sao/cường hoá bên trong thay vì bắt farm hai bản vẽ cùng hình. Đây chưa phải quyết định đã phê duyệt. Một bản vẽ có mở cả hai nhánh hay cần hai loại công thức là câu hỏi của phase spec, chưa tự chốt. Không dùng ví dụ này thay luật loài/hệ/recipe thực tế.

**Exit gate:** Nhận item→học một lần→mất đúng một bản vẽ→còn quyền sau relog; học trùng/retry không mất đồ ngoài luật; danh mục 1★–4★ có nguồn hợp lệ, 5★ chỉ được cấp event/admin và không thể roll từ quái. Kiểm chứng dữ liệu recipe/asset không mồ côi. Khi tích hợp P16, dùng một công thức đã học qua ít nhất hai lần dung hợp/cường hoá hợp lệ vẫn còn quyền; từ chối recipe chưa học, sai pet, thiếu asset hoặc nguồn cấp không hợp lệ.

**Cần chốt ở phase detail trước implementation plan:** owner account/character; sao bản vẽ theo đầu ra; công thức chung/hai nhánh; loài/recipe đích; drop rate 1★–4★; duplicate/binding/trade; sự kiện và cấp admin; thời điểm nhận, túi đầy và nguồn hiển thị; không tự thiết kế schema/API hoặc công thức balance trong master plan.

### P03 — Quản lý pet, inventory và chuẩn bị lai tạo

**Outcome:** Bắt pet có ý nghĩa: xem được điểm mạnh, nuôi đúng hướng, chọn bố mẹ hiểu được chi phí và nhận thế hệ mới có thể sử dụng.

- **P03-R01:** Mapping domain→UI cho name/species/race/element/gender/star/level/XP, derived stats, quality/growth/resistances và appraisal visibility. Không dùng field gần nghĩa làm số liệu thay thế.
- **P03-R02:** Danh sách mang theo tối đa 3 pet, thứ tự slot quyết định pet đầu ra trận PvE; follower/active pet, sắp thứ tự ngoài trận/learn/release. Quyền đổi pet giữa trận chốt P02/P07; trạng thái retired không thể dùng lại. Tên/rename chỉ thêm khi chốt domain và validation.
- **P03-R03:** Inventory/shop tích hợp item rules P19 và bản vẽ/công thức P20: đúng icon đã map hoặc fallback rõ, count/stack, selection/detail, quantity/cost/confirmation; dùng item ngoài combat chỉ khi có rule tương ứng. Chốt capacity/storage ở sprint spec trước khi áp vào save đang có.
- **P03-R04:** Appraise/strengthen và chuẩn bị synthesis theo thiết kế P10/P16: chọn pet hợp lệ, giải thích từng điều kiện thiếu, trình bày chi phí và xác nhận tiêu hai pet; cơ chế chi tiết thuộc P16, không thêm scope preview/planner nâng cao từ Q05/Q06; kết quả dung hợp/trứng/con và phả hệ được tích hợp, nghiệm thu end-to-end ở P16. Không buộc mở companion web để hiểu kết quả.
- **P03-R05:** Recipe discovery/học công thức từ vật phẩm theo P20; learn skill theo NPC; companion journal/lineage đọc cùng dữ liệu. Trang bị là scope bắt buộc của P14; P03 tích hợp UI theo slot/stat rules đã chốt. Không dựng tab đồ giả.

- **P03-R06:** **Task review gameplay & game design bắt buộc:** Review giá trị của bắt/nuôi/chọn bố mẹ, khả năng hiểu stats/recipe, chi phí và hậu quả tiêu pet. Chơi flow từ quản lý pet đến sử dụng con lai, ghi số bước thừa và quyết định gây nhầm; kiểm tra portrait/sprite/biến thể giữ thiết kế hiện tại. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 pet/schema/inventory UX; S02 training/appraisal + recipe eligibility; S03 chọn bố mẹ/strengthening/lineage; phối hợp P14 về equipment và P16 về storage/trứng. Toàn bộ dung hợp nghiệm thu ở P16.

**Exit gate:** Qua UI thật bắt pet, xem/appraise chỉ số, học skill, quản lý trang bị/túi/kho và chọn hai bố mẹ; giải thích được điều kiện thiếu theo ruleset đã chọn. Giữ được dữ liệu sau login lại; release/strengthen/retry không mất hoặc nhân pet/tài nguyên ngoài luật. Vòng dung hợp ra trứng và nở con nghiệm thu tại P16; account sạch và pacing toàn vòng nghiệm thu tại P04.

### P16 — Trang trại tài khoản, dung hợp và vòng đời trứng

**Outcome:** Mỗi tài khoản có nơi quản lý đàn pet, chọn dung hợp nâng sao hoặc bổ trợ, nhận trứng và nuôi thế hệ mới.

- **P16-R01:** Farm instance riêng theo account, lưu tiến độ; vai trò quản lý pet/kho/ấp, NPC và quyền khách nếu chọn. Không tự thêm trồng trọt, xây nhà, sản xuất offline hoặc mua bán farm.
- **P16-R02:** Cả hai pet tối thiểu lv20; cần công thức tương ứng đã học theo P20, không tiêu lại bản vẽ mỗi lần; nhánh nâng sao cần hai pet cùng sao, lên đúng bậc kế tiếp khi có hình ảnh pet đích và ít nhất một bố mẹ thuộc hệ tộc đích. Chốt species/recipe đích, lựa chọn khi bố mẹ khác hệ, định nghĩa asset đủ dùng, chi phí/giới tính; cả hai nhánh tiêu cả hai pet và giữ phả hệ đã chốt. Nhánh bổ trợ dùng pet phụ bắt buộc cùng sao, giữ loài/hệ/sao pet chính, trả về trứng level 0 và tăng cường chỉ số/độ cộng. Không tự chọn đầu ra khác khi thiếu ảnh, không sinh 6★.
- **P16-R03:** Cả cường hoá và nâng sao đều ra trứng lv0; sau ấp là pet lv1, không giữ level chiến đấu bố mẹ. Trứng là trạng thái thật có ownership, dung lượng, điều kiện ấp/nở, hủy/di chuyển nếu được chọn và recovery khi offline/reconnect; không đổi tên child hiện tại thành “trứng” trong UI rồi coi đã xong.
- **P16-R04:** Con kế thừa stat/growth/resistance và learned skills theo P11/P13, có lợi ích từ chỉ số tăng theo level bố mẹ. Thiết kế độ cộng tối đa +99, cap gốc theo sao + độ cộng; ví dụ +00/+00→+03 và +03/+03→+07 chưa là công thức. Nâng sao reset +00; pet chính +99 không được cường hoá tiếp, không ép +99 mới cho nâng sao. Chốt công thức cặp khác độ cộng và khả năng dùng pet +99 ở slot phụ; bảo toàn phả hệ của cả hai bố mẹ đã tiêu/retire; không dùng lại bố mẹ làm nguyên liệu. 5★ +99 có nhánh đổi build không tăng chỉ số/cap, scope skill/phân bổ stat/chi phí cần chốt riêng, không reset + để mở lại cường hoá. Đồng bộ planner, journal và bách khoa; trang bị xử lý theo P14.
- **P16-R05:** Cơ chế dung hợp/cường hoá phải được trình bày rõ trong phase spec; không thêm preview/planner nâng cao bị từ chối. Review toàn vòng bắt–luyện–chọn bố mẹ–dung hợp–nhận trứng–nở–dùng con, số pet/kho cần có, thời gian lặp tới 5★; đo cả nhánh nâng sao và bổ trợ pet 5★. So sánh lặp lv20 với nuôi gần max; mô phỏng chặn cường hoá pet chính +99, chuyển stat qua pet phụ/cặp chênh +, reset + khi nâng sao và lặp nguyên liệu nhiều thế hệ. Trần chỉ số kế thừa là đề xuất bổ sung để chống vượt giới hạn, chưa chốt công thức.

**Exit gate:** Hai account có farm riêng; dùng lại công thức đã học qua nhiều lần dung hợp/cường hoá hợp lệ mà không cần thêm bản vẽ; UI hoàn thành vòng dung hợp/ấp/nở, con dùng được và lineage đúng sau relog. Retry/timeout ở mỗi bước không mất/nhân bố mẹ, trứng, đồ hoặc tiền; kiểm chứng +99 không cường hoá, nâng sao reset +00, trứng lv0→pet lv1, giới hạn 5★ và storage đầy. P04 tiếp tục đo vòng này từ account sạch.

### P04 — Onboarding, progression và content có phiên bản

**Outcome:** Từ tài khoản mới, người chơi tự biết bước tiếp theo và có đủ nội dung/tài nguyên hợp lý để đạt first synthesis rồi mở vùng mới.

- **P04-R01:** Quest chain giới thiệu di chuyển, NPC, combat, capture, heal, skill learning, appraisal, synthesis→trứng→nở và arena gate; contextual hints biến mất sau khi hiểu, không chiếm HUD lâu dài.
- **P04-R02:** Quest state/reward/marker/tracking nhất quán; điều kiện thiếu và đường quay lại NPC rõ; không nhận reward hai lần.
- **P04-R03:** Đo progression từ account sạch: thời gian trận, trận/bắt thành công, XP, tiền tiêu/thu, chi phí nuôi hai bố mẹ. Tách difficulty/cadence khỏi fidelity lịch sử; không tune bằng cảm giác hoặc cộng tài nguyên debug.
- **P04-R04:** Tích hợp active ruleset có version/provenance từ P10/P15/P16; lv20 và cap theo sao/độ cộng là luật sản phẩm đã chốt; level 30 và gender/race lịch sử là reference, không tự thay hai nhánh dung hợp của yêu cầu mới. Chuyển ruleset phải xác định save compatibility và công thức nào đổi.
- **P04-R05:** Tích hợp nguồn item/công thức P19/P20: 1★–4★ theo drop quái/vùng, 5★ chỉ sự kiện/admin, không để quest/drop thường lách luật 5★. Mở content theo vùng hoàn chỉnh: map/NPC/quests/spawns/pets/skills/recipes/items có source coverage, không tăng số lượng JSON rời rạc. Có validation IDs, economy sources/sinks và đường thoát soft-lock.

- **P04-R06:** **Task review gameplay & game design bắt buộc:** Review onboarding, động lực tiếp tục, độ khó, grind và sources/sinks từ account sạch. Đối chiếu thời gian tới first capture/synthesis/vùng mới và phản hồi người chơi; lặp tuning rồi chơi lại, ghi rõ thay đổi reconstruction so với nguồn. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 first expedition/quest chain; S02 first synthesis pacing; S03 arena→beach→next region + catalog versioning.

**Exit gate:** Ít nhất một playthrough account mới tới dung hợp, nở con sử dụng được và mở beach không cần trợ giúp debug; lần hai kiểm tra save/recovery và thứ tự quest khác. Report chỉ ra thời gian/chi phí thực đo, chỗ phải grind và quyết định tuning. Không có dead-end khi hết potion/seal/vàng hoặc pet gục.

### P05 — Fidelity, UX và solo alpha

**Outcome:** Một bản solo alpha dễ chạy, dễ đọc, trình bày nhất quán và có thể đưa người khác chơi thử.

- **P05-R01:** Hoàn thiện source mapping cho pet alpha, HUD, D-pad, shield, skill/item icons, panels/tabs/tooltips, background layers; ghi riêng asset khác phiên bản và chưa xác minh.
- **P05-R02:** Side-by-side từng màn major với timestamp; typography Việt/Latin/CJK, selection/focus, truncation, scaling và resize ổn định. Chốt logical viewport dựa trên so sánh 960×640 hiện tại và tỷ lệ video, không âm thầm co giãn độc lập các control.
- **P05-R03:** VFX/audio feedback cho thao tác, hit/capture/result/portal; volume/mute và nguồn sử dụng asset rõ trước khi phân phối. Không lấy âm thanh khác game để mặc nhiên coi là bản gốc.
- **P05-R04:** Account/logout/reconnect/settings/help thực dụng; bản build không phụ thuộc `.tools` của máy tác giả hoặc test script tự tạo account. User progress không bị mất vì đổi sang build mới.
- **P05-R05:** External playtest theo kịch bản P01–P04, ghi blocker/friction bằng thời điểm và repro; baseline memory/frame/network trên máy được chọn. Kiểm tra companion API/catalog parity.

- **P05-R06:** **Task review gameplay & game design bắt buộc:** Review toàn bộ solo loop với người chơi thử: hiểu mục tiêu, điều khiển, nhịp chơi, lựa chọn và chất lượng nghe/nhìn. Đóng visual debt POC trong phạm vi alpha theo ưu tiên ảnh hưởng người chơi; so sánh bộ ảnh chuẩn để bảo toàn thiết kế nhân vật/quái vật, ghi riêng nợ chất lượng còn lại trước release. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 asset/render/localization; S02 audio/settings/packaging; S03 solo alpha playtest và sửa blocker.

**Exit gate M1:** Tải/chạy/login→full solo loop→quit/login lại trên build phát hành thử; không debug controls, không mất dữ liệu và không blocker. Các fidelity gap còn lại có danh sách rõ. Không gắn nhãn “clone hoàn chỉnh”.

### P06 — Shared world và social nền tảng

**Outcome:** Hai người thật nhìn thấy và tương tác trong cùng một thế giới, không chỉ cùng kết nối tới API.

- **P06-R01:** Map/room ownership theo loại map P12, cô lập farm theo account P16 và quyền khách nếu được chọn; enter/leave, presence snapshot/delta, interest range và disconnect cleanup; không phát toàn bộ character/pet private state cho người khác.
- **P06-R02:** Remote actor interpolation, map transition và resync; quy tắc hai session cùng account phải chốt trước khi triển khai.
- **P06-R03:** Chọn private hay shared spawn cho từng loại nội dung; nếu shared, server giữ ownership/reservation/respawn và xử lý hai người cùng chạm. Không lấy latch của client làm khóa dùng chung.
- **P06-R04:** Nearby list và chat tối thiểu có identity, rate limit, mute/block; friends/invite state cần persisted contract. Không làm mọi channel ngay từ sprint đầu.

- **P06-R05:** **Task review gameplay & game design bắt buộc:** Review hai người cùng khám phá: nhận diện người khác, tranh/chia encounter, cảm giác đông map, nhiễu chat và khả năng tiếp tục solo. Playtest ownership/reconnect dưới góc nhìn công bằng và rõ ràng; kiểm tra remote actor không đổi tỷ lệ/phong cách thiết kế. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

- **P06-R06:** Đạt bộ kiểm thử 50 CCU tại mục 2: world fan-out, battle/mutation load, reconnect và client thật dưới tải. Profile rồi tối ưu interest range/delta cadence, queue/backpressure, contention, DB pool/query/checkpoint theo bottleneck đo được; không mặc định cần nhiều replica để đạt 50 CCU.

**Sprint đề xuất:** S01 two-client presence; S02 disconnect/resync + spawn ownership; S03 nearby/chat/friends tối thiểu; S04 tải 50 CCU và tuning/playtest đông người.

**Exit gate:** Hai client qua nhiều map thấy đúng nhau; reconnect không nhân đôi actor; không rò data; simultaneous contact có kết quả đúng thiết kế; đạt profile tải/fan-out 50 CCU và budgets đã khóa tại P00, kèm playtest client thật dưới tải và report review gameplay đông người.

### P07 — Party tối đa ba người và PvP ba pet mỗi bên

**Outcome:** Party tối đa 3 người, mỗi người điều khiển 1 pet khi đánh quái; hai người đấu PvP bằng đội 3 pet mỗi bên.

- **P07-R01:** Party tối đa 3 user; mỗi user góp 1 pet khi đánh quái. Invite/accept/leave/kick/disband, leader, disconnect/rejoin và quyền vào trận; UI dựa trên đoạn nearby/party của video.
- **P07-R02:** Tái sử dụng multi-target PvE P02, mở rộng command ownership nhiều user, team/formation, target chết/không hợp lệ, thứ tự và timeout. PvP có 3 pet mỗi người (3v3); chốt bố trí, lượt/auto, điều kiện thắng và trường hợp thiếu pet hợp lệ. Số quái/độ khó encounter party cần chốt riêng; không mặc định tăng theo 3 quái mỗi user. Tương thích battle đang lưu.
- **P07-R03:** Single/group/self skill mapping, synergy/triệt tiêu nhiều actor theo P13 và target UX, reconnect giữa lượt, auto/AFK policy không chiếm quyền người khác.
- **P07-R04:** Reward/capture ownership, loot/XP split và leave/disconnect outcomes được chốt trước code; game không trao cùng một vật/pet cho hai owner ngoài rule đã chọn.

- **P07-R05:** **Task review gameplay & game design bắt buộc:** Review phối hợp nhóm, vai trò/lựa chọn, thời gian chờ đồng đội, đọc target/turn, chia thưởng và AFK. Chơi nhóm thật rồi chỉnh pacing và feedback; đánh giá đội hình đông có che sprite/UI hoặc làm mất nhận diện nhân vật/quái vật không. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 party lifecycle tối đa 3 user; S02 battle ownership/renderer mỗi user 1 pet; S03 group skills/rewards/recovery và playtest party 2–3 user; S04 PvP 3v3, quyền điều khiển/thắng thua/reconnect. Sprint spec quyết định chi tiết sau.

**Exit gate M2:** Chơi party 2 rồi 3 client, mỗi người đúng 1 pet; từ chối người thứ tư. Hai client PvP có 3 pet mỗi bên, phân quyền command/target và thắng thua đúng; thành viên disconnect/timeout/leave không làm khóa trận hoặc nhân thưởng. Có replay/debug trace đủ hiểu command nào tạo kết quả nào.

**Ngoài scope:** PvP ranking/mùa giải và toàn bộ guild/auction; PvP cơ bản 3v3 nằm trong scope P07.

### P08 — Economy và meta mở rộng, chỉ triển khai nhánh đã chọn

**Outcome:** Mở rộng tương tác dài hạn mà không phá ownership hoặc economy đã kiểm chứng.

- **P08-R01:** Nền ledger/escrow và transaction nhiều account cho vật phẩm, pet, tiền; giới hạn tradable/bound/retired/active pet, idempotency và recovery. Một transaction aggregate đơn người hiện tại chưa đủ chứng minh an toàn.
- **P08-R02:** Mail delivery/claim/expiry có atomic claim; direct trade hai bên xác nhận cùng offer version; reject khi một bên đổi offer hoặc disconnect.
- **P08-R03:** Auction listing/bid/buyout/expiry/return/fee dựa trên escrow; concurrent buyers, retry và job restart không tạo duplication. UI companion chỉ dùng cùng authoritative API.
- **P08-R04:** Guild/permissions, PvP ranking/mùa giải (không gồm PvP cơ bản P07), daily/repeatable quest là các sub-spec riêng: chỉ vào sprint sau khi xác minh reference hoặc ghi rõ thiết kế reconstruction.

- **P08-R05:** **Task review gameplay & game design bắt buộc:** Review game design cho từng nhánh được chọn: động lực giao dịch/meta, nguồn-tiêu tài nguyên, công bằng, rủi ro nhầm offer và áp lực lặp nhiệm vụ. Đo hành vi và mô phỏng economy trước/sau tuning; không thêm daily/ranking chỉ để đủ checklist, không đổi art direction khi thêm nội dung. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

**Sprint đề xuất:** S01 ledger/escrow design + một flow hoàn chỉnh; S02 mail/trade; S03 auction; guild/ranking/daily tách track, không gom vào một sprint “social”.

**Exit gate:** Race/retry/crash tests cho mỗi loại chuyển quyền; conservation accounting; admin truy vết được mọi transfer. Chỉ bật các nhánh đạt gate. P08 có thể bỏ qua ở lần phát hành đầu.

### P17 — Một cốt truyện chính gắn với bản đồ

**Outcome:** Sau khi các hệ thống trong phạm vi phát hành ổn định, có một hành trình chính liền mạch với mở đầu, mục tiêu, cao trào và kết thúc.

- **P17-R01:** Viết premise, nhân vật/NPC chủ chốt và chương truyện theo world graph P12; mỗi map có lý do xuất hiện và vai trò trong hành trình, không chỉ tăng level quái.
- **P17-R02:** Gắn mốc truyện với khám phá, bắt/nuôi pet, dung hợp/trứng, skill, arena/boss và mở vùng đã kiểm chứng; không thêm mechanic lớn chỉ để cứu một đoạn truyện.
- **P17-R03:** Tích hợp quest/dialogue/objective/reward với P04; nhịp truyện tôn trọng thời gian training P15, có recap/tiếp tục khi quay lại, không soft-lock vì đã tiêu pet/vật phẩm trước khi nhận quest.
- **P17-R04:** Review tuyến chính từ đầu tới kết thúc ở account mới và save cũ. Để hook cho truyện phụ nhưng chưa viết hàng loạt nhánh, daily hoặc lore ngoài tuyến chính.

**Exit gate:** Một campaign chính chơi trọn vẹn qua các map trong scope, pacing/reward phù hợp và save/reconnect đúng; có story/gameplay review. Sau đó P09 kiểm định release trên chính build có campaign này.

### P09 — Release hardening và vận hành

**Outcome:** Build có thể triển khai, giám sát, phục hồi và nâng cấp mà không dựa vào thao tác thủ công của tác giả.

- **P09-R01:** Môi trường dev/staging/prod, config/secrets riêng; TLS xác minh chứng chỉ khi triển khai ngoài dev; không đưa opt-in insecure của workspace vào production mặc định.
- **P09-R02:** Release/version compatibility giữa client/protocol/catalog/schema; backup/restore diễn tập, migration forward/rollback hoặc restore strategy được thử trên bản sao.
- **P09-R03:** Logs/metrics/traces không chứa token/password; giám sát battle errors, mutation latency, checkpoint lag, socket count, save failures, memory và content mismatch.
- **P09-R04:** Load/soak/disconnect/restart/failure injection theo concurrency và cấu hình công bố. Kiểm tra nhiều server replica chỉ sau khi thiết kế ownership/cache invalidation tương ứng, không nhân bản process một cách mù quáng.
- **P09-R05:** Quy trình phát hành/rollback, operator tooling quyền tối thiểu, hỗ trợ người chơi, moderation nếu có social, lịch live content và chống abuse có bằng chứng.

- **P09-R06:** **Task review gameplay & game design bắt buộc:** Review gameplay/game design tổng thể trên release candidate: account mới và save cũ, cốt truyện chính P17, solo cùng online scope đã chọn, độ mượt, progression và recovery. Review hình ảnh ở chuẩn player-facing cuối cùng; xử lý visual debt chặn release, xác nhận nhân vật/quái vật giữ thiết kế gốc hiện tại và có kết luận go/no-go về trải nghiệm, không chỉ vận hành. Thực hiện đủ review đầu/trong/cuối phase và lưu report theo mục 2.

- **P09-R07:** Chạy lại toàn bộ gate 50 CCU trên release candidate và cấu hình gần production, bao gồm MySQL/TLS/network thực tế; chứng minh soak, headroom, reconnect và frame pacing client. So sánh với P06, sửa regression rồi đo lại trước go/no-go; ghi rõ cấu hình hỗ trợ 50 CCU và giới hạn đã đo.

**Sprint đề xuất:** S01 packaging/environment/restore; S02 load + observability + failure recovery; S03 release rehearsal và go/no-go.

**Exit gate M4:** Chốt nền tảng, cấu hình triển khai, DB latency và error budget của release; đạt tối thiểu 50 CCU theo bộ kiểm thử và budgets đã khóa; restore/migrate/reconnect thử thành công; không còn blocker mất/nhân dữ liệu. Chất lượng hình ảnh/âm thanh và gameplay phải đạt checklist player-facing đã chốt từ review P05/P09, không còn hạng mục POC chặn release; các sai khác còn chấp nhận phải được ghi rõ. P06 và gate 50 CCU là bắt buộc cho release online; P07 party/PvP cơ bản đã được chọn và phải đạt gate, P08 chỉ bắt buộc cho nhánh meta được công bố. Solo alpha là bản thử trung gian, không được thay thế release multiplayer.

### P18 — Truyện phụ và mở rộng nội dung sau tuyến chính

**Outcome:** Thế giới có chiều sâu và lý do quay lại vùng cũ sau khi tuyến chính đã hoàn chỉnh.

- **P18-R01:** Chọn từng cụm truyện phụ theo NPC/map/pet, dùng nền quest hiện có, có phần thưởng và điều kiện rõ; không tự mở thêm sao hoặc reset progression.
- **P18-R02:** Phân biệt truyện phụ kể chuyện với repeatable/daily ở P08; không bắt làm mọi nhánh mới hoàn thành được tuyến chính.
- **P18-R03:** Review tác động tới lore, economy, thứ tự quest/save cũ và nhịp khám phá; phát hành từng gói qua kiểm định hồi quy P09.

**Exit gate:** Mỗi gói có tuyến phụ hoàn chỉnh, không mâu thuẫn tuyến chính hoặc phá progression; chỉ lên lịch sau P17 và baseline P09. Không chặn bản phát hành đầu.

## 7. Quality gates chung

Các con số dưới đây là **mục tiêu đề xuất để chốt ở P00**, không phải thông số game gốc hoặc thành tích đã đạt toàn hệ thống:

| Mặt đo | Gate đề xuất | Cách lấy evidence |
|---|---|---|
| Frame pacing | Build 60Hz: p95 ≤16.7ms, p99 ≤33.3ms sau warmup trên máy baseline; ghi riêng cold-load spike | Route 10 phút gồm world/menu/battle; frame-time distribution, máy/build/resolution đi kèm |
| Input | Preview nhìn thấy ở frame kế tiếp khi không bị khóa; focus loss/keyup dừng đúng | Capture input và vị trí, không chỉ đo request latency |
| Network | Không mất intent, replay chi phí hoặc stuck khi RTT 50/150/300ms, jitter và reconnect | Fault scenarios có request/revision/event trace; không hứa mượt tuyệt đối mọi mạng |
| Online capacity | Tối thiểu 50 active CCU; soak 2 giờ, hot map và battle/mutation profiles theo mục 2 | Report server/DB/network + client thật dưới tải; reconnect/stress riêng; P06 và P09 bắt buộc |
| Persistence | Durable rewards/costs exactly-once theo request ID; movement rollback window được đo và công bố | Duplicate, timeout-after-commit, restart/checkpoint failure, restore |
| Visual | Mỗi major screen có reference/implementation pair; POC không là chuẩn release; giữ art direction nhân vật/quái vật | Kiểm tra idle, pressed, selected, disabled, loading/error và bộ ảnh chuẩn actor; phân loại visual debt alpha/release |
| Gameplay | Hoàn thành milestone từ account sạch không debug/DB edits; có review gameplay/game design đầu/trong/cuối mỗi phase | Playthrough UI thật + save/relogin, số đo pacing/friction, quyết định tuning và report review; không thay bằng mock-rich account |

Một sprint xong phải có: task review gameplay/game design thuộc scope đã thực hiện, kiểm tra giữ thiết kế nhân vật/quái vật và cập nhật report phase, scope acceptance đạt, test liên quan qua, manual scenario tương ứng, bằng chứng lỗi trước/sau nếu là bug, không regress flow đã có, docs/decision/evidence cập nhật và rollback/build xác định được.

## 8. Rủi ro và quyết định cần chốt ở phase sở hữu

| ID | Quyết định / rủi ro | Mặc định để planning | Gate cần chốt |
|---|---|---|---|
| D01 | Target release gốc có nhiều phiên bản | Blue/gold footage là presentation baseline; yêu cầu sản phẩm mới ưu tiên khi khác reconstruction cũ | P00 provenance; P10/P16 thiết kế; P04 tích hợp ruleset |
| D02 | Video chỉ 4:33, nhiều screen không có | Không bịa fidelity; APK/additional research tạo evidence riêng | Trước acceptance của screen thiếu nguồn |
| D03 | Desktop hay mobile trước | Desktop Godot/Mac baseline hiện tại; chưa cam kết touch mobile export | P05 platform scope |
| D04 | Private/shared spawn, respawn | Private contact cho solo; coordinate dựng lại phải được gắn nhãn | P01 lifecycle; P06 ownership |
| D05 | Combat/roster — **đã chốt** | Mang 3 pet; PvE pet đầu vs 3 quái auto; PvP 3 pet/người; party tối đa 3 user mỗi user 1 pet. Swap/lượt/PvP formation và enemy count party chốt tại phase | P02, P03, P07 |
| D06 | Equipment/capacity/storage | Trang bị pet bắt buộc theo yêu cầu mới; slot, capacity và compatibility chưa chốt | P14 equipment; P03 inventory; P16 farm/trứng |
| D07 | Cấu hình server/DB, latency và cost vận hành | Mục tiêu đã chốt: tối thiểu 50 active CCU; cấu hình và budgets khóa ở P00, không suy capacity từ local smoke | P00 budget/harness, P06 load gate, P09 release rerun |
| D08 | Rights/provenance khi phân phối asset | Lưu nguồn/hash/phạm vi sử dụng và asset cần thay | P05 build share, P09 release |
| D09 | Save đang tồn tại và test accounts | Giữ nguyên người dùng hiện có; test tách biệt; migration có recovery | Mọi sprint đổi schema/catalog semantics |
| D10 | Điều kiện success của progression | First synthesis là milestone chính; thời gian mục tiêu chọn sau khi đo | P04 tuning review |
| D11 | Cấu trúc 8 hệ — **đã chốt 2026-09-23** | 8 hệ tộc gắn với 8 hệ skill tương khắc; một số skill dùng chung cho cả 8; mỗi hệ có nhánh vật lý và phép riêng. Không tuyên bố đây là ma trận gốc đã xác minh | P10 chốt tên/ánh xạ; P13 thiết kế ma trận, hai nhánh và skill chung |
| D12 | Ngưỡng dung hợp — **đã chốt** | Lv20 đủ; level cao hơn làm chỉ số bố mẹ tăng và cho trứng tốt hơn khi các yếu tố khác tương đương; không bắt buộc max cấp | P11 kế thừa; P15 pacing; P16 eligibility |
| D13 | Nhánh nâng sao — **đã chốt hướng** | Hai pet cùng sao → bậc sao kế tiếp nếu có ảnh pet đích; ít nhất một bố mẹ cùng hệ tộc đích. Chưa chốt loài/recipe và cách chọn đích; không mở 6★ | P10/P16; asset coverage P05 |
| D14 | Tiêu nguyên liệu — **đã chốt**; recipe/giới tính còn mở | Cả hai nhánh tiêu cả hai pet để tạo một trứng; bố mẹ chỉ còn trong phả hệ, không dùng lại. Loài đầu ra/recipe, giới tính và slot chính/phụ chưa chốt toàn bộ | P16; đánh giá save và planner |
| D15 | Trang trại riêng và ấp trứng | Private theo account đã yêu cầu; quyền khách, capacity, thời gian/cách ấp chưa chọn | P12 phân loại; P16 lifecycle |
| D16 | Tương tác hệ theo chế độ | P02 single/group target PvE 1v3; P07 synergy party và PvP 3v3. Học/kế thừa khác hệ brainstorm sâu tại P13, chưa tự chốt mọi skill đều truyền | P13/P16 |
| D17 | Thứ tự cốt truyện | P17 sau hệ thống release đã chọn, trước P09; P18 sau tuyến chính | P17 campaign; P09 release |
| D18 | Level cap và độ cộng — **đã chốt luật nền** | Cap gốc 1★…5★ = 60/70/80/90/100; +00…+99 chỉ tăng cap, không trực tiếp tăng stat. +99 chặn cường hoá; nâng sao reset +00; không bắt buộc +99 mới được nâng sao. Công thức tăng + chưa chốt | P10/P11/P15/P16 |
| D19 | Eligibility bổ trợ — **đã chốt** | Pet phụ bắt buộc cùng sao; kết quả giữ loài/hệ/sao pet chính, về trứng lv0 và tăng chỉ số/độ cộng. Điều kiện hệ tộc pet phụ còn cần chốt | P16 trước spec |
| D20 | Chống lặp tăng sức mạnh vô hạn | +99 chặn cường hoá đã chốt. Đề xuất thêm trần kế thừa theo sao, tách stat level khỏi stat di truyền, kiểm tra đường chuyển qua donor và reset +. Chưa chốt công thức/hệ số | P11/P16; mô phỏng P15 |
| D21 | Vòng đời trứng và asset đầu ra | Cả hai nhánh ra trứng lv0, nở pet lv1 — đã chốt. Điều kiện ấp, ảnh/sprite cần cho nâng sao, trường hợp thiếu asset chưa chốt | P16/P05 |
| D22 | Items/EXP share — **đã chốt hướng** | Item chia EXP giữa tối đa 3 pet mang theo; thiếu item phải tự farm; tỷ lệ/cách kích hoạt/thời hạn/tiêu item/giới hạn chưa chốt | P19/P15 |
| D23 | Bản vẽ và công thức — **đã chốt** | Dùng bản vẽ 1 lần để học, công thức dùng lâu dài cho dung hợp/cường hoá; 1★–4★ rơi từ quái, 5★ chỉ event/admin, không rơi từ quái | P20/P19/P16 |
| D24 | Chi tiết quyền công thức | Sao nhãn gắn với pet đích là convention đề xuất; chốt owner account hay character, một công thức áp một hay hai nhánh, học trùng/binding/trade. Không tự biến đề xuất thành luật | P20 |

Không cần chốt tất cả ngay để bắt đầu P00. Phase không được tự ý lấp một quyết định chưa chốt bằng UI thành công giả hoặc cơ chế phá save.


### Các câu hỏi thiết kế tiếp theo sau khi chốt hai nhánh dung hợp

Các mục dưới là backlog interview của phase sở hữu, không mở rộng scope implementation hiện tại:

1. **P16 — Danh tính/phả hệ:** đã chốt cả hai nhánh tiêu cả hai pet, chỉ giữ bố mẹ trong phả hệ. Cần chốt cách biểu diễn cá thể con và liên kết ancestry để không tái sử dụng ID bố mẹ đã tiêu.
2. **P10/P16 — Độ cộng:** tăng theo cả hai bố mẹ, pet chính hay mức thấp hơn; khác độ cộng xử lý thế nào; nâng sao đã chốt reset +00, +99 đã chặn cường hoá. Có cho pet +99 làm donor của pet chính chưa +99 không, Đổi build ở 5★ +99 đã được cho phép nhưng không tăng chỉ số/cap; phạm vi và chi phí là gì? Ví dụ +03/+07 chưa đủ suy ra công thức.
3. **P11/P16 — Kế thừa:** phần chỉ số do luyện cấp đóng góp bao nhiêu, phần di truyền cũ mang sang ra sao; chỉ số nào có giới hạn/lợi suất giảm dần? Yêu cầu đối chiếu hai trứng ở cùng level và điều kiện khác tương đương để đo lợi ích luyện bố mẹ cao cấp.
4. **P10/P16 — Loài/hệ đầu ra:** chọn bố/mẹ chính hay recipe quyết định pet nâng sao khi bố mẹ khác hệ; cùng hệ nhưng khác loài có lên bất kỳ loài nào cùng hệ không? Nhánh bổ trợ có cho pet phụ khác hệ không?
5. **P13/P16 — Skill:** giữ skill pet chính, chọn skill pet phụ hay ngẫu nhiên; skill khác hệ có được kế thừa; giới hạn slot/skill phép-vật lý và skill chung ảnh hưởng thế nào tới bản sắc 8 hệ?
6. **P16 — Trứng:** đã chốt trứng lv0 và nở lv1; còn ấp theo thời gian, hoạt động hoặc vật liệu; cơ chế kết quả/chi phí được giải thích thế nào (không mở scope preview nâng cao); dung hợp có thất bại không và chi phí nào mất?
7. **P15 — Pacing:** mất bao lâu để tới lv20, first 2★/5★ và +99; XP curve ở level cao; pet 1★ +99 cap159 so với pet 5★ +00 cap100 phải có trade-off rõ, không dùng sao như thứ hạng sức mạnh tuyệt đối.
8. **P12/P15 — Thế giới:** mở map theo trainer, pet, arena hay quest; map thấp phải quay lại được để luyện pet mới nở; phân bố quái và drop công thức 1★–4★; nguồn pet cùng sao đủ cho vòng bổ trợ.
9. **P14/P16 — Trang bị và kho:** đồ bố mẹ trả về đâu, kho đầy thì chặn trước hay xử lý thế nào; trứng có chiếm slot pet không; không được mất đồ vì tiêu pet.

**Đã chốt:** độ cộng chỉ mở cap; nâng sao reset +00; trứng lv0 nở lv1. **Đề xuất để thử nghiệm, chưa chốt công thức:** giới hạn phần chỉ số kế thừa theo sao; không để buff/trang bị ảnh hưởng trứng; so sánh mô phỏng lặp lv20 với luyện gần max và các cặp chênh độ cộng. Không cần dùng cùng một công thức cho cả tốc độ tăng + và chất lượng di truyền.

### Nghiên cứu giới hạn sức mạnh — cập nhật cùng lượt chốt cap/reset

**Nguồn đối chiếu:** [trang chính thức Pokémon Sword/Shield về nuôi Pokémon](https://swordshield.pokemon.com/en-gb/gameplay/features-raise-pokemon/) phân biệt thay đổi hướng tăng trưởng, base points có thể đạt mức tối đa, XP/level và Egg Moves. Tham khảo nguyên tắc tách các nguồn sức mạnh và đặt giới hạn; không lấy công thức Pokémon làm công thức Phimond, không dùng nguồn này để tuyên bố level bố mẹ truyền sang con trong Pokémon. Các phương án dưới là phân tích thiết kế riêng, chưa phải kết quả mô phỏng hoặc luật game gốc.

| Phương án | Tác dụng | Giới hạn / quyết định |
|---|---|---|
| Chỉ chặn cường hoá ở +99 | Giới hạn đường tăng + của pet chính | Đã chốt nhưng chưa đủ: stat có thể chuyển qua donor có + thấp hơn, hoặc bị cộng lặp khi nâng sao reset + |
| Giảm dần phần stat thêm qua thế hệ | Giảm tốc độ tăng và khuyến khích bố mẹ tốt | Không tự chứng minh có trần; tổng các lần tăng nhỏ vẫn có thể tăng không giới hạn |
| Trần kế thừa theo sao + tách nguồn stat + lợi ích luyện cấp có giới hạn | Chặn vượt ngân sách dù đổi vai chính/phụ hoặc qua nhiều thế hệ, vẫn thưởng luyện bố mẹ cao cấp | **Khuyến nghị để P11/P16 thiết kế**, cần định nghĩa per-stat/tổng budget và cách mang kế thừa sang sao mới |

**Ràng buộc đề xuất cho phase thiết kế, chưa khóa công thức:**

- Tách stat nền theo loài/sao, stat thực sự tăng do luyện level, phần di truyền có sẵn và hiệu ứng tạm/trang bị. Không cộng nguyên tổng stat chiến đấu của cả hai bố mẹ rồi lại cộng tiếp toàn bộ di truyền cũ vào trứng.
- Tính chất lượng kế thừa từ đóng góp có giới hạn của cả hai bố mẹ. Khi các yếu tố khác tương đương và chưa bão hoà, luyện lv60+ phải cho chất lượng trứng tốt hơn lv20. Nếu có RNG, lợi ích phải được kiểm chứng qua phân bố và giải thích trong luật dung hợp; không hứa mọi lần roll đều tốt hơn.
- Giới hạn phần kế thừa theo bậc sao/loài/vai trò; kiểm chứng ngân sách sao cao tại cùng level. Trần phải áp cả đầu ra cường hoá và đầu ra nâng sao, không chỉ kiểm tra trường +xx.
- Khi nâng sao: reset +00 và level về trứng lv0→nở lv1 đã chốt; phần kế thừa được chuyển vào ngân sách bậc mới theo luật cần chốt, không mặc nhiên xóa công luyện bố mẹ hoặc mang nguyên stat lv159 sang pet lv1.
- Độ cộng đầu ra cường hoá nên tiến lên so với pet chính, giới hạn +99; nếu không còn tăng được thì từ chối trước khi tiêu nguyên liệu. Đây là đề xuất cho công thức +, không suy ra chuỗi +03/+07 là luật số đã chốt. Trần kế thừa vẫn bảo vệ trường hợp đổi slot hoặc cho donor + cao.
- Ở 1★–4★ +99, muốn tiếp tục phát triển qua dung hợp phải nâng sao với pet cùng sao, đủ level và đầu ra hợp lệ có ảnh; thiếu đầu ra phải báo rõ, không âm thầm đổi pet hoặc cho cường hoá vượt trần. Không buộc pet chưa +99 phải chờ tới +99 mới nâng sao.
- 5★ +99 không thể nâng lên 6★ trong scope này; vẫn luyện tới lv199/chơi bình thường. Đã chốt cho đổi build không tăng chỉ số/cap, bằng thao tác riêng. Chưa chốt đổi skill hay phân bổ lại stat trong ngân sách cũ; không tự cho reset + hoặc tái sinh để đi vòng luật. Đổi build có thể cải thiện matchup/chiến thuật, không đồng nghĩa được cộng thêm chỉ số thô.

**Bằng chứng cần có khi vào P11/P15/P16:** so sánh cùng level khác sao; 1★ lv159 với 5★ lv1 theo sức mạnh chỉ số; bố mẹ lv20 với lv60+; lặp nhiều đời; cặp chênh + và đảo slot chính/phụ; donor +99; nâng sao reset +00; trần 5★ +99; không nhận lợi ích di truyền từ đồ/buff. Đo cả chất lượng trứng và chi phí/thời gian, không chỉ kiểm tra số stat hữu hạn. Chưa chạy mô phỏng balance vì công thức chưa được chọn.

**Quyết định bổ sung đã xác nhận:** cả hai nhánh dung hợp tiêu cả hai pet, lưu ancestry; 5★ +99 được đổi build không tăng chỉ số/cap. P13/P16 phải chốt danh sách thứ được đổi, chi phí và tác động tới level/skill trước triển khai; không mặc định thao tác đổi build cũng tiêu hai pet hoặc tạo trứng như dung hợp.

## 9. Sprint đầu tiên nên chọn

**P00-S01 — Baseline active client, canonical checks và reference ledger.** Thứ tự thống nhất với mục 6; xem [Implementation plan chi tiết P00](phases/P00-baseline/P00-implementation-plan.md).

- S01 bao phủ P00-R01/R03/R05 và review đầu phase P00-R06: restore point, active commands, baseline gameplay, ledger và bộ ảnh chuẩn actor.
- S02 xử lý P00-R02/F01/F02: live event bridge, terminal presentation, reconnect; giữ privacy và server rules. Có review gameplay sau thay đổi.
- S03 xử lý P00-R04 và review cuối phase: metrics/harness cho 50 CCU, fault baseline, evidence và quyết định exit gate.
- Không gộp particle/skill mới, rework map, party, balance hoặc rewrite architecture vào P00.
- Chỉ đánh dấu P00 hoàn thành khi cả ba sprint và exit gate có bằng chứng; plan đã viết không có nghĩa code đã triển khai.

## 10. Nguồn nội bộ và cách cập nhật

- [Video audit toàn timeline](../../docs/research/VIDEO_UI_AUDIT_2026-09-23.md)
- [Gallery đối chiếu](../../docs/research/ui-comparison-2026-09-23/index.html)
- [UI verification và giới hạn](../../docs/research/UI_RECONSTRUCTION_VERIFICATION_2026-09-23.md)
- [Contact playtest](../../docs/research/CONTACT_PLAYTEST_2026-09-23.md)
- [Historical fidelity ledger — có đoạn cũ cần đọc theo ngày](../../docs/research/fidelity.md)
- [Protocol hiện tại](../../packages/protocol/README.md)
- [Client entry/manual checks](../../apps/game-client/README.md)

Khi hoàn thành sprint: cập nhật requirement ID, link sprint spec/implementation plan/evidence, trạng thái `planned → in progress → verified`, và phần baseline bị thay thế. Giữ lịch sử quyết định; không ghi đè một phỏng đoán thành “confirmed” chỉ vì đã implement.
