extends SceneTree

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var client = root.get_node("PhimondClient")
	var data := ProjectSettings.globalize_path("res://../../data")
	for key in ["maps", "npcs", "skills", "items", "quests", "recipes"]:
		client.catalog[key] = JSON.parse_string(FileAccess.get_file_as_string(data.path_join(key + "/" + key + ".json")))
	client.catalog.species = JSON.parse_string(FileAccess.get_file_as_string(data.path_join("pets/species.json")))
	var pet := {"id": "audit-pet", "species_id": "snail", "name": "Ốc Sen Hoa", "level": 12, "gender": "female", "star": 1, "generation": 1, "hp": 82, "max_hp": 120, "mp": 32, "max_mp": 45, "skills": ["tackle"], "quality": {}, "growth": {}, "resistances": {}, "status_resistances": {}}
	client.state = {"id": "audit", "name": "Phimond", "map_id": "severa", "x": 8, "y": 12, "level": 12, "gold": 2400, "crystals": 15, "active_pet_id": pet.id, "pets": [pet], "quests": {}, "inventory": {"potion": 4}, "recipes": [], "battle": null}
	client.revision = 1
	var output := "/tmp/phimond-ui-before"
	pet.merge({"attack": 31, "defense": 28, "speed": 17, "magic": 25, "strength": 21, "vitality": 25, "agility": 20, "intelligence": 22})
	if not OS.get_cmdline_user_args().is_empty(): output = OS.get_cmdline_user_args()[0]
	DirAccess.make_dir_recursive_absolute(output)
	var login = load("res://scenes/LoginScreen.tscn").instantiate()
	root.add_child(login)
	await _capture(output + "/login.png")
	login.free()
	var world = load("res://scenes/MainMap.tscn").instantiate()
	root.add_child(world)
	current_scene = world
	await process_frame
	world._on_state_batch(1, client.state, [], {})
	await _capture(output + "/world.png")
	world.npc_id = "trainer"
	world._open("NPC")
	await _capture(output + "/npc.png")
	for page in ["Companions", "Inventory", "Quests", "Ranch"]:
		world._open(page)
		await _capture(output + "/" + page.to_lower() + ".png")
	world.free()
	client.state.battle = {"id": "audit-battle", "turn": 3, "phase": "active", "units": [{"id": "audit-pet", "species_id": "snail", "name": "Ốc Sen Hoa", "side": "player", "hp": 82, "max_hp": 120, "mp": 32, "max_mp": 45, "statuses": []}, {"id": "audit-enemy", "species_id": "mushroom", "name": "Nấm Hoa", "side": "enemy", "hp": 46, "max_hp": 90, "mp": 18, "max_mp": 24, "statuses": []}]}
	var battle = load("res://scenes/BattleScene.tscn").instantiate()
	root.add_child(battle)
	current_scene = battle
	await _capture(output + "/battle.png")
	battle.free()
	print("VISUAL_AUDIT: captured login, world, NPC and battle to ", output)
	quit()

func _capture(path: String) -> void:
	await create_timer(0.5).timeout
	if DisplayServer.get_name() != "headless":
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(path)
