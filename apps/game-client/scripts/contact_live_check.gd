extends SceneTree
var client: Node
var game: Control
var ready_auth := false
var authenticated := false

func _initialize() -> void: call_deferred("run")

func wait_for(check: Callable, label: String, seconds: float = 20) -> bool:
	var deadline := Time.get_ticks_msec() + int(seconds * 1000)
	while not check.call():
		if Time.get_ticks_msec() > deadline:
			push_error("FAIL: " + label)
			quit(1); return false
		await create_timer(0.01).timeout
	return true

func command(op: String, data: Dictionary) -> bool:
	var previous: int = client.revision
	client.send(op, data)
	if not await wait_for(func(): return not client.is_busy(), op): return false
	if client.revision <= previous:
		push_error("Rejected " + op + ": " + client.last_error)
		quit(1); return false
	return true

func run() -> void:
	client = root.get_node("PhimondClient")
	var crypto := Crypto.new()
	client.http_register("contact_" + crypto.generate_random_bytes(6).hex_encode(), crypto.generate_random_bytes(20).hex_encode(), func(ok: bool, _error: String): authenticated = ok; ready_auth = true)
	if not await wait_for(func(): return ready_auth, "registration"): return
	if not authenticated: push_error("Registration rejected"); quit(1); return
	client.fetch_content(func(_data: Dictionary): pass)
	if not await wait_for(func(): return not client.catalog.is_empty(), "catalog"): return
	assert(client.catalog.maps.forest.has("wild_spawns"), "Restart server to load contact catalog")
	client.connect_ws()
	if not await wait_for(func(): return client.is_ws_connected(), "connection"): return
	while int(client.state.x) < 37:
		if not await command("world.move", {"direction":"right"}): return
	if not await command("world.portal", {"portal_id":"forest_gate"}): return
	while int(client.state.x) < 9:
		if not await command("world.move", {"direction":"right"}): return
	while int(client.state.y) > 10:
		if not await command("world.move", {"direction":"up"}): return
	game = load("res://scenes/MainMap.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	var frame_times: Array[float] = []
	var last_frame := Time.get_ticks_usec()
	for i in range(120):
		await process_frame
		var now := Time.get_ticks_usec()
		frame_times.append((now - last_frame) / 1000.0)
		last_frame = now
	frame_times.sort()
	print("Native frame cadence ms: median=", snappedf(frame_times[60], 0.01), " p95=", snappedf(frame_times[114], 0.01))
	if "--play" in OS.get_cmdline_user_args():
		print("PLAYTEST READY: forest (9,10), walk right into Flower Snail or click it.")
		client.state_updated.connect(func(_revision: int, state: Dictionary):
			if state.get("battle") is Dictionary: print("PLAYTEST COMBAT: ", state.battle.units[1].species_id, " turn ", state.battle.turn)
			else: print("PLAYTEST FIELD: ", state.x, ",", state.y))
		return
	game.held = "right"
	if not await wait_for(func(): return client.has_battle(), "walking into creature enters combat"): return
	assert(client.state.battle.units[1].species_id == "snail")
	assert(game.held.is_empty() and game.destination.is_empty())
	await create_timer(0.3).timeout
	game._command("attack")
	game._confirm_target()
	if not await wait_for(func(): return not client.is_busy(), "attack"): return
	await create_timer(2.5).timeout
	game._command("flee")
	if not await wait_for(func(): return not client.has_battle(), "flee"): return
	await create_timer(2.5).timeout
	assert(not client.has_battle(), "Standing on contact after battle must not retrigger")
	game.held = "left"
	if not await wait_for(func(): return int(client.state.x) <= 9, "leave contact"): return
	game.held = ""
	game._approach("enemy", "forest:0")
	if not await wait_for(func(): return client.has_battle(), "click approaches and encounters same creature"): return
	assert(client.state.battle.units[1].species_id == "snail")
	print("PASS: walk contact -> correct species -> attack -> flee -> no standing retrigger -> click approach -> same species")
	client._socket.close()
	quit()
