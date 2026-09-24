class_name GameTab
extends Button
## GameTab — toggle tab button used in TabContainer / TabBar contexts.
##
## Has two visual states: selected (active) and unselected. The selected state
## uses the tab_selected stylebox; the unselected state uses tab_unselected.
## Toggling updates both the stylebox override and the modulate color.

const SEL_BG := "res://styles/styleboxes/tab_selected.tres"
const UNSEL_BG := "res://styles/styleboxes/tab_unselected.tres"

var _selected: bool = false
var _sel_sb: StyleBoxTexture = null
var _unsel_sb: StyleBoxTexture = null


func _ready() -> void:
	_sel_sb = load(SEL_BG) as StyleBoxTexture
	_unsel_sb = load(UNSEL_BG) as StyleBoxTexture
	toggle_mode = true
	focus_mode = Control.FOCUS_NONE
	_apply_state()


## Public API ------------------------------------------------------------

func set_selected(value: bool) -> void:
	_selected = value
	button_pressed = value
	_apply_state()


func is_selected() -> bool:
	return _selected


func set_text_label(text_value: String) -> void:
	text = text_value


## Internal ----------------------------------------------------------------

func _apply_state() -> void:
	if _selected:
		add_theme_stylebox_override("normal", _sel_sb)
		add_theme_stylebox_override("hover", _sel_sb)
		add_theme_stylebox_override("pressed", _sel_sb)
		add_theme_stylebox_override("focus", _sel_sb)
		modulate = Color(1, 1, 1, 1)
	else:
		add_theme_stylebox_override("normal", _unsel_sb)
		add_theme_stylebox_override("hover", _sel_sb)
		add_theme_stylebox_override("pressed", _sel_sb)
		add_theme_stylebox_override("focus", _unsel_sb)
		modulate = Color(0.85, 0.85, 0.85, 1)


func _toggled(button_pressed: bool) -> void:
	_selected = button_pressed
	_apply_state()