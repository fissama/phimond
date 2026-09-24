extends Control
## test_theme.gd — runtime driver for scenes/test_theme.tscn.
## Populates component instances with sample data so the scene has visible content.

@onready var _window: Control = $Window
@onready var _button1: Control = $ButtonsRow/Button1
@onready var _button2: Control = $ButtonsRow/Button2
@onready var _tab1: Control = $TabsRow/Tab1
@onready var _tab2: Control = $TabsRow/Tab2
@onready var _slot1: Control = $SlotsRow/Slot1
@onready var _slot2: Control = $SlotsRow/Slot2
@onready var _slot3: Control = $SlotsRow/Slot3
@onready var _slot4: Control = $SlotsRow/Slot4
@onready var _text_input: Control = $SidePanel/TextInput
@onready var _hp_bar: Control = $SidePanel/HPBar
@onready var _mp_bar: Control = $SidePanel/MPBar
@onready var _status: Label = $StatusLabel


func _ready() -> void:
	# Window
	if _window and _window.has_method("set_title"):
		_window.call("set_title", "Inventory")
	if _window and _window.has_method("set_close_callback"):
		_window.call("set_close_callback", _on_window_close)

	# Buttons
	if _button1:
		if _button1.has_method("set_label"):
			_button1.call("set_label", "Use")
		if _button1.has_method("connect_pressed"):
			_button1.call("connect_pressed", _on_button_use)
	if _button2:
		if _button2.has_method("set_label"):
			_button2.call("set_label", "Drop")
		if _button2.has_method("connect_pressed"):
			_button2.call("connect_pressed", _on_button_drop)

	# Tabs
	if _tab1:
		if _tab1.has_method("set_text_label"):
			_tab1.call("set_text_label", "Bags")
		if _tab1.has_method("set_selected"):
			_tab1.call("set_selected", true)
	if _tab2:
		if _tab2.has_method("set_text_label"):
			_tab2.call("set_text_label", "Equip")

	# Slots
	if _slot1:
		# Slot 1 stays empty (frame only)
		pass
	if _slot2:
		if _slot2.has_method("set_item"):
			_slot2.call("set_item", "res://assets/reference/ui/right_btn0.png", 0)
	if _slot3:
		if _slot3.has_method("set_item"):
			_slot3.call("set_item", "res://assets/reference/actors/Boy/Idle/000.png", 12)
	if _slot4:
		if _slot4.has_method("set_item"):
			_slot4.call("set_item", "res://assets/reference/actors/Boy/Run/000.png", 99)

	# TextInput
	if _text_input:
		if _text_input.has_method("set_placeholder_value"):
			_text_input.call("set_placeholder_value", "Search items…")

	# Bars
	if _hp_bar:
		if _hp_bar.has_method("set_value_instant"):
			_hp_bar.call("set_value_instant", 75.0)
	if _mp_bar:
		if _mp_bar.has_method("set_value_instant"):
			_mp_bar.call("set_value_instant", 40.0)

	_status.text = "test_theme.tscn loaded — all components instantiated"


func _on_window_close() -> void:
	_status.text = "Window close pressed"


func _on_button_use() -> void:
	_status.text = "Use pressed"


func _on_button_drop() -> void:
	_status.text = "Drop pressed"