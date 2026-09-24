## Replays sanitized Go-engine test evidence through the real client/renderer.
## These are seeded fixtures, not live progression or a multiplayer load test.
extends SceneTree

func _initialize() -> void: call_deferred("run")

func run() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() != 2:
		push_error("Expected wire fixture directory and screenshot output directory")
		quit(1); return
	var client = root.get_node("PhimondClient")
	client.set_process(false)
	var data := ProjectSettings.globalize_path("res://../../data")
	for key in ["maps", "npcs", "skills", "items", "quests", "recipes"]:
		client.catalog[key] = JSON.parse_string(FileAccess.get_file_as_string(data.path_join(key + "/" + key + ".json")))
	client.catalog.species = JSON.parse_string(FileAccess.get_file_as_string(data.path_join("pets/species.json")))
	var game = load("res://scenes/MainMap.tscn").instantiate()
	root.add_child(game)
	game.set_process(false)
	DirAccess.make_dir_recursive_absolute(args[1])
	for name in ["damage", "heal", "status", "miss", "win", "loss", "capture", "flee"]:
		var fixture: Variant = JSON.parse_string(FileAccess.get_file_as_string(args[0].path_join(name + ".json")))
		if not fixture is Dictionary:
			push_error("Missing Go wire fixture: " + name); quit(1); return
		client.revision = -1
		client._last_event_revision = -1
		client._connected = false
		game.room.reset_presentation()
		client._on_message(fixture.initial)
		client._on_message(fixture.action)
		var expected := str(fixture.expected)
		var target_time: float = game.room.elapsed + 0.1
		if name in ["damage", "heal", "status", "miss"]:
			var found := false
			for effect in game.room._effects:
				if str(effect.type) == expected:
					found = true
					target_time = float(effect.start) + 0.15
					break
			if not found: push_error("Missing effect " + expected); quit(1); return
		else:
			if game.room._battle.get("result") != name or client.has_battle():
				push_error("Terminal projection failed " + name); quit(1); return
		await create_timer(maxf(0.01, target_time - game.room.elapsed)).timeout
		if DisplayServer.get_name() != "headless":
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png(args[1].path_join(name + ".png"))
		print("PASS: public wire ", name, " (seeded Go engine fixture)")
	game.queue_free()
	quit()
