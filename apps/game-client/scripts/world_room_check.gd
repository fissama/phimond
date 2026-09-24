## Run with --headless --path apps/game-client --script res://scripts/world_room_check.gd
extends SceneTree
var room
var fixture: Dictionary
func _initialize():
	call_deferred("run")
func run():
	room = load("res://scripts/room.gd").new()
	root.add_child(room)
	room.size = Vector2(960, 440)
	var catalog = {"maps": JSON.parse_string(FileAccess.get_file_as_string("res://../../data/maps/maps.json")), "npcs": JSON.parse_string(FileAccess.get_file_as_string("res://../../data/npcs/npcs.json")), "species": JSON.parse_string(FileAccess.get_file_as_string("res://../../data/pets/species.json"))}
	fixture = {"map_id":"severa", "x":6, "name":"Phileanh", "pets":[{"id":"pet", "species_id":"snail"}], "active_pet_id":"pet"}
	room.set_snapshot(fixture, catalog)
	await process_frame
	assert(room.art.npc_texture("trainer") != null)
	assert(room.art.pet_texture("snail", 0, "attack") != null)
	room.preview_move("right")
	assert(room._preview_x == 7)
	room.cancel_preview()
	assert(room._preview_x == -1)
	room.preview_move("up")
	assert(room._preview_y == 11)
	await create_timer(0.12).timeout
	assert(room.displayed_y < 12, "Vertical input must change rendered position")
	room.cancel_preview()
	assert(room._preview_y == -1)
	fixture["battle"] = {"id":"b1", "units":[{"id":"p1", "name":"Flower Snail", "side":"player", "species_id":"snail", "hp":100,"max_hp":100},{"id":"e1", "name":"Thorn Wolf", "side":"enemy", "species_id":"wolf", "hp":100,"max_hp":100}]}
	room.apply_state_batch(1, fixture.duplicate(true), catalog, [], {"battle_id":"b1"})
	assert(room.selected_target == "e1")
	var events := [{"seq":1,"type":"skill_cast","actor_id":"p1","target_id":"e1"},{"seq":2,"type":"damage","actor_id":"p1","target_id":"e1","amount":18}]
	fixture.battle.units[1].hp = 82
	room.apply_state_batch(2, fixture.duplicate(true), catalog, events, {"battle_id":"b1"})
	assert(room._effects.size() == 2)
	room.apply_state_batch(2, fixture.duplicate(true), catalog, events, {"battle_id":"b1"})
	assert(room._effects.size() == 2, "Events must not replay on duplicate state")
	var completed: Dictionary = fixture.battle.duplicate(true)
	completed.result = "win"
	fixture.battle = null
	room.apply_state_batch(3, fixture.duplicate(true), catalog, [], {"battle_id":"b1","completed_battle":completed})
	assert(room._finish_until > room.elapsed)
	print("PASS: room cached art, preview/reconcile, target, event deduplication, completed battle retention")
	quit()
