import * as THREE from 'three';
import type { Light } from './daylight.ts';

export interface Lamp {
  x: number;
  y: number;
  z: number;
  /** Cỡ quầng sáng (đơn vị world). */
  size?: number;
  color?: number;
}

export interface Atmosphere {
  update(dt: number): void;
  setLight(l: Light): void;
  dispose(): void;
}

let glowTex: THREE.Texture | null = null;
function glowTexture(): THREE.Texture {
  if (glowTex) return glowTex;
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const g = c.getContext('2d')!;
  const r = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  r.addColorStop(0, 'rgba(255,255,255,1)');
  r.addColorStop(0.25, 'rgba(255,255,255,0.55)');
  r.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = r;
  g.fillRect(0, 0, 64, 64);
  glowTex = new THREE.CanvasTexture(c);
  return glowTex;
}

let shaftTex: THREE.Texture | null = null;
function shaftTexture(): THREE.Texture {
  if (shaftTex) return shaftTex;
  const c = document.createElement('canvas');
  c.width = 32;
  c.height = 128;
  const g = c.getContext('2d')!;
  const h = g.createLinearGradient(0, 0, 32, 0);
  h.addColorStop(0, 'rgba(255,255,255,0)');
  h.addColorStop(0.5, 'rgba(255,255,255,1)');
  h.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = h;
  g.fillRect(0, 0, 32, 128);
  // mờ dần xuống dưới
  g.globalCompositeOperation = 'destination-in';
  const v = g.createLinearGradient(0, 0, 0, 128);
  v.addColorStop(0, 'rgba(0,0,0,1)');
  v.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = v;
  g.fillRect(0, 0, 32, 128);
  shaftTex = new THREE.CanvasTexture(c);
  return shaftTex;
}

/**
 * Không khí của map: quầng sáng đèn/đuốc (đêm và trong nhà), tia nắng xuyên tán lá (ban ngày) và hạt bụi/phấn hoa trôi.
 * Mọi thứ là sprite cộng sáng (additive), chỉ bật khi mức đồ họa cho phép hiệu ứng (`fx`).
 */
export function makeAtmosphere(
  group: THREE.Group,
  o: { theme: string; W: number; H: number; lamps: Lamp[]; shafts: boolean; motes: number },
): Atmosphere {
  const glows: { s: THREE.Sprite; base: number; seed: number }[] = [];
  const disposables: { dispose(): void }[] = [];
  const add = (obj: THREE.Object3D) => group.add(obj);
  const indoor = o.theme === 'hall';

  for (const [i, l] of o.lamps.entries()) {
    const mat = new THREE.SpriteMaterial({ map: glowTexture(), color: l.color ?? 0xffb060, transparent: true, depthWrite: false, depthTest: false, blending: THREE.AdditiveBlending, opacity: 0 });
    const s = new THREE.Sprite(mat);
    s.position.set(l.x, l.y, l.z);
    const sz = l.size ?? 2.2;
    s.scale.set(sz, sz, 1);
    s.renderOrder = 50;
    add(s);
    disposables.push(mat);
    glows.push({ s, base: sz, seed: i * 1.7 });
  }

  const shaftMeshes: { m: THREE.Mesh; phase: number }[] = [];
  if (o.shafts) {
    const n = Math.max(3, Math.round(o.W / 9));
    for (let i = 0; i < n; i++) {
      const mat = new THREE.MeshBasicMaterial({ map: shaftTexture(), color: 0xfff0c0, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0, side: THREE.DoubleSide });
      const geo = new THREE.PlaneGeometry(2.4 + (i % 3) * 0.6, 9);
      const m = new THREE.Mesh(geo, mat);
      m.position.set(((i + 0.5) / n) * o.W + ((i % 2) - 0.5) * 2, 4.2, Math.min(o.H - 2, 3 + (i % 3) * 2));
      m.rotation.set(-0.42, 0, 0.45);
      m.renderOrder = 40;
      add(m);
      disposables.push(mat, geo);
      shaftMeshes.push({ m, phase: i * 2.1 });
    }
  }

  let motes: THREE.Points | null = null;
  let moteMat: THREE.PointsMaterial | null = null;
  const base: Float32Array = new Float32Array(o.motes * 3);
  if (o.motes > 0) {
    const pos = new Float32Array(o.motes * 3);
    for (let i = 0; i < o.motes; i++) {
      base[i * 3] = Math.random() * o.W;
      base[i * 3 + 1] = 0.4 + Math.random() * 3;
      base[i * 3 + 2] = Math.random() * o.H;
    }
    pos.set(base);
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    moteMat = new THREE.PointsMaterial({ map: glowTexture(), color: indoor ? 0xffd9a0 : 0xfff4c8, size: 0.28, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.0 });
    motes = new THREE.Points(geo, moteMat);
    motes.frustumCulled = false;
    motes.renderOrder = 45;
    add(motes);
    disposables.push(geo, moteMat);
  }

  let t = 0;
  let L: Light = { tint: [1, 1, 1], sat: 1, bright: 1, contrast: 1, shade: [0, 0, 0], hi: [0, 0, 0], night: 0, day: 1 };
  return {
    update(dt) {
      t += dt;
      // Đèn: sáng theo đêm (trong nhà luôn sáng), nhấp nháy nhẹ.
      const lit = indoor ? 0.85 : L.night;
      for (const g of glows) {
        const f = 0.88 + 0.12 * Math.sin(t * 7 + g.seed) * Math.sin(t * 3.1 + g.seed * 2);
        (g.s.material as THREE.SpriteMaterial).opacity = Math.min(1, lit * 0.85 * f);
        const k = g.base * (0.96 + 0.06 * f);
        g.s.scale.set(k, k, 1);
      }
      for (const s of shaftMeshes) (s.m.material as THREE.MeshBasicMaterial).opacity = Math.max(0, L.day * (0.2 + 0.08 * Math.sin(t * 0.5 + s.phase)));
      if (motes && moteMat) {
        moteMat.opacity = indoor ? 0.55 : 0.2 + L.day * 0.25 + L.night * 0.15;
        const p = motes.geometry.getAttribute('position') as THREE.BufferAttribute;
        for (let i = 0; i < o.motes; i++) {
          p.setXYZ(
            i,
            base[i * 3]! + Math.sin(t * 0.3 + i) * 0.6,
            base[i * 3 + 1]! + Math.sin(t * 0.45 + i * 1.3) * 0.35 + ((t * 0.05 * ((i % 5) + 1)) % 1) * 0.5,
            base[i * 3 + 2]! + Math.cos(t * 0.25 + i * 0.7) * 0.6,
          );
        }
        p.needsUpdate = true;
      }
    },
    setLight(l) {
      L = l;
    },
    dispose() {
      disposables.forEach((d) => d.dispose());
    },
  };
}
