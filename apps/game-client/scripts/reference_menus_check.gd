extends SceneTree

class FixtureClient extends Node:
	var catalog: Dictionary = {}
	var state: Dictionary = {}
	var sent: Array = []
	func send(op: String, data: Dictionary) -> void: sent.append({"op": op, "data": data})
	func activate(id: String) -> void: send("pet.activate", {"pet_id": id})
	func appraise(id: String) -> void: send("pet.appraise", {"pet_id": id})
	func accept_quest(id: String) -> void: send("quest.accept", {"quest_id": id})
	func claim_quest(id: String) -> void: send("quest.claim", {"quest_id": id})
	func learn_recipe(id: String) -> void: send("recipe.learn", {"recipe_id": id})

var client := FixtureClient.new()
var menus = preload("res://scripts/reference_menus.gd").new()
var content: VBoxContainer

func _initialize() -> void: call_deferred("_run")

func _run() -> void:
	root.size = Vector2i(960, 640)
	root.add_child(client)
	var data := ProjectSettings.globalize_path("res://../../data")
	for key in ["skills", "items", "quests", "recipes"]:
		client.catalog[key] = JSON.parse_string(FileAccess.get_file_as_string(data.path_join(key + "/" + key + ".json")))
	client.catalog.species = JSON.parse_string(FileAccess.get_file_as_string(data.path_join("pets/species.json")))
	var pet := {"id": "one", "species_id": "snail", "name": "Ốc Sen Hoa", "level": 20, "hp": 90, "max_hp": 120, "mp": 40, "max_mp": 55, "attack": 31, "magic": 25, "defense": 28, "speed": 17, "skills": ["attack"], "growth": {"strength": 100}, "quality": {"strength": 900}, "resistances": {"fire": 10}, "status_resistances": {"sleep": 8}}
	var other := pet.duplicate(true)
	other.id = "two"
	other.name = "Donor"
	client.state = {"pets": [pet, other], "active_pet_id": "one", "inventory": {"potion": 12, "ether": 3}, "quests": {}, "recipes": ["snail_refinement"], "gold": 500}
	var background := ColorRect.new()
	background.color = Color("061d31")
	background.size = Vector2(960, 640)
	root.add_child(background)
	content = VBoxContainer.new()
	content.position = Vector2(135, 45)
	content.size = Vector2(790, 350)
	root.add_child(content)
	for page in ["Companions", "Inventory", "Quests", "Ranch"]:
		_build(page)
		await process_frame
		await process_frame
		if DisplayServer.get_name() != "headless":
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("/tmp/phimond-menu-" + page.to_lower() + ".png")
	for tab in ["Attributes", "Resistance", "Skills", "Growth"]:
		menus.pet_tab = tab
		_build("Companions")
		await process_frame
	menus.ranch_tab = "Strengthen"
	menus.parent_a = "one"
	menus.parent_b = "two"
	_build("Ranch")
	_button_named(content, "Strengthen…").pressed.emit()
	assert(client.sent.is_empty(), "Strengthening must wait for explicit confirmation")
	assert(menus.confirmation.data.donor_id == "two")
	_button_named(content, "Cancel").pressed.emit()
	assert(client.sent.is_empty())
	_button_named(content, "Strengthen…").pressed.emit()
	_button_named(content, "Confirm").pressed.emit()
	assert(client.sent.size() == 1 and client.sent[0].op == "pet.strengthen")
	assert(client.sent[0].data == {"pet_id": "one", "donor_id": "two"})
	menus.ranch_tab = "Synthesis"
	menus.recipe_id = "snail_refinement"
	menus.parent_b = "one"
	_build("Ranch")
	_button_named(content, "Synthesize…").pressed.emit()
	assert(menus.confirmation.is_empty(), "The same pet cannot be used twice")
	menus.parent_b = "two"
	_build("Ranch")
	_button_named(content, "Synthesize…").pressed.emit()
	assert(client.sent.size() == 1, "Synthesis must wait for explicit confirmation")
	assert("Both parents will be consumed" in menus.confirmation.message)
	_button_named(content, "Confirm").pressed.emit()
	assert(client.sent.size() == 2 and client.sent[1].op == "breeding.synthesize")
	menus.selected_quest_id = "first_capture"
	_build("Quests")
	_button_named(content, "Accept quest").pressed.emit()
	assert(client.sent[2].data.quest_id == "first_capture", "Dispatch selected quest, not first catalog quest")
	client.state.quests = {"first_capture": {"progress": 0, "claimed": false}}
	_build("Quests")
	assert(_button_named(content, "Claim reward").disabled)
	client.state.quests.first_capture.progress = 1
	_build("Quests")
	assert(not _button_named(content, "Claim reward").disabled)
	client.state.pets[1].retired = true
	assert(menus._pet_list().size() == 1, "Retired pets cannot be selected for consuming actions")
	client.state.pets = []
	for page in ["Companions", "Ranch"]: _build(page)
	print("REFERENCE_MENUS_CHECK: four pages/tabs, empty/retired pets, donor/synthesis confirmation, distinct parents, selected quest/claim eligibility passed")
	quit()

func _build(page: String) -> void:
	for child in content.get_children():
		content.remove_child(child)
		child.queue_free()
	menus.build(page, content, client, _build)

func _button_named(parent: Node, title: String) -> Button:
	for child in parent.get_children():
		if child is Button and child.text == title: return child
		var found := _button_named(child, title)
		if found != null: return found
	return null
