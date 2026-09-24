class_name GameWindow
extends Control
## GameWindow — fantasy-framed window with title bar, draggable header, close button.
## The component is a self-contained Control that can be dropped into any container.
##
## Anchor contract (default in GameWindow.tscn):
##   anchors_preset = 0 (top-left). Callers control position + size via offset_left,
##   offset_top, offset_right, offset_bottom — these are interpreted relative to the
##   parent's top-left corner.
## If a caller needs the window to fill its parent (full-bleed container with
## negative margins), they must explicitly set anchors_preset=15 + anchor_right=1.0
## + anchor_bottom=1.0 on the instance node — see BattleScene.tscn for an example.

## Emitted when the close (X) button is pressed.
signal close_requested
## Emitted when the user starts/stops dragging the title bar.
signal drag_started
signal drag_ended

const FRAME_MARGIN := 16  # matches panel_9slice texture_margin

@onready var _frame: NinePatchRect = $Frame
@onready var _title_bar: PanelContainer = $Frame/TitleBar
@onready var _title_label: Label = $Frame/TitleBar/HBox/TitleLabel
@onready var _close_btn: Button = $Frame/TitleBar/HBox/CloseBtn
@onready var _body: MarginContainer = $Frame/Body

var _drag_offset := Vector2.ZERO
var _dragging := false


func _ready() -> void:
	_close_btn.pressed.connect(_on_close_pressed)
	_title_bar.gui_input.connect(_on_title_bar_gui_input)


## Public API ------------------------------------------------------------

func set_title(text: String) -> void:
	if _title_label:
		_title_label.text = text


func set_close_callback(callable: Callable) -> void:
	# Re-wire the close signal to the caller's handler.
	if _close_btn.pressed.is_connected(_on_close_pressed):
		_close_btn.pressed.disconnect(_on_close_pressed)
	_close_btn.pressed.connect(callable)


func set_size_px(w: float, h: float) -> void:
	custom_minimum_size = Vector2(w, h)
	size = Vector2(w, h)


## Returns the body MarginContainer so callers can add children.
func get_body() -> MarginContainer:
	return _body


## Returns the inner content container above the body (margin removed) for
## direct manipulation if a caller needs raw access.
func get_body_container() -> Control:
	return _body.get_child(0) as Control if _body.get_child_count() > 0 else null


# Internal ----------------------------------------------------------------

func _on_close_pressed() -> void:
	close_requested.emit()


func _on_title_bar_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		var mb: InputEventMouseButton = event
		if mb.button_index == MOUSE_BUTTON_LEFT:
			if mb.pressed:
				_dragging = true
				_drag_offset = global_position - get_global_mouse_position()
				drag_started.emit()
			else:
				_dragging = false
				drag_ended.emit()
			accept_event()
	elif event is InputEventMouseMotion and _dragging:
		var mm: InputEventMouseMotion = event
		global_position = get_global_mouse_position() + _drag_offset