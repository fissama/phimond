import * as THREE from 'three';
import { hd2dUrl, textures } from './assets.ts';

/**
 * Bụi/cỏ dưới chân người chơi (GPT 2026-10-30, batch-15): dải 4 khung 64×64 phát một lần mỗi ~0,5 ô đi được.
 * Cỏ ở rừng, bụi ở thành phố/ngoài trời; không phát trong sảnh (sàn đá/gỗ) để không bay bụi trong nhà.
 */
const FRAMES = 4;
const LIFE = 0.42; // giây cho 4 khung
const STRIDE = 0.55; // đơn vị world giữa hai lần bước
const SIZE = 0.6; // cạnh sprite theo world

interface Puff {
  mesh: THREE.Mesh;
  tex: THREE.Texture;
  t: number;
  on: boolean;
}

export class Footsteps {
  private readonly puffs: Puff[] = [];
  private acc = 0;
  private next = 0;
  private flip = false;
  private constructor(private readonly root: THREE.Group) {}

  static async create(parent: THREE.Object3D, theme: string): Promise<Footsteps | null> {
    if (theme === 'hall') return null;
    const kind = theme === 'forest' || theme === 'deep_forest' ? 'grass' : 'dust';
    const base = await textures.get(hd2dUrl(`fx-footstep-${kind}`));
    const root = new THREE.Group();
    root.name = 'footsteps';
    const f = new Footsteps(root);
    const geo = new THREE.PlaneGeometry(SIZE, SIZE);
    geo.translate(0, SIZE / 2, 0);
    for (let i = 0; i < 6; i++) {
      const tex = base.clone();
      tex.repeat.set(1 / FRAMES, 1);
      tex.needsUpdate = true;
      const mat = new THREE.MeshBasicMaterial({ map: tex, alphaTest: 0.35, transparent: true, depthWrite: false });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.visible = false;
      mesh.rotation.x = -0.42;
      mesh.renderOrder = 3;
      root.add(mesh);
      f.puffs.push({ mesh, tex, t: 0, on: false });
    }
    parent.add(root);
    return f;
  }

  /** `d` = quãng đường vừa đi trong khung này (world). */
  travel(d: number, x: number, z: number, facingLeft: boolean): void {
    if (d <= 0.002) return;
    this.acc += d;
    if (this.acc < STRIDE) return;
    this.acc = 0;
    const p = this.puffs[this.next++ % this.puffs.length]!;
    this.flip = !this.flip;
    p.on = true;
    p.t = 0;
    p.mesh.visible = true;
    // Đặt lùi sau gót một chút (ngược hướng nhìn) để bụi nằm ở chân sau.
    p.mesh.position.set(x + (facingLeft ? 0.12 : -0.12) * (this.flip ? 1 : 0.6), 0.02, z + 0.05);
    p.mesh.scale.x = this.flip ? 1 : -1;
  }

  update(dt: number): void {
    for (const p of this.puffs) {
      if (!p.on) continue;
      p.t += dt;
      const f = Math.floor((p.t / LIFE) * FRAMES);
      if (f >= FRAMES) {
        p.on = false;
        p.mesh.visible = false;
        continue;
      }
      p.tex.offset.x = f / FRAMES;
    }
  }

  dispose(): void {
    for (const p of this.puffs) {
      p.tex.dispose();
      (p.mesh.material as THREE.Material).dispose();
    }
    this.puffs[0]?.mesh.geometry.dispose();
    this.root.parent?.remove(this.root);
  }
}
