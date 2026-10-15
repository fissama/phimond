import { signal } from '@preact/signals';
import type { Catalog } from '@phimond/protocol';

export type Lang = 'vi' | 'en';
const KEY = 'phimond.lang';
function read(): Lang { try { return localStorage.getItem(KEY) === 'en' ? 'en' : 'vi'; } catch { return 'vi'; } }
/** Ngôn ngữ tên hiển thị của nội dung (loài, bản đồ, NPC, vật phẩm...). Mặc định tiếng Việt. */
export const lang = signal<Lang>(read());
export function setLang(l: Lang): void {
  try { localStorage.setItem(KEY, l); } catch { /* ignore */ }
  lang.value = l; location.reload(); // tên được cache trong cảnh/menu -> nạp lại cho nhất quán
}

type Dict = Record<string, Record<string, string | { name: string; description?: string }>>;
async function loadDict(): Promise<Dict | null> {
  try { const r = await fetch(new URL('assets/i18n/vi.json', document.baseURI)); return r.ok ? ((await r.json()) as Dict) : null; } catch { return null; }
}

const rev = new Map<string, string>();
/** Dịch một tên gốc của server (dùng cho tin nhắn sự kiện chỉ mang chuỗi tên). */
export function tn(name: string): string { return rev.get(name) ?? name; }

/** Thay tên/mô tả trong catalog bằng bản dịch (id nào thiếu thì giữ tên của server). */
export async function localizeCatalog(cat: Catalog): Promise<Catalog> {
  if (lang.value !== 'vi') return cat;
  const d = await loadDict(); if (!d) return cat;
  const out = { ...cat } as Record<string, Record<string, Record<string, unknown>>>;
  for (const kind of ['species', 'maps', 'npcs', 'items', 'skills', 'statuses', 'quests', 'recipes']) {
    const src = (cat as Record<string, Record<string, Record<string, unknown>>>)[kind]; const tr = d[kind]; if (!src || !tr) continue;
    const next: Record<string, Record<string, unknown>> = {};
    for (const [id, v] of Object.entries(src)) {
      const t = tr[id]; if (t && typeof v.name === 'string') rev.set(v.name, typeof t === 'string' ? t : t.name);
      next[id] = !t ? v : typeof t === 'string' ? { ...v, name: t } : { ...v, name: t.name, ...(t.description ? { description: t.description } : {}) };
    }
    out[kind] = next;
  }
  return out as unknown as Catalog;
}
