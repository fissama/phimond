import * as THREE from 'three';
import type { MapDef, Npc, WildSpawn } from '@phimond/protocol';
import { PRESETS, settings, type FpsCap, type Quality } from '../state/settings.ts';
import { INDOOR, lightAt, type Light } from './daylight.ts';
import { Post } from './post.ts';
import { asset, textures } from './assets.ts';
import { buildScene, THEMES, type BuiltScene } from './scene.ts';
import { blobShadow, CharacterSprite, PetSprite, propSprite } from './sprites.ts';
import type { Cell, Direction } from '../world/coords.ts';

export type Pick =
  | { kind: 'ground'; cell: Cell }
  | { kind: 'npc'; id: string }
  | { kind: 'spawn'; id: string }
  | { kind: 'pedestal'; index: number }
  | { kind: 'pillar' };

interface Actor {
  root: THREE.Group;
  label: HTMLDivElement | null;
}

const PITCH = 0.66; // rad, góc nhìn xuống
const DIST = 20;
const FOV = 24;

/**
 * Renderer world: cảnh HD-2D, camera bám người chơi, NPC/quái/người chơi, chọn đối tượng bằng chạm/click,
 * nhãn tên (DOM), giới hạn FPS và mức đồ họa.
 */
export class Engine {
  readonly renderer: THREE.WebGLRenderer;
  readonly scene = new THREE.Scene();
  readonly camera = new THREE.PerspectiveCamera(FOV, 1, 0.5, 160);
  private readonly hemi = new THREE.HemisphereLight(0xffffff, 0x5a5048, 1);
  private readonly sun = new THREE.DirectionalLight(0xffffff, 1.2);
  private world: BuiltScene | null = null;
  private map: MapDef | null = null;
  private player: CharacterSprite | null = null;
  private readonly playerRoot = new THREE.Group();
  private playerBlob: THREE.Mesh | null = null;
  private readonly npcs = new Map<string, Actor & { sprite: CharacterSprite | THREE.Object3D }>();
  private readonly spawns = new Map<string, Actor & { sprite: PetSprite; base: Cell; t: number }>();
  /** Thần thú 5★ trưng bày trên bệ đá (chỉ là mô hình, không nhận được). */
  private readonly showcases: { root: THREE.Group; sprite: PetSprite; t: number; baseY: number }[] = [];
  private readonly labels: HTMLDivElement;
  private readonly target = new THREE.Vector3();
  private readonly ray = new THREE.Raycaster();
  private readonly resizeObs: ResizeObserver;
  private post: Post | null = null;
  private lightClock = 0;
  private indoor = false;
  private raf = 0;
  private last = 0;
  private cap: FpsCap = 60;
  private quality: Quality = 'medium';
  private frameCb: ((dt: number) => void) | null = null;
  /** Thời gian khung gần nhất (ms) để đo/HUD debug. */
  readonly frameTimes: number[] = [];

  constructor(private readonly host: HTMLElement) {
    this.renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance' });
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.domElement.dataset.testid = 'world-canvas';
    this.renderer.domElement.style.display = 'block';
    host.appendChild(this.renderer.domElement);
    this.labels = document.createElement('div');
    this.labels.style.cssText = 'position:absolute;inset:0;pointer-events:none;overflow:hidden';
    host.appendChild(this.labels);
    this.sun.position.set(-8, 14, 10);
    this.scene.add(this.hemi, this.sun, this.sun.target, this.playerRoot);
    this.resizeObs = new ResizeObserver(() => this.resize());
    this.resizeObs.observe(host);
  }

  setFpsCap(cap: FpsCap): void {
    this.cap = cap;
  }

  setQuality(q: Quality): void {
    this.quality = q;
    const P = PRESETS[q];
    textures.budget = P.textureBudgetMB * 1024 * 1024;
    this.renderer.shadowMap.enabled = P.shadows === 'real';
    this.renderer.shadowMap.type = THREE.PCFShadowMap;
    this.sun.castShadow = P.shadows === 'real';
    if (P.post === 'none') {
      this.post?.dispose();
      this.post = null;
    } else {
      this.post ??= new Post(this.renderer, this.scene, this.camera);
      this.post.setQuality(q);
    }
    if (P.shadowMapSize) this.sun.shadow.mapSize.set(P.shadowMapSize, P.shadowMapSize);
    this.resize();
  }

  get currentQuality(): Quality {
    return this.quality;
  }

  onFrame(cb: (dt: number) => void): void {
    this.frameCb = cb;
  }

  /** Dựng cảnh map mới (giải phóng cảnh cũ). NPC/quái/người chơi được dựng lại theo dữ liệu map. */
  async loadMap(map: MapDef, npcs: Npc[], playerAsset: string): Promise<void> {
    this.unloadMap();
    this.map = map;
    const T = THEMES[map.theme] ?? THEMES.forest!;
    this.scene.background = new THREE.Color(T.sky);
    this.scene.fog = T.fog && PRESETS[this.quality].backdrop ? new THREE.Fog(T.fog[0], T.fog[1], T.fog[2]) : null;
    this.hemi.intensity = T.ambient;
    this.sun.intensity = T.sun;
    this.sun.color.set(T.sunColor);
    const W = map.width;
    const H = map.height || map.width;
    const sc = this.sun.shadow.camera;
    sc.left = -W;
    sc.right = W;
    sc.top = H;
    sc.bottom = -H;
    sc.far = 120;
    this.sun.position.set(W / 2 - 10, 24, H / 2 + 16);
    this.sun.target.position.set(W / 2, 0, H / 2);
    sc.updateProjectionMatrix();

    const real = PRESETS[this.quality].shadows === 'real';
    const blob = PRESETS[this.quality].shadows === 'blob';
    this.world = await buildScene(map, this.quality);
    this.scene.add(this.world.group);
    this.indoor = T.indoor === true;
    this.updateLight(0, true);

    if (!this.player) {
      this.player = await CharacterSprite.create(playerAsset, { castShadow: real });
      this.playerRoot.add(this.player.root);
    }
    if (this.playerBlob) this.playerRoot.remove(this.playerBlob);
    this.playerBlob = blob ? blobShadow(0.42) : null;
    if (this.playerBlob) this.playerRoot.add(this.playerBlob);

    await Promise.all(
      npcs.map(async (n) => {
        const id = `npc-${n.id}`;
        let sprite: CharacterSprite | THREE.Object3D;
        const root = new THREE.Group();
        if (asset(id)?.category === 'npc') {
          const cs = await CharacterSprite.create(id, { castShadow: real, tint: T.tint });
          sprite = cs;
          root.add(cs.root);
        } else {
          // Hòm thư là vật thể, không phải NPC.
          const prop = n.id === 'sq_mailbox' ? await propSprite('city-mailbox', { castShadow: real }) : null;
          sprite = prop ?? new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.4, 0.6), new THREE.MeshBasicMaterial({ color: 0xc9a24a }));
          if (!prop) (sprite as THREE.Mesh).position.y = 0.7;
          root.add(sprite);
        }
        if (n.face === 'left' && sprite instanceof CharacterSprite) sprite.setMotion(false, true);
        if (blob) root.add(blobShadow(0.42));
        root.position.set(n.x + 0.5, 0, n.y + 0.5);
        root.traverse((o) => (o.userData = { ...o.userData, kind: 'npc', id: n.id }));
        this.scene.add(root);
        this.npcs.set(n.id, { root, sprite, label: this.makeLabel(n.name, 'npc') });
      }),
    );

    await Promise.all(map.wild_spawns.map((s) => this.addSpawn(s, blob, real)));
    await Promise.all(
      map.pedestals.map(async (p) => {
        const display = (p as { display?: string }).display;
        if (!display) return;
        const sprite = await PetSprite.create(display, { castShadow: real, scale: 0.95 });
        const root = new THREE.Group();
        root.add(sprite.root);
        const baseY = 0.62;
        root.position.set(p.x + 0.5, baseY, p.y + 0.5);
        root.traverse((o) => (o.userData = { ...o.userData, kind: 'pedestal', index: p.index }));
        this.scene.add(root);
        this.showcases.push({ root, sprite, t: Math.random() * 6, baseY });
      }),
    );
  }

  private async addSpawn(s: WildSpawn, blob: boolean, real: boolean): Promise<void> {
    const sprite = await PetSprite.create(s.species_id, { castShadow: real });
    const root = new THREE.Group();
    root.add(sprite.root);
    if (blob) root.add(blobShadow(0.38));
    root.position.set(s.x + 0.5, 0, s.y + 0.5);
    root.traverse((o) => (o.userData = { ...o.userData, kind: 'spawn', id: s.id }));
    this.scene.add(root);
    this.spawns.set(s.id, { root, sprite, label: null, base: { x: s.x, y: s.y }, t: Math.random() * 10 });
  }

  unloadMap(): void {
    if (this.world) {
      this.scene.remove(this.world.group);
      this.world.dispose();
      this.world = null;
    }
    for (const a of [...this.npcs.values(), ...this.spawns.values()]) {
      this.scene.remove(a.root);
      a.label?.remove();
      a.root.traverse((o) => {
        const m = o as THREE.Mesh;
        if (m.isMesh) {
          m.geometry.dispose();
          (m.material as THREE.Material).dispose();
        }
      });
    }
    this.npcs.clear();
    this.spawns.clear();
    for (const c of this.showcases) {
      this.scene.remove(c.root);
      c.root.traverse((o) => {
        const m = o as THREE.Mesh;
        if (m.isMesh) {
          m.geometry.dispose();
          (m.material as THREE.Material).dispose();
        }
      });
    }
    this.showcases.length = 0;
    textures.unpinAll();
  }

  /** Vị trí hiển thị người chơi (số thực, theo ô) + trạng thái để chọn khung. */
  setPlayer(pos: { x: number; y: number }, moving: boolean, facing: Direction): void {
    this.playerRoot.position.set(pos.x + 0.5, 0, pos.y + 0.5);
    this.player?.setMotion(moving, facing === 'left' ? true : facing === 'right' ? false : undefined, facing === 'up' ? 'up' : facing === 'down' ? 'down' : null);
  }

  setSpawnVisible(id: string, visible: boolean): void {
    const s = this.spawns.get(id);
    if (s) s.root.visible = visible;
  }

  snapCamera(): void {
    this.updateCamera(1);
  }

  /** Chọn đối tượng tại tọa độ màn hình: NPC/quái/bệ/trụ trước, rồi đến ô mặt đất. */
  pick(clientX: number, clientY: number): Pick | null {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const ndc = new THREE.Vector2(((clientX - rect.left) / rect.width) * 2 - 1, -((clientY - rect.top) / rect.height) * 2 + 1);
    this.ray.setFromCamera(ndc, this.camera);
    const objs: THREE.Object3D[] = [];
    for (const a of this.npcs.values()) objs.push(a.root);
    for (const a of this.spawns.values()) if (a.root.visible) objs.push(a.root);
    for (const c of this.showcases) objs.push(c.root);
    if (this.world) objs.push(...this.world.pickables);
    const hits = this.ray.intersectObjects(objs, true);
    for (const h of hits) {
      const u = h.object.userData as { kind?: string; id?: string; index?: number };
      if (u.kind === 'npc' && u.id) return { kind: 'npc', id: u.id };
      if (u.kind === 'spawn' && u.id) return { kind: 'spawn', id: u.id };
      if (u.kind === 'pedestal' && u.index !== undefined) return { kind: 'pedestal', index: u.index };
      if (u.kind === 'pillar') return { kind: 'pillar' };
    }
    const p = new THREE.Vector3();
    if (this.ray.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), p)) return { kind: 'ground', cell: { x: Math.floor(p.x), y: Math.floor(p.z) } };
    return null;
  }

  start(): void {
    const tick = (t: number) => {
      this.raf = requestAnimationFrame(tick);
      const minDt = 1000 / this.cap - 1.5;
      if (this.last && t - this.last < minDt) return;
      const dt = this.last ? Math.min(0.1, (t - this.last) / 1000) : 1 / 60;
      this.frameTimes.push(t - this.last);
      if (this.frameTimes.length > 240) this.frameTimes.shift();
      this.last = t;
      this.frame(dt);
    };
    this.raf = requestAnimationFrame(tick);
  }

  dispose(): void {
    cancelAnimationFrame(this.raf);
    this.unloadMap();
    this.resizeObs.disconnect();
    this.post?.dispose();
    this.renderer.dispose();
    this.renderer.domElement.remove();
    this.labels.remove();
  }

  stats(): { calls: number; triangles: number; textures: number; geometries: number; cacheMB: number } {
    const i = this.renderer.info;
    return { calls: i.render.calls, triangles: i.render.triangles, textures: i.memory.textures, geometries: i.memory.geometries, cacheMB: textures.stats().mb };
  }

  private frame(dt: number): void {
    this.frameCb?.(dt);
    this.player?.update(dt);
    for (const n of this.npcs.values()) if (n.sprite instanceof CharacterSprite) n.sprite.update(dt);
    for (const s of this.spawns.values()) {
      // Quái đi lắc nhẹ quanh điểm của nó (không rời ô: vị trí luật vẫn là điểm cố định).
      s.t += dt;
      const ox = Math.sin(s.t * 0.7) * 0.25;
      s.root.position.x = s.base.x + 0.5 + ox;
      s.sprite.setRow(Math.abs(Math.cos(s.t * 0.7)) > 0.3 ? 'move' : 'idle');
      s.sprite.update(dt, Math.cos(s.t * 0.7) > 0);
    }
    for (const c of this.showcases) {
      // Thần thú lơ lửng nhẹ trên bệ.
      c.t += dt;
      c.root.position.y = c.baseY + Math.sin(c.t * 1.6) * 0.05;
      c.sprite.setRow('idle');
      c.sprite.update(dt, false);
    }
    this.world?.update(dt, this.playerRoot.position);
    this.updateCamera(Math.min(1, dt * 6));
    this.updateLight(dt);
    if (this.post) this.post.render(dt);
    else this.renderer.render(this.scene, this.camera);
    this.updateLabels();
  }

  private updateCamera(k: number): void {
    const map = this.map;
    const p = this.playerRoot.position;
    let tx = p.x;
    let tz = p.z;
    if (map) {
      const W = map.width;
      const H = map.height || map.width;
      const halfW = DIST * Math.tan(THREE.MathUtils.degToRad(FOV / 2)) * this.camera.aspect;
      tx = W <= halfW * 2 ? W / 2 : THREE.MathUtils.clamp(tx, halfW - 0.5, W - halfW + 0.5);
      tz = THREE.MathUtils.clamp(tz, 3, H - 1.5);
    }
    this.target.x += (tx - this.target.x) * k;
    this.target.z += (tz - this.target.z) * k;
    this.target.y = 0.8;
    this.camera.position.set(this.target.x, this.target.y + DIST * Math.sin(PITCH), this.target.z + DIST * Math.cos(PITCH));
    this.camera.lookAt(this.target);
  }

  private makeLabel(text: string, kind: 'npc'): HTMLDivElement {
    const d = document.createElement('div');
    d.textContent = text;
    d.className = `label label-${kind}`;
    d.style.cssText =
      'position:absolute;transform:translate(-50%,-100%);font-size:12px;font-weight:600;color:#fff6dc;white-space:nowrap;text-shadow:0 1px 2px #000,0 0 3px #000;';
    this.labels.appendChild(d);
    return d;
  }

  private updateLabels(): void {
    const w = this.host.clientWidth;
    const h = this.host.clientHeight;
    const v = new THREE.Vector3();
    for (const n of this.npcs.values()) {
      if (!n.label) continue;
      v.set(n.root.position.x, 1.75, n.root.position.z).project(this.camera);
      const on = v.z < 1 && Math.abs(v.x) < 1.1 && Math.abs(v.y) < 1.1;
      n.label.style.display = on ? 'block' : 'none';
      if (on) n.label.style.left = `${((v.x + 1) / 2) * w}px`;
      if (on) n.label.style.top = `${((1 - v.y) / 2) * h}px`;
    }
  }

  private resize(): void {
    const w = this.host.clientWidth || 1;
    const h = this.host.clientHeight || 1;
    const P = PRESETS[this.quality];
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, P.maxPixelRatio) * P.renderScale);
    this.renderer.setSize(w, h, false);
    this.renderer.domElement.style.width = '100%';
    this.renderer.domElement.style.height = '100%';
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.post?.setSize(w, h, this.renderer.getPixelRatio());
  }

  /** Cập nhật ánh sáng theo giờ (mỗi giây một lần): hậu kỳ + đèn/tia nắng trong cảnh. */
  private updateLight(dt: number, force = false): void {
    this.lightClock -= dt;
    if (this.lightClock > 0 && !force) return;
    this.lightClock = 1;
    const l: Light = this.indoor ? INDOOR : lightAt(settings.value.time);
    this.post?.setLight(l);
    this.world?.setLight(l);
    this.light = l;
  }
  /** Ánh sáng hiện tại (cho debug/test). */
  light: Light = INDOOR;
}
