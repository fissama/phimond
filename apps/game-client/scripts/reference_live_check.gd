extends SceneTree
var client: Node
var game: Control
var auth_done := false
var auth_ok := false
var samples: Array[int] = []

func _initialize() -> void:
	call_deferred("run")

func wait_until(check: Callable, label: String) -> bool:
	var deadline := Time.get_ticks_msec() + 20000
	while not check.call():
		if Time.get_ticks_msec() > deadline:
			push_error("FAIL: " + label)
			quit(1)
			return false
		await create_timer(0.02).timeout
	return true

func action(op: String, data: Dictionary = {}) -> bool:
	var revision: int = client.revision
	var started := Time.get_ticks_msec()
	client.send(op, data)
	if not await wait_until(func(): return not client.is_busy(), op): return false
	if client.revision <= revision:
		push_error("Rejected action: " + op + ": " + client.last_error)
		quit(1)
		return false
	samples.append(Time.get_ticks_msec() - started)
	return true

func run() -> void:
	create_timer(180).timeout.connect(func(): push_error("Overall live check timeout"); quit(1))
	client = root.get_node("PhimondClient")
	var crypto := Crypto.new()
	var username := "ref_" + crypto.generate_random_bytes(7).hex_encode()
	var password := crypto.generate_random_bytes(20).hex_encode()
	client.http_register(username, password, func(ok: bool, _error: String): auth_ok = ok; auth_done = true)
	if not await wait_until(func(): return auth_done, "register"): return
	if not auth_ok: push_error("Registration failed"); quit(1); return
	client.fetch_content(func(_data: Dictionary): pass)
	if not await wait_until(func(): return not client.catalog.is_empty(), "catalog"): return
	client.connect_ws()
	if not await wait_until(func(): return client.is_ws_connected(), "WebSocket"): return
	game = load("res://scenes/MainMap.tscn").instantiate()
	root.add_child(game)
	current_scene = game
	await process_frame
	var initial := Vector2i(client.state.x, client.state.y)
	for direction in ["up", "down", "left", "right"]:
		game.move_delay = 0
		var before: int = client.revision
		game._move(direction)
		if not await wait_until(func(): return not client.is_busy(), "UI move " + direction): return
		assert(client.revision > before, "UI move rejected")
	assert(Vector2i(client.state.x, client.state.y) == initial)
	for page in ["Companions", "Inventory", "Quests", "Ranch"]:
		game._open(page)
		await process_frame
		assert(game.hud.menu.visible)
	game._close()
	if not await action("npc.interact", {"npc_id": "trainer"}): return
	game.npc_id = "trainer"
	game._open("NPC")
	assert(game.dialogue.visible)
	if not await action("quest.accept", {"quest_id": "first_steps"}): return
	if not await action("shop.buy", {"item_id": "potion", "quantity": 1}): return
	if not await action("pet.heal"): return
	game._close()
	while int(client.state.x) < 37:
		if not await action("world.move", {"direction": "right"}): return
	if not await action("world.portal", {"portal_id": "forest_gate"}): return
	assert(client.state.map_id == "forest")
	while int(client.state.x) < 3:
		if not await action("world.move", {"direction": "right"}): return
	if not await action("quest.claim", {"quest_id": "first_steps"}): return
	if not await action("world.encounter"): return
	assert(client.has_battle())
	await create_timer(0.3).timeout
	game._open("Skills")
	assert(game.hud.content_box.get_child_count() > 1)
	game._close()
	game._command("defend")
	if not await wait_until(func(): return not client.is_busy(), "UI defend"): return
	assert(int(client.state.battle.turn) > 1)
	await create_timer(2.5).timeout
	var potion_count := int(client.state.inventory.get("potion", 0))
	game._battle_send("item", "", "potion")
	if not await wait_until(func(): return not client.is_busy(), "UI battle item"): return
	assert(int(client.state.inventory.get("potion", 0)) == potion_count - 1)
	await create_timer(2.5).timeout
	var skill_id := str(client.state.pets[0].skills[0])
	var skill_revision: int = client.revision
	game._battle_send("skill", skill_id)
	if not await wait_until(func(): return not client.is_busy(), "UI skill"): return
	assert(client.revision > skill_revision)
	await create_timer(2.5).timeout
	if not client.has_battle():
		if not await action("world.encounter"): return
		await create_timer(0.3).timeout
	game._command("attack")
	game._confirm_target()
	if not await wait_until(func(): return not client.is_busy(), "UI attack"): return
	var snapshot: Dictionary = client.state.duplicate(true)
	client.connect_ws()
	if not await wait_until(func(): return client.is_ws_connected(), "reconnect"): return
	assert(client.state.id == snapshot.id)
	assert(client.state.battle == snapshot.battle)
	if client.has_battle():
		await create_timer(2.5).timeout
		game._command("flee")
		if not await wait_until(func(): return not client.is_busy(), "UI flee"): return
	assert(not client.has_battle())
	await create_timer(2.5).timeout
	if not await action("world.encounter"): return
	await create_timer(0.3).timeout
	var seals := int(client.state.inventory.get("capture_seal", 0))
	game._command("capture")
	game._confirm_target()
	if not await wait_until(func(): return not client.is_busy(), "UI capture"): return
	assert(int(client.state.inventory.get("capture_seal", 0)) == seals - 1)
	if client.has_battle():
		await create_timer(2.5).timeout
		game._command("flee")
		if not await wait_until(func(): return not client.is_busy(), "post-capture flee"): return
	auth_done = false
	client.http_login(username, password, func(ok: bool, _error: String): auth_ok = ok; auth_done = true)
	if not await wait_until(func(): return auth_done, "password login"): return
	assert(auth_ok)
	client.connect_ws()
	if not await wait_until(func(): return client.is_ws_connected(), "persisted state"): return
	assert(client.state.id == snapshot.id and client.state.quests.first_steps.claimed)
	samples.sort()
	print("PASS: actual registration/login, four UI directions, menus, NPC, shop, quest/portal/reward, battle defend/item/skill/attack/capture/flee, reconnect and persisted state")
	print("Action roundtrip ms: median=", samples[int(samples.size() / 2)], " max=", samples.back(), " samples=", samples.size())
	client._socket.close()
	quit()
