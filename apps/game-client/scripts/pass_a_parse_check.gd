extends SceneTree
## Pass A parse check — loads each scene as a PackedScene and instantiates it briefly
## to surface any runtime scene errors. Quits 0 if all 5 scenes load.

func _initialize() -> void:
	var scenes := [
		"res://scenes/LoginScreen.tscn",
		"res://scenes/MainMap.tscn",
		"res://scenes/BattleScene.tscn",
		"res://scenes/NpcMenu.tscn",
		"res://scenes/ShopMenu.tscn",
	]
	var failed := 0
	for path in scenes:
		var ps: PackedScene = load(path)
		if ps == null:
			print("[parse_check] FAIL load: ", path)
			failed += 1
			continue
		var inst := ps.instantiate()
		if inst == null:
			print("[parse_check] FAIL instantiate: ", path)
			failed += 1
			continue
		# Adding then freeing simulates a real load path. We defer to the next frame
		# so _ready() runs; in --quit-after mode we don't actually wait.
		root.add_child(inst)
		print("[parse_check] OK   ", path, "  root=", inst.get_class())
		inst.queue_free()
	if failed == 0:
		print("[parse_check] PASS — all 5 scenes loadable")
		quit(0)
	else:
		print("[parse_check] FAIL — ", failed, " scenes")
		quit(1)
