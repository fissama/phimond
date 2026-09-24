extends Control
## NpcMenu — fantasy-framed NPC dialogue popup. Title-bar is the NPC's name, body
## shows an 80x80 portrait (looked up from assets/reference/npcs/manifest.json by
## gameplay_mapping key), a placeholder dialogue RichTextLabel, and a row of
## GameButtons for the NPC's roles. Closing the window via the X button (or Esc)
## queue_frees the popup.

const NPC_SPRITE_PATH: Dictionary = {
	"trainer": "res://assets/reference/npcs/level3_1030.png",
	"ranch_keeper": "res://assets/reference/npcs/level3_1029.png",
	"arena_master": "res://assets/reference/npcs/level3_1024.png",
	"forest_guide": "res://assets/reference/npcs/level4_353.png",
	"beach_guide": "res://assets/reference/npcs/level5_668.png",
}

var npc_id: String = ""

@onready var _window: Control = $Window
@onready var _name_label: Label = $Window/Frame/Body/BodyContainer/BodyRoot/HeaderRow/HeaderCol/NameLabel
@onready var _dialogue: RichTextLabel = $Window/Frame/Body/BodyContainer/BodyRoot/HeaderRow/HeaderCol/Dialogue
@onready var _portrait: TextureRect = $Window/Frame/Body/BodyContainer/BodyRoot/HeaderRow/Portrait
@onready var _shop_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/ShopBtn
@onready var _heal_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/HealBtn
@onready var _appraise_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/AppraiseBtn
@onready var _breed_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/BreedBtn
@onready var _recipe_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/RecipeBtn
@onready var _quest_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/QuestBtn
@onready var _arena_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/RoleRow/ArenaBtn


func _ready() -> void:
	if _window and _window.has_method("set_close_callback"):
		_window.call("set_close_callback", _on_close)
	if _window and _window.has_method("set_title"):
		_window.call("set_title", _resolve_npc_name())
	_build()


func _resolve_npc_name() -> String:
	var npc: Variant = PhimondClient.catalog.get("npcs", {}).get(npc_id, {})
	if npc is Dictionary:
		return str(npc.get("name", npc_id))
	return npc_id


func _build() -> void:
	var npc: Variant = PhimondClient.catalog.get("npcs", {}).get(npc_id, {})
	if not npc is Dictionary: npc = {}
	var display_name: String = str(npc.get("name", npc_id))
	if is_instance_valid(_name_label): _name_label.text = display_name
	# Title-bar carries the NPC name as well so the popup is identifiable when
	# several modals are stacked.
	if _window and _window.has_method("set_title"):
		_window.call("set_title", display_name)
	var dialogue_text: String = str(npc.get("dialogue", "..."))
	if is_instance_valid(_dialogue):
		# Plain text (no italics) with default font colour — italics made the
		# line italic+dim which the user reported as "mờ".
		_dialogue.text = dialogue_text
	# Portrait lookup — fall back gracefully to a flat color when not mapped.
	var tex_path: String = NPC_SPRITE_PATH.get(npc_id, "")
	if is_instance_valid(_portrait):
		if not tex_path.is_empty() and ResourceLoader.exists(tex_path):
			_portrait.texture = load(tex_path)
			_portrait.modulate = Color(1, 1, 1, 1)
		else:
			_portrait.texture = null
			_portrait.modulate = Color(0.6, 0.5, 0.3, 1)
	var roles: Array = npc.get("roles", [])
	_set_role_visible(_shop_btn, "shop" in roles)
	_set_role_visible(_heal_btn, "heal" in roles)
	_set_role_visible(_appraise_btn, "appraise" in roles)
	_set_role_visible(_breed_btn, "breed" in roles or "breeding" in roles)
	_set_role_visible(_recipe_btn, "recipe" in roles)
	_set_role_visible(_quest_btn, "quest" in roles)
	_set_role_visible(_arena_btn, "arena" in roles)
	_bind_role(_shop_btn, _on_shop)
	_bind_role(_heal_btn, _on_heal)
	_bind_role(_appraise_btn, _on_appraise)
	_bind_role(_breed_btn, _on_breed)
	_bind_role(_recipe_btn, _on_recipe)
	_bind_role(_quest_btn, _on_quest)
	_bind_role(_arena_btn, _on_arena)


func _set_role_visible(btn: Control, visible: bool) -> void:
	if btn: btn.visible = visible


func _bind_role(btn: Control, method: Callable) -> void:
	if btn == null: return
	if btn.has_method("connect_pressed"):
		btn.call("connect_pressed", method)


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		_on_close()
		get_viewport().set_input_as_handled()


func _on_close() -> void:
	queue_free()


func _on_shop() -> void: PhimondClient.send("npc.shop", {"npc_id": npc_id})
func _on_heal() -> void: PhimondClient.heal_pets()
func _on_appraise() -> void:
	var pid := _first_pet_id()
	if not pid.is_empty(): PhimondClient.appraise(pid)


func _first_pet_id() -> String:
	var pets: Array = PhimondClient.state.get("pets", [])
	if pets.is_empty(): return ""
	return str(pets[0].get("id", ""))


func _on_breed() -> void:
	var pets: Array = PhimondClient.state.get("pets", [])
	if pets.size() < 2: return
	PhimondClient.synthesize(str(pets[0].id), str(pets[1].id), "default", false)


func _on_recipe() -> void:
	var recipes: Dictionary = PhimondClient.catalog.get("recipes", {})
	if recipes.is_empty(): return
	PhimondClient.learn_recipe(str(recipes.keys()[0]))


func _on_quest() -> void:
	var quests: Dictionary = PhimondClient.catalog.get("quests", {})
	if quests.is_empty(): return
	PhimondClient.accept_quest(str(quests.keys()[0]))


func _on_arena() -> void: PhimondClient.challenge_arena()