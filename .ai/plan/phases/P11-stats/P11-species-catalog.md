# P11 — 152 Species catalog v2: Race and Species identity

Status: **AUTHORED DESIGN; NOT RUNTIME-ACTIVATED**, 2026-10-12.

These are Phimond authoring decisions under the owner’s delegated P11 completion scope. The frozen roster remains unchanged. This companion JSON is the complete stat/Element/role design, not a replacement runtime dataset, save migration, recovered APK table or P13 skill implementation.

## Provenance and constraints

- 152 frozen IDs: 135 Normal, 4 Special4★, 13 Special5★. Names, Race, Star, class, source IDs, assets and recipes remain frozen in their existing files; no art or parent recipe is edited.
- 97 source descriptions are quoted verbatim in JSON as qualitative evidence. The other 55 remain explicitly missing; their roles and all Element placements are intentional Phimond authoring, never claimed as recovered source behavior.
- Element IDs: `fire`, `water`, `wind`, `earth`, `light`, `dark`. Ice themes use water and thunder themes use wind in this initial vocabulary. This is an explicit design simplification, not an APK fact. No automatic Race mapping, stat multiplier, STAB or element chart is supplied.
- Primary describes dominant intended native function; optional Secondary describes a usable supporting function. JSON records both concrete thematic rationale and the P13 native-pool function contract. P13 must realize these roles through concrete skills or explicitly reopen the assignment. No skill is granted here.
- Poison/burn damage alone does not justify Disruptor; assigned Disruptors require control/impairment beyond HP loss. Self-only recovery/resistance alone does not justify Support.
- Budget/template version: accepted P11 Q10/Q11 main shares, 75/25 blend, main budgets 100/110/122/136/160, Special148/172, growth2% of main base target; approved SR/SPD factors. Exact intermediates are Decimal. Nearest integer base and nearest .001 growth use half-up authoring quantization, with representable main-band clamping; Bird SPD and Undead SR use floor-to-grid of their exact +5% upper bounds; every constraint is checked. This is catalog-authoring quantization, not a change to gameplay floor rules.
- V1.1 encodes the owner-approved Bird SPD priority inside Species base/growth: the highest representable value at or below 105% of the exact SPD target. V2 adds budget-conserving main-stat Race emphases and explicit per-Species accents; Undead SR uses the same upper-band flooring. At the same Star/class, ordered role blend, level and SPD grade, Bird grown SPD is strictly higher. Different roles, inheritance, equipment and effects can change matchup order. This is an authoring rule, not a runtime Race multiplier. The other seven Race directions were owner-approved; concrete modifier strengths are delegated authoring choices. Function briefs require P13 skills; broader combat balance remains unverified.
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
| species_0001 | Âm Chu | dark | physical_dps | Present | spectral physical hunter |
| species_0002 | Cốt Binh | earth | tank / support | Present | durable bone guard with ally healing |
| species_0003 | Hắc Giải | dark | physical_dps / tank | Present | dark claw attacker with bulk |
| species_0004 | Triền Thi | dark | magic_dps | Present | curse caster; resistance is not a control skill |
| species_0005 | Cự Thi | earth | tank | Present | slow durable corpse wall |
| species_0006 | Tử Hồn | dark | magic_dps | Present | spectral vitality caster |
| species_0007 | Thi Lang | fire | physical_dps | Present | aggressive infernal physical hound |
| species_0008 | Quỷ Hỏa | fire | magic_dps / support | Present | flame caster with single-target recovery |
| species_0009 | Lợi Trảo Thi | dark | physical_dps | Missing | authored claw attacker; source prose absent |
| species_0010 | Cốt Ngư | water | physical_dps / tank | Present | aquatic bone bruiser |
| species_0011 | Đồ Phu | dark | physical_dps | Present | counterattacking butcher |
| species_0012 | Tàn Thi | dark | tank / disruptor | Present | bulky curse controller |
| species_0013 | Ma Ảnh | dark | physical_dps / support | Present | physical shade with cleanse support |
| species_0014 | Phệ Hồn Thảo | earth | magic_dps / support | Present | forest occult caster with ally buffs |
| species_0015 | Tử Thần | dark | physical_dps / support | Present | death-themed attacker with petrification cleanse |
| species_0016 | Sa Thi Vương | dark | magic_dps / disruptor | Present | confusion caster |
| species_0017 | Băng Cốt Long | water | physical_dps / tank | Present | ice-themed physical dragon |
| species_0018 | Bạch Cốt Nữ Vương | dark | magic_dps / support | Missing | authored bone queen with ally protection |
| species_0019 | Minh Giới Nữ Đế | dark | magic_dps / disruptor | Missing | authored underworld control caster |
| species_0020 | Hắc Kỵ Vương | dark | tank / physical_dps | Missing | authored armored dark commander |
| species_0021 | Tiên Chưởng | earth | tank | Missing | authored thorn guard |
| species_0022 | Hoa Tinh | light | support / magic_dps | Missing | authored flower healer with magic fallback |
| species_0023 | Xích Linh Chi | earth | disruptor | Missing | authored fungal action inhibition, beyond poison damage |
| species_0024 | Bích Hồ Thảo | earth | magic_dps | Missing | authored woodland caster |
| species_0025 | Hải Quỳ | water | magic_dps | Present | concealed aquatic group caster |
| species_0026 | Quỷ Mộc | earth | physical_dps / tank | Present | strong living-wood bruiser |
| species_0027 | Quỷ Diện Quả | dark | disruptor | Missing | authored fright and attack-debuff fruit |
| species_0028 | Thủy Linh | water | support / magic_dps | Present | team healer with aquatic magic |
| species_0029 | Trúc Linh | earth | tank / support | Present | bamboo guard with recovery |
| species_0030 | Thực Nhân Hoa | earth | physical_dps / disruptor | Missing | authored biting plant with binding |
| species_0031 | Kim Thứ Quả | earth | physical_dps | Present | repeated physical damage does not imply Disruptor |
| species_0032 | Chu Thần Hoa | earth | physical_dps / tank | Present | sturdy flower fighter |
| species_0033 | Thái Dương Hoa | light | magic_dps / disruptor | Present | light-themed caster with defense reduction |
| species_0034 | Quỷ Nam Qua | dark | tank / disruptor | Present | pumpkin guard with binding |
| species_0035 | Mộc Trưởng Lão | earth | tank / support | Missing | authored elder tree protector |
| species_0036 | Tam Thủ Thực Hoa | earth | physical_dps / tank | Present | multiheaded plant bruiser |
| species_0037 | Độc Đằng Nữ | earth | disruptor / magic_dps | Missing | authored vine binding and magic; poison alone insufficient |
| species_0038 | Bách Hoa Tiên Tử | light | support / tank | Present | flower spirit team recovery with defensive emphasis |
| species_0039 | Dực Long | wind | physical_dps | Present | fast winged physical attacker |
| species_0040 | Xích Quan Long | fire | physical_dps | Present | red dragon physical offense |
| species_0041 | Cốt Xà | earth | magic_dps / tank | Present | intelligent resilient bone serpent |
| species_0042 | Tiểu Ma Long | dark | hybrid / support | Present | physical and magic dragon with minor healing |
| species_0043 | Thứ Bối Long | earth | tank / disruptor | Present | high-vitality dragon with weakening |
| species_0044 | Cốt Trảo Long | earth | physical_dps / disruptor | Present | claw attacker with defense reduction |
| species_0045 | Nham Long | earth | tank / magic_dps | Present | rock dragon with magic support offense |
| species_0046 | Tiêm Nha Long | earth | magic_dps | Present | armored magic attacker with self enhancement |
| species_0047 | Viêm Long | fire | physical_dps / support | Present | flame dragon with ally combat support |
| species_0048 | Lôi Long | wind | magic_dps | Present | thunder-themed magic dragon |
| species_0049 | Phỉ Thúy Long | earth | disruptor / tank | Present | weakening-focused durable emerald dragon |
| species_0050 | Tam Thủ Hải Long | water | magic_dps / disruptor | Present | water caster with action control |
| species_0051 | Hắc Long Vương | dark | hybrid | Missing | authored dark dragon dual damage |
| species_0052 | Thái Cổ Thánh Long | light | hybrid / support | Missing | authored ancient holy dragon with protection |
| species_0053 | Tiểu Ác Ma | fire | magic_dps | Missing | authored small infernal caster |
| species_0054 | Hải Yêu | water | physical_dps / support | Present | fast sea attacker with recovery |
| species_0055 | Tiểu Ma Nhãn | dark | magic_dps / support | Present | eye caster with healing |
| species_0056 | Long Trảo Quỷ | dark | physical_dps / tank | Present | armored demonic claw fighter |
| species_0057 | Dạ Xoa | fire | hybrid | Present | infernal agile dual attacker |
| species_0058 | Ngục Khuyển | fire | physical_dps | Missing | authored infernal hunting hound |
| species_0059 | Ma Giáp Binh | fire | physical_dps / tank | Present | resilient demonic warrior |
| species_0060 | Ngục Thú | earth | tank / physical_dps | Present | counterattacking durable beast |
| species_0061 | Ma Trư | dark | magic_dps | Present | broadly balanced demonic caster |
| species_0062 | Dương Đầu Ma | dark | magic_dps / disruptor | Present | caster reducing enemy physical offense |
| species_0063 | Ma Tướng | fire | physical_dps / tank | Present | slow powerful demon general |
| species_0064 | Ma Cơ | dark | disruptor | Present | binding dancer and attack debuffer |
| species_0065 | Chiêm Tinh Quỷ | dark | magic_dps | Present | divination-themed high magic attacker |
| species_0066 | Đại Ác Ma | dark | magic_dps / disruptor | Present | magic attacker with offensive debuffs |
| species_0067 | Địa Ngục Ma Vương | fire | physical_dps / tank | Present | durable infernal physical king |
| species_0068 | Thanh Long | water | hybrid | Missing | authored azure dragon dual damage |
| species_0069 | Đọa Thiên Sứ | dark | support / magic_dps | Missing | authored fallen angel protective magic |
| species_0070 | Kim Chủy Thú | earth | physical_dps | Missing | authored large-claw beast |
| species_0071 | Xích Ưng | fire | physical_dps | Missing | authored red raptor physical offense |
| species_0072 | Lâm Yêu | earth | tank / disruptor | Missing | authored living tree guard with roots |
| species_0073 | Phú Quý Quy | water | tank / support | Missing | authored turtle guard with ally protection |
| species_0074 | Lam Lang | earth | physical_dps | Missing | authored grounded wolf hunter |
| species_0075 | Xuyên Sơn Giáp | earth | tank | Missing | authored armored pangolin |
| species_0076 | Kiếm Xỉ Hổ | earth | physical_dps | Missing | authored saber-tooth attacker |
| species_0077 | Cực Băng Nga | water | physical_dps / support | Present | polar bird with ally buffs |
| species_0078 | Miên Dương | earth | support | Missing | authored flock protector with recovery |
| species_0079 | Mặc Ngư | water | disruptor / magic_dps | Missing | authored ink-based accuracy impairment and magic |
| species_0080 | Đao Ba Hùng | earth | physical_dps / tank | Missing | authored sturdy scarred bear |
| species_0081 | Nham Quy | fire | tank / support | Present | lava turtle with group buffs |
| species_0082 | Cự Nhĩ Tượng | earth | physical_dps / tank | Present | high-vitality physical elephant |
| species_0083 | Cửu Vĩ Hồ | fire | magic_dps / support | Present | fox caster with ally resource support |
| species_0084 | Thạch Viên | earth | tank / disruptor | Present | vitality-focused ape with binding |
| species_0085 | Tuyết Mao Quái | water | physical_dps / disruptor | Present | snow attacker with blindness |
| species_0086 | Ma Pháp Hùng Miêu | light | magic_dps | Present | eastern magic panda |
| species_0087 | Bạch Hổ | wind | physical_dps | Missing | authored swift white tiger |
| species_0088 | Xích Viêm Lang | fire | physical_dps | Missing | authored flame wolf hunter |
| species_0089 | Phong Điểu | wind | physical_dps / support | Present | small bird attacker with recovery |
| species_0090 | Biên Bức | dark | disruptor | Missing | authored bat disorientation beyond HP damage |
| species_0091 | Hoa Quan Điểu | wind | physical_dps | Missing | authored crested aerial attacker |
| species_0092 | Lôi Điểu | wind | physical_dps / tank | Present | thunder bird with physical group attack |
| species_0093 | Ma Ưng | dark | physical_dps / support | Present | swift dark raptor with healing |
| species_0094 | Dạ Kiêu | wind | magic_dps | Missing | authored owl wind caster |
| species_0095 | Thiết Ưng | wind | physical_dps | Missing | authored aerial scavenger fighter |
| species_0096 | Ưng Yêu | dark | magic_dps | Present | dark harpy caster |
| species_0097 | Độc Nhãn Bức | dark | magic_dps / disruptor | Present | vitality caster with slowing |
| species_0098 | Mộ Nha | dark | physical_dps / support | Present | grave raven with ally speed support |
| species_0099 | Tê Điểu | wind | physical_dps | Present | physical bird; self resistance does not imply Support |
| species_0100 | Độc Trảo Anh Vũ | wind | physical_dps | Missing | authored poison-claw attacker; poison not control |
| species_0101 | Sư Thứu | wind | physical_dps / disruptor | Present | griffin attacker with slowing |
| species_0102 | Hồng Vũ Ưng | fire | magic_dps | Present | red-feather caster with self speed |
| species_0103 | Đại Phúc Điểu | wind | disruptor / magic_dps | Present | sleep and group slow with magic fallback |
| species_0104 | Liệt Phong Ưng | wind | physical_dps / support | Present | bird attacker with speed and silence cleanse |
| species_0105 | Chu Tước | fire | magic_dps / support | Missing | authored vermilion bird with recovery |
| species_0106 | Địa Ngục Quái Điểu | dark | magic_dps / disruptor | Present | fast infernal owl with slowing |
| species_0107 | Kim Sí Đại Bằng | wind | physical_dps | Missing | owner-approved wind eagle physical offense; golden plumage is visual theme |
| species_0108 | Độc Phong | earth | physical_dps | Present | venom attacker; no control role from venom alone |
| species_0109 | Sa Hạt | earth | magic_dps | Present | earth magic scorpion directly described in source |
| species_0110 | Thiết Đường Lang | earth | tank / physical_dps | Present | armored mantis physical guard |
| species_0111 | Hoa Loa | water | tank | Present | heavily defended snail |
| species_0112 | Sơn Chu | earth | physical_dps | Present | authored mountain spider claw offense |
| species_0113 | Thiên Ngưu | earth | hybrid | Present | explicitly physical and magic beetle |
| species_0114 | Kiếm Giáp Trùng | earth | physical_dps / tank | Missing | authored armored saber beetle |
| species_0115 | Thứ Sa Trùng | earth | physical_dps / disruptor | Present | burrowing attacker with max-HP debuff |
| species_0116 | Cự Trảo Trùng | earth | magic_dps | Present | magic and poison locust; poison not control |
| species_0117 | Độc Giác Trùng | earth | magic_dps / tank | Present | sturdy magic beetle with self vitality |
| species_0118 | Hoa Vũ Điệp | wind | support / magic_dps | Present | butterfly group healing with magic fallback |
| species_0119 | Ký Cư Giải | water | tank / hybrid | Present | aquatic guard with both damage modes |
| species_0120 | Cự Ngao Hà | water | physical_dps / support | Present | lobster with curse cleanse and ally vitality |
| species_0121 | Thủy Bào Hải Mã | water | magic_dps / disruptor | Present | sea caster with max-HP impairment |
| species_0122 | Ách Vận Trùng | dark | magic_dps / disruptor | Present | curse insect with misfortune impairment |
| species_0123 | Thạch Thứ Trùng | earth | physical_dps / disruptor | Present | physical insect with petrification |
| species_0124 | Địa Huyệt Ma Trùng | earth | tank | Missing | authored durable underground insect |
| species_0125 | Điệp Hậu | light | magic_dps | Present | vitality-focused spirit-touched caster |
| species_0126 | Kim Quan Chu Hậu | earth | support / disruptor | Missing | authored brood protector with enemy binding |
| species_0127 | Bảo Tương Yêu | earth | physical_dps / support | Present | chest fighter with recovery |
| species_0128 | Phong Xa Linh | wind | magic_dps | Present | wind construct area magic |
| species_0129 | Nham Quái | fire | physical_dps / tank | Present | lava physical bruiser |
| species_0130 | Quỷ Diện Thạch | earth | tank | Present | stone guard with petrification resistance |
| species_0131 | Hư Ảnh | dark | magic_dps | Present | void caster with speed emphasis reserved for skills |
| species_0132 | Ma Đạo Thư | light | magic_dps / support | Present | spellbook caster with healing |
| species_0133 | Ma Kiếm | dark | physical_dps | Present | magic sword physical attack with self vitality |
| species_0134 | Thạch Khôi Lỗi | earth | physical_dps / disruptor | Present | stone construct with weakening |
| species_0135 | Tiểu Sửu Hạp | dark | magic_dps / tank | Present | sturdy magic jack-in-box |
| species_0136 | Thảo Nhân Binh | earth | disruptor / physical_dps | Missing | authored scarecrow binding and physical fallback |
| species_0137 | Thủy Tinh Ma Kính | light | magic_dps / disruptor | Present | reflective caster with misfortune impairment |
| species_0138 | Dung Nham Cự Nhân | fire | physical_dps / disruptor | Present | lava bruiser with group magic-offense debuff |
| species_0139 | Huyền Vũ | water | tank / support | Missing | authored sacred turtle protector |
| species_0140 | Nhân Sư | earth | hybrid | Missing | authored sphinx dual attacker |
| species_0141 | Thượng Cổ Đồ Đằng | earth | support / magic_dps | Missing | authored totem ally buffs with magic fallback |
| species_0142 | Thần Tướng Cự Ma | earth | physical_dps / tank | Missing | authored giant warrior bruiser |
| species_0143 | Đăng Thần | wind | magic_dps / support | Missing | authored djinn with ally protection |
| species_0144 | Linh Tiên Hoa Hương | light | support / magic_dps | Missing | authored flower spirit healer |
| species_0145 | Cự Linh Mộc | earth | tank / support | Missing | authored great tree protector |
| species_0146 | Huyết Ma Vương | dark | magic_dps | Missing | authored vampiric caster; self recovery not Support |
| species_0147 | Viễn Cổ Tuyết Nhân | water | tank / physical_dps | Missing | authored ancient snow guard |
| species_0148 | Vân Mao Đà | earth | physical_dps / support | Missing | authored grass-mud mount with ally protection |
| species_0149 | Kim Kỳ Lân | light | physical_dps | Missing | authored golden unicorn attacker |
| species_0150 | Thiên Đường Điểu | water | tank / support | Missing | authored island guardian with ally protection |
| species_0151 | Độc Hạt Vương | earth | physical_dps / disruptor | Missing | authored scorpion king with binding beyond poison |
| species_0152 | Ái Thần Điểu | light | support / magic_dps | Missing | authored love bird healer with magic fallback |

## Numeric and gameplay ledger

Order: HP / ATK / MAG / DEF / SPD / SR. Base integers; growth per level before grade. These briefs are intended functions for P13, not granted skills.

| ID | Race | Base | Growth | Authored gameplay description |
|---|---|---|---|---|
| species_0001 | Vong Linh | 246 / 46 / 10 / 20 / 40 / 21 | 4.918 / 0.918 / 0.197 / 0.393 / 1.02 / 0.535 | Thiên về sát thương vật lý. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: ATK. |
| species_0002 | Vong Linh | 359 / 17 / 14 / 33 / 38 / 23 | 7.18 / 0.347 / 0.272 / 0.663 / 0.956 / 0.589 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: DEF. |
| species_0003 | Vong Linh | 286 / 37 / 10 / 24 / 39 / 21 | 5.714 / 0.745 / 0.199 / 0.485 / 0.995 / 0.548 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: DEF. |
| species_0004 | Vong Linh | 246 / 10 / 46 / 20 / 40 / 21 | 4.918 / 0.197 / 0.918 / 0.393 / 1.02 / 0.535 | Thiên về sát thương phép. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: MAG. |
| species_0005 | Vong Linh | 408 / 15 / 10 / 35 / 36 / 23 | 8.16 / 0.296 / 0.197 / 0.691 / 0.918 / 0.589 | Thiên về chống chịu. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: HP. |
| species_0006 | Vong Linh | 255 / 10 / 45 / 20 / 40 / 21 | 5.1 / 0.199 / 0.894 / 0.397 / 1.02 / 0.535 | Thiên về sát thương phép. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: HP. |
| species_0007 | Vong Linh | 246 / 46 / 10 / 20 / 40 / 21 | 4.918 / 0.918 / 0.197 / 0.393 / 1.02 / 0.535 | Thiên về sát thương vật lý. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: ATK. |
| species_0008 | Vong Linh | 271 / 15 / 45 / 23 / 41 / 22 | 5.427 / 0.298 / 0.898 / 0.461 / 1.053 / 0.565 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: MAG. |
| species_0009 | Vong Linh | 271 / 50 / 11 / 22 / 41 / 21 | 5.41 / 1.01 / 0.216 / 0.433 / 1.04 / 0.551 | Thiên về sát thương vật lý. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: ATK. |
| species_0010 | Vong Linh | 314 / 41 / 11 / 27 / 40 / 22 | 6.286 / 0.82 / 0.219 / 0.533 / 1.014 / 0.565 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: DEF. |
| species_0011 | Vong Linh | 271 / 50 / 11 / 22 / 41 / 21 | 5.41 / 1.01 / 0.216 / 0.433 / 1.04 / 0.551 | Thiên về sát thương vật lý. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: ATK. |
| species_0012 | Vong Linh | 438 / 21 / 17 / 40 / 40 / 23 | 8.76 / 0.423 / 0.332 / 0.809 / 1.008 / 0.61 | Thiên về chống chịu với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: DEF. |
| species_0013 | Vong Linh | 301 / 50 / 17 / 26 / 42 / 22 | 6.019 / 0.996 / 0.331 / 0.512 / 1.074 / 0.581 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: ATK. |
| species_0014 | Vong Linh | 301 / 17 / 50 / 26 / 42 / 22 | 6.019 / 0.331 / 0.996 / 0.512 / 1.074 / 0.581 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: MAG. |
| species_0015 | Vong Linh | 335 / 55 / 18 / 29 / 43 / 23 | 6.709 / 1.11 / 0.369 / 0.57 / 1.095 / 0.598 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: ATK. |
| species_0016 | Vong Linh | 335 / 18 / 55 / 29 / 43 / 22 | 6.709 / 0.369 / 1.11 / 0.57 / 1.108 / 0.583 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: MAG. |
| species_0017 | Vong Linh | 457 / 60 / 16 / 39 / 42 / 24 | 9.143 / 1.193 / 0.318 / 0.775 / 1.074 / 0.614 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: DEF. |
| species_0018 | Vong Linh | 395 / 22 / 65 / 34 / 44 / 24 | 7.893 / 0.434 / 1.306 / 0.671 / 1.115 / 0.614 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: MAG. |
| species_0019 | Vong Linh | 424 / 23 / 70 / 36 / 45 / 23 | 8.485 / 0.467 / 1.404 / 0.721 / 1.14 / 0.607 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: MAG. |
| species_0020 | Vong Linh | 618 / 38 / 17 / 55 / 40 / 25 | 12.357 / 0.767 / 0.341 / 1.097 / 1.028 / 0.653 | Thiên về chống chịu với chức năng phụ sát thương vật lý. Thiên về kháng status đầu vào; không đồng nghĩa miễn nhiễm. Điểm nhấn riêng: DEF. |
| species_0021 | Thực Vật | 415 / 14 / 9 / 35 / 36 / 22 | 8.31 / 0.276 / 0.184 / 0.709 / 0.918 / 0.561 | Thiên về chống chịu. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0022 | Thực Vật | 260 / 20 / 32 / 22 / 42 / 22 | 5.2 / 0.399 / 0.636 / 0.445 / 1.058 / 0.548 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0023 | Thực Vật | 265 / 24 / 26 / 24 / 44 / 20 | 5.3 / 0.475 / 0.52 / 0.475 / 1.122 / 0.51 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: HP. |
| species_0024 | Thực Vật | 256 / 9 / 47 / 18 / 40 / 20 | 5.13 / 0.184 / 0.935 / 0.368 / 1.02 / 0.51 | Thiên về sát thương phép. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0025 | Thực Vật | 261 / 9 / 46 / 18 / 40 / 20 | 5.218 / 0.184 / 0.926 / 0.368 / 1.02 / 0.51 | Thiên về sát thương phép. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: HP. |
| species_0026 | Thực Vật | 305 / 36 / 10 / 24 / 39 / 21 | 6.095 / 0.715 / 0.191 / 0.485 / 0.995 / 0.523 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0027 | Thực Vật | 265 / 24 / 26 / 24 / 44 / 20 | 5.3 / 0.475 / 0.52 / 0.475 / 1.122 / 0.51 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: HP. |
| species_0028 | Thực Vật | 286 / 22 / 35 / 24 / 42 / 22 | 5.72 / 0.438 / 0.7 / 0.49 / 1.079 / 0.565 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0029 | Thực Vật | 420 / 18 / 14 / 36 / 38 / 23 | 8.398 / 0.354 / 0.278 / 0.728 / 0.975 / 0.578 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0030 | Thực Vật | 292 / 45 / 14 / 22 / 42 / 21 | 5.83 / 0.898 / 0.283 / 0.437 / 1.066 / 0.525 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: ATK. |
| species_0031 | Thực Vật | 292 / 50 / 10 / 20 / 41 / 21 | 5.83 / 1.01 / 0.202 / 0.405 / 1.04 / 0.525 | Thiên về sát thương vật lý. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: ATK. |
| species_0032 | Thực Vật | 372 / 44 / 12 / 30 / 41 / 22 | 7.436 / 0.873 / 0.233 / 0.591 / 1.034 / 0.554 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0033 | Thực Vật | 315 / 16 / 51 / 24 / 43 / 21 | 6.301 / 0.309 / 1.024 / 0.477 / 1.087 / 0.541 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0034 | Thực Vật | 466 / 20 / 16 / 40 / 40 / 23 | 9.315 / 0.393 / 0.309 / 0.807 / 1.008 / 0.581 | Thiên về chống chịu với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0035 | Thực Vật | 519 / 22 / 17 / 45 / 40 / 24 | 10.384 / 0.438 / 0.344 / 0.9 / 1.014 / 0.611 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0036 | Thực Vật | 414 / 49 / 13 / 33 / 41 / 22 | 8.289 / 0.973 / 0.259 / 0.659 / 1.054 / 0.57 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0037 | Thực Vật | 416 / 32 / 51 / 36 / 46 / 22 | 8.32 / 0.638 / 1.018 / 0.713 / 1.184 / 0.571 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ với chức năng phụ sát thương phép. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0038 | Thực Vật | 478 / 34 / 36 / 42 / 44 / 25 | 9.568 / 0.685 / 0.721 / 0.837 / 1.115 / 0.628 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ chống chịu. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0039 | Rồng | 235 / 46 / 9 / 21 / 40 / 20 | 4.7 / 0.918 / 0.188 / 0.424 / 1.02 / 0.51 | Thiên về sát thương vật lý. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK. |
| species_0040 | Rồng | 235 / 46 / 9 / 21 / 40 / 20 | 4.7 / 0.918 / 0.188 / 0.424 / 1.02 / 0.51 | Thiên về sát thương vật lý. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK. |
| species_0041 | Rồng | 280 / 11 / 35 / 26 / 39 / 21 | 5.607 / 0.219 / 0.707 / 0.513 / 0.995 / 0.523 | Thiên về sát thương phép với chức năng phụ chống chịu. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: DEF. |
| species_0042 | Rồng | 234 / 29 / 29 / 19 / 41 / 21 | 4.675 / 0.581 / 0.581 / 0.371 / 1.033 / 0.523 | Thiên về sát thương vật lý và phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK và MAG. |
| species_0043 | Rồng | 406 / 18 / 14 / 38 / 39 / 22 | 8.124 / 0.354 / 0.278 / 0.755 / 0.988 / 0.565 | Thiên về chống chịu với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: HP. |
| species_0044 | Rồng | 260 / 45 / 14 / 25 / 42 / 21 | 5.205 / 0.898 / 0.286 / 0.496 / 1.066 / 0.525 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK. |
| species_0045 | Rồng | 384 / 15 / 20 / 37 / 38 / 22 | 7.685 / 0.292 / 0.398 / 0.743 / 0.962 / 0.565 | Thiên về chống chịu với chức năng phụ sát thương phép. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: DEF. |
| species_0046 | Rồng | 270 / 11 / 49 / 24 / 41 / 21 | 5.39 / 0.216 / 0.97 / 0.475 / 1.04 / 0.525 | Thiên về sát thương phép. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: DEF. |
| species_0047 | Rồng | 289 / 50 / 16 / 27 / 42 / 22 | 5.773 / 0.996 / 0.318 / 0.55 / 1.074 / 0.554 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK. |
| species_0048 | Rồng | 287 / 11 / 56 / 26 / 42 / 21 | 5.734 / 0.229 / 1.12 / 0.517 / 1.061 / 0.541 | Thiên về sát thương phép. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: MAG. |
| species_0049 | Rồng | 340 / 27 / 25 / 36 / 44 / 22 | 6.802 / 0.532 / 0.503 / 0.725 / 1.114 / 0.554 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ với chức năng phụ chống chịu. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: DEF. |
| species_0050 | Rồng | 322 / 18 / 55 / 31 / 43 / 22 | 6.436 / 0.354 / 1.11 / 0.613 / 1.108 / 0.556 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: MAG. |
| species_0051 | Rồng | 320 / 41 / 41 / 22 / 42 / 22 | 6.392 / 0.824 / 0.824 / 0.432 / 1.081 / 0.556 | Thiên về sát thương vật lý và phép. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK và MAG. |
| species_0052 | Rồng | 374 / 46 / 46 / 30 / 44 / 23 | 7.48 / 0.929 / 0.929 / 0.594 / 1.115 / 0.585 | Thiên về sát thương vật lý và phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về DEF, đánh đổi một phần phân bổ chỉ số khác. Điểm nhấn riêng: ATK và MAG. |
| species_0053 | Ác Ma | 234 / 9 / 49 / 19 / 40 / 20 | 4.673 / 0.187 / 0.972 / 0.374 / 1.02 / 0.51 | Thiên về sát thương phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0054 | Ác Ma | 237 / 43 / 13 / 20 / 41 / 21 | 4.733 / 0.864 / 0.26 / 0.402 / 1.033 / 0.523 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: ATK. |
| species_0055 | Ác Ma | 237 / 13 / 43 / 20 / 41 / 21 | 4.733 / 0.26 / 0.864 / 0.402 / 1.033 / 0.523 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0056 | Ác Ma | 267 / 40 / 9 / 24 / 39 / 21 | 5.346 / 0.795 / 0.186 / 0.485 / 0.995 / 0.523 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: DEF. |
| species_0057 | Ác Ma | 230 / 32 / 32 / 14 / 40 / 20 | 4.6 / 0.632 / 0.632 / 0.276 / 1.02 / 0.51 | Thiên về sát thương vật lý và phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: ATK và MAG. |
| species_0058 | Ác Ma | 234 / 49 / 9 / 19 / 40 / 20 | 4.673 / 0.972 / 0.187 / 0.374 / 1.02 / 0.51 | Thiên về sát thương vật lý. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: ATK. |
| species_0059 | Ác Ma | 294 / 44 / 10 / 27 / 40 / 21 | 5.88 / 0.875 / 0.205 / 0.533 / 1.014 / 0.538 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: DEF. |
| species_0060 | Ác Ma | 407 / 26 / 10 / 33 / 38 / 22 | 8.135 / 0.525 / 0.209 / 0.653 / 0.962 / 0.565 | Thiên về chống chịu với chức năng phụ sát thương vật lý. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: HP. |
| species_0061 | Ác Ma | 257 / 10 / 53 / 21 / 41 / 21 | 5.14 / 0.206 / 1.069 / 0.411 / 1.04 / 0.525 | Thiên về sát thương phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0062 | Ác Ma | 260 / 14 / 48 / 22 / 42 / 21 | 5.207 / 0.286 / 0.95 / 0.443 / 1.066 / 0.525 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0063 | Ác Ma | 326 / 48 / 11 / 30 / 41 / 22 | 6.522 / 0.97 / 0.227 / 0.591 / 1.034 / 0.554 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: DEF. |
| species_0064 | Ác Ma | 311 / 29 / 32 / 29 / 46 / 21 | 6.222 / 0.586 / 0.647 / 0.586 / 1.167 / 0.541 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: HP. |
| species_0065 | Ác Ma | 285 / 11 / 59 / 23 / 42 / 21 | 5.701 / 0.228 / 1.186 / 0.456 / 1.061 / 0.541 | Thiên về sát thương phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0066 | Ác Ma | 322 / 18 / 59 / 27 / 43 / 22 | 6.437 / 0.354 / 1.175 / 0.547 / 1.108 / 0.556 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0067 | Ác Ma | 364 / 54 / 13 / 33 / 41 / 22 | 7.27 / 1.081 / 0.253 / 0.659 / 1.054 / 0.57 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: DEF. |
| species_0068 | Ác Ma | 340 / 47 / 47 / 20 / 43 / 22 | 6.808 / 0.935 / 0.935 / 0.408 / 1.091 / 0.564 | Thiên về sát thương vật lý và phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: ATK và MAG. |
| species_0069 | Ác Ma | 386 / 33 / 52 / 37 / 45 / 24 | 7.726 / 0.657 / 1.037 / 0.734 / 1.143 / 0.614 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: MAG. |
| species_0070 | Thú | 265 / 46 / 9 / 18 / 40 / 20 | 5.3 / 0.918 / 0.184 / 0.368 / 1.02 / 0.51 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0071 | Thú | 265 / 46 / 9 / 18 / 40 / 20 | 5.3 / 0.918 / 0.184 / 0.368 / 1.02 / 0.51 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0072 | Thú | 382 / 16 / 13 / 33 / 38 / 22 | 7.635 / 0.322 / 0.253 / 0.662 / 0.969 / 0.548 | Thiên về chống chịu với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: DEF. |
| species_0073 | Thú | 382 / 16 / 13 / 33 / 38 / 22 | 7.635 / 0.322 / 0.253 / 0.662 / 0.956 / 0.561 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: DEF. |
| species_0074 | Thú | 265 / 46 / 9 / 18 / 40 / 20 | 5.3 / 0.918 / 0.184 / 0.368 / 1.02 / 0.51 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0075 | Thú | 415 / 14 / 9 / 35 / 36 / 22 | 8.31 / 0.276 / 0.184 / 0.709 / 0.918 / 0.561 | Thiên về chống chịu. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: DEF. |
| species_0076 | Thú | 265 / 46 / 9 / 18 / 40 / 20 | 5.3 / 0.918 / 0.184 / 0.368 / 1.02 / 0.51 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0077 | Thú | 292 / 45 / 14 / 22 / 41 / 21 | 5.83 / 0.898 / 0.283 / 0.437 / 1.053 / 0.538 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0078 | Thú | 297 / 27 / 27 / 27 / 43 / 23 | 5.94 / 0.535 / 0.535 / 0.535 / 1.092 / 0.578 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: HP. |
| species_0079 | Thú | 292 / 22 / 34 / 25 / 44 / 21 | 5.83 / 0.446 / 0.673 / 0.498 / 1.118 / 0.525 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ với chức năng phụ sát thương phép. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: MAG. |
| species_0080 | Thú | 335 / 39 / 10 / 27 / 40 / 21 | 6.705 / 0.787 / 0.21 / 0.533 / 1.014 / 0.538 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: DEF. |
| species_0081 | Thú | 466 / 20 / 16 / 40 / 39 / 23 | 9.315 / 0.393 / 0.309 / 0.807 / 0.995 / 0.595 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: DEF. |
| species_0082 | Thú | 379 / 44 / 12 / 28 / 41 / 22 | 7.576 / 0.885 / 0.236 / 0.561 / 1.034 / 0.554 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: HP. |
| species_0083 | Thú | 323 / 16 / 50 / 24 / 42 / 22 | 6.466 / 0.313 / 0.996 / 0.484 / 1.074 / 0.554 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: MAG. |
| species_0084 | Thú | 532 / 23 / 18 / 42 / 40 / 23 | 10.649 / 0.454 / 0.357 / 0.844 / 1.027 / 0.598 | Thiên về chống chịu với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: HP. |
| species_0085 | Thú | 360 / 55 / 17 / 27 / 43 / 22 | 7.208 / 1.11 / 0.349 / 0.54 / 1.108 / 0.556 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0086 | Thú | 360 / 13 / 62 / 25 / 42 / 22 | 7.208 / 0.25 / 1.248 / 0.5 / 1.081 / 0.556 | Thiên về sát thương phép. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: MAG. |
| species_0087 | Thú | 392 / 68 / 14 / 27 / 43 / 22 | 7.844 / 1.359 / 0.272 / 0.545 / 1.091 / 0.564 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0088 | Thú | 424 / 73 / 15 / 29 / 43 / 22 | 8.48 / 1.469 / 0.294 / 0.589 / 1.102 / 0.571 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0089 | Chim | 247 / 41 / 14 / 21 / 42 / 21 | 4.933 / 0.816 / 0.271 / 0.419 / 1.084 / 0.523 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0090 | Chim | 255 / 25 / 25 / 25 / 46 / 20 | 5.1 / 0.497 / 0.497 / 0.497 / 1.178 / 0.51 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: HP. |
| species_0091 | Chim | 246 / 46 / 10 / 20 / 42 / 20 | 4.918 / 0.918 / 0.197 / 0.393 / 1.071 / 0.51 | Thiên về sát thương vật lý. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0092 | Chim | 284 / 38 / 10 / 23 / 40 / 21 | 5.681 / 0.765 / 0.198 / 0.469 / 1.044 / 0.523 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0093 | Chim | 247 / 41 / 14 / 21 / 42 / 21 | 4.933 / 0.816 / 0.271 / 0.419 / 1.084 / 0.523 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0094 | Chim | 246 / 10 / 46 / 20 / 42 / 20 | 4.918 / 0.197 / 0.918 / 0.393 / 1.071 / 0.51 | Thiên về sát thương phép. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |
| species_0095 | Chim | 246 / 46 / 10 / 20 / 42 / 20 | 4.918 / 0.918 / 0.197 / 0.393 / 1.071 / 0.51 | Thiên về sát thương vật lý. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0096 | Chim | 271 / 11 / 50 / 22 / 42 / 21 | 5.41 / 0.216 / 1.01 / 0.433 / 1.092 / 0.525 | Thiên về sát thương phép. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |
| species_0097 | Chim | 281 / 15 / 44 / 23 / 43 / 21 | 5.61 / 0.3 / 0.874 / 0.464 / 1.119 / 0.525 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: HP. |
| species_0098 | Chim | 271 / 45 / 15 / 23 / 43 / 21 | 5.427 / 0.898 / 0.298 / 0.461 / 1.106 / 0.538 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0099 | Chim | 271 / 50 / 11 / 22 / 42 / 21 | 5.41 / 1.01 / 0.216 / 0.433 / 1.092 / 0.525 | Thiên về sát thương vật lý. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0100 | Chim | 300 / 56 / 12 / 24 / 43 / 21 | 6 / 1.12 / 0.24 / 0.48 / 1.113 / 0.541 | Thiên về sát thương vật lý. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0101 | Chim | 301 / 50 / 17 / 26 / 44 / 21 | 6.019 / 0.996 / 0.331 / 0.512 / 1.141 / 0.541 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0102 | Chim | 300 / 12 / 56 / 24 / 43 / 21 | 6 / 0.24 / 1.12 / 0.48 / 1.113 / 0.541 | Thiên về sát thương phép. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |
| species_0103 | Chim | 337 / 29 / 42 / 32 / 47 / 22 | 6.742 / 0.573 / 0.832 / 0.64 / 1.22 / 0.556 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ với chức năng phụ sát thương phép. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |
| species_0104 | Chim | 335 / 55 / 18 / 29 / 45 / 22 | 6.709 / 1.11 / 0.369 / 0.57 / 1.149 / 0.57 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0105 | Chim | 365 / 20 / 60 / 31 / 45 / 23 | 7.301 / 0.402 / 1.208 / 0.621 / 1.16 / 0.578 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |
| species_0106 | Chim | 395 / 22 / 65 / 34 / 46 / 22 | 7.893 / 0.434 / 1.306 / 0.671 / 1.185 / 0.571 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |
| species_0107 | Chim | 393 / 73 / 16 / 31 / 45 / 22 | 7.869 / 1.469 / 0.315 / 0.63 / 1.156 / 0.571 | Thiên về sát thương vật lý. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: ATK. |
| species_0108 | Côn Trùng | 240 / 47 / 10 / 19 / 40 / 20 | 4.795 / 0.945 / 0.192 / 0.384 / 1.02 / 0.51 | Thiên về sát thương vật lý. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK. |
| species_0109 | Côn Trùng | 240 / 10 / 47 / 19 / 40 / 20 | 4.795 / 0.192 / 0.945 / 0.384 / 1.02 / 0.51 | Thiên về sát thương phép. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: MAG. |
| species_0110 | Côn Trùng | 354 / 22 / 10 / 33 / 37 / 22 | 7.085 / 0.44 / 0.195 / 0.656 / 0.944 / 0.548 | Thiên về chống chịu với chức năng phụ sát thương vật lý. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: DEF. |
| species_0111 | Côn Trùng | 389 / 15 / 10 / 37 / 36 / 22 | 7.785 / 0.292 / 0.195 / 0.735 / 0.918 / 0.561 | Thiên về chống chịu. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: DEF. |
| species_0112 | Côn Trùng | 240 / 47 / 10 / 19 / 40 / 20 | 4.795 / 0.945 / 0.192 / 0.384 / 1.02 / 0.51 | Thiên về sát thương vật lý. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK. |
| species_0113 | Côn Trùng | 241 / 31 / 30 / 14 / 40 / 20 | 4.813 / 0.624 / 0.606 / 0.289 / 1.02 / 0.51 | Thiên về sát thương vật lý và phép. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK và MAG. |
| species_0114 | Côn Trùng | 276 / 39 / 10 / 24 / 39 / 21 | 5.513 / 0.773 / 0.192 / 0.485 / 0.995 / 0.523 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: DEF. |
| species_0115 | Côn Trùng | 266 / 46 / 15 / 23 / 42 / 21 | 5.317 / 0.924 / 0.292 / 0.452 / 1.066 / 0.525 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK. |
| species_0116 | Côn Trùng | 264 / 11 / 52 / 21 / 41 / 21 | 5.275 / 0.211 / 1.04 / 0.422 / 1.04 / 0.525 | Thiên về sát thương phép. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: MAG. |
| species_0117 | Côn Trùng | 323 / 12 / 41 / 25 / 40 / 21 | 6.452 / 0.236 / 0.821 / 0.498 / 1.014 / 0.538 | Thiên về sát thương phép với chức năng phụ chống chịu. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: HP. |
| species_0118 | Côn Trùng | 269 / 23 / 35 / 26 / 42 / 22 | 5.382 / 0.457 / 0.693 / 0.511 / 1.079 / 0.565 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: MAG. |
| species_0119 | Côn Trùng | 433 / 22 / 18 / 38 / 38 / 23 | 8.655 / 0.448 / 0.358 / 0.769 / 0.981 / 0.581 | Thiên về chống chịu với chức năng phụ sát thương vật lý và phép. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: DEF. |
| species_0120 | Côn Trùng | 295 / 51 / 16 / 25 / 42 / 22 | 5.897 / 1.025 / 0.324 / 0.501 / 1.074 / 0.554 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK. |
| species_0121 | Côn Trùng | 295 / 16 / 51 / 25 / 43 / 21 | 5.897 / 0.324 / 1.025 / 0.501 / 1.087 / 0.541 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: MAG. |
| species_0122 | Côn Trùng | 329 / 18 / 57 / 28 / 43 / 22 | 6.573 / 0.362 / 1.142 / 0.559 / 1.108 / 0.556 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: MAG. |
| species_0123 | Côn Trùng | 329 / 57 / 18 / 28 / 43 / 22 | 6.573 / 1.142 / 0.362 / 0.559 / 1.108 / 0.556 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK. |
| species_0124 | Côn Trùng | 623 / 23 / 16 / 59 / 39 / 25 | 12.455 / 0.467 / 0.311 / 1.176 / 0.991 / 0.628 | Thiên về chống chịu. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: DEF. |
| species_0125 | Côn Trùng | 408 / 15 / 74 / 30 / 43 / 22 | 8.16 / 0.3 / 1.483 / 0.601 / 1.102 / 0.571 | Thiên về sát thương phép. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: HP. |
| species_0126 | Côn Trùng | 439 / 42 / 44 / 42 / 46 / 24 | 8.772 / 0.839 / 0.886 / 0.839 / 1.181 / 0.622 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: HP. |
| species_0127 | Linh | 247 / 41 / 14 / 21 / 41 / 21 | 4.933 / 0.816 / 0.271 / 0.419 / 1.033 / 0.523 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: ATK. |
| species_0128 | Linh | 234 / 9 / 49 / 19 / 40 / 20 | 4.673 / 0.187 / 0.972 / 0.374 / 1.02 / 0.51 | Thiên về sát thương phép. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: MAG. |
| species_0129 | Linh | 284 / 38 / 10 / 23 / 39 / 21 | 5.681 / 0.765 / 0.198 / 0.469 / 0.995 / 0.523 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: ATK. |
| species_0130 | Linh | 396 / 15 / 10 / 36 / 36 / 22 | 7.914 / 0.297 / 0.198 / 0.714 / 0.918 / 0.561 | Thiên về chống chịu. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: DEF. |
| species_0131 | Linh | 234 / 9 / 49 / 19 / 40 / 20 | 4.673 / 0.187 / 0.972 / 0.374 / 1.02 / 0.51 | Thiên về sát thương phép. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: MAG. |
| species_0132 | Linh | 260 / 14 / 48 / 22 / 41 / 21 | 5.207 / 0.286 / 0.95 / 0.443 / 1.053 / 0.538 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: MAG. |
| species_0133 | Linh | 281 / 49 / 11 / 22 / 41 / 21 | 5.61 / 0.983 / 0.219 / 0.437 / 1.04 / 0.525 | Thiên về sát thương vật lý. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: HP. |
| species_0134 | Linh | 301 / 50 / 17 / 26 / 43 / 21 | 6.019 / 0.996 / 0.331 / 0.512 / 1.087 / 0.541 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: ATK. |
| species_0135 | Linh | 328 / 13 / 47 / 30 / 41 / 22 | 6.55 / 0.256 / 0.938 / 0.591 / 1.034 / 0.554 | Thiên về sát thương phép với chức năng phụ chống chịu. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: DEF. |
| species_0136 | Linh | 311 / 35 / 27 / 28 / 45 / 21 | 6.222 / 0.708 / 0.55 / 0.56 / 1.14 / 0.541 | Thiên về khống chế hoặc làm giảm hiệu quả đối thủ với chức năng phụ sát thương vật lý. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: HP. |
| species_0137 | Linh | 322 / 18 / 59 / 27 / 43 / 22 | 6.437 / 0.354 / 1.175 / 0.547 / 1.108 / 0.556 | Thiên về sát thương phép với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: MAG. |
| species_0138 | Linh | 335 / 55 / 18 / 29 / 43 / 22 | 6.709 / 1.11 / 0.369 / 0.57 / 1.108 / 0.556 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: ATK. |
| species_0139 | Linh | 531 / 26 / 20 / 49 / 40 / 24 | 10.627 / 0.513 / 0.403 / 0.981 / 1.023 / 0.62 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: DEF. |
| species_0140 | Linh | 376 / 48 / 51 / 23 / 43 / 22 | 7.52 / 0.97 / 1.027 / 0.451 / 1.102 / 0.571 | Thiên về sát thương vật lý và phép. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: ATK và MAG. |
| species_0141 | Linh | 386 / 33 / 52 / 37 / 45 / 24 | 7.726 / 0.657 / 1.037 / 0.734 / 1.143 / 0.614 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: MAG. |
| species_0142 | Linh | 491 / 64 / 17 / 42 / 43 / 23 | 9.828 / 1.282 / 0.342 / 0.833 / 1.084 / 0.593 | Thiên về sát thương vật lý với chức năng phụ chống chịu. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: DEF. |
| species_0143 | Linh | 407 / 22 / 74 / 35 / 44 / 23 | 8.141 / 0.448 / 1.486 / 0.692 / 1.126 / 0.593 | Thiên về sát thương phép với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về phép ở role phù hợp; role vật lý hoặc Tank vẫn giữ chức năng chính. Điểm nhấn riêng: MAG. |
| species_0144 | Thực Vật | 447 / 34 / 55 / 38 / 45 / 24 | 8.944 / 0.686 / 1.094 / 0.766 / 1.153 / 0.622 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: MAG. |
| species_0145 | Thực Vật | 657 / 28 / 22 / 57 / 41 / 25 | 13.132 / 0.554 / 0.435 / 1.138 / 1.042 / 0.637 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Định hướng duy trì giao tranh bằng hồi phục hoặc bảo vệ phù hợp role. Điểm nhấn riêng: DEF. |
| species_0146 | Ác Ma | 436 / 16 / 81 / 32 / 44 / 23 | 8.729 / 0.316 / 1.618 / 0.633 / 1.112 / 0.579 | Thiên về sát thương phép. Ưu tiên áp lực tấn công, đổi bằng một phần sức chịu đòn hoặc chỉ số phụ. Điểm nhấn riêng: HP. |
| species_0147 | Thú | 612 / 33 / 15 / 51 / 40 / 24 | 12.246 / 0.662 / 0.294 / 1.019 / 1.019 / 0.614 | Thiên về chống chịu với chức năng phụ sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: DEF. |
| species_0148 | Thú | 456 / 70 / 22 / 34 / 44 / 23 | 9.116 / 1.404 / 0.442 / 0.683 / 1.126 / 0.593 | Thiên về sát thương vật lý với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0149 | Thú | 456 / 79 / 16 / 32 / 44 / 23 | 9.116 / 1.579 / 0.316 / 0.633 / 1.112 / 0.579 | Thiên về sát thương vật lý. Thiên về lượng HP để duy trì hiện diện trong giao tranh. Điểm nhấn riêng: ATK. |
| species_0150 | Chim | 617 / 30 / 23 / 57 / 42 / 25 | 12.35 / 0.596 / 0.468 / 1.14 / 1.094 / 0.637 | Thiên về chống chịu với chức năng phụ hồi phục, bảo vệ hoặc hỗ trợ đồng đội. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: DEF. |
| species_0151 | Côn Trùng | 416 / 72 / 23 / 35 / 45 / 23 | 8.313 / 1.445 / 0.457 / 0.707 / 1.14 / 0.579 | Thiên về sát thương vật lý với chức năng phụ khống chế hoặc làm giảm hiệu quả đối thủ. Định hướng tiêu hao, gây áp lực kéo dài hoặc cản trở phù hợp role. Điểm nhấn riêng: ATK. |
| species_0152 | Chim | 426 / 36 / 53 / 40 / 47 / 24 | 8.526 / 0.725 / 1.053 / 0.81 / 1.211 / 0.622 | Thiên về hồi phục, bảo vệ hoặc hỗ trợ đồng đội với chức năng phụ sát thương phép. Ưu tiên tốc độ khi cùng Star, class, role, level và grade. Điểm nhấn riêng: MAG. |

## Downstream acceptance

P13 owns the interaction chart, skill formulas/eligibility and actual native pools. P02/P07 own battle-mode viability testing; P15 owns pacing. Content activation and legacy14→152 mapping require a later additive implementation delivery with migration/rollback review. Passing this static catalog validator establishes only the approved numeric constraints and frozen-identity coverage.
