shader_type spatial;
render_mode unshaded, blend_add, depth_draw_never, cull_disabled;
void fragment() {
	vec2 p = UV - 0.5;
	float r = length(p) * 2.0;
	float ring = smoothstep(0.08, 0.0, abs(r - 0.78 - 0.04 * sin(TIME * 2.0)));
	float core = smoothstep(1.0, 0.0, r) * 0.35;
	ALBEDO = vec3(0.5, 1.0, 0.85) * (ring + core);
	ALPHA = 1.0;
}
