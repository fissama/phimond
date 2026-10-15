import * as THREE from 'three';
import { SharedUniforms } from './sceneBuilder.ts';

const ACTOR_VERT = /* glsl */ `
uniform vec2 uSize; uniform float uPitch; uniform float uFlip; uniform vec2 uCell; uniform vec2 uGrid; uniform float uYOff; uniform float uBob;
varying vec2 vUv; varying float vDepth;
void main(){
  vec3 l = vec3(position.x * uSize.x, position.y * uSize.y + uYOff, 0.0);
  float cp = cos(uPitch), sp = sin(uPitch);
  vec3 w = vec3(l.x, l.y * cp + uBob, -l.y * sp);
  vec2 u = uv; if (uFlip > 0.5) u.x = 1.0 - u.x;
  vUv = (u + vec2(uCell.x, uGrid.y - 1.0 - uCell.y)) / uGrid;
  vec4 mv = viewMatrix * modelMatrix * vec4(w, 1.0); vDepth = -mv.z; gl_Position = projectionMatrix * mv;
}`;
const ACTOR_FRAG = /* glsl */ `
uniform sampler2D map; uniform float uOpacity; uniform vec3 uMul; uniform vec3 uAdd;
varying vec2 vUv; varying float vDepth;
uniform vec3 uFogColor; uniform vec2 uFog; uniform vec3 uTint;
void main(){
  vec4 t = texture2D(map, vUv);
  if (t.a < 0.5) discard;
  vec3 c = (t.rgb / t.a) * uMul * uTint + uAdd;
  float f = clamp((vDepth - uFog.x) / max(uFog.y - uFog.x, 0.001), 0.0, 1.0) * 0.6;
  c = mix(c, uFogColor, f);
  gl_FragColor = vec4(c, uOpacity);
  #include <colorspace_fragment>
}`;

let quad: THREE.BufferGeometry | null = null;
const getQuad = (): THREE.BufferGeometry => {
  if (!quad) { quad = new THREE.PlaneGeometry(1, 1); quad.translate(0, 0.5, 0); }
  return quad;
};
let blob: THREE.Texture | null = null;
function blobTex(): THREE.Texture {
  if (blob) return blob;
  const c = document.createElement('canvas'); c.width = c.height = 64;
  const g = c.getContext('2d')!; const gr = g.createRadialGradient(32, 32, 2, 32, 32, 30);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.6, 'rgba(255,255,255,0.5)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  blob = new THREE.CanvasTexture(c); blob.minFilter = THREE.LinearFilter; blob.generateMipmaps = false; return blob;
}
const SHADOW_V = /* glsl */ `uniform vec2 uS; varying vec2 vUv; void main(){ vUv = uv; vec4 mv = viewMatrix * modelMatrix * vec4(position.x * uS.x, 0.012, position.y * uS.y, 1.0); gl_Position = projectionMatrix * mv; }`;
const SHADOW_F = /* glsl */ `uniform sampler2D map; uniform float uA; varying vec2 vUv; void main(){ float a = texture2D(map, vUv).a * uA; gl_FragColor = vec4(0.02, 0.03, 0.06, a);\n#include <colorspace_fragment>\n}`;

export interface AtlasSpec {
  texture: THREE.Texture; cols: number; rows: number; cellPx: [number, number];
  /** đơn vị thế giới trên mỗi pixel nguồn */
  unitsPerPx: number; footPadPx: number; shadowW?: number;
}

/** Sprite hoạt họa lấy khung từ atlas, đứng nghiêng theo camera, có bóng dưới chân. */
export class AtlasSprite {
  readonly group = new THREE.Group();
  readonly mesh: THREE.Mesh;
  readonly shadow: THREE.Mesh;
  private readonly mat: THREE.ShaderMaterial;
  readonly bodyHeight: number;
  constructor(readonly spec: AtlasSpec, U: SharedUniforms, bodyPx: number) {
    const w = spec.cellPx[0] * spec.unitsPerPx, h = spec.cellPx[1] * spec.unitsPerPx;
    this.bodyHeight = bodyPx * spec.unitsPerPx;
    this.mat = new THREE.ShaderMaterial({
      vertexShader: ACTOR_VERT, fragmentShader: ACTOR_FRAG, transparent: true, depthWrite: true,
      uniforms: {
        map: { value: spec.texture }, uSize: { value: new THREE.Vector2(w, h) }, uPitch: U.uPitch, uFlip: { value: 0 }, uCell: { value: new THREE.Vector2(0, 0) }, uGrid: { value: new THREE.Vector2(spec.cols, spec.rows) },
        uYOff: { value: -spec.footPadPx * spec.unitsPerPx }, uBob: { value: 0 }, uOpacity: { value: 1 }, uMul: { value: new THREE.Color(1, 1, 1) }, uAdd: { value: new THREE.Color(0, 0, 0) },
        uFogColor: U.uFogColor, uFog: U.uFog, uTint: U.uTint,
      },
    });
    this.mesh = new THREE.Mesh(getQuad(), this.mat); this.mesh.frustumCulled = false; this.mesh.renderOrder = 2;
    const sw = (spec.shadowW ?? Math.min(w * 0.55, 1.6));
    const sm = new THREE.ShaderMaterial({ vertexShader: SHADOW_V, fragmentShader: SHADOW_F, transparent: true, depthWrite: false, side: THREE.DoubleSide, uniforms: { map: { value: blobTex() }, uS: { value: new THREE.Vector2(sw, sw * 0.38) }, uA: { value: 0.4 } } });
    this.shadow = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), sm); this.shadow.renderOrder = -6; this.shadow.frustumCulled = false;
    this.group.add(this.shadow, this.mesh);
  }
  setCell(col: number, row: number): void { (this.mat.uniforms.uCell!.value as THREE.Vector2).set(col, row); }
  setFlip(f: boolean): void { this.mat.uniforms.uFlip!.value = f ? 1 : 0; }
  setOpacity(a: number): void { this.mat.uniforms.uOpacity!.value = a; (this.shadow.material as THREE.ShaderMaterial).uniforms.uA!.value = 0.4 * a; }
  setMul(r: number, g: number, b: number): void { (this.mat.uniforms.uMul!.value as THREE.Color).setRGB(r, g, b); }
  setAdd(r: number, g: number, b: number): void { (this.mat.uniforms.uAdd!.value as THREE.Color).setRGB(r, g, b); }
  setBob(y: number): void { this.mat.uniforms.uBob!.value = y; }
  setPos(x: number, y: number, z: number): void { this.group.position.set(x, y, z); }
  dispose(): void { this.mat.dispose(); (this.shadow.material as THREE.Material).dispose(); this.shadow.geometry.dispose(); }
}

/** Dòng hoạt họa thuần: tính ô (col,row) từ thời gian. */
export interface AnimClip { row: number; frames: number; fps: number; loop: boolean }
export function clipFrame(c: AnimClip, t: number): number {
  const f = Math.floor(t * c.fps);
  return c.loop ? ((f % c.frames) + c.frames) % c.frames : Math.min(f, c.frames - 1);
}
