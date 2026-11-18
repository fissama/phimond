import { createHash } from 'node:crypto';
import { copyFileSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import type { Plugin } from 'vite';

/**
 * AD1 — băm tên asset tĩnh khi build (`vite build`), để nginx/CDN cache 1 năm (`immutable`).
 *
 * Ảnh/âm thanh/json trong `public/{hd2d,ui,battle,pets,audio,i18n}` được Vite chép nguyên vào `dist/`. Sau khi build xong,
 * plugin này:
 *  1. thêm bản sao `<tên>.<10 ký tự sha256>.<đuôi>` cho mỗi file (cùng nội dung → cùng tên, đổi ảnh → đổi tên). File tên gốc
 *     vẫn giữ: người đang chơi bản cũ (index.html cũ) sau khi rollout sẽ không còn file băm cũ, client tự lùi về tên gốc;
 *  2. ghi `dist/asset-manifest.json` (đường dẫn logic → đường dẫn đã băm) cho công cụ/CDN;
 *  3. nhúng manifest vào `dist/index.html` (`window.__PHIMOND_ASSETS__`) để client tra không tốn thêm request;
 *  4. sửa `url(../ui/x.png)` trong CSS đã build sang tên đã băm.
 * Bản dev (`vite`) không chạy plugin: client dùng đường dẫn gốc (`src/assetUrl.ts`).
 */
export const HASHED_DIRS = ['hd2d', 'ui', 'battle', 'pets', 'audio', 'i18n'];
const SKIP = /(^|\/)\.DS_Store$|\.md$/i;
export const HASH_LEN = 10;

function walk(dir: string, out: string[] = []): string[] {
  let names: string[];
  try {
    names = readdirSync(dir);
  } catch {
    return out;
  }
  for (const n of names) {
    const p = join(dir, n);
    if (statSync(p).isDirectory()) walk(p, out);
    else out.push(p);
  }
  return out;
}

/** `hd2d/bush-01.png` + nội dung → `hd2d/bush-01.3fa9c1d2e4.png`; `x.idle.png` → `x.idle.<hash>.png`. */
export function hashedName(logical: string, content: Buffer): string {
  const h = createHash('sha256').update(content).digest('hex').slice(0, HASH_LEN);
  const dot = logical.lastIndexOf('.');
  const slash = logical.lastIndexOf('/');
  return dot > slash ? `${logical.slice(0, dot)}.${h}${logical.slice(dot)}` : `${logical}.${h}`;
}

/** Thay `url(../<logic>)` (CSS build nằm ở `dist/assets/`) bằng tên đã băm. */
export function rewriteCssUrls(css: string, manifest: Record<string, string>): string {
  return css.replace(/url\(\s*(['"]?)\.\.\/([^'")?#]+)\1\s*\)/g, (all, q: string, path: string) =>
    manifest[path] ? `url(${q}../${manifest[path]}${q})` : all,
  );
}

export function hashPublic(): Plugin {
  let outDir = 'dist';
  return {
    name: 'phimond-hash-public',
    apply: 'build',
    configResolved(c) {
      outDir = c.build.outDir.startsWith('/') ? c.build.outDir : join(c.root, c.build.outDir);
    },
    closeBundle() {
      const manifest: Record<string, string> = {};
      for (const d of HASHED_DIRS) {
        for (const file of walk(join(outDir, d))) {
          const logical = relative(outDir, file).split(sep).join('/');
          if (/\.DS_Store$/.test(logical)) {
            rmSync(file);
            continue;
          }
          if (SKIP.test(logical)) continue;
          // Tên gốc trông như đã băm sẽ bị nginx cache 1 năm và bị client cắt nhầm khi lùi về tên gốc: chặn từ lúc build.
          if (/\.[0-9a-f]{10}\.[a-z0-9]+$/i.test(logical)) throw new Error(`phimond-hash-public: tên gốc giống tên đã băm: ${logical}`);
          const name = hashedName(logical, readFileSync(file));
          copyFileSync(file, join(outDir, name));
          manifest[logical] = name;
        }
      }
      const sorted = Object.fromEntries(Object.entries(manifest).sort(([a], [b]) => a.localeCompare(b)));
      writeFileSync(join(outDir, 'asset-manifest.json'), JSON.stringify(sorted, null, 1));
      for (const f of walk(join(outDir, 'assets'))) {
        if (f.endsWith('.css')) writeFileSync(f, rewriteCssUrls(readFileSync(f, 'utf8'), sorted));
      }
      const indexPath = join(outDir, 'index.html');
      const html = readFileSync(indexPath, 'utf8');
      // `<` trong JSON không thể đóng thẻ script vì tên file không chứa ký tự đó; vẫn thoát cho chắc.
      const inline = `<script>window.__PHIMOND_ASSETS__=${JSON.stringify(sorted).replace(/</g, '\\u003c')}</script>`;
      if (!html.includes('</title>')) throw new Error('phimond-hash-public: index.html không có </title> để chèn manifest');
      writeFileSync(indexPath, html.replace('</title>', `</title>\n    ${inline}`));
      this.info?.(`băm ${Object.keys(sorted).length} asset → asset-manifest.json`);
    },
  };
}
