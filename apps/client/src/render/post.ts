import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
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
  },
  vertexShader: `varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }`,
  fragmentShader: `
    uniform sampler2D tDiffuse; uniform vec2 res; uniform float blur; uniform vec3 tint; uniform float sat; uniform float bright; uniform float vig;
    varying vec2 vUv;
    void main(){
      // Tilt-shift: giữ nét dải giữa, mờ dần lên/xuống (lấy mẫu vòng 8 điểm).
      float d = abs(vUv.y - 0.5);
      float amt = smoothstep(0.2, 0.55, d) * blur;
      vec3 c = texture2D(tDiffuse, vUv).rgb;
      if (amt > 0.001) {
        float r = amt * 4.0 / res.y;
        vec3 s = c;
        for (int i = 0; i < 8; i++) {
          float a = float(i) * 0.7853982;
          vec2 o = vec2(cos(a) * r * res.y / res.x, sin(a) * r);
          s += texture2D(tDiffuse, vUv + o).rgb;
        }
        c = mix(c, s / 9.0, clamp(amt * 1.4, 0.0, 1.0));
      }
      float l = dot(c, vec3(0.299, 0.587, 0.114));
      c = mix(vec3(l), c, sat) * tint * bright;
      vec2 q = vUv - 0.5;
      c *= 1.0 - vig * smoothstep(0.25, 0.85, dot(q, q) * 2.2);
      gl_FragColor = vec4(c, 1.0);
    }`,
};

export class Post {
  private readonly composer: EffectComposer;
  private readonly bloom: UnrealBloomPass;
  private readonly grade: ShaderPass;
  private quality: Quality = 'high';

  constructor(renderer: THREE.WebGLRenderer, scene: THREE.Scene, camera: THREE.Camera) {
    this.composer = new EffectComposer(renderer);
    this.composer.addPass(new RenderPass(scene, camera));
    this.bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.35, 0.6, 0.82);
    this.composer.addPass(this.bloom);
    this.grade = new ShaderPass(GRADE);
    this.composer.addPass(this.grade);
    this.composer.addPass(new OutputPass());
  }

  setQuality(q: Quality): void {
    this.quality = q;
    this.bloom.enabled = q === 'high';
    this.grade.uniforms.blur!.value = q === 'high' ? 1 : 0.6;
  }

  setSize(w: number, h: number, pixelRatio: number): void {
    this.composer.setPixelRatio(pixelRatio);
    this.composer.setSize(w, h);
    this.grade.uniforms.res!.value.set(w * pixelRatio, h * pixelRatio);
    // Bloom ở nửa độ phân giải cho nhẹ.
    this.bloom.setSize(Math.max(64, Math.floor((w * pixelRatio) / 2)), Math.max(64, Math.floor((h * pixelRatio) / 2)));
  }

  setLight(l: Light): void {
    const u = this.grade.uniforms;
    (u.tint!.value as THREE.Vector3).set(l.tint[0], l.tint[1], l.tint[2]);
    u.sat!.value = l.sat;
    u.bright!.value = l.bright;
    // Ban đêm bloom mạnh hơn để đèn lồng tỏa sáng.
    this.bloom.strength = (this.quality === 'high' ? 0.3 : 0) + l.night * 0.35;
    this.bloom.threshold = 0.82 - l.night * 0.2;
  }

  render(dt: number): void {
    this.composer.render(dt);
  }

  dispose(): void {
    this.composer.dispose();
  }
}
