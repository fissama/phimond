extends Control
## Persistent source-client composition, shared by world and battle entry scenes.
const HUD = preload("res://scripts/classic_hud.gd")
const Menus = preload("res://scripts/reference_menus.gd")
var hud: Control
var room: Control
var menus = Menus.new()
var client: Node
var page := "World"
var npc_id := ""
var held := ""
var move_delay := 0.0
var destination: Dictionary = {}
var selected_action: Dictionary = {}
var automatic := false
var action_delay := 0.0
var history: Array[String] = []
var shortcuts: Control
var dialogue: PanelContainer
var dialogue_text: Label
var last_battle := ""
var debug_label: Label
var hud_delay := 0.0
var contact_latch := ""
var contact_map := ""

func _ready() -> void:
	client = get_node("/root/PhimondClient")
	hud = HUD.new()
	add_child(hud)
	room = hud.world
	hud.page_requested.connect(_open)
	hud.command_requested.connect(_command)
	hud.move_started.connect(func(direction: String):
		if page != "World": _menu_direction(direction); return
		held = direction; destination.clear(); _move(direction))
	hud.move_stopped.connect(func(): held = "")
	room.npc_selected.connect(func(id: String): _approach("npc", id))
	room.portal_selected.connect(func(id: String): _approach("portal", id))
	room.enemy_selected.connect(func(id: String): _approach("enemy", id))
	room.target_selected.connect(func(_id: String): _confirm_target())
	room.ground_selected.connect(_move)
	client.state_batch_received.connect(_on_state_batch)
	client.log_message.connect(_message)
	client.action_pending_changed.connect(func(_busy: bool): _sync_hud())
	client.connection_changed.connect(func(connected: bool):
		if not connected:
			held = ""
			destination.clear()
			automatic = false
			selected_action.clear()
			room.cancel_preview())
	client.connection_changed.connect(func(connected: bool):
		if not connected: room.reset_presentation())
	_build_overlays()
	_on_state_batch(client.revision, client.state, [], {})
	_message("Mũi tên / WASD: di chuyển · E: tương tác · Esc: menu")

func _build_overlays() -> void:
	shortcuts = Control.new()
	shortcuts.position = Vector2(741, 108)
	shortcuts.size = Vector2(210, 220)
	shortcuts.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shortcuts)
	var entries := [["button_pet", "Companions", "Linh thú"], ["button_inventory", "Inventory", "Túi đồ"], ["button_quest", "Quests", "Nhiệm vụ"], ["button_orb", "Journey", "Bản đồ"], ["button_shop", "Shop", "Cửa hàng gần đây"], ["button_guild", "Ranch", "Trang trại"], ["button_settings", "Settings", "Kết nối"], ["button_cancel", "World", "Đóng"]]
	for i in range(entries.size()):
		var entry: Array = entries[i]
		var button = hud._image_button(str(entry[0]), "", Rect2((i % 3) * 68, int(i / 3) * 70, 58, 60), str(entry[2]), shortcuts)
		button.pressed.connect(func(): _open(str(entry[1])))
	shortcuts.hide()
	dialogue = PanelContainer.new()
	dialogue.position = Vector2(75, 87)
	dialogue.size = Vector2(807, 83)
	var box := StyleBoxFlat.new()
	box.bg_color = Color("06182d")
	box.border_color = Color("a18e56")
	box.set_border_width_all(2)
	box.set_corner_radius_all(17)
	box.content_margin_left = 20
	box.content_margin_right = 20
	box.content_margin_top = 9
	box.content_margin_bottom = 9
	dialogue.add_theme_stylebox_override("panel", box)
	dialogue_text = Label.new()
	dialogue_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	dialogue_text.add_theme_font_size_override("font_size", 17)
	dialogue_text.add_theme_color_override("font_color", Color("fff0c4"))
	dialogue.add_child(dialogue_text)
	add_child(dialogue)
	dialogue.hide()
	debug_label = Label.new()
	debug_label.position = Vector2(270, 420)
	debug_label.add_theme_font_size_override("font_size", 12)
	debug_label.hide()
	add_child(debug_label)

func _on_state_batch(revision: int, character: Dictionary, events: Array, presentation: Dictionary) -> void:
	if character.is_empty(): return
	room.apply_state_batch(revision, character, client.catalog, events, presentation)
	var battle = character.get("battle")
	var battle_id := str(battle.get("id", "")) if battle is Dictionary else ""
	if battle_id != last_battle:
		_close()
		held = ""
		destination.clear()
		selected_action.clear()
		last_battle = battle_id
	if battle_id.is_empty(): automatic = false
	action_delay = 0.8
	_sync_hud()
	if page != "World": _render_menu()

func _sync_hud() -> void:
	for control in hud.field_controls: control.visible = page in ["World", "NPC"]
	hud.update_state(client.state, client.catalog, client.is_busy(), automatic)
	hud.battle_bar.visible = client.has_battle() and page == "World" and selected_action.is_empty() and not client.is_busy() and not room.is_animating()
	hud.detail.text = "Chọn mục tiêu · Esc: hủy" if not selected_action.is_empty() else ("Chọn lệnh chiến đấu" if client.has_battle() else "Mũi tên / WASD: đi · E: tương tác · Esc: menu")
	if debug_label != null: debug_label.text = "rev %d · (%d,%d) · %s" % [client.revision, int(client.state.get("x", 0)), int(client.state.get("y", 0)), str(client.state.get("map_id", ""))]

func _process(delta: float) -> void:
	if client == null: return
	move_delay -= delta
	action_delay -= delta
	hud_delay -= delta
	if hud_delay <= 0:
		_sync_hud()
		hud_delay = 0.10
	if client.is_busy() or not client.is_ws_connected() or page != "World": return
	if client.has_battle():
		if automatic and action_delay <= 0 and not room.is_animating(): _battle_send("auto")
		return
	if room.is_animating(): return
	if _check_contact(): return
	if not destination.is_empty() and move_delay <= 0: _travel_step()
	elif not held.is_empty() and move_delay <= 0: _move(held)

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey: return
	var direction := ""
	match event.keycode:
		KEY_A, KEY_LEFT: direction = "left"
		KEY_D, KEY_RIGHT: direction = "right"
		KEY_W, KEY_UP: direction = "up"
		KEY_S, KEY_DOWN: direction = "down"
	if not event.pressed:
		if direction == held: held = ""
		return
	if event.echo or get_viewport().gui_get_focus_owner() is LineEdit: return
	if event.keycode == KEY_F3: debug_label.visible = not debug_label.visible; return
	if event.keycode == KEY_ESCAPE: _command("back")
	elif event.keycode in [KEY_E, KEY_SPACE, KEY_ENTER]: _command("confirm")
	elif not direction.is_empty() and page == "World":
		destination.clear()
		held = direction
		_move(direction)

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		held = ""
		destination.clear()

func _move(direction: String) -> void:
	if page != "World" or client.has_battle() or client.is_busy() or room.is_animating() or move_delay > 0: return
	var state: Dictionary = client.state
	var map: Dictionary = client.catalog.get("maps", {}).get(state.get("map_id", ""), {})
	var point := Vector2i(int(state.get("x", 0)), int(state.get("y", 0)))
	match direction:
		"left": point.x -= 1
		"right": point.x += 1
		"up": point.y -= 1
		"down": point.y += 1
		_: return
	move_delay = room.STEP_SECONDS
	if point.x < 0 or point.y < 0 or point.x >= int(map.get("width", 40)) or point.y >= int(map.get("height", map.get("width", 40))):
		held = ""
		return
	client.world_move(direction)
	if client.is_busy(): room.preview_move(direction)

func _approach(kind: String, id: String) -> void:
	if client.has_battle() or room.is_animating() or client.is_busy(): return
	var state: Dictionary = client.state
	var point: Dictionary = client.catalog.get("npcs", {}).get(id, {}) if kind == "npc" else {}
	if kind == "portal":
		for portal in client.catalog.get("maps", {}).get(state.get("map_id", ""), {}).get("portals", []):
			if portal.get("id") == id: point = portal
	elif kind == "enemy":
		for spawn in client.catalog.get("maps", {}).get(state.get("map_id", ""), {}).get("wild_spawns", []):
			if spawn.get("id") == id: point = spawn
	if point.is_empty(): return
	_close()
	destination = {"kind": kind, "id": id, "x": int(point.get("x", 0)), "y": int(point.get("y", 12))}
	_travel_step()

func _travel_step() -> void:
	if client.is_busy() or room.is_animating(): return
	var dx := int(destination.x) - int(client.state.get("x", 0))
	var dy := int(destination.y) - int(client.state.get("y", 0))
	if absi(dx) > 1: _move("right" if dx > 0 else "left")
	elif absi(dy) > 1: _move("down" if dy > 0 else "up")
	else:
		var target := destination.duplicate()
		destination.clear()
		if target.kind == "portal": client.world_portal(str(target.id))
		elif target.kind == "enemy": _encounter(str(target.id))
		else:
			npc_id = str(target.id)
			client.interact_npc(npc_id)
			_open("NPC")

func _nearest() -> Dictionary:
	var best: Dictionary = {}
	var distance := 999
	for npc in client.catalog.get("npcs", {}).values():
		if npc.get("map_id") != client.state.get("map_id"): continue
		var d := absi(int(npc.get("x", 0)) - int(client.state.get("x", 0))) + absi(int(npc.get("y", 12)) - int(client.state.get("y", 0)))
		if d < distance:
			best = npc
			distance = d
	return best if distance <= 5 else {}

func _command(command: String) -> void:
	if room.is_animating(): return
	if command == "back":
		if not selected_action.is_empty(): selected_action.clear()
		elif page != "World" or shortcuts.visible: _close()
		else: _open("Menu")
		return
	if page != "World" and command in ["confirm", "interact"]:
		var focus = get_viewport().gui_get_focus_owner()
		if focus is Button and not focus.disabled: focus.pressed.emit()
		return
	if client.has_battle():
		match command:
			"Skills", "Items": _open(command)
			"auto": automatic = not automatic; action_delay = 0; _close()
			"attack", "capture": selected_action = {"choice": command}; automatic = false; _close()
			"defend", "flee": automatic = false; _battle_send(command)
			"confirm", "interact": _confirm_target()
	elif command in ["confirm", "interact"]:
		if page != "World": return
		var npc := _nearest()
		if not npc.is_empty(): _approach("npc", str(npc.id))
		else:
			for portal in client.catalog.get("maps", {}).get(client.state.get("map_id", ""), {}).get("portals", []):
				if absi(int(portal.x) - int(client.state.get("x", 0))) <= 2:
					_approach("portal", str(portal.id))
					return
			_message("Hãy chọn người hướng dẫn, cổng hoặc linh thú trên bản đồ.")

func _check_contact() -> bool:
	var map_id := str(client.state.get("map_id", ""))
	if map_id != contact_map:
		contact_map = map_id
		contact_latch = ""
	var spawn: Dictionary = room.contact_spawn(Vector2i(int(client.state.get("x", 0)), int(client.state.get("y", 0))))
	if spawn.is_empty(): contact_latch = ""; return false
	if str(spawn.id) == contact_latch: return false
	_encounter(str(spawn.id))
	return true

func _encounter(spawn_id: String = "") -> void:
	if page != "World" or client.has_battle() or client.is_busy() or room.is_animating(): return
	contact_latch = spawn_id
	held = ""
	destination.clear()
	client.encounter(spawn_id)

func _confirm_target() -> void:
	if not client.has_battle(): return
	_battle_send(str(selected_action.get("choice", "attack")), str(selected_action.get("skill_id", "")), str(selected_action.get("item_id", "")))

func _battle_send(choice: String, skill: String = "", item: String = "") -> void:
	if not client.has_battle() or client.is_busy() or room.is_animating(): return
	var battle: Dictionary = client.state.battle
	selected_action.clear()
	_close()
	action_delay = 0.8
	client.battle_action(str(battle.id), int(battle.turn), choice, skill, item)

func _open(value: String) -> void:
	held = ""
	destination.clear()
	if value == "Menu": shortcuts.visible = not shortcuts.visible; return
	shortcuts.hide()
	if value == "World": _close(); return
	if value == "Supplies": value = "Inventory"
	page = value
	_render_menu()

func _close() -> void:
	page = "World"
	hud.menu.hide()
	dialogue.hide()
	shortcuts.hide()
	get_viewport().gui_release_focus()

func _render_menu() -> void:
	for child in hud.content_box.get_children():
		hud.content_box.remove_child(child)
		child.queue_free()
	hud.menu.position = Vector2(7, 3)
	hud.menu.size = Vector2(946, 447)
	hud.menu.show()
	dialogue.hide()
	match page:
		"Companions", "Inventory", "Quests", "Ranch": menus.build(page, hud.content_box, client, _open)
		"NPC": _npc()
		"Skills": _skills()
		"Items": _items()
		"Shop": _shop()
		"Journey": _journey()
		"Settings":
			_heading("Kết nối")
			_button("Kết nối lại", func(): client.connect_ws(); _close())
			_text("Phimond · Mũi tên/WASD để di chuyển. Chọn NPC, cổng hoặc linh thú trên bản đồ.")
		_: _text("Tính năng chưa khả dụng.")
	_sync_hud()
	_focus_first(hud.content_box)

func _focus_first(parent: Node) -> bool:
	for child in parent.get_children():
		if child is Button and not child.disabled:
			child.grab_focus()
			return true
		if _focus_first(child): return true
	return false

func _menu_direction(direction: String) -> void:
	var focus = get_viewport().gui_get_focus_owner()
	if focus == null: _focus_first(hud.content_box); return
	var next: Control = focus.find_prev_valid_focus() if direction in ["up", "left"] else focus.find_next_valid_focus()
	if next != null: next.grab_focus()

func _npc() -> void:
	var npc: Dictionary = client.catalog.get("npcs", {}).get(npc_id, {})
	dialogue_text.text = str(npc.get("name", "")) + "\n" + str(npc.get("dialogue", "Bạn cần giúp gì trong chuyến đi này?"))
	dialogue.show()
	hud.menu.position = Vector2(338, 183)
	hud.menu.size = Vector2(380, 262)
	for entry in [["shop", "Cửa hàng", "Shop"], ["quest", "Nhiệm vụ", "Quests"], ["breed", "Lai tạo / cường hóa", "Ranch"], ["appraise", "Xem linh thú", "Companions"]]:
		if entry[0] in npc.get("roles", []): _button(entry[1], func(): _open(entry[2]))
	if "heal" in npc.get("roles", []): _button("Hồi phục linh thú", func(): client.heal_pets())
	if "arena" in npc.get("roles", []): _button("Thách đấu", func(): client.challenge_arena())
	_button("Đóng", _close)

func _journey() -> void:
	_heading(str(client.catalog.get("maps", {}).get(client.state.get("map_id", ""), {}).get("name", "Bản đồ")))
	for portal in client.catalog.get("maps", {}).get(client.state.get("map_id", ""), {}).get("portals", []):
		_button("→ " + str(client.catalog.maps.get(portal.to, {}).get("name", portal.to)), func(): _approach("portal", str(portal.id)))
	for npc in client.catalog.get("npcs", {}).values():
		if npc.get("map_id") == client.state.get("map_id"):
			_button(str(npc.name), func(): _approach("npc", str(npc.id)))

func _skills() -> void:
	_heading("Kỹ năng                       Cấp / MP")
	if not client.has_battle(): _text("Chưa có trận chiến."); return
	var mp := 0
	for unit in client.state.battle.get("units", []):
		if unit.get("side") == "player": mp = int(unit.get("mp", 0))
	for pet in client.state.get("pets", []):
		if pet.get("id") != client.state.get("active_pet_id"): continue
		for id in pet.get("skills", []):
			var skill: Dictionary = client.catalog.get("skills", {}).get(id, {})
			var button := _button("%s                          %d MP" % [skill.get("name", id), int(skill.get("mp_cost", 0))], func(): selected_action = {"choice": "skill", "skill_id": id}; automatic = false; _close())
			button.disabled = int(skill.get("mp_cost", 0)) > mp
			button.tooltip_text = str(skill.get("description", ""))
	_text("MP còn lại: %d · Chọn kỹ năng rồi chọn mục tiêu." % mp)

func _items() -> void:
	_heading("Vật phẩm chiến đấu")
	for id in client.state.get("inventory", {}):
		var item: Dictionary = client.catalog.get("items", {}).get(id, {})
		var count := int(client.state.inventory[id])
		if count > 0 and item.get("kind") in ["heal", "mp"]:
			_button("%s ×%d" % [item.get("name", id), count], func(): _battle_send("item", "", str(id)))
	_button("Bắt linh thú", func(): selected_action = {"choice": "capture"}; automatic = false; _close())

func _shop() -> void:
	_heading("Cửa hàng · %d vàng" % int(client.state.get("gold", 0)))
	var nearby := _nearest()
	if nearby.is_empty() or not "shop" in nearby.get("roles", []):
		_text("Hãy đến gặp thương nhân để mua vật phẩm.")
		return
	for item in client.catalog.get("items", {}).values():
		var row := HBoxContainer.new()
		hud.content_box.add_child(row)
		var name := Label.new()
		name.text = "%s  ·  %d vàng  ·  ×%d" % [item.get("name", item.id), int(item.get("price", 0)), int(client.state.get("inventory", {}).get(item.id, 0))]
		name.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name)
		var button := Button.new()
		button.text = "Mua 1"
		button.pressed.connect(func(): client.buy(str(item.id), 1))
		row.add_child(button)

func _heading(value: String) -> void:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", 18)
	label.add_theme_color_override("font_color", Color("f5d779"))
	hud.content_box.add_child(label)

func _text(value: String) -> void:
	var label := Label.new()
	label.text = value
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hud.content_box.add_child(label)

func _button(value: String, callback: Callable) -> Button:
	var button := Button.new()
	button.text = value
	button.custom_minimum_size.y = 34
	button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	button.pressed.connect(callback)
	hud.content_box.add_child(button)
	return button

func _message(value: String) -> void:
	history.append(value)
	if history.size() > 60: history.pop_front()
	hud.log_text.text = "\n".join(history)
	if value.begins_with("Không") or value.begins_with("Hãy"):
		automatic = false
		destination.clear()
		held = ""
