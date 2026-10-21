// P12 Stage 3 · Golden Scene Emerald HD-2D · Three.js (WebGLRenderer, r170)
// Cùng dữ liệu ../shared/scene.json với bản Godot. Chỉ để đo; không phải production.
import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';

THREE.ColorManagement.enabled = false; // mọi phép tính ở không gian hiển thị, giống bản Godot
const T0 = performance.now();
const Q = new URLSearchParams(location.search);
const $ = (id) => document.getElementById(id);
const ENGINE = 'three';
const marks = { start: 0 };
const mark = (k) => { marks[k] = Math.round(performance.now() - T0); };

const state = {
  tier: Q.get('tier') || 'high',
  dprCap: parseFloat(Q.get('dpr') || '2'),
  mapId: Q.get('map') || 'emerald_forest_main_woods',
  auto: Q.get('auto') === '1',
  secs: parseFloat(Q.get('secs') || '60'),
  contextLost: 0,
  bench: null,
  mapSwitches: [],
  inputLat: [],
};
const HUD = window.PhimondHUD || { vec: { x: 0, z: 0 }, on() {}, sys() {}, sysq() {}, setResult() {}, setDebug() {}, setState() {}, setFps() {}, setTier() {}, setBenchBusy() {}, shiftFrac: 0 };
HUD.setTier && HUD.setTier(state.tier);

// ---------- tải dữ liệu ----------
const canvas = $('c');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: 'high-performance' });
renderer.outputColorSpace = THREE.LinearSRGBColorSpace; renderer.info.autoReset = false;
canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); state.contextLost++; });
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, state.dprCap));
renderer.setSize(innerWidth, innerHeight, false);
const gl = renderer.getContext();
const dbg = gl.getExtension('WEBGL_debug_renderer_info');
const glInfo = { renderer: dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER), vendor: dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR), version: gl.getParameter(gl.VERSION), maxTex: gl.getParameter(gl.MAX_TEXTURE_SIZE) };

const SCENE = await (await fetch('../shared/scene.json')).json();
mark('json');
const texCache = new Map();
let texBytes = 0;
const loader = new THREE.TextureLoader();
function loadTex(name) {
  if (texCache.has(name)) return texCache.get(name);
  const once = () => new Promise((res, rej) => loader.load('../shared/tex/' + name, (t) => {
    t.magFilter = THREE.NearestFilter; t.minFilter = THREE.NearestFilter; t.generateMipmaps = false;
    t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping; t.premultiplyAlpha = false;
    texBytes += t.image.width * t.image.height * 4; res(t);
  }, undefined, rej));
  const p = (async () => {
    for (let i = 0; i < 3; i++) { try { return await once(); } catch (e) { HUD.sysq(`[lỗi] three tải texture ${name} lần ${i + 1} thất bại`); await new Promise((r) => setTimeout(r, 300 * (i + 1))); } }
    const c = document.createElement('canvas'); c.width = c.height = 8; const g = c.getContext('2d'); g.fillStyle = '#f0f'; g.fillRect(0, 0, 8, 8); const t = new THREE.CanvasTexture(c); t.magFilter = THREE.NearestFilter; return t;
  })();
  texCache.set(name, p); return p;
}
// tải trước tất cả texture để đo
const allTex = new Set(['player.png']);
for (const m of Object.values(SCENE.maps)) { allTex.add(m.ground.tex); m.props.forEach((p) => allTex.add(p.tex)); m.sky.forEach((p) => allTex.add(p.tex)); }
SCENE.actors.pets.forEach((p) => allTex.add(p.tex));
await Promise.all([...allTex].map(loadTex));
mark('textures');

// ---------- cảnh ----------
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(SCENE.camera.fov, innerWidth / innerHeight, 0.5, 120);
const camRight = new THREE.Vector3(1, 0, 0);
const U = { time: { value: 0 }, camRight: { value: camRight }, camPos: { value: cam.position }, player: { value: new THREE.Vector3() }, fog: { value: new THREE.Vector3(0.165, 0.54, 0.6) }, light: { value: 1 } };

const quad = new THREE.BufferGeometry();
quad.setAttribute('position', new THREE.Float32BufferAttribute([-0.5, 0, 0, 0.5, 0, 0, -0.5, 1, 0, 0.5, 1, 0], 3));
quad.setAttribute('uv', new THREE.Float32BufferAttribute([0, 0, 1, 0, 0, 1, 1, 1], 2));
quad.setIndex([0, 1, 2, 2, 1, 3]);

const SPRITE_VS = `
uniform vec3 uCenter; uniform vec2 uSize; uniform float uTime, uSway, uFlip; uniform vec3 uCamRight; uniform vec4 uUV;
varying vec2 vUv; varying vec3 vWorld; varying float vP;
void main(){
  vec2 p = position.xy; vP = p.y;
  vec3 w = uCenter + uCamRight * (p.x * uSize.x) + vec3(0.0, p.y * uSize.y, 0.0);
  w.x += sin(uTime * 1.4 + uCenter.x * 0.9 + uCenter.z * 0.5) * uSway * p.y * p.y * 0.05 * uSize.y;
  vec2 q = uv; if (uFlip < 0.0) q.x = 1.0 - q.x;
  vUv = uUV.xy + q * uUV.zw; vWorld = w;
  gl_Position = projectionMatrix * viewMatrix * vec4(w, 1.0);
}`;
const SPRITE_FS = `
uniform sampler2D map; uniform vec3 uFog, uPlayer, uCamPos; uniform float uLight, uFogAmt, uTopFade;
varying vec2 vUv; varying vec3 vWorld; varying float vP;
void main(){
  vec4 c = texture2D(map, vUv); if (c.a < 0.5) discard;
  vec3 col = c.rgb * vec3(0.93, 0.98, 1.0) * (0.86 + 0.14 * smoothstep(0.0, 3.0, vWorld.y));
  float pool = smoothstep(7.0, 0.0, distance(vWorld.xz, uPlayer.xz)) * 0.22 * uLight;
  col += vec3(1.0, 0.86, 0.55) * pool * c.rgb;
  float f = smoothstep(16.0, 40.0, length(vWorld - uCamPos));
  col = mix(col, uFog, f * uFogAmt);
  col = mix(col, uFog * 0.9, uTopFade * smoothstep(0.78, 1.0, vP));
  gl_FragColor = vec4(col, 1.0);
}`;
function spriteMat(tex, sway, uv) {
  return new THREE.ShaderMaterial({
    vertexShader: SPRITE_VS, fragmentShader: SPRITE_FS, side: THREE.DoubleSide,
    uniforms: {
      map: { value: tex }, uCenter: { value: new THREE.Vector3() }, uSize: { value: new THREE.Vector2(1, 1) },
      uTime: U.time, uSway: { value: sway }, uFlip: { value: 1 }, uCamRight: U.camRight, uUV: { value: new THREE.Vector4(0, 0, 1, 1) },
      uFog: U.fog, uPlayer: U.player, uCamPos: U.camPos, uLight: U.light, uFogAmt: { value: 0.6 }, uTopFade: { value: 0 },
    },
  });
}
function makeSprite(tex, w, h, x, y, z, sway = 0) {
  const m = new THREE.Mesh(quad, spriteMat(tex, sway));
  m.frustumCulled = false;
  m.material.uniforms.uCenter.value.set(x, y, z); m.material.uniforms.uSize.value.set(w, h);
  return m;
}

const GROUND_FS = `
uniform sampler2D map; uniform vec3 uFog, uPlayer, uCamPos; uniform float uLight; uniform vec2 uTile; uniform vec2 uZ;
varying vec3 vWorld;
void main(){
  vec2 uv = vec2(vWorld.x / uTile.x, 1.0 - (vWorld.z - uZ.x) / uTile.y);
  vec3 col = texture2D(map, fract(uv)).rgb;
  float back = smoothstep(uZ.x, uZ.y, vWorld.z);        // tối dần về phía sau
  col *= mix(0.62, 1.0, back);
  float pool = smoothstep(7.5, 0.0, distance(vWorld.xz, uPlayer.xz)) * 0.30 * uLight;
  col += vec3(1.0, 0.86, 0.55) * pool * col;
  float f = smoothstep(16.0, 40.0, length(vWorld - uCamPos));
  col = mix(col, uFog, f * 0.6);
  gl_FragColor = vec4(col, 1.0);
}`;
const GROUND_VS = `varying vec3 vWorld; void main(){ vWorld = (modelMatrix * vec4(position,1.0)).xyz; gl_Position = projectionMatrix * viewMatrix * vec4(vWorld,1.0); }`;

const PART_VS = `
attribute vec4 aSeed; uniform float uTime, uPx; varying float vA;
void main(){
  vec3 p = position;
  p.x += sin(uTime * (0.2 + aSeed.x * 0.4) + aSeed.y * 6.28) * 1.2;
  p.y += sin(uTime * (0.3 + aSeed.z * 0.5) + aSeed.w * 6.28) * 0.6;
  p.z += cos(uTime * (0.15 + aSeed.y * 0.3) + aSeed.x * 6.28) * 0.8;
  vec4 mv = viewMatrix * vec4(p, 1.0);
  gl_Position = projectionMatrix * mv;
  gl_PointSize = (0.10 + 0.12 * aSeed.z) * uPx / -mv.z;
  vA = 0.55 + 0.45 * sin(uTime * (1.0 + aSeed.w * 2.0) + aSeed.x * 20.0);
}`;
const PART_FS = `varying float vA; void main(){ float d = length(gl_PointCoord - 0.5) * 2.0; float a = smoothstep(1.0, 0.0, d); gl_FragColor = vec4(vec3(1.0, 0.95, 0.6) * a * vA, a * vA); }`;
const FX_VS = `varying vec2 vUv; varying vec3 vWorld; void main(){ vUv = uv; vec4 w = modelMatrix * vec4(position,1.0); vWorld = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`;
const SHAFT_FS = `uniform float uTime, uSeed; varying vec2 vUv; void main(){ float e = smoothstep(0.0,0.35,vUv.x) * smoothstep(1.0,0.65,vUv.x); float v = smoothstep(0.0,0.2,vUv.y) * smoothstep(1.0,0.4,vUv.y); float s = 0.75 + 0.25 * sin(uTime * 0.6 + uSeed + vUv.y * 4.0); gl_FragColor = vec4(vec3(1.0,0.93,0.65) * e * v * s * 0.20, 1.0); }`;
const GLOW_FS = `uniform float uTime; varying vec2 vUv; void main(){ vec2 p = vUv - 0.5; float r = length(p) * 2.0; float ring = smoothstep(0.08, 0.0, abs(r - 0.78 - 0.04 * sin(uTime * 2.0))); float core = smoothstep(1.0, 0.0, r) * 0.35; float beam = smoothstep(0.5, 0.0, abs(p.x)) * 0.0; gl_FragColor = vec4(vec3(0.5, 1.0, 0.85) * (ring + core), 1.0); }`;

let current = null; // { id, group, doors, bounds, zRange }
const dynamic = []; // các sprite hoạt họa
const pets = [];
const player = { x: 0, z: 0, facing: 1, moving: false, t: 0, mesh: null, shadow: null };
let particles = null; let particleCount = 0;

function shadowBlob() {
  const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
  const gr = g.createRadialGradient(32, 32, 2, 32, 32, 30); gr.addColorStop(0, 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  const t = new THREE.CanvasTexture(c); const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.05; m.renderOrder = 1; m.material.polygonOffset = true; m.material.polygonOffsetFactor = -2; m.material.polygonOffsetUnits = -2; return m;
}

async function buildMap(id) {
  const t0 = performance.now();
  const M = SCENE.maps[id];
  const g = new THREE.Group();
  const bg = M.bg; scene.background = new THREE.Color(bg[0], bg[1], bg[2]); U.fog.value.set(bg[0], bg[1], bg[2]);
  // nền đất
  const gr0 = M.ground; const gr = { ...gr0, x0: gr0.x0 - 12, x1: gr0.x1 + 12, zFront: gr0.zFront + 4 }; const gw = gr.x1 - gr.x0; const gd = gr.zFront - gr.zBack;
  const gm = new THREE.Mesh(new THREE.PlaneGeometry(gw, gd), new THREE.ShaderMaterial({
    vertexShader: GROUND_VS, fragmentShader: GROUND_FS, uniforms: { map: { value: await loadTex(gr.tex) }, uFog: U.fog, uPlayer: U.player, uCamPos: U.camPos, uLight: U.light, uTile: { value: new THREE.Vector2(gr.tileW, gr.tileD) }, uZ: { value: new THREE.Vector2(gr0.zBack, gr0.zFront) } } }));
  gm.rotation.x = -Math.PI / 2; gm.position.set((gr.x0 + gr.x1) / 2, 0, (gr.zBack + gr.zFront) / 2); gm.frustumCulled = false; g.add(gm);
  // bầu trời: một lớp xa, lát gương liên tục (mép khớp), đáy trùng màu nền
  { const s0 = M.sky[0]; const t = await loadTex(s0.tex); const sc = 2.4; const h = s0.h * sc, w = h * (s0.w / s0.h); let k = 0;
    for (let x = M.bounds[0] - 30; x < M.bounds[1] + 30; x += w, k++) { const sp = makeSprite(t, w * 1.002, h, x + w / 2, 0.6, M.ground.zBack - 7.0, 0); sp.material.uniforms.uFlip.value = k % 2 ? -1 : 1; sp.material.uniforms.uFogAmt.value = 0.0; g.add(sp); } }
  // props
  for (const p of M.props) {
    const sp = makeSprite(await loadTex(p.tex), p.w, p.h, p.x, 0, p.z, p.sway);
    if (/^(9_0|10_0|11_0)/.test(p.tex)) sp.material.uniforms.uTopFade.value = 0.9;
    g.add(sp);
  }
  // cửa
  const doors = [];
  for (const d of M.doors || []) {
    const gm2 = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.6), new THREE.ShaderMaterial({ vertexShader: FX_VS, fragmentShader: GLOW_FS, uniforms: { uTime: U.time }, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
    gm2.rotation.x = -Math.PI / 2; gm2.position.set(d.x, 0.03, d.z); gm2.renderOrder = 2; g.add(gm2); doors.push({ ...d, armed: false });
  }
  // tia sáng
  const shafts = [];
  for (let i = 0; i < 3; i++) {
    const sm = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 9), new THREE.ShaderMaterial({ vertexShader: FX_VS, fragmentShader: SHAFT_FS, uniforms: { uTime: U.time, uSeed: { value: i * 2.1 } }, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
    sm.position.set(M.bounds[0] + (M.bounds[1] - M.bounds[0]) * (0.2 + 0.3 * i), 4.0, M.ground.zBack + 0.6 + i * 0.4); sm.rotation.z = -0.35; sm.renderOrder = 3; g.add(sm); shafts.push(sm);
  }
  g.userData.shafts = shafts;
  // hạt
  const maxP = 240; const pos = new Float32Array(maxP * 3), seed = new Float32Array(maxP * 4);
  let r = 12345; const rnd = () => (r = (r * 1664525 + 1013904223) >>> 0) / 4294967296;
  for (let i = 0; i < maxP; i++) { pos[i * 3] = M.bounds[0] + rnd() * (M.bounds[1] - M.bounds[0]); pos[i * 3 + 1] = 0.2 + rnd() * 3.4; pos[i * 3 + 2] = M.zRange[0] + rnd() * (M.zRange[1] - M.zRange[0] + 3); for (let k = 0; k < 4; k++) seed[i * 4 + k] = rnd(); }
  const pg = new THREE.BufferGeometry(); pg.setAttribute('position', new THREE.BufferAttribute(pos, 3)); pg.setAttribute('aSeed', new THREE.BufferAttribute(seed, 4));
  const pts = new THREE.Points(pg, new THREE.ShaderMaterial({ vertexShader: PART_VS, fragmentShader: PART_FS, uniforms: { uTime: U.time, uPx: { value: 1 } }, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
  pts.material.uniforms.uPx.value = innerHeight * renderer.getPixelRatio() / (2 * Math.tan(THREE.MathUtils.degToRad(SCENE.camera.fov / 2)));
  pts.frustumCulled = false; pts.renderOrder = 4; g.add(pts); g.userData.pts = pts;
  // pet (atlas P10)
  const pa = SCENE.actors.petAtlas; const petList = [];
  for (const p of SCENE.actors.pets) {
    if (p.map !== id) continue;
    const ft = pa.feet[p.id] || { pad: 0, w: 0.5 }; const sp = makeSprite(await loadTex(p.tex), pa.h, pa.h, p.x, -ft.pad * pa.h, p.z, 0); sp.material.uniforms.uUV.value.set(0, 0, 1 / pa.cols, 1 / pa.rows);
    g.add(sp); const sh = shadowBlob(); sh.scale.set(pa.h * ft.w * 1.1, pa.h * ft.w * 0.5, 1); sh.position.set(p.x, 0.05, p.z + 0.05); g.add(sh);
    petList.push({ sp, p, phase: Math.random() * 4 });
  }
  // người chơi
  const pl = SCENE.actors.player; const pm = makeSprite(await loadTex(pl.tex), pl.h * (pl.cell[0] / pl.cell[1]), pl.h, 0, 0, 0, 0);
  pm.material.uniforms.uUV.value.set(0, 0.5, 1 / pl.cols, 1 / pl.rows); g.add(pm);
  const psh = shadowBlob(); psh.scale.set(0.9, 0.5, 1); g.add(psh);
  player.mesh = pm; player.shadow = psh;
  scene.add(g);
  if (current) { scene.remove(current.group); disposeGroup(current.group); }
  current = { id, group: g, doors, bounds: M.bounds, zRange: M.zRange, pets: petList, pts };
  setTier(state.tier);
  return performance.now() - t0;
}
function disposeGroup(g) { g.traverse((o) => { if (o.geometry && o.geometry !== quad) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }

async function switchMap(id, arrive, why) {
  const t0 = performance.now();
  const build = await buildMap(id);
  player.x = arrive[0]; player.z = arrive[1];
  for (const d of current.doors) d.armed = false; // chống kích hoạt lại ngay (R-S2-1): chỉ armed sau khi rời vùng cửa
  state.mapId = id; HUD.setState({ map: id.includes('deep') ? 'Emerald · Rừng sâu' : 'Emerald · Rừng chính' });
  const total = performance.now() - t0;
  state.mapSwitches.push({ to: id, why, buildMs: +build.toFixed(1), totalMs: +total.toFixed(1), at: Math.round(performance.now() - T0) });
  HUD.sysq(`[đo] three · đổi map → ${id.replace('emerald_forest_', '')}: dựng ${build.toFixed(0)} ms · tổng ${total.toFixed(0)} ms (${why})`);
  toast(`→ ${SCENE.maps[id].doors?.[0]?.label ? id.replace('emerald_forest_', '') : id} (${total.toFixed(0)} ms)`);
}

// ---------- hậu kỳ ----------
const TILT_SHADER = {
  uniforms: { tDiffuse: { value: null }, uRes: { value: new THREE.Vector2(1, 1) }, uTilt: { value: 1 }, uTime: U.time },
  vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }',
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform vec2 uRes; uniform float uTilt; varying vec2 vUv;
    void main(){
      float d = abs(vUv.y - 0.52);
      float r = uTilt * smoothstep(0.18, 0.55, d) * 3.2;
      vec2 px = r / uRes;
      vec3 c = texture2D(tDiffuse, vUv).rgb * 0.2;
      c += texture2D(tDiffuse, vUv + vec2( px.x, 0.0)).rgb * 0.1 + texture2D(tDiffuse, vUv - vec2( px.x, 0.0)).rgb * 0.1;
      c += texture2D(tDiffuse, vUv + vec2(0.0,  px.y)).rgb * 0.1 + texture2D(tDiffuse, vUv - vec2(0.0,  px.y)).rgb * 0.1;
      c += texture2D(tDiffuse, vUv + px * vec2( 0.7,  0.7)).rgb * 0.1 + texture2D(tDiffuse, vUv + px * vec2(-0.7, -0.7)).rgb * 0.1;
      c += texture2D(tDiffuse, vUv + px * vec2( 0.7, -0.7)).rgb * 0.1 + texture2D(tDiffuse, vUv + px * vec2(-0.7,  0.7)).rgb * 0.1;
      // grade: tăng bão hòa nhẹ, tông ấm ở sáng / lạnh ở tối, vignette
      float l = dot(c, vec3(0.299, 0.587, 0.114));
      c = mix(vec3(l), c, 1.12);
      c *= mix(vec3(0.93, 0.98, 1.05), vec3(1.06, 1.0, 0.92), smoothstep(0.2, 0.8, l));
      float v = smoothstep(0.95, 0.35, length((vUv - 0.5) * vec2(1.15, 1.0)));
      c *= mix(0.72, 1.0, v);
      gl_FragColor = vec4(c, 1.0);
    }`,
};
let composer = null, bloom = null, tiltPass = null;
function setupComposer() {
  const dpr = renderer.getPixelRatio();
  composer = new EffectComposer(renderer); composer.setPixelRatio(dpr); composer.setSize(innerWidth, innerHeight);
  composer.addPass(new RenderPass(scene, cam));
  bloom = new UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), 0.55, 0.6, 0.78); composer.addPass(bloom);
  tiltPass = new ShaderPass(TILT_SHADER); composer.addPass(tiltPass);
}
function setTier(t) {
  state.tier = t; const T = SCENE.tiers[t];
  if (!composer) setupComposer();
  bloom.enabled = !!T.bloom; tiltPass.enabled = !!T.tilt; state.post = !!T.post;
  if (current) {
    particleCount = T.particles; current.pts.visible = particleCount > 0; current.pts.geometry.setDrawRange(0, particleCount);
    current.group.userData.shafts.forEach((s) => (s.visible = !!T.shafts));
  }
  U.light.value = T.post ? 1 : 0.6; state.sway = T.sway;
}
function resize() {
  renderer.setSize(innerWidth, innerHeight, false); cam.aspect = innerWidth / innerHeight; cam.updateProjectionMatrix();
  if (composer) { composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(innerWidth, innerHeight); }
  if (tiltPass) tiltPass.uniforms.uRes.value.set(innerWidth * renderer.getPixelRatio(), innerHeight * renderer.getPixelRatio());
  if (current) current.pts.material.uniforms.uPx.value = innerHeight * renderer.getPixelRatio() / (2 * Math.tan(THREE.MathUtils.degToRad(cam.fov / 2)));
}
addEventListener('resize', resize);

// ---------- input ----------
const keys = new Set(); let joy = { x: 0, z: 0 }; let firstInputT = 0;
const noteInput = (t) => { if (!firstInputT) firstInputT = t; };
addEventListener('keydown', (e) => { keys.add(e.key.toLowerCase()); noteInput(e.timeStamp); });
addEventListener('keyup', (e) => keys.delete(e.key.toLowerCase()));
let joyId = null; // d-pad nằm trong HUD (HUD.vec)
HUD.on('input', (v) => noteInput(performance.now()));
HUD.on('tier', (t) => setTier(t));
HUD.on('pillar', () => pillarTeleport());
HUD.on('bench', () => startBench());
HUD.on('save', () => saveResult());
function pillarTeleport() { return switchMap('emerald_forest_deep_woods', SCENE.maps.emerald_forest_deep_woods.spawn, 'pillar'); }
function toast(s) { HUD.sys(s); }

// ---------- bot ----------
const bot = { on: false, leg: 0 };
function botInput() {
  const M = current; const mid = M.id; const door = mid === 'emerald_forest_main_woods' ? M.doors[0] : M.doors[0];
  const farX = mid === 'emerald_forest_main_woods' ? M.bounds[0] + 2.0 : M.bounds[1] - 3.0;
  const targetX = bot.leg === 0 ? farX : door.x;
  const dx = targetX - player.x; if (Math.abs(dx) < 0.25) bot.leg ^= 1;
  const wob = Math.sin(performance.now() / 1500) * 1.2; const dz = wob - player.z;
  return { x: Math.sign(dx) * (Math.abs(dx) > 0.2 ? 1 : 0), z: Math.max(-1, Math.min(1, dz)) * 0.5 };
}

// ---------- vòng lặp ----------
const SPEED = 3.2; let last = 0; let frameNo = 0; let hudT = 0; let animT = 0; let inputPending = 0;
function update(dt, now) {
  U.time.value = now / 1000;
  let ix = 0, iz = 0;
  if (keys.has('arrowleft') || keys.has('a')) ix -= 1; if (keys.has('arrowright') || keys.has('d')) ix += 1;
  if (keys.has('arrowup') || keys.has('w')) iz -= 1; if (keys.has('arrowdown') || keys.has('s')) iz += 1;
  ix += HUD.vec.x; iz += HUD.vec.z;
  if (bot.on) { const b = botInput(); ix = b.x; iz = b.z; }
  const m = Math.hypot(ix, iz); if (m > 1) { ix /= m; iz /= m; }
  const px = player.x, pz = player.z;
  player.x = Math.min(current.bounds[1] - 0.4, Math.max(current.bounds[0] + 0.4, player.x + ix * SPEED * dt));
  player.z = Math.min(current.zRange[1], Math.max(current.zRange[0], player.z + iz * SPEED * dt));
  player.moving = (Math.abs(player.x - px) + Math.abs(player.z - pz)) > 1e-5;
  if (player.moving && firstInputT) { state.inputLat.push(+(now - firstInputT).toFixed(2)); firstInputT = 0; }
  if (!player.moving && !keys.size && !HUD.vec.x && !HUD.vec.z && !bot.on) firstInputT = 0;
  if (ix > 0.05) player.facing = 1; else if (ix < -0.05) player.facing = -1;
  // anim
  animT += dt; const pl = SCENE.actors.player; const frame = Math.floor(animT * pl.fps) % 6; const row = player.moving ? 1 : 0; // hàng 0 trên cùng
  const pu = player.mesh.material.uniforms; pu.uUV.value.set(frame / pl.cols, 1 - (row + 1) / pl.rows, 1 / pl.cols, 1 / pl.rows); pu.uFlip.value = player.facing; pu.uCenter.value.set(player.x, 0, player.z);
  player.shadow.position.set(player.x, 0.05, player.z + 0.05); U.player.value.set(player.x, 0, player.z);
  const pa = SCENE.actors.petAtlas;
  for (const p of current.pets) { const f = Math.floor((animT + p.phase) * pa.fps) % 4; p.sp.material.uniforms.uUV.value.set(f / pa.cols, 1 - (pa.idleRow + 1) / pa.rows, 1 / pa.cols, 1 / pa.rows); }
  // camera
  const pitch = THREE.MathUtils.degToRad(SCENE.camera.pitchDeg), d = SCENE.camera.dist;
  const tx = THREE.MathUtils.clamp(player.x, current.bounds[0] + 7, current.bounds[1] - 7), tz = player.z * 0.6;
  const shiftY = (HUD.shiftFrac || 0) * 2 * d * Math.tan(THREE.MathUtils.degToRad(SCENE.camera.fov / 2)) / 2;
  cam.position.lerp(new THREE.Vector3(tx, 1.0 - shiftY + Math.sin(pitch) * d, tz + Math.cos(pitch) * d), 1 - Math.exp(-SCENE.camera.follow * dt));
  cam.lookAt(cam.position.x, 1.0 - shiftY, cam.position.z - Math.cos(pitch) * d); cam.updateMatrixWorld();
  camRight.setFromMatrixColumn(cam.matrixWorld, 0); camRight.y = 0; camRight.normalize();
  // cửa
  for (const door of current.doors) {
    const near = Math.abs(player.x - door.x) < 0.7 && Math.abs(player.z - door.z) < 1.6;
    if (!near) door.armed = true;
    else if (door.armed) {
      door.armed = false;
      if (door.to) { switchMap(door.to, door.arrive, 'door:' + door.id); return 'switch'; }
      else { toast('Cổng Hoàng cung → (đường về/recovery) quay lại bằng trụ'); pillarTeleport(); return 'switch'; }
    }
  }
}
let switching = false;
function frame(now) {
  requestAnimationFrame(frame);
  if (!last) { last = now; return; }
  renderer.info.reset();
  const dt = Math.min(0.1, (now - last) / 1000); const raw = now - last; last = now;
  if (!switching) { switching = true; const r = update(dt, now); if (r === 'switch') { Promise.resolve().then(() => 0); } switching = false; }
  if (state.post) composer.render(); else renderer.render(scene, cam);
  frameNo++;
  if (frameNo === 1) mark('firstFrame');
  if (state.bench) { if (frameNo > state.bench.warm) state.bench.dts.push(raw); else state.bench.warmDts.push(raw); const el = (now - state.bench.t0) / 1000; if (el >= state.secs) finishBench(); }
  sysWindow(raw);
  if (now - hudT > 500) { hudT = now; hud(raw); }
}
const win = { dts: [], t0: performance.now() };
function sysWindow(raw) {
  win.dts.push(raw); const now = performance.now(); if (now - win.t0 < 5000) return;
  const d = win.dts; const sum = d.reduce((a, b) => a + b, 0); const i = renderer.info; const h = performance.memory ? (performance.memory.usedJSHeapSize / 1048576).toFixed(0) + 'MB' : 'n/a';
  HUD.sysq(`[đo] three · ${state.tier} · ${(1000 * d.length / sum).toFixed(1)} fps · avg ${(sum / d.length).toFixed(1)} · p95 ${pct(d, 0.95).toFixed(1)} · max ${Math.max(...d).toFixed(1)} ms · calls ${i.render.calls} · tris ${(i.render.triangles / 1000).toFixed(1)}k · heap ${h}`);
  win.dts = []; win.t0 = now;
}
function hud(raw) {
  const i = renderer.info; const h = performance.memory ? (performance.memory.usedJSHeapSize / 1048576).toFixed(0) + 'MB' : 'n/a';
  const dbg = `three r${THREE.REVISION} · tier ${state.tier} · dpr ${renderer.getPixelRatio().toFixed(2)} · ${innerWidth}x${innerHeight}\n${(1000 / raw).toFixed(0)} fps · ${raw.toFixed(1)} ms · calls ${i.render.calls} · tris ${i.render.triangles}\nmap ${current.id.replace('emerald_forest_', '')} · x ${player.x.toFixed(1)} · heap ${h}${state.bench ? '\nBENCH ' + Math.round((performance.now() - state.bench.t0) / 1000) + '/' + state.secs + 's' : ''}`;
  HUD.setDebug(dbg); HUD.setFps(`${(1000 / raw).toFixed(0)} fps · ${raw.toFixed(1)} ms · three`);
}

// ---------- bench ----------
function startBench() { bot.on = true; bot.leg = 0; state.mapSwitches = []; state.inputLat = []; state.bench = { t0: performance.now(), dts: [], warmDts: [], warm: parseInt(Q.get('warm') || '120'), startTier: state.tier, calls: 0 }; HUD.setBenchBusy(true); toast('Bench bắt đầu'); }
const BR = {}; // kết quả bench đã xong, theo tier
function pct(a, p) { const s = [...a].sort((x, y) => x - y); return s.length ? s[Math.min(s.length - 1, Math.floor(s.length * p))] : 0; }
function finishBench() {
  const b = state.bench; state.bench = null; bot.on = false; HUD.setBenchBusy(false);
  const d = b.dts; const sum = d.reduce((x, y) => x + y, 0);
  const res = collect();
  res.frames = { n: d.length, seconds: +(sum / 1000).toFixed(2), fpsAvg: +(1000 * d.length / sum).toFixed(2), avgMs: +(sum / d.length).toFixed(2), p50Ms: +pct(d, 0.5).toFixed(2), p95Ms: +pct(d, 0.95).toFixed(2), p99Ms: +pct(d, 0.99).toFixed(2), maxMs: +Math.max(...d).toFixed(2), over16_7: d.filter((x) => x > 16.9).length, over33: d.filter((x) => x > 33.4).length, over50: d.filter((x) => x > 50).length, warmupFrames: b.warmDts.length };
  res.fps1pLow = +(1000 / pct(d, 0.99)).toFixed(2);
  HUD.sysq(`[đo] three bench ${state.tier}: ${res.frames.fpsAvg} fps · avg ${res.frames.avgMs} · p50 ${res.frames.p50Ms} · p95 ${res.frames.p95Ms} · p99 ${res.frames.p99Ms} · max ${res.frames.maxMs} ms · >33ms: ${res.frames.over33}`);
  BR[res.tier] = res; window.__bench = res; saveResult(res); toast(`Xong: ${res.frames.fpsAvg} fps, p95 ${res.frames.p95Ms} ms`);
}
function collect() {
  const res = performance.getEntriesByType('resource'); const bytes = res.reduce((s, r) => s + (r.encodedBodySize || 0), 0);
  const nav = performance.getEntriesByType('navigation')[0];
  const inl = [...state.inputLat].sort((a, b) => a - b);
  return {
    engine: ENGINE, engineVersion: 'three r' + THREE.REVISION + ' WebGLRenderer', page: location.href, when: new Date().toISOString(),
    tier: state.tier, dprCap: state.dprCap, dpr: renderer.getPixelRatio(), canvas: [innerWidth, innerHeight], ua: navigator.userAgent, cores: navigator.hardwareConcurrency, deviceMemoryGB: navigator.deviceMemory ?? null,
    gl: glInfo, load: { marksMs: marks, domInteractiveMs: nav ? Math.round(nav.domInteractive) : null, transferBytes: bytes, textureBytesEstimate: texBytes },
    render: { calls: renderer.info.render.calls, triangles: renderer.info.render.triangles, geometries: renderer.info.memory.geometries, textures: renderer.info.memory.textures },
    memory: { jsHeapMB: performance.memory ? +(performance.memory.usedJSHeapSize / 1048576).toFixed(1) : null, note: 'Safari không công bố heap; dùng Web Inspector Timeline/Instruments cho iOS' },
    contextLost: state.contextLost, mapSwitches: state.mapSwitches, input: { samples: inl.length, p50Ms: inl.length ? inl[Math.floor(inl.length / 2)] : null, maxMs: inl.length ? inl[inl.length - 1] : null },
  };
}
async function saveResult(res) {
  res = res || BR[state.tier] || Object.assign(collect(), { note: 'CHƯA có bench hoàn tất cho tier này; frames=null' }); res.frames = res.frames || null; window.__bench = res;
  const txt = JSON.stringify(res, null, 1);
  try { const r = await fetch('/__result?engine=three&tier=' + state.tier, { method: 'POST', body: txt, headers: { 'content-type': 'application/json' } }); if (r.ok) toast('Đã gửi kết quả về máy chủ'); } catch (e) { /* máy chủ tĩnh không có /__result */ }
  HUD.setResult && HUD.setResult(txt);
  try { await navigator.clipboard.writeText(txt); } catch (e) { /* bỏ qua */ }
  console.log('BENCH_RESULT ' + JSON.stringify(res));
}

// ---------- khởi động ----------
(async () => {
  setupComposer();
  const bt = await buildMap(state.mapId);
  const sp = SCENE.maps[state.mapId].spawn; player.x = sp[0]; player.z = sp[1];
  resize(); mark('ready'); $('msg').remove();
  const P0 = SCENE.actors.pets[0];
  HUD.setState({ name: 'Phimond', level: 12, map: 'Emerald · Rừng chính', gold: 2400, crystals: 15, playerImg: '../shared/tex/player.png', pet: { name: P0.name, level: 5, hp: 82, maxHp: 120, mp: 32, maxMp: 45, img: '../shared/tex/' + P0.tex } });
  { const rs = performance.getEntriesByType('resource'); const bytes = rs.reduce((a, r) => a + (r.encodedBodySize || 0), 0);
    HUD.sysq(`[đo] three r${THREE.REVISION} · GPU ${glInfo.renderer} · DPR ${(window.devicePixelRatio || 1).toFixed(2)} → ${renderer.getPixelRatio().toFixed(2)} · ${innerWidth}x${innerHeight}`);
    HUD.sysq(`[đo] tải: dữ liệu ${marks.json ?? '?'} ms · texture ${marks.textures ?? '?'} ms · sẵn sàng ${marks.ready} ms · truyền ${(bytes / 1048576).toFixed(1)} MB · texture ${(texBytes / 1048576).toFixed(1)} MB`); }
  window.__three = { state, SCENE, switchMap, pillarTeleport, startBench, setTier, get player() { return player; }, collect };
  if (state.auto) startBench();
  requestAnimationFrame(frame);
})().catch((e) => { const m = $('msg'); if (m) m.textContent = 'Lỗi: ' + e.message; console.error('INIT', (e && e.stack) || e); });
