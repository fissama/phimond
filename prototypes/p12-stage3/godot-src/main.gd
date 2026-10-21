extends Node3D
# P12 Stage 3 · Golden Scene Emerald HD-2D · Godot 4.7 (Compatibility, Web).
# Cùng ../shared/scene.json và ../shared/tex/*.png với bản Three.js; tải qua HTTP lúc chạy.

const SHARED := "../shared/"
const ENGINE := "godot"
const SPEED := 3.2

var T0 := Time.get_ticks_msec()
var marks := {"start": 0}
var SCENE: Dictionary
var tex := {}
var tex_bytes := 0

var tier := "high"
var dpr_cap := 2.0
var map_id := "emerald_forest_main_woods"
var auto := false
var secs := 60.0
var warm_frames := 120

var cam: Camera3D
var env: Environment
var post_layer: CanvasLayer
var post_rect: ColorRect
var quad: QuadMesh
var sh_sprite: Shader
var sh_ground: Shader
var sh_part: Shader
var sh_shaft: Shader
var sh_ring: Shader
var sh_blob: Shader
var sh_post: Shader

var current := {}          # id, root, doors, bounds, zrange, pets, pts, shafts, props
var player := {"x": 0.0, "z": 0.0, "facing": 1.0, "moving": false, "mesh": null, "shadow": null}
var keys_joy := Vector2.ZERO
var first_input_t := 0.0
var input_lat: Array = []
var shift_frac := 0.0
var map_switches: Array = []
var ctx_lost := 0
var bench := {}
var bot_on := false
var bot_leg := 0
var anim_t := 0.0
var last_us := 0
var frame_no := 0
var hud_t := 0
var tier_cfg: Dictionary
var ready_to_run := false


func _ready() -> void:
	_parse_query()
	RenderingServer.global_shader_parameter_add("g_player", RenderingServer.GLOBAL_VAR_TYPE_VEC3, Vector3.ZERO)
	RenderingServer.global_shader_parameter_add("g_fog", RenderingServer.GLOBAL_VAR_TYPE_VEC3, Vector3(0.02, 0.25, 0.32))
	RenderingServer.global_shader_parameter_add("g_light", RenderingServer.GLOBAL_VAR_TYPE_FLOAT, 1.0)
	sh_sprite = load("res://shaders/sprite.gdshader")
	sh_ground = load("res://shaders/ground.gdshader")
	sh_part = load("res://shaders/particles.gdshader")
	sh_shaft = load("res://shaders/shaft.gdshader")
	sh_ring = load("res://shaders/glow_ring.gdshader")
	sh_blob = load("res://shaders/blob.gdshader")
	sh_post = load("res://shaders/post.gdshader")
	quad = QuadMesh.new()
	quad.size = Vector2(1, 1)
	quad.center_offset = Vector3(0, 0.5, 0)
	_setup_viewport()
	_setup_ui()
	await _load_all()
	await _build_map(map_id)
	var sp: Array = SCENE.maps[map_id].spawn
	player.x = sp[0]
	player.z = sp[1]
	_mark("ready")
	var gl = _js("(()=>{const c=document.createElement('canvas');const g=c.getContext('webgl2');if(!g)return '';const e=g.getExtension('WEBGL_debug_renderer_info');return e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER);})()")
	_sysq("[đo] godot %s Compatibility · GPU %s · DPR %.2f → scale3d %.2f · %dx%d" % [Engine.get_version_info().string, str(gl), _dpr(), get_viewport().scaling_3d_scale, int(get_viewport().get_visible_rect().size.x), int(get_viewport().get_visible_rect().size.y)])
	var xfer = _js("performance.getEntriesByType('resource').reduce((s,r)=>s+(r.encodedBodySize||0),0)")
	_sysq("[đo] tải: dữ liệu %s ms · texture %s ms · sẵn sàng %s ms · truyền %.1f MB · texture %.1f MB" % [str(marks.get("json", "?")), str(marks.get("textures", "?")), str(marks.get("ready", "?")), float(xfer if xfer != null else 0) / 1048576.0, tex_bytes / 1048576.0])
	ready_to_run = true
	_expose_api()
	if auto:
		start_bench()


func _mark(k: String) -> void:
	marks[k] = Time.get_ticks_msec() - T0


func _js(code: String) -> Variant:
	if OS.has_feature("web"):
		return JavaScriptBridge.eval(code, true)
	return null


func _parse_query() -> void:
	var qs = _js("location.search")
	if qs == null:
		return
	for part in String(qs).trim_prefix("?").split("&"):
		var kv := part.split("=")
		if kv.size() < 2:
			continue
		match kv[0]:
			"tier": tier = kv[1]
			"dpr": dpr_cap = float(kv[1])
			"map": map_id = kv[1]
			"auto": auto = kv[1] == "1"
			"secs": secs = float(kv[1])
			"warm": warm_frames = int(kv[1])


func _dpr() -> float:
	var v = _js("window.devicePixelRatio")
	return float(v) if v != null else 1.0


func _setup_viewport() -> void:
	var d := _dpr()
	get_window().content_scale_factor = d  # UI theo CSS px
	get_viewport().scaling_3d_mode = Viewport.SCALING_3D_MODE_BILINEAR
	get_viewport().scaling_3d_scale = minf(1.0, dpr_cap / d)
	if OS.has_feature("web"):
		_js("(()=>{const c=document.querySelector('canvas');window.__ctxLost=0;if(c)c.addEventListener('webglcontextlost',()=>{window.__ctxLost++});})()")
	cam = Camera3D.new()
	cam.fov = 30.0
	cam.near = 0.5
	cam.far = 120.0
	cam.current = true
	add_child(cam)
	env = Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.tonemap_mode = Environment.TONE_MAPPER_LINEAR
	env.glow_enabled = false
	var we := WorldEnvironment.new()
	we.environment = env
	add_child(we)


func _setup_ui() -> void:
	# HUD (menu, chat, d-pad...) là lớp DOM dùng chung ../shared/hud/hud.js; Godot chỉ giữ lớp post cho thế giới.
	post_layer = CanvasLayer.new()
	post_layer.layer = 5
	add_child(post_layer)
	post_rect = ColorRect.new()
	post_rect.set_anchors_preset(Control.PRESET_FULL_RECT)
	post_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var pm := ShaderMaterial.new()
	pm.shader = sh_post
	post_rect.material = pm
	post_layer.add_child(post_rect)


func _note_input() -> void:
	if first_input_t == 0.0:
		first_input_t = Time.get_ticks_usec() / 1000.0


func _input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and not e.echo:
		_note_input()


func _sysq(msg: String) -> void:
	if OS.has_feature("web"):
		_js("window.PhimondHUD&&PhimondHUD.sysq&&PhimondHUD.sysq(" + JSON.stringify(msg) + ")")


var win_dts: Array = []
var win_t0 := 0


func _sys_window(raw_ms: float) -> void:
	win_dts.append(raw_ms)
	var now := Time.get_ticks_msec()
	if win_t0 == 0:
		win_t0 = now
	if now - win_t0 < 5000:
		return
	var sum := 0.0
	var mx := 0.0
	for x in win_dts:
		sum += x
		mx = maxf(mx, x)
	var heap = _js("performance.memory?(performance.memory.usedJSHeapSize/1048576).toFixed(0)+'MB':'n/a'")
	_sysq("[đo] godot · %s · %.1f fps · avg %.1f · p95 %.1f · max %.1f ms · calls %d · tris %.1fk · heap %s" % [tier, 1000.0 * win_dts.size() / maxf(sum, 0.001), sum / maxf(win_dts.size(), 1), _pct(win_dts, 0.95), mx, int(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)), RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME) / 1000.0, str(heap)])
	win_dts = []
	win_t0 = now


func _toast(msg: String) -> void:
	if OS.has_feature("web"):
		_js("window.PhimondHUD&&PhimondHUD.sys(" + JSON.stringify(msg) + ")")


# ---------- tải dữ liệu ----------
func _shared_base() -> String:
	var u = _js("new URL('../shared/', location.href).href")
	return str(u) if u != null else "http://localhost:8765/shared/"


func _read_bundled(rel: String) -> PackedByteArray:
	# Dữ liệu cảnh nằm trong .pck (res://data/*.bin), không phụ thuộc HTTP của host.
	var path := "res://data/" + rel + ".bin"
	if not FileAccess.file_exists(path):
		_sysq("[lỗi] godot thiếu file " + path)
		return PackedByteArray()
	return FileAccess.get_file_as_bytes(path)


func _placeholder() -> ImageTexture:
	var img := Image.create(8, 8, false, Image.FORMAT_RGBA8)
	img.fill(Color(1, 0, 1, 1))
	return ImageTexture.create_from_image(img)


func _load_all() -> void:
	var raw := _read_bundled("scene.json")
	SCENE = JSON.parse_string(raw.get_string_from_utf8())
	tier_cfg = SCENE.tiers
	_mark("json")
	var names := {"player.png": true}
	for m in SCENE.maps.values():
		names[m.ground.tex] = true
		for p in m.props:
			names[p.tex] = true
		for p in m.sky:
			names[p.tex] = true
	for p in SCENE.actors.pets:
		names[p.tex] = true
	var bad := 0
	for n in names.keys():
		var img := Image.new()
		var err := img.load_png_from_buffer(_read_bundled("tex/" + n))
		if err != OK:
			bad += 1
			_sysq("[lỗi] godot giải mã PNG thất bại: " + n)
			tex[n] = _placeholder()
			continue
		tex_bytes += img.get_width() * img.get_height() * 4
		tex[n] = ImageTexture.create_from_image(img)
	_sysq("[đo] godot nạp %d texture từ .pck (%d lỗi)" % [names.size(), bad])
	_mark("textures")


# ---------- dựng cảnh ----------
func _sprite(tx: Texture2D, w: float, h: float, x: float, y: float, z: float, sway: float) -> MeshInstance3D:
	var m := MeshInstance3D.new()
	m.mesh = quad
	m.position = Vector3(x, y, z)
	m.scale = Vector3(w, h, 1)
	m.custom_aabb = AABB(Vector3(-60, -60, -60), Vector3(120, 120, 120))
	var mat := ShaderMaterial.new()
	mat.shader = sh_sprite
	mat.set_shader_parameter("tex", tx)
	mat.set_shader_parameter("sway", sway)
	m.material_override = mat
	m.set_meta("base_sway", sway)
	return m


func _blob(w: float, h: float) -> MeshInstance3D:
	var m := MeshInstance3D.new()
	var pm := PlaneMesh.new()
	pm.size = Vector2(1, 1)
	m.mesh = pm
	m.scale = Vector3(w, 1, h)
	var mat := ShaderMaterial.new()
	mat.shader = sh_blob
	mat.render_priority = 1
	m.material_override = mat
	return m


func _build_map(id: String) -> float:
	var t0 := Time.get_ticks_usec()
	var M: Dictionary = SCENE.maps[id]
	var root := Node3D.new()
	var bg: Array = M.bg
	env.background_color = Color(bg[0], bg[1], bg[2]).srgb_to_linear() if false else Color(bg[0], bg[1], bg[2])
	var fogc := Color(bg[0], bg[1], bg[2]).srgb_to_linear()
	RenderingServer.global_shader_parameter_set("g_fog", Vector3(fogc.r, fogc.g, fogc.b))
	# nền đất
	var g0: Dictionary = M.ground
	var gx0: float = g0.x0 - 12.0
	var gx1: float = g0.x1 + 12.0
	var gz1: float = g0.zFront + 4.0
	var gm := MeshInstance3D.new()
	var pl := PlaneMesh.new()
	pl.size = Vector2(gx1 - gx0, gz1 - g0.zBack)
	gm.mesh = pl
	gm.position = Vector3((gx0 + gx1) / 2.0, 0, (g0.zBack + gz1) / 2.0)
	var gmat := ShaderMaterial.new()
	gmat.shader = sh_ground
	gmat.set_shader_parameter("tex", tex[g0.tex])
	gmat.set_shader_parameter("tile", Vector2(g0.tileW, g0.tileD))
	gmat.set_shader_parameter("zr", Vector2(g0.zBack, g0.zFront))
	gm.material_override = gmat
	root.add_child(gm)
	# bầu trời: một lớp xa, lát gương liên tục, đáy trùng màu nền
	var s0: Dictionary = M.sky[0]
	var sky_h: float = float(s0.h) * 2.4
	var sky_w: float = sky_h * float(s0.w) / float(s0.h)
	var sx: float = float(M.bounds[0]) - 30.0
	var sk := 0
	while sx < float(M.bounds[1]) + 30.0:
		var ssp := _sprite(tex[s0.tex], sky_w * 1.002, sky_h, sx + sky_w / 2.0, 0.6, g0.zBack - 7.0, 0.0)
		ssp.material_override.set_shader_parameter("fog_amt", 0.0)
		ssp.material_override.set_shader_parameter("flip", -1.0 if sk % 2 == 1 else 1.0)
		root.add_child(ssp)
		sx += sky_w
		sk += 1
	# props
	var props := []
	for p in M.props:
		var sp := _sprite(tex[p.tex], p.w, p.h, p.x, 0.0, p.z, float(p.sway))
		if String(p.tex).begins_with("9_0") or String(p.tex).begins_with("10_0") or String(p.tex).begins_with("11_0"):
			sp.material_override.set_shader_parameter("top_fade", 0.9)
		root.add_child(sp)
		props.append(sp)
	# cửa
	var doors := []
	for d in M.get("doors", []):
		var rm := MeshInstance3D.new()
		var rq := QuadMesh.new()
		rq.size = Vector2(1.6, 1.6)
		rq.orientation = PlaneMesh.FACE_Y
		rm.mesh = rq
		var rmat := ShaderMaterial.new()
		rmat.shader = sh_ring
		rmat.render_priority = 2
		rm.material_override = rmat
		rm.position = Vector3(d.x, 0.03, d.z)
		root.add_child(rm)
		var dd: Dictionary = d.duplicate()
		dd["armed"] = false
		doors.append(dd)
	# tia sáng
	var shafts := []
	var b: Array = M.bounds
	for i in 3:
		var sm := MeshInstance3D.new()
		var sq := QuadMesh.new()
		sq.size = Vector2(3.2, 9.0)
		sm.mesh = sq
		var smat := ShaderMaterial.new()
		smat.shader = sh_shaft
		smat.set_shader_parameter("seed", i * 2.1)
		smat.render_priority = 3
		sm.material_override = smat
		sm.position = Vector3(b[0] + (b[1] - b[0]) * (0.2 + 0.3 * i), 4.0, g0.zBack + 0.6 + i * 0.4)
		sm.rotation.z = -0.35
		root.add_child(sm)
		shafts.append(sm)
	# hạt
	var maxp := 240
	var verts := PackedVector3Array()
	var cols := PackedColorArray()
	var rs := 12345
	var zr: Array = M.zRange
	for i in maxp:
		var r := []
		for k in 7:
			rs = (rs * 1664525 + 1013904223) & 0xFFFFFFFF
			r.append(float(rs) / 4294967296.0)
		verts.append(Vector3(b[0] + r[0] * (b[1] - b[0]), 0.2 + r[1] * 3.4, zr[0] + r[2] * (zr[1] - zr[0] + 3.0)))
		cols.append(Color(r[3], r[4], r[5], r[6]))
	var am := ArrayMesh.new()
	var arr := []
	arr.resize(Mesh.ARRAY_MAX)
	arr[Mesh.ARRAY_VERTEX] = verts
	arr[Mesh.ARRAY_COLOR] = cols
	am.add_surface_from_arrays(Mesh.PRIMITIVE_POINTS, arr)
	var pts := MeshInstance3D.new()
	pts.mesh = am
	pts.custom_aabb = AABB(Vector3(-100, -100, -100), Vector3(300, 300, 300))
	var pmat := ShaderMaterial.new()
	pmat.shader = sh_part
	pmat.render_priority = 4
	pts.material_override = pmat
	root.add_child(pts)
	# pet P10
	var pa: Dictionary = SCENE.actors.petAtlas
	var pet_list := []
	for p in SCENE.actors.pets:
		if p.map != id:
			continue
		var ft: Dictionary = pa.feet.get(p.id, {"pad": 0.0, "w": 0.5})
		var sp := _sprite(tex[p.tex], pa.h, pa.h, p.x, -float(ft.pad) * float(pa.h), p.z, 0.0)
		sp.material_override.set_shader_parameter("uv_rect", Vector4(0, 0, 1.0 / pa.cols, 1.0 / pa.rows))
		root.add_child(sp)
		var sh := _blob(float(pa.h) * float(ft.w) * 1.1, float(pa.h) * float(ft.w) * 0.5)
		sh.position = Vector3(p.x, 0.05, p.z + 0.05)
		root.add_child(sh)
		pet_list.append({"sp": sp, "phase": randf() * 4.0})
	# người chơi
	var pd: Dictionary = SCENE.actors.player
	var pm := _sprite(tex[pd.tex], pd.h * float(pd.cell[0]) / float(pd.cell[1]), pd.h, 0, 0, 0, 0.0)
	pm.material_override.set_shader_parameter("uv_rect", Vector4(0, 0, 1.0 / pd.cols, 1.0 / pd.rows))
	root.add_child(pm)
	var psh := _blob(0.9, 0.5)
	root.add_child(psh)
	player.mesh = pm
	player.shadow = psh
	add_child(root)
	if current.has("root"):
		current.root.queue_free()
	current = {"id": id, "root": root, "doors": doors, "bounds": b, "zrange": zr, "pets": pet_list, "pts": pts, "shafts": shafts, "props": props, "pmat": pmat}
	_set_tier(tier)
	return (Time.get_ticks_usec() - t0) / 1000.0


func _set_tier(t: String) -> void:
	tier = t
	var T: Dictionary = tier_cfg[t]
	env.glow_enabled = bool(T.bloom)
	if env.glow_enabled:
		env.glow_intensity = 0.8
		env.glow_strength = 1.0
		env.glow_bloom = 0.1
		env.glow_hdr_threshold = 0.85
		env.glow_blend_mode = Environment.GLOW_BLEND_MODE_ADDITIVE
	post_layer.visible = bool(T.tilt)
	(post_rect.material as ShaderMaterial).set_shader_parameter("tilt", 1.0)
	if current.has("pts"):
		current.pts.visible = int(T.particles) > 0
		for s in current.shafts:
			s.visible = bool(T.shafts)
		for sp in current.props:
			(sp.material_override as ShaderMaterial).set_shader_parameter("sway", float(sp.get_meta("base_sway")) * float(T.sway))
	RenderingServer.global_shader_parameter_set("g_light", 1.0 if int(T.post) == 1 else 0.6)


func _switch_map(id: String, arrive: Array, why: String) -> void:
	var t0 := Time.get_ticks_usec()
	var build := await _build_map(id)
	player.x = arrive[0]
	player.z = arrive[1]
	for d in current.doors:
		d.armed = false  # R-S2-1: chỉ armed sau khi rời vùng cửa
	map_id = id
	var total := (Time.get_ticks_usec() - t0) / 1000.0
	map_switches.append({"to": id, "why": why, "buildMs": snappedf(build, 0.1), "totalMs": snappedf(total, 0.1), "at": Time.get_ticks_msec() - T0})
	_sysq("[đo] godot · đổi map → %s: dựng %.0f ms · tổng %.0f ms (%s)" % [id.replace("emerald_forest_", ""), build, total, why])
	_js("window.PhimondHUD&&PhimondHUD.setState({map:" + JSON.stringify("Emerald · Rừng sâu" if id.contains("deep") else "Emerald · Rừng chính") + "})")
	_toast("→ %s (%d ms)" % [id.replace("emerald_forest_", ""), int(total)])


func _pillar() -> void:
	_switch_map("emerald_forest_deep_woods", SCENE.maps.emerald_forest_deep_woods.spawn, "pillar")


# ---------- vòng lặp ----------
func _process(_delta: float) -> void:
	if not ready_to_run or current.is_empty():
		return
	var now_us := Time.get_ticks_usec()
	if last_us == 0:
		last_us = now_us
		return
	var raw_ms := (now_us - last_us) / 1000.0
	last_us = now_us
	var dt := minf(0.1, raw_ms / 1000.0)
	_update(dt, now_us / 1000.0)
	frame_no += 1
	_sys_window(raw_ms)
	if frame_no == 1:
		_mark("firstFrame")
	if not bench.is_empty():
		if frame_no > bench.warm:
			bench.dts.append(raw_ms)
		else:
			bench.warm_n += 1
		if (Time.get_ticks_msec() - bench.t0) / 1000.0 >= secs:
			_finish_bench()
	if Time.get_ticks_msec() - hud_t > 500:
		hud_t = Time.get_ticks_msec()
		_hud(raw_ms)


func _update(dt: float, now_ms: float) -> void:
	var ix := 0.0
	var iz := 0.0
	if Input.is_key_pressed(KEY_LEFT) or Input.is_key_pressed(KEY_A): ix -= 1.0
	if Input.is_key_pressed(KEY_RIGHT) or Input.is_key_pressed(KEY_D): ix += 1.0
	if Input.is_key_pressed(KEY_UP) or Input.is_key_pressed(KEY_W): iz -= 1.0
	if Input.is_key_pressed(KEY_DOWN) or Input.is_key_pressed(KEY_S): iz += 1.0
	ix += keys_joy.x
	iz += keys_joy.y
	if bot_on:
		var b := _bot()
		ix = b.x
		iz = b.y
	var m := Vector2(ix, iz).length()
	if m > 1.0:
		ix /= m
		iz /= m
	var px: float = player.x
	var pz: float = player.z
	var bnd: Array = current.bounds
	var zr: Array = current.zrange
	player.x = clampf(px + ix * SPEED * dt, bnd[0] + 0.4, bnd[1] - 0.4)
	player.z = clampf(pz + iz * SPEED * dt, zr[0], zr[1])
	player.moving = absf(player.x - px) + absf(player.z - pz) > 1e-5
	if player.moving and first_input_t != 0.0:
		input_lat.append(snappedf(now_ms - first_input_t, 0.01))
		first_input_t = 0.0
	if ix > 0.05: player.facing = 1.0
	elif ix < -0.05: player.facing = -1.0
	anim_t += dt
	var pd: Dictionary = SCENE.actors.player
	var fr := int(anim_t * pd.fps) % 6
	var row := 1 if player.moving else 0
	var pmat: ShaderMaterial = player.mesh.material_override
	pmat.set_shader_parameter("uv_rect", Vector4(float(fr) / pd.cols, float(row) / pd.rows, 1.0 / pd.cols, 1.0 / pd.rows))
	pmat.set_shader_parameter("flip", player.facing)
	player.mesh.position = Vector3(player.x, 0, player.z)
	player.shadow.position = Vector3(player.x, 0.05, player.z + 0.05)
	RenderingServer.global_shader_parameter_set("g_player", Vector3(player.x, 0, player.z))
	var pa: Dictionary = SCENE.actors.petAtlas
	for p in current.pets:
		var f := int((anim_t + p.phase) * pa.fps) % 4
		(p.sp.material_override as ShaderMaterial).set_shader_parameter("uv_rect", Vector4(float(f) / pa.cols, float(pa.idleRow) / pa.rows, 1.0 / pa.cols, 1.0 / pa.rows))
	# camera
	var pitch := deg_to_rad(SCENE.camera.pitchDeg)
	var d: float = SCENE.camera.dist
	var tx := clampf(player.x, bnd[0] + 7.0, bnd[1] - 7.0)
	var tz: float = player.z * 0.6
	var shift_y := shift_frac * d * tan(deg_to_rad(float(SCENE.camera.fov) * 0.5))
	var target := Vector3(tx, 1.0 - shift_y + sin(pitch) * d, tz + cos(pitch) * d)
	cam.position = cam.position.lerp(target, 1.0 - exp(-float(SCENE.camera.follow) * dt))
	cam.look_at(Vector3(cam.position.x, 1.0 - shift_y, cam.position.z - cos(pitch) * d), Vector3.UP)
	# cửa
	for door in current.doors:
		var near := absf(player.x - door.x) < 0.7 and absf(player.z - door.z) < 1.6
		if not near:
			door.armed = true
		elif door.armed:
			door.armed = false
			if door.to != null:
				_switch_map(door.to, door.arrive, "door:" + door.id)
			else:
				_toast("Cổng Hoàng cung → (đường về/recovery) quay lại bằng trụ")
				_pillar()
			return


func _bot() -> Vector2:
	var door: Dictionary = current.doors[0]
	var bnd: Array = current.bounds
	var far_x: float = bnd[0] + 2.0 if current.id == "emerald_forest_main_woods" else bnd[1] - 3.0
	var tgt: float = far_x if bot_leg == 0 else door.x
	var dx: float = tgt - player.x
	if absf(dx) < 0.25:
		bot_leg ^= 1
	var wob := sin(Time.get_ticks_msec() / 1500.0) * 1.2
	return Vector2(signf(dx) * (1.0 if absf(dx) > 0.2 else 0.0), clampf(wob - player.z, -1.0, 1.0) * 0.5)


func _hud(raw_ms: float) -> void:
	var heap = _js("performance.memory?(performance.memory.usedJSHeapSize/1048576).toFixed(0)+'MB':'n/a'")
	var txt := "godot %s · tier %s · scale3d %.2f · %dx%d\n%d fps · %.1f ms · calls %d\nmap %s · x %.1f · heap %s%s" % [
		Engine.get_version_info().string, tier, get_viewport().scaling_3d_scale, int(get_viewport().get_visible_rect().size.x), int(get_viewport().get_visible_rect().size.y),
		int(1000.0 / maxf(raw_ms, 0.001)), raw_ms, int(RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME)),
		String(current.id).replace("emerald_forest_", ""), player.x, str(heap),
		("" if bench.is_empty() else "\nBENCH %d/%ds" % [(Time.get_ticks_msec() - bench.t0) / 1000, int(secs)])]
	var fps := "%d fps · %.1f ms · godot" % [int(1000.0 / maxf(raw_ms, 0.001)), raw_ms]
	_js("window.PhimondHUD&&(PhimondHUD.setDebug(" + JSON.stringify(txt) + "),PhimondHUD.setFps(" + JSON.stringify(fps) + "))")


# ---------- bench ----------
func start_bench() -> void:
	bot_on = true
	bot_leg = 0
	map_switches = []
	input_lat = []
	bench = {"t0": Time.get_ticks_msec(), "dts": [], "warm": warm_frames, "warm_n": 0}
	_js("window.PhimondHUD&&PhimondHUD.setBenchBusy(true)")
	_toast("Bench bắt đầu")


func _pct(a: Array, p: float) -> float:
	var s := a.duplicate()
	s.sort()
	return float(s[mini(s.size() - 1, int(s.size() * p))]) if s.size() > 0 else 0.0


func _finish_bench() -> void:
	var d: Array = bench.dts
	var warm_n: int = bench.warm_n
	bench = {}
	bot_on = false
	var sum := 0.0
	var mx := 0.0
	var o167 := 0
	var o33 := 0
	var o50 := 0
	for x in d:
		sum += x
		mx = maxf(mx, x)
		if x > 16.9: o167 += 1
		if x > 33.4: o33 += 1
		if x > 50.0: o50 += 1
	var res := _collect()
	res["frames"] = {"n": d.size(), "seconds": snappedf(sum / 1000.0, 0.01), "fpsAvg": snappedf(1000.0 * d.size() / maxf(sum, 0.001), 0.01), "avgMs": snappedf(sum / maxf(d.size(), 1), 0.01), "p50Ms": snappedf(_pct(d, 0.5), 0.01), "p95Ms": snappedf(_pct(d, 0.95), 0.01), "p99Ms": snappedf(_pct(d, 0.99), 0.01), "maxMs": snappedf(mx, 0.01), "over16_7": o167, "over33": o33, "over50": o50, "warmupFrames": warm_n}
	res["fps1pLow"] = snappedf(1000.0 / maxf(_pct(d, 0.99), 0.001), 0.01)
	_save_result(res)
	_sysq("[đo] godot bench %s: %s fps · avg %s · p50 %s · p95 %s · p99 %s · max %s ms · >33ms: %s" % [tier, res.frames.fpsAvg, res.frames.avgMs, res.frames.p50Ms, res.frames.p95Ms, res.frames.p99Ms, res.frames.maxMs, res.frames.over33])
	_js("window.PhimondHUD&&PhimondHUD.setBenchBusy(false)")
	_toast("Xong: %s fps, p95 %s ms" % [res.frames.fpsAvg, res.frames.p95Ms])


func _collect() -> Dictionary:
	var info := Engine.get_version_info()
	var ua = _js("navigator.userAgent")
	var heap = _js("performance.memory?+(performance.memory.usedJSHeapSize/1048576).toFixed(1):null")
	var lost = _js("window.__ctxLost||0")
	var xfer = _js("performance.getEntriesByType('resource').reduce((s,r)=>s+(r.encodedBodySize||0),0)")
	var glr = _js("(()=>{const c=document.createElement('canvas');const g=c.getContext('webgl2');if(!g)return '';const e=g.getExtension('WEBGL_debug_renderer_info');return e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER);})()")
	var sorted_lat := input_lat.duplicate()
	sorted_lat.sort()
	return {
		"engine": ENGINE, "engineVersion": "godot " + info.string + " Compatibility (WebGL2, nothreads)", "page": _js("location.href"), "when": Time.get_datetime_string_from_system(true),
		"tier": tier, "dprCap": dpr_cap, "dpr": _dpr(), "scale3d": get_viewport().scaling_3d_scale, "canvas": [int(get_viewport().get_visible_rect().size.x), int(get_viewport().get_visible_rect().size.y)],
		"ua": str(ua), "cores": _js("navigator.hardwareConcurrency"), "deviceMemoryGB": _js("navigator.deviceMemory||null"), "gl": {"renderer": str(glr)},
		"load": {"marksMs": marks, "transferBytes": xfer, "textureBytesEstimate": tex_bytes},
		"render": {"calls": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_DRAW_CALLS_IN_FRAME), "objects": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_OBJECTS_IN_FRAME), "primitives": RenderingServer.get_rendering_info(RenderingServer.RENDERING_INFO_TOTAL_PRIMITIVES_IN_FRAME), "textureMemMB": snappedf(Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED) / 1048576.0, 0.1), "videoMemMB": snappedf(Performance.get_monitor(Performance.RENDER_VIDEO_MEM_USED) / 1048576.0, 0.1)},
		"memory": {"jsHeapMB": heap, "staticMB": snappedf(OS.get_static_memory_usage() / 1048576.0, 0.1), "note": "Safari không công bố heap; dùng Web Inspector Timeline/Instruments cho iOS"},
		"contextLost": lost, "mapSwitches": map_switches, "input": {"samples": sorted_lat.size(), "p50Ms": (sorted_lat[sorted_lat.size() / 2] if sorted_lat.size() > 0 else null), "maxMs": (sorted_lat[-1] if sorted_lat.size() > 0 else null)},
	}


func _save_result(res: Dictionary) -> void:
	var txt := JSON.stringify(res, " ")
	if OS.has_feature("web"):
		var lit := JSON.stringify(txt)
		_js("window.__benchStr=" + lit + ";window.__bench=JSON.parse(window.__benchStr);fetch('/__result?engine=godot&tier=" + tier + "',{method:'POST',body:window.__benchStr,headers:{'content-type':'application/json'}}).catch(()=>{});window.PhimondHUD&&PhimondHUD.setResult&&PhimondHUD.setResult(window.__benchStr);try{navigator.clipboard.writeText(window.__benchStr).catch(()=>{})}catch(e){};console.log('BENCH_RESULT '+JSON.stringify(window.__bench));")
	else:
		print("BENCH_RESULT ", txt)


func _expose_api() -> void:
	if not OS.has_feature("web"):
		return
	var win = JavaScriptBridge.get_interface("window")
	var api = JavaScriptBridge.create_object("Object")
	var cb_pillar := JavaScriptBridge.create_callback(func(_a): _pillar())
	var cb_bench := JavaScriptBridge.create_callback(func(_a): start_bench())
	var cb_tier := JavaScriptBridge.create_callback(func(a): _set_tier(String(a[0])))
	var cb_move := JavaScriptBridge.create_callback(func(a):
		keys_joy = Vector2(float(a[0]), float(a[1]))
		_note_input())
	var cb_shift := JavaScriptBridge.create_callback(func(a): shift_frac = float(a[0]))
	var cb_save := JavaScriptBridge.create_callback(func(_a): _save_result(_collect()))
	api.pillar = cb_pillar
	api.bench = cb_bench
	api.setTier = cb_tier
	api.move = cb_move
	api.shift = cb_shift
	api.save = cb_save
	win.__godot = api
	set_meta("cbs", [cb_pillar, cb_bench, cb_tier, cb_move, cb_shift, cb_save])
	_js("""(()=>{try{const H=window.PhimondHUD,G=window.__godot;if(!H||H.off)return;
H.on('tier',t=>G.setTier(t));H.on('pillar',()=>G.pillar());H.on('bench',()=>G.bench());H.on('save',()=>G.save());
H.on('layout',o=>G.shift(o.shift));G.shift(H.shiftFrac);H.setTier(%s);
const P=%s;H.setState({name:'Phimond',level:12,map:'Emerald · Rừng chính',gold:2400,crystals:15,playerImg:'../shared/tex/player.png',pet:{name:P.name,level:5,hp:82,maxHp:120,mp:32,maxMp:45,img:'../shared/tex/'+P.tex}});}catch(e){window.PhimondHUD&&PhimondHUD.sysq('[lỗi] api godot: '+e)}})()""" % [JSON.stringify(tier), JSON.stringify(SCENE.actors.pets[0])])
