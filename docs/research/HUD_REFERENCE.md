# HUD and battle reference

## Sources and extraction

Reviewed the user-supplied `Spirit Beast World 3.2.apk` (SHA-256 `4585589356c3aaebdf99589f0194d72e74c471cc71425d3b54f7e119437f72ac`) and the supplied `Pokezoo - Huyền thoại một thời.mp4` (1280×720, 273.2 seconds).

`tools/assets/export_hud.py` reproducibly copies 44 reviewed Unity **Sprite** slices into `apps/game-client/assets/reference/hud/`. Run with `rtk proxy tools/.cache/asset-venv/bin/python tools/assets/export_hud.py`. The extractor reads original Sprite metadata from the APK. No screenshots were used as replacement art; no approximate image crops were needed. `hud.json` records each source serialized file/object ID, Unity rectangle (bottom-left origin), border, pivot, extracted filename, dimensions and PNG SHA-256. PNG files retain the extraction's original alpha and polygon mask.

The APK is a version variant of the older video. Specifically, its D-pad is round/diamond shaped with a decorated center, while the video's pad has a thinner cross silhouette. The APK bar chrome is silver; the video uses gold. Do not describe these differing pieces as pixel-identical to the video.

## Asset interface

All aliases below are PNG filenames under `res://assets/reference/hud/`. Full object mapping is in `hud.json`.

| Alias | Source Sprite | Intended usage |
| --- | --- | --- |
| `dpad` | UIall_10 | Four-direction control; 128×124; APK variant |
| `frame_bars` | UIall_4 | Silver stepped status chrome; 139×40 |
| `frame_portrait` | UIall_14 | Two diagonally overlapping gold portrait rings; 66×57 |
| `bar_hp`, `bar_mp` | UIall_8, UIall_1 | Red 106×9 / cyan 103×8 fills |
| `bar_xp`, `bar_green` | UIall_7, UIall_16 | Yellow / green thin fills; semantic assignments beyond color require behavior evidence |
| `button_round`, `button_round_red` | UIall_15, UIall_20 | Blank circular blue/red buttons |
| `button_confirm`, `button_back` | UIall_3 | Same blank diagonal blue oval; labels are separate text |
| `button_accept`, `button_cancel` | DongY, Huy 1 | Circular checkmark / cross buttons |
| `button_menu` | UIall_21 | Wide cyan button, 102×35 |
| `button_side` | UIall_5 | Gold edge toggle, 37×48 |
| `button_orb`, `frame_small` | UIall_12, UIall_13 | Cyan orb and small gold/cyan frame |
| `frame_chat` | chatbg_0 | Cyan 10×85 gradient strip; stretch horizontally; **not** a complete border |
| `panel_controls` | UIall_2 | Gray-to-blue patterned rectangle with gold top edge, 99×90 |
| `panel_ornate` | UIall_9 | Patterned panel with raised ornamental top edge, 150×125 |
| `panel_menu` | UI_0 | Large blue/gold menu with decorated left side, 491×232; visually matches video menu family |
| `row_menu`, `row_selected`, `tab_menu` | tableitem_0, tableitem1_0, tab | Dark row, cyan selected-row highlight, raised tab |
| `slot`, `slot_light` | UIall_19, UIall_18 | Blue / light square slots |
| `ornament_corner` | UIall_0 | Small gold corner flourish |
| `battle_actions` | battlebg_0 | Cyan horizontal oval action platform, 239×44 |
| `icon_auto`, `icon_attack`, `icon_magic`, `icon_inventory`, `icon_run` | Auto_0, Attack_0, Magic_0, Iventory_0, Run_0 | Ice blocks, claw, staff, bag, fleeing pink creature |
| `button_inventory`, `button_pet`, `button_settings` | item, pet, CaiDat | Labeled-by-icon circular shortcut variants |
| `button_quest`, `button_shop`, `button_guild` | NV, shop, Bang | Circular scroll, coins, castle shortcuts |
| `icon_chat` | chat | Yellow speech bubbles |
| `selection`, `arrow_up` | Select_0, dir_arrow0_0 | Small cyan/gold selection arrow; red/gold upward triangle |
| `battle_win`, `battle_loss` | bwin, blost | Vietnamese outcome word art |

Use nearest-neighbor texture filtering when displaying original low-resolution art. Scale fills within the original stepped frame, rather than replacing the entire frame with generic rectangular progress bars. Put portraits behind the ring overlay. The supplied Sprite border metadata is authoritative; several pieces are not configured for nine-slicing.

## Composition measured from video

Measurements are approximate pixel observations from 193s, excluding recording black margins. Active game rectangle: **x≈227–1086, y≈0–558**. Treat this as a roughly 860×558 reference canvas, not the full 1280×720 recording.

| Region | Approximate normalized position in game rectangle |
| --- | --- |
| Map/battle world | x 0–100%, y 0–71% |
| Bottom control/chat strip | y 71–100% |
| Left D-pad panel | x 0–25.5%, y 71–100%; top lobe rises to y≈60% |
| Cyan chat area | x 25.5–79.5%, y 72–100% |
| Confirm/back panel | x 79.5–100%, y 71–100%; two diagonally staggered oval controls |
| Upper-left portrait/bars | x≈1–35%, y≈0–15% |
| Two left round shortcuts | x≈2–13%, centered at y≈26% and 44% |
| Map/minimap/timer indicators | upper-right, x≈68–100%, y≈0–13% |
| Gold edge toggle | right edge, centered at y≈26% |
| Battle action menu | icons span x≈18–77%, y≈16–30%; cyan oval x≈25–73%, y≈27–38% |
| Skill/list overlay at 209s | x≈1–99%, y≈0–71%; bottom controls remain exposed |

The game fills its canvas with the map. There is no permanent external side inspector or dashboard. Map entities occupy much less screen area than the HUD pieces; names float above actors. Bottom chat is a real, prominent pale-cyan block with tightly packed text. Confirm and back are always visually separate from the central chat block.

## Visible battle/control flow, 180–220 seconds

Extracted every integer second into `tools/.cache/reference/video-hud/180.png` through `220.png`; three contact sheets are `contact-180.jpg`, `contact-194.jpg`, and `contact-208.jpg`. These are research/cache artifacts, not runtime assets. Full-size frames at 193, 209, 210 and 215 seconds were inspected in addition to all contact sheets.

| Seconds | Visible behavior |
| --- | --- |
| 180 | Outdoor hub with multiple named people; normal map and entire HUD visible. |
| 181 | Map blacks out while HUD persists; small loading status appears. |
| 182 | Standalone branded loading page. |
| 183–191 | Cave field appears. Characters walk among small rock-like creatures; HUD and chat persist. Around 184–187 a short white notification crosses the field. This is field movement before the action menu. |
| 192 | Cyan action platform and first icons appear above the field. |
| 193–194 | Full horizontal action menu: ice blocks, claw, staff, bag, shield, pink fleeing creature. Actors remain visible below it. Menu is placed toward upper-middle, not in the bottom chat strip. |
| 195–198 | Action platform disappears. Blue creature and smaller actors remain arranged in the field; pale/white short effect labels and floating combat text appear. |
| 199–204 | A short cyan skill-name label appears near actors; red/green floating numeric text and small effects appear in successive frames. No numeric damage formula can be inferred from these images. |
| 205 | Effects subside; actors hold their battle positions. |
| 206–208 | Same action platform returns, then its icons populate. This supports a repeating command-selection phase. |
| 209 | Blue/gold skill list covers the world region while bottom HUD remains. Two visible rows, gold heading, MP column, cyan highlighted first row, and a blue description tooltip overlapping the rows. Staff selection leading into a skill list is visually consistent, but the exact click is not captured by one-second samples. |
| 210 | Skill list closes. A cyan diamond marks the blue creature's feet; a small cyan/gold arrow points toward it. The actor name and a short bar remain above it. This is visible target-selection feedback. |
| 211–212 | Field background becomes black while HUD and actors remain; animated effects and floating numeric text appear. This is a battle effect presentation, distinct from the branded loading page at 182. |
| 213–214 | Cave background returns; white marker/tomb-like sprites replace several earlier small actors. |
| 215 | Red status text crosses the middle field. Exact low-resolution Chinese wording is not transcribed. |
| 216–218 | Action platform and icon choices appear again. White marker sprites remain. |
| 219 | Platform closes; field/HUD remain and a small cyan status/control appears near lower-right world edge. |
| 220 | Background blacks out again with actors and HUD retained and another cyan skill/effect label. The battle has not visibly concluded within this sample. |

The observed loop is **field movement → command platform → skill list when invoked → actor targeting → action effects → command platform again**. The record does not establish server turn rules, cooldowns, exact hotkeys, targeting validity, or battle formulas. The D-pad, chat, and confirm/back strip persist during battle and skill menus.

## Gaps

- Exact old-video slender D-pad and gold stepped bar chrome were not found among reviewed 3.2 slices; exported alternatives are explicitly the APK variants.
- The video's shield/defend action icon has not been mapped to an APK Sprite. Five other action icons and the cyan action platform are mapped.
- The two video left shortcuts use different center symbols than the inventory/pet shortcuts in this APK. Blank blue circular chrome is provided so behavior can use separate icons.
- Exact minimap frame and old Chinese bitmap font have not been mapped. Use existing supplied font assets separately; do not flatten text into these HUD images.
- `panel_menu` provides an authentic decorative frame, but the video's internal gradients, table header, tooltip, and text require composition from rows/colors/text. `frame_chat` needs separately composed borders.
- No numerical stats or mechanics should be claimed as recovered from visual estimates.

## Verification

All exported PNGs were opened with Pillow and checked against source dimensions; an assembled contact sheet was visually inspected. All requested core controls use original Sprite slice exports and contain source provenance. Every output PNG hash matches its extracted source PNG. The exporter creates only HUD assets and metadata; it does not alter scene scripts or the backend.
