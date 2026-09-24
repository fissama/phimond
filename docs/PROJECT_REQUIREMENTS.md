# PROJECT UPDATE: 《靈獸世界 Online》 Gameplay Reconstruction

Bạn đang tiếp tục phát triển một project game hiện có. Hãy đọc toàn bộ codebase hiện tại trước khi thay đổi, giữ lại những phần có thể tái sử dụng và refactor theo yêu cầu dưới đây.

Mục tiêu của project là tái dựng gameplay của game MMORPG mobile cũ **《靈獸世界 Online》 / 《灵兽世界OL》 / Spirit Beast World** với mức fidelity gameplay cao nhất có thể.

Mục tiêu là tái tạo hệ thống gameplay, progression, combat, pet system, breeding/synthesis, maps, quests, economy và social systems của game gốc càng sát càng tốt.

Không được đơn giản hóa game thành một Pokémon clone thông thường. Ba pillar quan trọng nhất phải được giữ là:

1. Individual pet variance.
2. Multi-generation pet lineage/breeding.
3. Skill/stat/resistance inheritance.

Nếu project được public hoặc commercialize, không được phụ thuộc vào asset, artwork, music, dialogue, logo hoặc nội dung có bản quyền của game gốc nếu chưa có quyền sử dụng. Architecture phải cho phép giữ gameplay tương đương nhưng thay thế toàn bộ presentation/content protected khi cần.

---

# 1. TECH STACK

Sử dụng monorepo.

Backend chính:

* Go.
* Modular monolith.
* Không dùng microservices ở giai đoạn hiện tại.
* Backend là authoritative server.
* `net/http` + router nhẹ như `chi`.
* WebSocket dùng `coder/websocket` hoặc thư viện tương đương maintained tốt.
* MySQL cho persistence.
* Không dùng PostgreSQL.

Frontend game:

* Godot 4.x.
* GDScript.
* Godot chỉ là game client, không phải authoritative game server.

Frontend web:

* Next.js.
* TypeScript.
* React.
* Có thể dùng Tailwind/shadcn nếu project hiện tại đã phù hợp.

Protocol:

* HTTP/REST cho account, encyclopedia, auction browsing, admin, metadata.
* WebSocket cho game realtime.
* JSON cho protocol MVP.
* Thiết kế protocol sao cho có thể chuyển sang binary protocol/Protobuf/MessagePack sau này nếu thật sự cần.

Deployment hiện tại:

* Local/dev-first.
* Docker/Docker Compose nếu repo hiện tại phù hợp.
* Không introduce Kubernetes.
* Redis không bắt buộc.
* Chỉ thêm Redis sau này nếu thật sự cần presence, caching, distributed locking, matchmaking queue hoặc Pub/Sub.

---

# 2. DATABASE REQUIREMENT

Máy local đã có MySQL đang chạy.

TUYỆT ĐỐI KHÔNG sử dụng database/schema hiện tại của project hoặc các schema có sẵn cho dữ liệu game mới.

Hãy tạo một database MySQL mới dành riêng cho game.

Tên database phải configurable bằng environment variable, ví dụ:

```env
GAME_DB_NAME=spirit_world
```

Có thể mặc định development là:

```text
spirit_world
```

Nhưng không hard-code tên database vào business logic.

Không drop, truncate hoặc migrate schema/database hiện tại ngoài database game mới.

Tất cả migration mới chỉ được target database game mới.

Thiết kế migration có versioning.

Backend phải có config:

```text
MYSQL_HOST
MYSQL_PORT
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DATABASE
```

Nếu project đã có infrastructure/config convention, tích hợp theo convention hiện tại.

---

# 3. MONOREPO TARGET STRUCTURE

Ưu tiên structure tương đương:

```text
/
├ apps/
│  ├ game-server/
│  ├ game-client/
│  └ web/
│
├ packages/
│  ├ game-data/
│  ├ protocol/
│  └ shared-tools/
│
├ data/
│  ├ pets/
│  ├ skills/
│  ├ items/
│  ├ recipes/
│  ├ quests/
│  ├ maps/
│  ├ npcs/
│  ├ spawns/
│  └ balance/
│
├ migrations/
├ infra/
├ docs/
└ tools/
```

Không bắt buộc rename project hiện tại nếu structure hiện có tương đương và refactor sẽ gây churn không cần thiết.

Backend Go nên được chia module/domain logic, ví dụ:

```text
internal/
├ auth/
├ account/
├ character/
├ world/
├ battle/
├ pet/
├ breeding/
├ capture/
├ skill/
├ status/
├ quest/
├ inventory/
├ economy/
├ auction/
├ mail/
├ arena/
├ party/
├ guild/
├ chat/
├ npc/
├ content/
├ persistence/
└ transport/
```

Đây vẫn là một modular monolith và build/deploy thành một server binary chính trong giai đoạn đầu.

---

# 4. SOURCE OF TRUTH PRINCIPLE

Backend Go là source of truth cho toàn bộ gameplay.

Client KHÔNG được quyết định:

* damage;
* crit;
* hit/miss;
* capture success;
* item drop;
* pet generation;
* breeding result;
* inheritance;
* EXP;
* loot;
* currency;
* status effects;
* quest completion;
* auction transaction.

Client chỉ gửi intent.

Ví dụ client gửi:

```json
{
  "op": "battle.cast_skill",
  "data": {
    "battle_id": "battle_x",
    "actor_id": "pet_x",
    "skill_id": "skill_x",
    "target_id": "enemy_x"
  }
}
```

Không cho client gửi result như:

```json
{
  "damage": 999,
  "enemy_hp": 0
}
```

Server resolve toàn bộ kết quả rồi gửi event về client.

---

# 5. GAME IDENTITY

Gameplay loop chính phải là:

```text
Explore
→ nhận quest
→ gặp wild spirit beast
→ battle
→ làm yếu monster
→ capture
→ appraisal/divination
→ đánh giá individual stats/resistance
→ train pet
→ học/nâng skill
→ chuẩn bị breeding stock
→ synthesis/breeding
→ pet con kế thừa traits
→ tiếp tục train thế hệ sau
→ mở map/arena/content khó hơn
→ repeat
```

Player character chủ yếu là trainer/avatar.

Pet mới là combat unit và progression unit chính.

Không biến player avatar thành combat class chính nếu không có bằng chứng từ game gốc.

---

# 6. WORLD STRUCTURE

Game world phải được thiết kế theo mô hình 2D room/scene-based horizontal world.

Không cần seamless open world.

Mỗi map scene có thể gồm:

```text
Map
├ static background
├ walkable/collision area
├ player entities
├ NPC
├ pet follower
├ monster spawn
├ portal
├ trigger
└ encounter area
```

Map definitions phải data-driven.

Map connection ví dụ:

```json
{
  "from": "forest_middle",
  "exit": "east",
  "to": "forest_depth",
  "spawn": "west_entry"
}
```

Các world/zone đã biết từ game gốc cần được đưa vào reconstruction backlog:

## Severa / Main City

Bao gồm các area từng được ghi nhận như:

* Training Ground.
* Arena Rest Room.
* Imperial Arena.
* Palace Entrance.
* City Market.
* City Square / Severa City.

NPC/system hub gồm:

* newbie trainer;
* spirit beast trainer;
* teleport;
* battle master;
* imperial officer;
* pet merchant;
* item shop;
* skill trainer;
* guild manager;
* pet healer;
* auction manager.

## Emerald/Wave Forest / 碧波森林

Các area:

* Forest.
* Forest Camp.
* Forest West.
* Forest Middle.
* Forest East.
* Forest Depths.

## Treasure Beach / 寻宝沙滩

Các area:

* Beach West.
* Main Beach.
* Treasure area.
* Fisherman's Beach.
* Beach East.

## Barren Desert / 荒芜沙漠

Các area được ghi nhận:

* North Desert.
* Barren Desert.
* Stone Ruins.
* West Desert.
* Huru Tribe.
* Desert Entrance.
* Punishment Wasteland.
* Screaming Canyon.
* Bone Wasteland.
* Sealed Land.

## Windrock Mountain / 风岩山

Các area:

* mountain foot;
* mountain waist;
* camp;
* path;
* summit;
* summit stone bridge;
* Sacred Spirit Peak.

## Nightmare Island / 梦魔岛 / 梦魇岛

Các area:

* east;
* central island;
* survivor camp;
* ruins;
* deep ruins;
* Death Ruins;
* Gate of the Dead.

Late-game/referenced content backlog:

* Saint Cemetery.
* Undersea Tunnel.
* 赤风号.
* Time-Space Reincarnation.
* Ancient Ruins.
* Ancient Castle.
* World Tree.

Các tên localization có thể thay đổi. Internal ID phải ổn định và tách khỏi display name.

---

# 7. PET RACE SYSTEM

Ít nhất các race đã được ghi nhận:

```text
INSECT
PLANT
BIRD / FLYING
BEAST
UNDEAD
SPIRIT
DEMON
DRAGON
```

Dragon có thể là content ra sau/late-game; không giả định nó hoạt động hoàn toàn giống 7 race ban đầu nếu chưa xác minh.

Race phải data-driven.

Ví dụ:

```go
type RaceID string
```

Không hard-code game rules rải rác theo string comparison.

---

# 8. ELEMENT / SKILL FAMILY SYSTEM

7 family/element cốt lõi đã được ghi nhận:

```text
Insect -> Earth
Spirit -> Water
Bird -> Wind
Demon -> Fire
Beast -> Neutral
Plant -> Light
Undead -> Dark
```

Skill definitions cần hỗ trợ:

* element;
* physical/magical;
* target type;
* MP cost;
* power;
* hit chance;
* crit modifier;
* status application;
* duration;
* buff/debuff;
* dispel;
* capture-related effects nếu tìm thấy;
* learned level;
* race restrictions nếu có;
* inheritance eligibility.

Game gốc từng quảng bá hơn 300 skill. Hệ thống phải scale được đến ít nhất vài trăm/thousands skill definition mà không cần code mới cho từng skill.

---

# 9. SIGNATURE STATUS SYSTEM

Các identity status đã biết:

```text
Insect -> Petrify
Spirit -> Doom
Bird -> Sleep
Demon -> Silence
Beast -> Bind
Plant -> Blind
Undead -> Confusion
```

Status system phải generic/data-driven.

Các behavior cần support:

## Petrify

* khóa hành động thích hợp;
* có thể tăng defense trong trạng thái.

## Doom

* khóa hoặc giới hạn hành động theo rules;
* countdown;
* death khi countdown kết thúc nếu ruleset xác nhận.

## Sleep

* không hành động;
* damage có thể wake target;
* cần configurable modifier cho hit đánh thức nếu game gốc dùng damage bonus.

## Silence

* khóa magic skill.

## Bind

* khóa physical attack/skill.

## Blind

* giảm hit chance.

## Confusion

* mất quyền chọn target/action bình thường;
* có thể attack ally/enemy tùy rules.

Không hard-code mỗi status trong battle loop. Thiết kế StatusEffect abstraction.

---

# 10. STATUS COUNTER / CLEANSE SYSTEM

Các counter đã được ghi nhận gồm các quan hệ như:

```text
Insect -> dispel Doom
Spirit -> wake/remove Sleep
Bird -> remove Silence
Demon -> remove Bind
Plant -> remove Confusion
Undead -> remove Petrify
```

Phải implement dưới dạng data/rules.

Nếu một counter mapping còn chưa chắc chắn theo version, đánh dấu metadata:

```text
confidence: confirmed | likely | unknown
source_version: ...
```

Không tự coi guide của một version là universal truth cho mọi version.

---

# 11. RACE BUFF/DEBUFF IDENTITY

Các specialization đã được ghi nhận:

```text
Insect -> max HP
Spirit -> magic attack
Bird -> speed
Demon -> physical attack
Beast -> max MP
Plant -> defense
Undead -> critical chance
```

Mỗi race cần support:

* buff specialty;
* debuff specialty;
* native status;
* cleanse/counter;
* element/resistance identity.

---

# 12. PET STATS

Core pet stats đã biết:

```text
Strength
Agility
Stamina
Intelligence
Spirit
Defense
Critical
```

Primary relationship:

```text
Strength     -> Physical Attack
Agility      -> Speed / initiative related
Stamina      -> Max HP
Intelligence -> Magic Attack
Spirit       -> Max MP
```

Derived stat formulas phải nằm ở centralized rules module.

Không hard-code trực tiếp trong UI.

Do formula gốc chính xác chưa được xác minh đầy đủ, hãy tạo configurable rules:

```text
PhysicalAttackFormula
MagicAttackFormula
HPFormula
MPFormula
SpeedFormula
DefenseFormula
CritFormula
HitFormula
```

Implementation MVP có thể dùng reconstruction formula hợp lý, nhưng phải đánh dấu rõ là reconstructed, không phải exact original formula.

---

# 13. PET SPECIES VS PET INSTANCE

Bắt buộc tách:

```text
PetSpecies
```

khỏi:

```text
PetInstance
```

PetSpecies là static content.

PetInstance là cá thể persistent.

Hai pet cùng species phải có thể khác nhau về:

* gender;
* individual stat quality;
* growth/potential;
* resistance;
* status resistance;
* learned skills;
* level;
* EXP;
* star;
* generation;
* parentage;
* blessing/appraisal values;
* other hidden traits nếu sau này tìm được.

Ví dụ concept:

```json
{
  "id": "pet-instance-uuid",
  "species_id": "dark_crab",
  "level": 23,
  "gender": "female",
  "generation": 3,
  "quality": {
    "str": 1073,
    "agi": 944,
    "sta": 1031,
    "int": 725,
    "spi": 891
  },
  "resistances": {
    "dark": 18,
    "sleep": 4,
    "blind": 7
  }
}
```

Individual variance là core gameplay, không phải cosmetic feature.

---

# 14. PHYSICAL VS MAGIC PET ARCHETYPE

Pet/build phải support ít nhất:

```text
Physical
Magic
Hybrid nếu rules cho phép
```

Guides của game gốc từng khuyên:

```text
physical × physical
magic × magic
```

vì mixing build type có thể tạo offspring kém tối ưu.

Không nhất thiết biến recommendation này thành hard restriction nếu chưa có bằng chứng.

---

# 15. STAR / RARITY SYSTEM

Hệ thống pet cần support ít nhất khoảng:

```text
1★
2★
3★
4★
5★
```

Star ảnh hưởng:

* rarity;
* growth;
* progression;
* synthesis requirements;
* recipes;
* species access.

Không coi star là toàn bộ sức mạnh.

Generation refinement cũng phải ảnh hưởng pet quality.

Một 4★ generation cao có thể đáng giá hơn một 4★ generation thấp.

Architecture cần support:

```text
species star
instance generation
instance growth quality
lineage refinement
```

độc lập.

---

# 16. CAPTURE SYSTEM

Wild monster cần có thể:

* catchable;
* non-catchable;
* boss-only;
* synthesis-only;
* rare-capture.

Capture rate phải phụ thuộc vào state battle.

Game gốc có evidence rằng capture dễ hơn khi HP monster xuống thấp, khoảng vùng dưới ~20% trong một số guide.

Capture formula chính xác chưa xác minh.

Hãy implement generic formula module hỗ trợ:

```text
base capture rate
HP modifier
status modifier
species modifier
item modifier
level modifier
rarity modifier
server RNG
```

Toàn bộ RNG capture nằm server.

---

# 17. APPRAISAL / DIVINATION

Pet mới capture không nhất thiết expose toàn bộ value ngay theo gameplay gốc.

Cần support concept:

```text
capture
→ appraisal/divination
→ reveal/evaluate pet potential
→ keep/release/train/breed
```

Ranch hoặc pet-management hub phải có Divination/Appraisal.

Các chỉ số appraisal lịch sử có reference scale kiểu ~1000 trong một số version, nhưng exact formula chưa xác minh.

Hệ thống phải configurable.

---

# 18. RANCH

Ranch là subsystem quan trọng.

Ít nhất support:

* pet storage;
* pet management;
* divination/appraisal;
* breeding;
* synthesis;
* strengthening;
* lineage viewing;
* pet-related NPC.

Không biến ranch thành một menu placeholder duy nhất nếu về sau cần world interaction.

---

# 19. BREEDING / SYNTHESIS

Đây là core feature quan trọng nhất của game.

Hệ thống cần support nhiều version/ruleset.

Các requirement từng xuất hiện trong các version:

* minimum player level;
* minimum pet level;
* opposite gender;
* specific recipe;
* required synthesis item/Synthesis Soul;
* ranch NPC;
* possibly cross-race requirements;
* required parent species.

Không hard-code duy nhất một rule nếu source lịch sử thay đổi theo version.

Thiết kế rule engine/data definition cho recipe.

Pipeline cơ bản:

```text
validate parents
→ validate ownership
→ validate level/gender/race/recipe
→ validate materials/currency
→ lock resources
→ determine child species
→ inherit stats/growth
→ inherit resistances
→ inherit skills
→ apply mutation
→ apply strengthening/blessing
→ assign generation
→ create Lv1 child
→ consume/retire parents according to ruleset
→ commit transaction
```

Breeding phải chạy trong DB transaction.

Không được xảy ra:

```text
parents/material đã mất
nhưng child không được tạo
```

---

# 20. BREEDING RECIPES

Breeding/synthesis phải support recipe graph.

Ví dụ:

```text
target 5★ pet
├ parent A
│  ├ ancestor A1
│  └ ancestor A2
└ parent B
   ├ ancestor B1
   └ ancestor B2
```

Player phải có thể reverse-plan từ pet endgame về pet 1★.

Data model cần support:

```text
recipe_id
parent condition A
parent condition B
result species
result star
min level
gender requirement
race requirement
materials
currency
rare result
version
```

Website cần có breeding tree/planner sau này.

---

# 21. INHERITANCE

Pet offspring phải support inheritance ít nhất cho:

* base stats / potential;
* growth;
* resistance;
* status resistance;
* learned skills;
* race/bloodline;
* generation.

Exact original formula chưa được xác minh.

Do đó phải implement inheritance trong một centralized configurable module.

Ví dụ conceptual:

```text
child potential =
parent weighted average
+ generation modifier
+ strengthening
+ blessing
+ mutation
```

Nhưng không ghi chú formula giả định là “original formula”.

Phải có test/simulator cho breeding distribution.

---

# 22. SKILL INHERITANCE

Điểm cực kỳ quan trọng:

Offspring phải kế thừa dựa trên **skills parent đã thực sự học**, không đơn thuần toàn bộ species skill pool.

Do đó cần tách:

```text
species_skill_pool
```

và:

```text
pet_instance_learned_skills
```

Breeding logic đọc learned skills của parent.

Player có incentive:

```text
capture parent
→ train
→ learn desired skill
→ breed
```

---

# 23. STRENGTHENING

Game có concept dùng pet cùng/similar star level để cải thiện nền tảng cho breeding.

Cần tạo subsystem/rule placeholder cho:

```text
strengthening
```

và không trộn nó trực tiếp với leveling thông thường.

Strengthening có thể modify:

* potential;
* growth;
* inheritance quality;
* breeding quality.

Exact formula cần research/reconstruction.

---

# 24. BLESSING

Breeding/synthesis từng có Blessing mechanic.

Cần support:

```text
blessing level/value
blessing item/material
blessing inheritance modifier
```

Nếu remake không monetized, blessing item chuyển thành gameplay-earned material.

Exact formula chưa xác minh nên phải configurable.

---

# 25. BATTLE SYSTEM

Combat là turn-based.

Player avatar không phải combat unit chính.

Battle cần support:

```text
player pet(s)
vs
wild monster(s)
NPC/trainer pet(s)
arena/PvP pet(s)
boss
```

Battle state machine:

```text
WAIT_COMMAND
→ LOCK_COMMANDS
→ CALCULATE_ORDER
→ EXECUTE_ACTIONS
→ APPLY_END_TURN_EFFECTS
→ CHECK_VICTORY
→ NEXT_TURN
```

Action categories:

```text
ATTACK
SKILL
ITEM
CAPTURE
DEFEND nếu rules cần
SWITCH nếu rules cần
AUTO
```

Không cần copy UI cũ từng menu depth nếu UI đó chỉ là limitation của mobile Java đời cũ.

Giữ mechanic, hiện đại hóa UX.

---

# 26. DETERMINISTIC BATTLE

Battle engine phải cố gắng deterministic/reproducible.

Mỗi battle lưu:

```text
battle_id
seed
turn
commands
events
```

Server RNG phải deterministic theo battle seed và command sequence nếu khả thi.

Mục tiêu:

* replay;
* debugging;
* anti-cheat investigation;
* reproducible bug;
* balance simulation.

Battle event output ví dụ:

```json
[
  {
    "seq": 1,
    "type": "skill_cast",
    "actor_id": "pet_a",
    "skill_id": "sleep_powder"
  },
  {
    "seq": 2,
    "type": "status_applied",
    "target_id": "pet_b",
    "status_id": "sleep",
    "duration": 2
  }
]
```

Godot chỉ render animation từ event stream.

---

# 27. SPEED / INITIATIVE

Agility ảnh hưởng speed/attack order.

Exact initiative formula chưa xác minh.

Tạo centralized initiative calculator và config.

Không để UI/client tự sort actions.

---

# 28. MP / RESOURCE SYSTEM

Pet có MP.

Spirit liên quan Max MP.

Skills cần support MP cost.

Combat model phải có ít nhất:

```text
HP
MP
Physical Attack
Magic Attack
Defense
Speed
Critical
Hit/Evasion nếu rules cần
Element resistance
Status resistance
```

---

# 29. AUTO BATTLE / AUTO GRIND

Game gốc từng quảng bá auto-grinding miễn phí.

Game architecture phải support Auto mode cho PvE.

Auto battle logic có thể server-authoritative với strategy config:

```text
basic attack
priority skill
heal threshold
capture preference
MP management
```

Không cần implement full advanced AI ngay, nhưng architecture không được chặn feature này.

---

# 30. QUEST SYSTEM

Support ít nhất:

* main quest;
* side quest;
* repeatable quest;
* daily quest;
* boss quest;
* arena/progression quest.

Quest system cần data-driven conditions/actions.

Condition ví dụ:

```text
player level
pet level
kill monster
capture species
own item
talk NPC
reach map
clear arena
reputation
time window
```

Reward:

```text
EXP
pet EXP
gold
item
currency
reputation
unlock map
unlock recipe
```

Cần support quest reward scaling/reduction khi player/pet over-level nếu ruleset yêu cầu.

---

# 31. LEVEL / ZONE PROGRESSION

Historical route cần support reconstruction tương đương:

```text
1–10   Forest
10–15  Beach
15–20  Desert
20–25  Windrock
25–30  Nightmare
30–35  Saint Cemetery
35–40  Undersea
40–45  Time-Space
45–50  Ancient Ruins
```

Không coi exact level range là immutable nếu later source chứng minh version khác.

Content data phải versionable/tunable.

---

# 32. ARENA

Arena là progression system quan trọng.

Need support:

* arena tiers;
* minimum level;
* NPC challenge;
* unlock next zone/content;
* PvP extension.

Historical tier gates từng có dạng:

```text
Arena I   Lv10
Arena II  Lv15
Arena III Lv20
Arena IV  Lv25
Arena V   Lv30
```

Đưa vào initial reconstruction data nhưng mark as version-specific.

---

# 33. NPC SYSTEM

NPC cần data-driven.

Support role:

```text
quest giver
merchant
skill trainer
pet healer
pet manager
breeding NPC
arena master
teleporter
guild manager
auction manager
story NPC
```

NPC interaction cần server validation.

---

# 34. INVENTORY / ITEMS

Item system support:

* consumable;
* quest;
* capture item;
* healing;
* MP restore;
* stat item;
* skill-related item;
* breeding material;
* blessing material;
* synthesis soul;
* bag expansion;
* teleport-related;
* currency token;
* equipment nếu later source xác nhận.

Inventory mutations phải transactional cho economy-sensitive action.

---

# 35. ECONOMY

Need support at least:

```text
normal currency / gold
Magic Crystal or equivalent trade currency
items
auction
mail
```

Nếu original premium currency mechanic được tái dựng cho non-commercial clone/prototype, có thể convert acquisition thành gameplay reward.

Không introduce real-money monetization trừ khi explicitly requested sau này.

---

# 36. AUCTION HOUSE

Auction support:

* listing;
* starting bid;
* buyout;
* listing duration;
* listing/storage fee;
* transaction fee;
* sold item;
* unsold item return;
* mail delivery;
* currency transfer.

Auction buyout/bid phải dùng transaction/locking để tránh duplication.

Website cũng phải có ability browse/search auction sau này.

---

# 37. MAIL

Mail system support:

* system mail;
* auction item return;
* auction proceeds;
* rewards;
* attachments/items/currency;
* expiration nếu cần.

---

# 38. SOCIAL SYSTEMS

Architecture phải support:

* party;
* guild;
* chat;
* player inspect/interact;
* PvP/challenge;
* friend system nếu later source xác nhận.

Không cần hoàn thiện guild endgame ngay trong vertical slice.

---

# 39. WORLD SERVER MODEL

Go backend có thể dùng lightweight actor-like ownership.

Ví dụ:

```text
one zone/map instance
→ one owning goroutine
→ receives commands
→ owns mutable state
```

Avoid excessive shared-state mutex.

World movement không cần 60Hz simulation.

Khoảng 5–10Hz authoritative update là đủ cho dạng room-based 2D MMORPG này, tùy test.

Battle là event-driven và không cần continuous tick khi đang chờ command.

---

# 40. PERSISTENCE RULE

Không persist player position mỗi frame.

Online world state giữ trong memory.

Persist ở các điểm như:

* map change;
* logout;
* checkpoint;
* periodic save.

Economy-critical operation phải commit ngay:

* breeding;
* synthesis;
* inventory consumption;
* capture finalization;
* auction;
* trade;
* currency spending;
* important rewards.

---

# 41. MYSQL DATA MODEL

Thiết kế schema mới trong database riêng.

Các entity tối thiểu:

```text
accounts
sessions
characters

pet_species_reference nếu cần DB mirror
pet_instances
pet_instance_stats
pet_instance_resistances
pet_instance_skills
pet_lineage

items
character_inventory

quests
character_quests

maps/content reference nếu cần
character_world_state

battle_logs
battle_commands
battle_events

auction_listings
auction_bids

mail
mail_attachments

guilds
guild_members

player_events
```

Static game definitions ưu tiên version control trong repository.

Persistent player-owned state nằm MySQL.

Không nhất thiết normalize quá mức nếu gây phức tạp, nhưng lineage, ownership và transaction-sensitive fields phải queryable/indexable tốt.

---

# 42. STATIC GAME DATA

Static definitions không nên phụ thuộc hoàn toàn vào DB.

Ưu tiên:

```text
data/pets/
data/skills/
data/items/
data/recipes/
data/maps/
data/quests/
data/npcs/
data/spawns/
```

YAML hoặc JSON.

Server validate data khi startup hoặc build step.

Ví dụ pet species:

```yaml
id: dark_crab

names:
  zh_TW: ...
  zh_CN: ...
  vi: ...

race: undead
element: dark
star: 1
archetype: physical

capture:
  enabled: true
  base_rate: 0.18

base_growth:
  strength: ...
  agility: ...
  stamina: ...
  intelligence: ...
  spirit: ...
```

Static IDs không phụ thuộc localization.

---

# 43. GAME DATA CONFIDENCE

Do reconstruction dựa trên historical guides/videos/source, mỗi data point quan trọng nên có metadata tùy trường hợp:

```text
confirmed
likely
reconstructed
unknown
```

Có thể thêm:

```text
source_version
source_note
```

Đặc biệt cho:

* formulas;
* exact recipe;
* skill stats;
* spawn;
* quest reward;
* arena rule;
* version-specific mechanics.

Không silently invent exact historical values.

---

# 44. KNOWN UNKNOWN SYSTEMS

Các phần hiện chưa được xác minh chính xác 100%:

* damage formula;
* initiative formula;
* hit formula;
* crit formula;
* capture formula;
* offspring stat formula;
* exact resistance scale;
* full 300+ skill database;
* full synthesis graph;
* full monster database;
* full item/drop tables;
* complete quest database;
* complete late-game maps;
* exact military rank mechanic;
* exact divination formula;
* exact blessing formula;
* exact arena/PvP rules by version.

Architecture phải cho phép replace/tune những công thức này mà không rewrite domain.

Không giả định reconstructed formula là original.

---

# 45. PLAYER EVENT / AUDIT LOG

Tạo lightweight audit/event log.

Ít nhất track:

```text
pet_capture
pet_release
pet_breed
pet_strengthen

currency_gain
currency_spend

item_gain
item_spend

battle_win
battle_loss

auction_create
auction_buy
auction_sell

quest_complete
```

Mục tiêu:

* debugging;
* economy investigation;
* balance;
* support;
* anti-duplication.

Không cần full event sourcing.

---

# 46. WEBSITE

Web app là companion ecosystem chứ không phải authoritative game backend.

Các section mục tiêu:

## Public

* landing;
* news;
* patch notes;
* pet encyclopedia;
* skill encyclopedia;
* item encyclopedia;
* map information;
* breeding calculator.

## Account

* characters;
* owned pets;
* pet lineage;
* auction;
* mail;
* rankings;
* guild.

## Admin

* content inspection;
* pet/skill/item definitions;
* recipe editor;
* spawn inspection;
* quest tools;
* player inspect;
* grant item/currency;
* economy log;
* battle log;
* GM actions.

Web gọi Go API.

Không duplicate business rule chính trong Next.js.

---

# 47. BREEDING PLANNER WEBSITE

Đây là feature quan trọng.

Cho phép chọn target pet:

```text
Target ★★★★★
```

Website render dependency tree:

```text
Target
├ Parent A
│  ├ A1
│  └ A2
└ Parent B
   ├ B1
   └ B2
```

Planner phải đọc cùng static recipe definitions với game server.

Không maintain recipe copy riêng trong web.

---

# 48. PET LINEAGE VIEWER

Cho phép xem ancestry:

```text
Pet Gen4
├ Parent A Gen3
│  ├ ...
│  └ ...
└ Parent B Gen2
   ├ ...
   └ ...
```

Lineage là first-class feature.

---

# 49. GAME CLIENT

Godot chịu trách nhiệm:

* rendering;
* sprite/animation;
* UI;
* audio;
* map presentation;
* NPC presentation;
* battle animation;
* input;
* client prediction/interpolation nếu thật sự cần.

Client nhận server events và render.

Không duplicate authoritative formulas nếu tránh được.

---

# 50. WEBSOCKET MESSAGE NAMESPACE

Thiết kế namespace rõ ràng:

```text
auth.*
character.*
world.*
npc.*
battle.*
pet.*
breeding.*
inventory.*
quest.*
arena.*
party.*
chat.*
guild.*
notification.*
```

Message nên có:

```text
op
request_id
payload/data
```

Server event có:

```text
op
sequence
payload/data
```

Version protocol nếu cần.

---

# 51. AUTH

Support:

```text
register
login
logout
session
character selection
WebSocket authentication
```

Opaque session hoặc short-lived access token đều được nếu phù hợp codebase hiện tại.

Không để Godot giữ DB credentials.

---

# 52. SECURITY / CONSISTENCY

Backend validate:

* ownership;
* pet state;
* inventory;
* quest state;
* map state;
* range/interaction;
* battle turn;
* skill availability;
* cooldown nếu có;
* MP;
* target validity;
* auction ownership;
* currency.

Không trust client timestamps hoặc RNG.

---

# 53. TESTING

Ưu tiên test cho:

```text
battle
capture
breeding
inheritance
status effects
quest conditions
inventory
economy
auction
```

Đặc biệt phải có simulation tests cho breeding/capture distributions.

Ví dụ:

```text
simulate 100,000 breeding attempts
```

để xem distribution có đúng expected balance.

---

# 54. VERTICAL SLICE

Không cố implement toàn bộ MMORPG trong một commit.

Nhưng architecture phải support toàn bộ gameplay ở trên.

Vertical slice đầu tiên nên gồm:

```text
Severa City
Emerald Forest
Treasure Beach
```

Khoảng:

```text
10 pet species
20+ skills
capture
individual pet stats
appraisal
turn-based battle
status effects
skill learning
breeding/synthesis
lineage
basic quest
basic inventory
one arena tier
MySQL persistence
Godot client
Go WebSocket
```

Ví dụ pet initial content có thể gồm các species lịch sử như:

* Snail.
* Flower Fairy.
* Mushroom.
* Dark Crab.
* Wealth Turtle.
* Treasure Chest Monster.
* Sea Demon.
* Spider.
* Wolf.
* Windmill Spirit.

Không bắt buộc exact list nếu current reconstruction data có lựa chọn tốt hơn.

---

# 55. IMPLEMENTATION PRIORITY

Thứ tự ưu tiên:

```text
1. Inspect/refactor current repository
2. Establish new MySQL database + migrations
3. Static game-data loader
4. Character/session model
5. World/map protocol
6. Pet Species + Pet Instance
7. Turn-based Battle Engine
8. Status Effect Engine
9. Capture
10. Appraisal/Divination
11. Skill learning
12. Breeding/Synthesis
13. Lineage
14. Quest
15. Inventory/Economy
16. Arena
17. Auction/Mail
18. Social/Guild
19. Web encyclopedia/planner
20. Admin tools
```

Nếu project hiện tại đã có feature tương đương, reuse/refactor thay vì rewrite vô lý.

---

# 56. IMPORTANT DESIGN RULE

Khi phải chọn giữa:

```text
"giống Pokémon nhưng dễ code"
```

và:

```text
"giữ đúng pet lineage / synthesis DNA của 靈獸世界 Online"
```

hãy chọn phương án thứ hai.

Đặc trưng chính phải giữ là:

```text
wild pet
→ individual variance
→ appraisal
→ training
→ skill preparation
→ parent selection
→ recipe/synthesis
→ inheritance
→ generation improvement
→ rare/high-star pet
```

Đây là core game loop quan trọng nhất.

---

# 57. RESEARCH-FRIENDLY ARCHITECTURE

Project này là reconstruction của một game cũ và sẽ còn tìm được thêm:

* videos;
* screenshots;
* old guides;
* recipes;
* skill tables;
* maps;
* formulas.

Do đó tuyệt đối không thiết kế hệ thống theo cách khiến việc cập nhật historical data cần rewrite code.

Game rule/content cần data-driven tối đa.

Code chỉ implement generic engine.

Data quyết định:

```text
species
skill
status
recipe
spawn
quest
item
map
balance
```

---

# 58. DO NOT OVERENGINEER

Không introduce ở giai đoạn hiện tại:

* microservices;
* Kubernetes;
* Kafka;
* distributed event sourcing;
* multiple game server languages;
* Rust FFI;
* premature Redis dependency;
* premature binary protocol.

Go modular monolith + MySQL + WebSocket + Godot + Next.js là target hiện tại.

Rust có thể được dùng sau này cho tooling/simulation/WASM nếu có lợi ích rõ ràng, nhưng không introduce chỉ vì performance speculation.

---

# 59. FIRST TASK

Trước khi code feature mới:

1. Inspect toàn bộ repository hiện tại.
2. Viết ngắn gọn current architecture.
3. Xác định phần nào reuse được.
4. Xác định phần nào conflict với architecture target.
5. Không phá các feature đang hoạt động nếu không cần thiết.
6. Chuẩn bị incremental migration/refactor plan.
7. Tạo database MySQL game mới.
8. Thiết lập migrations.
9. Thiết lập domain models/data definitions cơ bản.
10. Sau đó bắt đầu vertical slice.

Không hỏi lại những quyết định đã được khóa trong prompt này trừ khi codebase hiện tại tạo ra technical blocker thực sự.

Nếu gặp chi tiết gameplay chưa rõ, không tự tạo fact giả.

Thay vào đó:

```text
- implement system extensibly;
- mark rule as reconstructed/unknown;
- document assumption;
- continue development.
```

---

# 60. END GOAL

End goal là một reconstruction có gameplay fidelity rất cao với 《靈獸世界 Online》, bao gồm:

```text
world exploration
map progression
NPC
quest
wild encounter
turn-based battle
capture
individual pet variance
pet appraisal
pet leveling
skill learning
race/element identity
status/control
resistance
star rarity
physical/magic builds
ranch
breeding
synthesis
strengthening
blessing
skill inheritance
stat inheritance
resistance inheritance
multi-generation lineage
recipe trees
arena
daily quests
auto battle/grinding
inventory
economy
auction
mail
party
guild
chat
PvP-compatible architecture
pet encyclopedia
breeding planner
lineage viewer
admin/content tooling
```

Không coi project hoàn thành nếu chỉ có:

```text
walk around
fight monster
catch monster
```

Breeding/lineage ecosystem phải là first-class gameplay system.

Sau mỗi major implementation phase, cập nhật tài liệu trong `/docs` để phản ánh:

* architecture;
* database schema;
* protocol;
* gameplay rules;
* confirmed original behavior;
* reconstructed behavior;
* remaining unknowns.
