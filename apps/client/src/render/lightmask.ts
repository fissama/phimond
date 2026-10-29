import * as THREE from 'three';
import type { Light } from './daylight.ts';
import type { Lamp } from './atmosphere.ts';

/**
 * Tương phản sáng/tối kiểu HD-2D: một lớp NHÂN màu phủ mặt đất — nền hơi tối ngả xanh tím, chỗ có nắng/đèn sáng trắng ấm —
 * nên sprite đứng trên (không bị nhân) nổi hẳn lên, và cảnh có vệt sáng/vệt bóng thay vì phẳng đều.
 * Thêm quầng sáng ấm mờ dưới chân người chơi. Tất cả tĩnh/rẻ: một texture nhỏ + một mặt phẳng.
 */
const PPU = 14;

export interface LightMaskOpts {
  theme: string;
  W: number;
  H: number;
  lamps: Lamp[];
  seed: number;
}

interface Style {
  base: [number, number, number]; // màu vùng bóng (nhân)
  dapple: number; // mật độ vệt nắng (blob/ô)
  rMin: number;
  rMax: number;
  warm: [number, number, number];
}
const STYLES: Record<string, Style> = {
  hall: { base: [0.9, 0.9, 0.96], dapple: 0.03, rMin: 1.2, rMax: 2.4, warm: [1, 0.97, 0.88] },
  city: { base: [0.74, 0.77, 0.89], dapple: 0.07, rMin: 1.8, rMax: 3.8, warm: [1, 0.97, 0.86] },
  forest: { base: [0.64, 0.74, 0.74], dapple: 0.17, rMin: 0.9, rMax: 2.2, warm: [1, 0.98, 0.8] },
  deep_forest: { base: [0.6, 0.68, 0.78], dapple: 0.15, rMin: 0.9, rMax: 2.1, warm: [0.9, 1, 0.9] },
};

function rng(seed: number) {
  let s = seed >>> 0 || 1;
  return () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296);
}

export interface LightMask {
  update(playerX: number, playerZ: number): void;
  setLight(l: Light): void;
  dispose(): void;
}

export function makeLightMask(group: THREE.Group, o: LightMaskOpts): LightMask {
  const st = STYLES[o.theme] ?? STYLES.forest!;
  const cw = Math.max(16, Math.ceil(o.W * PPU));
  const ch = Math.max(16, Math.ceil(o.H * PPU));
  const c = document.createElement('canvas');
  c.width = cw;
  c.height = ch;
  const g = c.getContext('2d')!;
  const rgb = (v: number[]) => `rgb(${Math.round(v[0]! * 255)},${Math.round(v[1]! * 255)},${Math.round(v[2]! * 255)})`;
  g.fillStyle = rgb(st.base);
  g.fillRect(0, 0, cw, ch);
  const pool = (x: number, z: number, r: number, a: number) => {
    const px = x * PPU;
    const py = z * PPU;
    const rr = r * PPU;
    const gr = g.createRadialGradient(px, py, 0, px, py, rr);
    const w = rgb(st.warm).slice(4, -1);
    gr.addColorStop(0, `rgba(${w},${a})`);
    gr.addColorStop(0.55, `rgba(${w},${a * 0.6})`);
    gr.addColorStop(1, `rgba(${w},0)`);
    g.fillStyle = gr;
    g.fillRect(px - rr, py - rr, rr * 2, rr * 2);
  };
  const rand = rng(o.seed);
  const n = Math.round(o.W * o.H * st.dapple);
  for (let i = 0; i < n; i++) {
    const r = st.rMin + rand() * (st.rMax - st.rMin);
    pool(rand() * o.W, rand() * o.H, r, 0.55 + rand() * 0.4);
  }
  for (const l of o.lamps) pool(l.x, l.z, (l.size ?? 2) * 1.1, 0.9);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = THREE.LinearFilter;
  tex.generateMipmaps = false;
  const mat = new THREE.MeshBasicMaterial({ map: tex, blending: THREE.MultiplyBlending, premultipliedAlpha: true, depthWrite: false, transparent: true, fog: false });
  const geo = new THREE.PlaneGeometry(o.W, o.H);
  const m = new THREE.Mesh(geo, mat);
  m.rotation.x = -Math.PI / 2;
  m.position.set(o.W / 2, 0.035, o.H / 2);
  m.renderOrder = 2;
  group.add(m);

  // Quầng ấm dưới chân người chơi (cộng sáng).
  const gc = document.createElement('canvas');
  gc.width = gc.height = 64;
  const gg = gc.getContext('2d')!;
  const rg = gg.createRadialGradient(32, 32, 0, 32, 32, 32);
  rg.addColorStop(0, 'rgba(255,230,170,0.5)');
  rg.addColorStop(0.5, 'rgba(255,230,170,0.14)');
  rg.addColorStop(1, 'rgba(255,236,190,0)');
  gg.fillStyle = rg;
  gg.fillRect(0, 0, 64, 64);
  const gtex = new THREE.CanvasTexture(gc);
  const gmat = new THREE.MeshBasicMaterial({ map: gtex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, opacity: 0.3, fog: false });
  const halo = new THREE.Mesh(new THREE.PlaneGeometry(5.5, 5.5), gmat);
  halo.rotation.x = -Math.PI / 2;
  halo.renderOrder = 3;
  group.add(halo);

  return {
    update(px, pz) {
      halo.position.set(px, 0.04, pz);
    },
    setLight(l) {
      // Ban đêm lớp nhân tối thêm (trừ chỗ đèn đã có quầng cộng sáng); quầng chân người rõ hơn khi tối.
      const k = 1 - l.night * 0.35;
      mat.color.setRGB(k, k, k + l.night * 0.05);
      gmat.opacity = 0.28 + l.night * 0.3;
    },
    dispose() {
      tex.dispose();
      gtex.dispose();
      mat.dispose();
      gmat.dispose();
      geo.dispose();
      halo.geometry.dispose();
    },
  };
}
