> Active review: **P13 candidate V7** — catalog **160 species**, **97 skills**, **28 recipe candidates**. Role/stats/MP/Native Pool changes and two new Hybrid signatures supersede the older 152-species roster statements below. See [P13-owner-feedback-v7.md](P13-owner-feedback-v7.md), [roster-review-package.json](roster-review-package.json), and [P13-candidate-species-catalog-160.json](P13-candidate-species-catalog-160.json). Core combat/learning contracts below remain the baseline. **Owner accepted V7.1 on 2026-10-20 (design closed, see [P13-closure.md](P13-closure.md)); runtime and P10/P11 promotion remain separate.**

# P13 — Skill pet/quái và tương tác giữa các hệ

**Status: CANDIDATE — owner acceptance pending.** Date: 2026-10-13. Runtime chưa kích hoạt.

## Outcome
Bản v3: giữ skill APK Nhẹ/Thường/Cao cấp/Siêu cấp riêng để farm ít MP; làm rõ đơn thể/AoE và damage/hiệu ứng; kiểm tra cả8 Race có pet vật lý lẫn phép. 7 signature Special mới giữ nguyên.

## Authority
P10/P11 accepted decisions giữ nguyên. Các P13-D dưới đây là đề xuất do agent lựa chọn theo quyền owner giao; chưa phải owner approval. Source facts xem P13-source-audit.md. Handoff/closure sau nghiệm thu.

## Traceability
P13-R01/R01a/R01b: D02–D04,D15,D16. R02: D05–D14. R03: D09,D14,D16. R04: D04,D17. R05: D10–D14,D18. R06: D04,D15 và 152 native pools.

## Decisions

### P13-D01 — Giữ skill nhẹ và tier gốc APK
7 chuỗi AoE giữ4 skill riêng Nhẹ/Thường/Cao cấp/Siêu cấp, đúng tên và ID nguồn. Trị liệu nhóm/siêu cấp cũng riêng. Tier không gộp rank; học tier mạnh vẫn giữ tier nhẹ.

Rationale: Owner yêu cầu farm ítMP. Source target/channel/name có chứng cứ; Mana/Dame raw chưa hiểu encoding, numbers Phimond riêng. APK3.2/8.4 vẫn đối chiếu13conflicts.

Acceptance:
- 60sourceIDs đều mapping;28AoE source tier có28candidateIDs riêng.
- Tier cao không xóa/thay/khóa tier thấp.

Downstream: Runtime thuộc P02; tên source, số authored.

### P13-D02 — Giữ 6 slot: đủ vai trò, còn đánh đổi
6 current skill + basic riêng, signature cũng chiếm1 slot. Native/Inherited là pool lựa chọn, không phải tất cả đều phải mang vào trận; newborn0, re-hatch giữ skill/rank.

Rationale: Review owner: 4 slot dễ bó hẹp pet hai role; 6 chứa 2 hướng damage + phòng thủ + hồi/cleanse + control + signature. 8 slot dễ mang quá nhiều đáp án, tăng pool truyền current và UI. Basic0MP riêng giúp kit không cần tốn slot cho fallback. Đây là lập luận thiết kế, chưa phải playtest.

Acceptance:
- 0/6 vẫn basic được; rank không chiếm thêm slot.
- Học khi6/6 cần replacement + xác nhận; không slot7 riêng cho Special.
- P02/P07 so kit4/6/8 cùng pool/MP/stats/AI, đo role coverage, skill usage, thời lượng trận, control pressure; owner duyệt trước thay limit.

Downstream: P03/P16 giữ6; P02/P07 chứng minh bằng trận thật. Xem P13-owner-feedback-v2.md.

### P13-D03 — Học tier riêng, giữ skill farm ítMP
Common strike/heal/guard. AoE APK và2groupheal tier cố địnhrank1, học từngID, mang nhẹ+mạnh chiếm2slot. 7signature mới cố địnhrank1. Damage/heal khác rank1–3: power/heal×1.15/1.30,MPceil×1.20/1.40, effects/CD không đổi; rank2Lvmax(20,base+15),rank3max(40,base+30). Giá học20+10×level;upgrade2/3=3×/6×base;relearn20%base.

Rationale: Tier là skillID riêng; rank là upgrade cùngID. Không auto-upgrade nhẹ, không nhânrank AoE tier. Giá học vẫn ứng viên P19.

Acceptance:
- Native/inherit/current lưu từngtierID; học tier cao không consume tier thấp.
- Full6/6 thay đúng skill đã chọn, không thay cảfamily.
- Tier MP/CD cố định, không có rank2/3 cho cácfamily này.

Downstream: P03/P16 snapshots; P19 pacing.

### P13-D04 — Eligibility và độc quyền từng species
Native được học theo species pool. Inheritance chỉ Race whitelist mỗi skill; khác Element không loại. Revive/dragon_breath/death_scythe/love_kiss không truyền. 7 signature mới có exclusive_species, chỉ loài đó được học; inheritance rỗng, không vào common hoặc pool loài khác.

Rationale: Giữ bản sắc và lựa chọn donor. No RNG chọn skill, chỉ current skills truyền. Độc quyền gắn species ID, không dùng Race/Star làm quyền chung. Signature dùng active cost, rank1 cố định.

Acceptance:
- Union→dedupe→filter deterministic;7 signature luôn bị lọc khỏi inheritance.
- Giữ inherited pool qua hoàn nguyên; quên current không xóa pool.
- Species thay đổi không được auto cấp/giữ quyền signature của species cũ; P16 kiểm tra ownership trước giao dịch.

Downstream: P16 snapshots/migration version; P03 trước-sau. 7 signature là Phimond-authored, không claim source mechanics.

### P13-D05 — Ma trận 6 Element
Hỏa>Phong>Địa>Thủy>Hỏa: thuận1.25×, nghịch0.80×; Quang/Âm khắc nhau1.25×; còn lại1×. Basic và neutral1×.

Rationale: Thay chart cực đoan bằng chênh lệch vừa; không miễn nhiễm damage theo Element/Race.

Acceptance:
- 36 ô đủ; chart không đi từ Race.
- Skill khác Element vẫn dùng bình thường.

Downstream: Numeric candidate; P02/P07 balance phải đo.

### P13-D06 — Damage vật lý/phép
Base=offense×power×100/(100+DEF); nhân chart, crit; floor một lần. Offense0→0, offense>0 damage tối thiểu1. Physical ATK; magic MAG; basic neutral1.00×ATK.

Rationale: Một DEF P11; tránh phép subtraction khiến low level hoàn toàn vô dụng.

Acceptance:
- ATK100,DEF50,power1.2: thuận100; nghịch64.
- HP loss dùng min(damage,currentHP), không overkill.

Downstream: P02 exact rational + replay.

### P13-D07 — Đơn thể/AoE; damage và hiệu ứng
Mỗi skill có single/AoE và damage thuần/damage+effect/effect khôngdamage. AoE4tier power mỗi target .45/.75/1.05/1.35;physicalMP10/18/26/36,magicMP12/20/28/38;learnLv1/5/20/40;CD0/1/1/2. Hit95%,blind−20pp clamp50–95;crit5%×1.50 cho directdamage.

Rationale: Power đã là mỗi target, không nhân thêm .75. Poison/burn códamage+effect; sleep/bind/debuff/cleanse khôngdamage. Hit/crit/status riêng mỗi target; DoT/heal/control khôngcrit.

Acceptance:
- Web card và filter có target shape/effect mode.
- Offense100,DEF50 neutral khôngcrit: mỗi target30/50/70/90, đủ3hit tổng90/150/210/270.
- Farm3quái25HP: nhẹ/mạnh đều đủkill nếuhit, nhẹ tiết kiệmMP.
- Dead targets không nhận hit/proc, AoEheal chỉ ally sống.

Downstream: Numbers Phimond; P02/P07 đo balance.

### P13-D08 — MP, cooldown và action
MP cost trả một lần khi action hợp lệ bắt đầu; miss vẫn tốn. CD C: cast vòngR dùng lại từR+C+1. Một actor1 action/vòng; CD không thêm action. Không passive regen/end-battle refill.

Rationale: Tuân MP P11. Dùng skill retained Lv1 theo MP thực, không khóa level lần nữa.

Acceptance:
- Không đủ MP: auto fallback basic.
- Invalid request không mất MP/action; retry không trừ hai lần.

Downstream: P19 items có account cooldown riêng.

### P13-D09 — Vòng, SPD và replay
Đầu vòng chốt list actor sống theo SPD P11, random rank battle khi hòa. Không resort giữa vòng. Dead trước action bị bỏ; revive lên action vòng sau.

Rationale: P11 SPD không tự thêm lượt. Chọn vòng rõ để buff/control đo được.

Acceptance:
- Haste cast giữa vòng chỉ đổi order vòng sau.
- Reconnect trả snapshot/event cursor, không reroll rank.

Downstream: P02 scheduling; P07 command deadline30s, timeout auto.

### P13-D10 — Status, SR và duration
p_final=p_base×(1−0.8×SR/(SR+100));1 draw/status sau hit. Base chances ghi từng skill. Buff/debuff2 vòng castR hết cuốiR+2; DoT/regen tickR+1,R+2, không tick ngay.

Rationale: Kháng status không xóa direct damage. DoT snapshot offense; DEF/chart target lúc tick, không crit.

Acceptance:
- p75%,SR100→45%.
- SR không giảm damage/tick/duration; cleanse remove được.

Downstream: P02 event order/disconnect tests.

### P13-D11 — Control và chống khóa liên tục
Sleep/petrify/confuse tối đa1 action; không stack với nhau. Khi trigger, expire hoặc cleanse: control grace đến cuối vòng kế tiếp, không nhận3 status đó. Bind/silence2 vòng nhưng không chặn mọi action cùng lúc: status đến sau bị reject khi trạng thái kia còn hoạt động.

Rationale: Solo1v3 cần đường thoát. NPC trainer không cứu pet đang sleep trong combat. Basic còn dùng được khi silence; bind cho phép magic/support.

Acceptance:
- Sleep bị direct damage đánh thức, không double damage.
- Petrify vẫn nhận damage, chỉ DEF+25%.
- Confuse basic random địch sống, không friendly fire.

Downstream: P07 kiểm chứng control pressure3v3.

### P13-D12 — Stack, DoT và pipeline
Cùng status giữ potency lớn hơn, refresh có trần2 vòng kể từ lần apply mới; tối đa poison+burn,1 stack/type. Buff cùng stat giữ strongest positive; debuff strongest negative; khác nhóm cộng theo P11. Battle percent stat clamp tổng−50%..+50%.

Rationale: No multiplicative infinite stack; reapply vẫn tiêuMP/action/CD, grace chặn hard lock. Không buff maxHP trong v1.

Acceptance:
- Gear/buff không vào inheritance.
- Counter tối đa1/vòng, không reaction cascade.

Downstream: P14 phối hợp item/equipment effect budgets.

### P13-D13 — Triệt tiêu và tăng cường
Cleanse chuyên biệt MP8/CD1; genericMP16/CD2 gỡ1 status theo priority. Water hit thành công dập burn trên target (sau damage, trước status mới); mọi rank như nhau. Không phản ứng dây chuyền/free damage. Buff ATK/MAG/SPD hỗ trợ đồng đội theo role.

Rationale: Giải trạng thái là lựa chọn rõ; source7 cleanse được giữ tên. Counter chart, synergy buff và cleanse là3 trục riêng.

Acceptance:
- Dispel gỡbuff không quaSR nhưng kiểm tra hit.
- Cleanse target không có trạng thái phù hợp không mất cost.

Downstream: P02 single/group; P07 multi-owner.

### P13-D14 — Shield, hồi phục và revive
Heal1.50×MAG+10; group thường0.85×MAG+6/28MP/CD2; group siêu cấp1.10×MAG+10/40MP/CD3 mỗi ally sống, họcLv40, riêngID/rank1. Shield1.20×MAG+8%maxHP nguồn,2 vòng; shield cùng loại giữ lớn hơn, không stack. Revive35MP/CD4 họcLv40:25%HP, không refillMP,1 lần/actor/battle, không self.

Rationale: P11 không tự heal. Source passive rebirth/regeneration thành paid active; kiss thành shield thay immunity.

Acceptance:
- Heal không hồi sinh.
- Shield nhận trướcHP, drain tính HP mất.
- Ally-fainted không hợp lệ trong PvE solo1pet.

Downstream: P07 revive; P02 announce unavailability.

### P13-D15 — Native pools (160 loài) + 9 signature Special4★/5★ (tiêu đề gốc v3: 152 pools + 7 signature)

> **V7 update:** pools nay phủ 160 loài (152 + 8 proposal) và có 9 signature (7 + 2 Hybrid Special 5★). Nội dung bên dưới là bản v3 giữ làm baseline; số liệu hiện hành xem README.
Giữ Race/Element/Star/roles P11. Special4: Thanh Long–Triều áp(Thủy/slow), Bạch Hổ–Phong trảo(Phong/selfhaste), Chu Tước–Ly hỏa(Hỏa/burn), Huyền Vũ–Thủy giáp(Thủy/shield+gỡburn). Special5: Nữ Đế–Minh ấn(Âm/antiheal), Cự Ma–Địa chấn hộ thể(Địa/selfarmor), Hoa Hương–Quang tịnh(Quang/heal+cleanse). Mỗi signature1/6slot, rank1, CD3;4★ họcLv30/24MP;5★ Lv40/28MP. Pool mở đủtier nhẹ→siêu cấp theo damage channel. Mỗi Race có≥2 primaryphysical và≥2 primarymagic; web có số lượng, ví dụ và gaps theoStar, không claim mỗiStar đều đủ.

Rationale: Giá trị Special đến từ nén hai công dụng phù hợp role vào1action có cost/CD, không tăng stats P11 hay tự thắng. Hiệu ứng tận dụng status/buff hiện có; Element chart chỉ tăng damage, không khuếch đại heal/shield/status. Đây là đề xuất authored sau owner review, không recovered source.

Acceptance:
- 152 IDs đủ, role/reference hợp lệ;27 loài cùng stats khác pool.
- 7 signature chỉ xuất hiện ở7 species sở hữu, đủ6Element, cả4★/5★; sample build vẫn≤6.
- MP/CD/counterplay rõ; buffs không stack loại cũ, không control mới/instant kill.
- P02/P07 so Special có/không signature và Normal cùng level/grade; không chứng nhận balance từ static checks.

Downstream: Candidate cần owner duyệt D15 lại; P02/P07 kit review, Special operation gates P16/P20 giữ nguyên.

### P13-D16 — Quái, auto và targeting
Quái dùng native subset theo level: mỗi lượt lọc skill hợp lệ, priority control chưa có→heal ally<40%→AoE>=2địch→buff chưa có→single; tie pool order. Tier auto theo thứ tự người chơi chọn trong6skill, không tự ưu tiên tier mạnh. Farm kit nên đặt nhẹ trước mạnh; burst kit đổi thứ tự trước trận; quái tie pool order nhẹ trước mạnh. Pet mặc định heal ally/self<40% → cleanse cần thiết → control chưa có/grace-free → buff chưa có → AoE>=2 → single → basic.

Rationale: Không quái tự có mọi skill; không macro nâng cao. Target enemy_single mặc địnhHP thấp nhất, hòa stableID; ally heal%HP thấp nhất.

Acceptance:
- PvE solo1pet vs3quái, party3người×1pet, PvP3pet/bên.
- Một mode khóa target phải báo rõ; không mất MP khi invalid.

Downstream: P02 PvE implementation; P07 arena formation separate.

### P13-D17 — Save, event và retry contract
Version p13-candidate-v1; learning intent idempotency key + expected pet revision; costs+replace atomic. Battle events có instance/source/target/skill/rank/sequence/hit/crit/status outcomes; client trình bày kết quả server.

Rationale: Inherited skills rank reset1 lúc học con; preserved current giữ rank. Migration legacy14→152 cần mapping rõ, không guess.

Acceptance:
- Retry/reconnect không double-charge/replay.
- Snapshot không lộ seed/RNG/hidden appraisal.

Downstream: P02/P03/P16 migration và atomic integration.

### P13-D18 — Exit gate và giới hạn cân bằng
Candidate cần owner acceptance qua web; arithmetic/catalog checks chỉ chứng minh consistency. P02/P07 đo trận thật, P15/P19 đo chi phí học và retraining; không claim50CCU/balance.

Rationale: Handoff chỉ tạo sau owner acceptance, đính exact candidate hash và unresolved dispositions.

Acceptance:
- Có examples damage, neutral, counter, synergy, cleanse,0skills.
- Feedback được lưu theo hash; owner có thể từ chối từng nhóm.

Downstream: Design ready for review, closure pending.

## Content artifacts
- (V7 hiện hành: roster-review-package.json — 160 species, 97 skills, 28 recipe candidates; P13-candidate-species-catalog-160.json.)
- P13-skill-catalog.json (V7.1, 97 skills; bản 95 skill ở evidence/P13-skill-catalog-v3-95.json): all concrete skills, functions, power/effects, cost, CD, learn gate, inheritance whitelist and source mapping.
- P13-species-pools.json (pre-V7): 152 explicit species pools + illustrative builds of up to6 skills; builds assume required learning levels and paid learning.
- review-package.json: exact candidate shown in web, combining decisions/catalog/chart/scenarios/evidence.
- P13-behavior-contract.md: timing, transaction, input/result and error semantics.

## Phase gate
Candidate prepared and statically checked. Owner acceptance PENDING. P02/P07 live, balance and save migration remain separate release blockers. Numeric consistency is not measured kit balance. No handoff/closure yet.
