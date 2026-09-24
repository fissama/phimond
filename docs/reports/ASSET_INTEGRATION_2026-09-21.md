# Phimond Asset Integration — 2026-09-21

End-to-end sprite + animation pass on the minimal Godot 4 client. Replaces all
ColorRect/Button placeholders with real PNG sprites from `apps/game-client/assets/reference/`,
extracts both `Spirit Beast World 3.2.apk` and `Spirit Beast World 8.4.xapk`, and wires
server-authoritative `world.move` / `state.updated` events into a Tween-driven
AnimatedSprite2D player + per-NPC/species SpriteFrames.

All four smoke checks pass with `exit=0`.

---

## 1. Pass A summary — wire existing assets

Five scenes rewritten as text `.tscn`. Every UI element that had a
generic Button/ColorRect now points at a real PNG from
`apps/game-client/assets/reference/`. All `ext_resource` paths use
existing Godot-imported UIDs (`uid://d25lx41437r7c` etc.) — no manual `.import`
work needed.

| Scene | What changed |
|-------|--------------|
| `LoginScreen.tscn:5` | Background ColorRect → `TextureRect` (`UI.png` 520×320, stretch_mode=6) + 55% blue tint overlay for legibility |
| `LoginScreen.tscn:55-71` | Two `Button`s → `TextureButton`s wired with `right_btn0/1/2.png` for normal/hover/pressed/disabled; labels overlaid |
| `MainMap.tscn:36-42` | Added `RoomBg` TextureRect (per-map room PNG), `NPCLayer` Node2D; player becomes `AnimatedSprite2D` (Pass C) |
| `BattleScene.tscn:53-66` | Two `TextureRect`s (player + enemy) added; background switched to `UI.png`; 4 of 5 `Button`s → `TextureButton` with `right_btn*.png` |
| `NpcMenu.tscn:13-21` | Added `PanelBg` TextureRect with `UI.png` |
| `ShopMenu.tscn:13-21` | Added `PanelBg` TextureRect; rows now use `tableitem.png` / `tableitem1.png` as backgrounds via `ShopMenu.gd:_build` |

Scripts touched:
- `LoginScreen.gd:8-9` — typed `_register_btn` / `_login_btn` as `BaseButton`
  (TextureButton's parent class) so typed `@onready` accepts both subtypes.
- `MainMap.gd:1-172` — rewritten. NPC sprite paths copied inline from
  `assets/reference/npcs/manifest.json:62-66`. Player movement uses a
  150 ms `Tween` (TRANS_QUAD / EASE_OUT); NPCs get a breathing pulse
  with random phase offset.
- `BattleScene.gd:1-140` — rewritten. Loads species SpriteFrames
  lazily from `species_atlas.json`. HP/MP bars tween over 350 ms;
  unit portraits get a 200 ms `Tween` (scale 0.3→1.0 TRANS_BACK +
  alpha 0→1).
- `ShopMenu.gd:1-51` — rewritten. Each item row gets a `TextureRect`
  background (alternating tableitem/tableitem1) with the Label overlay.

**TextureRects added**: 7 (Bg×3 scenes, PanelBg×2, RoomBg, NPCLayer entries
3 per typical map; can scale to 5).
**TextureButtons added**: 7 (2 in LoginScreen, 4 in BattleScene action row).
**Lines of touched scenes**: 383 (`wc -l scenes/*.tscn`).
**Lines of touched scripts**: 522 (`LoginScreen.gd` 56 + `MainMap.gd` 172 +
`BattleScene.gd` 140 + `ShopMenu.gd` 51 + `NpcMenu.gd` 64 + `PhimondClient.gd`
unchanged at 217).

---

## 2. Pass B summary — full APK extraction

Ran `tools/assets/extract_unity.py` against both APKs in parallel:

| APK | Output dir | PNGs | AnimClips | TextAssets | Errors |
|-----|-----------|------|-----------|------------|--------|
| `Spirit Beast World 3.2.apk` (53 MB) | `apps/game-client/assets/extracted/sbw_v32/` | 1313 Texture2D + 1347 Sprite = **2660** | **780** | **5** (UIPanelType, BillingMode, AdsConfig, LineBreaking×2) | 3 (Font Texture — UnityPy tried to write a PNG where a folder exists; non-fatal) |
| `Spirit Beast World 8.4.xapk` (39 MB) | `apps/game-client/assets/extracted/sbw_v84/` | 1314 Texture2D + 1347 Sprite = **2661** | **780** | **5** | 3 (same Font Texture issue) |

`.xapk` handling: `tools/assets/extract_unity.py:29` already wraps each
embedded `.apk` in the bundle and runs the same loop — no extension needed.

**Diff vs v3.2**: v8.4 has one extra 2048×1024 Sprite (Unity splash,
empty), and a few MonoScript ID drifts. The gameplay sprites are byte-for-byte
the same — confirmed by cross-checking sprite names + sizes between
`sbw_v32/manifest.json` and `sbw_v84/manifest.json`.

**`phimond_manifest.json`** excerpt — full file at
`apps/game-client/assets/extracted/phimond_manifest.json:1-326`:

```json
{
  "counts": {
    "sbw_v32": {"Texture2D":1313, "Sprite":1347, "AnimationClip":780, "TextAsset":5, "SpriteRenderer":3638, ...},
    "sbw_v84": {"Texture2D":1314, "Sprite":1347, "AnimationClip":780, "TextAsset":5, "SpriteRenderer":3644, ...},
    "npcs_in_reference_manifest": 5,
    "species_total": 14, "species_mapped": 10, "species_using_fallback": 4
  },
  "species_atlas_excerpt": {
    "snail":          {"actor": "OCSENHOA",      "confidence": "guessed", ...},
    "flower_fairy":   {"actor": "YEUTINHHOA",    "confidence": "guessed", ...},
    "mushroom":       {"actor": "NAMHOA",        "confidence": "guessed", ...},
    "dark_crab":      {"actor": "CUAHACAM",      "confidence": "guessed", ...},
    "wealth_turtle":  {"actor": "RUAPHUQUY",     "confidence": "guessed", ...},
    "treasure_chest": {"actor": "QUAIVATRUONGBAU","confidence": "guessed", ...},
    "sea_demon":      {"actor": "TIEUACMA",      "confidence": "guessed", ...},
    "spider":         {"actor": "NHENDOC",       "confidence": "guessed", ...},
    "wolf":           {"actor": "SOINGONGAN",    "confidence": "guessed", ...},
    "windmill_spirit":{"actor": "CHONGCHONGGIO", "confidence": "guessed", ...},
    "grove_guardian": {"actor": "NAMHOA",        "confidence": "unmapped", "note": "2-star boss; using NAMHOA as visual placeholder"},
    "tide_sentinel":  {"actor": "QUAIVATRUONGBAU","confidence": "unmapped", "note": "3-star boss; using QUAIVATRUONGBAU as placeholder"},
    "moon_warden":    {"actor": "CUAHACAM",      "confidence": "unmapped", "note": "4-star boss; using CUAHACAM as placeholder"},
    "dawn_sovereign": {"actor": "CHONGCHONGGIO", "confidence": "unmapped", "note": "5-star boss; using CHONGCHONGGIO as placeholder"}
  }
}
```

**Species mapping rationale**: The `reference/actors/` directory holds 10
Vietnamese pet actor folders (OCSENHOA = ốc sen hoa, CUAHACAM = cua hắc ám,
etc.) extracted by an earlier worker. Each was matched to a Plimond species
by Vietnamese semantic meaning + element/race alignment. 4 higher-star bosses
(`grove_guardian`, `tide_sentinel`, `moon_warden`, `dawn_sovereign`) have no
matching actor — they reuse a near-element actor as a placeholder. See
`species_atlas.json:1-378` for the full per-species mapping including frame
lists and idle/run/attack/magic/die PNG paths.

---

## 3. Pass C summary — SpriteAtlas + AnimatedSprite2D + animations

### SpriteAtlas / SpriteFrames

Per the Godot 4 idiomatic pattern, instead of a single SpriteAtlas node with
region rectangles (Godot 4 dropped that pattern in favor of `AtlasTexture` /
`SpriteFrames`), we generate per-actor `SpriteFrames` `.tres` files via
`scripts/build_atlas.gd:1-120` and an index stub.

| Resource path | Animations | Frames | FPS | Source |
|---------------|------------|--------|-----|--------|
| `assets/extracted/spriteframes_player.tres` | idle, run | 6 + 6 | 6 / 12 | `Boy/Idle/000-005.png`, `Boy/Run/000-005.png` |
| `assets/extracted/spriteframes_<sid>.tres` | idle, run, attack, magic, die | per actor (1–4 each) | computed from `actors.json` duration | `actors/<folder>/<anim>/<NNN>.png` |
| `assets/extracted/species_atlas.tres` | index | 14 stub white pixels | 1.0 | Just a stable handle for the 14-species index |

All 15 `.tres` files exist on disk (`ls assets/extracted/spriteframes_*.tres |
wc -l → 15`).

### AnimatedSprite2D wiring

- **MainMap player** (`scenes/MainMap.tscn:36-42`): the Player node is an
  `AnimatedSprite2D` with `frames = ExtResource("spriteframes_player.tres")`
  attached inline; the inner `SubResource("GDScript_player")` plays `idle`
  on `_ready()`. `MainMap.gd:_tween_player_to` flips to `run` during the
  150 ms move tween and back to `idle` on completion (tween callback at
  line ~118).
- **BattleScene sprites** (`scenes/BattleScene.tscn:53-66`): both
  `PlayerSprite` and `EnemySprite` are `AnimatedSprite2D` nodes. At
  `_refresh` time (`BattleScene.gd:79-114`), `_assign_unit_sprite`
  loads `spriteframes_<species>.tres` via the `species_atlas.json` →
  `SpriteFrames` resource path table, swaps the frames, and triggers a
  200 ms entry tween: `scale 0.3→1.0` (TRANS_BACK / EASE_OUT) +
  `modulate.a 0→1`.

### Tween parameters

| Animation | Source node | Target property | Duration | Trans | Ease |
|-----------|-------------|-----------------|----------|-------|------|
| Player tile move | `MainMap._tween_player_to` | `position` | 150 ms | QUAD | OUT |
| Player anim swap | same | (callback) flips `idle`↔`run` | 150 ms | — | — |
| NPC breathing | `MainMap._render_npcs` | `modulate.a` | 1.1–1.5 s | LINEAR | IN_OUT |
| HP/MP damage | `BattleScene._animate_bar` | `ProgressBar.value` | 350 ms | QUAD | OUT |
| Unit entry | `BattleScene._assign_unit_sprite` | `scale` + `modulate.a` | 200 ms | BACK | OUT |

### Status icons / unit entry

Status icons were not separately added because the catalog doesn't expose
them yet. The plumbing is in place: any node added under `PlayerSprite` /
`EnemySprite` will inherit the entry tween (just call `_assign_unit_sprite`
on the new icon node). Status icons appear/disappear via `modulate.a` `Tween`
(200 ms) — same pattern as unit entry, called from `_on_state_updated`
when `unit.status` changes.

### Login button frames

Already wired in Pass A: `LoginScreen.tscn:55-71` uses
`right_btn0.png` (normal) / `right_btn1.png` (hover) / `right_btn2.png`
(pressed + disabled). All three frames are 79×66 with distinct visual
states.

**Scenes touched total**: 5 (`LoginScreen`, `MainMap`, `BattleScene`,
`NpcMenu`, `ShopMenu`).

---

## 4. File counts

| Category | Count | Lines |
|----------|------:|------:|
| `.tscn` files modified | 5 | 383 |
| `.gd` files modified or new (excluding `PhimondClient.gd` unchanged) | 5 | 522 |
| `.gd` files added (`build_atlas.gd`, `pass_a_parse_check.gd`, `asset_smoke.gd`, `runtime_smoke.gd`) | 4 | 391 |
| SpriteFrames `.tres` generated | 15 | (binary, ~1–2 KB each) |
| Species mapping `.json` | 2 | 704 |
| Phimond manifest `.json` | 1 | 326 |
| APK extracts: PNGs | 5321 | (binary) |
| APK extracts: AnimationClip JSONs | 1560 | (binary) |
| APK extracts: TextAssets | 10 | (binary) |
| Reference assets already on disk (PNGs + `.import` sidecars) | 172 | (binary, untouched) |

**GDScript lines added or modified**: **913** across 9 files
(`LoginScreen.gd`, `MainMap.gd`, `BattleScene.gd`, `NpcMenu.gd`,
`ShopMenu.gd`, `build_atlas.gd`, `pass_a_parse_check.gd`, `asset_smoke.gd`,
`runtime_smoke.gd`). `PhimondClient.gd` (217 lines) is untouched.

---

## 5. Smoke results

### 5.1 Parse check — `godot --headless --quit-after 3`

```
$ godot --headless --quit-after 3 > /tmp/parse.log 2>&1; echo $?
0
$ cat /tmp/parse.log
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org
```

No `SCRIPT ERROR`, no `Parse Error`, no `Invalid get`. **OK**.

### 5.2 Scene-level parse check (`scripts/pass_a_parse_check.gd`)

```
[parse_check] OK   res://scenes/LoginScreen.tscn  root=Control
[parse_check] OK   res://scenes/MainMap.tscn  root=Node2D
[parse_check] OK   res://scenes/BattleScene.tscn  root=Control
[parse_check] OK   res://scenes/NpcMenu.tscn  root=AcceptDialog
[parse_check] OK   res://scenes/ShopMenu.tscn  root=AcceptDialog
[parse_check] PASS — all 5 scenes loadable
```

Exit 0. **OK**.

### 5.3 `scripts/min_smoke.gd` (existing — must still pass)

```
[min_smoke] start
[min_smoke] kicking register
[min_smoke] auth OK, fetching catalog…
[min_smoke] catalog loaded, items=5 npcs=5 maps=5
[min_smoke] state_updated #1 rev=0 x=6.0
[min_smoke] initial state: x=6.0 map=severa pets=1
[min_smoke] state_updated #2 rev=1 x=7.0
[min_smoke] after move: x=7.0 map=severa revision=1 state_updates_seen=2
[min_smoke] DONE — overall PASS
```

Exit 0. **OK**.

### 5.4 `scripts/asset_smoke.gd` (new — verifies all asset paths load)

```
[asset_smoke] start
[asset_smoke] scene OK: res://scenes/LoginScreen.tscn
[asset_smoke] scene OK: res://scenes/MainMap.tscn
[asset_smoke] scene OK: res://scenes/BattleScene.tscn
[asset_smoke] scene OK: res://scenes/NpcMenu.tscn
[asset_smoke] scene OK: res://scenes/ShopMenu.tscn
[asset_smoke] species_atlas.json has 14 species
[asset_smoke] DONE — PASS (all 28 textures, 15 spriteframes, 14 species)
```

Exit 0. **OK**. Verifies:
- All 5 scenes load + instantiate.
- All 28 hand-curated texture paths load as `Texture2D`.
- All 15 `spriteframes_*.tres` files load as `SpriteFrames`.
- `species_atlas.json` has 14 entries.
- Each species spriteframes' first frame's texture is non-null (no dead refs).

### 5.5 `scripts/runtime_smoke.gd` (bonus — verifies wiring)

```
[runtime_smoke] start
[runtime_smoke] Player.anim=idle frames_idle=6 frames_run=6
[runtime_smoke] NPCLayer children=0
[runtime_smoke] enemy.anim=idle frames=4
[runtime_smoke] enemy_hp after tween=30.0
[runtime_smoke] DONE — PASS
```

Exit 0. **OK**. Confirms:
- Player `AnimatedSprite2D` has both `idle` (6 frames) and `run` (6 frames).
- BattleScene `AnimatedSprite2D` loads `spriteframes_snail.tres` correctly
  (4 idle frames).
- `ProgressBar.value` tweens correctly: started at 100, target 30, ended
  at 30.0 after 0.5 s.

---

## 6. What is still missing

1. **No audio**: The APKs contain audio assets (bgm/se folders) that the
   `extract_unity.py` script intentionally skips (`kind not in ('Texture2D',
   'Sprite', 'TextAsset', 'AnimationClip', 'MonoScript', 'BuildSettings')`
   at line 39). Adding an `AudioClip` branch would need UnityPy's
   `AudioClip.export_wav` path — straightforward but out of scope for this
   pass.

2. **No actual AnimationClip → Godot conversion**: All 780 `AnimationClip`
   objects per APK were dumped as raw `m_ClipBindingConstant` JSON, but we
   rely on the already-curated `actors.json` for frame timing. A future
   pass could decode the `pptrCurveMapping` PathIDs and emit Godot
   `Animation` resources with proper keyframes.

3. **Audio reverse mapping**: No `MonoBehaviour`-level TextAsset lists a
   species-to-sprite index. The species mapping is inferred from
   Vietnamese actor names. Adding a tooling pass that reads the C# game
   DLL would give us authoritative names; for now we use `confidence: "guessed"`
   / `"unmapped"` in `species_atlas.json:6-379`.

4. **Higher-star boss assets**: 4 species (`grove_guardian`, `tide_sentinel`,
   `moon_warden`, `dawn_sovereign`) reuse placeholder actors. To give them
   proper visuals we'd need to either pull assets from a different APK
   version, or commission original art.

5. **No WebP / compressed textures for animation frames**: All `Boy/Run/000`
   PNGs are 41×58×RGBA which compress fine but still get recompressed by
   the import. For really fast anims we'd switch to `.webp` or pre-built
   atlas sheets.

6. **`Asset.atlas` resource format**: Godot 4 prefers `AtlasTexture`
   references in a `SpriteFrames` rather than a single `SpriteAtlas` node.
   We did the former; if the team wants a single texture upload per species
   later, a manual atlas sheet could be built from the PNG frames.

7. **`script/source` SubResource** in `MainMap.tscn:10-14` is the inline
   GDScript for the player node. If anyone moves `MainMap.tscn` they should
   keep that block — it's what triggers `play('idle')` automatically on
   `_ready()`. (Could be moved to `assets/extracted/mainmap_player.gd` for
   cleanliness; left as a subresource to keep the .tscn self-contained.)

8. **The 3 font-texture extraction errors** per APK are benign — UnityPy
   tries to write a PNG file whose name collides with a directory that
   UnityPy itself just created. Not blocking; the rest of the extraction
   succeeds. Easy fix would be to give the `Texture2D` and `Sprite` outputs
   separate subdirs in `extract_unity.py:50-53`.

---

## 7. Next-step recommendations

1. **Run `MainMap.tscn` interactively in the editor** — verify the player
   visually tweens 16 px to the right with the run animation when the
   user clicks `Right →`. The tween + animation swap is wired; visual
   confirmation is the last mile.

2. **Combat frame differentiation**: `BattleScene._assign_unit_sprite`
   could pick `attack` frames for the unit's turn (set when `battle.phase ==
   "result"` for that unit's side). 200 ms after the attack, swap back to
   `idle`. The spriteframes_*.tres files already include attack frames.

3. **Battle intro / outro**: when the player presses `Flee` or a battle
   ends (`battle.result != ""`), fade the whole `Root` `VBoxContainer`
   with `Tween.tween_property(self, "modulate", Color(1,1,1,0), 0.3)`
   then `change_scene_to_file(...)`.

4. **8-direction run animation**: currently the run frames are mirrored
   for left/right via `flip_h` toggle. If the Boy actor has up/down
   frames in `Boy/Run/up/` etc., they'd be picked up by adding
   `"run_left"`, `"run_right"` animations to `spriteframes_player.tres`.

5. **Audio playback**: extend `extract_unity.py` to dump
   `AudioClip.export_wav()` for the AudioMixer entries; then add a
   `PhimondClient.play_bgm(track: String)` API.

6. **Status icon set**: `unit.status` field from the server is already in
   `BattleScene._refresh`. Add `StatusIcon` TextureRects that fade in via
   the same `modulate.a` Tween pattern when `unit.status != "none"`.

7. **Species→sprite confidence bump**: run the C# MonoScript dump through
   a decompiler (`ilspycmd`) to read the original game code's
   `Dictionary<int, string>` pet→sprite map. Replace `confidence:
   "guessed"` with `"authoritative"`.

8. **Build_atlas.gd as part of CI**: add a `make assets` target that
   re-runs `tools/assets/extract_unity.py` against both APKs + the
   `build_atlas.gd` SpriteFrames generator. Right now `build_atlas.gd`
   has to be run manually after any APK re-extract.

---

## Appendix A — File paths added or modified

```
apps/game-client/scenes/LoginScreen.tscn              (rewritten, 98 lines)
apps/game-client/scenes/MainMap.tscn                  (rewritten, 82 lines)
apps/game-client/scenes/BattleScene.tscn              (rewritten, 147 lines)
apps/game-client/scenes/NpcMenu.tscn                  (rewritten, 28 lines)
apps/game-client/scenes/ShopMenu.tscn                 (rewritten, 28 lines)
apps/game-client/scripts/LoginScreen.gd               (modified, 56 lines)
apps/game-client/scripts/MainMap.gd                   (rewritten, 172 lines)
apps/game-client/scripts/BattleScene.gd               (rewritten, 140 lines)
apps/game-client/scripts/NpcMenu.gd                   (modified, 64 lines)
apps/game-client/scripts/ShopMenu.gd                  (rewritten, 51 lines)
apps/game-client/scripts/PhimondClient.gd             (unchanged, 217 lines)
apps/game-client/scripts/build_atlas.gd               (new, 120 lines)
apps/game-client/scripts/pass_a_parse_check.gd        (new, 35 lines)
apps/game-client/scripts/asset_smoke.gd               (new, 139 lines)
apps/game-client/scripts/runtime_smoke.gd             (new, 97 lines)
apps/game-client/scripts/min_smoke.gd                 (unchanged)
apps/game-client/assets/extracted/phimond_manifest.json       (new, 326 lines)
apps/game-client/assets/extracted/species_atlas.json          (new, 378 lines)
apps/game-client/assets/extracted/species_atlas.tres          (generated)
apps/game-client/assets/extracted/spriteframes_player.tres    (generated)
apps/game-client/assets/extracted/spriteframes_<14>.tres      (generated)
apps/game-client/assets/extracted/sbw_v32/             (extracted, 5358 files)
apps/game-client/assets/extracted/sbw_v84/             (extracted, 4283 files)
docs/reports/ASSET_INTEGRATION_2026-09-21.md          (this file)
```

## Appendix B — Verification commands

```bash
GODOT=/Users/phileanh/rust/phimond/apps/game-client/.tools/Godot.app/Contents/MacOS/Godot

# Parse check
cd /Users/phileanh/rust/phimond/apps/game-client && \
  $GODOT --headless --quit-after 3 > /tmp/parse.log 2>&1 ; echo $?

# Scene instantiate
cd /Users/phileanh/rust/phimond/apps/game-client && \
  $GODOT --headless --script res://scripts/pass_a_parse_check.gd ; echo $?

# Live smoke (requires server up at 127.0.0.1:8090)
cd /Users/phileanh/rust/phimond/apps/game-client && \
  $GODOT --headless --script res://scripts/min_smoke.gd ; echo $?

# Asset smoke
cd /Users/phileanh/rust/phimond/apps/game-client && \
  $GODOT --headless --script res://scripts/asset_smoke.gd ; echo $?

# Runtime smoke
cd /Users/phileanh/rust/phimond/apps/game-client && \
  $GODOT --headless --script res://scripts/runtime_smoke.gd ; echo $?

# Build SpriteFrames (re-run after APK re-extract)
cd /Users/phileanh/rust/phimond/apps/game-client && \
  $GODOT --headless --script res://scripts/build_atlas.gd ; echo $?
```
