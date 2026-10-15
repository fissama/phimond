/** Lớp nhãn DOM phủ trên canvas: tên, thanh HP, số sát thương. Cập nhật bằng transform mỗi khung, không qua Preact. */
export interface Label {
  key: string; x: number; y: number; on: boolean;
  html: string; cls: string; scale?: number; z?: number;
}
export class Overlay {
  readonly root: HTMLElement;
  private pool = new Map<string, HTMLElement>();
  private seen = new Set<string>();
  private lastHtml = new Map<string, string>();
  constructor(parent: HTMLElement) {
    this.root = document.createElement('div'); this.root.className = 'overlay'; this.root.setAttribute('aria-hidden', 'true'); parent.appendChild(this.root);
  }
  begin(): void { this.seen.clear(); }
  put(l: Label): void {
    let el = this.pool.get(l.key);
    if (!el) { el = document.createElement('div'); this.root.appendChild(el); this.pool.set(l.key, el); }
    if (el.className !== `lbl ${l.cls}`) el.className = `lbl ${l.cls}`;
    if (this.lastHtml.get(l.key) !== l.html) { el.innerHTML = l.html; this.lastHtml.set(l.key, l.html); }
    el.style.display = l.on ? '' : 'none';
    el.style.transform = `translate3d(${Math.round(l.x)}px,${Math.round(l.y)}px,0) translate(-50%,-100%)${l.scale && l.scale !== 1 ? ` scale(${l.scale})` : ''}`;
    if (l.z !== undefined) el.style.zIndex = String(l.z);
    this.seen.add(l.key);
  }
  end(): void {
    for (const [k, el] of this.pool) if (!this.seen.has(k)) { el.remove(); this.pool.delete(k); this.lastHtml.delete(k); }
  }
  clear(): void { for (const el of this.pool.values()) el.remove(); this.pool.clear(); this.lastHtml.clear(); }
}
export const esc = (s: string): string => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
