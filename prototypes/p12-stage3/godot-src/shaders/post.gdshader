shader_type canvas_item;
uniform sampler2D screen_tex : hint_screen_texture, filter_linear, repeat_disable;
uniform float tilt = 1.0;
void fragment() {
	vec2 uv = SCREEN_UV;
	vec2 res = 1.0 / SCREEN_PIXEL_SIZE;
	float d = abs(uv.y - 0.52);
	float r = tilt * smoothstep(0.18, 0.55, d) * 3.2;
	vec2 px = r / res;
	vec3 c = texture(screen_tex, uv).rgb * 0.2;
	c += texture(screen_tex, uv + vec2(px.x, 0.0)).rgb * 0.1 + texture(screen_tex, uv - vec2(px.x, 0.0)).rgb * 0.1;
	c += texture(screen_tex, uv + vec2(0.0, px.y)).rgb * 0.1 + texture(screen_tex, uv - vec2(0.0, px.y)).rgb * 0.1;
	c += texture(screen_tex, uv + px * vec2(0.7, 0.7)).rgb * 0.1 + texture(screen_tex, uv + px * vec2(-0.7, -0.7)).rgb * 0.1;
	c += texture(screen_tex, uv + px * vec2(0.7, -0.7)).rgb * 0.1 + texture(screen_tex, uv + px * vec2(-0.7, 0.7)).rgb * 0.1;
	float l = dot(c, vec3(0.299, 0.587, 0.114));
	c = mix(vec3(l), c, 1.12);
	c *= mix(vec3(0.93, 0.98, 1.05), vec3(1.06, 1.0, 0.92), smoothstep(0.2, 0.8, l));
	float v = smoothstep(0.95, 0.35, length((uv - 0.5) * vec2(1.15, 1.0)));
	c *= mix(0.72, 1.0, v);
	COLOR = vec4(c, 1.0);
}
