extends Control
## BattleScene — battle UI. Fantasy-framed window covering the viewport with two unit
## panels (AnimatedSprite2D portrait + GameHPBar + GameMPBar), a compact battle log
## (RichTextLabel) and a row of GameButton actions (Attack / Skill / Item / Capture
## / Auto / Flee). HP/MP bars tween smoothly on damage. Sprite portraits fade-in +
## scale-from-0 when a new unit appears. The close button on the GameWindow returns
## the player to MainMap only when the server has cleared the battle (no battle
## data on state).

@onready var _window: Control = $Window
@onready var _player_hp: ProgressBar = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/PlayerPanel/PlayerVBox/PlayerHP
@onready var _player_mp: ProgressBar = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/PlayerPanel/PlayerVBox/PlayerMP
@onready var _player_name: Label = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/PlayerPanel/PlayerVBox/PlayerName
@onready var _player_sprite: AnimatedSprite2D = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/PlayerPanel/PlayerVBox/PlayerSprite
@onready var _enemy_hp: ProgressBar = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/EnemyPanel/EnemyVBox/EnemyHP
@onready var _enemy_mp: ProgressBar = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/EnemyPanel/EnemyVBox/EnemyMP
@onready var _enemy_name: Label = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/EnemyPanel/EnemyVBox/EnemyName
@onready var _enemy_sprite: AnimatedSprite2D = $Window/Frame/Body/BodyContainer/BodyRoot/UnitsRow/EnemyPanel/EnemyVBox/EnemySprite
@onready var _log: RichTextLabel = $Window/Frame/Body/BodyContainer/BodyRoot/LogPanel/LogMargin/Log
@onready var _turn_indicator: Label = $Window/Frame/Body/BodyContainer/BodyRoot/TurnIndicator
@onready var _atk_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/ActionRow/AttackBtn
@onready var _skill_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/ActionRow/SkillBtn
@onready var _item_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/ActionRow/ItemBtn
@onready var _capture_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/ActionRow/CaptureBtn
@onready var _auto_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/ActionRow/AutoBtn
@onready var _flee_btn: Control = $Window/Frame/Body/BodyContainer/BodyRoot/ActionRow/FleeBtn

# Tween handles — used to avoid leaking tweens when state updates fire rapidly.
var _hp_tween: Tween = null
var _entry_tween: Tween = null
var _last_player_species: String = ""
var _last_enemy_species: String = ""
# HP snapshots — used to compute damage delta between state updates so we can
# spawn floating "-N" labels above the hit sprite.
var _prev_player_hp: int = -1
var _prev_enemy_hp: int = -1
# Cached lookup: species_id → SpriteFrames resource path.
var _species_atlas: Dictionary = {}


func _ready() -> void:
	_species_atlas = _load_species_atlas()
	if _window and _window.has_method("set_title"):
		_window.call("set_title", "Battle")
	if _window and _window.has_method("set_close_callback"):
		_window.call("set_close_callback", _on_window_close)
	_label_action(_atk_btn, "Attack")
	_label_action(_skill_btn, "Skill")
	_label_action(_item_btn, "Item")
	_label_action(_capture_btn, "Capture")
	_label_action(_auto_btn, "Auto")
	_label_action(_flee_btn, "Flee")
	_connect_action(_atk_btn, "_on_attack")
	_connect_action(_skill_btn, "_on_skill")
	_connect_action(_item_btn, "_on_item")
	_connect_action(_capture_btn, "_on_capture")
	_connect_action(_auto_btn, "_on_auto")
	_connect_action(_flee_btn, "_on_flee")
	PhimondClient.state_updated.connect(_on_state_updated)
	if is_instance_valid(_log):
		PhimondClient.log_message.connect(func(t): _log.append_text(t + "\n"))
	_refresh()


func _label_action(btn: Control, text: String) -> void:
	if btn and btn.has_method("set_label"):
		btn.call("set_label", text)


func _connect_action(btn: Control, method: String) -> void:
	if btn == null: return
	if btn.has_method("connect_pressed"):
		btn.call("connect_pressed", Callable(self, method))


func _refresh() -> void:
	var battle = PhimondClient.state.get("battle")
	if not battle is Dictionary:
		# Defer the scene swap so we don't trip the "node busy adding children"
		# guard while BattleScene is still inside _ready().
		if not is_queued_for_deletion():
			call_deferred("_go_back_to_map")
		return
	var player_unit := {}
	var enemy_unit := {}
	for unit in battle.get("units", []):
		if unit.get("side") == "player": player_unit = unit
		elif unit.get("side") == "enemy": enemy_unit = unit
	if is_instance_valid(_player_name): _player_name.text = str(player_unit.get("name", "Player"))
	if is_instance_valid(_enemy_name): _enemy_name.text = str(enemy_unit.get("name", "Enemy"))
	if _window and _window.has_method("set_title"):
		_window.call("set_title", "Battle — Turn %s vs %s" % [str(battle.get("turn", 0)), str(enemy_unit.get("name", "Enemy"))])
	_assign_unit_sprite(_player_sprite, player_unit, true)
	_assign_unit_sprite(_enemy_sprite, enemy_unit, false)
	if is_instance_valid(_player_hp): _animate_bar(_player_hp, int(player_unit.get("hp", 0)), int(player_unit.get("max_hp", 1)))
	if is_instance_valid(_player_mp): _animate_bar(_player_mp, int(player_unit.get("mp", 0)), int(player_unit.get("max_mp", 1)))
	if is_instance_valid(_enemy_hp): _animate_bar(_enemy_hp, int(enemy_unit.get("hp", 0)), int(enemy_unit.get("max_hp", 1)))
	if is_instance_valid(_enemy_mp): _animate_bar(_enemy_mp, int(enemy_unit.get("mp", 0)), int(enemy_unit.get("max_mp", 1)))


func _go_back_to_map() -> void:
	if PhimondClient.state.get("battle") == null:
		get_tree().change_scene_to_file("res://scenes/MainMap.tscn")


func _assign_unit_sprite(target: AnimatedSprite2D, unit: Dictionary, is_player: bool) -> void:
	if target == null: return
	var species_id := str(unit.get("species", unit.get("id", "")))
	var frames_path := ""
	# Player side: prefer spriteframes_player.tres. Otherwise fall back to species.
	if is_player:
		frames_path = "res://assets/extracted/spriteframes_player.tres"
	else:
		frames_path = _species_atlas.get(species_id, "")
	if frames_path.is_empty() or not ResourceLoader.exists(frames_path):
		# Fallback to player frame.
		frames_path = "res://assets/extracted/spriteframes_player.tres"
	var last := _last_player_species if is_player else _last_enemy_species
	# Detect species swap for re-triggering entry tween.
	var swap_key := frames_path + "|" + species_id
	if swap_key == last:
		return
	if is_player: _last_player_species = swap_key
	else: _last_enemy_species = swap_key
	var frames: SpriteFrames = load(frames_path)
	target.sprite_frames = frames
	if frames and frames.has_animation("idle"):
		target.play("idle")
	else:
		target.stop()
	# Entry tween: scale-from-center + fade-in. AnimatedSprite2D centers the texture
	# around its position when `centered` is true (default), so a plain scale animates
	# outward from the sprite's visual center without needing pivot_offset — which is
	# important because AnimatedSprite2D has no `size` property.
	target.scale = Vector2(0.3, 0.3)
	target.modulate = Color(1, 1, 1, 0.0)
	if _entry_tween and _entry_tween.is_valid():
		_entry_tween.kill()
	_entry_tween = create_tween().set_parallel(true)
	_entry_tween.tween_property(target, "scale", Vector2(1, 1), 0.2).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_entry_tween.tween_property(target, "modulate", Color(1, 1, 1, 1.0), 0.2)


func _load_species_atlas() -> Dictionary:
	var path := "res://assets/extracted/species_atlas.json"
	if not FileAccess.file_exists(path):
		return {}
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null: return {}
	var txt := f.get_as_text()
	f.close()
	var parsed: Variant = JSON.parse_string(txt)
	if not parsed is Dictionary: return {}
	var species_dict: Dictionary = parsed.get("species", {})
	var out := {}
	for sid in species_dict.keys():
		out[sid] = "res://assets/extracted/spriteframes_" + String(sid) + ".tres"
	return out


func _animate_bar(bar: ProgressBar, value: int, max_value: int) -> void:
	if bar == null: return
	var new_max: int = max(max_value, 1)
	var new_val: float = clamp(float(value), 0.0, float(new_max))
	if bar.max_value != new_max:
		bar.max_value = new_max
	if _hp_tween and _hp_tween.is_valid():
		_hp_tween.kill()
	_hp_tween = create_tween()
	_hp_tween.tween_property(bar, "value", new_val, 0.35).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)


func _on_state_updated(_rev: int, _c: Dictionary) -> void: _refresh()


func _on_window_close() -> void:
	# Only honour the close request when the server has already ended the battle;
	# otherwise the player must finish the fight.
	if PhimondClient.state.get("battle") == null:
		get_tree().change_scene_to_file("res://scenes/MainMap.tscn")


func _battle_id() -> String: return str(PhimondClient.state.get("battle", {}).get("id", ""))
func _turn() -> int: return int(PhimondClient.state.get("battle", {}).get("turn", 0))

func _on_attack() -> void: PhimondClient.battle_action(_battle_id(), _turn(), "attack")
func _on_skill() -> void: PhimondClient.battle_action(_battle_id(), _turn(), "skill", "skill_basic")
func _on_item() -> void: PhimondClient.battle_action(_battle_id(), _turn(), "item", "", "potion")
func _on_capture() -> void: PhimondClient.battle_action(_battle_id(), _turn(), "capture")
func _on_auto() -> void: PhimondClient.battle_action(_battle_id(), _turn(), "auto")
func _on_flee() -> void: PhimondClient.battle_action(_battle_id(), _turn(), "flee")