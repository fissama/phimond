import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { Pass, FullScreenQuad } from 'three/examples/jsm/postprocessing/Pass.js';
import { FG_LAYER } from './layers.ts';
import type { Light } from './daylight.ts';
import type { Quality } from '../state/settings.ts';

/**
 * Hậu kỳ kiểu HD-2D (Octopath): làm mờ dải trên/dưới (tilt-shift) để cảnh như mô hình thu nhỏ, bloom ở vùng sáng
 * (đèn, nắng), chỉnh màu theo giờ trong ngày và tối góc. Cao: đủ bộ; Trung bình: tilt-shift + chỉnh màu + tối góc
 * (không bloom); Thấp: không dùng (render thẳng).
 */
const GRADE = {
  uniforms: {
    tDiffuse: { value: null as THREE.Texture | null },
    res: { value: new THREE.Vector2(1, 1) },
    blur: { value: 1 },
    tint: { value: new THREE.Vector3(1, 1, 1) },
    sat: { value: 1 },
    bright: { value: 1 },
    vig: { value: 0.32 },
    contrast: { value: 1 },
    shade: { value: new THREE.Vector3(0, 0, 0) },
    hi: { value: new THREE.Vector3(0, 0, 0) },
  },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform vec2 res; uniform float blur; uniform vec3 tint; uniform float sat; uniform float bright; uniform float vig; uniform float contrast; uniform vec3 shade; uniform vec3 hi;
    varying vec2 vUv;
    void main(){
      // Tilt-shift kiểu Octopath: dải nét hẹp ở giữa, mờ nhanh lên/xuống (2 vòng, 16 điểm).
      float d = abs(vUv.y - 0.46);
      float amt = smoothstep(0.1, 0.5, d) * blur;
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      if (amt > 0.001) {
        float r = amt * 7.0 / res.y;
        vec3 s = c; float wsum = 1.0;
        for (int i = 0; i < 16; i++) {
          float a = float(i) * 0.3926991;
          float k = (i % 2 == 0) ? 1.0 : 0.55;
          vec2 o = vec2(cos(a) * res.y / res.x, sin(a)) * r * k;
          vec3 t = texture2D(tDiffuse, vUv + o).rgb;
          float w = 1.0 + 1.5 * smoothstep(0.7, 1.0, dot(t, vec3(0.299, 0.587, 0.114))); // đốm sáng nở như bokeh
          s += t * w; wsum += w;
        }
        c = mix(c, s / wsum, clamp(amt * 1.6, 0.0, 1.0));
      }
      float l = dot(c, vec3(0.299, 0.587, 0.114));
      c = mix(vec3(l), c, sat) * tint * bright;
      // Tách tông + tương phản: vùng tối ngả màu (xanh tím), vùng sáng ngả ấm — nét phối màu HD-2D.
      float lum = dot(c, vec3(0.299, 0.587, 0.114));
      c += shade * (1.0 - smoothstep(0.0, 0.55, lum)) + hi * smoothstep(0.5, 1.0, lum);
      c = (c - 0.5) * contrast + 0.5;
      c = c * (1.0 + 0.12 * smoothstep(0.6, 1.0, dot(c, vec3(0.299, 0.587, 0.114)))); // đẩy vùng sáng cho bloom/phát sáng
      vec2 q = vUv - 0.5;
      c *= 1.0 - vig * smoothstep(0.25, 0.85, dot(q, q) * 2.2);
      gl_FragColor = vec4(c, 1.0);
    }`,
};


/**
 * Tiền cảnh mờ theo độ sâu: vật ở lớp FG_LAYER (cành lá, cờ, đèn, rèm sát camera) được vẽ riêng ra render target nửa độ phân
 * giải, làm mờ Gauss hai chiều (cộng alpha nhân sẵn để mép không viền đen) rồi chồng lên cảnh trước khi phối màu/bloom.
 * Độ mờ đo bằng điểm ảnh, tăng theo chiều cao màn hình. Cảnh không có vật nào ở lớp này thì bỏ qua bước vẽ.
 */
const BLUR_FRAG = `
  uniform sampler2D tIn; uniform vec2 dir; uniform float premul;
  varying vec2 vUv;
  void main(){
    vec4 acc = vec4(0.0); float ws = 0.0;
    for (int i = -6; i <= 6; i++) {
      float f = float(i);
      float w = exp(-f * f / 18.0);
      vec4 t = texture2D(tIn, vUv + dir * f);
      if (premul > 0.5) t.rgb *= t.a;
      acc += t * w; ws += w;
    }
    gl_FragColor = acc / ws;
  }`;
const COMP_FRAG = `
  uniform sampler2D tBase; uniform sampler2D tFg;
  varying vec2 vUv;
  void main(){
    vec4 b = texture2D(tBase, vUv);
    vec4 f = texture2D(tFg, vUv);
    gl_FragColor = vec4(f.rgb + b.rgb * (1.0 - f.a), 1.0);
  }`;
const VERT = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }';

class FgBlurPass extends Pass {
  radius = 5;
  private readonly rtA = new THREE.WebGLRenderTarget(64, 64, { type: THREE.HalfFloatType });
  private readonly rtB = new THREE.WebGLRenderTarget(64, 64, { type: THREE.HalfFloatType });
  private readonly blurMat = new THREE.ShaderMaterial({ uniforms: { tIn: { value: null }, dir: { value: new THREE.Vector2() }, premul: { value: 1 } }, vertexShader: VERT, fragmentShader: BLUR_FRAG, depthTest: false, depthWrite: false });
  private readonly compMat = new THREE.ShaderMaterial({ uniforms: { tBase: { value: null }, tFg: { value: null } }, vertexShader: VERT, fragmentShader: COMP_FRAG, depthTest: false, depthWrite: false });
  private readonly quad = new FullScreenQuad(this.blurMat);
  private size = new THREE.Vector2(1, 1);
  constructor(private readonly scene: THREE.Scene, private readonly camera: THREE.Camera) {
    super();
    this.rtA.depthBuffer = true;
  }
  override setSize(w: number, h: number): void {
    this.size.set(w, h);
    const hw = Math.max(32, Math.floor(w / 2));
    const hh = Math.max(32, Math.floor(h / 2));
    this.rtA.setSize(hw, hh);
    this.rtB.setSize(hw, hh);
  }
  override render(renderer: THREE.WebGLRenderer, writeBuffer: THREE.WebGLRenderTarget, readBuffer: THREE.WebGLRenderTarget): void {
    const cam = this.camera;
    const prevMask = cam.layers.mask;
    const prevBg = this.scene.background;
    const prevFog = this.scene.fog;
    const prevClear = renderer.getClearColor(new THREE.Color());
    const prevAlpha = renderer.getClearAlpha();
    cam.layers.set(FG_LAYER);
    this.scene.background = null;
    this.scene.fog = null;
    renderer.setRenderTarget(this.rtA);
    renderer.setClearColor(0x000000, 0);
    renderer.clear();
    renderer.render(this.scene, cam);
    cam.layers.mask = prevMask;
    this.scene.background = prevBg;
    this.scene.fog = prevFog;
    renderer.setClearColor(prevClear, prevAlpha);
    // Gauss tách hai chiều (nửa độ phân giải).
    const px = this.radius / this.rtA.width;
    const py = this.radius / this.rtA.height / 6;
    this.quad.material = this.blurMat;
    this.blurMat.uniforms.tIn!.value = this.rtA.texture;
    (this.blurMat.uniforms.dir!.value as THREE.Vector2).set(px / 6, 0);
    this.blurMat.uniforms.premul!.value = 1;
    renderer.setRenderTarget(this.rtB);
    this.quad.render(renderer);
    this.blurMat.uniforms.tIn!.value = this.rtB.texture;
    (this.blurMat.uniforms.dir!.value as THREE.Vector2).set(0, this.radius / this.rtA.height / 6);
    this.blurMat.uniforms.premul!.value = 0;
    renderer.setRenderTarget(this.rtA);
    this.quad.render(renderer);
    void py;
    this.quad.material = this.compMat;
    this.compMat.uniforms.tBase!.value = readBuffer.texture;
    this.compMat.uniforms.tFg!.value = this.rtA.texture;
    renderer.setRenderTarget(this.renderToScreen ? null : writeBuffer);
    this.quad.render(renderer);
  }
  override dispose(): void {
    this.rtA.dispose();
    this.rtB.dispose();
    this.blurMat.dispose();
    this.compMat.dispose();
    this.quad.dispose();
  }
}

export class Post {
  private readonly composer: EffectComposer;
  private readonly bloom: UnrealBloomPass;
  private readonly grade: ShaderPass;
  private readonly fg: FgBlurPass;
  /** Bật khi cảnh hiện tại có vật ở lớp tiền cảnh. */
  hasFg = false;
  private quality: Quality = 'high';

  constructor(renderer: THREE.WebGLRenderer, scene: THREE.Scene, camera: THREE.Camera) {
    this.composer = new EffectComposer(renderer);
    this.composer.addPass(new RenderPass(scene, camera));
    this.fg = new FgBlurPass(scene, camera);
    this.composer.addPass(this.fg);
    this.bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.35, 0.6, 0.82);
    this.composer.addPass(this.bloom);
    this.grade = new ShaderPass(GRADE);
    this.composer.addPass(this.grade);
    this.composer.addPass(new OutputPass());
  }

  setQuality(q: Quality): void {
    this.quality = q;
    this.bloom.enabled = q !== 'low';
    this.grade.uniforms.blur!.value = q === 'high' ? 1 : 0.85;
  }

  setSize(w: number, h: number, pixelRatio: number): void {
    this.composer.setPixelRatio(pixelRatio);
    this.composer.setSize(w, h);
    this.grade.uniforms.res!.value.set(w * pixelRatio, h * pixelRatio);
    // Bloom ở nửa độ phân giải cho nhẹ.
    const div = this.quality === 'high' ? 2 : 4;
    this.fg.setSize(w * pixelRatio, h * pixelRatio);
    this.fg.radius = 6 * Math.max(1, (h * pixelRatio) / 720);
    this.bloom.setSize(Math.max(64, Math.floor((w * pixelRatio) / div)), Math.max(64, Math.floor((h * pixelRatio) / div)));
  }

  setLight(l: Light): void {
    const u = this.grade.uniforms;
    (u.tint!.value as THREE.Vector3).set(l.tint[0], l.tint[1], l.tint[2]);
    u.sat!.value = l.sat;
    u.bright!.value = l.bright;
    u.contrast!.value = l.contrast;
    (u.shade!.value as THREE.Vector3).set(l.shade[0], l.shade[1], l.shade[2]);
    (u.hi!.value as THREE.Vector3).set(l.hi[0], l.hi[1], l.hi[2]);
    u.vig!.value = 0.42 + l.night * 0.22;
    // Ban đêm bloom mạnh hơn để đèn lồng tỏa sáng.
    this.bloom.strength = (this.quality === 'high' ? 0.34 : 0.2) + l.night * 0.35;
    this.bloom.threshold = 0.8 - l.night * 0.2;
  }

  render(dt: number): void {
    this.fg.enabled = this.hasFg;
    this.composer.render(dt);
  }

  dispose(): void {
    this.fg.dispose();
    this.composer.dispose();
  }
}
