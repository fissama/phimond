class_name GameSlot
extends PanelContainer
## GameSlot — 32x32 fantasy inventory / equipment slot.
##
## Renders a frame (stylebox from theme), a centred item icon, and a small
## quantity label in the bottom-right corner. The slot is interactive
## (clickable + emits slot_clicked signal).

signal slot_clicked

const SIZE_DEFAULT := 32

@onready var _icon: TextureRect = $Margin/Icon
@onready var _qty_label: Label = $Margin/Qty


func _ready() -> void:
	custom_minimum_size = Vector2(SIZE_DEFAULT, SIZE_DEFAULT)
	# Use gui_input so PanelContainer (which lacks a pressed signal) can detect clicks.
	gui_input.connect(_on_gui_input)
	mouse_filter = Control.MOUSE_FILTER_STOP
	focus_mode = Control.FOCUS_ALL


## Public API ------------------------------------------------------------

## Set the slot's item icon. Pass an empty string or null to clear.
func set_item(icon_path: String, qty: int = 0) -> void:
	if icon_path.is_empty():
		_icon.texture = null
		_icon.visible = false
		_qty_label.visible = false
		return
	var tex: Texture2D = load(icon_path)
	if tex == null:
		push_warning("GameSlot.set_item: failed to load '%s'" % icon_path)
		_icon.texture = null
		_icon.visible = false
		_qty_label.visible = false
		return
	_icon.texture = tex
	_icon.visible = true
	if qty > 1:
		_qty_label.text = str(qty)
		_qty_label.visible = true
	else:
		_qty_label.visible = false


func set_item_texture(tex: Texture2D, qty: int = 0) -> void:
	if tex == null:
		_icon.texture = null
		_icon.visible = false
		_qty_label.visible = false
		return
	_icon.texture = tex
	_icon.visible = true
	if qty > 1:
		_qty_label.text = str(qty)
		_qty_label.visible = true
	else:
		_qty_label.visible = false


func clear() -> void:
	set_item("", 0)


## Connect a Callable to be invoked on slot click.
func set_click_callback(callable: Callable) -> void:
	if slot_clicked.is_connected(callable):
		return
	slot_clicked.connect(callable)


## Internal ----------------------------------------------------------------

func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		var mb: InputEventMouseButton = event
		if mb.button_index == MOUSE_BUTTON_LEFT and mb.pressed:
			slot_clicked.emit()
			accept_event()