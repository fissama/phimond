import { signal } from '@preact/signals';
// Canvas thiết kế gốc 960×640 (APK). k = hệ số theo chiều cao; t = hệ số cho vùng chạm (không nhỏ hơn 0.95 để ngón tay bấm được).
export const K = signal(1);
export const T = signal(1);
export function applyScale(): void {
  const vv = window.visualViewport; const h = vv?.height ?? window.innerHeight, w = vv?.width ?? window.innerWidth;
  let k = Math.min(Math.max(h / 640, 0.72), 1.6);
  k = Math.min(k, Math.max(0.72, (w - 280) / 442)); // chat tối thiểu ~280px
  const t = Math.max(k, 0.98);
  K.value = k; T.value = t;
  const r = document.documentElement.style; r.setProperty('--k', k.toFixed(3)); r.setProperty('--t', t.toFixed(3));
}
export function watchScale(): () => void {
  applyScale();
  const f = () => applyScale(); window.addEventListener('resize', f); window.visualViewport?.addEventListener('resize', f);
  return () => { window.removeEventListener('resize', f); window.visualViewport?.removeEventListener('resize', f); };
}
