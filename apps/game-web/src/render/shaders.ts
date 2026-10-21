// GLSL cho cảnh HD-2D. Mọi vật liệu đều là ShaderMaterial riêng (không đèn thật) để giữ chi phí thấp trên iPhone.
// Màu làm việc ở không gian tuyến tính; <colorspace_fragment> chuyển sang sRGB khi vẽ thẳng ra màn hình.

export const FOG_COMMON = /* glsl */ `
uniform vec3 uFogColor; uniform vec2 uFog; uniform vec3 uTint;
float fogAmt(float d){ return clamp((d - uFog.x) / max(uFog.y - uFog.x, 0.001), 0.0, 1.0); }
`;

// Sprite dựng đứng nghiêng theo camera, instancing. iMisc = (pha, cờ, nhấp nháy).
// cờ: 1 = đung đưa, 2 = sương xa, 4 = lật ngang, 8 = nhấp nhô (sóng/thuyền), 16 = billboard phẳng (glow/bóng sáng)
export const SPRITE_VERT = /* glsl */ `
attribute vec3 iPos; attribute vec2 iSize; attribute vec3 iMisc;
uniform float uTime; uniform float uPitch; uniform float uFrames; uniform float uFps;
varying vec2 vUv; varying float vDepth; varying float vHaze; varying float vFlick; varying float vShade;
float bit(float f, float b){ return mod(floor(f / b), 2.0); }
void main(){
  float f = iMisc.y;
  float sway = bit(f,1.0), haze = bit(f,2.0), flip = bit(f,4.0), bob = bit(f,8.0);
  vec3 l = vec3(position.x * iSize.x, position.y * iSize.y, 0.0);
  float top = position.y;
  l.x += sway * sin(uTime * 1.25 + iMisc.x + iPos.x * 0.6) * 0.045 * top * top * min(iSize.y, 3.0);
  l.x += sway * sin(uTime * 2.3 + iMisc.x * 1.7) * 0.012 * top;
  float by = bob * (sin(uTime * 0.9 + iMisc.x) * 0.05 + sin(uTime * 0.37 + iMisc.x * 2.0) * 0.03);
  float bx = bob * sin(uTime * 0.4 + iMisc.x * 3.0) * 0.07;
  float cp = cos(uPitch), sp = sin(uPitch);
  vec3 w = iPos + vec3(l.x + bx, l.y * cp + by, -l.y * sp);
  vec2 u2 = uv;
  float fr = floor(mod(uTime * uFps + iMisc.x, uFrames));
  u2.x = (flip > 0.5 ? 1.0 - u2.x : u2.x);
  u2.x = (u2.x + fr) / uFrames;
  vUv = u2; vHaze = haze;
  vFlick = 1.0 + iMisc.z * (sin(uTime * 13.0 + iMisc.x * 5.0) * 0.5 + sin(uTime * 7.3 + iMisc.x) * 0.5);
  vShade = 1.0;
  vec4 mv = viewMatrix * vec4(w, 1.0);
  vDepth = -mv.z;
  gl_Position = projectionMatrix * mv;
}`;
export const SPRITE_FRAG = /* glsl */ `
uniform sampler2D map; uniform float uAdditive; uniform float uAlphaCut;
varying vec2 vUv; varying float vDepth; varying float vHaze; varying float vFlick; varying float vShade;
${FOG_COMMON}
void main(){
  vec4 t = texture2D(map, vUv);
  if (uAdditive < 0.5 && t.a < uAlphaCut) discard;
  vec3 c = t.a > 0.001 ? t.rgb / t.a : t.rgb;
  c *= uTint;
  float fa = fogAmt(vDepth) * 0.85 + vHaze * 0.32;
  c = mix(c, uFogColor, clamp(fa, 0.0, 0.95));
  if (uAdditive > 0.5) { gl_FragColor = vec4(c * t.a * vFlick, t.a * vFlick); }
  else gl_FragColor = vec4(c, 1.0);
  #include <colorspace_fragment>
}`;

// Decal nằm trên sàn (instancing): iPos tâm, iSize (rộng, sâu), iMisc.y: 4 = lật ngang.
export const FLAT_VERT = /* glsl */ `
attribute vec3 iPos; attribute vec2 iSize; attribute vec3 iMisc;
varying vec2 vUv; varying float vDepth;
void main(){
  vec3 l = vec3(position.x * iSize.x, 0.0, position.y * iSize.y);
  vec2 u = uv; if (mod(floor(iMisc.y / 4.0), 2.0) > 0.5) u.x = 1.0 - u.x;
  vUv = u;
  vec4 mv = viewMatrix * vec4(iPos + l + vec3(0.0, 0.012, 0.0), 1.0);
  vDepth = -mv.z; gl_Position = projectionMatrix * mv;
}`;
export const FLAT_FRAG = /* glsl */ `
uniform sampler2D map;
varying vec2 vUv; varying float vDepth;
${FOG_COMMON}
void main(){
  vec4 t = texture2D(map, vUv);
  if (t.a < 0.5) discard;
  vec3 c = (t.rgb / t.a) * uTint;
  c = mix(c, uFogColor, clamp(fogAmt(vDepth) * 0.85, 0.0, 0.95));
  gl_FragColor = vec4(c * t.a, t.a);
  #include <colorspace_fragment>
}`;

// Sàn lặp họa tiết, có biến thiên sắc độ nhẹ để không lộ ô gạch lặp.
export const FLOOR_VERT = /* glsl */ `
uniform vec4 uRect; uniform vec2 uTile;
varying vec2 vUv; varying vec2 vW; varying float vDepth;
void main(){
  vec3 p = vec3(mix(uRect.x, uRect.z, position.x + 0.5), 0.0, mix(uRect.y, uRect.w, position.y + 0.5));
  vUv = vec2((p.x - uRect.x) / uTile.x, (p.z - uRect.y) / uTile.y);
  vW = p.xz;
  vec4 mv = viewMatrix * vec4(p, 1.0); vDepth = -mv.z; gl_Position = projectionMatrix * mv;
}`;
export const FLOOR_FRAG = /* glsl */ `
uniform sampler2D map; uniform float uTime; uniform float uVar;
varying vec2 vUv; varying vec2 vW; varying float vDepth;
${FOG_COMMON}
float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(h21(i), h21(i + vec2(1,0)), f.x), mix(h21(i + vec2(0,1)), h21(i + vec2(1,1)), f.x), f.y); }
void main(){
  vec3 c = texture2D(map, vUv).rgb * uTint;
  float n = vn(vW * 0.35) * 0.6 + vn(vW * 0.9 + 7.0) * 0.4;
  c *= 1.0 + (n - 0.5) * uVar;
  c = mix(c, uFogColor, clamp(fogAmt(vDepth) * 0.85, 0.0, 0.95));
  gl_FragColor = vec4(c, 1.0);
  #include <colorspace_fragment>
}`;

// Bóng mềm dưới chân (instancing).
export const SHADOW_VERT = FLAT_VERT;
export const SHADOW_FRAG = /* glsl */ `
uniform sampler2D map; uniform float uAlpha;
varying vec2 vUv; varying float vDepth;
void main(){
  float a = texture2D(map, vUv).a * uAlpha;
  gl_FragColor = vec4(0.02, 0.03, 0.06, a);
  #include <colorspace_fragment>
}`;

// Nước biển (bãi biển): gradient sâu→nông, gợn sóng, bọt ven bờ, lấp lánh.
export const WATER_VERT = /* glsl */ `
uniform vec4 uRect; varying vec2 vW; varying float vDepth;
void main(){
  vec3 p = vec3(mix(uRect.x, uRect.z, position.x + 0.5), 0.0, mix(uRect.y, uRect.w, position.y + 0.5));
  vW = p.xz; vec4 mv = viewMatrix * vec4(p + vec3(0.0, 0.006, 0.0), 1.0); vDepth = -mv.z; gl_Position = projectionMatrix * mv;
}`;
export const WATER_FRAG = /* glsl */ `
uniform float uTime; uniform float uShore; uniform vec3 uDeep, uMid, uShallow, uFoam; uniform float uFar;
varying vec2 vW; varying float vDepth;
${FOG_COMMON}
float h21(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3.0 - 2.0 * f);
  return mix(mix(h21(i), h21(i + vec2(1,0)), f.x), mix(h21(i + vec2(0,1)), h21(i + vec2(1,1)), f.x), f.y); }
void main(){
  float shoreLine = uShore - 0.18 - 0.16 * sin(vW.x * 0.55 + uTime * 0.7) - 0.10 * sin(vW.x * 1.3 - uTime * 0.5) - 0.28 * (0.5 + 0.5 * sin(uTime * 0.45));
  float dist = shoreLine - vW.y;               // >0: nằm trong nước
  float a = smoothstep(-0.05, 0.1, dist);
  float d01 = clamp(dist / 5.5, 0.0, 1.0);
  vec3 col = mix(uShallow, uMid, smoothstep(0.0, 0.35, d01));
  col = mix(col, uDeep, smoothstep(0.3, 1.0, d01));
  float rip = vn(vec2(vW.x * 1.4 + uTime * 0.25, vW.y * 3.2 - uTime * 0.35)) * 0.6 + vn(vW * 4.0 + uTime * 0.2) * 0.4;
  col *= 0.88 + rip * 0.28;
  float spark = smoothstep(0.80, 0.95, vn(vW * 7.0 + vec2(uTime * 0.6, -uTime * 0.3)));
  col += spark * 0.35 * (1.0 - d01 * 0.6);
  float foamBand = smoothstep(0.22, 0.0, abs(dist - 0.08)) * (0.6 + 0.4 * vn(vec2(vW.x * 3.0 + uTime * 0.4, uTime * 0.2)));
  float foam2 = smoothstep(0.12, 0.0, abs(dist - (1.1 + 0.4 * sin(uTime * 0.5 + vW.x * 0.8)))) * 0.35 * step(0.5, vn(vec2(vW.x * 2.1, uTime * 0.15)));
  // sóng xa: các dải bọt trắng chạy vào bờ, mờ dần theo khoảng cách
  float wphase = dist * 0.85 - uTime * 0.55;
  float crest = pow(max(0.0, sin(wphase * 3.14159 * 0.9 + vn(vec2(vW.x * 0.7, dist * 0.3)) * 2.0)), 14.0) * smoothstep(0.7, 2.2, dist) * (1.0 - smoothstep(0.35, 1.0, d01) * 0.7);
  vec3 sky = vec3(0.55, 0.62, 0.8);
  col = mix(col, sky, smoothstep(0.82, 1.0, d01) * 0.55);
  col = mix(col, uFoam, clamp(foamBand + foam2 + crest * 0.8, 0.0, 0.92));
  col *= uTint;
  col = mix(col, uFogColor, clamp(fogAmt(vDepth) * 0.6, 0.0, 0.9));
  // cát ướt sau mép nước
  float wet = smoothstep(-1.1, 0.0, dist) * (1.0 - a);
  vec3 outc = col; float outa = a;
  if (a < 0.999) { outc = mix(vec3(0.16, 0.12, 0.08) * uTint, col, a); outa = max(a, wet * 0.38); }
  gl_FragColor = vec4(outc, outa);
  #include <colorspace_fragment>
}`;

// Hạt (phấn hoa, lá, cánh hoa, bụi, tàn lửa, bọt nước, bướm, đài phun).
export const PARTICLE_VERT = /* glsl */ `
attribute vec4 aSeed; // x,y,z ngẫu nhiên; w = góc/pha
uniform float uTime; uniform float uKind; uniform vec4 uArea; // x0,z0,x1,z1 vùng phát
uniform float uCamX; uniform float uSpan; uniform float uSize; uniform float uPx; uniform vec3 uOrigin;
varying float vA; varying float vKind; varying float vRot; varying float vTw;
void main(){
  vec3 p; float a = 1.0; float size = uSize;
  float span = uSpan;
  float t = uTime;
  if (uKind < 0.5) {                 // 0 phấn hoa: trôi chậm, nhấp nháy
    p.x = uCamX + mod(aSeed.x * span + t * (0.18 + aSeed.y * 0.2), span) - span * 0.5;
    p.z = mix(uArea.y, uArea.w, aSeed.z);
    p.y = 0.4 + aSeed.y * 3.6 + sin(t * 0.7 + aSeed.w * 6.28) * 0.35;
    a = 0.5 + 0.5 * sin(t * 1.7 + aSeed.w * 9.0);
  } else if (uKind < 1.5) {          // 1 lá / cánh hoa: rơi xoay
    float fall = mod(t * (0.35 + aSeed.y * 0.35) + aSeed.z * 5.0, 5.0);
    p.x = uCamX + mod(aSeed.x * span + t * 0.35, span) - span * 0.5 + sin(t * 1.1 + aSeed.w * 6.28) * 0.7;
    p.z = mix(uArea.y, uArea.w, fract(aSeed.z * 7.13));
    p.y = 4.6 - fall + sin(t * 0.9 + aSeed.w * 6.0) * 0.1;
    a = smoothstep(0.0, 0.4, fall) * smoothstep(5.0, 4.3, fall);
  } else if (uKind < 2.5) {          // 2 bụi: lơ lửng rất chậm
    p.x = uCamX + mod(aSeed.x * span + t * 0.05, span) - span * 0.5;
    p.z = mix(uArea.y, uArea.w, aSeed.z);
    p.y = 0.3 + aSeed.y * 4.0 + sin(t * 0.3 + aSeed.w * 6.28) * 0.2;
    a = 0.25 + 0.25 * sin(t * 0.8 + aSeed.w * 9.0);
  } else if (uKind < 3.5) {          // 3 tàn lửa: bay lên
    float rise = mod(t * (0.5 + aSeed.y * 0.6) + aSeed.z * 6.0, 4.5);
    p.x = uCamX + mod(aSeed.x * span, span) - span * 0.5 + sin(t * 1.4 + aSeed.w * 6.28) * 0.4;
    p.z = mix(uArea.y, uArea.w, aSeed.z);
    p.y = 0.3 + rise; a = smoothstep(4.5, 1.5, rise) * (0.5 + 0.5 * sin(t * 9.0 + aSeed.w * 20.0));
  } else if (uKind < 4.5) {          // 4 bọt nước biển: bắn lên ven bờ
    float ph = fract(t * 0.35 + aSeed.y);
    p.x = uCamX + mod(aSeed.x * span, span) - span * 0.5;
    p.z = uArea.w + 0.1 - aSeed.z * 0.7;
    p.y = 0.05 + sin(ph * 3.14159) * (0.4 + aSeed.z * 0.8);
    a = sin(ph * 3.14159) * 0.8;
  } else if (uKind < 5.5) {          // 5 bướm: bay lượn
    float ph = aSeed.w * 6.28;
    p.x = uCamX + sin(t * 0.21 + ph) * span * 0.45 + sin(t * 0.9 + ph * 2.0) * 0.5;
    p.z = mix(uArea.y, uArea.w, 0.5 + 0.5 * sin(t * 0.17 + ph * 3.0));
    p.y = 0.9 + sin(t * 0.5 + ph) * 0.5 + abs(sin(t * 6.0 + ph)) * 0.25;
    a = 1.0; size = uSize * (0.7 + 0.5 * abs(sin(t * 9.0 + ph)));
  } else {                           // 6 đài phun
    float ph = fract(t * 0.8 + aSeed.x);
    float ang = aSeed.y * 6.28318; float sp = 0.25 + aSeed.z * 0.55;
    p = uOrigin + vec3(cos(ang) * sp * ph * 1.2, 1.35 * ph * 2.0 * (1.0 - ph * 0.82) + 0.55, sin(ang) * sp * ph * 0.7);
    a = (1.0 - ph) * 0.9; size = uSize * (0.6 + ph * 0.6);
  }
  vA = a; vKind = uKind; vRot = aSeed.w * 6.28318 + t * 1.5; vTw = aSeed.y;
  vec4 mv = viewMatrix * vec4(p, 1.0);
  gl_Position = projectionMatrix * mv;
  gl_PointSize = max(size * uPx / max(-mv.z, 0.5), 1.5);
}`;
export const PARTICLE_FRAG = /* glsl */ `
uniform vec3 uColor; uniform float uOpacity;
varying float vA; varying float vKind; varying float vRot; varying float vTw;
void main(){
  vec2 q = gl_PointCoord - 0.5; float a;
  if (vKind > 0.5 && vKind < 1.5) {
    float c = cos(vRot), s = sin(vRot); vec2 r = vec2(c * q.x - s * q.y, s * q.x + c * q.y);
    a = 1.0 - smoothstep(0.18, 0.28, length(r * vec2(1.0, 2.6)));
  } else if (vKind > 4.5 && vKind < 5.5) {
    a = (1.0 - smoothstep(0.1, 0.45, abs(q.x))) * (1.0 - smoothstep(0.05, 0.3, abs(q.y)));
  } else {
    float d = length(q) * 2.0; a = pow(max(1.0 - d, 0.0), 1.6);
  }
  a *= vA * uOpacity; if (a < 0.01) discard;
  vec3 col = uColor * (0.8 + 0.4 * vTw);
  gl_FragColor = vec4(col * a, a);
  #include <colorspace_fragment>
}`;

// Cột nắng / ánh sáng thể tích: quad đứng cộng sáng, mờ theo chiều ngang và dọc.
export const SHAFT_VERT = /* glsl */ `
attribute vec3 iPos; attribute vec2 iSize; attribute vec3 iMisc;
uniform float uTime; uniform float uPitch;
varying vec2 vUv; varying float vPh; varying float vDepth;
void main(){
  float cp = cos(uPitch), sp = sin(uPitch);
  vec3 l = vec3(position.x * iSize.x + (position.y - 0.5) * iSize.x * 1.1, position.y * iSize.y, 0.0);
  vec3 w = iPos + vec3(l.x, l.y * cp, -l.y * sp);
  vUv = uv; vPh = iMisc.x; vec4 mv = viewMatrix * vec4(w, 1.0); vDepth = -mv.z; gl_Position = projectionMatrix * mv;
}`;
export const SHAFT_FRAG = /* glsl */ `
uniform float uTime; uniform vec3 uColor; uniform float uAlpha;
varying vec2 vUv; varying float vPh; varying float vDepth;
void main(){
  float x = 1.0 - abs(vUv.x * 2.0 - 1.0); x = pow(x, 1.4);
  float y = pow(1.0 - vUv.y, 1.2) * smoothstep(0.0, 0.12, vUv.y);
  float a = x * y * uAlpha * (0.75 + 0.25 * sin(uTime * 0.6 + vPh) + 0.1 * sin(uTime * 1.7 + vPh * 2.0));
  gl_FragColor = vec4(uColor * a, a);
  #include <colorspace_fragment>
}`;

// Hậu kỳ HD-2D: tilt-shift (làm mờ trên/dưới), chỉnh màu, vignette, hạt phim nhẹ.
export const POST_FRAG = /* glsl */ `
uniform sampler2D tDiffuse; uniform vec2 uRes; uniform float uTilt; uniform float uFocus; uniform float uBand;
uniform float uSat; uniform float uContrast; uniform float uWarm; uniform float uVig; uniform float uTime;
varying vec2 vUv;
vec3 sat(vec3 c, float s){ float l = dot(c, vec3(0.299, 0.587, 0.114)); return mix(vec3(l), c, s); }
void main(){
  float d = abs(vUv.y - uFocus);
  float blur = smoothstep(uBand, uBand + 0.32, d) * uTilt;
  vec2 px = 1.0 / uRes; vec3 c = texture2D(tDiffuse, vUv).rgb;
  if (blur > 0.01) {
    vec3 acc = c; float wsum = 1.0;
    for (int i = 1; i <= 4; i++) {
      float fi = float(i) * blur * 1.6;
      vec2 o = vec2(0.0, fi) * px * 2.0; vec2 o2 = vec2(fi, 0.0) * px * 2.0;
      float w = 1.0 - float(i) * 0.18;
      acc += (texture2D(tDiffuse, vUv + o).rgb + texture2D(tDiffuse, vUv - o).rgb + texture2D(tDiffuse, vUv + o2).rgb + texture2D(tDiffuse, vUv - o2).rgb) * 0.25 * w; wsum += w;
    }
    c = mix(c, acc / wsum, clamp(blur * 1.2, 0.0, 1.0));
  }
  c = sat(c, uSat);
  c = (c - 0.5) * uContrast + 0.5;
  c += vec3(uWarm, uWarm * 0.35, -uWarm * 0.6) * 0.5;
  float v = smoothstep(1.15, 0.35, length((vUv - 0.5) * vec2(1.0, 0.9) * 1.55));
  c *= mix(1.0 - uVig, 1.0, v);
  gl_FragColor = vec4(max(c, 0.0), 1.0);
}`;
