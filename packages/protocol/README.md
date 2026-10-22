# Phimond v1 protocol

Go server default http://127.0.0.1:8090. New Godot and Next.js clients only; legacy protocol unchanged.

HTTP:
- GET /healthz
- GET /api/content -> catalog object (species,skills,statuses,races,maps,npcs,items,recipes,quests,rules) each definitions map keyed by id; rules object. Species: id,name,race,element,star,archetype,base (strength,agility,stamina,intelligence,spirit,defense,critical),skills (list of ids),capture_rate,catchable,confidence,source. Recipe: id,name,parent_a,parent_b,result,min_level,min_player_level,opposite_gender,same_star,cross_race,consume_parents,soul_cost,gold_cost,confidence,source. Map: id,name,width,portals [{id,x,to,spawn}],spawns [species ids],min_level,arena_required,confidence. NPC: id,name,map_id,x,roles [strings]. Skill: id,name,element,kind (physical/magic/status/heal/cleanse/buff),target (enemy/self),power,mp_cost,hit,status,duration,cleanse,stat,modifier,learn_level,inheritable,confidence.
- POST /api/register or /api/login {username,password} -> {token,character_id}; register creates character/starter. token opaque; do not log or put it in URLs. REST Bearer Authorization. Browser may use proxied Next routes.
- POST /api/logout Bearer token -> {ok:true}
- GET /api/character Bearer token -> character snapshot below.
- GET /api/lineage/{pet_id} Bearer token -> {pet:pet,parents:[recursive nodes]} (includes retired ancestors)

WS /ws: first frame {op:"auth.session",request_id:"...",data:{token}}. Subsequent {op,request_id,data}. Unique request_id per action (a deliberate retry must reuse the same ID and intent; clients do not automatically retry uncertain mutations). Server responds {op:"state",request_id,sequence,data:{character,events,presentation?}} or {op:"error",request_id,data:{message}}. Sequence=character revision, including acknowledged in-memory movement awaiting checkpoint. Initial auth returns the same wrapper with no replayable events. Polling via character.get supported. Game intents:
world.move {direction:"left"|"right"|"up"|"down"}; world.portal {portal_id}; world.encounter {spawn_id?}; npc.interact {npc_id}; pet.appraise {pet_id}; pet.activate {pet_id}; pet.learn {pet_id,skill_id}; pet.release {pet_id}; pet.strengthen {pet_id,donor_id}; breeding.synthesize {parent_a,parent_b,recipe_id,blessing:0|1}; recipe.learn {recipe_id}; quest.accept/quest.claim {quest_id}; shop.buy {item_id,quantity}; arena.challenge {}; battle.action {battle_id,turn,choice:"attack"|"skill"|"capture"|"defend"|"item"|"auto"|"flee",skill_id?,item_id?}; pet.heal {}. Service role NPC must be nearby for appraisal/breeding/learning/healing/shop/quest/arena. role NPCs x=6 in respective rooms. Root city spawn x=6, exits at 0/39. world.move moves 1 integer step.

`maps[*].wild_spawns` contains stable `{id,species_id,x,y}` entries derived from each map's existing species pool. Contact UI sends `world.encounter {spawn_id}` after an acknowledged move enters a spawn's one-cell X/Y contact area. The server validates current map and proximity and uses that spawn's species, while still owning individual stats/level/RNG/battle calculations. Invalid contact is rejected without changing state. Omitting `spawn_id` preserves the legacy random-pool encounter for older clients. Contact is a separate durable intent, not part of the cached movement checkpoint path. The client latches contact until leaving its area to avoid immediately restarting after battle.

Character snapshot: {id,name,level,xp,gold,crystals,map_id,x,active_pet_id,revision,pets:[{id,species_id,name,level,xp,gender,star,generation,refinement,appraised,retired,quality:{stat:number},growth:{stat:number},resistances:{element:number},status_resistances:{status:number},skills:[ids],parents:[ids],strengthening,blessing,hp,mp,max_hp,max_mp,attack,magic,defense,speed,critical}],inventory:{id:qty},recipes:[id],quests:{id:{progress,claimed}},arena_tier,battle:null|{id,turn,phase,result,units:[{id,name,side:"player"|"enemy",species_id,hp,max_hp,mp,max_mp,statuses:[{id,remaining}]}]}}. Hidden pet potential/resistances absent until appraisal. Battle events: {seq,type,actor_id,target_id,amount,message}; clients render, never calculate.

Public world presence can be added without changing gameplay operations. No client outcome/RNG fields accepted.

## Implementation notes

HTTP GET /api/battles returns `{battles:[...]}` for the authenticated account's last 20 completed battles. Public battle records include outcomes/events but omit seeds, PRNG state, commands and private pet snapshots. Internal replay state remains server-only. `character.get` reads the latest snapshot without a mutation. All other accepted operations increment revision, including a discrete movement checkpoint; rejected actions do not. Duplicate request IDs return the current snapshot without spending resources again. Client must render events only once per revision.

Numeric intent fields must be JSON integers. Godot parses received JSON numbers as floats, so convert `battle.turn` with `int(...)` when sending. Older-server `events` may be null; treat it as an empty array. Maps with no wild creatures may have `wild_spawns:null`; clients normalize this to an empty list. Maps have `height`, characters and NPCs have `y`. Buffs are `{stat,multiplier,remaining,applied_turn}` on battle units. Status durations do not tick down on their application turn. Session tokens go only in first-frame data or Authorization headers, never query strings.

## P00 public presentation contract

- Auth, `character.get`, and duplicate receipt responses are state-only: `events: []`, no `presentation`. A duplicate can return newer state; its unrelated last events must not replay.
- A newly applied action has `data.events` ordered within that response. `event.seq` restarts at 1 for each Apply, so never use it as a battle/session-global dedup key. Dedup accepted batches by character revision within the current identity/session.
- Active battle updates may include `presentation: {battle_id}`. Finishing actions include `{battle_id, completed_battle}` while `character.battle` is null. Completed battle is selected by the action's battle ID and sanitized through the same public Snapshot projector. No seed, RNG, commands, embedded private pet, full history or hidden appraisal is added.
- Client treats character as authoritative immediately, keeping the terminal battle only as a render cache. Effects complete before world input/contact/NPC resumes. Disconnect clears the cache; resuming state is not historical effect playback.
- `PhimondClient.state_batch_received(revision, character, events, presentation)` is the atomic active-renderer signal. Legacy `state_updated`/`events_received` consumers remain supported; active room must not process both paths.
- Presentation is additive; an old server without it restores authoritative state but cannot supply new terminal feedback. No save migration or new gameplay outcome calculation is needed.

## P01 world 2D (v1.0.0, ADR-P01-01) — cộng thêm

Tọa độ là ô nguyên `(x, y)`: x sang phải, y xuống dưới, 1 ô = 1 đơn vị world. Map nạp từ `data/maps/p01/*.json`; 5 map cũ (`severa`, `forest`, `beach`, `ranch`, `arena`) đã gỡ.

- `/api/content` → `maps[id]` thêm: `kind`, `theme`, `level` (cấp quái khuyến nghị, không phải điều kiện vào), `spawn_default {x,y,face}`, `respawn_to`, `walk` (lưới RLE: hàng nối bằng `/`, `.` đi được, `#` chặn; ô NPC/trụ đã bị chặn sẵn), `layout` (bố cục cảnh cho client), `facades`, `backdrop`, `pedestals [{index,x,y,starter,species}]`, `pillar {x,y,npc,dest:[{map,arrive,locked,min_level}]}`, `wild_spawns [{id,zone,species_id,x,y,respawn_s}]`.
  `portals[]` đổi thành `{id, rect:[x,y,w,h], to, arrive:{x,y,face}, locked?, requires?, redirect?:{if_visited,to,arrive}}` (không còn `x/spawn`).
  `npcs[id]` lấy vị trí từ map, thêm `face`, `dialogue`.
- `world.move`: từ chối ô bị chặn (`"Không đi được vào đó"`), không tăng revision.
- `world.portal {portal_id}`: hợp lệ khi đứng **trong** `rect`. Cổng `locked` → `"Khu vực này chưa mở"` (khi đứng trong/kề). `requires:"has_pet"` cần có pet. Có `redirect` và đã từng vào `if_visited` thì đi tới `redirect.to`. Đặt `map_id/x/y = arrive`.
- `npc.interact`, mọi dịch vụ NPC (`pet.heal`, `shop.buy`, `pet.learn`, `quest.*`…): đứng kề NPC, Chebyshev ≤ 1 (cả chéo). Sự kiện `npc_dialogue` có `actor_id` = id NPC.
- `starter.choose {pedestal}` (mới): chỉ khi chưa có pet và đứng kề bệ; nhận pet khởi đầu đã giám định rồi dịch chuyển một chiều tới điểm đến của cổng `requires:"has_pet"` (Bìa Rừng). Sự kiện `starter_chosen`, `map_enter`.
- `pillar.travel {map_id}` (mới): đứng kề trụ hoặc NPC vận hành; đích `locked` → `"Khu vực này chưa mở"`. Sự kiện `teleport`, `map_enter`.
- `world.encounter {spawn_id}`: đứng kề điểm quái (Chebyshev ≤ 1) và điểm quái không đang ẩn. Mọi kết quả trận hoang (thắng/thua/bắt/chạy/hòa) làm điểm đó ẩn `respawn_s` giây **riêng cho người chơi đó**. Thua: về `spawn_default` của `respawn_to`, hồi đầy HP/MP mọi pet, sự kiện `map_enter` + `respawn`. Bỏ `spawn_id` vẫn là gặp ngẫu nhiên kiểu cũ ở map có quái.
- Snapshot nhân vật thêm `visited: [map_id]`, `spawn_hidden: {spawn_id: unix_ms}` (chỉ điểm còn ẩn), `server_time_ms`; battle thêm `spawn_id`.
- Nhân vật mới: ở `summoning_hall_main_hall`, chưa có pet. Nhân vật ở map/ô không còn hợp lệ được đưa về `spawn_default` (map cũ → Quảng Trường, hoặc Triệu Linh Điện nếu chưa có pet) ở intent kế tiếp.
