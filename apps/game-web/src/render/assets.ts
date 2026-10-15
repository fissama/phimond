import * as THREE from 'three';

const loader = new THREE.TextureLoader();
const cache = new Map<string, Promise<THREE.Texture>>();
const BASE = import.meta.env.BASE_URL.replace(/\/?$/, '/');
export const assetUrl = (p: string): string => `${BASE}${p.replace(/^\//, '')}`;

export interface TexOpts { mip?: boolean; repeat?: boolean; aniso?: number; premult?: boolean }

/** Nạp texture pixel-art: nearest khi phóng to; mipmap khi thu nhỏ (tránh nhấp nháy trên iPhone). */
export function loadTexture(path: string, o: TexOpts = {}): Promise<THREE.Texture> {
  const key = `${path}|${o.mip ? 1 : 0}|${o.repeat ? 1 : 0}|${o.premult === false ? 0 : 1}`;
  let p = cache.get(key);
  if (!p) {
    p = new Promise<THREE.Texture>((resolve, reject) => {
      loader.load(assetUrl(path), (t) => {
        t.colorSpace = THREE.SRGBColorSpace;
        t.magFilter = THREE.NearestFilter;
        t.minFilter = o.mip === false ? THREE.NearestFilter : THREE.LinearMipmapLinearFilter;
        t.generateMipmaps = o.mip !== false;
        t.anisotropy = o.aniso ?? 4;
        t.premultiplyAlpha = o.premult !== false;
        if (o.repeat) t.wrapS = t.wrapT = THREE.RepeatWrapping;
        else t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
        t.needsUpdate = true;
        resolve(t);
      }, undefined, () => reject(new Error(`Không tải được ${path}`)));
    });
    cache.set(key, p);
  }
  return p;
}

export function textureBytes(): number {
  return cache.size;
}
export function disposeAllTextures(): void {
  for (const p of cache.values()) void p.then((t) => t.dispose());
  cache.clear();
}

export async function loadJson<T>(path: string): Promise<T> {
  const r = await fetch(assetUrl(path));
  if (!r.ok) throw new Error(`Không tải được ${path} (${r.status})`);
  return (await r.json()) as T;
}
