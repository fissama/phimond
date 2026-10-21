shader_type spatial;
render_mode unshaded, blend_add, depth_draw_never, cull_disabled;
uniform float seed = 0.0;
void fragment() {
	vec2 u = vec2(UV.x, 1.0 - UV.y);
	float e = smoothstep(0.0, 0.35, u.x) * smoothstep(1.0, 0.65, u.x);
	float v = smoothstep(0.0, 0.2, u.y) * smoothstep(1.0, 0.4, u.y);
	float s = 0.75 + 0.25 * sin(TIME * 0.6 + seed + u.y * 4.0);
	ALBEDO = vec3(1.0, 0.93, 0.65) * e * v * s * 0.20;
	ALPHA = 1.0;
}
