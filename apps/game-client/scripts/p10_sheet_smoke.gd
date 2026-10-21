extends SceneTree
## Focused offline routing and duration/loop smoke. No server or account writes.

const ReferenceArt = preload("res://scripts/reference_art.gd")
const Room = preload("res://scripts/room.gd")
const STATES := ["idle", "run", "attack", "magic", "die"]
var fails: Array[String] = []

func expect(ok: bool, message: String) -> void:
	if not ok:
		fails.append(message)

func _initialize() -> void:
	var art := ReferenceArt.new()
	for sid in ["DocDangNu", "DaoThienDuong", "NuVuongBachCot", "MaVuongHutMau"]:
		var is_reference: bool = sid in ["DocDangNu", "DaoThienDuong"]
		var root_path := "res://assets/pets/redraws/references/" if is_reference else "res://assets/pets/apk84/"
		var path: String = root_path + sid + "/frames.tres"
		var frames := load(path) as SpriteFrames
		expect(frames != null, "frames load: " + path)
		if frames == null:
			continue
		for state in STATES:
			expect(frames.has_animation(state), "missing state: " + sid + "/" + state)
			if not frames.has_animation(state):
				continue
			var count := frames.get_frame_count(state)
			expect(count > 0, "empty state: " + sid + "/" + state)
			if count == 0:
				continue
			expect(art.pet_texture(sid, 0.0, state) == frames.get_frame_texture(state, 0), "routing: " + sid + "/" + state)
			if is_reference:
				expect(count == 4, "reference frame count: " + sid + "/" + state)
				expect(frames.get_animation_loop(state) == (state in ["idle", "run"]), "reference loop: " + sid + "/" + state)
				if state not in ["idle", "run"]:
					expect(art.pet_texture(sid, 1000.0, state) == frames.get_frame_texture(state, count - 1), "one-shot clamp: " + sid + "/" + state)

	# Deliberately unequal durations expose equal-frame timing regressions.
	var fixture := SpriteFrames.new()
	for state in STATES:
		fixture.add_animation(state)
		fixture.set_animation_speed(state, 2.0)
		fixture.set_animation_loop(state, state in ["idle", "run"])
		for duration in [0.5, 1.5, 1.0, 1.0]:
			fixture.add_frame(state, GradientTexture2D.new(), duration)
	ReferenceArt.sheet_frames["timing_fixture"] = fixture
	for state in STATES:
		for sample in [[-1.0, 0], [0.0, 0], [0.249, 0], [0.25, 1], [0.999, 1], [1.0, 2], [1.5, 3]]:
			expect(art.sheet_texture("timing_fixture", state, sample[0]) == fixture.get_frame_texture(state, sample[1]), "duration: " + state + " @ " + str(sample[0]))
		var last := 0 if state in ["idle", "run"] else 3
		expect(art.sheet_texture("timing_fixture", state, 2.0) == fixture.get_frame_texture(state, last), "end boundary: " + state)
		expect(art.sheet_texture("timing_fixture", state, 2000.0) == fixture.get_frame_texture(state, last), "late playback: " + state)
	expect(art.sheet_texture("timing_fixture", "unknown", 0.0) == fixture.get_frame_texture("idle", 0), "fallback idle")

	var room := Room.new()
	room.elapsed = 1000.0
	room._effects.assign([{"type": "skill_cast", "actor_id": "unit", "start": 999.9, "end": 1000.55}])
	var age: float = room._battle_animation_age("unit", "attack")
	expect(is_equal_approx(age, 0.1), "attack uses local age after long uptime")
	expect(art.sheet_texture("timing_fixture", "attack", age) == fixture.get_frame_texture("attack", 0), "late-start attack begins first frame")
	expect(room._battle_animation_age("unit", "die") == 0.0, "death begins first frame")
	room.elapsed += 3.0
	expect(room._battle_animation_age("unit", "die") == 3.0, "death age persists")
	room._select_battle({"id": "next", "units": []})
	expect(room._battle_animation_age("unit", "die") == 0.0, "new battle clears death age")
	room.reset_presentation()
	expect(room._death_started.is_empty(), "reset clears death age")
	room.free()
	ReferenceArt.sheet_frames.erase("timing_fixture")
	if fails.is_empty():
		print("PASS: P10 source/reference routing, weighted durations, loop/one-shot and action-local age")
		quit(0)
	else:
		for failure in fails:
			print("FAIL: ", failure)
		quit(1)
