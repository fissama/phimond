extends Node
##
## Message builders + type constants.
## Keep all JSON shapes in one place so client + server never drift.
##

const TYPE_HELLO: String = "HELLO"
const TYPE_MOVE: String = "MOVE"
const TYPE_ACTION: String = "ACTION"

const TYPE_STATE: String = "STATE"
const TYPE_ERROR: String = "ERROR"

# Phase 2+ (declared for reference; not used in MVP slice)
const TYPE_ENCOUNTER: String = "ENCOUNTER"
const TYPE_BATTLE_START: String = "BATTLE_START"
const TYPE_BATTLE_TURN: String = "BATTLE_TURN"
const TYPE_BATTLE_END: String = "BATTLE_END"


static func make_state(players: Array) -> String:
	return JSON.stringify({
		"type": TYPE_STATE,
		"players": players,
	})


static func make_error(message: String) -> String:
	return JSON.stringify({
		"type": TYPE_ERROR,
		"message": message,
	})


static func make_battle_start(wild: Dictionary, player_monster: Dictionary, inventory: Array, skills_detail: Array = [], items_detail: Array = []) -> String:
	return JSON.stringify({
		"type": TYPE_BATTLE_START,
		"wild": wild,
		"player": player_monster,
		"inventory": inventory,
		"skills": skills_detail,
		"items": items_detail,
	})


static func make_battle_turn(events: Array, awaiting_input: bool) -> String:
	return JSON.stringify({
		"type": TYPE_BATTLE_TURN,
		"events": events,
		"awaitingInput": awaiting_input,
	})


static func make_battle_end(result: String, xp_gained: int = 0) -> String:
	return JSON.stringify({
		"type": TYPE_BATTLE_END,
		"result": result,
		"xpGained": xp_gained,
	})
