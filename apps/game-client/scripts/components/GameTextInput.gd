class_name GameTextInput
extends LineEdit
## GameTextInput — fantasy-styled single-line text input.
##
## Wraps LineEdit with sensible defaults (theme is applied via the project
## theme already). Exposes set_text_value/set_placeholder_value + a focus() helper.

signal input_submitted(text: String)


func _ready() -> void:
	text_submitted.connect(_on_text_submitted)


## Public API ------------------------------------------------------------

func set_text_value(value: String) -> void:
	text = value


func set_placeholder_value(value: String) -> void:
	placeholder_text = value


func focus_input() -> void:
	grab_focus()


## Internal ----------------------------------------------------------------

func _on_text_submitted(text: String) -> void:
	input_submitted.emit(text)