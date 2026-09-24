extends Node
class_name Battle
##
## Stateless battle FSM (per-player). Owned by World.battles[name] while the
## player is in a fight; World disposes the node when the battle ends.
##
## Flow:
##   AWAITING_INPUT  --(action)-->  PROCESSING
##   PROCESSING      --(apply events, check end)-->  FINISHED
##   FINISHED        --(caller reads result)-->  cleanup
##

enum State { AWAITING_INPUT, PROCESSING, FINISHED }

var game_data: Node
var player_monster: Dictionary   # mutable, level/xp persists
var wild_monster: Dictionary     # mutable
var state: int = State.AWAITING_INPUT
var xp_gained: int = 0


func _init(p_game_data: Node, p_player_monster: Dictionary, p_wild_monster: Dictionary) -> void:
	game_data = p_game_data
	player_monster = p_player_monster
	wild_monster = p_wild_monster


func is_awaiting_input() -> bool:
	return state == State.AWAITING_INPUT


func is_finished() -> bool:
	return state == State.FINISHED


func get_result() -> String:
	if wild_monster["hp"] == 0:
		return "win"
	if player_monster["hp"] == 0:
		return "lose"
	return "flee"


## Process one ACTION from the client. Returns the event list to broadcast.
func handle_action(action: Dictionary) -> Array:
	if state != State.AWAITING_INPUT:
		return []
	state = State.PROCESSING
	var events: Array = []
	var choice: String = action.get("choice", "")
	match choice:
		"attack":
			# Use the player's first skill as the default attack.
			var skill_id: String = player_monster["skills"][0]
			events.append_array(_execute_player_skill(skill_id))
		"skill":
			var skill_id: String = action.get("skillId", "")
			events.append_array(_execute_player_skill(skill_id))
		"item":
			var item_id: String = action.get("itemId", "")
			events.append_array(_execute_player_item(item_id))
		"flee":
			events.append({"kind": "text", "msg": "%s fled!" % player_monster["name"]})
		_:
			events.append({"kind": "text", "msg": "Unknown action."})

	if state == State.FINISHED:
		_finalize(events)
	elif not events.is_empty():
		# Re-arm for next round.
		state = State.AWAITING_INPUT
	return events


# --- Player actions --------------------------------------------------------

func _execute_player_skill(skill_id: String) -> Array:
	var events: Array = []
	var skill: Dictionary = game_data.get_skill(skill_id)
	if skill.is_empty():
		events.append({"kind": "text", "msg": "But it failed!"})
		return events
	events.append({"kind": "text", "msg": "%s used %s!" % [player_monster["name"], skill["name"]]})
	match skill.get("kind", "physical"):
		"physical", "special":
			_apply_damage(player_monster, wild_monster, skill, "wild", events)
		"status":
			events.append({"kind": "text", "msg": "(status effect — no-op for MVP)"})

	if wild_monster["hp"] == 0:
		events.append({"kind": "text", "msg": "Wild %s fainted!" % wild_monster["name"]})
		state = State.FINISHED
	elif state != State.FINISHED:
		events.append_array(_wild_turn())
	return events


func _execute_player_item(item_id: String) -> Array:
	var events: Array = []
	var item: Dictionary = game_data.get_item(item_id)
	if item.is_empty():
		events.append({"kind": "text", "msg": "Item not found."})
		return events
	var eff: Dictionary = item.get("effect", {})
	if eff.get("kind", "") == "heal":
		var amount: int = int(eff.get("amount", 0))
		var before: int = player_monster["hp"]
		player_monster["hp"] = min(player_monster["max_hp"], before + amount)
		var actual: int = player_monster["hp"] - before
		events.append({"kind": "text", "msg": "Used %s! Restored %d HP." % [item["name"], actual]})
		events.append({"kind": "heal", "target": "player", "amount": actual, "hp": {"cur": player_monster["hp"], "max": player_monster["max_hp"]}})
	# Items give the wild a free turn.
	if state != State.FINISHED:
		events.append_array(_wild_turn())
	return events


# --- Wild actions ----------------------------------------------------------

func _wild_turn() -> Array:
	var events: Array = []
	if wild_monster["skills"].is_empty():
		return events
	var skill_id: String = wild_monster["skills"][randi() % wild_monster["skills"].size()]
	var skill: Dictionary = game_data.get_skill(skill_id)
	if skill.is_empty():
		return events
	events.append({"kind": "text", "msg": "Wild %s used %s!" % [wild_monster["name"], skill.get("name", "?")]})
	if skill.get("kind", "physical") in ["physical", "special"]:
		_apply_damage(wild_monster, player_monster, skill, "player", events)
	if player_monster["hp"] == 0:
		events.append({"kind": "text", "msg": "%s fainted!" % player_monster["name"]})
		state = State.FINISHED
	return events


# --- Damage math -----------------------------------------------------------

func _apply_damage(attacker: Dictionary, defender: Dictionary, skill: Dictionary, target: String, events: Array) -> void:
	var atk: float = float(attacker["attack"])
	var dfs: float = max(1.0, float(defender["defense"]))
	var power: float = float(skill.get("power", 5))
	var raw: int = int((power * atk / dfs) / 2.0) + randi() % 5 - 2
	var dmg: int = max(1, raw)
	defender["hp"] = max(0, defender["hp"] - dmg)
	events.append({"kind": "damage", "target": target, "amount": dmg, "hp": {"cur": defender["hp"], "max": defender["max_hp"]}})


# --- End-of-battle ---------------------------------------------------------

func _finalize(events: Array) -> void:
	if wild_monster["hp"] == 0:
		xp_gained = int(wild_monster["level"]) * 5
		player_monster["xp"] = int(player_monster.get("xp", 0)) + xp_gained
		events.append({"kind": "text", "msg": "%s gained %d XP." % [player_monster["name"], xp_gained]})
		# Level-up check: 30 XP per level.
		while int(player_monster["xp"]) >= 30:
			player_monster["xp"] = int(player_monster["xp"]) - 30
			player_monster["level"] = int(player_monster["level"]) + 1
			player_monster["max_hp"] = int(player_monster["max_hp"]) + 4
			player_monster["hp"] = int(player_monster["max_hp"])
			player_monster["attack"] = int(player_monster["attack"]) + 1
			player_monster["defense"] = int(player_monster["defense"]) + 1
			player_monster["speed"] = int(player_monster["speed"]) + 1
			events.append({"kind": "text", "msg": "%s grew to level %d!" % [player_monster["name"], player_monster["level"]]})
