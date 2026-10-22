import { tn } from '../i18n';
import * as THREE from 'three';
import type { Engine } from './engine.ts';
import { CAMERA } from './engine.ts';
import { Overlay, esc, type Label } from './overlay.ts';
import { AtlasSprite, clipFrame, type AnimClip } from './actors.ts';
import { createNpcSprite, createPetSprite, createPlayerSprite, PET_ROWS } from './pets.ts';
import type { Presentation, Fx } from '../game/presentation.ts';
import { clamp } from '../game/presentation.ts';
import type { SceneRuntime } from './sceneBuilder.ts';

export type Hit =
  | { kind: 'npc' | 'portal' | 'pillar' | 'enemy' | 'target'; id: string }
  | { kind: 'ground'; dir: 'left' | 'right' | 'up' | 'down' };

interface Rect { x0: number; y0: number; x1: number; y1: number; hit: Hit }
interface Ent { sprite: AtlasSprite; x: number; z: number; flip?: boolean }
/** Quái hoang dạo quanh chỗ đứng gốc (server vẫn tính va chạm theo ô gốc: khi người chơi lại gần quái quay về ô gốc rồi quay mặt ra). */
interface Wild extends Ent { name: string; id: string; hx: number; hz: number; tx: number; tz: number; wait: number; amp: number; spd: number; moving: boolean }
interface Burst { mesh: THREE.Mesh; born: number; life: number; scale: number; kind: 'spark' | 'ring' | 'heal' }

const hash01 = (str: string): number => { let h = 2166136261; for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return ((h >>> 0) % 10000) / 10000; };
const PET_WORLD_H = 1.1, WILD_H = 1.3, BATTLE_H = 2.2;

function makeFxTextures(): Record<Burst['kind'], THREE.Texture> {
  const mk = (draw: (g: CanvasRenderingContext2D) => void): THREE.Texture => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d')!; draw(g);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  };
  return {
    spark: mk((g) => {
      const gr = g.createRadialGradient(64, 64, 2, 64, 64, 60); gr.addColorStop(0, 'rgba(255,250,220,1)'); gr.addColorStop(0.35, 'rgba(255,200,90,0.8)'); gr.addColorStop(1, 'rgba(255,120,40,0)');
      g.fillStyle = gr; g.fillRect(0, 0, 128, 128); g.strokeStyle = 'rgba(255,255,255,0.95)'; g.lineWidth = 5; g.lineCap = 'round';
      g.beginPath(); g.moveTo(22, 100); g.lineTo(106, 28); g.moveTo(26, 40); g.lineTo(102, 92); g.stroke();
    }),
    ring: mk((g) => { g.strokeStyle = 'rgba(190,130,255,1)'; g.lineWidth = 8; g.beginPath(); g.arc(64, 64, 48, 0, 7); g.stroke(); const gr = g.createRadialGradient(64, 64, 20, 64, 64, 60); gr.addColorStop(0, 'rgba(190,130,255,0)'); gr.addColorStop(1, 'rgba(190,130,255,0.35)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }),
    heal: mk((g) => { const gr = g.createRadialGradient(64, 64, 2, 64, 64, 60); gr.addColorStop(0, 'rgba(180,255,200,1)'); gr.addColorStop(0.5, 'rgba(110,235,150,0.55)'); gr.addColorStop(1, 'rgba(90,220,130,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); g.fillStyle = 'rgba(255,255,255,0.95)'; g.fillRect(56, 34, 16, 60); g.fillRect(34, 56, 60, 16); }),
  };
}
function makeRingTexture(col: string): THREE.Texture {
  const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d')!;
  const gr = g.createRadialGradient(64, 64, 30, 64, 64, 62); gr.addColorStop(0, col.replace('1)', '0)')); gr.addColorStop(0.72, col.replace('1)', '0.0)')); gr.addColorStop(0.82, col); gr.addColorStop(0.92, col.replace('1)', '0.35)')); gr.addColorStop(1, col.replace('1)', '0)'));
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}


/** Trụ đá teleport pixel-art (vẽ bằng mã, cùng mật độ texel 40px/đơn vị với vật trang trí của cảnh). */
function pxCanvas(w: number, h: number): [HTMLCanvasElement, CanvasRenderingContext2D] {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d', { willReadFrequently: true })!; g.imageSmoothingEnabled = false; return [c, g];
}
function pxTex(c: HTMLCanvasElement): THREE.Texture {
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.magFilter = THREE.NearestFilter; t.minFilter = THREE.NearestFilter; t.generateMipmaps = false; return t;
}
const PW = 44, PH = 32, CW = 28, CH = 52;
/** Bệ đá + thủy tinh vận chuyển xanh băng (video/JAR: "Thủy tinh vận chuyển ở phía Đông quảng trường"). */
function makePillarTextures(): { stone: THREE.Texture; rune: THREE.Texture; crystal: THREE.Texture; glow: THREE.Texture } {
  const outline = (g: CanvasRenderingContext2D, w: number, h: number): void => {
    const src = g.getImageData(0, 0, w, h); const out = g.getImageData(0, 0, w, h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      if ((src.data[(y * w + x) * 4 + 3] ?? 0) > 40) continue;
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as [number, number][]) {
        const nx = x + dx, ny = y + dy; if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
        if ((src.data[(ny * w + nx) * 4 + 3] ?? 0) > 200) { const o = (y * w + x) * 4; out.data[o] = 24; out.data[o + 1] = 20; out.data[o + 2] = 32; out.data[o + 3] = 255; break; }
      }
    }
    g.putImageData(out, 0, 0);
  };
  // --- bệ đá hai bậc ---
  const [c, g] = pxCanvas(PW, PH); const px = (x: number, y: number, w: number, h: number, col: string): void => { g.fillStyle = col; g.fillRect(x, y, w, h); };
  const block = (x0: number, y0: number, x1: number, y1: number): void => { px(x0, y0, x1 - x0, y1 - y0, '#8a8f96'); px(x0, y0, x1 - x0, 1, '#c9ced3'); px(x0, y0, 1, y1 - y0, '#b9bfc4'); px(x1 - 2, y0 + 1, 2, y1 - y0 - 1, '#5f646f'); px(x0 + 1, y1 - 1, x1 - x0 - 1, 1, '#444956'); };
  block(3, 18, 41, 30); block(8, 8, 36, 19);
  for (const [x, y, w] of [[3, 18, 9], [30, 19, 10], [10, 8, 7]] as [number, number, number][]) { px(x, y, w, 2, '#2f7a2a'); px(x + 1, y, w - 3, 1, '#4fa83a'); px(x + 2, y - 1, 2, 1, '#8ad04a'); }
  px(14, 22, 2, 1, '#6c717c'); px(26, 25, 3, 1, '#a3a9b0');
  outline(g, PW, PH); const stone = pxTex(c);
  // --- ký tự rune trên mặt bệ (cộng màu) ---
  const [r, rg] = pxCanvas(PW, PH); const rp = (x: number, y: number, w: number, h: number, col: string): void => { rg.fillStyle = col; rg.fillRect(x, y, w, h); };
  rp(12, 11, 20, 1, '#6feaff'); rp(20, 12, 4, 1, '#e8fdff'); rp(9, 22, 2, 1, '#6feaff'); rp(21, 25, 2, 3, '#6feaff'); rp(33, 22, 2, 1, '#6feaff');
  const rune = pxTex(r);
  // --- thủy tinh (đặc, nhiều mặt) ---
  const [cc, cg] = pxCanvas(CW, CH); const poly = (pts: number[][], col: string): void => { cg.fillStyle = col; cg.beginPath(); pts.forEach(([x, y], i) => (i ? cg.lineTo(x!, y!) : cg.moveTo(x!, y!))); cg.closePath(); cg.fill(); };
  const cx = 14;
  poly([[cx, 1], [26, 17], [cx, 50], [2, 17]], '#2a7fc0');
  poly([[cx, 1], [2, 17], [cx, 26]], '#bff6ff'); poly([[cx, 1], [26, 17], [cx, 26]], '#7fdcf5'); poly([[2, 17], [cx, 26], [cx, 50]], '#4cb4e6'); poly([[26, 17], [cx, 26], [cx, 50]], '#2a8ccc');
  poly([[cx, 5], [8, 15], [cx, 19]], '#f4feff'); poly([[cx, 33], [cx - 3, 40], [cx, 44]], '#aeeaff');
  outline(cg, CW, CH); const crystal = pxTex(cc);
  // --- hào quang (cộng màu): hình thủy tinh sáng + vầng ---
  const [gc, gg] = pxCanvas(CW, CH); gg.fillStyle = 'rgba(160,240,255,0.55)'; gg.beginPath(); gg.moveTo(cx, 0); gg.lineTo(27, 17); gg.lineTo(cx, 51); gg.lineTo(1, 17); gg.closePath(); gg.fill();
  const glow = pxTex(gc);
  return { stone, rune, crystal, glow };
}
function makeDiamondTex(): THREE.Texture {
  const [c, g] = pxCanvas(20, 32); const poly = (pts: number[][], col: string): void => { g.fillStyle = col; g.beginPath(); pts.forEach(([x, y], i) => (i ? g.lineTo(x!, y!) : g.moveTo(x!, y!))); g.closePath(); g.fill(); };
  poly([[10, 0], [19, 16], [10, 31], [1, 16]], '#181420'); poly([[10, 2], [17, 16], [10, 29], [3, 16]], '#3fb9d6');
  poly([[10, 2], [3, 16], [10, 16]], '#9af1ff'); poly([[10, 16], [17, 16], [10, 29]], '#1f7fa3'); poly([[10, 5], [6, 14], [10, 14]], '#e8fdff');
  return pxTex(c);
}
function makeRuneCircle(): THREE.Texture {
  const N = 64; const [c, g] = pxCanvas(N, N); const m = N / 2;
  for (let a = 0; a < 360; a += 3) {
    const rad = (a * Math.PI) / 180; const dash = Math.floor(a / 18) % 2 === 0;
    for (const [r, col, on] of [[29, 'rgba(111,234,255,0.95)', dash], [24, 'rgba(111,234,255,0.5)', true], [18, 'rgba(232,253,255,0.55)', !dash]] as [number, string, boolean][]) {
      if (!on) continue; g.fillStyle = col; g.fillRect(Math.round(m + Math.cos(rad) * r), Math.round(m + Math.sin(rad) * r), 1, 1);
    }
  }
  g.fillStyle = 'rgba(111,234,255,0.2)'; g.beginPath(); g.arc(m, m, 15, 0, Math.PI * 2); g.fill();
  return pxTex(c);
}

/** Cảnh thế giới + trận đấu HD-2D. Đọc Presentation (logic thuần) và vẽ bằng Engine. */
export class Stage {
  readonly overlay: Overlay;
  readonly root = new THREE.Group();
  private scn: SceneRuntime | null = null;
  private mapId = '';
  /** Id map đã tải xong (dùng cho màn loading khi chuyển map). */
  get loadedMap(): string { return this.scn ? this.mapId : ''; }
  private loading = false;
  private player: Ent | null = null;
  private pet: (Ent & { species: string; sprite: AtlasSprite }) | null = null;
  private npcs = new Map<string, Ent & { name: string }>();
  private spawns = new Map<string, Wild>();
  private units = new Map<string, Ent & { species: string }>();
  private portals: { id: string; x: number; z: number; name: string; mesh: THREE.Group; rune: THREE.Sprite; disc: THREE.Mesh; hub: boolean; crystal: THREE.Sprite | null }[] = [];
  private hits: Rect[] = [];
  private bursts: Burst[] = [];
  private fxSpawned = new WeakSet<Fx>();
  private fxTex = makeFxTextures();
  private pillar = makePillarTextures();
  private diamondTex = makeDiamondTex();
  private runeCircle = makeRuneCircle();
  private ringTex = { portal: makeRingTexture('rgba(111,237,255,1)'), player: makeRingTexture('rgba(165,242,216,1)'), target: makeRingTexture('rgba(111,237,255,1)') };
  private camX = 0; private camZ = 0; private camInit = false;
  private ringPlayer: THREE.Mesh; private ringTarget: THREE.Mesh;
  private shake = new Map<string, number>();
  /** Gỡ lỗi / e2e: trạng thái trình diễn đọc được từ trang. */
  banner = '';
  onPick: ((h: Hit) => void) | null = null;
  onMapLoaded: ((id: string) => void) | null = null;
  private pointerDown: { x: number; y: number; t: number } | null = null;
  private unsub: () => void;

  constructor(readonly engine: Engine, readonly host: HTMLElement, readonly pres: Presentation) {
    this.overlay = new Overlay(host);
    engine.scene.add(this.root);
    const ringGeo = new THREE.PlaneGeometry(1, 1); ringGeo.rotateX(-Math.PI / 2);
    const rm = (tex: THREE.Texture): THREE.Mesh => { const m = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ map: tex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide })); m.renderOrder = -5; m.visible = false; this.root.add(m); return m; };
    this.ringPlayer = rm(this.ringTex.player); this.ringTarget = rm(this.ringTex.target);
    this.unsub = engine.onFrame((dt) => this.update(dt));
    host.addEventListener('pointerdown', this.onDown);
    host.addEventListener('pointerup', this.onUp);
  }

  // ---------- nhập liệu ----------
  private onDown = (e: PointerEvent): void => { if ((e.target as HTMLElement).closest('[data-ui]')) return; this.pointerDown = { x: e.clientX, y: e.clientY, t: performance.now() }; };
  private onUp = (e: PointerEvent): void => {
    const d = this.pointerDown; this.pointerDown = null; if (!d) return;
    if (Math.hypot(e.clientX - d.x, e.clientY - d.y) > 14) return;
    const r = this.host.getBoundingClientRect(); const hit = this.pick(e.clientX - r.left, e.clientY - r.top);
    if (hit) this.onPick?.(hit);
  };
  pick(x: number, y: number): Hit | null {
    for (let i = this.hits.length - 1; i >= 0; i--) { const h = this.hits[i]!; if (x >= h.x0 && x <= h.x1 && y >= h.y0 && y <= h.y1) return h.hit; }
    if (!this.pres.battle && this.player) {
      const p = this.engine.project(this.player.x, 0, this.player.z); const dx = x - p.x, dy = y - p.y;
      return { kind: 'ground', dir: Math.abs(dx) > Math.abs(dy) ? (dx < 0 ? 'left' : 'right') : (dy < 0 ? 'up' : 'down') };
    }
    return null;
  }

  // ---------- nạp ----------
  private async ensureMap(): Promise<void> {
    const id = this.pres.mapId;
    if (this.loading || id === this.mapId || !this.pres.character) return;
    this.loading = true;
    try {
      this.scn = await this.engine.loadMap(id);
      this.mapId = id; this.camInit = false;
      this.clearEntities();
      this.onMapLoaded?.(id);
    } finally { this.loading = false; }
  }
  private clearEntities(): void {
    for (const e of [this.player, this.pet, ...this.npcs.values(), ...this.spawns.values(), ...this.units.values()]) if (e) { this.root.remove(e.sprite.group); e.sprite.dispose(); }
    this.player = null; this.pet = null; this.npcs.clear(); this.spawns.clear(); this.units.clear();
    for (const p of this.portals) { this.root.remove(p.mesh); p.mesh.traverse((o) => { const m = (o as THREE.Mesh).material as THREE.Material | undefined; m?.dispose(); }); }
    this.portals = [];
  }
  private creating = new Set<string>();
  private async make(key: string, f: () => Promise<void>): Promise<void> {
    if (this.creating.has(key)) return; this.creating.add(key);
    try { await f(); } catch (e) { console.warn('stage:make', key, e); } finally { this.creating.delete(key); }
  }
  private grid(gx: number, gy: number): { x: number; z: number } {
    const d = this.pres.definition; return this.scn!.gridToWorld(gx, gy, d?.width ?? 40, d?.height ?? 24);
  }

  private syncEntities(): void {
    const c = this.pres.character, cat = this.pres.catalog; if (!c || !cat || !this.scn) return;
    const U = this.engine.U; const mapId = this.mapId;
    if (!this.player) void this.make('player', async () => { const s = await createPlayerSprite(U); if (this.mapId !== mapId) { s.dispose(); return; } this.player = { sprite: s, x: 0, z: 0 }; this.root.add(s.group); });
    const active = c.pets.find((p) => p.id === c.active_pet_id);
    if (active && (!this.pet || this.pet.species !== active.species_id)) {
      const sp = active.species_id;
      void this.make('pet:' + sp, async () => {
        const { sprite } = await createPetSprite(sp, PET_WORLD_H, U, this.engine.tier.name === 'low');
        if (this.mapId !== mapId) { sprite.dispose(); return; }
        if (this.pet) { this.root.remove(this.pet.sprite.group); this.pet.sprite.dispose(); }
        const start = this.player ? { x: this.player.x, z: this.player.z } : { x: 0, z: 0 };
        this.pet = { sprite, x: start.x, z: start.z, species: sp }; this.root.add(sprite.group);
      });
    } else if (!active && this.pet) { this.root.remove(this.pet.sprite.group); this.pet.sprite.dispose(); this.pet = null; }
    for (const npc of Object.values(cat.npcs)) {
      if (npc.map_id !== mapId || this.npcs.has(npc.id)) continue;
      void this.make('npc:' + npc.id, async () => {
        const s = await createNpcSprite(npc.id, U); if (this.mapId !== mapId) { s.dispose(); return; }
        const g = this.grid(npc.x, npc.y); const e = { sprite: s, x: g.x, z: g.z, name: npc.name }; this.npcs.set(npc.id, e); this.root.add(s.group); s.setPos(g.x, 0, g.z);
      });
    }
    for (const [i, sp] of (this.pres.definition?.wild_spawns ?? []).entries()) {
      if (this.spawns.has(sp.id)) continue;
      void this.make('spawn:' + sp.id, async () => {
        const { sprite } = await createPetSprite(sp.species_id, WILD_H, U, this.engine.tier.name === 'low');
        if (this.mapId !== mapId) { sprite.dispose(); return; }
        const g = this.grid(sp.x, sp.y); const name = cat.species[sp.species_id]?.name ?? sp.species_id;
        const r1 = hash01(sp.id + 'a'), r2 = hash01(sp.id + 'b'), r3 = hash01(sp.id + 'c'); const amp = 1.3 + r1 * 1.3;
        this.spawns.set(sp.id, { sprite, x: g.x + (r2 - 0.5) * amp, z: g.z, name, id: sp.id, flip: i % 2 === 0, hx: g.x, hz: g.z, tx: g.x + (r3 - 0.5) * 2 * amp, tz: g.z, wait: r2 * 2.5, amp, spd: 0.38 + r3 * 0.22, moving: false }); this.root.add(sprite.group); sprite.setPos(g.x, 0, g.z);
      });
    }
    if (this.portals.length === 0 && this.pres.definition) {
      const defn = this.pres.definition; const pl = this.scn!.data.pillar;
      // Cổng cùng x gộp thành một "trụ" (map trung tâm); cổng lẻ là cửa kim cương xanh ở mép map như bản gốc.
      const groups = new Map<number, typeof defn.portals>();
      for (const p of defn.portals) { const px = p.x ?? p.rect?.[0] ?? 0; groups.set(px, [...(groups.get(px) ?? []), p]); } // P01: portal có rect thay x
      for (const [gx, list] of groups) {
        const first = list[0]!; const hub = list.length > 1 && !!pl;
        const g0 = this.grid(gx, (defn.height || 24) / 2); const mid = (this.scn!.data.walk.x0 + this.scn!.data.walk.x1) / 2;
        const g = hub ? { x: pl!.x, z: pl!.z } : { x: g0.x + Math.sign(mid - g0.x) * 1.6, z: g0.z };
        const mesh = new THREE.Group(); mesh.position.set(g.x, 0, g.z);
        const disc = new THREE.Mesh(new THREE.PlaneGeometry(hub ? 2.3 : 1.9, hub ? 2.3 : 1.9).rotateX(-Math.PI / 2), new THREE.MeshBasicMaterial({ map: this.runeCircle, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide }));
        disc.position.y = 0.02; disc.renderOrder = -5; mesh.add(disc);
        let rune: THREE.Sprite; let crystal: THREE.Sprite | null = null;
        if (hub) {
          const W = (PW / 40) * 1.25, H = (PH / 40) * 1.25;
          const st = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.pillar.stone, transparent: true, fog: false })); st.scale.set(W, H, 1); st.center.set(0.5, 0); st.position.y = -0.05;
          const pr = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.pillar.rune, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false })); pr.scale.set(W, H, 1); pr.center.set(0.5, 0); pr.position.y = -0.05;
          const cw = (CW / 40) * 1.35, ch = (CH / 40) * 1.35;
          crystal = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.pillar.crystal, transparent: true, fog: false })); crystal.scale.set(cw, ch, 1); crystal.center.set(0.5, 0); crystal.userData.base = 0.95;
          rune = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.pillar.glow, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, fog: false })); rune.scale.set(cw * 1.5, ch * 1.5, 1); rune.center.set(0.5, 0.17); rune.userData.base = 0.95;
          mesh.add(st, pr, crystal, rune);
        } else {
          crystal = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.diamondTex, transparent: true, fog: false })); crystal.scale.set(0.7, 1.12, 1); crystal.center.set(0.5, 0); crystal.userData.base = 0.7; mesh.add(crystal);
          rune = new THREE.Sprite(new THREE.SpriteMaterial({ map: this.diamondTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, opacity: 0.4, fog: false })); rune.scale.set(0.9, 1.44, 1); rune.center.set(0.5, 0); rune.userData.base = 0.6; mesh.add(rune);
        }
        this.root.add(mesh);
        this.portals.push({ id: first.id, x: g.x, z: g.z, name: hub ? 'Thủy Tinh Dịch Chuyển' : (cat.maps[first.to]?.name ?? first.to), mesh, rune, disc, hub, crystal });
      }
    }
  }

  private unitEntities(): void {
    const b = this.pres.battle; if (!b) { if (this.units.size) { for (const e of this.units.values()) { this.root.remove(e.sprite.group); e.sprite.dispose(); } this.units.clear(); } return; }
    for (const u of b.units) {
      const have = this.units.get(u.id);
      if (have && have.species === u.species_id) continue;
      void this.make('unit:' + u.id, async () => {
        const { sprite } = await createPetSprite(u.species_id, BATTLE_H, this.engine.U, this.engine.tier.name === 'low');
        if (!this.pres.battle) { sprite.dispose(); return; }
        const old = this.units.get(u.id); if (old) { this.root.remove(old.sprite.group); old.sprite.dispose(); }
        this.units.set(u.id, { sprite, x: 0, z: 0, species: u.species_id }); this.root.add(sprite.group);
      });
    }
    for (const [id, e] of [...this.units]) if (!b.units.some((u) => u.id === id)) { this.root.remove(e.sprite.group); e.sprite.dispose(); this.units.delete(id); }
  }

  // ---------- khung hình ----------
  update(dt: number): void {
    const pres = this.pres; pres.update(dt);
    if (!pres.character) { this.overlay.clear(); return; }
    void this.ensureMap();
    if (!this.scn || this.mapId !== pres.mapId) return;
    this.syncEntities(); this.unitEntities();
    const eng = this.engine; const battle = pres.battle; const t = pres.elapsed;
    this.hits = []; this.overlay.begin();
    const sw = eng.canvas.clientWidth; void sw;
    const def = pres.definition; const walk = this.scn.data.walk;
    for (const p of this.portals) p.mesh.visible = !battle;
    for (const e of [this.player, this.pet, ...this.npcs.values(), ...this.spawns.values()]) if (e) e.sprite.group.visible = !battle;
    const targetDist = battle ? eng.baseDist * 0.8 : eng.baseDist; eng.camDist += (targetDist - eng.camDist) * (1 - Math.exp(-dt * 4));
    const midZ = (walk.z0 + walk.z1) / 2;
    let focusX = this.camX, focusZ = midZ;

    if (!battle) {
      const pp = this.grid(pres.displayedX, pres.displayedY);
      for (const p of this.portals) {
        const bob = p.crystal ? 0.08 * Math.sin(t * 2 + p.x) : 0; if (p.crystal) { p.crystal.position.y = (p.crystal.userData.base as number) + bob; p.rune.position.y = (p.rune.userData.base as number) + bob; }
        (p.rune.material as THREE.SpriteMaterial).opacity = (p.hub ? 0.55 : 0.3) + 0.35 * Math.sin(t * 2.4 + p.x); p.disc.rotation.y = t * 0.35; p.disc.scale.setScalar(1 + 0.04 * Math.sin(t * 2.2));
        const pr = eng.project(p.x, p.hub ? 2.6 : 2.0, p.z); const on = pr.on && pr.x > 8 && pr.x < eng.canvas.clientWidth - 8; // nhãn chỉ hiện khi cổng nằm trong màn hình, tránh đè tên khu vực/nút HUD
        this.overlay.put({ key: 'portal:' + p.id, x: Math.max(80 + (pr.y < 280 ? 56 : 0), Math.min(eng.canvas.clientWidth - 80 - (pr.y < 120 ? 78 : 0), pr.x)), y: Math.max(14, pr.y - 6), on, html: p.hub ? `✦ ${esc(p.name)} ✦` : `<span class="arrow">${p.x < (walk.x0 + walk.x1) / 2 ? '◀' : '▶'}</span> ${esc(p.name)}`, cls: 'portal' });
        this.pushHit(p.x, 0.0, p.z, 2.0, p.hub ? 2.6 : 1.8, p.hub ? { kind: 'pillar', id: p.id } : { kind: 'portal', id: p.id });
      }
      for (const n of this.npcs.values()) {
        n.sprite.setPos(n.x, 0, n.z); n.sprite.setCell(0, 0);
        const head = eng.project(n.x, n.sprite.bodyHeight + 0.15, n.z);
        this.overlay.put({ key: 'npc:' + n.name, x: head.x, y: head.y, on: head.on, html: `<b class="bang" style="--d:${(n.x * 0.37).toFixed(2)}s">!</b><span>${esc(n.name)}</span>`, cls: 'npc' });
      }
      const npcEntries = [...this.npcs.entries()];
      for (const [id, n] of npcEntries) this.pushHit(n.x, 0, n.z, 1.4, n.sprite.bodyHeight + 0.5, { kind: 'npc', id });
      for (const s of this.spawns.values()) {
        this.wander(s, dt, pp.x, pp.z, walk);
        const f = Math.floor(t * (s.moving ? 8 : 4) + s.hx) % 4; s.sprite.setCell(f, s.moving ? PET_ROWS.move : PET_ROWS.idle); s.sprite.setFlip(!!s.flip); s.sprite.setPos(s.x, 0, s.z); s.sprite.setBob(0);
        const head = eng.project(s.x, WILD_H + 0.2, s.z);
        this.overlay.put({ key: 'wild:' + s.id, x: head.x, y: head.y, on: head.on, html: esc(s.name), cls: 'wild' });
        this.pushHit(s.x, 0, s.z, 1.6, WILD_H + 0.3, { kind: 'enemy', id: s.id });
      }
      if (this.player) {
        const pl = this.player; pl.x = pp.x; pl.z = pp.z;
        const run = pres.walking; const f = Math.floor(t * 8) % 6;
        pl.sprite.setCell(f, run ? 1 : 0); pl.sprite.setFlip(pres.facingLeft); pl.sprite.setPos(pp.x, 0, pp.z);
        this.ringPlayer.visible = true; this.ringPlayer.position.set(pp.x, 0.02, pp.z); this.ringPlayer.scale.set(1.5, 1, 1.5);
        const head = eng.project(pp.x, pl.sprite.bodyHeight + 0.2, pp.z);
        this.overlay.put({ key: 'me', x: head.x, y: head.y, on: head.on, html: esc(pres.character.name), cls: 'me' });
      } else this.ringPlayer.visible = false;
      this.ringTarget.visible = false;
      if (this.pet) {
        const behind = pres.facingLeft ? 1.25 : -1.25;
        const tx = pp.x + behind, tz = pp.z + 0.15; const k = 1 - Math.exp(-dt * 6);
        const moving = Math.abs(tx - this.pet.x) > 0.08 || Math.abs(tz - this.pet.z) > 0.08;
        this.pet.x += (tx - this.pet.x) * k; this.pet.z += (tz - this.pet.z) * k;
        this.pet.sprite.setPos(this.pet.x, 0, this.pet.z);
        this.pet.sprite.setCell(Math.floor(t * (moving ? 8 : 4)) % 4, moving ? PET_ROWS.move : PET_ROWS.idle);
        this.pet.sprite.setFlip(!pres.facingLeft); this.pet.sprite.group.visible = true;
      }
      focusX = pp.x; focusZ = midZ + (pp.z - midZ) * 0.4;
    } else {
      this.ringPlayer.visible = false;
      this.layoutBattle(dt, focusX, midZ);
      const first = [...this.units.values()][0];
      void first; focusX = this.battleCenterX; focusZ = midZ;
    }
    // camera
    const hw = eng.halfWidth; const x0 = this.scn.data.len[0], x1 = this.scn.data.len[1];
    const tx = x1 - x0 > hw * 2 ? clamp(focusX, x0 + hw, x1 - hw) : (x0 + x1) / 2;
    if (!this.camInit) { this.camX = tx; this.camZ = focusZ; this.camInit = true; }
    const k = 1 - Math.exp(-dt * 7); this.camX += (tx - this.camX) * k; this.camZ += (focusZ - this.camZ) * k;
    eng.U.uCamX.value = this.camX; eng.placeCamera(this.camX, this.camZ);
    void def;
    this.updateBursts(t);
    this.overlay.end();
  }

  /** Quái đi qua lại trong biên độ nhỏ, đứng nghỉ ngẫu nhiên; khi người chơi tới gần thì về ô gốc (khớp va chạm của server) và quay mặt về phía người chơi. */
  private wander(s: Wild, dt: number, px: number, pz: number, walk: { x0: number; x1: number; z0: number; z1: number }): void {
    const near = Math.abs(px - s.hx) < 4.2 && Math.abs(pz - s.hz) < 2.6;
    let gx = s.tx, gz = s.tz, sp = s.spd;
    if (near) { gx = s.hx; gz = s.hz; sp = 2.6; }
    else if (s.wait > 0) { s.wait -= dt; s.moving = false; return; }
    const dx = gx - s.x, dz = gz - s.z; const d = Math.hypot(dx, dz);
    if (d < 0.05) {
      s.moving = false;
      if (near) s.flip = px > s.x;               // đứng ở ô gốc, nhìn về phía người chơi
      else {
        s.wait = 0.9 + Math.random() * 2.6;
        s.tx = clamp(s.hx + (Math.random() * 2 - 1) * s.amp, walk.x0 + 0.4, walk.x1 - 0.4);
        s.tz = clamp(s.hz + (Math.random() * 2 - 1) * 0.55, walk.z0, walk.z1);
      }
      return;
    }
    const st = Math.min(d, sp * dt); s.x += (dx / d) * st; s.z += (dz / d) * st; s.moving = true;
    if (Math.abs(dx) > 0.02) s.flip = dx > 0;     // atlas quái nhìn sang trái; đi sang phải thì lật
  }

  private battleCenterX = 0;
  private layoutBattle(dt: number, _fx: number, midZ: number): void {
    const pres = this.pres; const b = pres.battle!; const eng = this.engine; const t = pres.elapsed;
    const x0 = this.scn!.data.len[0], x1 = this.scn!.data.len[1]; const hw = eng.halfWidth;
    const px = this.grid(pres.displayedX, pres.displayedY).x;
    const cx = x1 - x0 > hw * 2 ? clamp(px, x0 + hw, x1 - hw) : (x0 + x1) / 2; this.battleCenterX = cx;
    const spread = Math.min(hw * 0.5, 4.2);
    const pos = new Map<string, { x: number; z: number }>(); let li = 0, ri = 0;
    for (const u of b.units) { const enemy = u.side !== 'player'; const row = enemy ? ri++ : li++; pos.set(u.id, { x: cx + (enemy ? -spread : spread), z: midZ + 0.9 - row * 1.7 }); }
    for (const u of b.units) {
      const e = this.units.get(u.id); const base = pos.get(u.id)!; if (!e) continue;
      const enemy = u.side !== 'player'; let x = base.x, z = base.z; let row: number = PET_ROWS.idle; let frame = Math.floor(t * 4 + (u.id.length)) % 4; let mulG = 1;
      let opacity = 1;
      for (const fx of pres.effects) {
        const age = t - fx.start; if (age < 0) continue;
        if (fx.type === 'skill_cast' && fx.actor_id === u.id && age < 0.5) {
          row = this.rowFor(fx); frame = Math.min(3, Math.floor((age / 0.5) * 4));
          const tp = pos.get(fx.target_id) ?? base; const dx = tp.x - base.x, dz = tp.z - base.z; const n = Math.hypot(dx, dz) || 1; const lunge = Math.sin((age / 0.5) * Math.PI) * 1.1;
          x += (dx / n) * lunge; z += (dz / n) * lunge;
        }
        if (fx.type === 'damage' && fx.target_id === u.id && age < 0.35) { mulG = 0.65 + age; x += Math.sin(age * 65) * 0.1; }
      }
      if (u.hp <= 0) {
        row = PET_ROWS.down; if (!pres.deathStarted.has(u.id)) pres.deathStarted.set(u.id, t);
        frame = Math.min(3, Math.floor((t - pres.deathStarted.get(u.id)!) * 6)); opacity = 0.5;
      }
      e.x = x; e.z = z;
      e.sprite.setPos(x, 0, z); e.sprite.setCell(frame, row); e.sprite.setFlip(enemy); e.sprite.setMul(1, mulG, mulG); e.sprite.setOpacity(opacity); e.sprite.group.visible = true;
      const head = eng.project(x, BATTLE_H + 0.05, z); head.y = Math.max(head.y, 96); const foot = eng.project(x, 0, z);
      const hpNow = pres.hpDisplay.get(u.id) ?? u.hp; const max = Math.max(u.max_hp, 1); const pct = clamp(hpNow / max, 0, 1) * 100;
      const status = u.statuses.map((s) => `<i>${esc(this.pres.catalog?.statuses?.[s.id]?.name ?? s.id)}·${s.remaining}</i>`).join('');
      this.overlay.put({ key: 'u:' + u.id, x: head.x, y: head.y, on: head.on, cls: `unit ${enemy ? 'enemy' : 'ally'}`, z: Math.round(foot.y),
        html: `<span class="nm">${esc(tn(u.name))}</span><span class="hp"><b style="width:${pct.toFixed(1)}%"></b></span><span class="num">${Math.max(0, Math.round(u.hp))} / ${Math.round(max)}</span>${status ? `<span class="st">${status}</span>` : ''}` });
      if (enemy && u.hp > 0) {
        const w = 1.9; this.pushHit(x, 0, z, w, BATTLE_H + 0.4, { kind: 'target', id: u.id });
        if (u.id === pres.selectedTarget) {
          this.ringTarget.visible = true; this.ringTarget.position.set(x, 0.02, z); const s = 2.6 + Math.sin(t * 5) * 0.12; this.ringTarget.scale.set(s, 1, s);
          const mk = eng.project(x, BATTLE_H + 1.0, z); this.overlay.put({ key: 'tgt', x: mk.x, y: mk.y + Math.sin(t * 6) * 3, on: mk.on, html: '▼', cls: 'marker' });
        }
      }
    }
    if (!b.units.some((u) => u.id === pres.selectedTarget && u.hp > 0)) this.ringTarget.visible = false;
    // hiệu ứng
    for (const fx of pres.effects) {
      const age = t - fx.start; if (age < 0) continue;
      const tp = pos.get(fx.target_id); if (!tp) continue;
      const tu = pres.unitById(fx.target_id); void tu;
      if (!this.fxSpawned.has(fx)) {
        this.fxSpawned.add(fx);
        if (fx.type === 'damage') this.burst('spark', tp.x, BATTLE_H * 0.5, tp.z, 0.35, 2.2);
        else if (fx.type === 'heal') this.burst('heal', tp.x, BATTLE_H * 0.5, tp.z, 0.8, 2.4);
        else if (fx.type === 'status_applied') this.burst('ring', tp.x, BATTLE_H * 0.4, tp.z, 0.9, 3.0);
      }
      const rise = age * 0.9; const a = clamp(1.2 - age, 0, 1);
      const p = eng.project(tp.x, BATTLE_H + 0.5 + rise, tp.z);
      if (fx.type === 'damage') this.overlay.put({ key: `fx:${fx.start}:${fx.target_id}:d`, x: p.x, y: p.y, on: p.on, html: `−${Math.round(fx.amount)}`, cls: 'num-dmg', scale: 1 + Math.max(0, 0.3 - age) * 2, z: 9999 });
      else if (fx.type === 'heal') this.overlay.put({ key: `fx:${fx.start}:${fx.target_id}:h`, x: p.x, y: p.y, on: p.on, html: `+${Math.round(fx.amount)}`, cls: 'num-heal', z: 9999 });
      else if (fx.type === 'miss') this.overlay.put({ key: `fx:${fx.start}:${fx.target_id}:m`, x: p.x, y: p.y, on: p.on, html: 'Trượt', cls: 'num-miss', z: 9999 });
      void a;
    }
    if (pres.finishUntil > 0) {
      const r = b.result; const text = r === 'win' || r === 'victory' ? 'CHIẾN THẮNG' : r === 'loss' || r === 'defeat' ? 'THẤT BẠI' : r === 'flee' || r === 'fled' ? 'RÚT LUI' : String(r || '').toUpperCase();
      this.banner = text; if (text) this.overlay.put({ key: 'banner', x: eng.canvas.clientWidth / 2, y: eng.canvas.clientHeight * 0.34, on: true, html: text === 'CHIẾN THẮNG' ? '<img class="bimg" src="./assets/ui/battle_win.png" alt="Chiến thắng">' : text === 'THẤT BẠI' ? '<img class="bimg" src="./assets/ui/battle_loss.png" alt="Thất bại">' : esc(text), cls: 'banner' });
    } else this.banner = '';
    void dt;
  }
  private rowFor(fx: Fx): number {
    const id = (fx as unknown as { skill_id?: string }).skill_id ?? ''; const sk = id ? (this.pres.catalog?.skills[id] as { kind?: string; category?: string } | undefined) : undefined;
    const kind = sk?.kind ?? sk?.category ?? '';
    return /magic|spell|cast|heal|buff|status/.test(kind) ? PET_ROWS.cast : PET_ROWS.attack;
  }

  private pushHit(x: number, y: number, z: number, w: number, h: number, hit: Hit): void {
    const eng = this.engine; const a = eng.project(x, y, z), b = eng.project(x, y + h, z);
    if (!a.on) return;
    const wpx = Math.max(Math.abs(eng.project(x + w / 2, y, z).x - eng.project(x - w / 2, y, z).x), 48);
    const top = Math.min(a.y, b.y), bot = Math.max(a.y, b.y);
    const hpx = Math.max(bot - top, 48);
    this.hits.push({ x0: a.x - wpx / 2, x1: a.x + wpx / 2, y0: bot - hpx, y1: bot + 14, hit });
  }

  private burst(kind: Burst['kind'], x: number, y: number, z: number, life: number, scale: number): void {
    const mat = new THREE.MeshBasicMaterial({ map: this.fxTex[kind], transparent: true, blending: THREE.AdditiveBlending, depthWrite: false, depthTest: false, side: THREE.DoubleSide });
    const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat); m.position.set(x, y, z + 0.4); m.rotation.x = -(CAMERA.pitchDeg * Math.PI) / 180 * 0 ; m.renderOrder = 20;
    this.root.add(m); this.bursts.push({ mesh: m, born: this.pres.elapsed, life, scale, kind });
  }
  private updateBursts(t: number): void {
    for (const b of this.bursts) {
      const age = (t - b.born) / b.life; const m = b.mesh; const mat = m.material as THREE.MeshBasicMaterial;
      if (age >= 1) { this.root.remove(m); mat.dispose(); m.geometry.dispose(); (b as { dead?: boolean }).dead = true; continue; }
      m.scale.setScalar(b.scale * (0.5 + age * 0.9)); mat.opacity = 1 - age;
    }
    this.bursts = this.bursts.filter((b) => !(b as { dead?: boolean }).dead);
  }

  /** Số liệu cho kiểm thử/đo hiệu năng. */
  debug(): Record<string, unknown> {
    const c = this.pres.character;
    return { map: this.mapId, x: c?.x, y: c?.y, dispX: +this.pres.displayedX.toFixed(2), battle: this.pres.battleId, animating: this.pres.isAnimating(), npcs: this.npcs.size, spawns: this.spawns.size, units: this.units.size, hits: this.hits.length, banner: this.banner };
  }
  hitRects(): { kind: string; id?: string; x0: number; y0: number; x1: number; y1: number }[] {
    return this.hits.map((h) => ({ kind: h.hit.kind, id: 'id' in h.hit ? h.hit.id : undefined, x0: h.x0, y0: h.y0, x1: h.x1, y1: h.y1 }));
  }
  dispose(): void {
    this.unsub(); this.host.removeEventListener('pointerdown', this.onDown); this.host.removeEventListener('pointerup', this.onUp);
    this.clearEntities(); this.overlay.clear();
  }
}
export type { AnimClip };
export { clipFrame };
