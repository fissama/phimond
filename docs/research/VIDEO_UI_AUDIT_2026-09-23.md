# Phimond — video-first reconstruction audit

## Reference and coverage

Primary: [Pokezoo - Huyền thoại một thời](https://www.youtube.com/watch?v=FXJtLBPoGgo), 04:33. User confirmed this exact reference on 2026-09-23 after its duration was checked in the YouTube player. Local supplied MP4 is 1280×720, 273.285760 seconds; title, duration and opening imagery match the link. No new remote video was downloaded.

Reviewed the entire local timeline in chronological one-second contact sheets, 00:00–04:32, including the final partial second. Detailed native-size frames were inspected for inventory, pet attributes and battle, alongside the earlier 180–220s battle study. This is a full-timeline scrub, not a claim of frame-by-frame analysis at 30fps. Transient sub-second states and illegible Chinese text remain uncertain.

Evidence: `/tmp/phimond-audit-01.jpg` through `18.jpg`; `/tmp/phimond-ref-inventory.png`; `/tmp/phimond-ref-pet.png`; existing `docs/research/reference/video-0210.png`. Current client was rendered from real scenes with offline fixture state into `/tmp/phimond-ui-before/{login,world,npc,battle}.png` using `scripts/visual_audit.gd`. Fixtures do not imply a successful server playtest.

**Two visual variants occur in this one video.** 00:10–00:28 promotional montage uses a horizontal brown toolbar and tan chat. The sustained playable-client footage at 00:34–04:33 uses the blue/gold HUD, bottom D-pad/chat/confirm strip, and world-region overlays. Use the latter as the consistent reconstruction target; do not mix montage chrome with its HUD.

## Video UI inventory

Times below are directly observed sampled timestamps, not estimated action start times.

| Timestamp | Observed state | Composition, controls and flow |
|---|---|---|
| 00:00–00:09 | Illustrated intro | Full-frame tree-house painting and Chinese promotional text; not an account form. |
| 00:10–00:12 | Promotional town view | Full-width top bars, brown square icon toolbar above tan chat; many characters and labels. Different client presentation. |
| 00:13–00:30 | Promotional montage | Title cards alternate with cave, tree bridges, castle, monsters; 00:22 narrow menu. Synthesis is advertised at 00:25, but its actual interface is not demonstrated. |
| 00:32–00:33 | Branded loading | Logo, animated small figures on loading platform, black surround, web address. |
| 00:34–00:35 | Character entry | Village background; small character/location/level strip upper area; left/right character arrows; central dark list with enter/create/delete entries. No username/password screen visible. |
| 00:36–00:38 | Enter world / notice | Black field with persistent HUD, loading card, then town with large translucent notice and central confirmation. |
| 00:39–01:05 | Town exploration | Dominant raster town field, overlapping outlined actor names, cyan diamonds/portals, small player and larger pet follower; camera pans horizontally. HUD stable. |
| 01:06–01:07 | Portal transition / castle | Field blacks out with compact loading notice; same controls persist; castle map follows. |
| 01:08–01:12 | Castle approach | Named NPCs across open plaza, cyan marker above selected NPC, pet follows trainer. |
| 01:13–01:16 | NPC dialogue + actions | Thin wide rounded navy speech strip near upper world area; tiny NPC image left, cream text. Separate narrow dark option list floats lower-center, cyan selected row and small scroll arrows. Map remains visible. |
| 01:18–01:20 | Quest detail / rewards | Ornate panel replaces world region only. Vertical title rail left, objective text, cyan separators/highlight, compact numeric rewards, page arrows upper-right. Bottom HUD remains. |
| 01:21 | System notice | Small translucent centered notice over world; chat reflects updates. |
| 01:26–01:29 | NPC quest options / item reward | Same dialogue+list, then quest/reward panel and blue item tooltip. |
| 01:31–01:35 | Repeat NPC / quest flow | Options, detail, then field and system message. No modern centered modal with seven big buttons. |
| 01:38 | Edge menu opening | Round shortcut icons expand along right edge. |
| 01:39–01:47 | Inventory | Blue/gold world-region panel, vertical left title, **six-column, four-row visible slot grid**, quantity numerals lower-right, cyan/gold selection. Blue rectangular item tooltip overlaps grid; two bag pages indicated. This is not the merchant screen. |
| 01:48–01:49 | Expanded main menu | Approximately 3×3 round icon group upper-right of world; edge toggle remains. |
| 01:50–01:53 | Pet list / context menu | World-region pet panel; row selection opens narrow dark action list. Some entry labels are too blurred to transcribe confidently. |
| 01:54–01:55 | Pet attributes | Portrait and name/level/race/star/gender above compact tabs; two columns of base/derived stat rows; HP/MP/EXP stacked at right. Left vertical title rail, gold frame. |
| 01:56–01:57 | Pet resistance | Same header; tab change reveals dense colored numeric resistance rows. |
| 01:58–01:59 | Pet equipment | Compact item table under pet header, selected cyan row, small overlapping item tooltip. |
| 02:00–02:02 | Pet growth | Brief loading/blank panel then growth/stat table; same tab strip with previous/next arrows. |
| 02:03–02:08 | Pet skills / descriptions | Skill rows with level/type columns, cyan selection, blue tooltip with skill text and MP information. No large cards. |
| 02:09–02:12 | Further pet tabs / description | Dense numeric stats then largely empty description tab. Exact all-tab names need higher-resolution source. |
| 02:13–02:16 | Back to world / menu | Panel fades to world; round menu opens; centered loading notice precedes player list. |
| 02:17–02:27 | Nearby players / context menu | Ornate list with name/level/status columns and avatars; context menu includes invitation/friend-related entries. Backend support must not be fabricated. |
| 02:28–02:32 | Party confirmation / controls | Confirmation inside list, return to world with additional small party portraits/status; narrow party menu opens. |
| 02:33–02:51 | Party in castle | Two trainers and companions move together; persistent blue action/status at lower-right field. |
| 02:52–03:02 | Travel / town / cave transition | Branded loading, town fountain, field-black loading, then cave. |
| 03:03–03:11 | Cave exploration | Small ground creatures, rugged raster backdrop, party/companion labels; visible vertical differences between actors, no proof of exact collision grid. |
| 03:12–03:14 | Battle commands | Same cave field and bottom HUD. Six icons across cyan oval platform upper-middle: ice-block/auto, claw, staff, bag, shield, fleeing pink creature. No two-card arena. |
| 03:15–03:25 | Attack/effect resolution | Platform hides; actors act in field, small HP bars above, floating white/red/green feedback and short cyan skill labels. |
| 03:26–03:28 | Next command selection | Same six-icon platform returns. |
| 03:29 | Battle skill list | Ornate world-region panel, compact skill/level/MP columns, cyan row highlight and blue description tooltip. Bottom strip still visible. |
| 03:30 | Target selection | Menu closes; cyan diamond at target feet, small selection arrow and name/bar above actor. |
| 03:31–03:35 | Group skill effect | Field darkens to black while actors/HUD remain; ice-like effects and damage numbers; background returns, several defeated markers, red central message. Formula/target semantics not inferable from video. |
| 03:36–03:49 | Repeat / automatic battle | Command platform returns, repeated skill effects, blue lower-right automatic-mode control. No separate full-screen reward card. |
| 03:50–04:01 | Battle end / world / travel | Party returns to field, chat updates; loading back to town, short system notice, then next portal. |
| 04:02–04:06 | Beach exploration | Sea-wave raster background, small pink plant creatures, NPC labels and portal. This is a beach, not snow. |
| 04:07–04:20 | Beach battle | Pet to right, small foes to left; repeated darkened skill effects, numbers and defeated markers; stable HUD, auto control visible. |
| 04:21–04:32 | World return / further beach battles | Brief party exploration, then more attacks with same visual language. Video ends during combat; no credits or final victory dialogue. |

## Repeating visual system and measured composition

The active client rectangle is approximately x=227–1086, y=0–558 inside the recording (black video margins are not part of the game). Aspect is about 1.54:1. Adopt a fixed 960×624 logical composition with aspect-preserving scaling, rather than a fluid webpage.

- World / replacing menu: upper ~71% (about 444 logical pixels).
- Persistent bottom controls: ~29%; left D-pad panel ~25.5% width, pale cyan chat ~54%, right confirm/back panel ~20.5%.
- Upper-left: overlapping small portrait rings and stepped HP/MP/other colored bars. Two circular shortcuts descend along the left.
- Upper-right: small map/location/minimap-like strip and clock; original geography mapping is not available. Do not invent a functional minimap.
- Main menu: gold right-edge toggle opens compact round icons.
- Menu panel: deep navy interior, blue gradient inner edges, gold/bronze ornamental left side and corners, narrow title rail, cyan row selection, compact cream/white text with dark outline; titles mostly normal game-text size.
- Bottom chat: about 4–6 dense lines, channel-colored text with dark outlines. No permanent modern tab bar in this playable-client variant.
- Input: D-pad and two confirmation/back softkeys are visible. Exact physical keyboard/touch mappings cannot be proven; desktop WASD/arrows and click/tap affordances are an explicit platform adaptation.
- World pans horizontally and changes by room portals; vertical actor movement is present. No evidence sufficient to recover collision meshes, parallax layers or original map dimensions.
- Combat positions vary by player/party. Do not infer fixed player-left from convention: footage often puts the large blue companion at right and enemies left.

## Current UI gap analysis / screen matching

Current audit is based on scene code and actual fixture renders, not old reports alone.

| Reference | Current implementation | Gap / required change |
|---|---|---|
| 00:39 world HUD | `MainMap` full top toolbar + dark bottom chat; inset dim map | Restore edge HUD, field-first framing, persistent source softkey strip; retain 2D server movement. |
| 03:13 battle | Separate full-window two-card UI; trainer sprite used for both sides in audit | Render actual species in map field and preserve HUD; six-icon platform and nested selectors. |
| 01:13 NPC | Huge 768×480 window, duplicated title, placeholder `Button` labels; world renders over it | Correct CanvasLayer ordering; upper speech band + contextual list; label every action. |
| 01:39 inventory | No production bag screen; shop list is not inventory | Six-column slots, quantities, selection/detail, currency; show only real inventory data. |
| 01:54–02:12 pet | Legacy `main.gd` has menus, but current scene entry path does not expose them | Add compact pet list/detail tabs to active client, not parallel obsolete UI. |
| 01:18 quest | NPC picks first quest silently | Visible quest list/objective/progress/reward/accept/claim using server definitions. |
| 03:29 skill selection | Hard-coded `skill_basic`; item hard-coded `potion` | Actual owned skills and inventory; costs; target confirmation. |
| 03:15 effects | Variables for damage declared but unused; single shared tween cancels earlier bar/entry tween | Sequential authoritative-event presentation, independently updated bars, no fabricated damage. |
| 00:34 entry | Oversized account form over stretched source UI texture | Account login is not shown in video: use APK frame/button language as an explicitly adapted screen. No fake character slots. |
| Shop (not observed) | Purchase list in generic large modal; NPC sends unsupported `npc.shop` | Contextual shop opens locally and sends existing `shop.buy`; layout adaptation needs additional reference before claiming exact fidelity. |
| 02:17 social/party | No matching game server APIs | Mark unsupported; do not add fake online players, chat, invitations or success states. |

Additional compatibility findings (reported, backend unchanged): NPC/portal server proximity currently checks X only; portals preserve Y; MainMap hard-codes grid dimensions despite catalog width/height; `PhimondClient` leaves rejected requests pending and repeats messages for duplicate revisions. These are distinct from visual fidelity and should not justify rewriting game rules.

## Available original asset inventory and mapping

Repository manifests record APK3.2: 1,313 Texture2D, 1,347 Sprite, 780 AnimationClip; APK8.4: 1,314 Texture2D, 1,347 Sprite, 780 AnimationClip. These are object counts, not unique images. Curated reference assets include 44 HUD aliases, five map composites, five NPC images, 10 semantically mapped species plus player actors. Four project-only evolved species remain unmapped; existing placeholder mappings are not source identity evidence.

| Class | Video element / time | Existing asset | Reuse method / confidence |
|---|---|---|---|
| A/F | Blue/gold menu, 01:18/01:39 | `reference/hud/panel_menu.png` (`UI_0`) | Nine-slice, fixed corners and left ornament; strong visual family match. |
| B | Selected/list rows, 01:52/03:29 | `row_menu`, `row_selected`, `tab_menu` | Tile/stretch plain center, retain short edges. |
| D/F | D-pad, 00:39 onward | `dpad` (`UIall_10`) | Aspect-preserving image; **APK diamond/round variant differs from video slender cross**. |
| F | Bottom panels | `panel_controls`, `panel_ornate`, `frame_chat` | Tile ornamental panel; cyan gradient strip may stretch; no stretched decorated corners. |
| D/F | Confirm/back | `button_confirm`, `button_back` | Original oval silhouette, independent text; aspect preserved. |
| F | Portrait/bar chrome | `frame_portrait`, `frame_bars`, `bar_hp`, `bar_mp`, `bar_xp` | Fixed chrome and clipped fills; APK silver vs video gold difference documented. |
| D | Round shortcuts, 01:48 | `button_pet`, `button_inventory`, `button_quest`, `button_settings`, `button_shop` | Actual raster icons; exact video centers differ for some entries. |
| D/F | Battle platform, 03:13 | `battle_actions`, `icon_auto`, `icon_attack`, `icon_magic`, `icon_inventory`, `icon_run` | Platform ellipse plus separate fixed-size icons; shield still unmapped. |
| D | Slots, 01:39 | `slot`, `slot_light`, extracted item/pet icons | Grid cells, selected border overlay; do not assign arbitrary unknown icons to item IDs. |
| C | Player/pets | `reference/actors`, `actors.json`; extracted SpriteFrames | Actual frame sequences; original per-frame timing not recovered. |
| E | Town/beach, 00:39/04:02 | `reference/rooms/severa.png`, `beach.png` | Camera framing/crop, no uniform aspect distortion. Other server maps retain their existing art correspondence. |
| C/D | NPC | `reference/npcs` + manifest | Five source sprites, gameplay role mapping reconstructed. |
| G | Fonts | extracted Arial/LiberationSans/DroidSerif | Latin/Vietnamese coverage must be tested; these alone do not establish Chinese coverage. Use tested CJK fallback, compact sizes. |
| G | Extended raw assets | `assets/extracted/{sbw_v32,sbw_v84,extended}` | Names/categories are search hints, not verified video mappings. |

Detailed source Sprite IDs, hashes, borders and pivots: `apps/game-client/assets/reference/hud/hud.json`; earlier forensic notes: `HUD_REFERENCE.md` and `APK_VIDEO_RECONSTRUCTION.md`.

## Missing / unproven assets and systems

- Exact old-video cross D-pad, gold stepped bar chrome, shield action icon, all top-level shortcut variants, original bitmap/CJK font and minimap data.
- Exact skill particle sequences, original frame timing, defeated marker mapping and all item-ID-to-icon relationships.
- Account/password login, shop transactions, ranch, appraisal, strengthening, breeding/synthesis, auction, mail and guild screens are **not clearly shown as usable interfaces** in this 4:33 video. A promotional synthesis title is not interface evidence.
- Character selection and nearby-player/party screens are visible, but multi-character/party server systems are not established in this project. Preserve truthful availability.

## Shared UI component inventory

Reconstruct one persistent `ReferenceHUD` (world canvas + bottom strip); `SourcePanel` with fixed-corner frame/title rail; source oval softkeys; round icon controls; compact highlighted list; six-column item slots; adjacent tooltip; clipped source HP/MP bars; game-styled input; speech band + option list; shared system-message area. All overlays stay in the same top CanvasLayer. Menus replace only world-region content; no browser-style independent reflow.

## Implementation priority and interaction decisions

1. World HUD / viewport / four-direction interaction: most screen time, base for every overlay. Cache assets/NPC nodes, use catalog dimensions and direct world interactions. No permanent debug movement buttons.
2. Field battle: second sustained gameplay sequence; restore platform → skill/item selector → target → effect → next command. Keep backend one-active-pet/one-opponent semantics; do not fabricate party combat. Capture is available through the bag/action mapping rather than replacing observed shield control. Auto uses actual server turn responses.
3. NPC + quests: clearly observed repeated workflow; correct overlay ordering and contextual options.
4. Pet list/details + inventory: substantial clear reference; compact tabs/slots/tooltips with actual state.
5. Shop + trainer/ranch operations: use same source components and existing backend actions; label reference fidelity as adapted until additional original footage is verified.
6. Entry: compact source-framed authentication; no claim of exact unseen login reconstruction.
7. Unsupported social/guild/mail/auction: documented gaps, not mock functionality.

Use equivalent desktop interaction only where necessary (WASD/arrows, click targets, hover descriptions); record deviations in implementation report. Preserve server calculations, schema, economics and network authority.

## Acceptance / comparison loop

For each implemented major screen, render a deterministic scene fixture at logical size and a larger aspect-preserving window, compare with its timestamped reference, then revise geometry/assets/text. Keep before/after artifacts. Playtest real account login, all four directions, NPC→quest/shop, field encounter, skill/item/capture/flee, battle end and reconnect. Passing parser tests alone is not visual or gameplay acceptance.

## Risks

Video is low-resolution, contains version variants, and does not show every requested system. APK variants supply different chrome. Reconstructed map topology/stats cannot be recovered visually. Current NPC overlay/layering and battle sprite binding have functional defects in addition to style problems. Current test scripts include stale scene paths; tests must exercise the active entry path. Exact 100% reproduction is neither established nor promised.

Audit completed before changes to production GUI code. The only new code at audit time is the offline screenshot harness.

## Implementation follow-up (after audit)

The delivered client retains the existing 960×640 logical viewport (1152×768 default window), with a 454px world and 186px controls. This is a 2.6% aspect difference from the proposed 960×624 reference measurement, retained for compatibility with existing source components. Fixed anchors and aspect-preserving output remain; it is a documented fidelity difference, not exact geometry acceptance.

Additional reference search on 2026-09-23 found [historical Android release coverage](https://games.sina.com.cn/y/n/2010-11-05/1559449774.shtml) describing D-pad/confirm/cancel and direct touch operation. [Historical synthesis description](https://baike.so.com/doc/6094355-6307463.html) supplies contextual workflow but does not verify shop/ranch screen geometry. Neither is evidence to change current server rules. No reliable additional visual reference for those screens was established; they remain adaptations.

Side-by-side evidence and remaining deviations: [comparison gallery](ui-comparison-2026-09-23/index.html), [implementation verification](UI_RECONSTRUCTION_VERIFICATION_2026-09-23.md).
