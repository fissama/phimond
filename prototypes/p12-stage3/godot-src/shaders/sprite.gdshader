shader_type spatial;
render_mode unshaded, cull_disabled, skip_vertex_transform, depth_draw_opaque;
global uniform vec3 g_player;
global uniform vec3 g_fog;
global uniform float g_light;
uniform sampler2D tex : source_color, filter_nearest, repeat_disable;
uniform vec4 uv_rect = vec4(0.0, 0.0, 1.0, 1.0);
uniform float flip = 1.0;
uniform float sway = 0.0;
uniform float fog_amt = 0.6;
uniform float top_fade = 0.0;
varying vec3 vworld;
varying float vp;
void vertex() {
	vec3 center = MODEL_MATRIX[3].xyz;
	vec2 size = vec2(length(MODEL_MATRIX[0].xyz), length(MODEL_MATRIX[1].xyz));
	vec3 right = normalize(vec3(INV_VIEW_MATRIX[0].x, 0.0, INV_VIEW_MATRIX[0].z));
	vec3 w = center + right * (VERTEX.x * size.x) + vec3(0.0, VERTEX.y * size.y, 0.0);
	w.x += sin(TIME * 1.4 + center.x * 0.9 + center.z * 0.5) * sway * VERTEX.y * VERTEX.y * 0.05 * size.y;
	vworld = w;
	vp = VERTEX.y;
	vec2 q = UV;
	if (flip < 0.0) q.x = 1.0 - q.x;
	UV = uv_rect.xy + q * uv_rect.zw;
	VERTEX = (VIEW_MATRIX * vec4(w, 1.0)).xyz;
}
void fragment() {
	vec4 c = texture(tex, UV);
	if (c.a < 0.5) discard;
	vec3 col = c.rgb * vec3(0.93, 0.98, 1.0) * (0.86 + 0.14 * smoothstep(0.0, 3.0, vworld.y));
	float pool = smoothstep(7.0, 0.0, distance(vworld.xz, g_player.xz)) * 0.22 * g_light;
	col += vec3(1.0, 0.86, 0.55) * pool * c.rgb;
	float f = smoothstep(16.0, 40.0, length(vworld - CAMERA_POSITION_WORLD));
	col = mix(col, g_fog, f * fog_amt);
	col = mix(col, g_fog * 0.9, top_fade * smoothstep(0.78, 1.0, vp));
	ALBEDO = col;
}
