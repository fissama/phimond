import * as THREE from 'three';
import type { MapDef } from '@phimond/protocol';
import { Grid } from '../world/grid.ts';
import { findPath } from '../world/path.ts';
import { walkSpeed } from '../world/smooth.ts';
import { asset } from './assets.ts';
import { blobShadow, CharacterSprite, propSprite, animate } from './sprites.ts';

/**
 * Sự sống trong thành (đơn 10): người đi đường, bồ câu, mèo, chó, bướm, quạ.
 * Chỉ để nhìn — không có trên server, không chặn người chơi. Nhà/tường đứng yên.
 */
export interface Ambient {
  update(dt: number, player: THREE.Vector3 | null): void;
}

type Rand = () => number;
const rng = (seed: number): Rand => {
  let s = seed >>> 0 || 1;
  return () => {
    s ^= s << 13;
    s ^= s >>> 17;
    s ^= s << 5;
    return (s >>> 0) / 4294967296;
  };
};

const WALKERS: Record<string, string[]> = {
  city_square: ['walker-baker', 'walker-elder', 'walker-boy', 'walker-girl', 'walker-traveller'],
  city_palace_gate: ['walker-guard', 'walker-traveller'],
};

/** Ô đi được ở vùng giữa (tránh hàng sát mặt tiền và mép dưới). */
function openCells(grid: Grid, map: MapDef): { x: number; y: number }[] {
  const out: { x: number; y: number }[] = [];
  for (let y = 3; y < grid.h - 1; y++) for (let x = 1; x < grid.w - 1; x++) if (grid.walkable(x, y)) out.push({ x, y });
  void map;
  return out;
}

class Walker {
  private path: { x: number; y: number }[] = [];
  private wait: number;
  private pos: THREE.Vector2;
  private t = 0;
  private vel = 0;
  constructor(
    readonly sprite: CharacterSprite,
    readonly root: THREE.Group,
    private readonly grid: Grid,
    private readonly cells: { x: number; y: number }[],
    private readonly r: Rand,
    start: { x: number; y: number },
    private readonly speed: number,
  ) {
    this.pos = new THREE.Vector2(start.x + 0.5, start.y + 0.5);
    this.wait = 1 + r() * 4;
    this.root.position.set(this.pos.x, 0, this.pos.y);
  }

  update(dt: number): void {
    this.t += dt;
    if (this.path.length === 0) {
      this.wait -= dt;
      this.vel = 0;
      this.sprite.setMotion(false);
      if (this.wait <= 0) this.pick();
    } else {
      const next = this.path[0]!;
      const tx = next.x + 0.5;
      const ty = next.y + 0.5;
      const dx = tx - this.pos.x;
      const dy = ty - this.pos.y;
      const d = Math.hypot(dx, dy);
      // Tăng/giảm tốc dần (đi tiếp qua góc thì giữ đà): không phóng đi hết tốc rồi khựng lại.
      this.vel = walkSpeed(this.vel, this.speed, d + this.path.length - 1, dt);
      const step = this.vel * dt;
      if (d <= step) {
        this.pos.set(tx, ty);
        this.path.shift();
        if (this.path.length === 0) this.wait = 2 + this.r() * 5;
      } else {
        this.pos.x += (dx / d) * step;
        this.pos.y += (dy / d) * step;
      }
      this.sprite.travel(Math.min(d, step));
      const vert = Math.abs(dy) > Math.abs(dx);
      this.sprite.setMotion(true, !vert && Math.abs(dx) > 0.01 ? dx < 0 : undefined, vert ? (dy > 0 ? 'down' : 'up') : null); // có dải dọc thì dùng, thiếu thì rơi về dải ngang
    }
    this.root.position.set(this.pos.x, 0, this.pos.y);
    this.sprite.update(dt);
  }

  private pick(): void {
    const from = { x: Math.floor(this.pos.x), y: Math.floor(this.pos.y) };
    for (let i = 0; i < 6; i++) {
      const goal = this.cells[Math.floor(this.r() * this.cells.length)]!;
      if (Math.abs(goal.x - from.x) + Math.abs(goal.y - from.y) < 4) continue;
      const p = findPath(this.grid, from, [goal], 2500);
      if (p && p.length > 0) {
        this.path = p.slice(0, 14);
        return;
      }
    }
    this.wait = 2;
  }
}

/** Đàn bồ câu: mổ thóc; người chơi lại gần thì bay lên rồi quay lại sau một lúc. */
class Pigeons {
  private birds: { peck: THREE.Mesh; fly: THREE.Mesh; home: THREE.Vector3; vx: number }[] = [];
  private state: 'ground' | 'fly' | 'gone' = 'ground';
  private timer = 0;
  constructor(
    readonly group: THREE.Group,
    private readonly at: THREE.Vector3,
  ) {}

  async init(r: Rand, n: number): Promise<void> {
    for (let i = 0; i < n; i++) {
      const peck = await propSprite('animal-pigeon-peck');
      const fly = await propSprite('animal-pigeon-fly');
      if (!peck || !fly) return;
      const home = new THREE.Vector3(this.at.x + (r() - 0.5) * 1.4, 0, this.at.z + (r() - 0.5) * 0.8);
      peck.position.copy(home);
      if (r() < 0.5) peck.scale.x = -1;
      (peck.userData.anim as { fps: number }).fps = 1.5 + r() * 2;
      fly.visible = false;
      this.group.add(peck, fly);
      this.birds.push({ peck, fly, home, vx: r() < 0.5 ? -1 : 1 });
    }
  }

  update(dt: number, player: THREE.Vector3 | null): void {
    for (const b of this.birds) {
      animate(b.peck, dt);
      animate(b.fly, dt);
    }
    if (this.state === 'ground') {
      if (player && Math.hypot(player.x - this.at.x, player.z - this.at.z) < 1.8) {
        this.state = 'fly';
        this.timer = 0;
        for (const b of this.birds) {
          b.peck.visible = false;
          b.fly.visible = true;
          b.fly.position.copy(b.home);
          b.fly.scale.x = b.vx < 0 ? 1 : -1;
        }
      }
    } else if (this.state === 'fly') {
      this.timer += dt;
      for (const b of this.birds) {
        b.fly.position.x += b.vx * dt * 2.2;
        b.fly.position.y += dt * 1.6;
        b.fly.position.z -= dt * 0.8;
      }
      if (this.timer > 2.5) {
        this.state = 'gone';
        this.timer = 0;
        for (const b of this.birds) b.fly.visible = false;
      }
    } else {
      this.timer += dt;
      const far = !player || Math.hypot(player.x - this.at.x, player.z - this.at.z) > 4;
      if (this.timer > 10 && far) {
        this.state = 'ground';
        for (const b of this.birds) b.peck.visible = true;
      }
    }
  }
}

export async function spawnAmbient(map: MapDef, group: THREE.Group, blob: boolean, density: number): Promise<Ambient[]> {
  const out: Ambient[] = [];
  if (map.theme !== 'city' || !map.walk) return out;
  let grid: Grid;
  try {
    grid = Grid.parse(map.walk, map.width, map.height || map.width);
  } catch {
    return out;
  }
  const r = rng(map.id.length * 7919 + map.width * 31);
  const cells = openCells(grid, map);
  if (cells.length === 0) return out;

  // Người đi đường.
  const names = (WALKERS[map.id] ?? []).filter((id) => asset(id));
  const count = Math.max(1, Math.round(names.length * Math.min(1, density + 0.2)));
  for (let i = 0; i < count; i++) {
    const id = names[i]!;
    const sprite = await CharacterSprite.create(id);
    sprite.framesPerCell = 3.2; // dải 2 khung: một chu kỳ ≈ 0.6 ô
    sprite.bobAmp = 0.035;
    const root = new THREE.Group();
    root.add(sprite.root);
    if (blob) root.add(blobShadow(0.32));
    group.add(root);
    const start = cells[Math.floor(r() * cells.length)]!;
    const w = new Walker(sprite, root, grid, cells, r, start, id === 'walker-elder' ? 0.8 : id === 'walker-guard' ? 1.1 : 1.3);
    out.push({ update: (dt) => w.update(dt) });
  }

  // Bồ câu ở quảng trường.
  if (asset('animal-pigeon-peck')) {
    const spots = map.id === 'city_square' ? [new THREE.Vector3(21.5, 0, 5.4), new THREE.Vector3(9.5, 0, 5.4)] : [new THREE.Vector3(7, 0, 7.4)];
    for (const at of spots) {
      const p = new Pigeons(group, at);
      await p.init(r, 3);
      out.push(p);
    }
  }

  // Mèo ngồi cạnh mặt tiền, chó nằm cạnh giếng/xe, quạ trên viền vườn, bướm quanh hoa.
  const still = async (id: string, x: number, z: number, flip = false) => {
    const s = await propSprite(id);
    if (!s) return null;
    s.position.set(x, 0, z);
    if (flip) s.scale.x = -1;
    group.add(s);
    return s;
  };
  if (map.id === 'city_square') {
    const cat = await still('animal-cat', 2.6, 2.35);
    if (cat) out.push({ update: (dt) => animate(cat, dt) });
    const dog = await still('animal-dog', 2.2, 8.1, true);
    if (dog) {
      let t = 0;
      out.push({ update: (dt) => { t += dt; dog.scale.y = 1 + Math.sin(t * 2.2) * 0.025; } });
    }
    const crow = await still('animal-crow', 30.2, 10.6, true);
    if (crow) {
      let t = 0;
      out.push({
        update: (dt) => {
          t += dt;
          const hop = (t % 7) > 6.6 ? Math.sin(((t % 7) - 6.6) / 0.4 * Math.PI) * 0.08 : 0;
          crow.position.y = hop;
        },
      });
    }
  }
  if (map.id === 'city_palace_gate') {
    const cat = await still('animal-cat', 23.3, 2.4, true);
    if (cat) out.push({ update: (dt) => animate(cat, dt) });
  }
  if (asset('animal-butterflies')) {
    const spots = map.id === 'city_square' ? [[1.5, 9.4], [30.5, 9.4], [12.6, 2.6]] : [[3.5, 9.3], [21.5, 9.3]];
    for (const [x, z] of spots) {
      const b = await still('animal-butterflies', x!, z!);
      if (!b) continue;
      const ph = r() * 10;
      let t = 0;
      out.push({
        update: (dt) => {
          t += dt;
          b.position.set(x! + Math.sin(t * 0.6 + ph) * 0.7, 0.55 + Math.sin(t * 1.3 + ph) * 0.18, z! + Math.cos(t * 0.5 + ph) * 0.3);
          b.scale.x = 0.55 + Math.abs(Math.sin(t * 9 + ph)) * 0.45; // vỗ cánh
        },
      });
    }
  }
  return out;
}
