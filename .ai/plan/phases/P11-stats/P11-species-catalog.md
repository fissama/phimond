# P11 — 152 Species catalog v1

Status: **DESIGN COMPLETE; NOT RUNTIME-ACTIVATED**, 2026-10-12.

These are Phimond authoring decisions under the owner’s delegated P11 completion scope. The frozen roster remains unchanged. This companion JSON is the complete stat/Element/role design, not a replacement runtime dataset, save migration, recovered APK table or P13 skill implementation.

## Provenance and constraints

- 152 frozen IDs: 135 Normal, 4 Special4★, 13 Special5★. Names, Race, Star, class, source IDs, assets and recipes remain frozen in their existing files; no art or parent recipe is edited.
- 97 source descriptions are quoted verbatim in JSON as qualitative evidence. The other 55 remain explicitly missing; their roles and all Element placements are intentional Phimond authoring, never claimed as recovered source behavior.
- Element IDs: `fire`, `water`, `wind`, `earth`, `light`, `dark`. Ice themes use water and thunder themes use wind in this initial vocabulary. This is an explicit design simplification, not an APK fact. No automatic Race mapping, stat multiplier, STAB or element chart is supplied.
- Primary describes dominant intended native function; optional Secondary describes a usable supporting function. JSON records both concrete thematic rationale and the P13 native-pool function contract. P13 must realize these roles through concrete skills or explicitly reopen the assignment. No skill is granted here.
- Poison/burn damage alone does not justify Disruptor; assigned Disruptors require control/impairment beyond HP loss. Self-only recovery/resistance alone does not justify Support.
- Budget/template version: accepted P11 Q10/Q11 main shares, 75/25 blend, main budgets 100/110/122/136/160, Special148/172, growth2% of main base target; approved SR/SPD factors. Exact intermediates are Decimal. Nearest integer base and nearest .001 growth use half-up authoring quantization, then every constraint is checked. This is catalog-authoring quantization, not a change to gameplay floor rules.
- V1 chooses no extra species jitter: the small recorded modifiers come solely from quantization. Species with the same Star/class/role blend may share numeric vectors intentionally. Future distinct tuning must stay inside the same approved bounds and receive its own revision; raw budgets do not certify combat balance.
- Base and growth guards run separately; modifiers, exact templates and realized normalized main budgets are included per record. Roles do not constrain owned-Pet inherited totals.

## Reproduce / validate

From repository root:

```sh
rtk proxy python3 .ai/plan/phases/P11-stats/evidence/build_species_catalog.py --write
rtk proxy python3 .ai/plan/phases/P11-stats/evidence/build_species_catalog.py --check
```

The builder writes only these design artifacts and static evidence. `--check` independently checks committed JSON constraints and exact deterministic reproduction, without writing. It is not a stat engine or gameplay simulation. Source file hashes bind this catalog to the frozen inputs.

## Assignment ledger

P=physical_dps, M=magic_dps, T=tank, S=support, D=disruptor, H=hybrid. “Missing” means source description absent, not authoring incomplete. Full six-stat values and provenance are in `P11-species-catalog.json`.

| ID | Name | Element | Primary / Secondary | Source prose | Phimond design rationale |
|---|---|---|---|---|---|
| species_0001 | Nhện Vong Linh | dark | physical_dps | Present | spectral physical hunter |
| species_0002 | Chiến Sĩ Đầu Lâu | earth | tank / support | Present | durable bone guard with ally healing |
| species_0003 | Cua Hắc Ám | dark | physical_dps / tank | Present | dark claw attacker with bulk |
| species_0004 | Xác Ướp | dark | magic_dps | Present | curse caster; resistance is not a control skill |
| species_0005 | Xác Chết Ác Ma | earth | tank | Present | slow durable corpse wall |
| species_0006 | U Linh | dark | magic_dps | Present | spectral vitality caster |
| species_0007 | Chó Ác Ma | fire | physical_dps | Present | aggressive infernal physical hound |
| species_0008 | Lửa Yêu | fire | magic_dps / support | Present | flame caster with single-target recovery |
| species_0009 | Xác Chết Vuốt Sắc | dark | physical_dps | Missing | authored claw attacker; source prose absent |
| species_0010 | Cá Xương | water | physical_dps / tank | Present | aquatic bone bruiser |
| species_0011 | Kẻ Đồ Tể | dark | physical_dps | Present | counterattacking butcher |
| species_0012 | Xác Chết Nửa Người | dark | tank / disruptor | Present | bulky curse controller |
| species_0013 | Ma Ảnh | dark | physical_dps / support | Present | physical shade with cleanse support |
| species_0014 | Tinh Tinh Xanh Ma Giới | earth | magic_dps / support | Present | forest occult caster with ally buffs |
| species_0015 | Tử Thần | dark | physical_dps / support | Present | death-themed attacker with petrification cleanse |
| species_0016 | Pharaon | dark | magic_dps / disruptor | Present | confusion caster |
| species_0017 | Rồng Xương Băng | water | physical_dps / tank | Present | ice-themed physical dragon |
| species_0018 | Nữ Vương Bạch Cốt | dark | magic_dps / support | Missing | authored bone queen with ally protection |
| species_0019 | Nữ Đế Minh Giới | dark | magic_dps / disruptor | Missing | authored underworld control caster |
| species_0020 | Thủ Lĩnh Hắc Ám | dark | tank / physical_dps | Missing | authored armored dark commander |
| species_0021 | Xương Rồng | earth | tank | Missing | authored thorn guard |
| species_0022 | Yêu Tinh Hoa | light | support / magic_dps | Missing | authored flower healer with magic fallback |
| species_0023 | Nấm Hoa | earth | disruptor | Missing | authored fungal action inhibition, beyond poison damage |
| species_0024 | Tinh Tinh Xanh | earth | magic_dps | Missing | authored woodland caster |
| species_0025 | Hải Quỳ | water | magic_dps | Present | concealed aquatic group caster |
| species_0026 | Gỗ Quỷ | earth | physical_dps / tank | Present | strong living-wood bruiser |
| species_0027 | Quả Mặt Quỷ | dark | disruptor | Missing | authored fright and attack-debuff fruit |
| species_0028 | Thủy Linh | water | support / magic_dps | Present | team healer with aquatic magic |
| species_0029 | Trúc Địa Linh | earth | tank / support | Present | bamboo guard with recovery |
| species_0030 | Hoa Ăn Thịt Người | earth | physical_dps / disruptor | Missing | authored biting plant with binding |
| species_0031 | Yêu Tinh Dứa | earth | physical_dps | Present | repeated physical damage does not imply Disruptor |
| species_0032 | Hoa Môi | earth | physical_dps / tank | Present | sturdy flower fighter |
| species_0033 | Hoa Hướng Dương | light | magic_dps / disruptor | Present | light-themed caster with defense reduction |
| species_0034 | Bí Đỏ Quỷ Quái | dark | tank / disruptor | Present | pumpkin guard with binding |
| species_0035 | Trưởng Lão Người Cây | earth | tank / support | Missing | authored elder tree protector |
| species_0036 | Hoa ăn Thịt Người Ba Đầu | earth | physical_dps / tank | Present | multiheaded plant bruiser |
| species_0037 | Độc Đằng Nữ | earth | disruptor / magic_dps | Missing | authored vine binding and magic; poison alone insufficient |
| species_0038 | Tinh Linh Bách Hoa | light | support / tank | Present | flower spirit team recovery with defensive emphasis |
| species_0039 | Rồng Có Cánh | wind | physical_dps | Present | fast winged physical attacker |
| species_0040 | Rồng Mào Đỏ | fire | physical_dps | Present | red dragon physical offense |
| species_0041 | Rắn Xương Trắng | earth | magic_dps / tank | Present | intelligent resilient bone serpent |
| species_0042 | Tiểu Ma Long | dark | hybrid / support | Present | physical and magic dragon with minor healing |
| species_0043 | Rồng Cổ Dài | earth | tank / disruptor | Present | high-vitality dragon with weakening |
| species_0044 | Rồng Vuốt Xương | earth | physical_dps / disruptor | Present | claw attacker with defense reduction |
| species_0045 | Nham Long | earth | tank / magic_dps | Present | rock dragon with magic support offense |
| species_0046 | Giáp Long Răng Nhọn | earth | magic_dps | Present | armored magic attacker with self enhancement |
| species_0047 | Viêm Long | fire | physical_dps / support | Present | flame dragon with ally combat support |
| species_0048 | Rồng Sấm | wind | magic_dps | Present | thunder-themed magic dragon |
| species_0049 | Rồng Phỉ Thúy | earth | disruptor / tank | Present | weakening-focused durable emerald dragon |
| species_0050 | Hải Long Ba Đầu | water | magic_dps / disruptor | Present | water caster with action control |
| species_0051 | Long Vương Hắc Ám | dark | hybrid | Missing | authored dark dragon dual damage |
| species_0052 | Thánh Rồng Thái Cổ | light | hybrid / support | Missing | authored ancient holy dragon with protection |
| species_0053 | Tiểu Ác Ma | fire | magic_dps | Missing | authored small infernal caster |
| species_0054 | Yêu Tinh Biển | water | physical_dps / support | Present | fast sea attacker with recovery |
| species_0055 | Mắt Ác Ma | dark | magic_dps / support | Present | eye caster with healing |
| species_0056 | Ma Móng Rồng | dark | physical_dps / tank | Present | armored demonic claw fighter |
| species_0057 | Báo Địa Ngục | fire | hybrid | Present | infernal agile dual attacker |
| species_0058 | Chó Săn Ác Ma | fire | physical_dps | Missing | authored infernal hunting hound |
| species_0059 | Tướng Chiến Ma Rồng | fire | physical_dps / tank | Present | resilient demonic warrior |
| species_0060 | Ma Thú Địa Ngục | earth | tank / physical_dps | Present | counterattacking durable beast |
| species_0061 | Lợn Ác Ma | dark | magic_dps | Present | broadly balanced demonic caster |
| species_0062 | Quái Vật Đầu Dê | dark | magic_dps / disruptor | Present | caster reducing enemy physical offense |
| species_0063 | Ma Tướng Địa Ngục | fire | physical_dps / tank | Present | slow powerful demon general |
| species_0064 | Ma Muội | dark | disruptor | Present | binding dancer and attack debuffer |
| species_0065 | Thầy Bói Ác Ma | dark | magic_dps | Present | divination-themed high magic attacker |
| species_0066 | Đại Ác Ma | dark | magic_dps / disruptor | Present | magic attacker with offensive debuffs |
| species_0067 | Ma Vương Địa Ngục | fire | physical_dps / tank | Present | durable infernal physical king |
| species_0068 | Thanh Long | water | hybrid | Missing | authored azure dragon dual damage |
| species_0069 | Trụy Thiên Sứ | dark | support / magic_dps | Missing | authored fallen angel protective magic |
| species_0070 | Thú Móng Lớn | earth | physical_dps | Missing | authored large-claw beast |
| species_0071 | Ưng Đỏ | fire | physical_dps | Missing | authored red raptor physical offense |
| species_0072 | Ma Cây | earth | tank / disruptor | Missing | authored living tree guard with roots |
| species_0073 | Rùa Phú Quý | water | tank / support | Missing | authored turtle guard with ally protection |
| species_0074 | Sói Ngớ Ngẩn | earth | physical_dps | Missing | authored grounded wolf hunter |
| species_0075 | Tê Tê Vàng | earth | tank | Missing | authored armored pangolin |
| species_0076 | Thú Răng Kiếm | earth | physical_dps | Missing | authored saber-tooth attacker |
| species_0077 | Thiên Nga Cực Địa | water | physical_dps / support | Present | polar bird with ally buffs |
| species_0078 | Dương Dương Dương | earth | support | Missing | authored flock protector with recovery |
| species_0079 | Mực Hắc Ám | water | disruptor / magic_dps | Missing | authored ink-based accuracy impairment and magic |
| species_0080 | Gấu Vết Dao | earth | physical_dps / tank | Missing | authored sturdy scarred bear |
| species_0081 | Rùa Nham Thạch | fire | tank / support | Present | lava turtle with group buffs |
| species_0082 | Voi Tai To | earth | physical_dps / tank | Present | high-vitality physical elephant |
| species_0083 | Cáo Chín Đuôi | fire | magic_dps / support | Present | fox caster with ally resource support |
| species_0084 | Tinh Tinh Rock | earth | tank / disruptor | Present | vitality-focused ape with binding |
| species_0085 | Đại Tuyết Quái | water | physical_dps / disruptor | Present | snow attacker with blindness |
| species_0086 | Gấu Trúc Ma Pháp | light | magic_dps | Present | eastern magic panda |
| species_0087 | Bạch Hổ | wind | physical_dps | Missing | authored swift white tiger |
| species_0088 | Sói Xích Viêm | fire | physical_dps | Missing | authored flame wolf hunter |
| species_0089 | Chim Ong | wind | physical_dps / support | Present | small bird attacker with recovery |
| species_0090 | Dơi | dark | disruptor | Missing | authored bat disorientation beyond HP damage |
| species_0091 | Chim Chào Mào | wind | physical_dps | Missing | authored crested aerial attacker |
| species_0092 | Chim Sấm | wind | physical_dps / tank | Present | thunder bird with physical group attack |
| species_0093 | Ưng Trọc Ma | dark | physical_dps / support | Present | swift dark raptor with healing |
| species_0094 | Chim Cú | wind | magic_dps | Missing | authored owl wind caster |
| species_0095 | Ưng Trọc | wind | physical_dps | Missing | authored aerial scavenger fighter |
| species_0096 | Nữ Yêu Minh Ưng | dark | magic_dps | Present | dark harpy caster |
| species_0097 | Dơi Một Mắt | dark | magic_dps / disruptor | Present | vitality caster with slowing |
| species_0098 | Quạ Nghĩa Trang | dark | physical_dps / support | Present | grave raven with ally speed support |
| species_0099 | Tê Điểu | wind | physical_dps | Present | physical bird; self resistance does not imply Support |
| species_0100 | Vẹt Độc Vuốt | wind | physical_dps | Missing | authored poison-claw attacker; poison not control |
| species_0101 | Đại Bàng Sư Tử | wind | physical_dps / disruptor | Present | griffin attacker with slowing |
| species_0102 | Ưng Hồng Vũ | fire | magic_dps | Present | red-feather caster with self speed |
| species_0103 | Chim Đại Phì | wind | disruptor / magic_dps | Present | sleep and group slow with magic fallback |
| species_0104 | Chim Đa Đa | wind | physical_dps / support | Present | bird attacker with speed and silence cleanse |
| species_0105 | Chu Tước | fire | magic_dps / support | Missing | authored vermilion bird with recovery |
| species_0106 | Chim Cú Địa Ngục | dark | magic_dps / disruptor | Present | fast infernal owl with slowing |
| species_0107 | Đại Bàng Vàng | light | physical_dps | Missing | authored golden eagle physical offense |
| species_0108 | Ong Giết Người | earth | physical_dps | Present | venom attacker; no control role from venom alone |
| species_0109 | Bọ Cạp Sa Mạc | earth | magic_dps | Present | earth magic scorpion directly described in source |
| species_0110 | Bọ Ngựa Móng Sắt | earth | tank / physical_dps | Present | armored mantis physical guard |
| species_0111 | Ốc Sên Hoa | water | tank | Present | heavily defended snail |
| species_0112 | Nhện Độc | earth | physical_dps | Present | authored mountain spider claw offense |
| species_0113 | Thiên Ngưu | earth | hybrid | Present | explicitly physical and magic beetle |
| species_0114 | Bọ Cánh Cứng Răng Kiếm | earth | physical_dps / tank | Missing | authored armored saber beetle |
| species_0115 | Giun Đất Móng Sắt | earth | physical_dps / disruptor | Present | burrowing attacker with max-HP debuff |
| species_0116 | Châu Chấu Móng Lớn | earth | magic_dps | Present | magic and poison locust; poison not control |
| species_0117 | Thú Một Sừng Vỏ Cứng | earth | magic_dps / tank | Present | sturdy magic beetle with self vitality |
| species_0118 | Bướm Hoa Vũ | wind | support / magic_dps | Present | butterfly group healing with magic fallback |
| species_0119 | Cua Ký Sinh | water | tank / hybrid | Present | aquatic guard with both damage modes |
| species_0120 | Tôm Hùm Răng Cưa | water | physical_dps / support | Present | lobster with curse cleanse and ally vitality |
| species_0121 | Hải Mã Bong Bóng | water | magic_dps / disruptor | Present | sea caster with max-HP impairment |
| species_0122 | Trùng Hốt Lỗ | dark | magic_dps / disruptor | Present | curse insect with misfortune impairment |
| species_0123 | Trùng Gai Nhọn | earth | physical_dps / disruptor | Present | physical insect with petrification |
| species_0124 | Trùng Bất Tử Địa Huyệt | earth | tank | Missing | authored durable underground insect |
| species_0125 | Nhện Phu Nhân | light | magic_dps | Present | vitality-focused spirit-touched caster |
| species_0126 | Trùng Mẫu Mào Vàng | earth | support / disruptor | Missing | authored brood protector with enemy binding |
| species_0127 | Quái Vật Rương Báu | earth | physical_dps / support | Present | chest fighter with recovery |
| species_0128 | Chong Chóng Gió | wind | magic_dps | Present | wind construct area magic |
| species_0129 | Quái Vật Nham Thạch | fire | physical_dps / tank | Present | lava physical bruiser |
| species_0130 | Đá Mặt Quỷ | earth | tank | Present | stone guard with petrification resistance |
| species_0131 | Hư Không Hắc Ám | dark | magic_dps | Present | void caster with speed emphasis reserved for skills |
| species_0132 | Sách Ma Pháp | light | magic_dps / support | Present | spellbook caster with healing |
| species_0133 | Ma Kiếm | dark | physical_dps | Present | magic sword physical attack with self vitality |
| species_0134 | Con Rối Gạch Đá | earth | physical_dps / disruptor | Present | stone construct with weakening |
| species_0135 | Thằng Hề Hộp | dark | magic_dps / tank | Present | sturdy magic jack-in-box |
| species_0136 | Chiến Sĩ Bù Nhìn | earth | disruptor / physical_dps | Missing | authored scarecrow binding and physical fallback |
| species_0137 | Ma Gương Thủy Tinh | light | magic_dps / disruptor | Present | reflective caster with misfortune impairment |
| species_0138 | Thú Lớn Dung Nham | fire | physical_dps / disruptor | Present | lava bruiser with group magic-offense debuff |
| species_0139 | Huyền Vũ | water | tank / support | Missing | authored sacred turtle protector |
| species_0140 | Nhân Sư | earth | hybrid | Missing | authored sphinx dual attacker |
| species_0141 | Totem Thượng Cổ | earth | support / magic_dps | Missing | authored totem ally buffs with magic fallback |
| species_0142 | Thần Tướng Cự Ma | earth | physical_dps / tank | Missing | authored giant warrior bruiser |
| species_0143 | Thần Đèn | wind | magic_dps / support | Missing | authored djinn with ally protection |
| species_0144 | Linh Tiên Hoa Hương | light | support / magic_dps | Missing | authored flower spirit healer |
| species_0145 | Cây Cự Linh | earth | tank / support | Missing | authored great tree protector |
| species_0146 | Ma Vương Hút Máu | dark | magic_dps | Missing | authored vampiric caster; self recovery not Support |
| species_0147 | Người Tuyết Viễn Cổ | water | tank / physical_dps | Missing | authored ancient snow guard |
| species_0148 | Ngựa Bùn Cỏ | earth | physical_dps / support | Missing | authored grass-mud mount with ally protection |
| species_0149 | Thú Vàng Một Sừng | light | physical_dps | Missing | authored golden unicorn attacker |
| species_0150 | Đảo Thiên Đường | water | tank / support | Missing | authored island guardian with ally protection |
| species_0151 | Đại Vương Bọ Cạp | earth | physical_dps / disruptor | Missing | authored scorpion king with binding beyond poison |
| species_0152 | Chim Ái Thần | light | support / magic_dps | Missing | authored love bird healer with magic fallback |

## Downstream acceptance

P13 owns the interaction chart, skill formulas/eligibility and actual native pools. P02/P07 own battle-mode viability testing; P15 owns pacing. Content activation and legacy14→152 mapping require a later additive implementation delivery with migration/rollback review. Passing this static catalog validator establishes only the approved numeric constraints and frozen-identity coverage.
