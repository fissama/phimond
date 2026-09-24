extends Control

const RoomView = preload("res://scripts/room.gd")
const MINT = Color("f5d779")
const ReferenceArt = preload("res://scripts/reference_art.gd")
const ClassicHUD = preload("res://scripts/classic_hud.gd")
var hud: Control
var reference_art = ReferenceArt.new()
var socket := WebSocketPeer.new()
var http := HTTPRequest.new()
var catalog: Dictionary = {}
var character: Dictionary = {}
var token: String = ""
var base_url: String = "http://127.0.0.1:8090"
var revision: int = -1
var counter: int = 0
var session_prefix: String = str(Time.get_unix_time_from_system()) + "-" + str(randi())
var authenticated: bool = false
var auth_sent: bool = false
var connecting: bool = false
var http_kind: String = ""
var pending: Dictionary = {}
var history: Array[String] = []
var page: String = "World"
var pending_ops: Dictionary = {}
var walk_direction: String = ""
var walk_clock: float = 0
var auto_battle: bool = false
var auto_clock: float = 0
var travel_target: Dictionary = {}
var selected_action: Dictionary = {}
var root_box: VBoxContainer
var content_box: VBoxContainer
var status: Label
var room: Control
var user_field: LineEdit
var pass_field: LineEdit
var server_field: LineEdit
var detail: Label
var log_text: RichTextLabel
var title: Label
var meta: Label
var connection_age: float = 0

func _ready() -> void:
	_build_theme()
	add_child(http)
	http.timeout = 15
	http.request_completed.connect(_http_completed)
	_build_shell()
	_login_view()

func _build_theme() -> void:
	var skin := Theme.new()
	skin.default_font_size = 15
	for type_name in ["Label", "Button", "LineEdit", "OptionButton", "RichTextLabel"]:
		skin.set_color("font_color", type_name, Color("e0e9e7"))
	for state_name in ["normal", "hover", "pressed", "focus", "disabled"]:
		var box := StyleBoxFlat.new()
		box.bg_color = Color("17628a") if state_name == "hover" else Color("0b2c49")
		box.border_color = MINT if state_name == "focus" else Color("9b8655")
		box.set_border_width_all(1)
		box.set_corner_radius_all(3)
		box.content_margin_left = 13
		box.content_margin_right = 13
		box.content_margin_top = 10
		box.content_margin_bottom = 10
		for type_name in ["Button", "LineEdit", "OptionButton"]:
			skin.set_stylebox(state_name, type_name, box)
	skin.set_color("font_disabled_color", "Button", Color("6e8188"))
	skin.set_constant("separation", "VBoxContainer", 10)
	skin.set_constant("separation", "HBoxContainer", 10)
	theme = skin

func _build_shell() -> void:
	reference_art.prepare()
	hud = ClassicHUD.new()
	add_child(hud)
	room = hud.world
	content_box = hud.content_box
	status = hud.status
	detail = hud.detail
	log_text = hud.log_text
	title = hud.title
	meta = hud.meta
	hud.page_requested.connect(_open_page)
	hud.command_requested.connect(_command)
	hud.move_started.connect(_start_walk)
	hud.move_stopped.connect(func(): walk_direction = "")
	room.npc_selected.connect(func(id: String): _travel_to("npc", id))
	room.portal_selected.connect(func(id: String): _travel_to("portal", id))
	room.enemy_selected.connect(func(_id: String): _intent("world.encounter"))
	room.target_selected.connect(func(_id: String): _confirm_target())
	room.ground_selected.connect(func(direction: String): _walk_step(direction))

func _clear() -> void:
	for child in content_box.get_children():
		content_box.remove_child(child)
		child.queue_free()

func _login_view() -> void:
	page = "Login"
	hud.menu.show()
	_clear()
	_heading("PHIMOND", "Đăng nhập hoặc tạo tài khoản để bắt đầu hành trình.")
	server_field = _field("Server URL", base_url)
	user_field = _field("Username", "")
	pass_field = _field("Password", "", true)
	var row := HBoxContainer.new()
	content_box.add_child(row)
	_button(row, "Đăng nhập", func(): _authenticate("login"))
	_button(row, "Tạo tài khoản", func(): _authenticate("register"))
	_paragraph("Tên tài khoản: 3–24 chữ/số. Mật khẩu: từ 10 ký tự.")

func _authenticate(kind: String) -> void:
	if not http_kind.is_empty():
		return
	base_url = server_field.text.strip_edges().trim_suffix("/")
	if not (base_url.begins_with("http://") or base_url.begins_with("https://")):
		_notice("Enter a server URL beginning with http:// or https://.")
		return
	if user_field.text.strip_edges().is_empty() or pass_field.text.is_empty():
		_notice("Enter a username and password.")
		return
	_request(kind, "/api/" + kind, HTTPClient.METHOD_POST, {"username": user_field.text.strip_edges(), "password": pass_field.text})

func _request(kind: String, path: String, method: int = HTTPClient.METHOD_GET, body: Dictionary = {}) -> void:
	if not http_kind.is_empty():
		_notice("A request is still in progress.")
		return
	http_kind = kind
	var headers := PackedStringArray(["Content-Type: application/json"])
	if not token.is_empty():
		headers.append("Authorization: Bearer " + token)
	var error := http.request(base_url + path, headers, method, JSON.stringify(body) if method != HTTPClient.METHOD_GET else "")
	if error != OK:
		http_kind = ""
		_notice("Could not start HTTP request: " + error_string(error))
	else:
		status.text = "Connecting to the expedition server…"

func _http_completed(result: int, code: int, _headers: PackedStringArray, bytes: PackedByteArray) -> void:
	var kind := http_kind
	http_kind = ""
	var decoded = JSON.parse_string(bytes.get_string_from_utf8())
	if result != HTTPRequest.RESULT_SUCCESS or code < 200 or code >= 300 or not decoded is Dictionary:
		_notice("Request failed (%s). %s" % [code, str(decoded.get("error", decoded.get("message", "Check the server address and connection."))) if decoded is Dictionary else "Check the server address and connection."])
		return
	if kind in ["login", "register"]:
		token = str(decoded.get("token", ""))
		pass_field.text = ""
		revision = -1
		character = {}
		_request("content", "/api/content")
	elif kind == "content":
		catalog = decoded
		_connect_socket()
	elif kind == "lineage":
		_show_lineage(decoded)
	elif kind == "logout":
		_notice("Signed out.")

func _connect_socket() -> void:
	socket.close()
	socket = WebSocketPeer.new()
	auth_sent = false
	authenticated = false
	connecting = true
	connection_age = 0
	var ws_url := base_url.replace("https://", "wss://").replace("http://", "ws://") + "/ws"
	var error := socket.connect_to_url(ws_url)
	if error != OK:
		connecting = false
		_notice("Connection failed: " + error_string(error))

func _process(delta: float) -> void:
	if not connecting:
		return
	socket.poll()
	connection_age += delta
	var state := socket.get_ready_state()
	if state == WebSocketPeer.STATE_OPEN:
		if not auth_sent:
			auth_sent = true
			_send("auth.session", {"token": token})
		while socket.get_available_packet_count() > 0:
			_receive(socket.get_packet().get_string_from_utf8())
	elif state == WebSocketPeer.STATE_CLOSED:
		connecting = false
		authenticated = false
		_stop_actions()
		_notice("Disconnected. Reconnect to restore authoritative state. Unconfirmed actions are not automatically repeated.")
	elif connection_age > 15:
		socket.close()
		connecting = false
		_notice("Connection timed out. Check the server and reconnect.")
	for request_id in pending.keys():
		if Time.get_ticks_msec() - int(pending[request_id]) > 15000:
			pending.erase(request_id)
			pending_ops.erase(request_id)
			_stop_actions()
			room.cancel_preview()
			_notice("An action was not confirmed. Refresh or reconnect before trying again.")
	walk_clock -= delta
	auto_clock -= delta
	if authenticated and pending.is_empty() and page == "World":
		if not travel_target.is_empty() and walk_clock <= 0:
			_continue_travel()
		elif not walk_direction.is_empty() and walk_clock <= 0:
			_walk_step(walk_direction)
		elif auto_battle and auto_clock <= 0:
			var battle = character.get("battle")
			if battle is Dictionary:
				_battle_intent(battle, "auto")
			else: auto_battle = false

func _receive(raw: String) -> void:
	var envelope = JSON.parse_string(raw)
	if not envelope is Dictionary:
		_notice("The server returned an unreadable message.")
		return
	var request_id := str(envelope.get("request_id", ""))
	var request_op := str(pending_ops.get(request_id, ""))
	var latency := Time.get_ticks_msec() - int(pending.get(request_id, Time.get_ticks_msec()))
	pending.erase(request_id)
	pending_ops.erase(request_id)
	var data: Dictionary = envelope.get("data", {})
	if envelope.get("op") == "error":
		_stop_actions()
		room.cancel_preview()
		hud.update_state(character, catalog, false, false)
		_notice(str(data.get("message", "Action rejected by the server.")))
		return
	if envelope.get("op") != "state":
		return
	var seq := int(envelope.get("sequence", -1))
	if seq < revision:
		return
	var is_new_revision := seq > revision
	authenticated = true
	revision = seq
	character = data.get("character", {})
	if page == "Login": page = "World"
	if not character.get("battle") is Dictionary:
		auto_battle = false
	elif request_op == "world.encounter" or request_op == "arena.challenge":
		page = "World"
		walk_direction = ""
		travel_target.clear()
	auto_clock = 0.7
	var events = data.get("events", [])
	if not events is Array:
		events = []
	if is_new_revision:
		for event in events:
			_append_log(str(event.get("message", event.get("type", "Update"))))
	if request_op == "world.move":
		_update_world()
	else:
		_render()
	if latency > 0: status.text = "Đã kết nối · %d ms" % latency

func _send(op: String, data: Dictionary) -> void:
	var envelope := _envelope(op, data)
	var request_id: String = envelope.request_id
	var error := socket.send_text(JSON.stringify(envelope))
	if error == OK:
		pending[request_id] = Time.get_ticks_msec()
		pending_ops[request_id] = op
		status.text = "Đang xử lý…" if op != "world.move" else "Đang di chuyển"
		hud.update_state(character, catalog, true, auto_battle)
	else:
		_notice("Action could not be sent. Reconnect to continue.")

func _envelope(op: String, data: Dictionary) -> Dictionary:
	counter += 1
	var request_id := session_prefix + "-" + str(counter)
	return {"op": op, "request_id": request_id, "data": data}

func _intent(op: String, data: Dictionary = {}) -> void:
	if not authenticated or socket.get_ready_state() != WebSocketPeer.STATE_OPEN:
		_notice("Sign in or reconnect before taking an action.")
		return
	if not pending.is_empty():
		status.text = "Đang chờ hành động trước…"
		return
	_send(op, data)
	if op == "world.move" and not pending.is_empty(): room.preview_move(str(data.get("direction", "right")))

func _reconnect() -> void:
	if token.is_empty():
		_login_view()
		return
	pending.clear()
	pending_ops.clear()
	_stop_actions()
	if catalog.is_empty():
		_request("content", "/api/content")
	else:
		_connect_socket()

func _sign_out() -> void:
	if not http_kind.is_empty():
		_notice("Wait for the current request to finish before signing out.")
		return
	if not token.is_empty():
		_request("logout", "/api/logout", HTTPClient.METHOD_POST)
	socket.close()
	connecting = false
	authenticated = false
	token = ""
	character = {}
	pending.clear()
	pending_ops.clear()
	_stop_actions()
	revision = -1
	room.character = {}
	_login_view()

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not authenticated: return
	if not event.pressed and event.keycode in [KEY_LEFT, KEY_A, KEY_RIGHT, KEY_D]:
		walk_direction = ""
		return
	if not event.pressed or event.echo or get_viewport().gui_get_focus_owner() is LineEdit: return
	if event.keycode == KEY_ESCAPE: _command("back")
	elif event.keycode in [KEY_SPACE, KEY_ENTER, KEY_E]: _command("confirm")
	elif event.keycode in [KEY_LEFT, KEY_A]: _start_walk("left")
	elif event.keycode in [KEY_RIGHT, KEY_D]: _start_walk("right")
	elif event.keycode == KEY_1: _command("attack")
	elif event.keycode == KEY_2: _command("Skills")
	elif event.keycode == KEY_3: _command("Items")
	elif event.keycode == KEY_4: _command("capture")

func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		walk_direction = ""
		travel_target.clear()

func _update_world() -> void:
	room.set_snapshot(character, catalog)
	hud.update_state(character, catalog, not pending.is_empty(), auto_battle)
	detail.text = "1: đánh   2: kỹ năng   3: vật phẩm   4: bắt" if character.get("battle") is Dictionary else "A / D: di chuyển    E: tương tác    Esc: menu"
	if not selected_action.is_empty(): detail.text = "Chọn mục tiêu trên bản đồ hoặc nhấn Chọn. Esc: hủy."

func _render() -> void:
	if character.is_empty():
		return
	_update_world()
	hud.menu.visible = page != "World"
	if page == "World": return
	hud.menu.position = Vector2(16, 4) if page in ["Skills", "Items"] else Vector2(113, 94)
	hud.menu.size = Vector2(928, 440) if page in ["Skills", "Items"] else Vector2(734, 347)
	_clear()
	var map_def: Dictionary = catalog.get("maps", {}).get(character.get("map_id", ""), {})
	match page:
		"Menu": _main_menu()
		"Journey": _journey(map_def)
		"Companions": _companions()
		"Ranch": _ranch()
		"Quests": _quests()
		"Supplies": _supplies()
		"Battle": _battle()
		"Skills": _skills()
		"Items": _battle_items()
		"NPC": _npc_menu()

func _open_page(value: String) -> void:
	if character.is_empty(): return
	walk_direction = ""
	travel_target.clear()
	page = value
	_render()

func _close_menu() -> void:
	page = "World"
	hud.menu.hide()
	get_viewport().gui_release_focus()

func _main_menu() -> void:
	_heading("Phimond", "Hành trình của " + str(character.get("name", "")))
	var grid := GridContainer.new()
	grid.columns = 3
	content_box.add_child(grid)
	for definition in [["Journey", "Bản đồ"], ["Companions", "Linh thú"], ["Quests", "Nhiệm vụ"], ["Supplies", "Túi đồ"], ["Ranch", "Lai tạo"], ["Battle", "Chiến đấu"]]:
		_button(grid, definition[1], func(): _open_page(definition[0]))
	var row := HBoxContainer.new()
	content_box.add_child(row)
	_button(row, "Kết nối lại", _reconnect)
	_button(row, "Đăng xuất", _sign_out)
	_button(row, "Tiếp tục", _close_menu)

func _stop_actions() -> void:
	walk_direction = ""
	travel_target.clear()
	auto_battle = false
	selected_action.clear()

func _start_walk(direction: String) -> void:
	if page != "World" or character.get("battle") is Dictionary: return
	travel_target.clear()
	walk_direction = direction
	_walk_step(direction)

func _walk_step(direction: String) -> void:
	if page != "World" or character.get("battle") is Dictionary or not pending.is_empty(): return
	walk_clock = 0.18
	_intent("world.move", {"direction": direction})

func _travel_to(kind: String, id: String) -> void:
	if character.get("battle") is Dictionary: return
	var x := -1
	if kind == "npc": x = int(catalog.get("npcs", {}).get(id, {}).get("x", -1))
	else:
		for portal in catalog.get("maps", {}).get(character.get("map_id", ""), {}).get("portals", []):
			if portal.get("id") == id: x = int(portal.get("x", -1))
	if x < 0: return
	_close_menu()
	walk_direction = ""
	travel_target = {"kind": kind, "id": id, "x": x}
	_continue_travel()

func _continue_travel() -> void:
	if not pending.is_empty() or travel_target.is_empty(): return
	var distance := int(travel_target.x) - int(character.get("x", 0))
	if absi(distance) > 1:
		_walk_step("right" if distance > 0 else "left")
	else:
		var target := travel_target.duplicate()
		travel_target.clear()
		if target.kind == "portal": _intent("world.portal", {"portal_id": target.id})
		else:
			selected_npc = str(target.id)
			page = "NPC"
			_intent("npc.interact", {"npc_id": target.id})
			_render()

var selected_npc: String = ""

func _npc_menu() -> void:
	var npc: Dictionary = catalog.get("npcs", {}).get(selected_npc, {})
	_heading(str(npc.get("name", "Người hướng dẫn")), str(npc.get("dialogue", "Bạn cần giúp gì?")))
	var roles: Array = npc.get("roles", [])
	var row := HFlowContainer.new()
	content_box.add_child(row)
	if "quest" in roles: _button(row, "Nhiệm vụ", func(): _open_page("Quests"))
	if "shop" in roles: _button(row, "Mua vật phẩm", func(): _open_page("Supplies"))
	if "heal" in roles: _button(row, "Hồi phục", func(): _intent("pet.heal"))
	if "breed" in roles or "breeding" in roles: _button(row, "Lai tạo", func(): _open_page("Ranch"))
	if "arena" in roles: _button(row, "Thách đấu", func(): _close_menu(); _intent("arena.challenge"))
	_button(row, "Linh thú", func(): _open_page("Companions"))
	_button(row, "Trở về", _close_menu)

func _command(command: String) -> void:
	if character.is_empty(): return
	if command == "back":
		if not selected_action.is_empty(): selected_action.clear(); _update_world()
		elif page != "World": _close_menu()
		else: _open_page("Menu")
		return
	var battle = character.get("battle")
	if battle is Dictionary:
		if command in ["Skills", "Items"]: _open_page(command)
		elif command == "auto":
			auto_battle = not auto_battle
			_close_menu()
			auto_clock = 0
			hud.update_state(character, catalog, not pending.is_empty(), auto_battle)
		elif command in ["confirm", "interact"]:
			_confirm_target()
		elif command in ["attack", "defend", "capture", "flee"]:
			auto_battle = false
			_battle_intent(battle, command)
	elif command in ["confirm", "interact"]:
		if page != "World": _close_menu(); return
		var nearest: Dictionary = {}
		var distance := 999
		for npc in catalog.get("npcs", {}).values():
			var gap := absi(int(npc.get("x", 0)) - int(character.get("x", 0)))
			if npc.get("map_id") == character.get("map_id") and gap < distance:
				nearest = npc
				distance = gap
		if distance <= 3: _travel_to("npc", str(nearest.id))
		else: _intent("world.encounter")

func _journey(map_def: Dictionary) -> void:
	_heading("Bản đồ và hành trình", "Chọn cổng hoặc người hướng dẫn để tự đi tới.")
	for portal in map_def.get("portals", []):
		var target: Dictionary = catalog.get("maps", {}).get(portal.get("to", ""), {})
		_button(content_box, "→ %s" % target.get("name", portal.get("to", "")), func(): _travel_to("portal", str(portal.id)))
	for npc in catalog.get("npcs", {}).values():
		if npc.get("map_id") == character.get("map_id"):
			_paragraph("%s  ·  position %s\n%s" % [npc.get("name", "Guide"), npc.get("x", 0), ", ".join(npc.get("roles", []))])
			_button(content_box, "Gặp " + str(npc.get("name", "guide")), func(): _travel_to("npc", str(npc.id)))
	_button(content_box, "Tìm linh thú hoang", func(): _close_menu(); _intent("world.encounter"))
	_button(content_box, "Heal companions", func(): _intent("pet.heal"))
	_button(content_box, "Challenge the arena", func(): page = "Battle"; _intent("arena.challenge"))
	_paragraph("Arena tier: " + str(character.get("arena_tier", 0)))

func _companions() -> void:
	_heading("Your companions", "Each bond has its own potential. Appraisal reveals hidden traits.")
	for pet in _pets():
		var active: bool = pet.id == character.get("active_pet_id")
		_pet_portrait(str(pet.get("species_id", "")))
		_paragraph("%s%s  ·  Lv %s  ·  %s★  ·  %s\nHP %s/%s   MP %s/%s   Generation %s" % ["◆ " if active else "", pet.get("name", pet.species_id), pet.get("level", 1), pet.get("star", 1), pet.get("gender", "?"), pet.get("hp", 0), pet.get("max_hp", 0), pet.get("mp", 0), pet.get("max_mp", 0), pet.get("generation", 0)])
		var row := HFlowContainer.new()
		content_box.add_child(row)
		_button(row, "Activate", func(): _intent("pet.activate", {"pet_id": pet.id}))
		_button(row, "Appraise", func(): _intent("pet.appraise", {"pet_id": pet.id}))
		_button(row, "Lineage", func(): _request("lineage", "/api/lineage/" + str(pet.id).uri_encode()))
		if pet.get("appraised", false):
			_paragraph("Quality: %s\nGrowth: %s\nElement resistance: %s\nStatus resistance: %s" % [_stat_list(pet.get("quality", {})), _stat_list(pet.get("growth", {})), _stat_list(pet.get("resistances", {})), _stat_list(pet.get("status_resistances", {}))])
		_paragraph("Skills: " + ", ".join(_names(pet.get("skills", []), "skills")))
		var learnable: Array = []
		for skill_id in catalog.get("species", {}).get(pet.species_id, {}).get("skills", []):
			if not skill_id in pet.get("skills", []) and catalog.get("skills", {}).has(skill_id):
				learnable.append(catalog.skills[skill_id])
		var skill_picker := _picker(learnable, "Choose a species skill")
		_button(content_box, "Learn selected skill", func():
			var skill_id := _selected(skill_picker)
			if not skill_id.is_empty(): _intent("pet.learn", {"pet_id": pet.id, "skill_id": skill_id}))
		var donors := _pets().filter(func(other): return other.id != pet.id)
		var donor_picker := _picker(donors, "Strengthening donor")
		_button(content_box, "Strengthen (consumes donor)", func():
			var donor_id := _selected(donor_picker)
			if not donor_id.is_empty(): _confirm("Consume the selected donor to strengthen this companion?", "pet.strengthen", {"pet_id": pet.id, "donor_id": donor_id}))
		_button(content_box, "Release companion…", func(): _confirm("Release this companion permanently?", "pet.release", {"pet_id": pet.id}))
		content_box.add_child(HSeparator.new())

func _ranch() -> void:
	_heading("The starlight ranch", "Choose two parents and a known recipe. The server validates every requirement and determines inheritance.")
	var parent_a := _picker(_pets(), "Main parent (recipe parent A)")
	var parent_b := _picker(_pets(), "Secondary parent (recipe parent B)")
	var recipes: Array = []
	for id in character.get("recipes", []):
		if catalog.get("recipes", {}).has(id): recipes.append(catalog.recipes[id])
	var recipe := _picker(recipes, "Known recipe")
	var blessing := CheckBox.new()
	blessing.text = "Request blessing (server checks cost)"
	content_box.add_child(blessing)
	_button(content_box, "Synthesize…", func():
		var a := _selected(parent_a)
		var b := _selected(parent_b)
		var r := _selected(recipe)
		if a.is_empty() or b.is_empty() or r.is_empty():
			_notice("Choose both parents and a recipe first.")
		elif a == b:
			_notice("Choose two different companions.")
		else:
			_confirm("Proceed with synthesis? Recipes may consume parents and resources. Review the recipe requirements below.", "breeding.synthesize", {"parent_a": a, "parent_b": b, "recipe_id": r, "blessing": 1 if blessing.button_pressed else 0}))
	for definition in catalog.get("recipes", {}).values():
		_paragraph("%s\n%s + %s → %s\nParent level %s · player level %s · %s gold · %s souls\nOpposite gender: %s · same star: %s · cross race: %s · consumes parents: %s" % [definition.get("name", definition.id), definition.get("parent_a", "?"), definition.get("parent_b", "?"), definition.get("result", "?"), definition.get("min_level", 0), definition.get("min_player_level", 0), definition.get("gold_cost", 0), definition.get("soul_cost", 0), definition.get("opposite_gender", false), definition.get("same_star", false), definition.get("cross_race", false), definition.get("consume_parents", false)])
		if not definition.id in character.get("recipes", []):
			_button(content_box, "Learn " + str(definition.get("name", definition.id)), func(): _intent("recipe.learn", {"recipe_id": definition.id}))

func _quests() -> void:
	_heading("Field journal", "Accept a task with a nearby quest guide, then return for your reward.")
	for quest in catalog.get("quests", {}).values():
		var progress: Dictionary = character.get("quests", {}).get(quest.id, {})
		_paragraph("%s\n%s\nProgress: %s%s" % [quest.get("name", quest.id), quest.get("description", ""), progress.get("progress", "Not accepted"), " · Claimed" if progress.get("claimed", false) else ""])
		_button(content_box, "Accept" if progress.is_empty() else "Claim reward", func(): _intent("quest.accept" if progress.is_empty() else "quest.claim", {"quest_id": quest.id}))

func _supplies() -> void:
	_heading("Traveler’s satchel", "Your inventory and the local shop. Purchases require a nearby merchant.")
	for item in catalog.get("items", {}).values():
		_paragraph("%s  × %s\n%s · Price: %s gold" % [item.get("name", item.id), character.get("inventory", {}).get(item.id, 0), item.get("description", ""), item.get("price", "Server quoted")])
		_button(content_box, "Buy one", func(): _intent("shop.buy", {"item_id": item.id, "quantity": 1}))

func _battle() -> void:
	_heading("Chiến đấu", "Chọn lệnh trên bản đồ hoặc mở bảng kỹ năng.")
	var battle = character.get("battle")
	if not battle is Dictionary:
		_paragraph("Hãy đến khu hoang dã để gặp linh thú, hoặc gặp người quản lý đấu trường.")
		_button(content_box, "Tìm linh thú hoang", func(): _close_menu(); _intent("world.encounter"))
		return
	_paragraph("Lượt %s" % battle.get("turn", 0))
	for unit in battle.get("units", []):
		_paragraph("%s · HP %s/%s · MP %s/%s" % [unit.get("name", "Linh thú"), unit.get("hp", 0), unit.get("max_hp", 0), unit.get("mp", 0), unit.get("max_mp", 0)])
	var row := HFlowContainer.new()
	content_box.add_child(row)
	for choice in [["attack", "Tấn công"], ["defend", "Phòng thủ"], ["capture", "Bắt thú"], ["auto", "Tự động"], ["flee", "Bỏ chạy"]]:
		_button(row, choice[1], func(): _command(choice[0]))
	_button(row, "Kỹ năng", func(): _open_page("Skills"))
	_button(row, "Vật phẩm", func(): _open_page("Items"))

func _skills() -> void:
	_heading("Kỹ năng", "Chọn kỹ năng, sau đó chọn mục tiêu trên bản đồ.")
	var battle = character.get("battle")
	if not battle is Dictionary: _paragraph("Chưa có trận chiến."); return
	var mp := 0
	for unit in battle.get("units", []):
		if unit.get("side") == "player": mp = int(unit.get("mp", 0))
	_paragraph("Tên kỹ năng                                         MP còn lại: %d" % mp)
	for pet in _pets():
		if pet.id == character.get("active_pet_id"):
			for skill_id in pet.get("skills", []):
				var skill: Dictionary = catalog.get("skills", {}).get(skill_id, {})
				var button := _button(content_box, "%s                               %s MP" % [skill.get("name", skill_id), skill.get("mp_cost", "?")], func():
					selected_action = {"choice": "skill", "skill_id": skill_id}
					auto_battle = false
					_close_menu()
					_update_world())
				button.alignment = HORIZONTAL_ALIGNMENT_LEFT
				button.disabled = int(skill.get("mp_cost", 0)) > mp
				button.tooltip_text = str(skill.get("description", ""))
				var row_style := StyleBoxTexture.new()
				row_style.texture = reference_art.texture("res://assets/reference/hud/row_menu.png")
				row_style.content_margin_top = 9
				row_style.content_margin_bottom = 9
				button.add_theme_stylebox_override("normal", row_style)
	_button(content_box, "Trở về trận đấu", _close_menu)

func _battle_items() -> void:
	_heading("Vật phẩm", "Dùng vật phẩm cho linh thú đang chiến đấu.")
	var battle = character.get("battle")
	if not battle is Dictionary: _paragraph("Chưa có trận chiến."); return
	for item_id in character.get("inventory", {}):
		if int(character.inventory[item_id]) > 0 and catalog.get("items", {}).get(item_id, {}).get("kind", "") in ["heal", "mp"]:
			_button(content_box, "%s ×%d" % [catalog.items[item_id].get("name", item_id), int(character.inventory[item_id])], func(): _battle_intent(battle, "item", {"item_id": item_id}))
	_button(content_box, "Bắt linh thú", func(): _battle_intent(battle, "capture"))
	_button(content_box, "Trở về trận đấu", _close_menu)

func _confirm_target() -> void:
	var battle = character.get("battle")
	if not battle is Dictionary: return
	var action := selected_action.duplicate()
	var choice := str(action.get("choice", "attack"))
	action.erase("choice")
	_battle_intent(battle, choice, action)

func _pet_portrait(species_id: String) -> void:
	var sprite: Texture2D = reference_art.pet_texture(species_id, 0)
	if sprite == null:
		return
	var portrait := TextureRect.new()
	portrait.texture = sprite
	portrait.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	portrait.custom_minimum_size = Vector2(90, 90)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	content_box.add_child(portrait)

func _battle_intent(battle: Dictionary, choice: String, extra: Dictionary = {}) -> void:
	if not pending.is_empty(): return
	var data := {"battle_id": battle.id, "turn": int(battle.turn), "choice": choice}
	data.merge(extra)
	selected_action.clear()
	_close_menu()
	_intent("battle.action", data)

func _show_lineage(node: Dictionary) -> void:
	var popup := AcceptDialog.new()
	popup.title = "Companion lineage"
	popup.dialog_text = _lineage_text(node, 0)
	add_child(popup)
	popup.popup_centered(Vector2i(600, 400))
	popup.confirmed.connect(popup.queue_free)
	popup.canceled.connect(popup.queue_free)

func _lineage_text(node: Dictionary, depth: int) -> String:
	if depth > 12: return "…"
	var pet: Dictionary = node.get("pet", {})
	var value := "  ".repeat(depth) + str(pet.get("name", pet.get("species_id", "Unknown"))) + " · generation " + str(pet.get("generation", 0)) + (" (retired)" if pet.get("retired", false) else "") + "\n"
	for parent in node.get("parents", []): value += _lineage_text(parent, depth + 1)
	return value

func _confirm(message: String, op: String, data: Dictionary) -> void:
	var popup := ConfirmationDialog.new()
	popup.title = "Confirm companion action"
	popup.dialog_text = message
	add_child(popup)
	popup.confirmed.connect(func(): _intent(op, data); popup.queue_free())
	popup.canceled.connect(popup.queue_free)
	popup.popup_centered(Vector2i(470, 180))

func _pets() -> Array:
	return character.get("pets", []).filter(func(pet): return not pet.get("retired", false))

func _names(ids: Array, collection: String) -> PackedStringArray:
	var values := PackedStringArray()
	for id in ids: values.append(str(catalog.get(collection, {}).get(id, {}).get("name", id)))
	return values

func _picker(values: Array, placeholder: String) -> OptionButton:
	var picker := OptionButton.new()
	picker.add_item(placeholder)
	picker.set_item_metadata(0, "")
	for value in values:
		var description := str(value.get("name", value.get("id", "?")))
		if value.has("level"):
			description += " · Lv %s · %s · %s★ · #%s" % [value.level, value.get("gender", "?"), value.get("star", 1), str(value.id).get_slice("_pet_", 1)]
		elif value.has("learn_level"):
			description += " · requires Lv " + str(value.learn_level)
		picker.add_item(_display_text(description))
		picker.set_item_metadata(picker.item_count - 1, str(value.id))
	content_box.add_child(picker)
	return picker

func _selected(picker: OptionButton) -> String:
	return str(picker.get_item_metadata(picker.selected)) if picker.selected >= 0 else ""

func _field(placeholder: String, value: String, secret: bool = false) -> LineEdit:
	var field := LineEdit.new()
	field.placeholder_text = placeholder
	field.text = value
	field.secret = secret
	content_box.add_child(field)
	return field

func _heading(value: String, subtitle: String) -> void:
	content_box.add_child(_label(value, 24, MINT))
	_paragraph(subtitle)
	content_box.add_child(HSeparator.new())

func _paragraph(value: String) -> void:
	var label := _label(value, 14, Color("bdced0"))
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	content_box.add_child(label)

func _label(value: String, font_size: int = 16, tint: Color = Color("e5eee9")) -> Label:
	var label := Label.new()
	label.text = _display_text(value)
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", tint)
	return label

func _button(parent: Node, value: String, action: Callable) -> Button:
	var button := Button.new()
	button.text = _display_text(value)
	button.pressed.connect(action)
	parent.add_child(button)
	return button

func _display_text(value: String) -> String:
	# JSON numbers arrive as floats; hide the trailing .0 only in presentation.
	var pattern := RegEx.new()
	pattern.compile("(?<=\\d)\\.0(?=\\D|$)")
	return pattern.sub(value, "", true)

func _stat_list(values: Dictionary) -> String:
	var parts := PackedStringArray()
	for key in values:
		parts.append(str(key).capitalize() + " " + str(values[key]))
	return ", ".join(parts) if not parts.is_empty() else "None"

func _effect_list(unit: Dictionary) -> String:
	var parts := PackedStringArray()
	for effect in unit.get("statuses", []):
		var name: String = str(catalog.get("statuses", {}).get(effect.id, {}).get("name", str(effect.id).capitalize()))
		parts.append("%s · %s turns" % [name, effect.get("remaining", 0)])
	for effect in unit.get("buffs", []):
		parts.append("%s ×%s · %s turns" % [str(effect.get("stat", "Bonus")).capitalize(), effect.get("multiplier", 1), effect.get("remaining", 0)])
	return "  /  ".join(parts) if not parts.is_empty() else "No active effects"

func _notice(value: String) -> void:
	status.text = value
	_append_log(value)

func _append_log(value: String) -> void:
	history.append(value)
	if history.size() > 80: history.pop_front()
	log_text.text = "\n".join(history)
