extends SceneTree

# Run with --script res://scripts/smoke.gd -- /absolute/path/to/data
func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var client = load("res://main.tscn").instantiate()
	root.add_child(client)
	await process_frame
	var args := OS.get_cmdline_user_args()
	if args.is_empty():
		push_error("Pass the repository data directory after --")
		quit(1)
		return
	var sources := {"maps": "maps/maps.json", "npcs": "npcs/npcs.json", "species": "pets/species.json", "skills": "skills/skills.json", "items": "items/items.json", "recipes": "recipes/recipes.json", "quests": "quests/quests.json"}
	for collection in sources:
		client.catalog[collection] = JSON.parse_string(FileAccess.get_file_as_string(args[0].path_join(sources[collection])))
	var pet := {"id": "test-pet", "species_id": "snail", "name": "Mossbud", "level": 12, "gender": "female", "star": 1, "generation": 1, "hp": 25, "max_hp": 30, "mp": 10, "max_mp": 20, "appraised": true, "skills": [client.catalog.skills.keys()[0]], "quality": {"strength": 1.1}, "growth": {"strength": 1.2}, "resistances": {}, "status_resistances": {}, "retired": false}
	var state := {"id": "test-character", "name": "Smoke Traveler", "map_id": "severa", "x": 6, "level": 12, "gold": 200, "crystals": 5, "active_pet_id": pet.id, "pets": [pet], "recipes": [client.catalog.recipes.keys()[0]], "quests": {}, "inventory": {client.catalog.items.keys()[0]: 3}, "arena_tier": 1, "battle": null}
	client._receive(JSON.stringify({"op": "state", "sequence": 7, "data": {"character": state, "events": null}}))
	assert(client.revision == 7)
	for tab in ["Journey", "Companions", "Ranch", "Quests", "Supplies", "Battle"]:
		client.page = tab
		client._render()
		await process_frame
		assert(client.content_box.get_child_count() > 0)
	state.battle = {"id": "battle-1", "turn": 2, "phase": "active", "units": [{"id": pet.id, "species_id": "snail", "name": pet.name, "side": "player", "hp": 25, "max_hp": 30, "mp": 10, "max_mp": 20, "statuses": []}, {"id": "enemy", "species_id": "mushroom", "name": "Forest creature", "side": "enemy", "hp": 15, "max_hp": 40, "mp": 4, "max_mp": 10, "statuses": [{"id": "sleep", "remaining": 2}]}]}
	client._receive(JSON.stringify({"op": "state", "sequence": 8, "data": {"character": state, "events": [{"message": "Test encounter"}]}}))
	assert(client.character.battle.turn == 2)
	var log_size: int = client.history.size()
	client._receive(JSON.stringify({"op": "state", "sequence": 8, "data": {"character": state, "events": [{"message": "Test encounter"}]}}))
	assert(client.history.size() == log_size)
	client._receive(JSON.stringify({"op": "state", "sequence": 6, "data": {"character": {}, "events": []}}))
	assert(client.revision == 8)
	assert(not client.character.is_empty())
	client._receive(JSON.stringify({"op": "error", "data": {"message": "Too far from service"}}))
	assert(client.status.text == "Too far from service")
	assert("Mossbud" in client._lineage_text({"pet": pet, "parents": [{"pet": pet, "parents": []}]}, 0))
	var first: Dictionary = client._envelope("world.move", {"direction": "left"})
	var second: Dictionary = client._envelope("world.move", {"direction": "left"})
	assert(first.request_id != second.request_id)
	assert(first.data == {"direction": "left"})
	assert(first.keys().size() == 3)
	await process_frame
	if "--screenshot" in args and DisplayServer.get_name() != "headless":
		client.status.text = "Fixture preview · Assets from supplied APK · No account connected"
		client.history.clear()
		client._append_log("A forest companion steps into the lantern light.")
		await process_frame
		await RenderingServer.frame_post_draw
		DirAccess.make_dir_recursive_absolute("res://artifacts")
		root.get_texture().get_image().save_png("res://artifacts/first-expedition.png")
	print("PASS: all six panels, battle rendering, stale revision rejection, error feedback, recursive lineage, unique intent envelopes")
	client.queue_free()
	await process_frame
	quit(0)
