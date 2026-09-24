class_name GameButton
extends TextureButton
## GameButton — TextureButton + child Label + optional icon TextureRect.
##
## The component renders its own fantasy frame via the project theme, and shows
## an optional icon + text label. Use set_label()/set_icon() to update.

const ICON_NODE_NAME := "Icon"
const LABEL_NODE_NAME := "Label"

@onready var _icon: TextureRect = get_node_or_null(ICON_NODE_NAME) as TextureRect
@onready var _label: Label = get_node_or_null(LABEL_NODE_NAME) as Label


## Public API ------------------------------------------------------------

func set_label(text: String) -> void:
	if _label:
		_label.text = text


func get_label() -> String:
	return _label.text if _label else ""


func set_icon(path: String) -> void:
	if _icon == null:
		return
	if path.is_empty():
		_icon.visible = false
		_icon.texture = null
		return
	_icon.visible = true
	var tex: Texture2D = load(path)
	if tex == null:
		push_warning("GameButton.set_icon: failed to load '%s'" % path)
		_icon.visible = false
		return
	_icon.texture = tex


func set_icon_texture(tex: Texture2D) -> void:
	if _icon == null:
		return
	if tex == null:
		_icon.visible = false
		_icon.texture = null
		return
	_icon.visible = true
	_icon.texture = tex


## Connect a Callable to be invoked on press (wraps pressed signal).
func connect_pressed(callable: Callable) -> void:
	if pressed.is_connected(callable):
		return
	pressed.connect(callable)