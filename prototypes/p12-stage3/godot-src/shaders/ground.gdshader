shader_type spatial;
render_mode unshaded, depth_draw_opaque;
global uniform vec3 g_player;
global uniform vec3 g_fog;
global uniform float g_light;
uniform sampler2D tex : source_color, filter_nearest, repeat_disable;
uniform vec2 tile = vec2(7.49, 7.965);
uniform vec2 zr = vec2(-3.47, 4.49);
varying vec3 vworld;
void vertex() { vworld = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz; }
void fragment() {
	vec2 uv = vec2(vworld.x / tile.x, 1.0 - (vworld.z - zr.x) / tile.y);
	vec3 col = texture(tex, fract(uv)).rgb;
	float back = smoothstep(zr.x, zr.y, vworld.z);
	col *= mix(0.62, 1.0, back);
	float pool = smoothstep(7.5, 0.0, distance(vworld.xz, g_player.xz)) * 0.30 * g_light;
	col += vec3(1.0, 0.86, 0.55) * pool * col;
	float f = smoothstep(16.0, 40.0, length(vworld - CAMERA_POSITION_WORLD));
	col = mix(col, g_fog, f * 0.6);
	ALBEDO = col;
}
