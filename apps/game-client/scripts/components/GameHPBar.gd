class_name GameHPBar
extends ProgressBar
## GameHPBar — fantasy-styled HP bar with tween-driven value changes.
##
## Tweens between values over `duration_ms` so HP drops feel snappy. The bar
## foreground can be tinted to any colour (default red for HP).

const DEFAULT_TINT := Color(0.7, 0.18, 0.18)   # red

var _tween: Tween = null
var _tint: Color = DEFAULT_TINT


func _ready() -> void:
	min_value = 0.0
	max_value = 100.0
	value = 100.0
	_apply_tint()


## Public API ------------------------------------------------------------

## Animate from current value to `target` over `duration_ms` milliseconds.
func tween_value(target: float, duration_ms: int = 250) -> void:
	if _tween and _tween.is_running():
		_tween.kill()
	_tween = create_tween()
	_tween.tween_property(self, "value", clampf(target, min_value, max_value), float(duration_ms) / 1000.0).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)


## Set the bar value immediately (no tween).
func set_value_instant(target: float) -> void:
	if _tween and _tween.is_running():
		_tween.kill()
	value = clampf(target, min_value, max_value)


## Update the maximum HP (e.g. on level-up).
func update_max(new_max: float, keep_ratio: bool = true) -> void:
	if keep_ratio and max_value > 0:
		var ratio := value / max_value
		max_value = new_max
		value = ratio * max_value
	else:
		max_value = new_max


## Set the foreground tint (e.g. red→green for poison).
func set_bar_tint(color: Color) -> void:
	_tint = color
	_apply_tint()


## Internal ----------------------------------------------------------------

func _apply_tint() -> void:
	# The ProgressBar fill StyleBox is a StyleBoxTexture with modulate_color.
	# Mutating its modulate_color at runtime keeps the theme intact for other
	# bars while letting HP/MP/exp get individual tints.
	var fill_box: StyleBoxTexture = get_theme_stylebox("fill") as StyleBoxTexture
	if fill_box:
		fill_box = fill_box.duplicate() as StyleBoxTexture
		fill_box.modulate_color = _tint
		add_theme_stylebox_override("fill", fill_box)