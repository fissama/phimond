extends SceneTree
func _initialize() -> void: call_deferred("run")
func run() -> void:
	var room = load("res://scripts/room.gd").new()
	root.add_child(room)
	room.set_process(false)
	room.set_snapshot({"map_id":"forest", "x":11, "y":10}, {"maps":{"forest":{"width":40,"height":24,"wild_spawns":[{"id":"forest:0","species_id":"snail","x":12,"y":10}]}},"npcs":{}})
	room.preview_move("right")
	room._process(0.12)
	if room.displayed_x >= 11.9:
		push_error("FAIL: movement finishes early then stalls between 180ms steps")
		quit(1); return
	if not room.has_method("contact_spawn"):
		push_error("FAIL: visible creatures have no contact detection")
		quit(1); return
	assert(room.contact_spawn(Vector2i(12,10)).get("id") == "forest:0")
	assert(room.contact_spawn(Vector2i(12,14)).is_empty())
	room.set_snapshot({"map_id":"severa", "x":6, "y":12}, {"maps":{"severa":{"width":40,"height":24,"wild_spawns":null}},"npcs":{}})
	var empty: Variant = room.contact_spawn(Vector2i(6,12))
	if not empty is Dictionary or not empty.is_empty():
		push_error("A map with null wild_spawns must be an empty encounter list")
		quit(1); return
	print("PASS: continuous step interpolation and matching 2D contact hitbox")
	quit()
