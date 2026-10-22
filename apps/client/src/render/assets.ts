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
  provisional?: boolean;
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
export const hd2dUrl = (id: string, kind?: 'idle' | 'run') => `${BASE}hd2d/${id}${kind ? '.' + kind : ''}.png`;
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
  const sid = pets.legacy[speciesId]?.species ?? Object.keys(pets.species)[0];
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

  evict(): void {
    let total = [...this.entries.values()].reduce((s, e) => s + e.bytes, 0);
    if (total <= this.budget) return;
    const order = [...this.entries.entries()].filter(([, e]) => !e.pinned).sort((a, b) => a[1].used - b[1].used);
    for (const [k, e] of order) {
      if (total <= this.budget) break;
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

/** Nạp sẵn ảnh (vào cache HTTP của trình duyệt) cho map kề cổng, không giải mã thành texture. */
export function prefetch(urls: string[]): void {
  for (const u of urls) {
    const img = new Image();
    img.decoding = 'async';
    img.src = u;
  }
}
