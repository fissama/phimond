extends SceneTree

var client: Node
var game: Control

func _initialize() -> void: call_deferred("run")

func check(value: bool, message: String) -> bool:
	if not value:
		push_error(message)
		quit(1)
	return value

func run() -> void:
	client = root.get_node("PhimondClient")
	client.set_process(false)
	client.catalog = {"maps":{"forest":{"width":70,"height":24}},"species":{},"npcs":{}}
	var battle := {"id":"b1","turn":1,"units":[{"id":"p1","name":"Snail","side":"player","species_id":"snail","hp":100,"max_hp":100},{"id":"e1","name":"Wolf","side":"enemy","species_id":"wolf","hp":100,"max_hp":100}]}
	var character := {"id":"hero","map_id":"forest","x":6,"y":12,"pets":[],"battle":battle}
	client._on_message({"op":"state","sequence":1,"data":{"character":character.duplicate(true),"events":[]}})
	game = load("res://scenes/MainMap.tscn").instantiate()
	root.add_child(game)
	await process_frame
	game.set_process(false)
	game.room.set_process(false)
	var hit := {"seq":1,"type":"damage","actor_id":"p1","target_id":"e1","amount":18}
	var reply := {"op":"state","sequence":2,"data":{"character":character.duplicate(true),"events":[hit],"presentation":{"battle_id":"b1"}}}
	client._on_message(reply)
	if not check(game.room._effects.size() == 1, "Live public events must reach active room"): return
	reply.sequence = 3
	client._on_message(reply)
	if not check(game.room._effects.size() == 2, "seq=1 in a new revision must not be dropped"): return
	client._on_message(reply)
	if not check(game.room._effects.size() == 2, "Duplicate batch must not replay"): return
	var completed := battle.duplicate(true)
	completed.result = "win"
	completed.units[1].hp = 0
	character.battle = null
	reply = {"op":"state","sequence":4,"data":{"character":character.duplicate(true),"events":[hit],"presentation":{"battle_id":"b1","completed_battle":completed}}}
	client._on_message(reply)
	if not check(game.room.is_animating() and not client.has_battle(), "Terminal playback must survive authoritative battle=null"): return
	if not check(game.room._battle.get("result") == "win", "Terminal public result retained"): return
	var end: float = game.room._finish_until
	client._on_message(reply)
	if not check(game.room._finish_until == end, "Duplicate terminal cannot prolong animation"): return
	game.move_delay = 0
	game._move("right")
	if not check(game.room._preview_x < 0, "No world preview during terminal playback"): return
	client.catalog.npcs = {"nearby":{"id":"nearby","x":6,"y":12}}
	game._approach("npc", "nearby")
	if not check(game.page == "World", "No NPC interaction during terminal playback"): return
	game.room._process(10.0)
	if not check(not game.room.is_animating() and game.room._battle.is_empty(), "Playback ends without another packet"): return
	# An accepted read of the same revision restores visuals after reconnect,
	# but never plays persisted events, even when talking to an older server.
	client.connection_changed.emit(false)
	client._connected = false
	client._on_message({"op":"state","sequence":5,"data":{"character":character,"events":[hit]}})
	if not check(game.room._effects.is_empty(), "Reconnect must not replay old events"): return
	character.battle = battle
	client._on_message({"op":"state","sequence":6,"data":{"character":character,"events":[
		{"type":"skill_cast","actor_id":"p1","target_id":"p1"},
		{"type":"heal","target_id":"p1","amount":10},
		{"type":"skill_cast","actor_id":"e1","target_id":"p1"},
		{"type":"damage","target_id":"p1","amount":5}],"presentation":{"battle_id":"b1"}}})
	if not check(float(game.room._effects[3].start) >= float(game.room._effects[1].end), "Separate actions on the same target must not overlap numbers"): return
	print("PASS: active wire bridge, per-revision events, duplicate terminal, input lock, end timer, reconnect")
	game.queue_free()
	quit()
