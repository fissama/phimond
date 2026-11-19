import * as THREE from 'three';
import { assetUrl, fetchAsset, hasAsset, isBuild, unhashedUrl } from '../assetUrl.ts';

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

/** URL → id ảnh hd2d (`bush-01`, `npc-lio.idle`), để cache texture tra atlas (AD3). */
const hd2dIds = new Map<string, string>();
export const hd2dUrl = (id: string, kind?: 'idle' | 'run' | 'run-down' | 'run-up') => {
  const key = `${id}${kind ? '.' + kind : ''}`;
  const url = assetUrl(`hd2d/${key}.png`);
  hd2dIds.set(url, key);
  return url;
};
export const petUrl = (file: string) => assetUrl(`pets/${file}`);

let manifest: Record<string, AssetInfo> = {};
let pets: PetAtlas | null = null;

/** Atlas do bản build sinh (`vite-atlas.ts`); bản dev không có → mọi ảnh tải lẻ. */
export interface AtlasJson {
  pages: { file: string; w: number; h: number }[];
  sprites: Record<string, [number, number, number, number, number]>;
  maps: Record<string, number[]>;
}
let atlas: AtlasJson | null = null;
export function atlasInfo(): AtlasJson | null {
  return atlas;
}
/** URL các trang atlas mà một map dùng ở một preset (nạp sẵn map kề). */
export function atlasPageUrls(mapId: string, quality: string): string[] {
  return (atlas?.maps[`${mapId}@${quality}`] ?? []).map((i) => assetUrl(atlas!.pages[i]!.file));
}

export async function loadManifests(): Promise<void> {
  const [a, p, at] = await Promise.all([
    fetchAsset('hd2d/assets.json').then((r) => (r.ok ? r.json() : {})),
    fetchAsset('pets/manifest.json').then((r) => (r.ok ? r.json() : null)),
    // Chỉ bản build có atlas.json (có trong bảng tên đã băm); bản dev bỏ qua để không ăn trang index.html thay json.
    hasAsset('hd2d/atlas.json') && isBuild() ? fetchAsset('hd2d/atlas.json').then((r) => (r.ok ? r.json() : null)).catch(() => null) : null,
  ]);
  manifest = a as Record<string, AssetInfo>;
  pets = p as PetAtlas | null;
  atlas = at as AtlasJson | null;
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

/** Vùng UV của một ảnh trong texture (atlas: ô con; ảnh lẻ: cả ảnh). Gốc UV ở dưới-trái như three.js. */
export interface UvRect {
  u: number;
  v: number;
  w: number;
  h: number;
}
const FULL: UvRect = { u: 0, v: 0, w: 1, h: 1 };
export function uvRect(t: THREE.Texture): UvRect {
  return (t.userData.rect as UvRect | undefined) ?? FULL;
}
/**
 * Chọn khung `f` trong dải `frames` khung xếp ngang (sprite động, dải idle/run). Đúng cho cả ảnh lẻ và ô atlas.
 * Thay cho `tex.repeat.set(1 / frames, 1)` + `tex.offset.x = f / frames`.
 */
export function setFrame(t: THREE.Texture, f: number, frames: number): void {
  const r = uvRect(t);
  t.repeat.set(r.w / frames, r.h);
  t.offset.set(r.u + (r.w * f) / frames, r.v);
}

type Entry = {
  tex: Promise<THREE.Texture>;
  /** Byte ước tính trên GPU (0 với "view" atlas: byte tính ở trang). */
  bytes: number;
  used: number;
  pinned: boolean;
  /** View atlas: khóa trang chứa nó. */
  page?: string;
};

/**
 * Bộ nhớ đệm texture có giới hạn (P01-R08): đếm byte ước tính (w×h×4), bỏ texture ít dùng nhất
 * khi vượt budget, trừ texture đang được cảnh hiện tại giữ (`pin`).
 * AD3: ảnh nằm trong atlas trả về một "view" (bản sao texture của trang, offset/repeat trỏ đúng ô); các view chung một ảnh
 * trên GPU. Trang chỉ bị đẩy khi không còn view nào của nó đang được giữ.
 */
class TextureCache {
  private readonly loader = new THREE.TextureLoader();
  private readonly entries = new Map<string, Entry>();
  budget = 160 * 1024 * 1024;
  private tick = 0;

  get(url: string, opts: { repeat?: boolean } = {}): Promise<THREE.Texture> {
    const id = opts.repeat ? undefined : hd2dIds.get(url);
    const cell = id && atlas?.sprites[id];
    if (cell) return this.view(id!, cell);
    return this.load(url + (opts.repeat ? '#r' : ''), url, opts);
  }

  private load(k: string, url: string, opts: { repeat?: boolean }): Promise<THREE.Texture> {
    const hit = this.entries.get(k);
    if (hit) {
      hit.used = ++this.tick;
      hit.pinned = true;
      return hit.tex;
    }
    const e: Entry = { tex: Promise.resolve(null as unknown as THREE.Texture), bytes: 0, used: ++this.tick, pinned: true };
    // Bản băm không còn (bản mới vừa rollout) → lùi về tên gốc thay vì để trống texture.
    const load = this.loader.loadAsync(url).catch((err: unknown) => (unhashedUrl(url) !== url ? this.loader.loadAsync(unhashedUrl(url)) : Promise.reject(err)));
    e.tex = load.then((t) => {
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

  private view(id: string, [pi, x, y, w, h]: [number, number, number, number, number]): Promise<THREE.Texture> {
    const pg = atlas!.pages[pi]!;
    const pageUrl = assetUrl(pg.file);
    const pageKey = pageUrl + '#atlas';
    const k = `view:${id}`;
    const page = this.load(pageKey, pageUrl, {}); // ghim trang mỗi lần lấy view
    const hit = this.entries.get(k);
    if (hit) {
      hit.used = ++this.tick;
      hit.pinned = true;
      return hit.tex;
    }
    const e: Entry = { tex: Promise.resolve(null as unknown as THREE.Texture), bytes: 0, used: ++this.tick, pinned: true, page: pageKey };
    e.tex = page.then((t) => {
      const v = t.clone();
      const rect: UvRect = { u: x / pg.w, v: 1 - (y + h) / pg.h, w: w / pg.w, h: h / pg.h };
      v.userData = { rect, atlasId: id };
      v.offset.set(rect.u, rect.v);
      v.repeat.set(rect.w, rect.h);
      return v;
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
    // Trang atlas còn view đang giữ thì cũng đang được giữ.
    const held = new Set<string>();
    for (const e of this.entries.values()) if (e.page && e.pinned) held.add(e.page);
    const order = [...this.entries.entries()]
      .filter(([k, e]) => !e.pinned && !e.page && !held.has(k))
      .sort((a, b) => a[1].used - b[1].used);
    for (const [k, e] of order) {
      if (total <= limit) break;
      this.entries.delete(k);
      total -= e.bytes;
      // Đẩy trang thì đẩy luôn mọi view của nó.
      for (const [vk, ve] of [...this.entries.entries()]) {
        if (ve.page !== k) continue;
        this.entries.delete(vk);
        void ve.tex.then((t) => t.dispose());
      }
      void e.tex.then((t) => t.dispose());
    }
  }

  stats(): { count: number; mb: number } {
    const bytes = [...this.entries.values()].reduce((s, e) => s + e.bytes, 0);
    return { count: [...this.entries.values()].filter((e) => e.bytes > 0).length, mb: Math.round(bytes / 1048576) };
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

const prefetched = new Set<string>();
/**
 * Nạp sẵn ảnh (vào cache HTTP của trình duyệt) cho map kề cổng, không giải mã thành texture (AD5): chạy lúc rảnh,
 * tối đa 3 ảnh cùng lúc để không tranh băng thông với map đang chơi; bỏ qua khi người dùng bật tiết kiệm dữ liệu.
 */
export function prefetch(urls: string[]): void {
  const nav = navigator as Navigator & { connection?: { saveData?: boolean; effectiveType?: string } };
  if (nav.connection?.saveData || /(^|-)2g$/.test(nav.connection?.effectiveType ?? '')) return;
  const queue = urls.filter((u) => !prefetched.has(u));
  queue.forEach((u) => prefetched.add(u));
  const idle = (cb: () => void) => ((window as Window & { requestIdleCallback?: (f: () => void) => void }).requestIdleCallback ?? ((f: () => void) => setTimeout(f, 200)))(cb);
  const next = () => {
    const u = queue.shift();
    if (!u) return;
    const img = new Image();
    img.decoding = 'async';
    img.onload = img.onerror = () => idle(next);
    img.src = u;
  };
  idle(() => {
    for (let i = 0; i < 3; i++) next();
  });
}
