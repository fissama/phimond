/**
 * Đường dẫn asset tĩnh (AD1). Bản build nhúng bảng `đường dẫn logic → tên đã băm` vào index.html
 * (`window.__PHIMOND_ASSETS__`, xem `vite-hash-public.ts`); bản dev không có bảng nên dùng nguyên đường dẫn.
 * Mọi chỗ lấy ảnh/âm thanh/json trong public phải đi qua `assetUrl()` để được cache dài và đổi được sang CDN sau này.
 */
const BASE = import.meta.env.BASE_URL;
const table: Record<string, string> = (globalThis as { __PHIMOND_ASSETS__?: Record<string, string> }).__PHIMOND_ASSETS__ ?? {};
const hashed = Object.keys(table).length > 0;

/** `hd2d/bush-01.png` → `./hd2d/bush-01.3fa9c1d2e4.png` (bản build) hoặc `/hd2d/bush-01.png` (bản dev). */
export function assetUrl(path: string): string {
  return BASE + (table[path] ?? path);
}

/** Bản build: asset có thật trong gói không (để khỏi thử tải file không tồn tại). Bản dev: luôn true. */
export function hasAsset(path: string): boolean {
  return !hashed || path in table;
}

/** Tên gốc của một URL đã băm (`x.3fa9c1d2e4.png` → `x.png`); URL chưa băm trả nguyên. */
export function unhashedUrl(url: string): string {
  return url.replace(/\.[0-9a-f]{10}(\.[a-z0-9]+)$/i, '$1');
}

/**
 * fetch asset json theo đường dẫn logic. Nếu bản băm không còn (vừa rollout bản mới trong lúc đang chơi bản cũ)
 * thì thử lại tên gốc.
 */
export async function fetchAsset(path: string): Promise<Response> {
  const url = assetUrl(path);
  const r = await fetch(url).catch(() => null);
  if (r?.ok || url === unhashedUrl(url)) return r ?? fetch(url);
  return fetch(unhashedUrl(url));
}

/** Đang chạy bản build (có bảng tên đã băm). Bản dev: false. */
export function isBuild(): boolean {
  return hashed;
}
