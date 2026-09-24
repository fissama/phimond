## Run: Godot --headless --path apps/game-client --script res://scripts/client_protocol_check.gd
extends SceneTree

var client
var delivered := 0
var pending_changes: Array = []
var callbacks: Array = []

func _initialize() -> void:
	call_deferred("run")

func run() -> void:
	client = load("res://scripts/PhimondClient.gd").new()
	root.add_child(client)
	client.set_process(false)
	client.events_received.connect(func(events: Array): delivered += events.size())
	client.action_pending_changed.connect(func(value: bool): pending_changes.append(value))
	var character := {"id":"hero","map_id":"severa","x":2,"y":3,"pets":[],"battle":null}
	client._on_message({"op":"state", "sequence":3, "data":{"character":character,"events":[{"seq":1,"type":"item_gain","message":"Old event"}]}})
	assert(delivered == 0, "Session baseline must not replay stored events")
	var snapshot := {"op":"state", "request_id":"a", "sequence":4, "data":{"character":character,"events":[{"seq":1,"type":"item_gain","message":"Đã mua vật phẩm."}]}}
	client._pending["a"] = 100
	client._on_message(snapshot)
	assert(not client.is_busy() and client.state.y == 3 and delivered == 1)
	client._on_message(snapshot)
	assert(delivered == 1, "Duplicate revision must not replay events")
	client._pending["old"] = 100
	var stale := snapshot.duplicate(true)
	stale.sequence = 3
	stale.request_id = "old"
	stale.data.character.x = 99
	client._on_message(stale)
	assert(not client.is_busy() and client.state.x == 2, "Stale reply acknowledges request without rolling state back")
	client._pending["buy"] = 100
	client._on_message({"op":"error","request_id":"buy","data":{"message":"insufficient gold"}})
	assert(not client.is_busy() and client.last_error == "Không đủ vàng.")
	assert(client.state.x == 2)
	for malformed in [{"sequence":5,"character":{}}, {"sequence":"5","character":snapshot.data.character}, {"sequence":5.5,"character":snapshot.data.character}, {"sequence":5,"character":snapshot.data.character,"events":[42]}, {"sequence":5,"character":snapshot.data.character,"presentation":{"battle_id":"b","completed_battle":{"id":"b","units":null}}}]:
		client._pending["malformed"] = 100
		client._on_message({"op":"state","request_id":"malformed","sequence":malformed.sequence,"data":{"character":malformed.character,"events":malformed.get("events",[]),"presentation":malformed.get("presentation",{})}})
		if not client.is_busy() or client.revision != 4 or client.state.get("x") != 2:
			push_error("Malformed batch must not acknowledge or replace state")
			quit(1); return
	client._pending.erase("malformed")
	client._pending["invalid"] = 100
	client._on_message({"op":"state","request_id":"invalid","sequence":5,"data":{"character":null}})
	assert(client.is_busy() and client.revision == 4, "Malformed snapshot cannot replace authoritative state")
	assert(client._check_timeouts(101))
	assert(not client.is_busy() and not client.is_ws_connected())
	assert(client.state.x == 2 and pending_changes.back() == false)
	client._connecting = true
	client._connection_deadline = 200
	assert(client._check_timeouts(201) and not client._connecting)
	assert(client._begin_http("login", func(ok: bool, message: String): callbacks.append(["first",ok,message])))
	assert(not client._begin_http("register", func(ok: bool, message: String): callbacks.append(["second",ok,message])))
	assert(client._http_kind == "login" and callbacks.size() == 1 and callbacks[0][0] == "second")
	client._on_http_done(HTTPRequest.RESULT_TIMEOUT, 0, PackedStringArray(), PackedByteArray())
	assert(client._http_kind.is_empty() and callbacks.size() == 2 and callbacks[1][0] == "first")
	assert(not callbacks[1][1] and callbacks[1][2].contains("quá lâu"))
	client._pending["never-replay"] = 300
	client.connect_ws()
	assert(not client.is_busy() and not client.is_ws_connected())
	client._socket.close()
	client.queue_free()
	print("PASS: errors clear pending; revision event dedup; stale/malformed snapshots; timeout/disconnect; HTTP overlap; reconnect without replay")
	quit()
