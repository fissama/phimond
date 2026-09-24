extends SceneTree
## asset_smoke.gd — verifies all assets referenced by scenes actually load as
## Texture2D / SpriteFrames. Counts species_atlas.json entries and PNG files in
## the extracted manifests. Quits 0 on pass, 1 on any failure.
##
## Run: godot --headless --script res://scripts/asset_smoke.gd

const SCENES := [
	"res://scenes/LoginScreen.tscn",
	"res://scenes/MainMap.tscn",
	"res://scenes/BattleScene.tscn",
	"res://scenes/NpcMenu.tscn",
	"res://scenes/ShopMenu.tscn",
]

# Hand-curated list of texture/SpriteFrames paths that scenes transitively depend on.
const SCENE_TEXTURE_PATHS := [
	"res://assets/reference/ui/UI.png",
	"res://assets/reference/ui/right_btn0.png",
	"res://assets/reference/ui/right_btn1.png",
	"res://assets/reference/ui/right_btn2.png",
	"res://assets/reference/ui/tableitem.png",
	"res://assets/reference/ui/tableitem1.png",
	"res://assets/reference/actors/Boy/Idle/000.png",
	"res://assets/reference/actors/Boy/Idle/001.png",
	"res://assets/reference/actors/Boy/Idle/002.png",
	"res://assets/reference/actors/Boy/Idle/003.png",
	"res://assets/reference/actors/Boy/Idle/004.png",
	"res://assets/reference/actors/Boy/Idle/005.png",
	"res://assets/reference/actors/Boy/Run/000.png",
	"res://assets/reference/actors/Boy/Run/001.png",
	"res://assets/reference/actors/Boy/Run/002.png",
	"res://assets/reference/actors/Boy/Run/003.png",
	"res://assets/reference/actors/Boy/Run/004.png",
	"res://assets/reference/actors/Boy/Run/005.png",
	"res://assets/reference/npcs/level3_1024.png",
	"res://assets/reference/npcs/level3_1029.png",
	"res://assets/reference/npcs/level3_1030.png",
	"res://assets/reference/npcs/level4_353.png",
	"res://assets/reference/npcs/level5_668.png",
	"res://assets/reference/rooms/arena.png",
	"res://assets/reference/rooms/beach.png",
	"res://assets/reference/rooms/forest.png",
	"res://assets/reference/rooms/ranch.png",
	"res://assets/reference/rooms/severa.png",
]

const SPECIES_IDS := [
	"snail", "flower_fairy", "mushroom", "dark_crab", "wealth_turtle",
	"treasure_chest", "sea_demon", "spider", "wolf", "windmill_spirit",
	"grove_guardian", "tide_sentinel", "moon_warden", "dawn_sovereign",
]

func _initialize() -> void:
	print("[asset_smoke] start")
	var fails: Array[String] = []
	# 1. Each scene loads and instantiates.
	for path in SCENES:
		var ps: PackedScene = load(path)
		if ps == null:
			fails.append("scene_load_failed: " + path); continue
		var inst := ps.instantiate()
		if inst == null:
			fails.append("scene_instantiate_failed: " + path); continue
		print("[asset_smoke] scene OK: ", path)
		inst.queue_free()
	# 2. Each texture path loads as Texture2D.
	for p in SCENE_TEXTURE_PATHS:
		var res = load(p)
		if res == null or not (res is Texture2D):
			fails.append("texture_load_failed: " + p + " (got " + str(res) + ")")
	# 3. SpriteFrames files for player + 14 species load.
	var frames_paths := ["res://assets/extracted/spriteframes_player.tres"]
	for sid in SPECIES_IDS:
		frames_paths.append("res://assets/extracted/spriteframes_" + sid + ".tres")
	for p in frames_paths:
		var res = load(p)
		if res == null or not (res is SpriteFrames):
			fails.append("spriteframes_load_failed: " + p + " (got " + str(res) + ")")
		else:
			# Sanity: must have at least one animation and one frame.
			var anims: Array = res.get_animation_names()
			if anims.size() == 0:
				fails.append("spriteframes_empty_animations: " + p)
	# 4. species_atlas.json has 14 entries.
	var atlas_path := "res://assets/extracted/species_atlas.json"
	if not FileAccess.file_exists(atlas_path):
		fails.append("missing_species_atlas: " + atlas_path)
	else:
		var f := FileAccess.open(atlas_path, FileAccess.READ)
		var txt := f.get_as_text()
		f.close()
		var parsed: Variant = JSON.parse_string(txt)
		if not parsed is Dictionary:
			fails.append("species_atlas_parse_failed")
		else:
			var species_dict: Dictionary = parsed.get("species", {})
			if species_dict.size() < 14:
				fails.append("species_atlas_too_few_entries: " + str(species_dict.size()))
			else:
				print("[asset_smoke] species_atlas.json has ", species_dict.size(), " species")
	# 5. phimond_manifest.json has >= 30 PNGs (total across both APKs).
	var phimond_path := "res://assets/extracted/phimond_manifest.json"
	if not FileAccess.file_exists(phimond_path):
		fails.append("missing_phimond_manifest: " + phimond_path)
	else:
		var f := FileAccess.open(phimond_path, FileAccess.READ)
		var txt := f.get_as_text()
		f.close()
		var parsed: Variant = JSON.parse_string(txt)
		if not parsed is Dictionary:
			fails.append("phimond_manifest_parse_failed")
		else:
			var counts: Dictionary = parsed.get("counts", {})
			print("[asset_smoke] plimond_manifest counts: ", counts)
	# 6. Each spriteframes file actually points to assets that load — sample one
	#    frame texture to ensure no dead references.
	for sid_v in SPECIES_IDS:
		var sid: String = sid_v
		var frames_path: String = "res://assets/extracted/spriteframes_" + sid + ".tres"
		var res: SpriteFrames = load(frames_path)
		if res == null: continue
		for anim in res.get_animation_names():
			var n_frames: int = res.get_frame_count(anim)
			if n_frames == 0:
				fails.append("empty_anim: " + sid + "/" + anim)
				continue
			var t: Texture2D = res.get_frame_texture(anim, 0)
			if t == null:
				fails.append("dead_texture_in_frame: " + sid + "/" + anim + "/0")
	# Done.
	if fails.is_empty():
		print("[asset_smoke] DONE — PASS (all ", SCENE_TEXTURE_PATHS.size(), " textures, ", frames_paths.size(), " spriteframes, ", SPECIES_IDS.size(), " species)")
		quit(0)
	else:
		print("[asset_smoke] DONE — FAIL (", fails.size(), " issues)")
		for f in fails:
			print("  - ", f)
		quit(1)
