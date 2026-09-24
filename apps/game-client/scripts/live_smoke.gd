extends SceneTree

# Integration test: creates one disposable account on the explicitly supplied API.
# Uses the real client HTTP, WebSocket, UI render and intent paths. Never prints credentials.
var client
var failed: bool = false

func _initialize() -> void:
	call_deferred("_run")

func _wait_for(condition: Callable, label: String, timeout: float = 20.0) -> bool:
	var deadline := Time.get_ticks_msec() + int(timeout * 1000)
	while not condition.call():
		if Time.get_ticks_msec() >= deadline:
			push_error("FAIL: " + label + " / " + str(client.status.text))
			failed = true
			quit(1)
			return false
		await create_timer(0.02).timeout
	return true

func _action(op: String, data: Dictionary = {}) -> bool:
	var before: int = client.revision
	client._intent(op, data)
	if not await _wait_for(func(): return client.pending.is_empty(), op): return false
	if client.revision <= before:
		push_error("FAIL: rejected " + op + " / " + str(client.status.text))
		failed = true
		quit(1)
		return false
	return true

func _run() -> void:
	create_timer(240).timeout.connect(func(): push_error("Live smoke exceeded overall deadline"); quit(1))
	var args := OS.get_cmdline_user_args()
	if args.is_empty():
		push_error("Pass a disposable/test API URL after --")
		quit(1)
		return
	client = load("res://main.tscn").instantiate()
	root.add_child(client)
	await process_frame
	var crypto := Crypto.new()
	var username := "gdt_" + crypto.generate_random_bytes(8).hex_encode()
	var password := crypto.generate_random_bytes(24).hex_encode()
	client.server_field.text = args[0]
	client.user_field.text = username
	client.pass_field.text = password
	client._authenticate("register")
	if not await _wait_for(func(): return client.authenticated, "register + WS first-frame authentication"): return
	print("PASS: real Godot HTTP registration, catalog fetch, WebSocket authentication and initial snapshot")
	for tab in ["Journey", "Companions", "Ranch", "Quests", "Supplies", "Battle"]:
		client.page = tab
		client._render()
		await process_frame
	if not await _action("quest.accept", {"quest_id": "first_steps"}): return
	if not await _action("shop.buy", {"item_id": "potion", "quantity": 1}): return
	if not await _action("npc.interact", {"npc_id": "trainer"}): return
	if not await _action("pet.heal"): return
	var starter: Dictionary = client.character.pets[0]
	client._request("lineage", "/api/lineage/" + str(starter.id).uri_encode())
	if not await _wait_for(func(): return client.http_kind.is_empty(), "lineage endpoint"): return
	while int(client.character.x) < 37:
		if not await _action("world.move", {"direction": "right"}): return
		if int(client.character.x) % 10 == 0: print("Progress: authoritative position ", int(client.character.x))
	if not await _action("world.portal", {"portal_id": "forest_gate"}): return
	assert(client.character.map_id == "forest")
	assert(int(client.character.quests.first_steps.progress) == 1)
	while int(client.character.x) < 3:
		if not await _action("world.move", {"direction": "right"}): return
	if not await _action("quest.claim", {"quest_id": "first_steps"}): return
	assert(client.character.quests.first_steps.claimed)
	print("PASS: live six-panel rendering, NPC, shop, healing, lineage, movement, portal, quest acceptance/progress/reward")
	if not await _action("world.encounter"): return
	client.page = "Battle"
	client._render()
	assert(client.character.battle is Dictionary)
	var battle_id: String = client.character.battle.id
	var battle_revision: int = client.revision
	client._battle_intent(client.character.battle, "defend")
	if not await _wait_for(func(): return client.pending.is_empty(), "UI battle defend"): return
	assert(client.revision > battle_revision)
	assert(client.character.battle is Dictionary)
	var turn: int = client.character.battle.turn
	var hp: int = client.character.battle.units[0].hp
	client._reconnect()
	if not await _wait_for(func(): return client.authenticated, "resume authentication"): return
	assert(client.character.battle.id == battle_id)
	assert(int(client.character.battle.turn) == turn)
	assert(int(client.character.battle.units[0].hp) == hp)
	if not await _action("battle.action", {"battle_id": battle_id, "turn": turn, "choice": "flee"}): return
	assert(client.character.battle == null)
	print("PASS: live battle intent, exact battle/turn/HP recovery after reconnect, flee and battle completion")
	var character_id: String = client.character.id
	client._sign_out()
	if not await _wait_for(func(): return client.http_kind.is_empty(), "logout"): return
	client.server_field.text = args[0]
	client.user_field.text = username
	client.pass_field.text = password
	client._authenticate("login")
	if not await _wait_for(func(): return client.authenticated, "login persisted character"): return
	assert(client.character.id == character_id)
	assert(client.character.map_id == "forest")
	assert(client.character.quests.first_steps.claimed)
	client._sign_out()
	if not await _wait_for(func(): return client.http_kind.is_empty(), "final logout"): return
	print("PASS: logout, password login and persisted character/quest recovery; final session revoked")
	client.queue_free()
	await process_frame
	quit(0)
