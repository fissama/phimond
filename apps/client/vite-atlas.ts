import { existsSync, readdirSync, readFileSync, statSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import sharp from 'sharp';

/**
 * AD3/AD4 — bước build gói atlas và đổi ảnh sang WebP (chạy trong `vite-hash-public.ts`, trước khi băm tên).
 *
 * Atlas: ảnh hd2d (không lặp) được gom theo **tập map dùng nó** (`atlas-groups.json`, sinh bởi
 * `tests/e2e/atlas-usage.spec.ts`): ảnh chỉ một map dùng nằm trong trang của map đó; ảnh nhiều map cùng dùng nằm trong
 * trang chung đúng của các map ấy. Vì vậy một map chỉ tải trang chứa đúng ảnh nó dùng (không tải thừa, không lặp ảnh).
 * Mỗi ảnh được kéo dài mép 2 px (extrude) để lọc Linear khi thu nhỏ không lem màu ảnh bên cạnh.
 *
 * WebP: mọi PNG trong public được thêm bản WebP **lossless** (pixel y hệt) nếu nhỏ hơn; bảng tên trỏ đường dẫn logic `.png`
 * sang bản WebP. PNG gốc vẫn giữ để client bản cũ lùi về.
 */
export const ATLAS_MAX = 2048;
export const ATLAS_PAD = 2;

export interface PackItem {
  id: string;
  w: number;
  h: number;
}
export interface Placed extends PackItem {
  page: number;
  x: number;
  y: number;
}

/**
 * Xếp kiểu skyline bottom-left: sắp ảnh theo chiều cao rồi chiều rộng giảm dần; mỗi ảnh đặt ở vị trí có đáy thấp nhất
 * trên "đường chân trời" hiện tại (hòa thì lấy bên trái). Trang đầy (vượt `max`) thì sang trang mới.
 * Hiệu suất ~85–90% (xếp kệ đơn giản chỉ ~75%). `x, y` là góc ảnh (không tính viền); mỗi ô chiếm thêm `pad` mỗi phía.
 * Trả kích thước thật từng trang (cắt vừa).
 */
export function packShelves(items: PackItem[], max = ATLAS_MAX, pad = ATLAS_PAD, maxH = max): { placed: Placed[]; pages: { w: number; h: number }[] } {
  const sorted = [...items].sort((a, b) => b.h - a.h || b.w - a.w || a.id.localeCompare(b.id));
  const placed: Placed[] = [];
  const pages: { w: number; h: number }[] = [];
  let sky: { x: number; y: number; w: number }[] = [];
  const newPage = () => {
    pages.push({ w: 0, h: 0 });
    sky = [{ x: 0, y: 0, w: max }];
  };
  /** Đáy (y) nếu đặt ô rộng cw bắt đầu ở đoạn i; null nếu tràn chiều ngang. */
  const fit = (i: number, cw: number): number | null => {
    const x = sky[i]!.x;
    if (x + cw > max) return null;
    let y = 0;
    let left = cw;
    for (let j = i; left > 0; j++) {
      const seg = sky[j];
      if (!seg) return null;
      y = Math.max(y, seg.y);
      left -= seg.w;
    }
    return y;
  };
  const place = (i: number, cw: number, ch: number, y: number) => {
    const x = sky[i]!.x;
    const seg = { x, y: y + ch, w: cw };
    // Cắt các đoạn bị ô mới che.
    const rest: typeof sky = [];
    for (const s of sky) {
      const e = s.x + s.w;
      if (e <= x || s.x >= x + cw) rest.push(s);
      else {
        if (s.x < x) rest.push({ x: s.x, y: s.y, w: x - s.x });
        if (e > x + cw) rest.push({ x: x + cw, y: s.y, w: e - (x + cw) });
      }
    }
    rest.push(seg);
    rest.sort((a, b) => a.x - b.x);
    // Gộp đoạn kề cùng độ cao.
    sky = [];
    for (const s of rest) {
      const last = sky[sky.length - 1];
      if (last && last.y === s.y && last.x + last.w === s.x) last.w += s.w;
      else sky.push({ ...s });
    }
  };
  for (const it of sorted) {
    const cw = it.w + pad * 2;
    const ch = it.h + pad * 2;
    if (cw > max || ch > maxH) throw new Error(`atlas: ${it.id} ${it.w}×${it.h} lớn hơn trang ${max}×${maxH}`);
    if (!pages.length) newPage();
    let best: { i: number; y: number } | null = null;
    for (let i = 0; i < sky.length; i++) {
      const y = fit(i, cw);
      if (y === null || y + ch > maxH) continue;
      if (!best || y < best.y) best = { i, y };
    }
    if (!best) {
      newPage();
      best = { i: 0, y: 0 };
    }
    const x = sky[best.i]!.x;
    place(best.i, cw, ch, best.y);
    placed.push({ ...it, page: pages.length - 1, x: x + pad, y: best.y + pad });
    const p = pages[pages.length - 1]!;
    p.w = Math.max(p.w, x + cw);
    p.h = Math.max(p.h, best.y + ch);
  }
  return { placed, pages };
}

/**
 * Thử nhiều bề rộng trang (vẫn ≤ `max`), chọn cách xếp có tổng diện tích trang nhỏ nhất: nhóm ít ảnh không bị dàn thành
 * một hàng dài thấp lè tè với nhiều khoảng trống.
 */
export function packBest(items: PackItem[], max = ATLAS_MAX, pad = ATLAS_PAD): ReturnType<typeof packShelves> {
  const minW = Math.max(...items.map((i) => i.w + pad * 2));
  if (items.some((i) => i.h + pad * 2 > max)) return packShelves(items, max, pad); // để packShelves báo lỗi rõ
  let best: ReturnType<typeof packShelves> | null = null;
  let bestArea = Infinity;
  for (const w of [256, 384, 512, 640, 768, 1024, 1280, 1536, 1792, 2048]) {
    if (w < minW || w > max) continue;
    const r = packShelves(items, w, pad, max);
    const area = r.pages.reduce((s, p) => s + p.w * p.h, 0) * (1 + 0.02 * r.pages.length); // phạt nhẹ mỗi trang thêm (thêm request)
    if (area < bestArea) {
      bestArea = area;
      best = r;
    }
  }
  return best ?? packShelves(items, max, pad);
}

/** Bảng dùng ảnh: map → preset (`low|medium|high`) → id ảnh. */
export type Usage = Record<string, Record<string, string[]>>;

/**
 * Gom ảnh theo đúng tập "map@preset" dùng nó (preset thấp dựng ít đồ hơn, có ảnh chỉ preset thấp dùng như bóng vẽ sẵn).
 * Một map ở một preset chỉ tải trang có chứa nó → không tải ảnh map/preset khác. Khóa nhóm: các phần tử sắp xếp, nối '+'.
 */
export function groupBySignature(usage: Usage): Map<string, string[]> {
  const use = new Map<string, Set<string>>();
  for (const [m, qs] of Object.entries(usage))
    for (const [q, ids] of Object.entries(qs)) for (const id of ids) (use.get(id) ?? use.set(id, new Set()).get(id)!).add(`${m}@${q}`);
  const groups = new Map<string, string[]>();
  for (const [id, ms] of use) {
    const key = [...ms].sort().join('+');
    (groups.get(key) ?? groups.set(key, []).get(key)!).push(id);
  }
  for (const v of groups.values()) v.sort();
  return new Map([...groups.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

export interface AtlasJson {
  /** Trang: đường dẫn logic (trong public) + kích thước. */
  pages: { file: string; w: number; h: number }[];
  /** id ảnh (tên file hd2d không đuôi, ví dụ `bush-01`, `npc-lio.idle`) → [trang, x, y, w, h] tính bằng px, gốc trên-trái. */
  sprites: Record<string, [number, number, number, number, number]>;
  /** `map@preset` → các trang map đó dùng ở preset đó (để nạp sẵn map kề). */
  maps: Record<string, number[]>;
}

export async function buildAtlas(outDir: string, groupsFile: string): Promise<AtlasJson | null> {
  if (!existsSync(groupsFile)) return null;
  const usage = (JSON.parse(readFileSync(groupsFile, 'utf8')) as { maps: Usage }).maps;
  const hd2d = join(outDir, 'hd2d');
  const atlasDir = join(hd2d, 'atlas');
  mkdirSync(atlasDir, { recursive: true });
  const out: AtlasJson = { pages: [], sprites: {}, maps: {} };
  const pageOfGroup = new Map<string, number[]>();
  let gi = 0;
  for (const [key, ids] of groupBySignature(usage)) {
    const items: PackItem[] = [];
    for (const id of ids) {
      const f = join(hd2d, `${id}.png`);
      if (!existsSync(f)) continue; // ảnh đã bị xóa từ khi ghi usage: bỏ qua, tải lẻ cũng không có
      const m = await sharp(f).metadata();
      if (!m.width || !m.height || m.width + ATLAS_PAD * 2 > ATLAS_MAX || m.height + ATLAS_PAD * 2 > ATLAS_MAX) continue; // quá lớn: tải lẻ
      items.push({ id, w: m.width, h: m.height });
    }
    if (!items.length) continue;
    const { placed, pages } = packBest(items);
    const base = out.pages.length;
    const idx: number[] = [];
    for (let p = 0; p < pages.length; p++) {
      const { w, h } = pages[p]!;
      const comps: sharp.OverlayOptions[] = [];
      for (const it of placed.filter((q) => q.page === p)) {
        // Kéo dài mép: lặp lại hàng/cột pixel ngoài cùng ATLAS_PAD lần.
        const input = await sharp(join(hd2d, `${it.id}.png`))
          .ensureAlpha()
          .extend({ top: ATLAS_PAD, bottom: ATLAS_PAD, left: ATLAS_PAD, right: ATLAS_PAD, extendWith: 'copy' })
          .png()
          .toBuffer();
        comps.push({ input, left: it.x - ATLAS_PAD, top: it.y - ATLAS_PAD });
        out.sprites[it.id] = [base + p, it.x, it.y, it.w, it.h];
      }
      const file = `hd2d/atlas/g${String(gi).padStart(2, '0')}-${p}.webp`;
      await sharp({ create: { width: w, height: h, channels: 4, background: { r: 0, g: 0, b: 0, alpha: 0 } } })
        .composite(comps)
        .webp({ lossless: true, effort: 4 })
        .toFile(join(outDir, file));
      out.pages.push({ file, w, h });
      idx.push(base + p);
    }
    pageOfGroup.set(key, idx);
    gi++;
  }
  for (const [m, qs] of Object.entries(usage))
    for (const q of Object.keys(qs)) {
      const el = `${m}@${q}`;
      out.maps[el] = [...pageOfGroup.entries()].filter(([k]) => k.split('+').includes(el)).flatMap(([, v]) => v);
    }
  writeFileSync(join(hd2d, 'atlas.json'), JSON.stringify(out));
  return out;
}

function walk(dir: string, out: string[] = []): string[] {
  if (!existsSync(dir)) return out;
  for (const n of readdirSync(dir)) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

/**
 * Thêm bản WebP lossless cạnh mỗi PNG nếu nhỏ hơn ít nhất 3%. Trả danh sách PNG (đường dẫn tuyệt đối) đã có bản WebP.
 * Chạy song song có giới hạn để build không quá lâu.
 */
export async function webpify(outDir: string, dirs: string[], skipDir?: string): Promise<{ converted: Set<string>; before: number; after: number }> {
  const files = dirs.flatMap((d) => walk(join(outDir, d))).filter((f) => f.endsWith('.png') && (!skipDir || !f.startsWith(skipDir)));
  const converted = new Set<string>();
  let before = 0;
  let after = 0;
  let i = 0;
  const worker = async () => {
    while (i < files.length) {
      const f = files[i++]!;
      if (existsSync(f.slice(0, -4) + '.webp')) continue; // đã có file .webp cùng tên (ví dụ ảnh pet): không ghi đè
      const png = statSync(f).size;
      const buf = await sharp(f).webp({ lossless: true, effort: 4 }).toBuffer();
      before += png;
      if (buf.length < png * 0.97) {
        writeFileSync(f.slice(0, -4) + '.webp', buf);
        converted.add(f);
        after += buf.length;
      } else after += png;
    }
  };
  await Promise.all(Array.from({ length: 6 }, worker));
  return { converted, before, after };
}
