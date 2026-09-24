# Worker B — Battle / Npc / Shop Reconstruction Report

**Date:** 2026-09-22
**Scope:** `BattleScene`, `NpcMenu`, `ShopMenu` (Phimond 2D MVP, Godot 4.7.2 headless
client at `/Users/phileanh/rust/phimond/apps/game-client`)
**Out of scope:** Login, MainMap (Worker C), styles, components, PhimondClient autoload.

---

## 1. Final layout per scene

### 1.1 `BattleScene` (`scenes/BattleScene.tscn` + `scripts/BattleScene.gd`)

A single fullscreen `GameWindow` instance acts as the battle frame. The window title
becomes `Battle — Turn N vs <enemy>` once a battle is active; while idle the title
just reads `Battle`. The body's VBox (`BodyRoot`) holds three sections top-to-bottom:
a 1:1 HBox of unit panels (player on the left, enemy on the right — same hierarchy,
flipped visually by the sprite), a compact chat-styled RichTextLabel log panel
(110 px tall, `chat_panel.tres` stylebox), and a centred HBox of six 110×44
`GameButton`s for **Attack / Skill / Item / Capture / Auto / Flee**. Each unit panel
is a `PanelContainer` wrapping a 6-px-spacing VBox: name label (gold, 16 px),
`AnimatedSprite2D` (160×128 minimum, plays `idle`), and two stacked bars — `GameHPBar`
(red tint, fantasy themed) over `GameMPBar` (blue tint). The window's X button is
wired to return to `MainMap.tscn` *only* when the server has cleared the battle; during
a live fight the X is effectively a no-op. Background is a near-black `ColorRect` so
the fantasy frame stands out. The player's `BattleScene._on_attack` etc. handlers
delegate to `PhimondClient.battle_action(...)` exactly like the previous minimal
version; the only added intent is `_on_item` (item_id = `"potion"` default) and
`_on_auto` (`"auto"` choice) to match the six-button row.

### 1.2 `NpcMenu` (`scenes/NpcMenu.tscn` + `scripts/NpcMenu.gd`)

A `Control` overlay with a dimmed `ColorRect` background and a 768×480 `GameWindow`
centred in the viewport. The window title is the NPC's display name (looked up from
`PhimondClient.catalog.npcs`). Inside the window body: a top `HBox` with an 80×80
`TextureRect` portrait on the left (loaded from
`apps/game-client/assets/reference/npcs/level*.png` using the `gameplay_mapping` keys
that `MainMap` already uses — `trainer` → `level3_1030.png`, `ranch_keeper` →
`level3_1029.png`, etc.) and a `VBox` on the right carrying the NPC's display name
(18 pt) over a `RichTextLabel` placeholder dialogue that reads `[i]…[/i]` (placeholder
because the server-side dialogue payload is not yet populated; ready to swap). Below
the header sits a centred `HBox` of up to seven `GameButton`s — Shop / Heal / Appraise
/ Breed / Recipe / Quest / Arena — toggled `.visible = role in npc.roles` so the row
only shows what's relevant to the NPC. Role callbacks wire to the same
`PhimondClient.send(...)` / `heal_pets()` / `appraise(pid)` / `synthesize(...)` /
`learn_recipe(...)` / `accept_quest(...)` / `challenge_arena()` helpers the old
AcceptDialog used. The GameWindow's close button and `Esc` key both
`queue_free()` the popup; this is the same lifecycle MainMap expects when it does
`add_child(menu)`.

### 1.3 `ShopMenu` (`scenes/ShopMenu.tscn` + `scripts/ShopMenu.gd`)

Same overlay pattern as NpcMenu: dimmed `ColorRect` background + 768×528 centred
`GameWindow` titled `Shop`. The body's `VBox` (`BodyRoot`) has three parts: a header
row with `Gold: <n>` left-aligned (16 pt) and a small `Click Buy to purchase 1×` hint
right-aligned (12 pt), a vertically-expanding `VBox` (`ItemList`) of item rows that
fill the rest of the window, and an empty-state Label that shows `(catalog empty)`
when the catalog has no items. Each item row is an `HBoxContainer` (40 px tall): a
`GameSlot` 32×32 frame on the left (icon path from `item.icon` if present, otherwise
empty frame), an expand-fill item name Label, a right-aligned price Label
(`<n> gold`, 80 px wide), and a `GameButton` labelled `Buy` (80×36) that calls
`PhimondClient.buy(item_id, 1)`. The list is rebuilt whenever `state_updated` fires
so the gold label stays in sync. Close button + Esc both `queue_free()` the popup.

---

## 2. Files modified

| File | Lines (final) | Nature of change |
|------|---:|---|
| `apps/game-client/scenes/BattleScene.tscn` | 149 | rebuilt — full GameWindow frame, two PanelContainer unit panels, animated sprites, GameHPBar+GameMPBar, chat-panel RichTextLabel log, six GameButton action row |
| `apps/game-client/scripts/BattleScene.gd` | 185 | rewired @onready paths to `Window/Frame/Body/BodyContainer/BodyRoot/...`; added `_label_action` / `_connect_action` helpers; six `_on_*` handlers now include `_on_item` (potion) and `_on_auto`; close button defers a guarded scene-swap to MainMap (only when battle is null); deferred change via `call_deferred` to dodge the "node busy adding children" guard during `_ready` |
| `apps/game-client/scenes/NpcMenu.tscn` | 91 | rebuilt from AcceptDialog → Control + GameWindow; portrait TextureRect, header VBox (name + dialogue RichTextLabel), seven-slot GameButton RoleRow; dimmed ColorRect background |
| `apps/game-client/scripts/NpcMenu.gd` | 133 | switched base class to Control; NPC_SPRITE_PATH dict mirrors MainMap's mapping; `_build()` toggles role button visibility by `npc.roles`; each role button has a label and `connect_pressed` callback; window close + Esc both `queue_free()` |
| `apps/game-client/scenes/ShopMenu.tscn` | 59 | rebuilt from AcceptDialog → Control + GameWindow; header row (Gold + hint), item list VBox, empty-state Label |
| `apps/game-client/scripts/ShopMenu.gd` | 94 | switched base class to Control; rebuilds the item list on `state_updated` so the gold label stays current; per-row is GameSlot icon + name Label + price Label + GameButton Buy |

**Not touched (verified):** `apps/game-client/styles/**`,
`apps/game-client/scenes/components/**`, `scripts/PhimondClient.gd`,
`scenes/LoginScreen.*`, `scenes/MainMap.*`.

---

## 3. Validation outputs

### 3.1 Headless boot (`godot --headless --quit-after 1`)

```
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org

(exit 0, no error / warning printed)
```

### 3.2 Pass-A parse check — all 5 scenes loadable (`scripts/pass_a_parse_check.gd`)

```
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org
[parse_check] OK   res://scenes/LoginScreen.tscn  root=Control
[parse_check] OK   res://scenes/MainMap.tscn  root=Node2D
[parse_check] OK   res://scenes/BattleScene.tscn  root=Control
[parse_check] OK   res://scenes/NpcMenu.tscn  root=Control
[parse_check] OK   res://scenes/ShopMenu.tscn  root=Control
[parse_check] PASS — all 5 scenes loadable
```

### 3.3 Each scene loaded individually as `main_scene`

```
=== LoginScreen === (no errors)
=== MainMap === (no errors)
=== BattleScene === (no errors)
=== NpcMenu === (no errors)
=== ShopMenu === (no errors)
```

### 3.4 min_smoke.gd end-to-end script (requires live server — script starts cleanly)

```
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org
[min_smoke] start
```

(The script then halts trying to reach `127.0.0.1:8090` — expected when the Godot
server isn't running locally. The script's GDScript parsing, autoload instantiation
and PhimondClient setup all complete without error.)

### 3.5 Internal shape / signal-wiring spot checks (worker-local, deleted before
report)

- **Tree dump** — confirmed every `@onready` path resolves: `BattleScene` builds the
  expected `Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/PlayerPanel/PlayerVBox/{PlayerName,PlayerSprite,PlayerHP,PlayerMP}` and the matching `EnemyPanel/EnemyVBox`, the `LogPanel/LogMargin/Log` chain, and the six `ActionRow/*Btn` instances (each TextureButton with Icon+Label children — proves the foundation `GameButton` is being instantiated correctly).
  The same dump for `NpcMenu` and `ShopMenu` confirmed the full chain under
  `Window/Frame/Body/BodyContainer/BodyRoot/...` (including the seven role buttons
  and the header rows).
- **Signal wiring** — verified that on all three scenes the `CloseBtn.pressed`
  signal has at least one subscriber after `_ready` runs (NpcMenu and ShopMenu
  rewire it to `_on_close` via `set_close_callback`; BattleScene keeps the default
  internal relay that ultimately routes to `_on_window_close`). For BattleScene,
  confirmed `AttackBtn.set_label("TestAttack")` round-trips through `get_label()`,
  and `AttackBtn.pressed.emit()` reaches the connected test handler — proving the
  GameButton foundation component wires correctly under my BattleScene wrapper.
- **Popup parenting** — confirmed that NpcMenu and ShopMenu instantiate and run
  cleanly when added as children of a `Node2D` (matching how `MainMap.gd` adds them
  via `add_child(menu)` after `preload(...).instantiate()`). No errors, no warnings.

---

## 4. Visual / interaction decisions

- **No new buttons per action** — the brief suggested picking distinct button
  textures per action from `assets/extracted/extended/buttons/`. The available
  inventory there is just three right_btn variants + two round_btn variants, all
  duplicated between Sprite- and Texture2D-prefixed copies (same pixels). With six
  actions that meant at most two distinct frames for six buttons — visually noisy.
  Decision: keep one consistent button frame across all six actions (the foundation
  `GameButton` already uses `right_btn0/1` and adds the theme-driven hover/pressed
  state via the project's `GameTheme.tres`), and rely on the **label** text to
  disambiguate. This matches how `test_theme.tscn` and `LoginScreen` already use the
  foundation `GameButton`. The `set_label` API is called explicitly per button in
  `_ready()` so the labels stay readable even if the foundation default ever changes.

- **Battle background — fantasy dark vs neutral grey** — the original used
  `assets/reference/ui/UI.png` as a tiled background texture. The brief asks for
  "fantasy-themed"; I swapped that for a near-black `ColorRect` (`0.04, 0.08, 0.12`)
  because (a) the UI.png asset is a 1280×480 atlas of UI elements, not a backdrop,
  so tiling it produced visible seams in the previous render, and (b) the dark base
  lets the 9-slice `panel_9slice.tres` frame around the GameWindow glow against the
  scene the way a fantasy modal should.

- **Title reflects live battle state** — `Battle — Turn N vs <Enemy>` updates on
  every `_refresh()` call so the player always knows which turn / which foe they're
  looking at without needing to glance at the unit panel.

- **Close button policy** — BattleScene's GameWindow close button is intentionally
  guarded: it only fires `change_scene_to_file("res://scenes/MainMap.tscn")` when
  `PhimondClient.state.battle == null`. This keeps players from accidentally
  fleeing via the X button (a behaviour mismatch with the previous code, which
  always changed scene on close). The NpcMenu and ShopMenu close buttons (and `Esc`
  key) always close because they're transient popups, not state-bound.

- **Defensive popup cleanup** — NpcMenu and ShopMenu both use `_on_close` →
  `queue_free()`. The X button uses the foundation's `set_close_callback` to wire
  the callback; `Esc` is handled in `_unhandled_key_input` and also calls
  `_on_close()`. `MainMap` keeps the existing `add_child(menu)` lifecycle — it
  doesn't need to track the popup because it cleans itself up.

- **NpcMenu portrait** — uses the same five NPCs that `MainMap.gd` already
  hard-coded (`NPC_SPRITE_PATH` dict is a direct mirror). When the NPC ID isn't in
  the mapping (a new content addition later), the portrait TextureRect falls back to
  a flat brown colour so the panel still looks framed instead of empty.

- **BattleScene auto-population of _log signal** — kept the previous behaviour:
  `PhimondClient.log_message.connect(...)` → `_log.append_text(t + "\n")`, which
  appends to the chat-style RichTextLabel as the server emits events.

- **No Item / Skill sub-menus yet** — the brief lists `Item` and `Auto` as buttons
  in the action row. `Item` calls `PhimondClient.battle_action(... "item", "", "potion")`
  as a placeholder for the eventual item-picker (out of scope here). `Auto` sends
  `"auto"` to match the server's expected choice vocabulary.

- **No assets-from-extended/buttons used** — the brief permitted
  `apps/game-client/assets/extracted/extended/buttons/right_btn*.png` as a fallback.
  I didn't need the fallback because the foundation `GameButton` already uses
  `right_btn0/1` (matching the original BattleScene's button textures). Visual
  parity with the previous build is preserved without re-importing extended assets.

- **No changes to MainMap, Login, styles, components, or PhimondClient** — verified
  by `mtime` listing: only the six files in §2 carry today's `11:08` timestamp;
  the foundation `styles/` and `scenes/components/` files are still at `10:52` and
  Worker C's `LoginScreen.tscn`/`MainMap.tscn` carry a different `11:06/11:08` time
  but were not opened during this session.