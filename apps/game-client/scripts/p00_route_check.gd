extends "res://scripts/contact_live_check.gd"

var frames: Array[float] = []
var previews: Array[float] = []
var last_frame := 0
var sample_frames := false
var cycles := 0

func percentile(values: Array[float], fraction: float) -> float:
	if values.is_empty(): return -1
	var ordered := values.duplicate()
	ordered.sort()
	return ordered[mini(ordered.size() - 1, int(ceil(ordered.size() * fraction)) - 1)]

func sample() -> void:
	var now := Time.get_ticks_usec()
	if sample_frames and last_frame > 0: frames.append((now - last_frame) / 1000.0)
	last_frame = now

func run() -> void:
	var seconds := int(OS.get_environment("P00_ROUTE_SECONDS"))
	if seconds <= 0: seconds = 600
	create_timer(seconds + 120).timeout.connect(func(): push_error("P00 route timeout"); quit(1))
	client = root.get_node("PhimondClient")
	var crypto := Crypto.new()
	client.http_register("p00r_" + crypto.generate_random_bytes(6).hex_encode(), crypto.generate_random_bytes(20).hex_encode(), func(ok: bool, _error: String): authenticated = ok; ready_auth = true)
	if not await wait_for(func(): return ready_auth, "registration"): return
	if not authenticated: push_error("Registration failed"); quit(1); return
	print("P00_ROUTE_ACCOUNT ", client.account_id if "account_id" in client else "see authenticated state")
	client.fetch_content(func(_data: Dictionary): pass)
	if not await wait_for(func(): return not client.catalog.is_empty(), "catalog"): return
	client.connect_ws()
	if not await wait_for(func(): return client.is_ws_connected(), "connection"): return
	print("P00_ROUTE_ACCOUNT_ID ", client.state.id)
	while int(client.state.x) < 37:
		if not await command("world.move", {"direction":"right"}): return
	if not await command("world.portal", {"portal_id":"forest_gate"}): return
	while int(client.state.x) < 9:
		if not await command("world.move", {"direction":"right"}): return
	while int(client.state.y) > 10:
		if not await command("world.move", {"direction":"up"}): return
	var scene_started := Time.get_ticks_usec()
	game = load("res://scenes/MainMap.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	await RenderingServer.frame_post_draw
	var warmup_ms := (Time.get_ticks_usec() - scene_started) / 1000.0
	process_frame.connect(sample)
	sample_frames = true
	var start := Time.get_ticks_msec()
	while Time.get_ticks_msec() - start < seconds * 1000:
		for direction in ["left", "up", "right", "down"]:
			game.move_delay = 0
			var before := Vector2(game.room.displayed_x, game.room.displayed_y)
			var revision: int = client.revision
			var input_at := Time.get_ticks_usec()
			game._move(direction)
			if not await wait_for(func(): return Vector2(game.room.displayed_x, game.room.displayed_y).distance_to(before) > 0.001, "visible move preview"): return
			previews.append((Time.get_ticks_usec() - input_at) / 1000.0)
			if not await wait_for(func(): return not client.is_busy(), "move acknowledgement"): return
			if client.revision <= revision: push_error("Route move rejected"); quit(1); return
			await create_timer(0.25).timeout
		cycles += 1
		if cycles % 5 == 0:
			game._open("Companions")
			await create_timer(0.3).timeout
			game._close()
		if cycles % 10 == 0:
			game.held = "right"
			if not await wait_for(func(): return client.has_battle(), "contact"): return
			if not await wait_for(func(): return not game.room.is_animating(), "battle ready"): return
			game._command("flee")
			if not await wait_for(func(): return not client.has_battle() and not client.is_busy() and not game.room.is_animating(), "flee terminal"): return
			while int(client.state.x) > 9:
				if not await command("world.move", {"direction":"left"}): return
			await create_timer(0.3).timeout
		if cycles % 20 == 0: print("P00_ROUTE_PROGRESS cycles=", cycles, " seconds=", (Time.get_ticks_msec() - start) / 1000.0)
	sample_frames = false
	var report := {"account_id":client.state.id, "duration_ms":Time.get_ticks_msec()-start, "cycles":cycles, "frame_samples":frames.size(), "frame_p50_ms":percentile(frames,0.5), "frame_p95_ms":percentile(frames,0.95), "frame_p99_ms":percentile(frames,0.99), "ui_preview_p95_ms":percentile(previews,0.95), "scene_to_first_draw_ms":warmup_ms, "limitations":["Scripted active UI commands, not hardware input latency", "Local renderer with independent-account server load, no 50-actor fan-out", "Scene warmup with existing import/cache; not cold OS asset cache"]}
	print("P00_ROUTE_REPORT ", JSON.stringify(report))
	var output := OS.get_environment("P00_ROUTE_OUTPUT")
	if not output.is_empty():
		var file := FileAccess.open(output,FileAccess.WRITE)
		if file == null: push_error("Cannot write route report"); quit(1); return
		file.store_string(JSON.stringify(report,"  "))
	print("PASS: native sustained route, four directions, menus, contact and terminal return")
	client._socket.close()
	quit()
