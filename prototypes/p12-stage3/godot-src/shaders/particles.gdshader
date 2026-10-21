shader_type spatial;
render_mode unshaded, blend_add, depth_draw_never, skip_vertex_transform;
varying float va;
void vertex() {
	vec4 s = COLOR;
	vec3 p = VERTEX;
	p.x += sin(TIME * (0.2 + s.x * 0.4) + s.y * 6.28318) * 1.2;
	p.y += sin(TIME * (0.3 + s.z * 0.5) + s.w * 6.28318) * 0.6;
	p.z += cos(TIME * (0.15 + s.y * 0.3) + s.x * 6.28318) * 0.8;
	vec4 mv = VIEW_MATRIX * MODEL_MATRIX * vec4(p, 1.0);
	VERTEX = mv.xyz;
	POINT_SIZE = (0.10 + 0.12 * s.z) * (VIEWPORT_SIZE.y * 0.5 * PROJECTION_MATRIX[1][1]) / -mv.z;
	va = 0.55 + 0.45 * sin(TIME * (1.0 + s.w * 2.0) + s.x * 20.0);
}
void fragment() {
	float d = length(POINT_COORD - 0.5) * 2.0;
	float a = smoothstep(1.0, 0.0, d);
	ALBEDO = vec3(1.0, 0.95, 0.6) * a * va;
	ALPHA = a * va;
}
