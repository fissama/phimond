extends Control
## ShopMenu — fantasy-framed shop popup. Header shows current gold, then a list of
## catalog items; each row is a GameSlot (icon) + item name + price label + a
## GameButton Buy. The window's close button queue_frees the popup.

const ROW_HEIGHT := 40

@onready var _window: Control = $Window
@onready var _gold_label: Label = $Window/Frame/Body/BodyContainer/BodyRoot/HeaderRow/GoldLabel
@onready var _item_list: VBoxContainer = $Window/Frame/Body/BodyContainer/BodyRoot/ItemList
@onready var _empty_label: Label = $Window/Frame/Body/BodyContainer/BodyRoot/EmptyLabel


func _ready() -> void:
	if _window and _window.has_method("set_title"):
		_window.call("set_title", "Shop")
	if _window and _window.has_method("set_close_callback"):
		_window.call("set_close_callback", _on_close)
	PhimondClient.state_updated.connect(_on_state_updated)
	_refresh()


func _on_state_updated(_rev: int, _c: Dictionary) -> void: _refresh()


func _refresh() -> void:
	if is_instance_valid(_gold_label):
		_gold_label.text = "Gold: %s" % str(PhimondClient.state.get("gold", 0))
	_rebuild_items()


func _rebuild_items() -> void:
	if _item_list == null: return
	for child in _item_list.get_children():
		child.queue_free()
	var items: Dictionary = PhimondClient.catalog.get("items", {})
	if items.is_empty():
		if is_instance_valid(_empty_label): _empty_label.visible = true
		return
	if is_instance_valid(_empty_label): _empty_label.visible = false
	var row_index := 0
	for id in items.keys():
		var item: Dictionary = items[id]
		var row: HBoxContainer = HBoxContainer.new()
		row.custom_minimum_size = Vector2(0, ROW_HEIGHT)
		row.add_theme_constant_override("separation", 10)
		row.add_theme_constant_override("alignment", 0)
		_item_list.add_child(row)
		# Slot icon — game slot frame from foundation.
		var slot_scene: PackedScene = load("res://scenes/components/GameSlot.tscn")
		var slot: Control = slot_scene.instantiate()
		if slot:
			row.add_child(slot)
			if slot.has_method("set_item"):
				var icon_path: String = str(item.get("icon", ""))
				if not icon_path.is_empty() and ResourceLoader.exists(icon_path):
					slot.call("set_item", icon_path, 0)
		# Item name (truncate fantasy-style if too long)
		var name_label: Label = Label.new()
		name_label.text = str(item.get("name", id))
		name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		name_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(name_label)
		# Price
		var price_label: Label = Label.new()
		price_label.text = "%s gold" % str(item.get("price", "?"))
		price_label.custom_minimum_size = Vector2(80, 0)
		price_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		price_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		row.add_child(price_label)
		# Buy button — distinct per-row via label text but uses the shared foundation GameButton.
		var btn_scene: PackedScene = load("res://scenes/components/GameButton.tscn")
		var buy_btn: Control = btn_scene.instantiate()
		if buy_btn:
			buy_btn.custom_minimum_size = Vector2(80, 36)
			row.add_child(buy_btn)
			if buy_btn.has_method("set_label"):
				buy_btn.call("set_label", "Buy")
			if buy_btn.has_method("connect_pressed"):
				buy_btn.call("connect_pressed", func(): _on_buy(str(id)))
		row_index += 1


func _on_buy(item_id: String) -> void:
	PhimondClient.buy(item_id, 1)


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo and event.keycode == KEY_ESCAPE:
		_on_close()
		get_viewport().set_input_as_handled()


func _on_close() -> void:
	queue_free()