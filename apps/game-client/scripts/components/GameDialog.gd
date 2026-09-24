class_name GameDialog
extends AcceptDialog
## GameDialog — small confirm dialog with Title, Body, OK + Cancel.
##
## Wraps Godot's AcceptDialog so callers can build quickly with one line.
## Use show_confirm(title, body, on_ok, on_cancel) for the simplest flow.

signal dialog_confirmed
signal dialog_canceled


@onready var _body_label: Label = $Panel/VBox/BodyLabel


func _ready() -> void:
	dialog_hide_on_ok = true
	# AcceptDialog already exposes a `confirmed` signal — forward it.
	if not confirmed.is_connected(_on_ok):
		confirmed.connect(_on_ok)
	if not close_requested.is_connected(_on_close):
		close_requested.connect(_on_close)


## Public API ------------------------------------------------------------

func set_title_text(text: String) -> void:
	title = text


func set_body_text(text: String) -> void:
	if _body_label:
		_body_label.text = text


func set_ok_text(text: String) -> void:
	ok_button_text = text


func show_confirm(title_text: String, body_text: String,
		on_ok: Callable = Callable(),
		on_cancel: Callable = Callable()) -> void:
	title = title_text
	if _body_label:
		_body_label.text = body_text
	if on_ok.is_valid() and not dialog_confirmed.is_connected(on_ok):
		dialog_confirmed.connect(on_ok)
	if on_cancel.is_valid() and not dialog_canceled.is_connected(on_cancel):
		dialog_canceled.connect(on_cancel)
	popup_centered()


## Internal ----------------------------------------------------------------

func _on_ok() -> void:
	dialog_confirmed.emit()


func _on_close() -> void:
	dialog_canceled.emit()