extends SceneTree
## build_atlas.gd — one-shot tool that builds SpriteFrames .tres files for the player
## and every species in species_atlas.json. Run from the project root:
##   godot --headless --script res://scripts/build_atlas.gd
## Output:
##   assets/extracted/spriteframes_player.tres
##   assets/extracted/spriteframes_<species_id>.tres (one per species)
##   assets/extracted/species_atlas.tres (SpriteAtlas texture, but Godot 4 uses
##     AtlasTexture references in SpriteFrames rather than a SpriteAtlas node;
##     we keep a stub .tres here for callers that want to load the index)

const ATLAS_DIR := "res://assets/extracted/"

func _initialize() -> void:
	# Build player SpriteFrames first.
	_build_player()
	# Build per-species SpriteFrames.
	var species_path := "res://assets/extracted/species_atlas.json"
	if not FileAccess.file_exists(species_path):
		printerr("[build_atlas] missing ", species_path); quit(1); return
	var f := FileAccess.open(species_path, FileAccess.READ)
	var txt := f.get_as_text()
	f.close()
	var parsed: Variant = JSON.parse_string(txt)
	if not parsed is Dictionary:
		printerr("[build_atlas] atlas parse failed"); quit(1); return
	var species: Dictionary = parsed.get("species", {})
	for sid in species.keys():
		_build_species(sid, species[sid])
	# Stub species_atlas.tres so callers have a stable handle. We populate it as
	# a SpriteFrames whose frames index follows species_id alphabetical order.
	_write_index_stub(species.keys())
	print("[build_atlas] DONE — wrote SpriteFrames for player + ", species.size(), " species")
	quit(0)

func _build_player() -> void:
	var frames := SpriteFrames.new()
	if frames.has_animation("default"):
		frames.remove_animation("default")
	frames.add_animation("idle")
	for p in [
		"res://assets/reference/actors/Boy/Idle/000.png",
		"res://assets/reference/actors/Boy/Idle/001.png",
		"res://assets/reference/actors/Boy/Idle/002.png",
		"res://assets/reference/actors/Boy/Idle/003.png",
		"res://assets/reference/actors/Boy/Idle/004.png",
		"res://assets/reference/actors/Boy/Idle/005.png",
	]:
		frames.add_frame("idle", load(p))
	frames.set_animation_speed("idle", 6.0)  # 6 frames over 1s
	frames.set_animation_loop("idle", true)
	frames.add_animation("run")
	for p in [
		"res://assets/reference/actors/Boy/Run/000.png",
		"res://assets/reference/actors/Boy/Run/001.png",
		"res://assets/reference/actors/Boy/Run/002.png",
		"res://assets/reference/actors/Boy/Run/003.png",
		"res://assets/reference/actors/Boy/Run/004.png",
		"res://assets/reference/actors/Boy/Run/005.png",
	]:
		frames.add_frame("run", load(p))
	frames.set_animation_speed("run", 12.0)
	frames.set_animation_loop("run", true)
	var save_path := ATLAS_DIR + "spriteframes_player.tres"
	var err := ResourceSaver.save(frames, save_path)
	if err != OK:
		printerr("[build_atlas] save player failed: ", err)
	else:
		print("[build_atlas] wrote ", save_path)

func _build_species(sid: String, info: Dictionary) -> void:
	var frames := SpriteFrames.new()
	# SpriteFrames auto-creates an empty 'default' animation on new(). Remove it
	# so consumers can rely on `has_animation("idle")` without seeing a phantom slot.
	if frames.has_animation("default"):
		frames.remove_animation("default")
	for anim in ["idle", "run", "attack", "magic", "die"]:
		var paths: Array = info.get(anim + "_frames", [])
		if paths.is_empty():
			continue
		frames.add_animation(anim)
		for p in paths:
			var rp := "res://assets/" + String(p)
			if not ResourceLoader.exists(rp):
				printerr("[build_atlas] missing ", rp, " for ", sid, "/", anim)
				continue
			frames.add_frame(anim, load(rp))
		var dur: float = float(info.get(anim + "_duration", 1.0))
		# If we have N frames and total dur D, fps ≈ N/D.
		var n: float = float(paths.size())
		var fps: float = max(1.0, n / max(dur, 0.001))
		frames.set_animation_speed(anim, fps)
		frames.set_animation_loop(anim, anim in ["idle", "run"])
	var save_path := ATLAS_DIR + "spriteframes_" + sid + ".tres"
	var err := ResourceSaver.save(frames, save_path)
	if err != OK:
		printerr("[build_atlas] save ", sid, " failed: ", err)
	else:
		print("[build_atlas] wrote ", save_path)

func _write_index_stub(species_ids: Array) -> void:
	# Build a tiny SpriteFrames that names the species — useful as a stable handle
	# for code that wants "the atlas index". The frames themselves are placeholders;
	# the real per-species frames live in spriteframes_<sid>.tres.
	var frames := SpriteFrames.new()
	frames.add_animation("index")
	for sid in species_ids:
		# Add a 1×1 white pixel placeholder for each species so the .tres is valid.
		var img := Image.create(1, 1, false, Image.FORMAT_RGBA8)
		img.set_pixel(0, 0, Color(1, 1, 1, 1))
		var tex := ImageTexture.create_from_image(img)
		frames.add_frame("index", tex)
	frames.set_animation_speed("index", 1.0)
	frames.set_animation_loop("index", false)
	var save_path := ATLAS_DIR + "species_atlas.tres"
	var err := ResourceSaver.save(frames, save_path)
	if err != OK:
		printerr("[build_atlas] save stub failed: ", err)
	else:
		print("[build_atlas] wrote stub ", save_path)
