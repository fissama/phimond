# UI Foundation Report — 2026-09-22

**Worker:** UI Foundation worker
**Scope:** Fantasy GameTheme + reusable StyleBox / Window / Button / Tab / Slot
components for `apps/game-client`.
**Backend touched:** none (presentation-only).

---

## Result

Foundation delivered. The project compiles and parses cleanly (`godot --headless --quit-after 1` exits 0). All 8 reusable components parse as `PackedScene` and instantiate under the new `GameTheme.tres`. A `test_theme.tscn` exercises every component with sample data and runs without errors.

```
[parse_check] PASS — all 5 scenes loadable   (existing scenes still load)
godot --headless --quit-after 1 --scene res://scenes/test_theme.tscn → exit 0
```

---

## Files created

| Path | Purpose |
|------|---------|
| `apps/game-client/styles/GameTheme.tres` | Project default Theme (17 control types overridden) |
| `apps/game-client/styles/styleboxes/panel_9slice.tres` | Reusable 9-slice panel frame (48×48 px texture, 16-px margins) |
| `apps/game-client/styles/styleboxes/lineedit_frame.tres` | Fantasy input frame (32×16 texture, 2-px margins) |
| `apps/game-client/styles/styleboxes/button_normal.tres` | Button normal: blue body + gold rim |
| `apps/game-client/styles/styleboxes/button_hover.tres` | Button hover: cream body + gold rim |
| `apps/game-client/styles/styleboxes/button_pressed.tres` | Button pressed: brown body + gold rim |
| `apps/game-client/styles/styleboxes/button_disabled.tres` | Button disabled: gray body, modulate 50 % |
| `apps/game-client/styles/styleboxes/tab_selected.tres` | Tab active: light blue body + gold rim |
| `apps/game-client/styles/styleboxes/tab_unselected.tres` | Tab inactive: dark blue body + gold rim |
| `apps/game-client/styles/styleboxes/progress_bg.tres` | ProgressBar background (dark) |
| `apps/game-client/styles/styleboxes/progress_fg.tres` | ProgressBar fill (red, mutable per-instance) |
| `apps/game-client/styles/styleboxes/chat_panel.tres` | Chat panel — translucent dark blue |
| `apps/game-client/styles/styleboxes/top_hud.tres` | Top status bar — dark blue + gold accent |
| `apps/game-client/styles/styleboxes/_extract.py` | Asset-extraction helper (kept for re-runs) |
| `apps/game-client/styles/styleboxes/panel_9slice.png` | 9-slice texture source (48×48) |
| `apps/game-client/styles/styleboxes/lineedit_frame.png` | Input frame texture source (32×16) |
| `apps/game-client/styles/styleboxes/{button_normal,button_hover,button_pressed,button_disabled}.png` | Button tile sources (24×24) |
| `apps/game-client/styles/styleboxes/{tab_selected,tab_unselected}.png` | Tab tile sources (24×24) |
| `apps/game-client/styles/styleboxes/{progress_bg,progress_fg}.png` | Progress tile sources (32×12) |
| `apps/game-client/styles/styleboxes/{chat_panel,top_hud,panel_inner_fill}.png` | Misc panel sources |
| `apps/game-client/styles/styleboxes/{button_tl,button_tr,button_bl,button_br}.png` | Reserved raw button corner slices from `right_btn0.png` (kept for future use; visually transparent because `right_btn0` is round) |
| `apps/game-client/scenes/components/GameWindow.tscn` | Reusable fantasy window scene |
| `apps/game-client/scenes/components/GameButton.tscn` | Reusable button scene |
| `apps/game-client/scenes/components/GameTab.tscn` | Reusable tab scene |
| `apps/game-client/scenes/components/GameSlot.tscn` | Reusable 32×32 inventory slot |
| `apps/game-client/scenes/components/GameTextInput.tscn` | Reusable LineEdit scene |
| `apps/game-client/scenes/components/GameDialog.tscn` | Reusable confirm-dialog scene |
| `apps/game-client/scenes/components/GameHPBar.tscn` | Reusable HP bar scene |
| `apps/game-client/scenes/components/GameMPBar.tscn` | Reusable MP bar scene |
| `apps/game-client/scripts/components/GameWindow.gd` | GameWindow script (class_name GameWindow) |
| `apps/game-client/scripts/components/GameButton.gd` | GameButton script (class_name GameButton) |
| `apps/game-client/scripts/components/GameTab.gd` | GameTab script (class_name GameTab) |
| `apps/game-client/scripts/components/GameSlot.gd` | GameSlot script (class_name GameSlot) |
| `apps/game-client/scripts/components/GameTextInput.gd` | GameTextInput script (class_name GameTextInput) |
| `apps/game-client/scripts/components/GameDialog.gd` | GameDialog script (class_name GameDialog) |
| `apps/game-client/scripts/components/GameHPBar.gd` | GameHPBar script (class_name GameHPBar) |
| `apps/game-client/scripts/components/GameMPBar.gd` | GameMPBar script (class_name GameMPBar) |
| `apps/game-client/scripts/build_game_theme.gd` | Theme rebuilder (run once; idempotent) |
| `apps/game-client/scripts/test_theme.gd` | test_theme.tscn controller script |
| `apps/game-client/scenes/test_theme.tscn` | Verification scene: GameWindow + 2 buttons + 2 tabs + 4 slots + TextInput + HPBar + MPBar + plain Label/Button |

### Files modified

| Path | Change |
|------|--------|
| `apps/game-client/project.godot` | Added `[gui] theme/custom="res://styles/GameTheme.tres"` so all controls use the fantasy theme by default. No other settings touched. |

---

## 1. Theme file structure

`styles/GameTheme.tres` is a Godot `Theme` resource built from the 12 styleboxes and several color / font overrides. The full key list (44 entries) covers:

```
default_font_size = 14
default_base_scale = 1.0

AcceptDialog/styles/panel              = panel_9slice
Button/styles/normal/hover/pressed/focus/disabled
Button/colors/font_color              = warm white (0.95, 0.93, 0.88)
Button/colors/font_hover_color        = bright gold (1.00, 0.85, 0.55)
Button/colors/font_pressed_color      = dim gold (0.55, 0.45, 0.28)
Button/colors/font_disabled_color     = gray
Button/font_sizes/font_size           = 14
CheckBox/CheckButton/colors/…         = same color palette as Button
ConfirmationDialog/styles/panel       = panel_9slice
HScrollBar/VScrollBar/styles/scroll/grabber/grabber_highlight/grabber_pressed
Label/colors/font_color               = warm gold (0.78, 0.69, 0.47)
Label/colors/font_shadow_color        = black 60%
Label/constants/shadow_offset_{x,y}   = 1, 1
Label/font_sizes/font_size            = 14
LineEdit/colors/caret_color           = bright gold (1.00, 0.85, 0.40)
LineEdit/colors/font_color            = warm white
LineEdit/colors/font_placeholder_color = dim gray
LineEdit/colors/selection_color       = gold 40 %
LineEdit/colors/font_selected_color   = warm gold
LineEdit/constants/caret_width        = 2
LineEdit/styles/normal/focus/read_only = lineedit_frame
LineEdit/font_sizes/font_size         = 14
MenuBar/styles/normal/hover/pressed   = button tiles
OptionButton/styles/… + arrow_color   = gold
Panel/styles/panel                    = panel_9slice
PanelContainer/styles/panel           = panel_9slice
PopupMenu/styles/panel/hover/separator
ProgressBar/styles/background/fill    = progress_bg/fg
RichTextLabel/colors/default_color    = warm gold
RichTextLabel/colors/font_outline_color / font_shadow_color
ScrollContainer/styles/bg/panel       = panel_9slice
SpinBox/styles/normal                 = lineedit_frame
SpinBox/colors/caret_color            = bright gold
TabContainer/styles/tab_selected/tab_unselected/tab_*_close/panel
TabContainer/colors/font_selected_color = bright gold
TabContainer/colors/font_unselected_color = warm gold
TextureButton/colors/font_color/…     = same as Button
Tree/styles/panel/bg/selected/selected_focus/cursor
Tree/colors/font_color/font_selected_color/guide_color/title_button_color
VScrollBar/styles/grabber/…           = button tiles
Window/styles/embedded_border/embedded_unfocused_border
Window/colors/title_color             = warm gold
Window/constants/title_height         = 28
```

Generated by `scripts/build_game_theme.gd` (re-runnable). The theme **completely
overrides** Godot's default light-grey chrome; any control added without further
styling automatically looks fantasy.

---

## 2. StyleBoxes created

12 `.tres` resources in `styles/styleboxes/`. Each is a `StyleBoxTexture` pointing at a small PNG with calibrated `texture_margin_*` for 9-slice scaling.

| StyleBox | PNG size | Margins (L,T,R,B) | Source |
|----------|----------|-------------------|--------|
| `panel_9slice` | 48×48 (3×3 of 16×16) | 16, 16, 16, 16 | Synthesised (gold L-rim, dark-blue interior) |
| `lineedit_frame` | 32×16 | 2, 2, 2, 2 | Synthesised (gold top/bottom rim, dark interior) |
| `button_normal` | 24×24 | 4, 4, 4, 4 | Synthesised (blue body, gold rim) |
| `button_hover` | 24×24 | 4, 4, 4, 4 | Synthesised (cream body, gold rim) |
| `button_pressed` | 24×24 | 4, 4, 4, 4 | Synthesised (brown body, gold rim) |
| `button_disabled` | 24×24 | 4, 4, 4, 4 | Synthesised (gray body, modulate 50 %) |
| `tab_selected` | 24×24 | 4, 4, 4, 4 | Synthesised (light blue + gold rim) |
| `tab_unselected` | 24×24 | 4, 4, 4, 4 | Synthesised (dark blue + gold rim) |
| `progress_bg` | 32×12 | 2, 2, 2, 2 | Synthesised (dark) |
| `progress_fg` | 32×12 | 2, 2, 2, 2 | Synthesised (red; mutable per-instance via `set_bar_tint`) |
| `chat_panel` | 64×32 | 4, 4, 4, 4 | Synthesised (translucent dark blue) |
| `top_hud` | 128×16 | 4, 2, 4, 2 | Synthesised (dark blue + gold top accent) |

### Why synthesised, not extracted

A first pass extracted sub-regions from `assets/reference/ui/UI.png` using
Pillow. The result was visually asymmetric because `UI.png` (520×320) has its
inner content (username / password / buttons) **baked into the center** — only
the very outer rim is reusable. The 9-slice extracted from the source turned
out to be mostly transparent on the left and bottom-left corners.

I rewrote the extractor to produce a **clean, symmetric 9-slice** using the
palette already in `UI.png` (gold band #958C51, dark-blue interior #08345D,
dark-blue shadow #001620). All 9 patches are non-transparent, tile cleanly, and
match the fantasy theme the rest of `UI.png` evokes.

The original extraction helpers (`scripts/build_game_theme.gd` `_extract.py`)
and the round-corner slices from `right_btn0.png` (`button_tl/tr/bl/br.png`)
are kept on disk so a parallel asset-extraction worker can refine them when
richer artwork lands in `apps/game-client/assets/extracted/extended/`.

---

## 3. Reusable components and methods

All scripts are in `scripts/components/` with `class_name Foo` and matching `.tscn` files in `scenes/components/`.

### GameWindow (`Control`, root of the fantasy window)

```
signal close_requested
signal drag_started
signal drag_ended

set_title(text: String)
set_close_callback(callable: Callable)
set_size_px(w: float, h: float)
get_body() -> MarginContainer       # body container; child your content here
```

Internally: `NinePatchRect` (panel_9slice) + `PanelContainer` (title bar) +
`MarginContainer` (body). Title bar responds to left-mouse drag — moving the
window. Close button is a `Button` that emits `close_requested`.

### GameButton (`TextureButton`)

```
set_label(text: String)
set_icon(path: String)        # path; empty string hides
set_icon_texture(tex: Texture2D)
connect_pressed(callable: Callable)
```

Internal layout: `TextureRect Icon` (32×32, hidden by default) + `Label` (full
rect, anchored 15). The base texture is `right_btn0.png` (normal) and
`right_btn1.png` (hover); these can be overridden per-instance.

### GameTab (`Button`)

```
set_selected(value: bool)
is_selected() -> bool
set_text_label(text: String)
```

Toggling `_selected` swaps the `normal`/`focus` stylebox between
`tab_selected.tres` and `tab_unselected.tres`, and dims modulate when inactive.

### GameSlot (`PanelContainer`, 32×32 default)

```
signal slot_clicked

set_item(icon_path: String, qty: int = 0)   # qty shown when > 1
set_item_texture(tex: Texture2D, qty: int = 0)
clear()
set_click_callback(callable: Callable)
```

Internal: `MarginContainer` (2-px padding) → `TextureRect Icon` + `Label Qty`.
Click is detected via `gui_input` because `PanelContainer` lacks a `pressed`
signal.

### GameTextInput (`LineEdit`)

```
signal input_submitted(text: String)

set_text_value(text: String)
set_placeholder_value(text: String)
focus_input()
```

Theme already applied via project theme. The `input_submitted` signal mirrors
Godot's `text_submitted` with a friendlier name.

### GameDialog (`AcceptDialog`)

```
signal dialog_confirmed
signal dialog_canceled

set_title_text(text: String)
set_body_text(text: String)
set_ok_text(text: String)
show_confirm(title_text, body, on_ok = Callable(), on_cancel = Callable())
```

Internal layout: `PanelContainer` → `VBoxContainer` → `BodyLabel`. Title and
OK text are forwarded to the inherited AcceptDialog API; cancel is detected
via the inherited `close_requested` signal.

### GameHPBar (`ProgressBar`)

```
tween_value(target: float, duration_ms: int = 250)  # quad-out, default 250 ms
set_value_instant(target: float)
update_max(new_max: float, keep_ratio: bool = true)
set_bar_tint(color: Color)
```

The default tint is red (0.70, 0.18, 0.18) and is applied by duplicating the
`fill` StyleBoxTexture at runtime so the theme resource is left untouched for
other HP/MP/exp bars to share.

### GameMPBar (`ProgressBar`)

Identical API to `GameHPBar`; default tint is blue (0.22, 0.45, 0.85).

---

## 4. Project wiring

`apps/game-client/project.godot` gained a single new section:

```ini
[gui]

theme/custom="res://styles/GameTheme.tres"
```

No other project settings touched. After the change the project parses
cleanly:

```
$ godot --headless --quit-after 1
Godot Engine v4.7.2.stable.official.ed1daf0bf - https://godotengine.org
$ echo $?
0
```

---

## 5. Parse-test output

Run from `/Users/phileanh/rust/phimond/apps/game-client`:

| Test | Command | Result |
|------|---------|--------|
| Project parse | `godot --headless --quit-after 1` | exit 0 |
| Existing 5 scenes parse (regression) | `godot --headless --quit-after 1 --script scripts/pass_a_parse_check.gd` | `[parse_check] PASS — all 5 scenes loadable` |
| All 12 StyleBoxes load | inline Resource check | 12 / 12 OK |
| All 8 components parse + instantiate | inline PackedScene loop | 8 / 8 OK |
| `test_theme.tscn` parses | `godot --headless --quit-after 1 --scene res://scenes/test_theme.tscn` | exit 0 |
| Theme rebuilder is idempotent | `godot --headless --quit-after 1 --script scripts/build_game_theme.gd` | `[build_game_theme] wrote res://styles/GameTheme.tres` |

Pre-existing failure (not caused by this work): `scripts/BattleScene.gd`
calls `remove_child` synchronously inside `_refresh`, producing a "Parent is
busy" runtime error. Verified that the same error appears without the new
`[gui]` block, so it is independent of the theme.

### Component smoke test (executed + removed)

I ran an async smoke (`scripts/_smoke_components.gd`) that instantiated
`test_theme.tscn`, exercised every public method (set_title, get_body,
set_label, set_selected, set_item, set_placeholder_value, set_text_value,
set_value_instant, update_max), and confirmed each returns the expected
state. All 14 checks green. The script was deleted after verification — only
`build_game_theme.gd` (re-run-on-demand) and `test_theme.gd` (test scene
controller) remain.

---

## 6. Screenshots / expected behaviour

This run was headless; capturing a real PNG would require a working
`--display-driver macos` (MoltenVK crashes the GL Compatibility renderer on
this machine — see `--write-movie /tmp/movie.avi` abort). Visual inspection
must happen on a workstation, but the deterministic state below describes
what each component renders when displayed.

### `test_theme.tscn` (1152×768 layout)

- **Bg**: Solid dark-blue (`Color(0.04, 0.08, 0.12)`) covers the full window
  (mimics night sky / loading-screen background).
- **Title** (top-left): gold-colored "Phimond — Theme + Components Test"
  with 1-px black shadow.
- **Window** (left, 32..432 × 56..376): gold-rimmed dark-blue frame, title
  "Inventory", close "X" button on the right of the title bar. Empty 12-px
  inner margin ready for child content. Drag the title bar to move.
- **ButtonsRow** (32..600 × 392..448): two side-by-side TextureButtons with
  the cyan `right_btn0.png` frame and overlaid "Use" / "Drop" labels
  (warm-white text). Hover swaps to the cream `right_btn1.png` frame; press
  darkens to gold-brown.
- **TabsRow** (32..600 × 460..500): two GameTab instances with "Bags" /
  "Equip" labels. "Bags" is selected (light-blue + gold rim, full opacity);
  "Equip" is unselected (dark-blue + gold rim, 0.85 modulate).
- **SlotsRow** (32..600 × 512..552): four 32×32 GameSlot panels with the
  LineEdit-style frame:
  - Slot 1: empty (just the frame).
  - Slot 2: a cyan button texture, no quantity.
  - Slot 3: a Boy Idle frame, "12" in bottom-right corner (cream text).
  - Slot 4: a Boy Run frame, "99" in bottom-right.
- **SidePanel** (VBoxContainer, 460..928 × 56..600):
  - TextInput (full width, 32 px tall) — fantasy LineEdit; placeholder
    "Search items…" in dim gray; gold caret 2 px wide; gold selection.
  - HPBar — 75 % filled with a red bar (GameHPBar.set_value_instant(75)).
  - MPBar — 40 % filled with a blue bar.
  - PlainLabel — gold text "Default Label (gold text from theme)".
  - PlainButton — default-styled `Button` (no per-instance overrides);
    uses the Button styleboxes from the theme. Label "Plain Button
    (theme-driven)".
- **StatusLabel** (bottom, full width): gold text "test_theme.tscn loaded —
  all components instantiated" set by `test_theme.gd::_ready()`.

### Behavioural expectations for downstream screens

- **LoginScreen** will keep working: the existing per-instance texture buttons
  use `right_btn0/1/2.png` directly; theme only affects unstyled controls
  (Label, LineEdit, plain Button).
- **MainMap**, **BattleScene**, **NpcMenu**, **ShopMenu**: each scene's
  existing `Control` root inherits the new theme automatically. Their
  per-instance `texture_normal/hover/pressed` overrides on TextureButtons win
  over the theme.
- All four control types (Label, Button, LineEdit, ProgressBar) that the
  in-progress per-screen reconstruction workers need to style already have
  full theme overrides ready.
- Drag-to-move on GameWindow is bound to left-mouse on the title bar only;
  the body remains a normal container.
- HP/MP bar tweens use `Tween.TRANS_QUAD | Tween.EASE_OUT` so a 250 ms call
  feels snappy without being twitchy.

---

## 7. Known constraints / handoff notes

- Asset-extraction worker can drop richer 9-slice textures into
  `styles/styleboxes/panel_9slice.png` (and friends). The `.tres` margins are
  fixed at 16/16/16/16 for the panel; richer art can keep those margins
  unchanged.
- `GameTab` is designed for use inside a `TabContainer`, but currently it
  does **not** integrate with TabContainer's auto-managed `tab_changed`
  signal. If you want it to plug in as a real tab content switcher, the
  per-screen worker should call `tab.set_selected(true)` and
  `siblings.set_selected(false)` manually when wiring tabs.
- `GameDialog` wraps `AcceptDialog`; for full OK/Cancel flow with custom
  button text, call `add_cancel_button("Cancel")` (provided by
  `GameDialog.add_cancel_button`) and connect its `pressed` to
  `dialog_canceled`.
- All component scripts use `class_name`, so per-screen workers can
  `preload("res://scripts/components/GameWindow.gd")` and instantiate the
  class directly instead of going through `PackedScene` if they prefer.

## 8. Validation run

```
$ godot --headless --quit-after 1                                          → exit 0
$ godot --headless --quit-after 1 --script scripts/pass_a_parse_check.gd    → PASS
$ godot --headless --quit-after 1 --scene res://scenes/test_theme.tscn     → exit 0
$ godot --headless --quit-after 1 --script scripts/build_game_theme.gd      → OK
```

## 9. Assumptions

- The fantasy palette (warm gold #C7B377 / dim gold / dark-blue interior
  #08345D) matches the visual intent of `UI.png`. If a brand asset-extraction
  worker supplies a refined palette later, the same `GameTheme.tres` can be
  re-generated from `build_game_theme.gd` after updating the color literals.
- The 16-px 9-slice margin is sufficient for the default UI sizing
  (window ≥ 320×200, button ≥ 120×48). Smaller sizes would clip the corner
  decorations; per-screen callers should clamp `custom_minimum_size`.
- Existing scenes were left untouched as instructed. Their pre-existing
  per-instance texture overrides (e.g. `right_btn0.png` on TextureButtons in
  `LoginScreen.tscn`) continue to take precedence over the new theme.

## 10. Blockers / remaining risks

- None functional. The only outstanding item is the pre-existing BattleScene
  `remove_child` runtime error, which is a backend scripting bug unrelated
  to this task and not in scope.
- If a future asset-extraction worker lands rich UI bitmaps, they should
  also update `panel_9slice.png`, `lineedit_frame.png`, and the button tiles;
  no script changes will be required because every component reads its
  visual identity from the project's StyleBox resources.