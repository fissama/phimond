import * as THREE from 'three';

export interface AssetInfo {
  category: string;
  px: [number, number];
  pivot_px: [number, number];
  frames: number;
  fps?: number | null;
  sway?: boolean;
  world?: [number, number];
  tileable?: string | null;
  idle_frames?: number;
  run_frames?: number;
  /** Dải đi bộ hướng xuống/lên (khung nhìn thẳng vào/ra khỏi màn hình). Thiếu → dùng dải ngang. */
  run_down_frames?: number;
  run_up_frames?: number;
  provisional?: boolean;
  /** Đơn 10: động vật/đồ tĩnh được engine làm động nhẹ. */
  breathe?: boolean;
  flutter?: boolean;
}

export interface PetAtlas {
  cell: number;
  cols: number;
  rows: number;
  rowNames: string[];
  species: Record<string, { file: string; small: string; feet: number[][]; width: number[][]; height: number[][] }>;
  legacy: Record<string, { species: string; artPending?: boolean }>;
}

const BASE = import.meta.env.BASE_URL;
export const hd2dUrl = (id: string, kind?: 'idle' | 'run' | 'run-down' | 'run-up') => `${BASE}hd2d/${id}${kind ? '.' + kind : ''}.png`;
export const petUrl = (file: string) => `${BASE}pets/${file}`;

let manifest: Record<string, AssetInfo> = {};
let pets: PetAtlas | null = null;

export async function loadManifests(): Promise<void> {
  const [a, p] = await Promise.all([
    fetch(`${BASE}hd2d/assets.json`).then((r) => (r.ok ? r.json() : {})),
    fetch(`${BASE}pets/manifest.json`).then((r) => (r.ok ? r.json() : null)),
  ]);
  manifest = a as Record<string, AssetInfo>;
  pets = p as PetAtlas | null;
}

export function asset(id: string): AssetInfo | undefined {
  return manifest[id];
}
export function petAtlas(): PetAtlas | null {
  return pets;
}
/** Atlas hiển thị cho một loài server (14 loài cũ → atlas P10, nợ N02). */
export function petArt(speciesId: string) {
  if (!pets) return null;
  // Id chuẩn P10 (species_NNNN) tra thẳng; id loài cũ (save trước P11) qua bảng legacy.
  const sid = pets.species[speciesId] ? speciesId : (pets.legacy[speciesId]?.species ?? Object.keys(pets.species)[0]);
  return sid ? { id: sid, ...pets.species[sid]! } : null;
}

/**
 * Bộ nhớ đệm texture có giới hạn (P01-R08): đếm byte ước tính (w×h×4), bỏ texture ít dùng nhất
 * khi vượt budget, trừ texture đang được cảnh hiện tại giữ (`pin`).
 */
class TextureCache {
  private readonly loader = new THREE.TextureLoader();
  private readonly entries = new Map<string, { tex: Promise<THREE.Texture>; bytes: number; used: number; pinned: boolean }>();
  budget = 160 * 1024 * 1024;
  private tick = 0;

  get(url: string, opts: { repeat?: boolean } = {}): Promise<THREE.Texture> {
    const k = url + (opts.repeat ? '#r' : '');
    const hit = this.entries.get(k);
    if (hit) {
      hit.used = ++this.tick;
      hit.pinned = true;
      return hit.tex;
    }
    const e = { tex: Promise.resolve(null as unknown as THREE.Texture), bytes: 0, used: ++this.tick, pinned: true };
    e.tex = this.loader.loadAsync(url).then((t) => {
      t.colorSpace = THREE.SRGBColorSpace;
      t.magFilter = THREE.NearestFilter;
      t.minFilter = opts.repeat ? THREE.NearestMipmapLinearFilter : THREE.LinearFilter;
      t.generateMipmaps = !!opts.repeat;
      if (opts.repeat) t.wrapS = t.wrapT = THREE.RepeatWrapping;
      const img = t.image as { width: number; height: number };
      e.bytes = img.width * img.height * 4 * (opts.repeat ? 1.33 : 1);
      this.evict();
      return t;
    });
    this.entries.set(k, e);
    return e.tex;
  }

  /** Bỏ đánh dấu đang dùng (khi rời map); texture vẫn trong cache tới khi bị đẩy ra. */
  unpinAll(): void {
    for (const e of this.entries.values()) e.pinned = false;
  }

  /**
   * Sau khi vào map mới (AD2): đẩy texture của map cũ ra tới khi còn ≤ `ratio` × budget, thay vì giữ tới khi tràn budget.
   * Texture bị đẩy vẫn còn trong cache HTTP nên quay lại map cũ chỉ tốn thời gian giải mã, không tải lại qua mạng.
   */
  trim(ratio = 0.5): void {
    this.evict(this.budget * ratio);
  }

  evict(limit = this.budget): void {
    let total = [...this.entries.values()].reduce((s, e) => s + e.bytes, 0);
    if (total <= limit) return;
    const order = [...this.entries.entries()].filter(([, e]) => !e.pinned).sort((a, b) => a[1].used - b[1].used);
    for (const [k, e] of order) {
      if (total <= limit) break;
      this.entries.delete(k);
      total -= e.bytes;
      void e.tex.then((t) => t.dispose());
    }
  }

  stats(): { count: number; mb: number } {
    const bytes = [...this.entries.values()].reduce((s, e) => s + e.bytes, 0);
    return { count: this.entries.size, mb: Math.round(bytes / 1048576) };
  }
}

export const textures = new TextureCache();

/**
 * Bản sao texture dùng riêng một mesh (để đổi offset/repeat khung hình mà không ảnh hưởng texture gốc trong cache).
 * Bản sao giữ ảnh gốc trên GPU tới khi chính nó bị dispose, nên phải được `disposeTree` giải phóng khi rời map (AD2).
 */
export function ownedClone(base: THREE.Texture): THREE.Texture {
  const t = base.clone();
  t.userData.owned = true;
  return t;
}

function disposeOwned(t: unknown): void {
  const tex = t as THREE.Texture | null | undefined;
  if (tex && (tex as THREE.Texture).isTexture && tex.userData.owned) tex.dispose();
}

/**
 * Giải phóng một cây đối tượng: geometry, material, texture riêng (`ownedClone`) gắn trên material hoặc khai báo trong
 * `userData.ownedTextures` (dải khung không đang gắn vào material). Texture gốc của cache không bị đụng tới.
 */
export function disposeTree(root: THREE.Object3D): void {
  root.traverse((o) => {
    const m = o as THREE.Mesh;
    (o.userData.ownedTextures as THREE.Texture[] | undefined)?.forEach(disposeOwned);
    if (!m.isMesh && !(o as THREE.Points).isPoints && !(o as THREE.Sprite).isSprite) return;
    m.geometry?.dispose();
    const mats = Array.isArray(m.material) ? m.material : [m.material];
    for (const mat of [...mats, m.customDepthMaterial as THREE.Material | undefined]) {
      if (!mat) continue;
      disposeOwned((mat as THREE.MeshBasicMaterial).map);
      mat.dispose();
    }
  });
}

/** Nạp sẵn ảnh (vào cache HTTP của trình duyệt) cho map kề cổng, không giải mã thành texture. */
export function prefetch(urls: string[]): void {
  for (const u of urls) {
    const img = new Image();
    img.decoding = 'async';
    img.src = u;
  }
}
