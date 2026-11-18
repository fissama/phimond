import type { Engine } from './engine.ts';

/**
 * Đo hiệu năng tại chỗ (AD0, nợ P01 N08). Luôn có `window.__phimondBench()` (rẻ, chỉ đọc số đếm) để test/bench đọc;
 * overlay chỉ hiện khi URL có `?bench=1`. Không gửi số đo đi đâu.
 */
export interface BenchStats {
  /** FPS trung bình ~4 giây gần nhất. */
  fps: number;
  /** Thời gian khung chậm nhất trong ~4 giây (ms). */
  worstFrameMs: number;
  /** Texture đang nằm trên GPU theo three.js (đếm, không phải byte). */
  gpuTextures: number;
  gpuGeometries: number;
  /** Bộ nhớ ước tính của cache texture ảnh (w×h×4), MB. */
  cacheMB: number;
  cacheCount: number;
  drawCalls: number;
  /** Thời gian tải map gần nhất (ms). */
  lastMapLoadMs: number | null;
  /** Số request ảnh/âm thanh/json đã gửi từ lúc mở trang, và tổng byte nhận qua mạng (0 khi lấy từ cache). */
  requests: { images: number; audio: number; json: number; transferKB: number };
  /** Heap JS (chỉ Chromium), MB. */
  heapMB: number | null;
}

let engine: Engine | null = null;

export function attachBench(e: Engine): void {
  engine = e;
}

export function detachBench(e: Engine): void {
  if (engine === e) engine = null;
}

export function benchStats(): BenchStats | null {
  if (!engine) return null;
  const s = engine.stats();
  const ft = engine.frameTimes.filter((t) => t > 0 && t < 1000);
  const avg = ft.length ? ft.reduce((a, b) => a + b, 0) / ft.length : 0;
  let images = 0;
  let audio = 0;
  let json = 0;
  let bytes = 0;
  for (const r of performance.getEntriesByType('resource') as PerformanceResourceTiming[]) {
    const path = r.name.split('?')[0]!;
    if (/\.(png|webp|jpe?g|gif|avif)$/i.test(path)) images++;
    else if (/\.(ogg|mp3|wav)$/i.test(path)) audio++;
    else if (/\.json$/i.test(path)) json++;
    else continue;
    bytes += r.transferSize || 0;
  }
  const mem = (performance as unknown as { memory?: { usedJSHeapSize: number } }).memory;
  return {
    fps: avg ? Math.round(1000 / avg) : 0,
    worstFrameMs: ft.length ? Math.round(Math.max(...ft)) : 0,
    gpuTextures: s.textures,
    gpuGeometries: s.geometries,
    cacheMB: s.cacheMB,
    cacheCount: s.cacheCount,
    drawCalls: s.calls,
    lastMapLoadMs: (window as unknown as { __phimondLastMapLoadMs?: number }).__phimondLastMapLoadMs ?? null,
    requests: { images, audio, json, transferKB: Math.round(bytes / 1024) },
    heapMB: mem ? Math.round(mem.usedJSHeapSize / 1048576) : null,
  };
}

if (typeof window !== 'undefined') {
  (window as unknown as { __phimondBench: typeof benchStats }).__phimondBench = benchStats;
  // Bộ đệm resource mặc định chỉ 250 mục: nâng lên để đếm đủ request của cả phiên.
  performance.setResourceTimingBufferSize?.(5000);
}

/** Overlay góc trái dưới khi URL có `?bench=1`. Gọi một lần lúc khởi động. */
export function mountBenchOverlay(): void {
  if (!new URLSearchParams(location.search).has('bench')) return;
  const el = document.createElement('pre');
  el.dataset.testid = 'bench';
  el.style.cssText =
    'position:fixed;left:4px;bottom:4px;z-index:99999;margin:0;padding:4px 6px;font:11px/1.35 ui-monospace,monospace;color:#d8ffd0;background:rgba(0,0,0,.72);pointer-events:none;white-space:pre';
  document.body.appendChild(el);
  setInterval(() => {
    const b = benchStats();
    if (!b) {
      el.textContent = 'bench: chưa vào thế giới';
      return;
    }
    el.textContent = [
      `FPS ${b.fps}  khung chậm nhất ${b.worstFrameMs} ms  draw ${b.drawCalls}`,
      `GPU tex ${b.gpuTextures}  geo ${b.gpuGeometries}  cache ${b.cacheMB} MB / ${b.cacheCount} ảnh`,
      `tải map ${b.lastMapLoadMs ?? '-'} ms  heap ${b.heapMB ?? '-'} MB`,
      `req ảnh ${b.requests.images}  âm ${b.requests.audio}  json ${b.requests.json}  mạng ${b.requests.transferKB} KB`,
    ].join('\n');
  }, 1000);
}
