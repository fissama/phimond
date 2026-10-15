import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { POST_FRAG } from './shaders.ts';
import { applyGrade, makeShared, SceneRuntime, srgb, TIERS, type SharedUniforms, type Tier } from './sceneBuilder.ts';

export const CAMERA = { fov: 30, pitchDeg: 24, dist: 18, lookY: 0.9 };

export interface FrameStats {
  fps: number; frameMs: number; p95Ms: number; draws: number; triangles: number; textures: number; geometries: number;
  heapMB: number | null; gpu: string; longTasks: number; tier: string; pixelRatio: number; width: number; height: number;
}

export class Engine {
  readonly renderer: THREE.WebGLRenderer;
  readonly scene = new THREE.Scene();
  readonly camera = new THREE.PerspectiveCamera(CAMERA.fov, 2, 0.5, 120);
  readonly U: SharedUniforms = makeShared();
  private composer: EffectComposer | null = null;
  private postPass: ShaderPass | null = null;
  private bloom: UnrealBloomPass | null = null;
  tier: Tier = TIERS.high;
  tierMax: Tier['name'] = 'high';
  auto = true;
  map: SceneRuntime | null = null;
  camTarget = new THREE.Vector3();
  /** phần chiều cao canvas dành cho HUD dưới: cảnh dịch lên để người chơi nằm giữa vùng thế giới nhìn thấy */
  verticalShift = 0.04;
  camDist: number = CAMERA.dist;
  /** Khoảng cách camera khi đi dạo (tự khớp khung cảnh) và độ dịch dọc tương ứng. */
  baseDist: number = CAMERA.dist;
  private fitAspect = 0;
  private artFrame: { topY: number; topZ: number; botZ: number; midZ: number } | null = null;
  private raf = 0;
  private last = 0;
  time = 0;
  private readonly callbacks = new Set<(dt: number, t: number) => void>();
  private readonly ring = new Float32Array(120); private ringN = 0;
  private longTasks = 0;
  private slowRun = 0;
  private readonly ro: ResizeObserver;
  private cssW = 1; private cssH = 1;
  private bg = new THREE.Color();
  private gradeBase = { sat: 1, contrast: 1, warm: 0, vig: 0.3 };
  readonly info = { draws: 0, triangles: 0 };

  constructor(readonly canvas: HTMLCanvasElement, readonly host: HTMLElement) {
    this.renderer = new THREE.WebGLRenderer({ canvas, antialias: false, alpha: false, powerPreference: 'high-performance', stencil: false });
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.info.autoReset = false;
    this.scene.background = this.bg;
    this.ro = new ResizeObserver(() => this.resize());
    this.ro.observe(host);
    this.resize();
    try {
      new PerformanceObserver((l) => { this.longTasks += l.getEntries().length; }).observe({ entryTypes: ['longtask'] });
    } catch { /* Safari không hỗ trợ */ }
    this.setTier(this.defaultTier());
  }

  private defaultTier(): Tier['name'] {
    const q = new URLSearchParams(location.search).get('q');
    if (q === 'low' || q === 'medium' || q === 'high') { this.auto = false; return q; }
    const ua = navigator.userAgent; const mobile = /iPhone|iPad|Android/.test(ua);
    return mobile ? 'medium' : 'high';
  }

  setTier(name: Tier['name']): void {
    this.tier = TIERS[name];
    this.tierMax = this.auto ? this.tierMax : name;
    this.buildPost();
    this.resize();
  }

  private buildPost(): void {
    this.composer?.dispose(); this.composer = null; this.postPass = null; this.bloom = null;
    if (!this.tier.post) return;
    const size = this.renderer.getDrawingBufferSize(new THREE.Vector2());
    const rt = new THREE.WebGLRenderTarget(size.x, size.y, { type: THREE.HalfFloatType, colorSpace: THREE.LinearSRGBColorSpace });
    const c = new EffectComposer(this.renderer, rt);
    c.addPass(new RenderPass(this.scene, this.camera));
    if (this.tier.bloom) { this.bloom = new UnrealBloomPass(new THREE.Vector2(size.x / 2, size.y / 2), 0.28, 0.6, 0.86); c.addPass(this.bloom); }
    this.postPass = new ShaderPass(new THREE.ShaderMaterial({
      uniforms: { tDiffuse: { value: null }, uRes: { value: new THREE.Vector2(size.x, size.y) }, uTilt: { value: this.tier.tilt }, uFocus: { value: 0.42 }, uBand: { value: 0.3 }, uSat: { value: 1 }, uContrast: { value: 1 }, uWarm: { value: 0 }, uVig: { value: 0.3 }, uTime: this.U.uTime },
      vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
      fragmentShader: POST_FRAG,
    }));
    c.addPass(this.postPass); c.addPass(new OutputPass());
    this.composer = c;
    this.applyGradeUniforms();
  }

  private applyGradeUniforms(): void {
    const u = this.postPass?.uniforms; if (!u) return;
    u.uSat!.value = this.gradeBase.sat; u.uContrast!.value = this.gradeBase.contrast; u.uWarm!.value = this.gradeBase.warm; u.uVig!.value = this.gradeBase.vig;
    u.uTilt!.value = this.tier.tilt;
  }

  async loadMap(id: string): Promise<SceneRuntime> {
    const next = await SceneRuntime.load(id, this.U, this.tier);
    if (this.map) { this.scene.remove(this.map.group); this.map.dispose(); }
    this.map = next; this.scene.add(next.group);
    applyGrade(this.U, next.data);
    this.bg.copy(srgb(next.data.bg));
    this.gradeBase = { sat: next.data.grade.sat, contrast: next.data.grade.contrast, warm: next.data.grade.warm, vig: next.data.grade.vignette };
    this.applyGradeUniforms();
    this.artFrame = next.frameInfo(); this.fitFrame();
    return next;
  }

  /** Dựng lại cảnh hiện tại khi đổi tier (hạt/bóng/sương). */
  async reloadMap(): Promise<void> { if (this.map) await this.loadMap(this.map.data.id); }

  onFrame(fn: (dt: number, t: number) => void): () => void { this.callbacks.add(fn); return () => this.callbacks.delete(fn); }

  resize(): void {
    const w = Math.max(1, this.host.clientWidth), h = Math.max(1, this.host.clientHeight);
    this.cssW = w; this.cssH = h;
    const pr = Math.min(window.devicePixelRatio || 1, this.tier.pixelRatio);
    this.renderer.setPixelRatio(pr); this.renderer.setSize(w, h, false);
    this.camera.aspect = w / h; if (this.artFrame && Math.abs(this.camera.aspect - this.fitAspect) > 0.01) { this.fitAspect = this.camera.aspect; queueMicrotask(() => this.fitFrame()); }
    this.camera.setViewOffset(w, h, 0, Math.round(h * this.verticalShift), w, h);
    this.camera.updateProjectionMatrix();
    this.composer?.setPixelRatio(pr); this.composer?.setSize(w, h);
    const size = this.renderer.getDrawingBufferSize(new THREE.Vector2());
    this.postPass?.uniforms.uRes && ((this.postPass.uniforms.uRes.value as THREE.Vector2).set(size.x, size.y));
    this.U.uPx.value = (size.y * 0.5) / Math.tan((CAMERA.fov * Math.PI) / 360);
  }

  private gpuCache = '';
  private gpuName(): string { if (this.gpuCache) return this.gpuCache; try { const gl = this.renderer.getContext(); const e = gl.getExtension('WEBGL_debug_renderer_info'); this.gpuCache = String(gl.getParameter(e ? e.UNMASKED_RENDERER_WEBGL : gl.RENDERER)).slice(0, 40); } catch { this.gpuCache = '?'; } return this.gpuCache; }

  /** Tìm khoảng cách + độ dịch sao cho đỉnh cây và mép dưới của cảnh vừa khít chiều cao vùng nhìn (không còn khoảng trống). */
  fitFrame(): void {
    const f = this.artFrame; if (!f) return;
    const cam = new THREE.PerspectiveCamera(CAMERA.fov, this.camera.aspect, 0.5, 120); const pr = (CAMERA.pitchDeg * Math.PI) / 180;
    const top = new THREE.Vector3(0, f.topY, f.topZ), bot = new THREE.Vector3(0, 0, f.botZ);
    let d = this.baseDist, mid = 0;
    for (let i = 0; i < 12; i++) {
      cam.position.set(0, CAMERA.lookY + Math.sin(pr) * d, f.midZ + Math.cos(pr) * d); cam.lookAt(0, CAMERA.lookY, f.midZ); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
      const a = top.clone().project(cam).y, b = bot.clone().project(cam).y; const span = a - b; mid = (a + b) / 2;
      d = Math.min(24, Math.max(9, d * (span / 2)));
    }
    // Thiết kế gốc có vùng nhìn ~2.1:1. Màn quá ngang (điện thoại xoay ngang) thì thu hẹp bề ngang bằng cách phóng gần và neo mép dưới,
    // để không lộ phần ngoài tranh ở hai bên và vẫn thấy mặt đất.
    const MAXA = 2.3; let shift = -mid / 2;
    if (this.camera.aspect > MAXA) {
      d = Math.max(7, d * (MAXA / this.camera.aspect));
      cam.position.set(0, CAMERA.lookY + Math.sin(pr) * d, f.midZ + Math.cos(pr) * d); cam.lookAt(0, CAMERA.lookY, f.midZ); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
      shift = (-0.22 - new THREE.Vector3(0, 0, f.midZ).project(cam).y) / 2; // chân nhân vật ở ~39% từ đáy, đầu còn chỗ phía trên
    }
    this.baseDist = d; this.camDist = d; this.verticalShift = Math.max(-0.45, Math.min(0.45, shift));
    this.resize();
  }

  /** Nửa bề ngang nhìn thấy tại mặt phẳng người chơi (đơn vị thế giới). */
  get halfWidth(): number { return Math.tan((CAMERA.fov * Math.PI) / 360) * this.camDist * this.camera.aspect; }

  placeCamera(x: number, z: number): void {
    const p = (CAMERA.pitchDeg * Math.PI) / 180;
    this.camera.position.set(x, CAMERA.lookY + Math.sin(p) * this.camDist, z + Math.cos(p) * this.camDist);
    this.camera.lookAt(x, CAMERA.lookY, z);
    this.camera.updateMatrixWorld();
  }

  project(x: number, y: number, z: number, out = { x: 0, y: 0, on: false }): { x: number; y: number; on: boolean } {
    const v = new THREE.Vector3(x, y, z).project(this.camera);
    out.x = (v.x * 0.5 + 0.5) * this.cssW; out.y = (-v.y * 0.5 + 0.5) * this.cssH; out.on = v.z > -1 && v.z < 1;
    return out;
  }

  start(): void {
    if (this.raf) return;
    this.last = performance.now();
    const loop = (now: number): void => {
      this.raf = requestAnimationFrame(loop);
      const dt = Math.min(0.1, (now - this.last) / 1000); this.last = now; this.time += dt;
      this.frame(dt, now);
    };
    this.raf = requestAnimationFrame(loop);
  }
  stop(): void { cancelAnimationFrame(this.raf); this.raf = 0; }

  private frame(dt: number, nowMs: number): void {
    const t0 = performance.now();
    this.map?.update(this.time, this.U.uCamX.value);
    for (const cb of this.callbacks) cb(dt, this.time);
    this.renderer.info.reset();
    if (this.composer) this.composer.render(dt); else this.renderer.render(this.scene, this.camera);
    this.info.draws = this.renderer.info.render.calls; this.info.triangles = this.renderer.info.render.triangles;
    const ms = dt * 1000; this.ring[this.ringN++ % this.ring.length] = ms;
    void t0; void nowMs;
    if (this.auto && this.ringN % 30 === 0) this.autoTier();
  }

  private autoTier(): void {
    const n = Math.min(this.ringN, this.ring.length); let s = 0; for (let i = 0; i < n; i++) s += this.ring[i]!;
    const avg = s / n;
    if (document.hidden) return;
    this.slowRun = avg > 24 ? this.slowRun + 1 : 0;
    if (this.slowRun >= 3 && this.tier.name !== 'low') {
      this.slowRun = 0; this.ringN = 0;
      this.setTier(this.tier.name === 'high' ? 'medium' : 'low'); void this.reloadMap();
    }
  }

  stats(): FrameStats {
    const n = Math.min(this.ringN, this.ring.length) || 1; const arr = Array.from(this.ring.slice(0, n)).sort((a, b) => a - b); const avg = arr.reduce((s, v) => s + v, 0) / n;
    const mem = (performance as unknown as { memory?: { usedJSHeapSize: number } }).memory;
    const r = this.renderer.info;
    return {
      fps: avg > 0 ? 1000 / avg : 0, frameMs: avg, p95Ms: arr[Math.floor(n * 0.95)] ?? avg, draws: this.info.draws, triangles: this.info.triangles, textures: r.memory.textures, geometries: r.memory.geometries,
      heapMB: mem ? mem.usedJSHeapSize / 1048576 : null, gpu: this.gpuName(), longTasks: this.longTasks, tier: this.tier.name, pixelRatio: this.renderer.getPixelRatio(), width: this.cssW, height: this.cssH,
    };
  }

  dispose(): void { this.stop(); this.ro.disconnect(); this.composer?.dispose(); this.map?.dispose(); this.renderer.dispose(); }
}
