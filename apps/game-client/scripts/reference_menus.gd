extends RefCounted
## World-region menus. All numbers and actions come from the authoritative client.
## Ranch is a source-styled adaptation: its original screen is not in the video.

var selected_pet_id := ""
var pet_tab := "Attributes"
var selected_item_id := ""
var bag_page := 0
var selected_quest_id := ""
var ranch_tab := "Synthesis"
var parent_a := ""
var parent_b := ""
var recipe_id := ""
var blessing := false
var confirmation: Dictionary = {}
var notice := ""
var selected_skill_id := ""
var _client: Node
var _navigate: Callable
var _page := ""
var _art = preload("res://scripts/reference_art.gd").new()

func build(page: String, parent: VBoxContainer, client: Node, navigate: Callable) -> void:
	if page != _page:
		confirmation.clear()
		notice = ""
	_client = client
	_navigate = navigate
	_page = page
	parent.add_theme_constant_override("separation", 5)
	match page.to_lower():
		"pets", "companions": _pets(parent)
		"inventory", "supplies": _inventory(parent)
		"quests": _quests(parent)
		"ranch": _ranch(parent)
		_: _text(parent, "This menu is unavailable.")
	if not notice.is_empty(): _text(parent, notice, Color("ffd57f"))
	if not confirmation.is_empty():
		_text(parent, str(confirmation.message), Color("ffd57f"))
		var row := _row(parent)
		_button(row, "Confirm", func():
			var intent := confirmation.duplicate(true)
			confirmation.clear()
			_client.send(str(intent.op), intent.data)
			_refresh())
		_button(row, "Cancel", func(): confirmation.clear(); _refresh())

func _refresh() -> void:
	_navigate.call(_page)

func _pet_list() -> Array:
	var pets: Variant = _client.state.get("pets", [])
	var entries: Array = pets.values() if pets is Dictionary else pets
	return entries.filter(func(pet): return not pet.get("retired", false))

func _pet(id: String) -> Dictionary:
	for pet in _pet_list():
		if str(pet.get("id", "")) == id: return pet
	return {}

func _pets(parent: VBoxContainer) -> void:
	var pets := _pet_list()
	if pets.is_empty():
		_text(parent, "No companions.")
		return
	if _pet(selected_pet_id).is_empty(): selected_pet_id = str(pets[0].id)
	var columns := _row(parent)
	columns.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var list := _scroll(columns, 170)
	for pet in pets:
		var id := str(pet.id)
		var active := id == str(_client.state.get("active_pet_id", ""))
		_button(list, "%s%s  Lv.%s" % ["◆ " if active else "", pet.get("name", "Pet"), pet.get("level", 1)], func(): selected_pet_id = id; _refresh(), id == selected_pet_id)
	var detail := VBoxContainer.new()
	detail.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	columns.add_child(detail)
	var pet := _pet(selected_pet_id)
	var header := _row(detail)
	_art.prepare()
	var portrait := TextureRect.new()
	portrait.texture = _art.pet_texture(str(pet.get("species_id", "")), 0.0)
	portrait.custom_minimum_size = Vector2(62, 64)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	header.add_child(portrait)
	var species: Dictionary = _client.catalog.get("species", {}).get(pet.get("species_id", ""), {})
	_text(header, "%s   Lv.%s   %s★   %s\n%s   Generation %s" % [pet.get("name", "Pet"), pet.get("level", 1), pet.get("star", 1), pet.get("gender", "?"), species.get("race", pet.get("species_id", "")), pet.get("generation", 0)], Color("ffe1a0"))
	var tabs := _row(detail)
	for tab in ["Attributes", "Resistance", "Skills", "Growth"]:
		_button(tabs, tab, func(): pet_tab = tab; _refresh(), pet_tab == tab)
	var body := _scroll(detail)
	body.get_parent().custom_minimum_size.y = 195
	match pet_tab:
		"Attributes":
			var attributes := _row(body)
			var stats := GridContainer.new()
			stats.columns = 2
			stats.size_flags_horizontal = Control.SIZE_EXPAND_FILL
			stats.add_theme_constant_override("h_separation", 24)
			attributes.add_child(stats)
			for key in ["attack", "defense", "speed", "magic", "strength", "vitality", "agility", "intelligence"]:
				if pet.has(key): _text(stats, "%s  %s" % [key.capitalize(), pet[key]])
			var bars := VBoxContainer.new()
			bars.custom_minimum_size.x = 155
			attributes.add_child(bars)
			for key in ["hp", "mp"]:
				_text(bars, "%s  %s / %s" % [key.to_upper(), pet.get(key, 0), pet.get("max_" + key, 0)])
				var bar := TextureProgressBar.new()
				bar.texture_progress = load("res://assets/reference/hud/bar_" + key + ".png")
				bar.nine_patch_stretch = true
				bar.custom_minimum_size = Vector2(155, 9)
				bar.max_value = maxi(1, int(pet.get("max_" + key, 0)))
				bar.value = int(pet.get(key, 0))
				bars.add_child(bar)
			_text(bars, "EXP  %s" % pet.get("xp", 0))
		"Resistance":
			_values(body, pet.get("resistances", {}), "Element resistances unavailable until appraisal.")
			_values(body, pet.get("status_resistances", {}), "Status resistances unavailable until appraisal.")
		"Growth":
			_text(body, "Growth", Color("8fe7ed"))
			_values(body, pet.get("growth", {}), "Appraise this companion to reveal its growth.")
			_text(body, "Quality", Color("8fe7ed"))
			_values(body, pet.get("quality", {}), "Quality has not been revealed.")
		"Skills":
			for skill_id in pet.get("skills", []):
				var skill: Dictionary = _client.catalog.get("skills", {}).get(skill_id, {})
				var label := _text(body, "%s   MP %s   %s" % [skill.get("name", skill_id), skill.get("mp_cost", 0), skill.get("element", "")])
				label.tooltip_text = str(skill.get("description", ""))
			var learn_row := _row(body)
			_picker(learn_row, "Chọn kỹ năng để học", _client.catalog.get("skills", {}).values(), selected_skill_id, func(id): selected_skill_id = id; _refresh())
			var learn := _button(learn_row, "Học", func(): _client.send("pet.learn", {"pet_id": selected_pet_id, "skill_id": selected_skill_id}))
			learn.disabled = selected_skill_id.is_empty() or selected_skill_id in pet.get("skills", [])
	var actions := _row(detail)
	_button(actions, "Follow", func(): _client.activate(selected_pet_id))
	_button(actions, "Appraise", func(): _client.appraise(selected_pet_id))
	_button(actions, "Ranch", func(): parent_a = selected_pet_id; _navigate.call("Ranch"))
	var release := _button(actions, "Thả…", func(): _confirm("Thả %s? Linh thú sẽ rời đội; phả hệ được giữ lại." % pet.get("name", ""), "pet.release", {"pet_id": selected_pet_id}))
	release.disabled = selected_pet_id == str(_client.state.get("active_pet_id", ""))

func _inventory(parent: VBoxContainer) -> void:
	var inventory: Dictionary = _client.state.get("inventory", {})
	var ids: Array = inventory.keys().filter(func(id): return int(inventory[id]) > 0)
	ids.sort()
	var page_count := maxi(1, ceili(ids.size() / 24.0))
	bag_page = clampi(bag_page, 0, page_count - 1)
	var top := _row(parent)
	_text(top, "Gold  %s" % _client.state.get("gold", 0), Color("ffe1a0"))
	_button(top, "◀", func(): bag_page = maxi(0, bag_page - 1); _refresh())
	_text(top, "%d / %d" % [bag_page + 1, page_count])
	_button(top, "▶", func(): bag_page = mini(page_count - 1, bag_page + 1); _refresh())
	var layout := _row(parent)
	var grid := GridContainer.new()
	grid.columns = 6
	grid.add_theme_constant_override("h_separation", 3)
	grid.add_theme_constant_override("v_separation", 3)
	layout.add_child(grid)
	for index in 24:
		var offset := bag_page * 24 + index
		var id := str(ids[offset]) if offset < ids.size() else ""
		var item: Dictionary = _client.catalog.get("items", {}).get(id, {})
		var slot := _button(grid, str(item.get("name", id)) if not id.is_empty() else "", func(): selected_item_id = id; _refresh(), id == selected_item_id and not id.is_empty())
		slot.custom_minimum_size = Vector2(67, 59)
		slot.clip_text = true
		slot.add_theme_font_size_override("font_size", 10)
		slot.add_theme_stylebox_override("normal", _style("slot_light" if id == selected_item_id and not id.is_empty() else "slot"))
		slot.tooltip_text = "%s\n%s" % [item.get("name", id), item.get("description", item.get("kind", ""))]
		if not id.is_empty():
			var quantity := Label.new()
			quantity.text = str(inventory[id])
			quantity.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
			quantity.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
			quantity.vertical_alignment = VERTICAL_ALIGNMENT_BOTTOM
			quantity.offset_right = -5
			quantity.offset_bottom = -3
			quantity.mouse_filter = Control.MOUSE_FILTER_IGNORE
			quantity.add_theme_font_size_override("font_size", 12)
			slot.add_child(quantity)
	var tooltip := VBoxContainer.new()
	tooltip.custom_minimum_size.x = 195
	tooltip.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	layout.add_child(tooltip)
	if selected_item_id in ids:
		var item: Dictionary = _client.catalog.get("items", {}).get(selected_item_id, {})
		_text(tooltip, str(item.get("name", selected_item_id)), Color("8fe7ed"))
		_text(tooltip, "%s   ×%s" % [item.get("kind", "Item"), inventory[selected_item_id]])
		_text(tooltip, str(item.get("description", "")))
		if item.has("power"): _text(tooltip, "Power  %s" % item.power)
		_text(tooltip, "Select items from the battle bag when fighting.")
	else:
		_text(tooltip, "Select an item to inspect it.")

func _quests(parent: VBoxContainer) -> void:
	var quests: Dictionary = _client.catalog.get("quests", {})
	if quests.is_empty():
		_text(parent, "No quests available.")
		return
	if not quests.has(selected_quest_id): selected_quest_id = str(quests.keys()[0])
	var columns := _row(parent)
	columns.size_flags_vertical = Control.SIZE_EXPAND_FILL
	var list := _scroll(columns, 220)
	for id in quests:
		_button(list, str(quests[id].get("name", id)), func(): selected_quest_id = id; _refresh(), id == selected_quest_id)
	var detail := VBoxContainer.new()
	detail.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	columns.add_child(detail)
	var quest: Dictionary = quests[selected_quest_id]
	var progress: Dictionary = _client.state.get("quests", {}).get(selected_quest_id, {})
	_text(detail, str(quest.get("name", selected_quest_id)), Color("ffe1a0"))
	_text(detail, str(quest.get("description", "")))
	_text(detail, "Progress  %s / %s" % [progress.get("progress", 0), quest.get("count", 1)], Color("8fe7ed"))
	_text(detail, "Reward  %s gold   %s EXP" % [quest.get("gold", 0), quest.get("xp", 0)])
	for id in quest.get("items", {}):
		_text(detail, "%s ×%s" % [_client.catalog.get("items", {}).get(id, {}).get("name", id), quest.items[id]])
	if not str(quest.get("recipe", "")).is_empty(): _text(detail, "Recipe: " + str(_client.catalog.get("recipes", {}).get(quest.recipe, {}).get("name", quest.recipe)))
	if progress.is_empty():
		_button(detail, "Accept quest", func(): _client.accept_quest(selected_quest_id))
	elif progress.get("claimed", false):
		_text(detail, "Reward claimed")
	else:
		var claim := _button(detail, "Claim reward", func(): _client.claim_quest(selected_quest_id))
		claim.disabled = int(progress.get("progress", 0)) < int(quest.get("count", 1))

func _ranch(parent: VBoxContainer) -> void:
	var tabs := _row(parent)
	for tab in ["Synthesis", "Strengthen", "Appraise"]:
		_button(tabs, tab, func(): ranch_tab = tab; confirmation.clear(); notice = ""; _refresh(), tab == ranch_tab)
	var pets := _pet_list()
	var choices := _row(parent)
	_picker(choices, "Choose companion", pets, parent_a, func(id): parent_a = id; confirmation.clear(); _refresh())
	if ranch_tab != "Appraise":
		_picker(choices, "Choose second companion", pets, parent_b, func(id): parent_b = id; confirmation.clear(); _refresh())
	if ranch_tab == "Appraise":
		_text(parent, "Appraisal reveals quality, growth and resistances. Requires the appropriate NPC.")
		var appraise := _button(parent, "Appraise selected companion", func(): _client.appraise(parent_a))
		appraise.disabled = _pet(parent_a).is_empty()
		return
	if ranch_tab == "Strengthen":
		_text(parent, "The second companion is consumed to strengthen the first.")
		_button(parent, "Strengthen…", func():
			if not _valid_parents(): return
			_confirm("Consume %s to strengthen %s?" % [_pet(parent_b).get("name", parent_b), _pet(parent_a).get("name", parent_a)], "pet.strengthen", {"pet_id": parent_a, "donor_id": parent_b}))
		return
	var recipes: Array = _client.catalog.get("recipes", {}).values()
	_picker(parent, "Choose recipe", recipes, recipe_id, func(id): recipe_id = id; confirmation.clear(); _refresh())
	var recipe: Dictionary = _client.catalog.get("recipes", {}).get(recipe_id, {})
	if not recipe.is_empty():
		_text(parent, "%s + %s → %s\nParent Lv.%s · Trainer Lv.%s · %s gold · %s souls\nOpposite gender: %s · Same star: %s · Cross race: %s · Consumes parents: %s" % [recipe.get("parent_a", ""), recipe.get("parent_b", ""), recipe.get("result", ""), recipe.get("min_level", 0), recipe.get("min_player_level", 0), recipe.get("gold_cost", 0), recipe.get("soul_cost", 0), recipe.get("opposite_gender", false), recipe.get("same_star", false), recipe.get("cross_race", false), recipe.get("consume_parents", false)])
	var row := _row(parent)
	var check := CheckBox.new()
	check.text = "Blessing"
	check.button_pressed = blessing
	check.toggled.connect(func(value): blessing = value; confirmation.clear(); _refresh())
	row.add_child(check)
	if not recipe.is_empty() and not recipe_id in _client.state.get("recipes", []):
		_button(row, "Learn recipe", func(): _client.learn_recipe(recipe_id))
	else:
		_button(row, "Synthesize…", func():
			if not _valid_parents(): return
			if recipe.is_empty(): notice = "Choose a recipe first."; _refresh(); return
			_confirm("Synthesize %s + %s? %s gold, %s souls. %s%s" % [_pet(parent_a).get("name", parent_a), _pet(parent_b).get("name", parent_b), recipe.get("gold_cost", 0), recipe.get("soul_cost", 0), "Both parents will be consumed." if recipe.get("consume_parents", false) else "Parents are retained.", " Blessing requested." if blessing else ""], "breeding.synthesize", {"parent_a": parent_a, "parent_b": parent_b, "recipe_id": recipe_id, "blessing": 1 if blessing else 0}))

func _valid_parents() -> bool:
	if _pet(parent_a).is_empty() or _pet(parent_b).is_empty() or parent_a == parent_b:
		notice = "Choose two different companions."
		_refresh()
		return false
	return true

func _confirm(message: String, op: String, data: Dictionary) -> void:
	notice = ""
	confirmation = {"message": message, "op": op, "data": data}
	_refresh()

func _picker(parent: Node, title: String, entries: Array, selected_id: String, callback: Callable) -> void:
	var picker := OptionButton.new()
	picker.custom_minimum_size.x = 200
	picker.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	picker.add_item(title)
	picker.set_item_metadata(0, "")
	for entry in entries:
		picker.add_item(str(entry.get("name", entry.id)))
		picker.set_item_metadata(picker.item_count - 1, str(entry.id))
		if str(entry.id) == selected_id: picker.select(picker.item_count - 1)
	picker.item_selected.connect(func(index): callback.call(str(picker.get_item_metadata(index))))
	parent.add_child(picker)

func _values(parent: Node, values: Dictionary, empty: String) -> void:
	if values.is_empty(): _text(parent, empty); return
	var grid := GridContainer.new()
	grid.columns = 2
	grid.add_theme_constant_override("h_separation", 24)
	parent.add_child(grid)
	for key in values: _text(grid, "%s  %s" % [str(key).capitalize(), values[key]], Color("a9e4e8"))

func _row(parent: Node) -> HBoxContainer:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 8)
	parent.add_child(row)
	return row

func _scroll(parent: Node, width: float = 0) -> VBoxContainer:
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size.x = width
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL if width == 0 else Control.SIZE_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	parent.add_child(scroll)
	var box := VBoxContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(box)
	return box

func _text(parent: Node, value: String, color: Color = Color("eee4c6")) -> Label:
	var label := Label.new()
	label.text = value
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", color)
	label.add_theme_color_override("font_outline_color", Color("001322"))
	label.add_theme_constant_override("outline_size", 2)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(label)
	return label

func _style(asset: String) -> StyleBoxTexture:
	var style := StyleBoxTexture.new()
	style.texture = load("res://assets/reference/hud/" + asset + ".png")
	for edge in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]:
		style.set_texture_margin(edge, 5)
		style.set_content_margin(edge, 4)
	return style

func _button(parent: Node, title: String, callback: Callable, selected: bool = false) -> Button:
	var button := Button.new()
	button.text = title
	button.custom_minimum_size.y = 27
	button.add_theme_font_size_override("font_size", 13)
	button.add_theme_color_override("font_color", Color("eee4c6"))
	button.add_theme_stylebox_override("normal", _style("row_selected" if selected else "row_menu"))
	button.add_theme_stylebox_override("hover", _style("row_selected"))
	button.add_theme_stylebox_override("pressed", _style("row_selected"))
	button.pressed.connect(callback)
	parent.add_child(button)
	return button
