import * as THREE from 'three';
import { asset, hd2dUrl, petArt, petAtlas, petUrl, textures, type AssetInfo } from './assets.ts';

export const PPU = 128; // px mỗi đơn vị world (nền xa 64)
/** Góc nghiêng sprite theo camera (đứng nghiêng như HD-2D để không bị dẹt khi nhìn chéo xuống). */
export const SPRITE_TILT = -0.42;

export interface SpriteOpts {
  tint?: THREE.ColorRepresentation;
  castShadow?: boolean;
  ppu?: number;
  tilt?: number;
}

/** Plane có gốc ở pivot (đáy-giữa với prop/nhân vật), dựng đứng và nghiêng theo camera. */
export function spriteGeometry(wPx: number, hPx: number, pivot: [number, number], ppu = PPU): THREE.PlaneGeometry {
  const w = wPx / ppu;
  const h = hPx / ppu;
  const g = new THREE.PlaneGeometry(w, h);
  g.translate(w / 2 - pivot[0] / ppu, -h / 2 + pivot[1] / ppu, 0);
  return g;
}

export function spriteMaterial(tex: THREE.Texture, opts: SpriteOpts = {}): THREE.MeshBasicMaterial {
  return new THREE.MeshBasicMaterial({ map: tex, alphaTest: 0.5, color: opts.tint ?? 0xffffff });
}

/** Cho phép sprite đổ bóng thật theo hình (alpha) ở mức Cao. */
export function enableShadow(mesh: THREE.Mesh, tex: THREE.Texture): void {
  mesh.castShadow = true;
  mesh.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: tex, alphaTest: 0.5 });
}

/** Sprite tĩnh từ một asset HD-2D. Trả null nếu asset không có. */
export async function propSprite(id: string, opts: SpriteOpts = {}): Promise<THREE.Mesh | null> {
  const a = asset(id);
  if (!a) return null;
  const base = await textures.get(hd2dUrl(id));
  const frames = Math.max(1, a.frames || 1);
  const tex = frames > 1 ? base.clone() : base;
  const fw = a.px[0] / frames;
  if (frames > 1) {
    tex.repeat.set(1 / frames, 1);
    tex.needsUpdate = true;
  }
  const pivot: [number, number] = frames > 1 ? [fw / 2, a.pivot_px[1]] : a.pivot_px;
  const mesh = new THREE.Mesh(spriteGeometry(fw, a.px[1], pivot, opts.ppu), spriteMaterial(tex, opts));
  mesh.rotation.x = opts.tilt ?? SPRITE_TILT;
  if (opts.castShadow) enableShadow(mesh, tex);
  if (frames > 1) mesh.userData.anim = { tex, frames, fps: a.fps ?? 8, t: Math.random() };
  return mesh;
}

/** Bước khung hình cho sprite có nhiều khung (gọi mỗi frame). */
export function animate(mesh: THREE.Object3D, dt: number): void {
  const anim = mesh.userData.anim as { tex: THREE.Texture; frames: number; fps: number; t: number } | undefined;
  if (!anim) return;
  anim.t += dt;
  const f = Math.floor(anim.t * anim.fps) % anim.frames;
  anim.tex.offset.x = f / anim.frames;
}

/**
 * Nhân vật (người chơi/NPC) có dải khung idle/run 192×192. Thiếu dải thì dùng ảnh tĩnh.
 * Hướng: dải ngang nhìn sang phải (lật khi đi trái); dải xuống/lên (nếu có) dùng khi đi dọc. Thiếu dải dọc → dùng dải ngang.
 */
export class CharacterSprite {
  readonly root = new THREE.Group();
  private mesh: THREE.Mesh | null = null;
  private strips: Partial<Record<'idle' | 'run' | 'runDown' | 'runUp' | 'still', { tex: THREE.Texture; frames: number }>> = {};
  private mode: 'idle' | 'run' | 'runDown' | 'runUp' = 'idle';
  private t = Math.random();
  private flip = false;
  private vertical = false;
  private ghost: THREE.Mesh | null = null;
  /** Tốc độ khung khi chạy/đi (người đi đường đi chậm dùng số nhỏ). */
  runFps = 12;

  static async create(id: string, opts: SpriteOpts = {}): Promise<CharacterSprite> {
    const s = new CharacterSprite();
    const a = asset(id);
    const load = async (key: 'idle' | 'run' | 'runDown' | 'runUp', kind: 'idle' | 'run' | 'run-down' | 'run-up', frames?: number) => {
      if (!frames) return;
      const t = (await textures.get(hd2dUrl(id, kind))).clone();
      t.repeat.set(1 / frames, 1);
      t.needsUpdate = true;
      s.strips[key] = { tex: t, frames };
    };
    if (a) {
      await Promise.all([
        load('idle', 'idle', a.idle_frames),
        load('run', 'run', a.run_frames),
        load('runDown', 'run-down', a.run_down_frames),
        load('runUp', 'run-up', a.run_up_frames),
      ]);
      if (!s.strips.idle) s.strips.still = { tex: await textures.get(hd2dUrl(id)), frames: 1 };
    }
    const first = s.strips.idle ?? s.strips.still;
    const geo = spriteGeometry(192, 192, [96, 184]);
    const mat = first ? spriteMaterial(first.tex, opts) : new THREE.MeshBasicMaterial({ color: 0x3355cc });
    s.mesh = new THREE.Mesh(geo, mat);
    s.mesh.rotation.x = opts.tilt ?? SPRITE_TILT;
    if (opts.castShadow && first) enableShadow(s.mesh, first.tex);
    s.root.add(s.mesh);
    return s;
  }

  /**
   * Bóng xuyên vật cản: bản sao mờ xanh chỉ vẽ ở chỗ bị cây/nhà che (depthFunc Greater), để người chơi không bao giờ
   * mất dấu nhân vật sau tán cây (đánh giá v1.0.0).
   */
  enableSilhouette(): void {
    if (!this.mesh || this.ghost) return;
    const src = this.mesh.material as THREE.MeshBasicMaterial;
    const mat = new THREE.MeshBasicMaterial({ map: src.map, transparent: true, opacity: 0.45, color: 0x8fd6ff, alphaTest: 0.3, depthWrite: false, depthFunc: THREE.GreaterDepth });
    this.ghost = new THREE.Mesh(this.mesh.geometry, mat);
    this.ghost.rotation.copy(this.mesh.rotation);
    this.ghost.renderOrder = 20;
    this.root.add(this.ghost);
  }

  /** `vertical`: đang đi lên/xuống (dùng dải dọc nếu có). `faceLeft` chỉ cập nhật khi đi ngang. */
  setMotion(running: boolean, faceLeft?: boolean, vertical?: 'up' | 'down' | null): void {
    if (faceLeft !== undefined) this.flip = faceLeft;
    const v = vertical === 'down' ? this.strips.runDown && 'runDown' : vertical === 'up' ? this.strips.runUp && 'runUp' : null;
    this.vertical = !!v;
    this.mode = running ? (v || (this.strips.run ? 'run' : 'idle')) : 'idle';
  }

  update(dt: number): void {
    if (!this.mesh) return;
    this.t += dt;
    const strip = this.strips[this.mode] ?? this.strips.idle ?? this.strips.still;
    if (!strip) return;
    const mat = this.mesh.material as THREE.MeshBasicMaterial;
    if (mat.map !== strip.tex) {
      mat.map = strip.tex;
      mat.needsUpdate = true;
      if (this.mesh.customDepthMaterial) (this.mesh.customDepthMaterial as THREE.MeshDepthMaterial).map = strip.tex;
    }
    const fps = this.mode === 'idle' ? 6 : this.runFps;
    strip.tex.offset.x = (Math.floor(this.t * fps) % strip.frames) / strip.frames;
    this.mesh.scale.x = this.flip && !this.vertical ? -1 : 1;
    if (this.ghost) {
      const gm = this.ghost.material as THREE.MeshBasicMaterial;
      if (gm.map !== strip.tex) {
        gm.map = strip.tex;
        gm.needsUpdate = true;
      }
      this.ghost.scale.x = this.mesh.scale.x;
    }
  }
}

/** Linh thú từ atlas P10: ô `cell`, hàng idle/move/attack/cast/down, 4 khung mỗi hàng. */
export class PetSprite {
  readonly root = new THREE.Group();
  private mesh: THREE.Mesh | null = null;
  private tex: THREE.Texture | null = null;
  private row = 0;
  private t = Math.random();
  scale = 0.62;

  static async create(speciesId: string, opts: SpriteOpts & { scale?: number } = {}): Promise<PetSprite> {
    const s = new PetSprite();
    if (opts.scale) s.scale = opts.scale;
    const atlas = petAtlas();
    const art = petArt(speciesId);
    if (!atlas || !art) return s;
    const tex = (await textures.get(petUrl(art.file))).clone();
    tex.repeat.set(1 / atlas.cols, 1 / atlas.rows);
    tex.needsUpdate = true;
    s.tex = tex;
    const feet = art.feet[0]?.[0] ?? 40;
    const geo = spriteGeometry(atlas.cell, atlas.cell, [atlas.cell / 2, atlas.cell - feet], PPU / s.scale);
    s.mesh = new THREE.Mesh(geo, spriteMaterial(tex, opts));
    s.mesh.rotation.x = opts.tilt ?? SPRITE_TILT;
    if (opts.castShadow) enableShadow(s.mesh, tex);
    s.root.add(s.mesh);
    return s;
  }

  setRow(name: 'idle' | 'move' | 'attack' | 'cast' | 'down'): void {
    const atlas = petAtlas();
    this.row = Math.max(0, atlas?.rowNames.indexOf(name) ?? 0);
  }

  update(dt: number, flip = false): void {
    const atlas = petAtlas();
    if (!this.tex || !atlas || !this.mesh) return;
    this.t += dt;
    const col = Math.floor(this.t * 6) % atlas.cols;
    this.tex.offset.set(col / atlas.cols, 1 - (this.row + 1) / atlas.rows);
    this.mesh.scale.x = flip ? -1 : 1;
  }
}

let blobTex: THREE.Texture | null = null;
/** Bóng tròn mờ dưới chân (mức Trung bình; mức Cao dùng bóng thật). */
export function blobShadow(radius: number): THREE.Mesh {
  if (!blobTex) {
    const c = document.createElement('canvas');
    c.width = c.height = 64;
    const g = c.getContext('2d')!;
    const grad = g.createRadialGradient(32, 32, 2, 32, 32, 31);
    grad.addColorStop(0, 'rgba(0,0,0,0.45)');
    grad.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, 64, 64);
    blobTex = new THREE.CanvasTexture(c);
  }
  const m = new THREE.Mesh(
    new THREE.PlaneGeometry(radius * 2, radius * 1.2),
    new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false }),
  );
  m.rotation.x = -Math.PI / 2;
  m.position.y = 0.02;
  m.renderOrder = 1;
  return m;
}

export type { AssetInfo };

let ringTex: THREE.CanvasTexture | null = null;
/** Vòng cảnh báo dưới chân quái hoang (đỏ cam, viền đứt), nằm sát mặt đất. */
export function foeRing(): THREE.Mesh {
  if (!ringTex) {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const g = c.getContext('2d')!;
    g.strokeStyle = 'rgba(255,96,64,0.95)';
    g.lineWidth = 7;
    g.setLineDash([16, 10]);
    g.beginPath();
    g.arc(64, 64, 52, 0, Math.PI * 2);
    g.stroke();
    const grad = g.createRadialGradient(64, 64, 10, 64, 64, 56);
    grad.addColorStop(0, 'rgba(255,80,50,0.0)');
    grad.addColorStop(1, 'rgba(255,80,50,0.28)');
    g.fillStyle = grad;
    g.beginPath();
    g.arc(64, 64, 52, 0, Math.PI * 2);
    g.fill();
    ringTex = new THREE.CanvasTexture(c);
  }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.95), new THREE.MeshBasicMaterial({ map: ringTex, transparent: true, depthWrite: false, opacity: 0.6 }));
  m.rotation.x = -Math.PI / 2;
  m.position.y = 0.015;
  m.renderOrder = 1;
  return m;
}
