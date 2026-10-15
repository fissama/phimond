import * as THREE from 'three';
import { loadJson, loadTexture } from './assets.ts';
import * as SH from './shaders.ts';

export interface SceneProp {
  tex: string; x: number; z: number; w: number; h: number;
  y?: number; sway?: number; haze?: number; bob?: number; front?: number; shadow?: number;
  additive?: number; flicker?: number; frames?: number; fps?: number; far?: number; sky?: number; wave?: number; billboard?: number;
}
export interface SceneFlat { tex: string; x: number; z: number; w: number; d: number; mirror?: number }
export interface SceneFloor { mirror?: number; tex: string; x0: number; x1: number; z0: number; z1: number; tw: number; td: number }
export interface SceneAnim { type: 'shaft' | 'fountain'; x: number; z: number; w?: number; h: number; a?: number; color?: number[]; phase?: number }
export interface SceneParticles { kind: string; count: number; color: number[]; size: number }
export interface SceneJson {
  id: string; name: string; bg: number[]; len: [number, number];
  floor: SceneFloor[]; flats: SceneFlat[]; back: SceneProp[]; props: SceneProp[]; anim: SceneAnim[]; particles: SceneParticles[];
  water: null | { x0: number; x1: number; z0: number; z1: number; shore: number; deep: number[]; mid: number[]; shallow: number[]; foam: number[] };
  ambient: { color: number[]; strength: number };
  grade: { sat: number; contrast: number; warm: number; vignette: number; fog: number[]; fogNear: number; fogFar: number };
  walk: { x0: number; x1: number; z0: number; z1: number };
  /** Vị trí trụ teleport (chỉ ở map trung tâm như Quảng Trường). */
  pillar?: { x: number; z: number };
}

export interface Tier {
  name: 'low' | 'medium' | 'high';
  sway: boolean; shafts: boolean; particles: number; shadows: boolean; water: boolean; post: boolean; bloom: boolean; tilt: number; pixelRatio: number; fogHaze: boolean;
}
export const TIERS: Record<Tier['name'], Tier> = {
  low: { name: 'low', sway: false, shafts: false, particles: 0.25, shadows: true, water: true, post: false, bloom: false, tilt: 0, pixelRatio: 1, fogHaze: false },
  medium: { name: 'medium', sway: true, shafts: true, particles: 0.6, shadows: true, water: true, post: true, bloom: false, tilt: 0.8, pixelRatio: 1.5, fogHaze: true },
  high: { name: 'high', sway: true, shafts: true, particles: 1, shadows: true, water: true, post: true, bloom: true, tilt: 1, pixelRatio: 2, fogHaze: true },
};

export interface SharedUniforms {
  uTime: THREE.IUniform<number>; uPitch: THREE.IUniform<number>; uCamX: THREE.IUniform<number>; uPx: THREE.IUniform<number>;
  uFogColor: THREE.IUniform<THREE.Color>; uFog: THREE.IUniform<THREE.Vector2>; uTint: THREE.IUniform<THREE.Color>;
}
export function makeShared(): SharedUniforms {
  return {
    uTime: { value: 0 }, uPitch: { value: (24 * Math.PI) / 180 }, uCamX: { value: 0 }, uPx: { value: 600 },
    uFogColor: { value: new THREE.Color(0.5, 0.6, 0.7) }, uFog: { value: new THREE.Vector2(12, 30) }, uTint: { value: new THREE.Color(1, 1, 1) },
  };
}
const srgb = (a: number[]): THREE.Color => new THREE.Color().setRGB(a[0] ?? 0, a[1] ?? 0, a[2] ?? 0, THREE.SRGBColorSpace);

let spriteGeo: THREE.BufferGeometry | null = null;
let flatGeo: THREE.BufferGeometry | null = null;
function baseSprite(): THREE.BufferGeometry {
  if (!spriteGeo) { spriteGeo = new THREE.PlaneGeometry(1, 1); spriteGeo.translate(0, 0.5, 0); }
  return spriteGeo;
}
function baseFlat(): THREE.BufferGeometry { return (flatGeo ??= new THREE.PlaneGeometry(1, 1)); }

function blobTexture(): THREE.Texture {
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d')!; const gr = g.createRadialGradient(32, 32, 2, 32, 32, 30);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.55, 'rgba(255,255,255,0.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  const t = new THREE.CanvasTexture(c); t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter; t.generateMipmaps = false; return t;
}

interface Inst { x: number; y: number; z: number; w: number; h: number; ph: number; flags: number; fl: number }
function instanced(base: THREE.BufferGeometry, list: Inst[], mat: THREE.Material): THREE.Mesh {
  const g = new THREE.InstancedBufferGeometry(); g.index = base.index; g.attributes.position = base.attributes.position!; g.attributes.uv = base.attributes.uv!; g.attributes.normal = base.attributes.normal!;
  const n = list.length; const pos = new Float32Array(n * 3), size = new Float32Array(n * 2), misc = new Float32Array(n * 3);
  list.forEach((p, i) => { pos.set([p.x, p.y, p.z], i * 3); size.set([p.w, p.h], i * 2); misc.set([p.ph, p.flags, p.fl], i * 3); });
  g.setAttribute('iPos', new THREE.InstancedBufferAttribute(pos, 3)); g.setAttribute('iSize', new THREE.InstancedBufferAttribute(size, 2)); g.setAttribute('iMisc', new THREE.InstancedBufferAttribute(misc, 3));
  g.instanceCount = n;
  const m = new THREE.Mesh(g, mat); m.frustumCulled = false; return m;
}

export class SceneRuntime {
  readonly group = new THREE.Group();
  readonly data: SceneJson;
  readonly tier: Tier;
  private readonly disposables: { dispose(): void }[] = [];
  private readonly particleMats: THREE.ShaderMaterial[] = [];
  private readonly timeMats: THREE.ShaderMaterial[] = [];
  readonly shafts: THREE.Mesh[] = [];
  drawables = 0;
  textureCount = 0;
  private waterMat: THREE.ShaderMaterial | null = null;

  private constructor(data: SceneJson, readonly U: SharedUniforms, tier: Tier) { this.data = data; this.tier = tier; this.group.name = `scene:${data.id}`; }

  static async load(id: string, U: SharedUniforms, tier: Tier): Promise<SceneRuntime> {
    const data = await loadJson<SceneJson>(`scenes/${id}.json`);
    const rt = new SceneRuntime(data, U, tier);
    await rt.build();
    return rt;
  }

  /** Khung nghệ thuật của cảnh: đỉnh cao nhất của vật dựng đứng và mép dưới còn có nội dung (để camera lấp đầy vùng nhìn). */
  frameInfo(): { topY: number; topZ: number; botZ: number; midZ: number } {
    const w = this.data.walk; let topY = 0, topZ = w.z0;
    for (const p of [...this.data.props, ...this.data.back]) { const t = (p as { y?: number }).y ?? 0; const h = t + p.h; if (p.z <= w.z1 && h > topY) { topY = h; topZ = p.z; } }
    return { topY: Math.min(topY, 4.2), topZ, botZ: w.z1 + 1.15, midZ: (w.z0 + w.z1) / 2 };
  }

  /** Lưới server (gx,gy) -> tọa độ thế giới trong vùng đi được. */
  gridToWorld(gx: number, gy: number, gw: number, gh: number): { x: number; z: number } {
    const w = this.data.walk;
    return { x: w.x0 + (gx / Math.max(gw - 1, 1)) * (w.x1 - w.x0), z: w.z0 + (gy / Math.max(gh - 1, 1)) * (w.z1 - w.z0) };
  }

  private async build(): Promise<void> {
    const d = this.data; const U = this.U;
    const texCache = new Map<string, THREE.Texture>();
    const need = new Set<string>();
    for (const f of d.floor) need.add(`f:${f.tex}`);
    for (const p of [...d.props, ...d.back, ...d.flats]) need.add(`s:${p.tex}`);
    await Promise.all([...need].map(async (k) => {
      const [kind, name] = [k.slice(0, 1), k.slice(2)];
      const mir = kind === 'f' && d.floor.some((f) => f.tex === name && f.mirror);
      const t = await loadTexture(`scenes/tex/${name}`, kind === 'f' ? { repeat: true, mip: true, aniso: 8, premult: false } : { mip: true });
      if (mir) { t.wrapS = t.wrapT = THREE.MirroredRepeatWrapping; }
      texCache.set(k, t);
    }));
    this.textureCount = texCache.size;
    const tx = (kind: 'f' | 's', name: string): THREE.Texture => texCache.get(`${kind}:${name}`)!;

    // ---- sàn
    for (const f of d.floor) {
      const mat = new THREE.ShaderMaterial({
        vertexShader: SH.FLOOR_VERT, fragmentShader: SH.FLOOR_FRAG, depthWrite: true, side: THREE.DoubleSide,
        uniforms: { map: { value: tx('f', f.tex) }, uRect: { value: new THREE.Vector4(f.x0, f.z0, f.x1, f.z1 + 9) }, uTile: { value: new THREE.Vector2(f.tw, f.td) }, uTime: U.uTime, uVar: { value: 0.12 }, uFogColor: U.uFogColor, uFog: U.uFog, uTint: U.uTint },
      });
      const m = new THREE.Mesh(baseFlat(), mat); m.frustumCulled = false; m.renderOrder = -10; this.group.add(m); this.disposables.push(mat); this.drawables++;
    }
    // ---- nước
    if (d.water) {
      const w = d.water;
      const mat = new THREE.ShaderMaterial({
        vertexShader: SH.WATER_VERT, fragmentShader: SH.WATER_FRAG, transparent: true, depthWrite: false, side: THREE.DoubleSide,
        uniforms: { uRect: { value: new THREE.Vector4(w.x0, w.z0, w.x1, w.z1 + 1.2) }, uTime: U.uTime, uShore: { value: w.shore }, uDeep: { value: srgb(w.deep) }, uMid: { value: srgb(w.mid) }, uShallow: { value: srgb(w.shallow) }, uFoam: { value: srgb(w.foam) }, uFar: { value: w.z0 }, uFogColor: U.uFogColor, uFog: U.uFog, uTint: U.uTint },
      });
      const m = new THREE.Mesh(baseFlat(), mat); m.frustumCulled = false; m.renderOrder = -9; m.visible = this.tier.water; this.group.add(m); this.disposables.push(mat); this.drawables++; this.waterMat = mat;
    }
    // ---- decal trên sàn
    const flatGroups = new Map<string, SceneFlat[]>();
    for (const f of d.flats) { (flatGroups.get(f.tex) ?? flatGroups.set(f.tex, []).get(f.tex)!).push(f); }
    for (const [name, list] of flatGroups) {
      const mat = new THREE.ShaderMaterial({ vertexShader: SH.FLAT_VERT, fragmentShader: SH.FLAT_FRAG, transparent: true, depthWrite: false, depthTest: true, side: THREE.DoubleSide, premultipliedAlpha: true, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor, uniforms: { map: { value: tx('s', name) }, uFogColor: U.uFogColor, uFog: U.uFog, uTint: U.uTint } });
      const m = instanced(baseFlat(), list.map((f) => ({ x: f.x, y: 0, z: f.z, w: f.w, h: f.d, ph: 0, flags: f.mirror ? 4 : 0, fl: 0 })), mat); m.renderOrder = -8; this.group.add(m); this.disposables.push(mat); this.drawables++;
    }
    // ---- bóng
    if (this.tier.shadows) {
      const sh: Inst[] = [];
      for (const p of d.props) {
        if (p.shadow === 0 || p.additive || p.haze || p.w > 9 || p.h > 7.5 || (p.y ?? 0) > 0.01) continue;
        if (p.h < 0.3) continue;
        const ww = Math.min(p.w, 3.2) * 0.85;
        sh.push({ x: p.x, y: 0, z: p.z + 0.04, w: ww, h: Math.max(0.28, ww * 0.34), ph: 0, flags: 0, fl: 0 });
      }
      if (sh.length) {
        const bt = blobTexture(); this.disposables.push(bt);
        const mat = new THREE.ShaderMaterial({ vertexShader: SH.SHADOW_VERT, fragmentShader: SH.SHADOW_FRAG, transparent: true, depthWrite: false, side: THREE.DoubleSide, uniforms: { map: { value: bt }, uAlpha: { value: 0.34 } } });
        const m = instanced(baseFlat(), sh, mat); m.renderOrder = -7; this.group.add(m); this.disposables.push(mat); this.drawables++;
      }
    }
    // ---- sprite đứng (nền xa + vật thể)
    const groups = new Map<string, { tex: string; frames: number; fps: number; add: boolean; list: Inst[] }>();
    const push = (p: SceneProp, inst: Inst): void => {
      const key = `${p.tex}|${p.frames ?? 1}|${p.fps ?? 0}|${p.additive ? 1 : 0}`;
      let g = groups.get(key);
      if (!g) groups.set(key, (g = { tex: p.tex, frames: p.frames ?? 1, fps: p.fps ?? 0, add: !!p.additive, list: [] }));
      g.list.push(inst);
    };
    const flagsOf = (p: SceneProp): number => (this.tier.sway && p.sway ? 1 : 0) | (this.tier.fogHaze && p.haze ? 2 : 0) | (p.bob ? 8 : 0);
    // nền xa: trời tựa lát ngang, đồi/tường xa dịch lùi và phóng to bù phối cảnh
    const skies = d.back.filter((b) => b.sky);
    if (skies.length) {
      const dz = 9; const s = 1 + dz / 18; let x = d.len[0] - 14; let i = 0; const x1 = d.len[1] + 14;
      while (x < x1) { const b = skies[i % skies.length]!; const w = b.w * s; push(b, { x: x + w / 2, y: -4.2, z: Math.min(...skies.map((q) => q.z)) - dz, w, h: b.h * s, ph: 0, flags: 0, fl: 0 }); x += w - 0.02; i++; }
    }
    for (const b of d.back) {
      if (b.sky) continue;
      const dz = b.far ? 5 : 0; const s = 1 + dz / 18;
      push(b, { x: b.x, y: 0, z: b.z - dz, w: b.w * s, h: b.h * s, ph: b.x * 1.3, flags: b.wave ? 8 : 0, fl: 0 });
    }
    for (const p of d.props) {
      push(p, { x: p.x, y: (p.y ?? 0) - (p.additive ? p.h / 2 : 0), z: p.z, w: p.w, h: p.h, ph: Math.abs(p.x * 1.7 + p.z * 0.9) % 6.28, flags: flagsOf(p), fl: p.flicker ?? 0 });
    }
    for (const g of groups.values()) {
      const mat = new THREE.ShaderMaterial({
        vertexShader: SH.SPRITE_VERT, fragmentShader: SH.SPRITE_FRAG, transparent: g.add, depthWrite: !g.add, blending: g.add ? THREE.AdditiveBlending : THREE.NormalBlending, premultipliedAlpha: g.add,
        uniforms: { map: { value: tx('s', g.tex) }, uTime: U.uTime, uPitch: U.uPitch, uFrames: { value: g.frames }, uFps: { value: g.fps }, uAdditive: { value: g.add ? 1 : 0 }, uAlphaCut: { value: 0.5 }, uFogColor: U.uFogColor, uFog: U.uFog, uTint: U.uTint },
      });
      const m = instanced(baseSprite(), g.list, mat); m.renderOrder = g.add ? 5 : 0; this.group.add(m); this.disposables.push(mat); this.drawables++;
    }
    // ---- cột nắng
    if (this.tier.shafts) {
      const sf = d.anim.filter((a) => a.type === 'shaft');
      if (sf.length) {
        const mat = new THREE.ShaderMaterial({ vertexShader: SH.SHAFT_VERT, fragmentShader: SH.SHAFT_FRAG, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, uniforms: { uTime: U.uTime, uPitch: U.uPitch, uColor: { value: srgb(sf[0]!.color ?? [1, 1, 0.8]) }, uAlpha: { value: 0.7 } } });
        const m = instanced(baseSprite(), sf.map((a) => ({ x: a.x, y: 0, z: a.z, w: a.w ?? 2, h: a.h, ph: a.phase ?? 0, flags: 0, fl: 0 })), mat); m.renderOrder = 6;
        // độ đậm theo từng cột: nhân vào uAlpha trung bình
        mat.uniforms.uAlpha!.value = (sf.reduce((s, a) => s + (a.a ?? 0.1), 0) / sf.length) * 6.5;
        this.group.add(m); this.disposables.push(mat); this.shafts.push(m); this.drawables++;
      }
    }
    // ---- hạt
    const area = new THREE.Vector4(d.len[0], d.walk.z0 - 3.5, d.len[1], d.walk.z1 + 2.5);
    const addParticles = (kind: number, count: number, color: number[], size: number, origin?: THREE.Vector3): void => {
      const n = Math.max(0, Math.round(count)); if (!n) return;
      const g = new THREE.BufferGeometry(); const seed = new Float32Array(n * 4); const pos = new Float32Array(n * 3);
      let r = 12345 + kind * 77; const rnd = (): number => { r = (r * 1664525 + 1013904223) >>> 0; return r / 4294967296; };
      for (let i = 0; i < n; i++) seed.set([rnd(), rnd(), rnd(), rnd()], i * 4);
      g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('aSeed', new THREE.BufferAttribute(seed, 4));
      const add = kind !== 1;
      const mat = new THREE.ShaderMaterial({
        vertexShader: SH.PARTICLE_VERT, fragmentShader: SH.PARTICLE_FRAG, transparent: true, depthWrite: false, blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: add ? THREE.OneFactor : THREE.OneMinusSrcAlphaFactor,
        uniforms: { uTime: U.uTime, uCamX: U.uCamX, uPx: U.uPx, uKind: { value: kind }, uArea: { value: area }, uSpan: { value: 30 }, uSize: { value: size }, uColor: { value: srgb(color) }, uOpacity: { value: kind === 1 ? 0.95 : 0.8 }, uOrigin: { value: origin ?? new THREE.Vector3() } },
      });
      const pts = new THREE.Points(g, mat); pts.frustumCulled = false; pts.renderOrder = 7; this.group.add(pts); this.disposables.push(g, mat); this.particleMats.push(mat); this.drawables++;
    };
    const kindOf: Record<string, number> = { pollen: 0, leaf: 1, petal: 1, dust: 2, ember: 3, spray: 4, butterfly: 5 };
    for (const p of d.particles) { const k = kindOf[p.kind]; if (k !== undefined) addParticles(k, p.count * this.tier.particles * (k === 5 ? 1.5 : 1), p.color, p.size * (k === 3 ? 1.4 : 1)); }
    if (this.tier.particles > 0) for (const a of d.anim) if (a.type === 'fountain') addParticles(6, 70 * Math.max(this.tier.particles, 0.4), [0.8, 0.93, 1], 0.1, new THREE.Vector3(a.x, 0.9, a.z));
  }

  update(time: number, camX: number): void {
    this.U.uTime.value = time; this.U.uCamX.value = camX;
    void this.waterMat;
  }

  dispose(): void {
    for (const d of this.disposables) d.dispose();
    this.group.clear();
  }
}

export function applyGrade(U: SharedUniforms, d: SceneJson): void {
  U.uFogColor.value.copy(srgb(d.grade.fog));
  U.uFog.value.set(d.grade.fogNear, d.grade.fogFar);
  const a = d.ambient; U.uTint.value.setRGB(a.color[0]! * a.strength, a.color[1]! * a.strength, a.color[2]! * a.strength);
}
export { srgb };
