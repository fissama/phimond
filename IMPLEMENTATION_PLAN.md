# Pokémon-like 2D Game MVP — Implementation Plan

> Stack: **Godot 4 headless server + Phaser 3 web client (WebSocket)**
> Mục tiêu: playable trên web, solo, 1 map overworld, gặp quái hoang dã ngẫu nhiên lv 1–5, battle 4 lệnh (Đánh thường / Skill / Vật phẩm / Chạy), không bắt quái, không party switch giữa battle, asset AI.

---

## 1. Quyết định đã chốt

| Hạng mục | Chọn |
|---|---|
| Kiến trúc web | **B — Godot headless server + Phaser client riêng (WebSocket)** |
| Scope MVP | 1 map overworld + random encounter lv 1–5 + battle 4 lệnh |
| Asset | AI generate (PixelLab / SDXL) |
| Godot | 4.x (web export + GDScript đơn giản hơn C#) |
| Persistence | JSON file trên server (1 user = 1 file) |
| Auth | Nhập tên ở lần đầu, không có password/email cho MVP |
| Multiplayer | Architecture cho phép, không implement trong MVP |

---

## 2. Architecture tổng quan

```
┌─────────────────────────┐         WebSocket (JSON)        ┌─────────────────────────┐
│   Phaser Client (web)   │  ◄──────────────────────────►   │  Godot 4 Headless Server│
│  - Tilemap render       │                                  │  - Game state (authorit.)│
│  - Player sprite        │   Client → Server:               │  - Battle FSM           │
│  - Battle scene + UI    │     MOVE, ACTION                 │  - Random encounter     │
│  - Input (keyboard/     │   Server → Client:               │  - Damage formula       │
│    touch joystick)      │     STATE, ENCOUNTER, BATTLE_*   │  - Save/Load (JSON)     │
└─────────────────────────┘                                  └─────────────────────────┘
        │                                                              │
        │ static assets (PNG, audio)                                   │ save file
        ▼                                                              ▼
   Vercel/Netlify                                              Render/Railway/Fly.io
   (CDN)                                                       (persistent container)
```

**Tại sao tách 2 process:**
- Godot xử lý logic game (battle math, AI, encounter rate, save) — bạn không phải viết lại bằng JS.
- Phaser chỉ lo render + input — UI đẹp thoải mái, asset pipeline như web bình thường.
- WebSocket là lớp glue nhỏ (JSON message).

---

## 3. Tech stack

| Layer | Tech | Lý do |
|---|---|---|
| Game server | Godot 4.x + GDScript | Engine mạnh cho FSM + scene tree + signal; chạy headless OK |
| WebSocket | Godot built-in `WebSocketPeer` (server-side) | Không cần lib ngoài |
| Client framework | Phaser 3 + TypeScript | Mạnh cho tile map + scene; cộng đồng lớn; mobile-friendly |
| Build tool | Vite | Dev server + HMR + build static cực nhanh |
| State mgmt (client) | Native Phaser scene + một EventBus nhỏ | Không cần Redux cho MVP |
| HTTP (chỉ cho asset tĩnh) | Vercel/Netlify/Cloudflare Pages | CDN miễn phí |
| Server host | Render / Railway / Fly.io | Persistent container, free tier đủ cho MVP |
| Save | JSON file per user trên disk server | Đơn giản nhất; sau này chuyển Postgres dễ |
| Asset generation | PixelLab.app + SDXL fallback | PixelLab chuyên pixel art, style nhất quán hơn SDXL thuần |
| Audio (optional) | SFX freesound.org, BGM AI-generate | |

---

## 4. Project structure

```
phimond/
├── server/                          # Godot 4 headless
│   ├── project.godot
│   ├── server.gd                    # Entry: khởi WS server, port 8080
│   ├── net/
│   │   ├── ws_server.gd             # WebSocketServer wrapper
│   │   ├── message_router.gd        # Parse + dispatch client messages
│   │   └── protocol.gd              # Message type constants + JSON helpers
│   ├── game/
│   │   ├── world.gd                 # Tilemap state, player position, encounter zones
│   │   ├── player.gd                # Player class (x, y, name, party)
│   │   ├── monster.gd               # Monster class (id, lvl, hp, skills, types)
│   │   ├── skill.gd                 # Skill class (id, name, power, accuracy, effect)
│   │   ├── item.gd                  # Item class (id, name, effect)
│   │   ├── battle.gd                # Battle FSM + damage calc
│   │   ├── encounter.gd             # Random encounter rate per zone
│   │   └── data/
│   │       ├── monsters.json        # 6–8 monster definitions
│   │       ├── skills.json          # ~12–16 skill definitions
│   │       └── items.json           # 2–3 item definitions
│   ├── save/
│   │   └── save_manager.gd          # Đọc/ghi JSON file per player name
│   └── tests/
│       └── test_battle.gd           # GUT test cho damage formula
│
├── client/                          # Phaser 3 + TS
│   ├── package.json
│   ├── vite.config.ts
│   ├── index.html                   # Mount point
│   ├── src/
│   │   ├── main.ts                  # Khởi Phaser game
│   │   ├── net/
│   │   │   ├── socket.ts            # WS client wrapper, reconnect logic
│   │   │   └── protocol.ts          # Type definitions cho messages
│   │   ├── scenes/
│   │   │   ├── BootScene.ts         # Load assets, kết nối WS
│   │   │   ├── LoginScene.ts        # Nhập tên (lưu localStorage)
│   │   │   ├── WorldScene.ts        # Tilemap + player + encounter zones
│   │   │   └── BattleScene.ts       # Battle UI + animation
│   │   ├── ui/
│   │   │   ├── BattleMenu.ts        # 4 nút: Attack/Skill/Item/Flee
│   │   │   ├── SkillPicker.ts       # Submenu chọn skill
│   │   │   ├── ItemPicker.ts        # Submenu chọn item
│   │   │   └── HPBar.ts             # Thanh máu
│   │   ├── entities/
│   │   │   ├── Player.ts            # Player sprite + movement
│   │   │   ├── MonsterSprite.ts     # Monster render
│   │   │   └── TallGrass.ts         # Encounter zone marker
│   │   └── assets/                  # PNG sprite sheets + tileset + audio
│   │
│   └── tsconfig.json
│
├── shared/                          # Spec/data shared giữa 2 bên
│   └── PROTOCOL.md                  # WebSocket message reference
│
└── IMPLEMENTATION_PLAN.md           # File này
```

---

## 5. WebSocket Protocol

JSON, mỗi message 1 dòng. Field `type` luôn có. Mọi thông tin gameplay chỉ đi qua WS — không trust client.

### Client → Server

```jsonc
// Bắt đầu session
{ "type": "HELLO", "name": "phileanh" }

// Di chuyển 1 ô trong overworld (grid-based)
{ "type": "MOVE", "dir": "up" }      // "up" | "down" | "left" | "right"

// Battle action (chỉ khi server gửi BATTLE_START)
{ "type": "ACTION", "choice": "attack" }
{ "type": "ACTION", "choice": "skill", "skillId": "thunder_shock" }
{ "type": "ACTION", "choice": "item",   "itemId": "potion" }
{ "type": "ACTION", "choice": "flee" }
```

### Server → Client

```jsonc
// World state update (broadcast cho mọi client cùng phòng — MVP có thể chỉ 1 client)
{ "type": "STATE", "players": [{ "name": "phileanh", "x": 5, "y": 3, "dir": "up" }] }

// Bắt đầu battle, kèm data quái hoang dã
{
  "type": "BATTLE_START",
  "wild": {
    "id": "pikachu", "name": "Pikachu", "level": 3,
    "hp": 22, "maxHp": 25,
    "skills": ["thunder_shock", "tail_whip"],
    "sprite": "monster_pikachu.png"
  },
  "player": { "hp": 25, "maxHp": 25, "skills": [...], "items": [{ "id": "potion", "qty": 3 }] }
}

// Sau mỗi action: server trả sequence sự kiện để client animate
{
  "type": "BATTLE_TURN",
  "events": [
    { "kind": "text", "msg": "Pikachu used Thunder Shock!" },
    { "kind": "damage", "target": "player", "amount": 7, "hp": { "cur": 18, "max": 25 } },
    { "kind": "text", "msg": "You used Scratch!" },
    { "kind": "damage", "target": "wild", "amount": 5, "hp": { "cur": 17, "max": 25 } }
  ],
  "awaitingInput": true   // true nếu đến lượt player chọn action tiếp
}

// Kết thúc battle
{ "type": "BATTLE_END", "result": "win" | "flee" | "lose", "xpGained": 12 }
```

Định nghĩa đầy đủ trong `shared/PROTOCOL.md` — viết trước khi code để 2 bên cùng tham chiếu.

---

## 6. Data Model (GDScript sketch)

```gdscript
# monster.gd
class_name Monster
var id: String                 # "pikachu"
var name: String
var level: int
var max_hp: int
var hp: int
var attack: int
var defense: int
var speed: int                 # dùng cho turn order
var skills: Array[String]      # skill ids
```

```gdscript
# skill.gd
class_name Skill
var id: String                 # "thunder_shock"
var name: String
var power: int                 # base damage
var accuracy: int              # 0..100, % đánh trúng
var kind: String               # "physical" | "special"
var effect: Dictionary         # optional: {"stat": "attack", "delta": -1}
```

**Damage formula (MVP):**
```
damage = max(1, ((power * attacker.attack / defender.defense) / 2) + rand(-2..2))
```
Đơn giản, dễ test, balance sau. Type/element chưa có trong MVP (chờ quyết định ở vòng sau).

---

## 7. Phases & Deliverables

### Phase 0 — Setup (1–2 ngày)
- [ ] Cài Godot 4.x, Node 20+, tạo 2 project skeleton (`server/`, `client/`)
- [ ] Tạo Git repo, `.gitignore` chuẩn (Godot + Node)
- [ ] Hello WS: Godot server in log mỗi khi nhận message; client hiện "connected" badge
- [ ] Viết `shared/PROTOCOL.md` xong trước khi code phase 1

### Phase 1 — Vertical slice: di chuyển trong overworld (3–4 ngày)
- [ ] Server: Tilemap 20×15 ô, player entity, accept `MOVE` message, broadcast `STATE`
- [ ] Client: Phaser `WorldScene`, render tilemap (placeholder ô vuông 32×32 màu), player sprite tròn, keyboard input (WASD/arrow), gửi `MOVE`, nhận `STATE` để render vị trí server-authoritative
- [ ] Test local: mở 2 tab, di chuyển 1 tab thấy tab kia update (chứng minh WS sync OK)
- [ ] Vẽ "tall grass" zones bằng overlay màu xanh đậm — chưa có logic encounter

### Phase 2 — Monster data + encounter trigger (3–5 ngày)
- [ ] Server: 6–8 monster definitions trong `data/monsters.json`, mỗi con 2 skills
- [ ] Server: Khi player bước vào tall grass zone, 30% cơ hội / bước → gửi `BATTLE_START` với monster lv random 1–5
- [ ] Client: Chuyển sang `BattleScene`, render wild monster + player monster (placeholder), HP bar
- [ ] Client: 4 button menu (Attack/Skill/Item/Flee) gửi `ACTION`
- [ ] Test: đi vào bụi cỏ → vào battle UI

### Phase 3 — Battle mechanics (4–6 ngày)
- [ ] Server: Battle FSM xử lý 4 action — Attack (dùng `damage formula`), Skill (lookup skill data, áp dụng effect nếu có), Item (Potion heal +20 HP, giảm qty), Flee (luôn thành công với wild encounter)
- [ ] Server: Turn order dựa trên `speed`, sau mỗi lượt build `events[]` array gửi về client
- [ ] Server: Check win/lose/flee → gửi `BATTLE_END`, cộng XP cho player monster (đơn giản: +10 XP mỗi wild thắng, level up khi đủ 30 XP → +max_hp, +attack)
- [ ] Client: Animate damage (sprite flash), update HP bar mượt, hiện text log cuộn
- [ ] Client: SkillPicker submenu (liệt kê skills của player monster), ItemPicker (liệt kê items trong inventory)
- [ ] Test full loop: gặp quái → chọn attack → quái đánh lại → dùng skill → uống potion → chạy → thắng → XP

### Phase 4 — Asset AI + polish (3–5 ngày)
- [ ] Tạo "style reference sheet" 1 sprite chuẩn → dùng làm reference cho AI tool sinh các sprite khác (giữ style nhất quán)
- [ ] Generate 6–8 monster sprites (front-facing, 96×96 px) qua PixelLab
- [ ] Generate tileset (grass, path, tree, water, tall grass) — 16×16 tile
- [ ] Generate UI: button frame, menu background, font (nếu cần)
- [ ] Replace placeholder trong client, xử lý sprite sheet + frame config
- [ ] Bonus: 1–2 SFX (click, attack, hit) từ freesound.org

### Phase 5 — Save/Load + Login (1–2 ngày)
- [ ] Client: LoginScene nhập tên → lưu `localStorage.playerName` → gửi `HELLO`
- [ ] Server: `SaveManager` đọc/ghi `saves/<name>.json` (party, xp, items)
- [ ] Server: Khi reconnect → load save, gửi state tương ứng
- [ ] Test: chơi → tắt browser → mở lại → tiếp tục đúng chỗ

### Phase 6 — Deploy (2–3 ngày)
- [ ] **Server (Render):** tạo `Dockerfile` chạy Godot headless (`godot --headless --path /app/server`), expose port 8080, persistent volume cho `saves/`
- [ ] **Client (Vercel/Netlify):** `npm run build` → upload `dist/` → config env var `VITE_WS_URL=wss://...`
- [ ] **WS CORS:** Render cần allow origin của client domain
- [ ] Test full pipeline: client URL → kết nối được WS → chơi được → save persist

### Phase 7 — Test & iterate (ongoing)
- [ ] Cross-browser: Chrome, Firefox, Safari
- [ ] Mobile: thêm virtual joystick (Phaser plugin `phaser3-virtual-joystick`) cho touch
- [ ] Perf: bundle size, draw call, FPS check
- [ ] Bug bash 1 ngày tự chơi + mời 1–2 người test

**Timeline ước tính:** 3–4 tuần full-time, hoặc 6–8 tuần part-time 50%.

---

## 8. Asset pipeline (AI)

Pixel art qua AI rất dễ bị **style drift** giữa các sprite. Workflow đề xuất:

1. **Tạo 1 "hero sprite"** đầu tiên (vd: 1 con quái thử nghiệm) bằng PixelLab cho đến khi ưng style + palette.
2. **Lưu prompt + style keywords** đã dùng, ví dụ:
   ```
   "Pokemon-style monster, 32x32 pixel art, Game Boy Advance palette,
    centered, front-facing, transparent background, 4-frame idle,
    inspired by <hero sprite reference>"
   ```
3. **Generate các sprite còn lại** với cùng prompt + attach hero sprite làm reference image (img2img).
4. **Review & chỉnh tay** trong Aseprite (10–20 phút/sprite) để sửa lỗi AI.
5. **Tileset** generate riêng, dùng cùng palette hex codes.

**Tools:**
- **PixelLab.app** — tốt nhất cho pixel art có flow (~$5/lần mua credits hoặc subscription)
- **Aseprite** — chỉnh tay sprite sheet, export PNG
- **SDXL + ControlNet** — nếu PixelLab không đủ, nhưng pixel output cần hậu kỳ nhiều hơn

**Không cần làm asset đẹp ngay** — Phase 1–3 dùng placeholder, Phase 4 mới thay. Đừng để asset block gameplay.

---

## 9. Deployment chi tiết

### Server (Render.com, free tier đủ cho MVP)

```dockerfile
# server/Dockerfile
FROM barichello/godot-docker:4.2
WORKDIR /app
COPY server/ ./
EXPOSE 8080
CMD ["godot", "--headless", "--path", "/app", "res://server.gd"]
```

- Persistent disk gắn vào `/app/saves`
- Env var `WS_PORT=8080`

### Client (Vercel)

```json
// client/package.json scripts
"dev": "vite",
"build": "tsc && vite build",
"preview": "vite preview"
```

- Vercel project root = `client/`
- Env: `VITE_WS_URL=wss://phimond-server.onrender.com`
- Build output = `client/dist/`

### Connection flow
1. User mở `https://phimond.vercel.app`
2. BootScene connect `wss://phimond-server.onrender.com`
3. Server accept → gửi HELLO challenge → client respond
4. LoginScene hiện nếu chưa có name → user nhập → localStorage lưu
5. WorldScene render với state từ server

---

## 10. Risks & open questions

| Rủi ro | Mitigation |
|---|---|
| Godot headless trên Render có thể sleep khi idle (free tier) | Dùng paid tier $7/tháng, hoặc cron ping mỗi 5 phút |
| Phaser + Vite bundle lớn (~500KB cho Phaser core) | Code-split, lazy-load BattleScene assets |
| AI pixel art không nhất quán style | Style reference sheet + hậu kỳ Aseprite |
| WebSocket disconnect giữa battle | Client retry + reconnect, server giữ battle state 30s chờ reconnect |
| Save file corruption | Atomic write (ghi file `.tmp` → rename) |
| Mobile Safari audio | Polyfill hoặc yêu cầu user interaction trước khi play SFX |

**Câu hỏi để bạn quyết sau nếu mở rộng:**
- Có muốn **type/element system** (Fire/Water/Grass) cho vòng 2?
- Có muốn **shop + buy items** hay chỉ drop sau battle?
- Có muốn **evolution** cho monster?
- WebSocket hiện tại single-player-per-server; muốn **multiplayer thấy nhau trên map** chỉ cần mở rộng `players[]` array — đã có sẵn trong protocol.

---

## 11. Bước tiếp theo bạn làm ngay

1. **Tạo 2 project skeleton** theo structure ở mục 4.
2. **Cài Godot 4 + Node 20 + Vite + Phaser 3.**
3. **Làm Phase 0: Hello WS** — verify pipeline Godot ↔ Phaser chạy trước khi đụng gameplay.
4. Khi có gì kẹt (compile error Godot, TS config Phaser, deploy Render) — quay lại đây, mình debug cùng.

Mình recommend bắt tay vào Phase 0 hôm nay. Khi bạn stuck ở bước nào, paste error hoặc mô tả — mình giúp tiếp.
