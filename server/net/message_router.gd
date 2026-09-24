extends Node
##
## Parses inbound client JSON and dispatches to the right handler.
## Stateless — all state lives in WS_Server (clients[]) and World (players).
##

const VALID_DIRS: Array = ["up", "down", "left", "right"]

var NAME_RE: RegEx

var server: Node
var world: Node


func _init(p_server: Node, p_world: Node) -> void:
	server = p_server
	world = p_world
	NAME_RE = RegEx.new()
	NAME_RE.compile("^[a-zA-Z0-9_]{1,16}$")


func handle(client_id: int, text: String) -> void:
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		_send_error(client_id, "Invalid JSON")
		return
	var msg: Dictionary = parsed
	var msg_type: String = msg.get("type", "")
	if msg_type == "":
		_send_error(client_id, "Missing type field")
		return
	if not _is_hello_done(client_id) and msg_type != "HELLO":
		_send_error(client_id, "Send HELLO before any other message")
		return
	match msg_type:
		"HELLO":
			_handle_hello(client_id, msg)
		"MOVE":
			_handle_move(client_id, msg)
		"ACTION":
			_handle_action(client_id, msg)
		"BYE":
			# Client signals clean shutdown. Free its slot immediately so a
			# follow-up HELLO with the same name can re-register.
			server.force_disconnect(client_id)
		_:
			_send_error(client_id, "Unknown message type: %s" % msg_type)


# --- Handlers ---------------------------------------------------------------

func _handle_hello(client_id: int, msg: Dictionary) -> void:
	var name: String = String(msg.get("name", "")).strip_edges()
	if name == "":
		_send_error(client_id, "Missing name")
		return
	if NAME_RE.search(name) == null:
		_send_error(client_id, "Invalid name (1-16 alphanumeric/underscore)")
		return
	var entry: Dictionary = server.clients.get(client_id, {})
	if entry.is_empty():
		return
	if entry.get("hello", false):
		_send_error(client_id, "Already said hello")
		return
	if world.player_exists(name):
		_send_error(client_id, "Name already taken")
		return
	entry["player_name"] = name
	entry["hello"] = true
	server.clients[client_id] = entry
	world.add_player(name, 10, 7, "down")
	print("[Router] HELLO id=%d name=%s" % [client_id, name])
	_broadcast_state()


func _handle_move(client_id: int, msg: Dictionary) -> void:
	var entry: Dictionary = server.clients.get(client_id, {})
	if entry.is_empty() or not entry.get("hello", false):
		_send_error(client_id, "Send HELLO first")
		return
	var dir: String = String(msg.get("dir", ""))
	if not VALID_DIRS.has(dir):
		_send_error(client_id, "Invalid direction: %s" % dir)
		return
	var name: String = entry["player_name"]
	var result: Dictionary = world.move_player(name, dir)
	if not result.get("moved", false):
		return

	# Position changed → broadcast state (everyone sees the new position).
	_broadcast_state()

	# Encounter triggered → start a battle for this client only.
	var enc: Dictionary = result.get("encounter", {})
	if not enc.is_empty():
		var p: Dictionary = world.players[name]
		var msg_protocol = preload("res://net/protocol.gd")
		var inventory: Array = _inventory_to_array(p.get("inventory", {}))
		var skills_detail: Array = _skills_to_detail(p["monster"].get("skills", []))
		var items_detail: Array = _items_to_detail(p.get("inventory", {}))
		var start_payload: String = msg_protocol.make_battle_start(
			p["wild_monster"],
			p["monster"],
			inventory,
			skills_detail,
			items_detail
		)
		server.send(client_id, start_payload)
		print("[Router] BATTLE_START → %s vs wild %s (skills=%d items=%d)" % [
			name,
			p["wild_monster"]["name"],
			skills_detail.size(),
			items_detail.size(),
		])


func _handle_action(client_id: int, msg: Dictionary) -> void:
	var entry: Dictionary = server.clients.get(client_id, {})
	if entry.is_empty() or not entry.get("hello", false):
		_send_error(client_id, "Send HELLO first")
		return
	var name: String = entry["player_name"]
	var events: Array = world.apply_action(name, msg)
	if events.is_empty():
		# Not in battle, or action rejected. Stay quiet — client should
		# already be in WorldScene if battle ended.
		return

	var msg_protocol = preload("res://net/protocol.gd")
	var p: Dictionary = world.players[name]
	var battle: Node = p["battle"]
	var awaiting: bool = not battle.is_finished()
	server.send(client_id, msg_protocol.make_battle_turn(events, awaiting))

	if battle.is_finished():
		var result: String = battle.get_result()
		var xp: int = battle.xp_gained
		server.send(client_id, msg_protocol.make_battle_end(result, xp))
		world.end_battle(name)
		# Persist post-battle state — monster level/xp changes are the most
		# important progression milestones, so snapshot now.
		world.save_player(name)
		# Broadcast state so other clients see this player back in the world.
		_broadcast_state()
		print("[Router] BATTLE_END → %s result=%s xp=%d" % [name, result, xp])


# --- Helpers ----------------------------------------------------------------

func _is_hello_done(client_id: int) -> bool:
	var entry: Dictionary = server.clients.get(client_id, {})
	return entry.get("hello", false)


func _send_error(client_id: int, message: String) -> void:
	server.send(client_id, preload("res://net/protocol.gd").make_error(message))


func _broadcast_state() -> void:
	if not is_instance_valid(world):
		return
	server.broadcast(preload("res://net/protocol.gd").make_state(world.get_players_snapshot()))


func _inventory_to_array(inv: Dictionary) -> Array:
	var out: Array = []
	for id in inv.keys():
		var qty: int = int(inv[id])
		if qty > 0:
			out.append({"id": id, "qty": qty})
	return out


# Build the per-skill metadata array for BATTLE_START so the client can render
# the SkillPicker without needing its own copy of skills.json.
func _skills_to_detail(skill_ids: Array) -> Array:
	var out: Array = []
	for sid in skill_ids:
		var s: Dictionary = world.game_data.get_skill(sid)
		if s.is_empty():
			continue
		out.append({
			"id":     sid,
			"name":   s.get("name", sid),
			"kind":   s.get("kind", "physical"),
			"power":  int(s.get("power", 0)),
		})
	return out


# Same idea for items — adds the human-readable name so the ItemPicker can
# show "Potion ×3" instead of just an id.
func _items_to_detail(inv: Dictionary) -> Array:
	var out: Array = []
	for id in inv.keys():
		var qty: int = int(inv[id])
		if qty <= 0:
			continue
		var it: Dictionary = world.game_data.get_item(id)
		out.append({
			"id":   id,
			"name": it.get("name", id),
			"qty":  qty,
		})
	return out
