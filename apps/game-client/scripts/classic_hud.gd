extends Control

signal page_requested(page: String)
signal command_requested(command: String)
signal move_started(direction: String)
signal move_stopped

const Art = preload("res://scripts/reference_art.gd")
const Room = preload("res://scripts/room.gd")
var art = Art.new()
var world: Control
var content_box: VBoxContainer
var menu: PanelContainer
var menu_backing: ColorRect
var status: Label
var detail: Label
var log_text: RichTextLabel
var title: Label
var meta: Label
var name_label: Label
var hp_label: Label
var mp_label: Label
var hp_fill: TextureRect
var mp_fill: TextureRect
var portrait: TextureRect
var battle_bar: Control
var battle_buttons: Array[Button] = []
var auto_button: Button
var turn_label: Label
var field_controls: Array[Control] = []

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	art.prepare()
	world = Room.new()
	world.position = Vector2.ZERO
	world.size = Vector2(960, 454)
	add_child(world)
	# Original atlas slices retain the same field/control-strip proportions as the video.
	_picture("panel_controls", Rect2(0, 454, 245, 186))
	_picture("frame_chat", Rect2(245, 454, 518, 186))
	_picture("panel_controls", Rect2(763, 454, 197, 186))
	_picture("dpad", Rect2(31, 461, 184, 178))
	var left := _hit("", Rect2(26, 510, 65, 77), "Đi trái · A / ←")
	left.button_down.connect(func(): move_started.emit("left"))
	left.button_up.connect(func(): move_stopped.emit())
	var right := _hit("", Rect2(151, 510, 65, 77), "Đi phải · D / →")
	right.button_down.connect(func(): move_started.emit("right"))
	right.button_up.connect(func(): move_stopped.emit())
	var up := _hit("", Rect2(92, 462, 60, 60), "Đi lên · W / ↑")
	up.button_down.connect(func(): move_started.emit("up"))
	up.button_up.connect(func(): move_stopped.emit())
	var down := _hit("", Rect2(92, 581, 60, 59), "Đi xuống · S / ↓")
	down.button_down.connect(func(): move_started.emit("down"))
	down.button_up.connect(func(): move_stopped.emit())
	var center := _hit("", Rect2(92, 523, 60, 57), "Mở menu · Esc")
	center.pressed.connect(func(): page_requested.emit("Menu"))
	_label("Hệ thống", Rect2(256, 459, 105, 21), 15, Color("133c54"))
	status = _label("Chào mừng đến Phimond", Rect2(357, 461, 397, 21), 12, Color("17405a"))
	status.clip_text = true
	log_text = RichTextLabel.new()
	log_text.position = Vector2(257, 487)
	log_text.size = Vector2(494, 117)
	log_text.add_theme_color_override("default_color", Color("123548"))
	log_text.add_theme_font_size_override("normal_font_size", 15)
	log_text.add_theme_constant_override("outline_size", 0)
	log_text.add_theme_constant_override("shadow_offset_x", 0)
	log_text.add_theme_constant_override("shadow_offset_y", 0)
	log_text.scroll_following = true
	add_child(log_text)
	detail = _label("A / D: di chuyển    E: tương tác    Esc: menu", Rect2(256, 612, 500, 20), 12, Color("1a4355"))
	detail.clip_text = true
	var accept := _image_button("button_confirm", "Chọn", Rect2(785, 466, 157, 78), "Tương tác / tấn công · Space")
	accept.pressed.connect(func(): command_requested.emit("confirm"))
	var back := _image_button("button_back", "Trở về", Rect2(785, 548, 157, 78), "Đóng menu · Esc")
	back.pressed.connect(func(): command_requested.emit("back"))
	# Player and active companion occupy the original upper-left cluster.
	_picture("frame_bars", Rect2(48, 31, 187, 55))
	hp_fill = _picture("bar_hp", Rect2(71, 40, 142, 11))
	mp_fill = _picture("bar_mp", Rect2(92, 57, 138, 10))
	_picture("frame_portrait", Rect2(6, 5, 93, 88))
	portrait = TextureRect.new()
	portrait.position = Vector2(16, 14)
	portrait.size = Vector2(37, 41)
	portrait.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	portrait.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(portrait)
	var trainer := TextureRect.new()
	trainer.texture = art.actor_texture("Boy", "idle", 0)
	trainer.position = Vector2(47, 40)
	trainer.size = Vector2(33, 41)
	trainer.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	trainer.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	trainer.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(trainer)
	name_label = _label("PHIMOND", Rect2(68, 7, 204, 24), 16)
	hp_label = _label("", Rect2(114, 36, 110, 20), 11)
	mp_label = _label("", Rect2(114, 53, 110, 20), 11)
	var pet := _image_button("button_pet", "", Rect2(8, 98, 56, 58), "Linh thú")
	pet.pressed.connect(func(): page_requested.emit("Companions"))
	var quests := _image_button("button_quest", "", Rect2(8, 163, 56, 58), "Nhiệm vụ")
	quests.pressed.connect(func(): page_requested.emit("Quests"))
	title = _label("PHIMOND", Rect2(669, 9, 280, 27), 18)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	meta = _label("", Rect2(669, 38, 280, 22), 12)
	meta.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
	var menu_button := _image_button("button_settings", "", Rect2(894, 69, 54, 55), "Menu")
	menu_button.pressed.connect(func(): page_requested.emit("Menu"))
	_build_battle_bar()
	for child in get_children():
		if child is Control and child.position.y < 454: field_controls.append(child)
	_build_menu()

func _build_battle_bar() -> void:
	battle_bar = Control.new()
	battle_bar.position = Vector2(253, 100)
	battle_bar.size = Vector2(441, 82)
	battle_bar.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(battle_bar)
	_picture("battle_actions", Rect2(0, 12, 441, 70), battle_bar)
	var definitions := [["icon_auto", "Tự động", "auto"], ["icon_attack", "Đánh", "attack"], ["icon_magic", "Kỹ năng", "Skills"], ["icon_inventory", "Vật phẩm", "Items"], ["button_round", "Thủ", "defend"], ["icon_run", "Chạy", "flee"]]
	for i in range(definitions.size()):
		var definition: Array = definitions[i]
		var button := _image_button(str(definition[0]), "", Rect2(i * 70 + 22, 0, 42, 44), str(definition[1]), battle_bar)
		button.pressed.connect(func(): command_requested.emit(str(definition[2])))
		battle_buttons.append(button)
		if definition[2] == "auto": auto_button = button
		var label := _label(str(definition[1]), Rect2(i * 70 + 10, 45, 68, 19), 12, Color("fff3b8"), battle_bar)
		label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	turn_label = _label("", Rect2(80, 65, 230, 20), 13, Color("fff3b8"), battle_bar)
	turn_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	battle_bar.hide()

func _build_menu() -> void:
	menu_backing = ColorRect.new()
	menu_backing.color = Color("073054")
	menu_backing.mouse_filter = Control.MOUSE_FILTER_IGNORE
	menu_backing.hide()
	add_child(menu_backing)
	menu = PanelContainer.new()
	menu.position = Vector2(113, 94)
	menu.size = Vector2(734, 347)
	var frame := StyleBoxTexture.new()
	frame.texture = _texture("panel_menu")
	for edge in [SIDE_LEFT, SIDE_TOP, SIDE_RIGHT, SIDE_BOTTOM]:
		frame.set_texture_margin(edge, 34)
		frame.set_content_margin(edge, 24)
	frame.set_texture_margin(SIDE_LEFT, 112)
	frame.set_content_margin(SIDE_LEFT, 116)
	menu.add_theme_stylebox_override("panel", frame)
	add_child(menu)
	menu.visibility_changed.connect(func(): menu_backing.visible = menu.visible)
	var scroll := ScrollContainer.new()
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	menu.add_child(scroll)
	content_box = VBoxContainer.new()
	content_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	content_box.add_theme_constant_override("separation", 7)
	scroll.add_child(content_box)
	menu.hide()

func update_state(character: Dictionary, catalog: Dictionary, busy: bool, automatic: bool) -> void:
	menu_backing.position = menu.position + Vector2(90, 16)
	menu_backing.size = menu.size - Vector2(106, 32)
	var active: Dictionary = {}
	for pet in character.get("pets", []):
		if pet.get("id") == character.get("active_pet_id"): active = pet
	name_label.text = "%s · Lv.%d" % [character.get("name", "Phimond"), int(character.get("level", 1))]
	portrait.texture = art.pet_texture(str(active.get("species_id", "")), 0)
	var hp := float(active.get("hp", 0))
	var max_hp := maxf(float(active.get("max_hp", 1)), 1)
	var mp := float(active.get("mp", 0))
	var max_mp := maxf(float(active.get("max_mp", 1)), 1)
	hp_fill.size.x = 142 * clampf(hp / max_hp, 0, 1)
	mp_fill.size.x = 138 * clampf(mp / max_mp, 0, 1)
	hp_label.text = "%d / %d" % [hp, max_hp]
	mp_label.text = "%d / %d" % [mp, max_mp]
	var definition: Dictionary = catalog.get("maps", {}).get(character.get("map_id", ""), {})
	title.text = str(definition.get("name", "Phimond"))
	meta.text = "%d vàng   ·   %d pha lê" % [int(character.get("gold", 0)), int(character.get("crystals", 0))]
	var battle = character.get("battle")
	battle_bar.visible = battle is Dictionary
	if battle is Dictionary:
		turn_label.text = "Lượt %d%s" % [int(battle.get("turn", 1)), " · Đang xử lý…" if busy else (" · Tự động" if automatic else " · Chọn hành động")]
	for button in battle_buttons: button.disabled = busy and button != auto_button
	auto_button.modulate = Color("ffe077") if automatic else Color.WHITE

func _texture(id: String) -> Texture2D:
	return art.texture("res://assets/reference/hud/" + id + ".png")

func _picture(id: String, rect: Rect2, parent: Node = self) -> TextureRect:
	var picture := TextureRect.new()
	picture.texture = _texture(id)
	picture.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	picture.stretch_mode = TextureRect.STRETCH_SCALE
	picture.position = rect.position
	picture.size = rect.size
	picture.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(picture)
	return picture

func _hit(text: String, rect: Rect2, tip: String, parent: Node = self) -> Button:
	var button := Button.new()
	button.text = text
	button.position = rect.position
	button.size = rect.size
	button.tooltip_text = tip
	button.focus_mode = Control.FOCUS_NONE
	for state in ["normal", "hover", "pressed", "disabled", "focus"]:
		button.add_theme_stylebox_override(state, StyleBoxEmpty.new())
	button.add_theme_color_override("font_outline_color", Color("082540"))
	button.add_theme_constant_override("outline_size", 4)
	parent.add_child(button)
	return button

func _image_button(id: String, text: String, rect: Rect2, tip: String, parent: Node = self) -> Button:
	var button := _hit(text, rect, tip, parent)
	var picture := _picture(id, Rect2(Vector2.ZERO, rect.size), button)
	picture.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	picture.show_behind_parent = true
	button.mouse_entered.connect(func(): picture.modulate = Color(1.2, 1.2, 1.2))
	button.mouse_exited.connect(func(): picture.modulate = Color.WHITE)
	return button

func _label(text: String, rect: Rect2, font_size: int = 14, tint: Color = Color("fff0bb"), parent: Node = self) -> Label:
	var label := Label.new()
	label.text = text
	label.position = rect.position
	label.size = rect.size
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", tint)
	label.add_theme_constant_override("outline_size", 0)
	label.add_theme_constant_override("shadow_offset_x", 0)
	label.add_theme_constant_override("shadow_offset_y", 0)
	if rect.position.y < 454 and parent == self or parent == battle_bar:
		label.add_theme_color_override("font_outline_color", Color("142535"))
		label.add_theme_constant_override("outline_size", 3)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	parent.add_child(label)
	return label
