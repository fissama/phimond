extends Node
## PhimondClient — autoload singleton.
## WebSocket state container + HTTP helper + intent dispatcher.
## Other scenes access it as `PhimondClient`.

signal state_updated(revision: int, character: Dictionary)
signal connection_changed(connected: bool)
signal log_message(text: String)
signal action_pending_changed(pending: bool)
signal events_received(events: Array)
signal state_batch_received(revision: int, character: Dictionary, events: Array, presentation: Dictionary)

var BASE_URL: String = OS.get_environment("GAME_API_URL").trim_suffix("/") if not OS.get_environment("GAME_API_URL").is_empty() else "http://127.0.0.1:8090"
var WS_URL: String = BASE_URL.replace("https://", "wss://").replace("http://", "ws://") + "/ws"

var token: String = ""
var state: Dictionary = {}
var catalog: Dictionary = {}
var revision: int = -1
var last_error: String = ""

var _socket := WebSocketPeer.new()
var _http := HTTPRequest.new()
var _http_kind: String = ""
var _http_callback: Callable = Callable()
var _connected: bool = false
var _auth_sent: bool = false
var _counter: int = 0
var _session_prefix: String = str(Time.get_unix_time_from_system()) + "-" + str(randi())
var _pending: Dictionary = {}
var _connecting := false
var _connection_deadline := 0
var _last_event_revision := -1
const RESPONSE_TIMEOUT_MS := 15000

func _ready() -> void:
	add_child(_http)
	_http.timeout = 15
	_http.request_completed.connect(_on_http_done)

# ---------- HTTP ----------

func http_register(username: String, password: String, cb: Callable) -> void:
	if not _begin_http("register", cb): return
	var err := _http.request(
		BASE_URL + "/api/register",
		PackedStringArray(["Content-Type: application/json"]),
		HTTPClient.METHOD_POST,
		JSON.stringify({"username": username, "password": password})
	)
	if err != OK:
		_http_failure("Không thể kết nối máy chủ.")

func http_login(username: String, password: String, cb: Callable) -> void:
	if not _begin_http("login", cb): return
	var err := _http.request(
		BASE_URL + "/api/login",
		PackedStringArray(["Content-Type: application/json"]),
		HTTPClient.METHOD_POST,
		JSON.stringify({"username": username, "password": password})
	)
	if err != OK:
		_http_failure("Không thể kết nối máy chủ.")

func fetch_content(cb: Callable) -> void:
	if not _begin_http("content", cb): return
	var headers := PackedStringArray()
	if not token.is_empty():
		headers.append("Authorization: Bearer " + token)
	var err := _http.request(BASE_URL + "/api/content", headers, HTTPClient.METHOD_GET, "")
	if err != OK:
		_http_failure("Không thể tải dữ liệu trò chơi.")

func _begin_http(kind: String, cb: Callable) -> bool:
	if not _http_kind.is_empty():
		if cb.is_valid():
			if kind == "content": cb.call({})
			else: cb.call(false, "Đang xử lý yêu cầu trước, vui lòng chờ.")
		return false
	_http_kind = kind
	_http_callback = cb
	return true

func _http_failure(message: String) -> void:
	var kind := _http_kind
	var cb := _http_callback
	_http_kind = ""
	_http_callback = Callable()
	last_error = message
	log_message.emit(message)
	if cb.is_valid():
		if kind == "content": cb.call({})
		else: cb.call(false, message)

func _on_http_done(result: int, code: int, _h: PackedStringArray, bytes: PackedByteArray) -> void:
	if result != HTTPRequest.RESULT_SUCCESS or code < 200 or code >= 300:
		push_warning("HTTP request failed: result=%s status=%s" % [result, code])
		var message := "Không thể kết nối máy chủ. Vui lòng thử lại."
		if result == HTTPRequest.RESULT_TIMEOUT: message = "Máy chủ phản hồi quá lâu. Vui lòng thử lại."
		elif code == 401: message = "Tên đăng nhập hoặc mật khẩu không đúng."
		elif code == 409: message = "Tên đăng nhập đã được sử dụng."
		elif code == 400: message = "Thông tin đăng ký chưa hợp lệ."
		_http_failure(message)
		return
	var parsed: Variant = JSON.parse_string(bytes.get_string_from_utf8())
	if not parsed is Dictionary:
		_http_failure("Phản hồi máy chủ không hợp lệ. Vui lòng thử lại.")
		return
	var kind := _http_kind
	var cb := _http_callback
	_http_kind = ""
	_http_callback = Callable()
	if kind == "register" or kind == "login":
		var next_token := str(parsed.get("token", ""))
		if next_token.is_empty():
			if cb.is_valid(): cb.call(false, "Máy chủ chưa cấp phiên đăng nhập. Vui lòng thử lại.")
			return
		if token != next_token:
			revision = -1
			_last_event_revision = -1
		token = next_token
		if cb.is_valid(): cb.call(true, "")
	elif kind == "content":
		catalog = parsed
		if cb.is_valid(): cb.call(parsed)

# ---------- WebSocket ----------

func connect_ws() -> void:
	_socket.close()
	_socket = WebSocketPeer.new()
	_clear_pending()
	_auth_sent = false
	_connected = false
	_connecting = true
	_connection_deadline = Time.get_ticks_msec() + RESPONSE_TIMEOUT_MS
	connection_changed.emit(false)
	log_message.emit("Đang kết nối máy chủ…")
	if _socket.connect_to_url(WS_URL) != OK:
		_disconnect("Không thể kết nối máy chủ. Vui lòng kết nối lại.")
	set_process(true)

func _process(_delta: float) -> void:
	if _check_timeouts(Time.get_ticks_msec()):
		return
	_socket.poll()
	var ws_state := _socket.get_ready_state()
	if ws_state == WebSocketPeer.STATE_OPEN:
		if not _auth_sent:
			_auth_sent = true
			send_text_raw({"op": "auth.session", "request_id": _new_id(), "data": {"token": token}})
		while _socket.get_available_packet_count() > 0:
			var raw := _socket.get_packet().get_string_from_utf8()
			var env: Variant = JSON.parse_string(raw)
			if env is Dictionary:
				_on_message(env)
	elif ws_state == WebSocketPeer.STATE_CLOSING or ws_state == WebSocketPeer.STATE_CLOSED:
		if _connecting or _connected or _auth_sent:
			_disconnect("Mất kết nối máy chủ. Vui lòng kết nối lại.")
	else:
		# CONNECTING — keep polling
		pass

func _on_message(env: Dictionary) -> void:
	var op := str(env.get("op", ""))
	var request_id := str(env.get("request_id", ""))
	var data_value: Variant = env.get("data", {})
	if not data_value is Dictionary: return
	var data: Dictionary = data_value
	if op == "error":
		if request_id.is_empty(): _clear_pending()
		else: _finish_pending(request_id)
		var raw_error := str(data.get("message", ""))
		# Redact even unexpected server diagnostics; never print a session token.
		push_warning("Server rejected action: " + (raw_error.replace(token, "[redacted]") if not token.is_empty() else raw_error))
		last_error = _friendly_error(raw_error)
		log_message.emit(last_error)
		return
	if op != "state":
		return
	if not _valid_state_batch(env): return
	var seq := int(env.sequence)
	var raw_char: Variant = data.get("character")
	if not raw_char is Dictionary or seq < 0: return
	_finish_pending(request_id)
	if seq < revision:
		return
	var resuming := not _connected
	# Defensive: state must always be a Dictionary so callers can safely .get()
	if not _connected:
		_connected = true
		_connecting = false
		connection_changed.emit(true)
		log_message.emit("Đã kết nối máy chủ.")
	revision = seq
	state = raw_char
	last_error = ""
	var events: Array = []
	var presentation: Dictionary = {}
	if not resuming and seq > _last_event_revision:
		if data.get("events") is Array:
			for event in data.events:
				if event is Dictionary: events.append(event)
		if data.get("presentation") is Dictionary: presentation = data.presentation
	state_batch_received.emit(revision, state, events, presentation)
	state_updated.emit(revision, state)
	if seq <= _last_event_revision: return
	_last_event_revision = seq
	events_received.emit(events)
	for ev in events:
		var message := _event_message(ev)
		if not message.is_empty(): log_message.emit(message)

# Validate before acknowledging: malformed packets must time out/resync rather
# than unlock input or replace the last usable authoritative state.
func _wire_integer(value: Variant) -> bool:
	return (value is int or value is float) and is_finite(float(value)) and float(value) == floor(float(value)) and absf(float(value)) <= 9007199254740991.0

func _wire_id(value: Variant) -> bool:
	return value is String and not value.is_empty()

func _valid_battle(value: Variant) -> bool:
	if not value is Dictionary or not _wire_id(value.get("id")): return false
	if not _wire_integer(value.get("turn")) or int(value.turn) < 1: return false
	if not value.get("units") is Array or value.units.is_empty(): return false
	for unit in value.units:
		if not unit is Dictionary or not _wire_id(unit.get("id")) or not _wire_id(unit.get("species_id")): return false
		if unit.get("side") not in ["player", "enemy"]: return false
		for key in ["hp", "max_hp"]:
			if not _wire_integer(unit.get(key)) or int(unit[key]) < 0: return false
		for key in ["mp", "max_mp"]:
			if unit.has(key) and not _wire_integer(unit[key]): return false
		for key in ["statuses", "buffs"]:
			if unit.has(key):
				if not unit[key] is Array: return false
				for entry in unit[key]:
					if not entry is Dictionary: return false
	return true

func _valid_state_batch(env: Dictionary) -> bool:
	if not _wire_integer(env.get("sequence")) or int(env.sequence) < 0: return false
	var data: Dictionary = env.get("data", {})
	var character: Variant = data.get("character")
	if not character is Dictionary or not _wire_id(character.get("id")) or not _wire_id(character.get("map_id")): return false
	if not _wire_integer(character.get("x")) or not _wire_integer(character.get("y")): return false
	if not character.get("pets") is Array: return false
	for pet in character.pets:
		if not pet is Dictionary or not _wire_id(pet.get("id")) or not _wire_id(pet.get("species_id")): return false
	for key in ["inventory", "quests"]:
		if character.has(key) and not character[key] is Dictionary: return false
	if character.has("recipes") and not character.recipes is Array: return false
	var battle: Variant = character.get("battle")
	if battle != null and not _valid_battle(battle): return false
	var events: Variant = data.get("events")
	if events != null:
		if not events is Array: return false
		for event in events:
			if not event is Dictionary or not _wire_id(event.get("type")): return false
			for key in ["seq", "amount"]:
				if event.has(key) and not _wire_integer(event[key]): return false
			for key in ["actor_id", "target_id", "message"]:
				if event.has(key) and not event[key] is String: return false
	var presentation: Variant = data.get("presentation")
	if presentation != null:
		if not presentation is Dictionary: return false
		if not presentation.is_empty() and not _wire_id(presentation.get("battle_id")): return false
		var completed: Variant = presentation.get("completed_battle")
		if completed != null:
			if battle != null or not _valid_battle(completed) or completed.id != presentation.battle_id: return false
	return true

func _event_message(event: Dictionary) -> String:
	var kind := str(event.get("type", ""))
	var message := str(event.get("message", ""))
	match kind:
		"map_enter": return "Đã đến " + message + "."
		"quest_accept": return "Đã nhận nhiệm vụ: " + message
		"quest_complete": return "Hoàn thành nhiệm vụ: " + message
		"damage": return "Mục tiêu nhận %d sát thương." % int(event.get("amount", 0))
		"heal": return "Hồi phục %d sinh lực." % int(event.get("amount", 0))
	var labels := {
		"npc_dialogue":"Mỗi linh thú mang câu chuyện của những thế hệ tổ tiên.",
		"pet_appraise":"Đã giám định tiềm năng thú cưng.", "pet_activate":"Đã đổi thú cưng xuất chiến.",
		"pet_learn":"Thú cưng đã học kỹ năng.", "pet_release":"Đã thả thú cưng; phả hệ vẫn được lưu giữ.",
		"pet_strengthen":"Đã cường hóa thú cưng.", "recipe_learn":"Đã học công thức lai tạo.",
		"pet_heal":"Các thú cưng đã được hồi phục.", "item_gain":"Đã nhận vật phẩm.",
		"currency_spend":"Đã thanh toán vàng.", "currency_gain":"Đã nhận phần thưởng.",
		"pet_breed":"Lai tạo thành công; tổ tiên được lưu trong phả hệ.", "item_spend":"Đã sử dụng vật phẩm.",
		"battle_start":"Trận đấu bắt đầu!", "battle_flee":"Đã rút lui khỏi trận đấu.",
		"action_blocked":"Không thể thực hiện hành động này.", "pet_capture":"Đã bắt thú cưng! Hãy đến người giám định.",
		"capture_failed":"Thú cưng đã thoát khỏi phong ấn.", "defend":"Đang phòng thủ.",
		"status_fatal":"Thú cưng gục ngã do hiệu ứng bất lợi.", "status_expired":"Hiệu ứng đã kết thúc.",
		"battle_win":"Chiến thắng!", "battle_loss":"Thất bại. Hãy hồi phục và thử lại.",
		"skill_cast":"Đã thi triển kỹ năng.", "miss":"Đòn đánh trượt mục tiêu.",
		"status_cleansed":"Đã giải trừ hiệu ứng bất lợi.", "status_resisted":"Đã kháng hiệu ứng.",
		"status_applied":"Mục tiêu chịu hiệu ứng bất lợi.", "buff_applied":"Đã nhận hiệu ứng hỗ trợ."
	}
	return str(labels.get(kind, ""))

func _finish_pending(request_id: String) -> void:
	if _pending.erase(request_id): action_pending_changed.emit(is_busy())

func _clear_pending() -> void:
	if _pending.is_empty(): return
	_pending.clear()
	action_pending_changed.emit(false)

func _disconnect(message: String) -> void:
	_socket.close()
	_auth_sent = false
	_connected = false
	_connecting = false
	_clear_pending()
	connection_changed.emit(false)
	last_error = message
	log_message.emit(message)

func _check_timeouts(now: int) -> bool:
	if _connecting and now >= _connection_deadline:
		_disconnect("Kết nối quá lâu. Vui lòng kết nối lại.")
		return true
	for deadline in _pending.values():
		if now >= int(deadline):
			# An acknowledgement may have been lost: require a fresh snapshot,
			# never automatically replay a purchase, battle turn, or other intent.
			_disconnect("Chưa nhận được kết quả. Hãy kết nối lại để cập nhật trạng thái.")
			return true
	return false

func _friendly_error(message: String) -> String:
	match message:
		"insufficient gold": return "Không đủ vàng."
		"finish your battle first": return "Hãy hoàn thành trận đấu trước."
		"use a portal at the map edge": return "Bạn đã đến rìa bản đồ. Hãy tìm cổng dịch chuyển."
		"NPC is not nearby": return "Hãy đến gần nhân vật để trò chuyện."
		"no nearby portal": return "Không có cổng dịch chuyển ở gần."
		"wild beast is not nearby": return "Hãy đến gần linh thú để bắt đầu trận đấu."
		"heal your active beast before battle": return "Linh thú đã kiệt sức. Hãy hồi phục trước khi chiến đấu."
		"slow down": return "Thao tác quá nhanh. Vui lòng chờ một chút."
		"quest is not ready for reward": return "Nhiệm vụ chưa hoàn thành."
		"already appraised": return "Thú cưng đã được giám định."
		"switch active pet before releasing": return "Hãy đổi thú cưng xuất chiến trước khi thả."
	return "Chưa thể thực hiện thao tác này. Hãy kiểm tra điều kiện và thử lại."

func _new_id() -> String:
	_counter += 1
	return _session_prefix + "-" + str(_counter)

func send_text_raw(envelope: Dictionary) -> void:
	if _socket.get_ready_state() != WebSocketPeer.STATE_OPEN:
		return
	if _socket.send_text(JSON.stringify(envelope)) != OK:
		_disconnect("Không thể gửi yêu cầu. Vui lòng kết nối lại.")

# ---------- Intent helpers ----------

func send(op: String, data: Dictionary) -> void:
	if not _connected or _socket.get_ready_state() != WebSocketPeer.STATE_OPEN:
		log_message.emit("Chưa kết nối máy chủ. Vui lòng kết nối lại.")
		return
	if is_busy():
		log_message.emit("Đang chờ kết quả thao tác trước…")
		return
	var request_id := _new_id()
	_pending[request_id] = Time.get_ticks_msec() + RESPONSE_TIMEOUT_MS
	action_pending_changed.emit(true)
	send_text_raw({"op": op, "request_id": request_id, "data": data})

func world_move(direction: String) -> void: send("world.move", {"direction": direction})
func world_portal(portal_id: String) -> void: send("world.portal", {"portal_id": portal_id})
func encounter(spawn_id: String = "") -> void:
	send("world.encounter", {} if spawn_id.is_empty() else {"spawn_id": spawn_id})
func interact_npc(npc_id: String) -> void: send("npc.interact", {"npc_id": npc_id})
func battle_action(battle_id: String, turn: int, choice: String, skill_id: String = "", item_id: String = "") -> void:
	var d := {"battle_id": battle_id, "turn": turn, "choice": choice}
	if not skill_id.is_empty(): d["skill_id"] = skill_id
	if not item_id.is_empty(): d["item_id"] = item_id
	send("battle.action", d)
func buy(item_id: String, qty: int) -> void: send("shop.buy", {"item_id": item_id, "quantity": qty})
func appraise(pet_id: String) -> void: send("pet.appraise", {"pet_id": pet_id})
func activate(pet_id: String) -> void: send("pet.activate", {"pet_id": pet_id})
func synthesize(parent_a: String, parent_b: String, recipe_id: String, blessing: bool) -> void:
	send("breeding.synthesize", {"parent_a": parent_a, "parent_b": parent_b, "recipe_id": recipe_id, "blessing": 1 if blessing else 0})
func accept_quest(id: String) -> void: send("quest.accept", {"quest_id": id})
func claim_quest(id: String) -> void: send("quest.claim", {"quest_id": id})
func learn_recipe(id: String) -> void: send("recipe.learn", {"recipe_id": id})
func heal_pets() -> void: send("pet.heal", {})
func challenge_arena() -> void: send("arena.challenge", {})
func release_pet(pet_id: String) -> void: send("pet.release", {"pet_id": pet_id})
func pet_learn(pet_id: String, skill_id: String) -> void: send("pet.learn", {"pet_id": pet_id, "skill_id": skill_id})
func strengthen(pet_id: String, donor_id: String) -> void: send("pet.strengthen", {"pet_id": pet_id, "donor_id": donor_id})

func is_ws_connected() -> bool: return _connected
func is_busy() -> bool: return not _pending.is_empty()
func has_battle() -> bool: return state.get("battle") is Dictionary
