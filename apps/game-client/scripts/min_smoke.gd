extends SceneTree
## Live smoke for the minimal client.
## Run: godot --headless --path apps/game-client --script res://scripts/min_smoke.gd

var _pc: Node
var _received := 0
var _phase: int = 0  # 0=boot, 1=waiting auth, 2=waiting content, 3=waiting state, 4=done
var _phase_clock: float = 0.0
var _kicked: bool = false

func _initialize() -> void:
	print("[min_smoke] start")
	_pc = load("res://scripts/PhimondClient.gd").new()
	root.add_child(_pc)
	_pc.state_updated.connect(_on_state)
	_pc.log_message.connect(func(t): print("[evt] ", t))

func _kick() -> void:
	if _kicked: return
	_kicked = true
	print("[min_smoke] kicking register")
	_pc.http_register("minsmoke_" + str(Time.get_ticks_msec()), "minsmokepass1234", _on_auth)
	_phase = 1

func _on_auth(ok: bool, msg: String) -> void:
	if not ok:
		print("[min_smoke] auth FAILED: ", msg); quit(1); return
	print("[min_smoke] auth OK, fetching catalog…")
	_pc.fetch_content(_on_content)
	_phase = 2

func _on_content(_c: Dictionary) -> void:
	print("[min_smoke] catalog loaded, items=", _pc.catalog.get("items", {}).size(),
		" npcs=", _pc.catalog.get("npcs", {}).size(),
		" maps=", _pc.catalog.get("maps", {}).size())
	_pc.connect_ws()
	_phase = 3

func _on_state(_rev: int, _c: Dictionary) -> void:
	_received += 1
	print("[min_smoke] state_updated #", _received, " rev=", _rev, " x=", _pc.state.get("x"))

func _process(delta: float) -> bool:
	_phase_clock += delta
	if not _kicked and _phase_clock > 0.2:
		_kick()
	if _phase == 3 and _phase_clock > 1.5 and _pc.state.size() > 0:
		print("[min_smoke] initial state: x=", _pc.state.get("x"),
			" map=", _pc.state.get("map_id"),
			" pets=", (_pc.state.get("pets", []) as Array).size())
		_pc.world_move("right")
		_phase = 4
	elif _phase == 4 and _phase_clock > 2.7:
		print("[min_smoke] after move: x=", _pc.state.get("x"),
			" map=", _pc.state.get("map_id"),
			" revision=", _pc.revision,
			" state_updates_seen=", _received)
		var pass_ok: bool = _pc.revision >= 1 and int(_pc.state.get("x", 0)) >= 6
		print("[min_smoke] DONE — overall ", "PASS" if pass_ok else "FAIL")
		quit(0 if pass_ok else 1)
		return true
	return false