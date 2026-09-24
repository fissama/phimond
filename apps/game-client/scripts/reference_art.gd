extends RefCounted

const ROOT = "res://assets/reference/"
# APK identities; Phimond-only evolutions intentionally remain unmapped.
const SPECIES = {
	"snail": "OCSENHOA", "flower_fairy": "YEUTINHHOA", "mushroom": "NAMHOA",
	"spider": "NHENDOC", "wolf": "SOINGONGAN", "dark_crab": "CUAHACAM",
	"wealth_turtle": "RUAPHUQUY", "treasure_chest": "QUAIVATRUONGBAU",
	"sea_demon": "TIEUACMA", "windmill_spirit": "CHONGCHONGGIO"
}
const NPCS = {
	"trainer": "level3_1030.png", "ranch_keeper": "level3_1029.png",
	"arena_master": "level3_1024.png", "forest_guide": "level4_353.png",
	"beach_guide": "level5_668.png"
}
static var cache: Dictionary = {}
static var actors: Dictionary = {}
static var prepared := false

func prepare() -> void:
	if prepared:
		return
	actors = JSON.parse_string(FileAccess.get_file_as_string(ROOT + "actors.json"))
	for map_id in ["severa", "forest", "beach", "ranch", "arena"]:
		texture(ROOT + "rooms/" + map_id + ".png")
	for animations in actors.values():
		for animation in animations.values():
			for frame in animation.get("frames", []):
				texture(ROOT + "actors/" + str(frame), true)
	for filename in NPCS.values():
		texture(ROOT + "npcs/" + filename, true)
	prepared = true

func texture(path: String, trim: bool = false) -> Texture2D:
	if not cache.has(path):
		var imported: Texture2D = load(path) if ResourceLoader.exists(path) else null
		var source: Image = imported.get_image() if imported != null else null
		if source == null and FileAccess.file_exists(path):
			source = Image.load_from_file(ProjectSettings.globalize_path(path))
		# Composited Unity layers include transparent outer sprite margins.
		# Crop those margins once so the camera never exposes empty gutters.
		if source != null and "/rooms/" in path:
			var left := 200 if path.ends_with("forest.png") else 24
			var right := 100 if path.ends_with("forest.png") else 24
			source = source.get_region(Rect2i(left, 16, source.get_width() - left - right, source.get_height() - 40))
		if source != null and trim:
			var used := source.get_used_rect()
			if used.has_area():
				source = source.get_region(used)
		cache[path] = ImageTexture.create_from_image(source) if source != null else null
	return cache[path]

func room_texture(map_id: String) -> Texture2D:
	return cache.get(ROOT + "rooms/" + map_id + ".png")

func npc_texture(npc_id: String) -> Texture2D:
	return cache.get(ROOT + "npcs/" + str(NPCS.get(npc_id, "")))

func pet_texture(species_id: String, elapsed: float, action: String = "idle") -> Texture2D:
	return actor_texture(str(SPECIES.get(species_id, "")), action, elapsed)

func actor_texture(actor: String, action: String, elapsed: float) -> Texture2D:
	var animations: Dictionary = actors.get(actor, {})
	var animation: Dictionary = animations.get(action, animations.get("idle", {}))
	var frames: Array = animation.get("frames", [])
	if frames.is_empty():
		return null
	var duration := maxf(float(animation.get("duration", 1.0)), 0.1)
	# Running is a visual preview; source curve timings are not fully recovered.
	if action == "run":
		duration = minf(duration, 0.65)
	var index := int(fposmod(elapsed, duration) / duration * frames.size()) % frames.size()
	return cache.get(ROOT + "actors/" + str(frames[index]))
