extends Node
##
## Authoritative world state.
##
## Holds the grid, all connected players, their active monster + inventory, and
## an in-flight Battle instance per player (when in_battle). Everything
## broadcast over WS goes through here.
##

const WORLD_W: int = 20
const WORLD_H: int = 15

# Encounter zones — same coordinates the client draws.
const ENCOUNTER_ZONES: Array = [
	{"x": 5,  "y": 5,  "w": 3, "h": 3},
	{"x": 12, "y": 8,  "w": 4, "h": 2},
	{"x": 1,  "y": 10, "w": 5, "h": 3},
]

const ENCOUNTER_RATE: float = 0.30

# Wild pool rolls any monster in the table (level rolled 1-5 at spawn).
const WILD_POOL_IDS: Array = ["sproutling", "charmander", "squirtle", "rattata", "caterpie", "weedle"]

# Each player gets a fixed starter for MVP (one monster, no party switching).
const STARTER_ID: String = "starter"
const STARTER_LEVEL: int = 3

# name -> { name, x, y, dir, in_battle, monster, inventory, battle, wild_monster }
var players: Dictionary = {}

var game_data: Node

# Save module (injected from server_main). May be null in early boot — calls
# check for null before using.
var save: Node = null


func _init() -> void:
	game_data = preload("res://game/game_data.gd").new()


func attach_save(s: Node) -> void:
	save = s


func _default_starter() -> Dictionary:
	var starter_template: Dictionary = game_data.get_monster(STARTER_ID)
	return game_data.spawn_monster(starter_template, STARTER_LEVEL)


func add_player(name: String, x: int, y: int, dir: String) -> void:
	if players.has(name):
		return
	# Load prior session from disk if it exists — restores monster level/xp,
	# inventory, and last position. New players get the starter + 3 potions.
	var saved: Dictionary = save.load_save(name) if save != null else {}
	var p: Dictionary
	if not saved.is_empty():
		p = {
			"name":       name,
			"x":          int(saved.get("x", x)),
			"y":          int(saved.get("y", y)),
			"dir":        String(saved.get("dir", dir)),
			"in_battle":  false,
			"monster":    saved.get("monster", _default_starter()),
			"inventory":  saved.get("inventory", {"potion": 3}),
			"battle":     null,
			"wild_monster": null,
		}
		print("[World] Player %s restored from save at (%d,%d) — %s lv%d xp%d" % [
			name, p["x"], p["y"], p["monster"]["name"], p["monster"]["level"], p["monster"]["xp"]
		])
	else:
		p = {
			"name":       name,
			"x":          x,
			"y":          y,
			"dir":        dir,
			"in_battle":  false,
			"monster":    _default_starter(),
			"inventory":  {"potion": 3},
			"battle":     null,
			"wild_monster": null,
		}
		print("[World] Player added: %s at (%d, %d) with %s (lv%d)" % [name, x, y, p["monster"]["name"], p["monster"]["level"]])
	players[name] = p


## Persist the player's current state to disk. Skips players mid-battle so we
## never serialize an inconsistent snapshot (battle has live monster refs).
## Called on graceful BYE, force_disconnect, and battle end.
func save_player(name: String) -> void:
	if save == null:
		return
	if not players.has(name):
		return
	var p: Dictionary = players[name]
	if p["in_battle"]:
		return  # never save mid-battle
	var data: Dictionary = {
		"name":      name,
		"x":         p["x"],
		"y":         p["y"],
		"dir":       p["dir"],
		"monster":   p["monster"],
		"inventory": p["inventory"],
	}
	save.save_save(name, data)


func remove_player(name: String) -> void:
	if not players.has(name):
		return
	players.erase(name)
	print("[World] Player removed: %s" % name)


func player_exists(name: String) -> bool:
	return players.has(name)


## Returns:
##   { "moved": false }                            — invalid move (wall / in_battle)
##   { "moved": true,  "encounter": {} }           — moved, no encounter
##   { "moved": true,  "encounter": { ... }, "battle": Battle } — moved + encounter
func move_player(name: String, dir: String) -> Dictionary:
	if not players.has(name):
		return {"moved": false}
	var p: Dictionary = players[name]
	if p["in_battle"]:
		return {"moved": false}
	var nx: int = int(p["x"])
	var ny: int = int(p["y"])
	match dir:
		"up":    ny -= 1
		"down":  ny += 1
		"left":  nx -= 1
		"right": nx += 1
		_: return {"moved": false}
	nx = clamp(nx, 0, WORLD_W - 1)
	ny = clamp(ny, 0, WORLD_H - 1)
	if nx == int(p["x"]) and ny == int(p["y"]):
		return {"moved": false}
	p["x"] = nx
	p["y"] = ny
	p["dir"] = dir
	players[name] = p

	# Roll encounter (only fires if landed in a zone AND RNG).
	var enc: Dictionary = {}
	if is_in_encounter_zone(nx, ny) and randf() <= ENCOUNTER_RATE and WILD_POOL_IDS.size() > 0:
		var wild_id: String = WILD_POOL_IDS[randi() % WILD_POOL_IDS.size()]
		var wild_level: int = 1 + (randi() % 5)  # lv 1..5
		enc = {"id": wild_id, "level": wild_level}
	if enc.is_empty():
		return {"moved": true, "encounter": {}}

	# Spawn wild monster + start battle.
	var wild_template: Dictionary = game_data.get_monster(enc["id"])
	var wild: Dictionary = game_data.spawn_monster(wild_template, enc["level"])
	var BattleScript = preload("res://game/battle.gd")
	var battle = BattleScript.new(game_data, p["monster"], wild)
	p["in_battle"] = true
	p["wild_monster"] = wild
	p["battle"] = battle
	players[name] = p
	print("[World] %s encountered wild %s (lv%d)" % [name, wild["name"], wild["level"]])
	return {"moved": true, "encounter": enc, "battle": battle}


## Process an ACTION from a player in battle. Returns the event list to send.
## Returns an empty list if player isn't in battle or the action is invalid.
func apply_action(name: String, action: Dictionary) -> Array:
	if not players.has(name):
		return []
	var p: Dictionary = players[name]
	if not p["in_battle"]:
		return []
	var battle: Node = p["battle"]
	return battle.handle_action(action)


## End a player's in-flight battle and clean up.
func end_battle(name: String) -> void:
	if not players.has(name):
		return
	var p: Dictionary = players[name]
	if not p["in_battle"]:
		return
	p["in_battle"] = false
	p["battle"] = null
	p["wild_monster"] = null
	players[name] = p
	print("[World] %s battle ended (monster lv%d, xp %d)" % [name, p["monster"]["level"], p["monster"]["xp"]])


func get_players_snapshot() -> Array:
	var snapshot: Array = []
	for p in players.values():
		snapshot.append({
			"name": p["name"],
			"x":    p["x"],
			"y":    p["y"],
			"dir":  p["dir"],
		})
	return snapshot


# --- Encounter helpers -----------------------------------------------------

func is_in_encounter_zone(x: int, y: int) -> bool:
	for z in ENCOUNTER_ZONES:
		if x >= z["x"] and x < z["x"] + z["w"] and y >= z["y"] and y < z["y"] + z["h"]:
			return true
	return false
