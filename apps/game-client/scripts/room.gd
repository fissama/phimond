extends Control

signal npc_selected(id: String)
signal portal_selected(id: String)
signal enemy_selected(id: String)
signal target_selected(id: String)
signal ground_selected(direction: String)

const Art = preload("res://scripts/reference_art.gd")
const GOLD = Color("ffe084")
const BLUE = Color("6fedff")
const STEP_SECONDS := 0.18
var art = Art.new()
# Public assignments retained for fixture/older client compatibility.
var character: Dictionary = {}
var catalog: Dictionary = {}
var elapsed := 0.0
var displayed_x := -1.0
var displayed_y := 12.0
var last_position := -1.0
var last_map := ""
var walking_until := 0.0
var facing_left := false
var selected_target := ""
var _preview_x := -1.0
var _preview_y := -1.0
var _preview_until := 0.0
var _camera_x := 0.0
var _background: Texture2D
var _background_rect := Rect2()
var _definition: Dictionary = {}
var _battle: Dictionary = {}
var _battle_id := ""
var _batch_revision := -1
var _finish_until := 0.0
var _effects: Array[Dictionary] = []
var _hit_areas: Array[Dictionary] = []
var _unit_positions: Dictionary = {}
var _hp_display: Dictionary = {}
var _transition := 0.0

func _ready() -> void:
	custom_minimum_size = Vector2(480, 260)
	mouse_filter = Control.MOUSE_FILTER_STOP
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	clip_contents = true
	art.prepare()
	_sync_map()

func set_snapshot(next_character: Dictionary, next_catalog: Dictionary) -> void:
	var old_map := str(character.get("map_id", ""))
	character = next_character
	catalog = next_catalog
	cancel_preview()
	if old_map != str(character.get("map_id", "")):
		_sync_map()
	_sync_battle()
	queue_redraw()

func preview_move(direction: String) -> void:
	if not _battle.is_empty():
		return
	var step := -1.0 if direction in ["left", "west", "up"] else 1.0
	if direction not in ["left", "west", "right", "east", "up", "down"]: return
	_preview_x = float(character.get("x", 6))
	_preview_y = float(character.get("y", 12))
	if direction in ["up", "down"]:
		_preview_y = clampf(_preview_y + step, 0, float(_definition.get("height", 24)) - 1)
	else:
		_preview_x = clampf(_preview_x + step, 0, float(_definition.get("width", 40)) - 1)
		facing_left = step < 0
	_preview_until = elapsed + 1.5
	walking_until = elapsed + 0.3

func cancel_preview() -> void:
	_preview_x = -1.0
	_preview_y = -1.0
	_preview_until = 0.0

func _sync_map() -> void:
	var map_id := str(character.get("map_id", "severa"))
	_definition = catalog.get("maps", {}).get(map_id, {})
	# Go serializes an empty optional spawn slice as null on peaceful maps.
	# Normalize at the render boundary without changing the shared catalog.
	if not _definition.get("wild_spawns") is Array:
		_definition = _definition.duplicate()
		_definition["wild_spawns"] = []
	_background = art.room_texture(map_id)
	if map_id != last_map:
		displayed_x = float(character.get("x", 6))
		displayed_y = float(character.get("y", 12))
		last_position = displayed_x
		last_map = map_id
		_transition = 0.2
		_camera_x = -1

func _sync_battle() -> void:
	var next: Dictionary = character.get("battle") if character.get("battle") is Dictionary else {}
	_select_battle(next)

func reset_presentation() -> void:
	_batch_revision = -1
	_finish_until = 0
	_effects.clear()
	_hp_display.clear()
	_battle = {}
	_battle_id = ""
	selected_target = ""
	character = {}
	cancel_preview()
	queue_redraw()

func apply_state_batch(revision: int, next_character: Dictionary, next_catalog: Dictionary, events: Array, presentation: Dictionary) -> void:
	if revision <= _batch_revision: return
	_batch_revision = revision
	character = next_character
	catalog = next_catalog
	cancel_preview()
	_sync_map()
	var next: Dictionary = character.get("battle") if character.get("battle") is Dictionary else {}
	var completed: Variant = presentation.get("completed_battle")
	var terminal := next.is_empty() and completed is Dictionary and not str(presentation.get("battle_id", "")).is_empty() and str(completed.get("id", "")) == str(presentation.get("battle_id")) and completed.get("units") is Array
	if terminal:
		_select_battle(completed)
	elif not next.is_empty() or _finish_until <= elapsed:
		_select_battle(next)
	if not _battle.is_empty() and str(presentation.get("battle_id", "")) == _battle_id:
		_queue_events(events)
	if terminal:
		_finish_until = elapsed + 0.6
		for effect in _effects: _finish_until = maxf(_finish_until, float(effect.end) + 0.2)
	queue_redraw()

func _select_battle(next: Dictionary) -> void:
	var id := str(next.get("id", ""))
	if id != _battle_id:
		_battle_id = id
		_finish_until = 0
		_effects.clear()
		_hp_display.clear()
		_unit_positions.clear()
		selected_target = ""
		for unit in next.get("units", []):
			if unit.get("side") != "player" and int(unit.get("hp", 0)) > 0:
				selected_target = str(unit.get("id", ""))
				break
	_battle = next

func _queue_events(events: Array) -> void:
	var start := elapsed
	for effect in _effects: start = maxf(start, float(effect.end))
	var ids: Array = []
	for unit in _battle.get("units", []): ids.append(str(unit.get("id", "")))
	var available := start
	for event in events:
		if not event is Dictionary: continue
		var kind := str(event.get("type", ""))
		if kind not in ["skill_cast", "damage", "heal", "status_applied", "miss"]: continue
		if str(event.get("target_id", "")) not in ids: continue
		if kind == "skill_cast": start = maxf(start, available) + 0.12
		var effect: Dictionary = event.duplicate()
		effect["start"] = start
		effect["end"] = start + (0.65 if kind == "skill_cast" else 1.1)
		_effects.append(effect)
		available = maxf(available, float(effect.end))
		if kind == "damage": start += 0.28

func _process(delta: float) -> void:
	elapsed += delta
	_sync_map()
	# A fixture may assign character directly instead of calling set_snapshot.
	if character.get("battle") is Dictionary and str(character.battle.get("id", "")) != _battle_id:
		_sync_battle()
	if _finish_until > 0 and elapsed >= _finish_until:
		_battle = {}
		_battle_id = ""
		_finish_until = 0
		selected_target = ""
	var target := float(character.get("x", 6))
	if _preview_x >= 0 and elapsed < _preview_until:
		target = _preview_x
	if target != last_position:
		facing_left = target < last_position
		walking_until = elapsed + 0.25
		last_position = target
	displayed_x = move_toward(displayed_x, target, delta / STEP_SECONDS)
	var target_y := _preview_y if _preview_y >= 0 and elapsed < _preview_until else float(character.get("y", 12))
	if absf(displayed_y - target_y) > 0.01: walking_until = elapsed + 0.15
	displayed_y = move_toward(displayed_y, target_y, delta / STEP_SECONDS)
	_transition = maxf(0, _transition - delta)
	_update_camera(delta)
	_effects = _effects.filter(func(effect: Dictionary): return elapsed < float(effect.end))
	# Follow the display frame cadence. Resetting a 1/60 timer to zero dropped
	# every second frame when delta was just below the threshold.
	queue_redraw()

func _update_camera(delta: float) -> void:
	if _background == null or size.y < 1:
		_background_rect = Rect2(Vector2.ZERO, size)
		return
	var dimensions := _background.get_size()
	var zoom := maxf(size.x / dimensions.x, size.y / dimensions.y)
	var scaled := dimensions * zoom
	var world_x := 55 + displayed_x / maxf(float(_definition.get("width", 40)) - 1, 1) * (scaled.x - 110)
	var target := clampf(world_x - size.x * 0.42, 0, maxf(scaled.x - size.x, 0))
	if _camera_x < 0:
		_camera_x = target
	_camera_x = lerpf(_camera_x, target, 1 - exp(-delta * 7))
	_background_rect = Rect2(Vector2(-_camera_x, size.y - scaled.y), scaled)

func room_x(position: float) -> float:
	return 55 + position / maxf(float(_definition.get("width", 40)) - 1, 1) * (_background_rect.size.x - 110) - _camera_x

func _floor_y() -> float:
	return size.y * 0.78

func room_y(value: float) -> float:
	return size.y * (0.40 + 0.50 * value / maxf(float(_definition.get("height", 24)) - 1, 1))

func is_animating() -> bool:
	return not _effects.is_empty() or _finish_until > elapsed

func contact_spawn(point: Vector2i) -> Dictionary:
	for spawn in _definition.get("wild_spawns", []):
		if absi(point.x - int(spawn.x)) <= 1 and absi(point.y - int(spawn.y)) <= 1:
			return spawn
	return {}

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), Color("152633"))
	if _background != null:
		draw_texture_rect(_background, _background_rect, false)
	_hit_areas.clear()
	_unit_positions.clear()
	if _battle.is_empty():
		_draw_world()
	else:
		_draw_battle()
	_draw_effects()
	if _transition > 0:
		draw_rect(Rect2(Vector2.ZERO, size), Color(0.03, 0.07, 0.1, _transition * 2))

func _draw_world() -> void:
	var floor_y := _floor_y()
	for portal in _definition.get("portals", []):
		var x := clampf(room_x(float(portal.get("x", 0))), 24, size.x - 24)
		var pos := Vector2(x, floor_y + 17)
		_ring(pos, BLUE, 23)
		var direction := -1 if float(portal.get("x", 0)) < 10 else 1
		var arrow := PackedVector2Array([pos + Vector2(-7 * direction, -20), pos + Vector2(7 * direction, -29), pos + Vector2(-7 * direction, -38)])
		draw_polyline(arrow, BLUE, 3)
		var destination: Dictionary = catalog.get("maps", {}).get(portal.get("to", ""), {})
		var destination_name := str(destination.get("name", str(portal.get("to", "Gate")).capitalize()))
		var half_label := ThemeDB.fallback_font.get_string_size(destination_name, HORIZONTAL_ALIGNMENT_LEFT, -1, 12).x / 2 + 6
		_label(Vector2(clampf(pos.x, half_label, size.x - half_label), pos.y + 51), destination_name, BLUE, 12)
		_hit_areas.append({"rect": Rect2(pos - Vector2(34, 54), Vector2(68, 86)), "kind": "portal", "id": str(portal.get("id", ""))})
	for npc in catalog.get("npcs", {}).values():
		if str(npc.get("map_id", "")) != last_map:
			continue
		var pos := Vector2(room_x(float(npc.get("x", 6))), room_y(float(npc.get("y", 12))))
		var id := str(npc.get("id", ""))
		_actor(art.npc_texture(id), pos, 61, false)
		_label(pos - Vector2(0, 77), "!", GOLD, 21)
		_label(pos - Vector2(0, 63), str(npc.get("name", "Guide")), GOLD, 12)
		_hit_areas.append({"rect": Rect2(pos - Vector2(40, 85), Vector2(80, 105)), "kind": "npc", "id": id})
	# Draw the same contact positions that the server validates.
	var spawns: Array = _definition.get("wild_spawns", [])
	for index in range(spawns.size()):
		var species := str(spawns[index].species_id)
		var pos := Vector2(room_x(float(spawns[index].x)), room_y(float(spawns[index].y)))
		_actor(art.pet_texture(species, elapsed + index * 0.17), pos, 48, index % 2 == 0)
		_label(pos + Vector2(0, 17), str(catalog.get("species", {}).get(species, {}).get("name", species.capitalize())), Color("fff3c6"), 11)
		_hit_areas.append({"rect": Rect2(pos - Vector2(36, 61), Vector2(72, 81)), "kind": "enemy", "id": str(spawns[index].id)})
	var player := Vector2(room_x(displayed_x), room_y(displayed_y))
	_ring(player, Color("a5f2d8"), 17)
	var action := "run" if elapsed < walking_until else "idle"
	_actor(art.actor_texture("Boy", action, elapsed), player, 59, facing_left)
	for pet in character.get("pets", []):
		if pet.get("id") == character.get("active_pet_id"):
			_actor(art.pet_texture(str(pet.get("species_id", "")), elapsed, action), player + Vector2(47 if facing_left else -47, 9), 46, facing_left)
	_label(player - Vector2(0, 67), str(character.get("name", "Phimond")), Color("e5ffff"), 12)

func _draw_battle() -> void:
	var floor_y := _floor_y()
	var left_index := 0
	var right_index := 0
	for unit in _battle.get("units", []):
		var enemy: bool = unit.get("side") != "player"
		var row := right_index if enemy else left_index
		var pos := Vector2(size.x * (0.34 if enemy else 0.67), floor_y - 10 - row * 68)
		_unit_positions[str(unit.get("id", ""))] = pos
		if enemy: right_index += 1
		else: left_index += 1
	for unit in _battle.get("units", []):
		var id := str(unit.get("id", ""))
		var enemy: bool = unit.get("side") != "player"
		var pos: Vector2 = _unit_positions[id]
		var action := "idle"
		var tint := Color.WHITE
		for effect in _effects:
			var age := elapsed - float(effect.start)
			if age < 0:
				continue
			if effect.get("type") == "skill_cast" and str(effect.get("actor_id", "")) == id and age < 0.5:
				action = "attack"
				var target_pos: Vector2 = _unit_positions.get(str(effect.get("target_id", "")), pos)
				pos += (target_pos - pos).normalized() * sin(age / 0.5 * PI) * 32
			if effect.get("type") == "damage" and str(effect.get("target_id", "")) == id and age < 0.35:
				tint = Color(1, 0.65 + age, 0.65 + age)
				pos.x += sin(age * 65) * 3
		if int(unit.get("hp", 0)) <= 0:
			action = "die"
			tint.a = 0.5
		if id == selected_target and int(unit.get("hp", 0)) > 0:
			_ring(pos, BLUE, 30)
			_label(pos - Vector2(0, 94), "▼", BLUE, 17)
		# Source pets face left: mirror the left-side enemy toward its opponent.
		_actor(art.pet_texture(str(unit.get("species_id", "")), elapsed, action), pos, 62, enemy, tint)
		_label(pos - Vector2(0, 76), str(unit.get("name", "Creature")), GOLD if enemy else BLUE, 13)
		var hp := float(unit.get("hp", 0))
		var maximum := maxf(float(unit.get("max_hp", 1)), 1)
		_hp_display[id] = move_toward(float(_hp_display.get(id, hp)), hp, maximum / 12)
		draw_rect(Rect2(pos + Vector2(-35, 11), Vector2(70, 7)), Color("151d23"))
		draw_rect(Rect2(pos + Vector2(-34, 12), Vector2(68 * float(_hp_display[id]) / maximum, 5)), Color("ef765c") if enemy else Color("68e4a2"))
		_label(pos + Vector2(0, 33), "%d / %d" % [int(hp), int(maximum)], Color.WHITE, 10)
		if enemy and int(unit.get("hp", 0)) > 0:
			_hit_areas.append({"rect": Rect2(pos - Vector2(43, 88), Vector2(86, 121)), "kind": "target", "id": id})
	if _finish_until > 0:
		_label(Vector2(size.x * 0.5, size.y * 0.32), str(_battle.get("result", "")).to_upper(), GOLD, 24)

func _draw_effects() -> void:
	for effect in _effects:
		var age := elapsed - float(effect.start)
		if age < 0:
			continue
		var target := str(effect.get("target_id", ""))
		if not _unit_positions.has(target):
			continue
		var pos: Vector2 = _unit_positions[target]
		var kind := str(effect.get("type", ""))
		var tint := Color("fff2c1")
		tint.a = clampf(1.2 - age, 0, 1)
		if kind == "damage":
			tint = Color(1, 0.25, 0.22, tint.a)
			_label(pos - Vector2(0, 85 + age * 30), "−%d" % int(effect.get("amount", 0)), tint, 24)
			if age < 0.25:
				var center := pos - Vector2(0, 28)
				draw_line(center - Vector2(13, 17), center + Vector2(13, 17), Color(1, 0.9, 0.5, 1 - age * 4), 3)
				draw_line(center + Vector2(15, -12), center + Vector2(-15, 12), Color(1, 1, 1, 1 - age * 4), 2)
		elif kind == "heal":
			_label(pos - Vector2(0, 85 + age * 30), "+%d" % int(effect.get("amount", 0)), Color("89ffac"), 23)
		elif kind == "status_applied":
			_ring(pos - Vector2(0, 18), Color(0.74, 0.48, 1, tint.a), 27 + age * 9)
		elif kind == "miss":
			_label(pos - Vector2(0, 85 + age * 30), "Trượt", tint, 20)

func _actor(sprite: Texture2D, feet: Vector2, height: float, flipped: bool = false, tint: Color = Color.WHITE) -> void:
	if sprite == null:
		_ring(feet, Color("8299b0"), 14)
		_label(feet - Vector2(0, 16), "?", GOLD, 24)
		return
	var factor := minf(height / sprite.get_height(), 94.0 / sprite.get_width())
	var dimensions := sprite.get_size() * factor
	var shadow := PackedVector2Array()
	for i in range(20):
		shadow.append(feet + Vector2(cos(i * TAU / 20) * minf(dimensions.x * 0.36, 23), sin(i * TAU / 20) * 4))
	draw_colored_polygon(shadow, Color(0.04, 0.06, 0.07, 0.25 * tint.a))
	var rect := Rect2((feet - Vector2(dimensions.x / 2, dimensions.y)).round(), dimensions.round())
	if flipped:
		# draw_texture_rect flips negative widths without moving the destination.
		rect.size.x = -rect.size.x
	draw_texture_rect(sprite, rect, false, tint)

func _ring(pos: Vector2, tint: Color, radius: float) -> void:
	var points := PackedVector2Array()
	for i in range(33):
		points.append(pos + Vector2(cos(i * TAU / 32) * radius, sin(i * TAU / 32) * radius * 0.29))
	draw_polyline(points, tint, 1.6)

func _label(pos: Vector2, value: String, tint: Color, font_size: int) -> void:
	var width := ThemeDB.fallback_font.get_string_size(value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size).x
	var origin := pos - Vector2(width / 2, 0)
	draw_string_outline(ThemeDB.fallback_font, origin, value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, 3, Color(0.025, 0.055, 0.07, tint.a))
	draw_string(ThemeDB.fallback_font, origin, value, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, tint)

func _gui_input(event: InputEvent) -> void:
	var point := Vector2.ZERO
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		point = event.position
	elif event is InputEventScreenTouch and event.pressed:
		point = event.position
	else:
		return
	for index in range(_hit_areas.size() - 1, -1, -1):
		var hit: Dictionary = _hit_areas[index]
		if not hit.rect.has_point(point):
			continue
		match str(hit.kind):
			"npc": npc_selected.emit(str(hit.id))
			"portal": portal_selected.emit(str(hit.id))
			"enemy": enemy_selected.emit(str(hit.id))
			"target":
				selected_target = str(hit.id)
				target_selected.emit(selected_target)
		accept_event()
		return
	if _battle.is_empty():
		var offset := point - Vector2(room_x(displayed_x), room_y(displayed_y))
		ground_selected.emit(("left" if offset.x < 0 else "right") if absf(offset.x) > absf(offset.y) else ("up" if offset.y < 0 else "down"))
		accept_event()
