shader_type spatial;
render_mode unshaded, depth_draw_never, cull_disabled;
void fragment() {
	float r = length(UV - 0.5) * 2.0;
	ALBEDO = vec3(0.0);
	ALPHA = smoothstep(1.0, 0.0, r) * 0.55;
}
