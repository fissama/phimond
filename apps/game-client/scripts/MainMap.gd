extends Node2D
## MainMap — top-down world view (mobile-style portrait HUD).
##
## Layout (logical 360×640-ish area, anchored inside 960×640 project viewport):
##   ┌─ TopHud (48 px) — HP icon+bar, MP icon+bar, gold, pet portrait, name
##   ├─ Center        — animated world with Player, Pet, NPCs on a room BG
##   └─ ChatPanel     — tabs + RichTextLabel + bottom input placeholder
##
## Player is an AnimatedSprite2D that flips between 'idle' and 'run' during
## the 150 ms move tween. NPCs are 80×80 TextureRects using the catalog
## gameplay mapping (existing behaviour). Keyboard movement uses the default
## Godot InputMap actions (ui_left/ui_right/ui_up/ui_down).

const TILE := 16
const GRID_W := 40
const GRID_H := 24
const PLAYER_FRAME_W := 41
const PLAYER_FRAME_H := 58
const NPC_SIZE := 80
const MOVE_TWEEN_MS := 150
# Client-side movement throttle — server validates per-tick anyway, but
# without throttling we'd send one world.move per render frame (~60/s).
const MOVE_COOLDOWN_S := 0.12

@onready var _room_bg: TextureRect = $CanvasLayer/Viewport/Root/Center/RoomBg
@onready var _world: Node2D = $CanvasLayer/Viewport/Root/Center/World
@onready var _player: AnimatedSprite2D = $CanvasLayer/Viewport/Root/Center/World/Player
@onready var _pet: AnimatedSprite2D = $CanvasLayer/Viewport/Root/Center/World/Pet
@onready var _npc_layer: Node2D = $CanvasLayer/Viewport/Root/Center/World/NPCLayer
@onready var _hp_bar: Control = $CanvasLayer/Viewport/Root/TopHud/TopRow/HpBar
@onready var _mp_bar: Control = $CanvasLayer/Viewport/Root/TopHud/TopRow/MpBar
@onready var _gold_label: Label = $CanvasLayer/Viewport/Root/TopHud/TopRow/GoldLabel
@onready var _name_label: Label = $CanvasLayer/Viewport/Root/TopHud/TopRow/NameLabel
@onready var _pet_portrait: TextureRect = $CanvasLayer/Viewport/Root/TopHud/TopRow/PetPortrait
@onready var _chat_log: RichTextLabel = $CanvasLayer/Viewport/Root/ChatPanel/ChatBody/ChatLog
@onready var _world_tab: Control = $CanvasLayer/Viewport/Root/ChatPanel/ChatBody/TabsRow/WorldTab
@onready var _party_tab: Control = $CanvasLayer/Viewport/Root/ChatPanel/ChatBody/TabsRow/PartyTab
@onready var _guild_tab: Control = $CanvasLayer/Viewport/Root/ChatPanel/ChatBody/TabsRow/GuildTab
@onready var _system_tab: Control = $CanvasLayer/Viewport/Root/ChatPanel/ChatBody/TabsRow/SystemTab

# Pre-loaded menu scenes — Worker D owns the logic, we just give a handle so
# that the existing trigger paths (debug buttons) still work. Keep vars so the
# BattleScene's interaction-style menu openers don't break.
var _npc_menu_scene: PackedScene = preload("res://scenes/NpcMenu.tscn")
var _shop_menu_scene: PackedScene = preload("res://scenes/ShopMenu.tscn")

# NPC sprite mapping — copied from reference/npcs/manifest.json so the scene
# doesn't need to JSON.parse on the hot path.
var _npc_sprite_path: Dictionary = {
	"trainer": "res://assets/reference/npcs/level3_1030.png",
	"ranch_keeper": "res://assets/reference/npcs/level3_1029.png",
	"arena_master": "res://assets/reference/npcs/level3_1024.png",
	"forest_guide": "res://assets/reference/npcs/level4_353.png",
	"beach_guide": "res://assets/reference/npcs/level5_668.png",
}

var _move_tween: Tween = null
var _pet_tween: Tween = null
var _move_cooldown: float = 0.0
# -1 = facing left, +1 = facing right. Drives player + pet scale flip.
var _facing: int = 1
var _center_size: Vector2 = Vector2.ZERO
var _chat_log_count: int = 0
const CHAT_LOG_MAX := 50


func _ready() -> void:
	# Capture the center area's actual size — player/NPC positions are expressed
	# relative to it so re-sizing the viewport doesn't push them off-canvas.
	# Defer one frame so anchors resolve first.
	call_deferred("_capture_layout")

	if _player and not _player.is_playing():
		_player.play("idle")
	if _pet and _pet.sprite_frames and _pet.sprite_frames.has_animation("idle"):
		_pet.play("idle")

	# Tab labels + initial state.
	for node in [_world_tab, _party_tab, _guild_tab, _system_tab]:
		if node and node.has_method("set_text_label"):
			node.call("set_text_label", node.name.trim_suffix("Tab"))
	for tab in [_world_tab, _party_tab, _guild_tab, _system_tab]:
		if tab and tab.has_method("set_selected"):
			tab.call("set_selected", false)
	if _world_tab and _world_tab.has_method("set_selected"):
		_world_tab.call("set_selected", true)

	# Default bars / labels before first state arrives.
	if _hp_bar and _hp_bar.has_method("set_value_instant"):
		_hp_bar.call("set_value_instant", 100.0)
	if _mp_bar and _mp_bar.has_method("set_value_instant"):
		_mp_bar.call("set_value_instant", 100.0)
	if _gold_label: _gold_label.text = "G: 0"
	if _name_label: _name_label.text = "Wanderer"
	if _chat_log:
		_chat_log.text = ""
		_append_chat("[color=#a08040]connected.[/color]")
		_append_chat("[color=#a08040]tip: arrow keys to walk; Z to talk; B to battle.[/color]")

	# Subscribe to client events.
	PhimondClient.state_updated.connect(_on_state_updated)
	PhimondClient.connection_changed.connect(func(c):
		_append_chat("[color=#a08040]ws: " + ("connected" if c else "connecting…") + "[/color]")
	)
	PhimondClient.log_message.connect(func(t):
		# Catch non-WS chatter (network errors, action rejections).
		if t.begins_with("ws not open") or t.begins_with("error:"):
			_append_chat("[color=#c87060]" + t + "[/color]")
	)
	# Render NPCs on first frame after the catalog (if any) is loaded.
	_render_npcs()


func _capture_layout() -> void:
	var center: Control = $CanvasLayer/Viewport/Root/Center
	_center_size = center.size
	# Snap the player to its current tile position (or centre if no state yet).
	if _player:
		var tx := int(PhimondClient.state.get("x", GRID_W / 2))
		var ty := int(PhimondClient.state.get("y", GRID_H / 2))
		var nx := (float(tx) / float(GRID_W)) * _center_size.x
		var ny := (float(ty) / float(GRID_H)) * _center_size.y
		_player.position = Vector2(nx, ny)
	if _pet:
		_pet.position = _player.position + Vector2(16 * _facing, -8)


func _room_bg_for(map_id: String) -> String:
	var path := "res://assets/reference/rooms/%s.png" % map_id
	if ResourceLoader.exists(path):
		return path
	return "res://assets/reference/rooms/severa.png"


func _render_npcs() -> void:
	if _npc_layer == null: return
	for child in _npc_layer.get_children():
		child.queue_free()
	var map_id := str(PhimondClient.state.get("map_id", ""))
	if _room_bg:
		var room_path := _room_bg_for(map_id)
		var tex := load(room_path) as Texture2D
		if tex:
			_room_bg.texture = tex
	for npc in PhimondClient.catalog.get("npcs", {}).values():
		if npc.get("map_id") != map_id:
			continue
		var npc_id := str(npc.get("id", ""))
		var display_name := str(npc.get("name", npc_id))
		var tex_path: String = _npc_sprite_path.get(npc_id, "")

		# Container — positions the NPC + its name label as a unit so we can
		# tween / remove them atomically.
		var holder := Node2D.new()
		# Position NPCs relative to the world area, mapped from tile coords.
		var x := int(npc.get("x", 0))
		var y := int(npc.get("y", 0))
		var nx := (float(x) / float(GRID_W)) * _center_size.x - NPC_SIZE * 0.5
		var ny := (float(y) / float(GRID_H)) * _center_size.y - NPC_SIZE * 0.5
		holder.position = Vector2(nx, ny)
		_npc_layer.add_child(holder)

		# Sprite (texture or yellow-rect fallback).
		var sprite: CanvasItem = null
		if not tex_path.is_empty() and ResourceLoader.exists(tex_path):
			var tr := TextureRect.new()
			tr.size = Vector2(NPC_SIZE, NPC_SIZE)
			tr.texture = load(tex_path)
			tr.expand_mode = 1
			tr.stretch_mode = 5
			sprite = tr
		else:
			var cr := ColorRect.new()
			cr.size = Vector2(NPC_SIZE, NPC_SIZE)
			cr.color = Color(0.9, 0.7, 0.2, 1)
			sprite = cr
		holder.add_child(sprite)

		# Name label above the sprite — sized to fit text, centred.
		var name_label := Label.new()
		name_label.text = display_name
		name_label.add_theme_color_override("font_color", Color(1, 0.95, 0.85, 1))
		name_label.add_theme_color_override("font_outline_color", Color(0, 0, 0, 1))
		name_label.add_theme_constant_override("outline_size", 4)
		name_label.add_theme_font_size_override("font_size", 12)
		name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		name_label.position = Vector2(-NPC_SIZE * 0.5, -22)
		name_label.size = Vector2(NPC_SIZE * 2.0, 18)
		holder.add_child(name_label)

		# Tiny breathing pulse — different phases so they don't sync.
		var t := create_tween().set_loops()
		var dim := Color(1, 1, 1, 0.85)
		var period := 1.1 + (randf() * 0.4)
		t.tween_property(sprite, "modulate", dim, period)
		t.tween_property(sprite, "modulate", Color(1, 1, 1, 1.0), period)


func _append_chat(line: String) -> void:
	if _chat_log == null: return
	_chat_log.text += line + "\n"
	_chat_log_count += 1
	if _chat_log_count > CHAT_LOG_MAX:
		# Trim to last CHAT_LOG_MAX lines by rebuilding.
		var all_lines := _chat_log.text.split("\n")
		var keep := all_lines.slice(max(0, all_lines.size() - CHAT_LOG_MAX - 1))
		_chat_log.text = "\n".join(keep)


func _set_bar_pct(bar: Control, value: float, max_v: float) -> void:
	if bar == null: return
	if max_v <= 0:
		if bar.has_method("set_value_instant"):
			bar.call("set_value_instant", 0)
		return
	var pct: float = clampf(value / max_v, 0.0, 1.0) * 100.0
	if bar.has_method("set_value_instant"):
		bar.call("set_value_instant", pct)


func _on_state_updated(_revision: int, character: Dictionary) -> void:
	if character.is_empty():
		return
	var map_id := str(character.get("map_id", ""))
	var map_def: Dictionary = PhimondClient.catalog.get("maps", {}).get(map_id, {})
	# TopHud name + gold.
	if _name_label:
		var display_name := str(character.get("name", ""))
		if display_name.is_empty(): display_name = "Wanderer"
		_name_label.text = display_name
	if _gold_label:
		_gold_label.text = "G: %d" % int(character.get("gold", 0))

	# HP/MP — try active pet first; fall back to 100/100 if no pet yet.
	var pets = character.get("pets", []) as Array
	var active_pet_id := str(character.get("active_pet_id", ""))
	var pet_match: Variant = null
	if not active_pet_id.is_empty():
		for p in pets:
			if p is Dictionary and str(p.get("id", "")) == active_pet_id:
				pet_match = p; break
	if pet_match == null and pets.size() > 0 and pets[0] is Dictionary:
		pet_match = pets[0]
	if pet_match is Dictionary:
		_set_bar_pct(_hp_bar, float(pet_match.get("hp", 0)), float(pet_match.get("max_hp", 1)))
		_set_bar_pct(_mp_bar, float(pet_match.get("mp", 0)), float(pet_match.get("max_mp", 1)))
	else:
		if _hp_bar and _hp_bar.has_method("set_value_instant"):
			_hp_bar.call("set_value_instant", 100.0)
		if _mp_bar and _mp_bar.has_method("set_value_instant"):
			_mp_bar.call("set_value_instant", 100.0)

	# Player position — convert tile (x,y) → viewport-pixel centre area.
	# Vertical (y) tile now drives sprite y too (was previously hard-coded at
	# 0.55 of center height, which made up/down moves invisible).
	var center: Control = $CanvasLayer/Viewport/Root/Center
	if is_instance_valid(_player) and _center_size.x > 0:
		var tx := int(character.get("x", 0))
		var ty := int(character.get("y", 0))
		var nx: float = (float(tx) / float(GRID_W)) * _center_size.x
		# Invert y so tile y=0 is at the top of the screen and tile y=GRID_H-1
		# is at the bottom — matches top-down world convention.
		var ny: float = (float(ty) / float(GRID_H)) * _center_size.y
		_tween_player_to(Vector2(nx, ny))

	if character.get("battle") is Dictionary:
		_open_battle(character.battle)
		return
	_render_npcs()

	# Server log events.
	var events = character.get("events", [])
	if events is Array:
		for ev in events:
			if ev is Dictionary:
				var msg := str(ev.get("message", ev.get("type", "...")))
				_append_chat("[color=#c8a868]" + msg + "[/color]")


func _tween_player_to(target: Vector2) -> void:
	if not is_instance_valid(_player): return
	if _move_tween and _move_tween.is_valid():
		_move_tween.kill()
	# Direction-aware sprite flip — sprite frames face right by default.
	var dx := target.x - _player.position.x
	if dx > 0.5: _facing = 1
	elif dx < -0.5: _facing = -1
	_player.scale = Vector2(_facing, 1)
	# Flip to run during the move.
	if _player.sprite_frames and _player.sprite_frames.has_animation("run"):
		_player.play("run")
	_move_tween = create_tween()
	_move_tween.tween_property(_player, "position", target, MOVE_TWEEN_MS / 1000.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	_move_tween.tween_callback(func():
		if is_instance_valid(_player) and _player.sprite_frames and _player.sprite_frames.has_animation("idle"):
			_player.play("idle")
	)
	# Pet mirrors player facing + follows with a small tween (was: snapped).
	var pet_target := target + Vector2(16 * _facing, -8)
	if is_instance_valid(_pet):
		_pet.scale = Vector2(_facing, 1)
		_tween_pet_to(pet_target)


func _tween_pet_to(target: Vector2) -> void:
	if not is_instance_valid(_pet): return
	if _pet_tween and _pet_tween.is_valid():
		_pet_tween.kill()
	_pet_tween = create_tween()
	_pet_tween.tween_property(_pet, "position", target, MOVE_TWEEN_MS / 1000.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)


func _process(delta: float) -> void:
	# Keyboard movement — uses Godot's built-in ui_left/right/up/down actions.
	# Cooldown avoids spamming the server at frame rate.
	if not is_inside_tree(): return
	if get_tree().paused: return
	_move_cooldown = max(0.0, _move_cooldown - delta)
	if _move_cooldown <= 0.0:
		if Input.is_action_pressed("ui_left"):
			_try_move("left")
		elif Input.is_action_pressed("ui_right"):
			_try_move("right")
		elif Input.is_action_pressed("ui_up"):
			_try_move("up")
		elif Input.is_action_pressed("ui_down"):
			_try_move("down")
	if Input.is_action_just_pressed("ui_accept"):
		# Approximate "talk to nearest NPC" — checks all NPCs on this map.
		_talk_nearest()
	# B = manual encounter trigger (debug affordance; BattleScene will handle
	# the auto-encounter once the server dictates one).
	if Input.is_action_just_pressed("ui_cancel"):
		PhimondClient.encounter()


func _try_move(direction: String) -> void:
	# Client-side collision: don't even send the move if it would walk off the
	# map or into a known NPC tile. Server is still authoritative — this just
	# keeps the player sprite from snapping on a doomed request.
	var px := int(PhimondClient.state.get("x", 0))
	var py := int(PhimondClient.state.get("y", 0))
	var nx := px
	var ny := py
	match direction:
		"left":  nx = px - 1
		"right": nx = px + 1
		"up":    ny = py - 1
		"down":  ny = py + 1
	if nx < 0 or nx >= GRID_W or ny < 0 or ny >= GRID_H:
		return
	# Block movement into an NPC's tile — forces a "talk" interaction instead.
	for npc in PhimondClient.catalog.get("npcs", {}).values():
		if npc.get("map_id") != PhimondClient.state.get("map_id", ""): continue
		if int(npc.get("x", 0)) == nx and int(npc.get("y", 0)) == ny:
			return
	_move_cooldown = MOVE_COOLDOWN_S
	PhimondClient.world_move(direction)


func _talk_nearest() -> void:
	var nearest := ""
	var best_dist := 999
	var px := int(PhimondClient.state.get("x", 0))
	for npc in PhimondClient.catalog.get("npcs", {}).values():
		if npc.get("map_id") != PhimondClient.state.get("map_id", ""): continue
		var d := absi(int(npc.get("x", 0)) - px)
		if d < best_dist:
			best_dist = d
			nearest = str(npc.get("id", ""))
	if nearest.is_empty():
		_append_chat("[color=#c87060]no NPC on this map[/color]")
		return
	PhimondClient.interact_npc(nearest)
	if _npc_menu_scene == null: return
	var menu := _npc_menu_scene.instantiate()
	if menu == null: return
	menu.npc_id = nearest
	add_child(menu)


func _open_battle(_battle: Dictionary) -> void:
	if get_tree().current_scene.scene_file_path.ends_with("BattleScene.tscn"): return
	get_tree().change_scene_to_file("res://scenes/BattleScene.tscn")
