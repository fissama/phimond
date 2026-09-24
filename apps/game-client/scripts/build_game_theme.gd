extends SceneTree
## build_game_theme.gd — runtime-build GameTheme.tres with all overrides.
##
## Run once via:
##   godot --headless --quit-after 1 --script scripts/build_game_theme.gd
##
## Idempotent: replaces any existing styles/GameTheme.tres.
## All values come from styles/styleboxes/*.tres.

const OUT := "res://styles/GameTheme.tres"

func _initialize() -> void:
	var t := Theme.new()

	# Default font size + base font colour used by Label
	t.default_font_size = 14
	t.default_base_scale = 1.0

	# ---- Colors (used by all controls via theme_override) ----
	var gold := Color(0.78, 0.69, 0.47)           # warm gold #C7B377
	var gold_hover := Color(1.0, 0.85, 0.55)
	var gold_dim := Color(0.55, 0.45, 0.28)
	var text_dark := Color(0.04, 0.08, 0.12)      # on light bg
	var text_white := Color(0.95, 0.93, 0.88)
	var caret_gold := Color(1.0, 0.85, 0.4)

	# ---- StyleBoxes ----
	var sb_panel := load("res://styles/styleboxes/panel_9slice.tres") as StyleBoxTexture
	var sb_le := load("res://styles/styleboxes/lineedit_frame.tres") as StyleBoxTexture
	var sb_btn_n := load("res://styles/styleboxes/button_normal.tres") as StyleBoxTexture
	var sb_btn_h := load("res://styles/styleboxes/button_hover.tres") as StyleBoxTexture
	var sb_btn_p := load("res://styles/styleboxes/button_pressed.tres") as StyleBoxTexture
	var sb_btn_d := load("res://styles/styleboxes/button_disabled.tres") as StyleBoxTexture
	var sb_tab_s := load("res://styles/styleboxes/tab_selected.tres") as StyleBoxTexture
	var sb_tab_u := load("res://styles/styleboxes/tab_unselected.tres") as StyleBoxTexture
	var sb_pb_bg := load("res://styles/styleboxes/progress_bg.tres") as StyleBoxTexture
	var sb_pb_fg := load("res://styles/styleboxes/progress_fg.tres") as StyleBoxTexture
	var sb_chat := load("res://styles/styleboxes/chat_panel.tres") as StyleBoxTexture
	var sb_top := load("res://styles/styleboxes/top_hud.tres") as StyleBoxTexture

	# ---- Button (9-slice panel frame + fantasy colors) ----
	t.set_stylebox("normal", "Button", sb_btn_n)
	t.set_stylebox("hover", "Button", sb_btn_h)
	t.set_stylebox("pressed", "Button", sb_btn_p)
	t.set_stylebox("disabled", "Button", sb_btn_d)
	t.set_stylebox("focus", "Button", sb_btn_h)
	t.set_color("font_color", "Button", text_white)
	t.set_color("font_hover_color", "Button", gold_hover)
	t.set_color("font_pressed_color", "Button", gold_dim)
	t.set_color("font_disabled_color", "Button", Color(0.5, 0.5, 0.5))
	t.set_color("font_focus_color", "Button", gold_hover)
	t.set_font_size("font_size", "Button", 14)
	t.set_constant("h_separation", "Button", 8)
	t.set_constant("outline_size", "Button", 0)

	# ---- TextureButton (same color overrides; textures set per-instance) ----
	t.set_color("font_color", "TextureButton", text_white)
	t.set_color("font_hover_color", "TextureButton", gold_hover)
	t.set_color("font_pressed_color", "TextureButton", gold_dim)
	t.set_color("font_disabled_color", "TextureButton", Color(0.5, 0.5, 0.5))
	t.set_font_size("font_size", "TextureButton", 14)

	# ---- LineEdit ----
	t.set_stylebox("normal", "LineEdit", sb_le)
	t.set_stylebox("focus", "LineEdit", sb_le)
	t.set_stylebox("read_only", "LineEdit", sb_le)
	t.set_color("font_color", "LineEdit", text_white)
	t.set_color("font_selected_color", "LineEdit", gold)
	t.set_color("font_uneditable_color", "LineEdit", Color(0.5, 0.5, 0.5))
	t.set_color("font_placeholder_color", "LineEdit", Color(0.5, 0.5, 0.55, 0.8))
	t.set_color("caret_color", "LineEdit", caret_gold)
	t.set_color("selection_color", "LineEdit", Color(0.78, 0.69, 0.47, 0.4))
	t.set_color("clear_button_color", "LineEdit", gold)
	t.set_color("clear_button_color_pressed", "LineEdit", gold_hover)
	t.set_font_size("font_size", "LineEdit", 14)
	t.set_constant("minimum_character_width", "LineEdit", 8)
	t.set_constant("caret_width", "LineEdit", 2)

	# ---- PanelContainer (default frame) ----
	t.set_stylebox("panel", "PanelContainer", sb_panel)

	# ---- Panel ----
	t.set_stylebox("panel", "Panel", sb_panel)

	# ---- Label (default gold text) ----
	t.set_color("font_color", "Label", gold)
	t.set_color("font_shadow_color", "Label", Color(0, 0, 0, 0.6))
	t.set_constant("shadow_offset_x", "Label", 1)
	t.set_constant("shadow_offset_y", "Label", 1)
	t.set_font_size("font_size", "Label", 14)
	t.set_constant("line_spacing", "Label", 2)

	# ---- RichTextLabel ----
	t.set_color("default_color", "RichTextLabel", gold)
	t.set_color("font_shadow_color", "RichTextLabel", Color(0, 0, 0, 0.6))
	t.set_color("font_outline_color", "RichTextLabel", Color(0, 0, 0, 0.7))
	t.set_constant("shadow_offset_x", "RichTextLabel", 1)
	t.set_constant("shadow_offset_y", "RichTextLabel", 1)

	# ---- ButtonGroup (used by tab toggles via radio set) ----

	# ---- TabContainer ----
	# Use tab_selected/tab_unselected styleboxes for tab backgrounds
	t.set_stylebox("tab_selected", "TabContainer", sb_tab_s)
	t.set_stylebox("tab_unselected", "TabContainer", sb_tab_u)
	t.set_stylebox("tab_selected_close", "TabContainer", sb_tab_s)
	t.set_stylebox("tab_unselected_close", "TabContainer", sb_tab_u)
	t.set_stylebox("panel", "TabContainer", sb_panel)
	t.set_color("font_selected_color", "TabContainer", gold_hover)
	t.set_color("font_unselected_color", "TabContainer", gold)
	t.set_color("font_disabled_color", "TabContainer", Color(0.5, 0.5, 0.5))
	t.set_font_size("font_size", "TabContainer", 14)
	t.set_constant("side_margin", "TabContainer", 8)
	t.set_constant("h_separation", "TabContainer", 4)

	# ---- ProgressBar ----
	t.set_stylebox("background", "ProgressBar", sb_pb_bg)
	t.set_stylebox("fill", "ProgressBar", sb_pb_fg)
	t.set_color("font_color", "ProgressBar", text_white)
	t.set_color("font_outline_color", "ProgressBar", Color(0, 0, 0, 0.7))
	t.set_font_size("font_size", "ProgressBar", 12)

	# ---- Tree ----
	t.set_stylebox("panel", "Tree", sb_panel)
	t.set_stylebox("bg", "Tree", sb_panel)
	t.set_stylebox("selected", "Tree", sb_btn_h)
	t.set_stylebox("selected_focus", "Tree", sb_btn_h)
	t.set_stylebox("cursor", "Tree", sb_btn_h)
	t.set_color("font_color", "Tree", text_white)
	t.set_color("font_selected_color", "Tree", text_dark)
	t.set_color("guide_color", "Tree", Color(0.4, 0.4, 0.5, 0.6))
	t.set_color("title_button_color", "Tree", gold)
	t.set_font_size("font_size", "Tree", 13)

	# ---- OptionButton ----
	t.set_stylebox("normal", "OptionButton", sb_btn_n)
	t.set_stylebox("hover", "OptionButton", sb_btn_h)
	t.set_stylebox("pressed", "OptionButton", sb_btn_p)
	t.set_stylebox("disabled", "OptionButton", sb_btn_d)
	t.set_stylebox("focus", "OptionButton", sb_btn_h)
	t.set_color("font_color", "OptionButton", text_white)
	t.set_color("font_hover_color", "OptionButton", gold_hover)
	t.set_color("font_pressed_color", "OptionButton", gold_dim)
	t.set_color("font_disabled_color", "OptionButton", Color(0.5, 0.5, 0.5))
	t.set_color("arrow_color", "OptionButton", gold)
	t.set_font_size("font_size", "OptionButton", 14)

	# ---- ScrollContainer ----
	# The v_scroll stylebox lives on the inner VScrollBar.
	t.set_stylebox("bg", "ScrollContainer", sb_panel)
	t.set_stylebox("panel", "ScrollContainer", sb_panel)

	# ---- VScrollBar / HScrollBar ----
	t.set_stylebox("scroll", "VScrollBar", sb_btn_n)
	t.set_stylebox("scroll", "HScrollBar", sb_btn_n)
	t.set_stylebox("grabber", "VScrollBar", sb_btn_h)
	t.set_stylebox("grabber", "HScrollBar", sb_btn_h)
	t.set_stylebox("grabber_highlight", "VScrollBar", sb_btn_h)
	t.set_stylebox("grabber_highlight", "HScrollBar", sb_btn_h)
	t.set_stylebox("grabber_pressed", "VScrollBar", sb_btn_p)
	t.set_stylebox("grabber_pressed", "HScrollBar", sb_btn_p)

	# ---- CheckBox / CheckButton ----
	t.set_color("font_color", "CheckBox", text_white)
	t.set_color("font_hover_color", "CheckBox", gold_hover)
	t.set_color("font_pressed_color", "CheckBox", gold_dim)
	t.set_color("font_disabled_color", "CheckBox", Color(0.5, 0.5, 0.5))
	t.set_font_size("font_size", "CheckBox", 13)
	t.set_color("font_color", "CheckButton", text_white)
	t.set_color("font_hover_color", "CheckButton", gold_hover)
	t.set_color("font_pressed_color", "CheckButton", gold_dim)
	t.set_color("font_disabled_color", "CheckButton", Color(0.5, 0.5, 0.5))
	t.set_font_size("font_size", "CheckButton", 13)

	# ---- PopupMenu / MenuBar ----
	t.set_stylebox("panel", "PopupMenu", sb_panel)
	t.set_stylebox("hover", "PopupMenu", sb_btn_h)
	t.set_stylebox("separator", "PopupMenu", sb_pb_bg)
	t.set_color("font_color", "PopupMenu", text_white)
	t.set_color("font_hover_color", "PopupMenu", text_dark)
	t.set_color("font_disabled_color", "PopupMenu", Color(0.5, 0.5, 0.5))
	t.set_font_size("font_size", "PopupMenu", 13)
	t.set_stylebox("normal", "MenuBar", sb_btn_n)
	t.set_stylebox("hover", "MenuBar", sb_btn_h)
	t.set_stylebox("pressed", "MenuBar", sb_btn_p)
	t.set_color("font_color", "MenuBar", text_white)
	t.set_color("font_hover_color", "MenuBar", gold_hover)

	# ---- WindowDialog / AcceptDialog (window chrome) ----
	t.set_stylebox("embedded_border", "Window", sb_panel)
	t.set_stylebox("embedded_unfocused_border", "Window", sb_panel)
	t.set_color("title_color", "Window", gold)
	t.set_font_size("title_font_size", "Window", 14)
	t.set_constant("title_height", "Window", 28)
	t.set_stylebox("panel", "AcceptDialog", sb_panel)
	t.set_stylebox("panel", "ConfirmationDialog", sb_panel)

	# ---- SpinBox ----
	t.set_stylebox("normal", "SpinBox", sb_le)
	t.set_color("font_color", "SpinBox", text_white)
	t.set_color("caret_color", "SpinBox", caret_gold)
	t.set_font_size("font_size", "SpinBox", 14)

	# Save the theme
	var err := ResourceSaver.save(t, OUT)
	if err != OK:
		push_error("save error %d for %s" % [err, OUT])
		quit(1)
		return
	print("[build_game_theme] wrote ", OUT)
	quit(0)