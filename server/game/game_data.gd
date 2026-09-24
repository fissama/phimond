extends Node
##
## Loads static game data from res://game/data/*.json into dictionaries.
## Used by World to spawn monsters and by Battle to look up skills/items.
##

var monsters: Dictionary = {}
var skills: Dictionary = {}
var items: Dictionary = {}


func _init() -> void:
	_load("res://game/data/monsters.json", monsters)
	_load("res://game/data/skills.json", skills)
	_load("res://game/data/items.json", items)
	print("[GameData] Loaded %d monsters, %d skills, %d items" % [monsters.size(), skills.size(), items.size()])


func _load(path: String, target: Dictionary) -> void:
	if not FileAccess.file_exists(path):
		push_error("[GameData] Missing file: %s" % path)
		return
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		push_error("[GameData] Failed to open: %s" % path)
		return
	var text: String = file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_ARRAY:
		push_error("[GameData] Bad JSON in %s" % path)
		return
	for entry in parsed:
		target[entry.get("id", "")] = entry


# --- Lookups ---------------------------------------------------------------

func get_monster(id: String) -> Dictionary:
	return monsters.get(id, {})


func get_skill(id: String) -> Dictionary:
	return skills.get(id, {})


func get_item(id: String) -> Dictionary:
	return items.get(id, {})


# --- Spawning --------------------------------------------------------------

## Build a runtime monster instance from a template + level.
## Stats scale with level so lv5 wild is noticeably tougher than lv1.
func spawn_monster(template: Dictionary, level: int) -> Dictionary:
	var base: Dictionary = template.get("baseStats", {})
	var hp: int = int(base.get("hp", 10)) + level * 2
	return {
		"id":       template.get("id", ""),
		"name":     template.get("name", "?"),
		"level":    level,
		"max_hp":   hp,
		"hp":       hp,
		"attack":   int(base.get("attack", 5)) + level,
		"defense":  int(base.get("defense", 5)) + int(level / 2),
		"speed":    int(base.get("speed", 5)) + int(level / 2),
		"skills":   template.get("skills", []),
		"xp":       0,
	}
