import { effect, signal } from '@preact/signals';
import type { Character, IntentMap, IntentOp, MapDef } from '@phimond/protocol';
import type { Batch, Session } from '../net/session.ts';
import { Engine, type Pick } from '../render/engine.ts';
import { prefetch, hd2dUrl } from '../render/assets.ts';
import { settings } from '../state/settings.ts';
import { battleResultOpen, closeOverlay, fatal, loading, overlay, pushLog, toast } from '../state/ui.ts';
import { sfx } from '../ui/sound.ts';
import { chebyshev, type Cell, type Direction } from '../world/coords.ts';
import { Mover } from '../world/mover.ts';
import { around, findPath, rectCells } from '../world/path.ts';
import { Content, eventText } from './content.ts';

/** Map và vị trí đang hiển thị (cho HUD). */
export const currentMap = signal<MapDef | null>(null);

/** Gợi ý hành động của nút "Chọn" (null = không có gì ở gần). Cập nhật khi nhân vật đổi ô. */
export const interactHint = signal<string | null>(null);
/** Số ô quanh điểm chạm để tìm ô đi được gần nhất khi chạm vào ô bị chặn (đánh giá T3). */
const SNAP_RADIUS = 2;

/**
 * Điều phối world phía client: nhận trạng thái server, điều khiển di chuyển, tự kích hoạt cổng/quái khi đứng đúng chỗ,
 * tương tác NPC/bệ/trụ, chuyển map. Server luôn là nguồn sự thật; ở đây chỉ chọn intent để gửi.
 */
export class GameWorld {
  mover: Mover | null = null;
  private serverOffset = 0;
  private hidden: Record<string, number> = {};
  private portalLatch: string | null = null;
  private lockedLatch: string | null = null;
  private contactLatch = new Set<string>();
  private busy = false;
  private loadingMap: string | null = null;
  private readonly unsub: (() => void)[] = [];
  private hiddenTab = false;

  constructor(
    readonly engine: Engine,
    readonly content: Content,
    readonly session: Session,
    private readonly playerAsset: string,
  ) {}

  async start(): Promise<void> {
    const ch = this.session.character.value!;
    this.engine.setQuality(settings.value.quality);
    this.engine.setFpsCap(settings.value.fps);
    this.unsub.push(this.session.onBatch((b) => void this.onBatch(b)));
    this.unsub.push(
      effect(() => {
        const s = settings.value;
        this.engine.setFpsCap(s.fps);
        if (s.quality !== this.engine.currentQuality) void this.reloadScene(s.quality);
      }),
    );
    // Mở lớp phủ/hiện trận/mất focus → dừng di chuyển ngay (P01-R03).
    this.unsub.push(effect(() => this.updatePause(overlay.value.kind !== 'none', this.session.character.value?.battle != null || battleResultOpen.value, loading.value !== null)));
    // Tự kết nối lại khi mất kết nối (không gửi lại intent nào): 2s, 4s, 8s… tối đa 30s.
    let retry: ReturnType<typeof setTimeout> | null = null;
    let backoff = 2000;
    this.unsub.push(
      effect(() => {
        const st = this.session.status.value;
        if (st === 'online') backoff = 2000;
        if (st !== 'offline' || retry || !this.session.loggedIn) return;
        retry = setTimeout(() => {
          retry = null;
          void this.session.connect().catch(() => (backoff = Math.min(30000, backoff * 2)));
        }, backoff);
      }),
      () => retry && clearTimeout(retry),
    );
    const onVis = () => {
      this.hiddenTab = document.visibilityState === 'hidden';
      this.mover?.stop();
    };
    const onBlur = () => this.mover?.stop();
    document.addEventListener('visibilitychange', onVis);
    window.addEventListener('blur', onBlur);
    this.unsub.push(() => document.removeEventListener('visibilitychange', onVis), () => window.removeEventListener('blur', onBlur));
    this.engine.onFrame((dt) => this.frame(dt));
    this.engine.start();
    this.absorb(ch);
    this.welcome(ch);
    await this.enterMap(ch);
  }

  /** Vài dòng hệ thống đầu tiên để hộp chat không trống và người mới biết cách chơi (đánh giá G2/L1). */
  private welcome(ch: Character): void {
    pushLog('Chào mừng đến Phimond!');
    if (!ch.pets.some((p) => !p.retired)) pushLog('Hãy chạm vào một bệ đá trong Triệu Linh Điện để nhận linh thú đầu tiên.');
    pushLog('Di chuyển: chạm vào cảnh, phím mũi tên/WASD hoặc nút điều hướng. Tương tác: nút Chọn, phím E hoặc Space.');
  }

  dispose(): void {
    this.unsub.forEach((u) => u());
    this.engine.dispose();
  }

  // ------------------------------------------------------------ trạng thái server
  private absorb(ch: Character): void {
    if (ch.server_time_ms) this.serverOffset = ch.server_time_ms - Date.now();
    this.hidden = { ...ch.spawn_hidden };
  }

  private async onBatch(b: Batch): Promise<void> {
    const ch = b.character;
    this.absorb(ch);
    for (const e of b.events) {
      if (ch.battle || e.type === 'battle_start' || e.type === 'battle_capture' || ['damage', 'heal', 'miss', 'skill_cast', 'status_applied', 'defend'].includes(e.type)) continue;
      if (e.type === 'npc_dialogue') continue;
      if (e.type === 'quest_complete' || e.type === 'quest_accept') sfx('level');
      else if (e.type === 'item_spend' || e.type === 'pet_heal') sfx('magic');
      else if (e.type === 'currency_gain' && !b.presentation?.completed_battle) sfx('coin');
      pushLog(eventText(e), e.type === 'map_enter' ? 'area' : 'system');
    }
    if (!this.mover) return;
    if (ch.map_id !== this.mover.mapId) {
      await this.enterMap(ch);
      return;
    }
    this.mover.setAuthoritative(ch.map_id, { x: ch.x, y: ch.y });
  }

  private async enterMap(ch: Character): Promise<void> {
    const map = this.content.map(ch.map_id);
    const grid = this.content.grid(ch.map_id);
    if (!map || !grid) {
      // Thường do server đang chạy bản cũ (catalog chưa có map P01/lưới đi): báo rõ thay vì đứng im.
      fatal.value = map
        ? `Server chưa có dữ liệu va chạm của "${map.name}". Hãy build lại và chạy server bản mới (apps/game-server).`
        : `Server gửi map "${ch.map_id}" không có trong dữ liệu P01. Hãy build lại và chạy server bản mới (apps/game-server), rồi tải lại trang.`;
      return;
    }
    if (this.loadingMap === map.id) return;
    this.loadingMap = map.id;
    loading.value = map.name;
    const t0 = performance.now();
    await this.engine.loadMap(map, this.content.npcsOn(map.id), this.playerAsset);
    const latest = this.session.character.value ?? ch;
    if (!this.mover) {
      this.mover = new Mover(grid, map.id, { x: latest.x, y: latest.y }, (dir) => this.sendMove(dir));
      this.mover.onBlocked = (msg) => toast(msg);
      this.mover.stopAt = (c) => this.stopAtTrigger(c);
    } else {
      this.mover.setAuthoritative(map.id, { x: latest.x, y: latest.y }, grid);
    }
    this.mover.facing = 'down';
    this.portalLatch = this.portalAt(this.mover.cell)?.id ?? null;
    this.contactLatch.clear();
    currentMap.value = map;
    this.engine.setPlayer(this.mover.pos, false, this.mover.facing);
    this.engine.snapCamera();
    this.refreshSpawns();
    // Giữ màn tải tối thiểu một chút để không nháy; ghi thời gian tải để đo (R08).
    const spent = performance.now() - t0;
    (window as unknown as { __phimondLastMapLoadMs?: number }).__phimondLastMapLoadMs = Math.round(spent);
    setTimeout(() => (loading.value = null), Math.max(0, 250 - spent));
    this.loadingMap = null;
    this.prefetchNeighbors(map);
  }

  private async reloadScene(q: typeof settings.value.quality): Promise<void> {
    const ch = this.session.character.value;
    const map = ch && this.content.map(ch.map_id);
    this.engine.setQuality(q);
    if (!map) return;
    loading.value = map.name;
    await this.engine.loadMap(map, this.content.npcsOn(map.id), this.playerAsset);
    this.refreshSpawns();
    loading.value = null;
  }

  private prefetchNeighbors(map: MapDef): void {
    const next = new Set<string>();
    for (const p of map.portals) {
      if (p.locked) continue;
      next.add(p.to);
      if (p.redirect) next.add(p.redirect.to);
    }
    const urls: string[] = [];
    for (const id of next) {
      const m = this.content.map(id);
      if (m?.backdrop) urls.push(hd2dUrl(m.backdrop));
    }
    prefetch(urls);
  }

  // ------------------------------------------------------------ vòng khung hình
  private frame(dt: number): void {
    const m = this.mover;
    if (!m) return;
    m.update(dt);
    this.engine.setPlayer(m.pos, m.moving, m.facing);
    if (Math.random() < 0.05) this.refreshSpawns();
    if (m.settled && !this.busy) this.checkTriggers();
    const key = `${m.cell.x},${m.cell.y}`;
    if (key !== this.hintKey) {
      this.hintKey = key;
      interactHint.value = this.nearby()?.label ?? null;
    }
  }

  private hintKey = '';

  /** Thứ gần nhất trong tầm 1 ô mà nút "Chọn" sẽ tương tác. */
  private nearby(): { label: string; run: () => void } | null {
    const m = this.mover;
    const map = currentMap.value;
    if (!m || !map) return null;
    const c = m.cell;
    const npc = this.content.npcsOn(map.id).find((n) => chebyshev(n, c) <= 1);
    if (npc) return { label: 'Nói chuyện', run: () => void this.talk(npc.id) };
    const ped = map.pedestals.find((p) => chebyshev(p, c) <= 1);
    if (ped) return { label: 'Chọn bệ', run: () => (overlay.value = { kind: 'pedestal', index: ped.index }) };
    if (map.pillar && chebyshev(map.pillar, c) <= 1) return { label: 'Dùng trụ', run: () => (overlay.value = { kind: 'pillar' }) };
    return null;
  }

  /** Ô đi được gần nhất (Chebyshev ≤ SNAP_RADIUS), ưu tiên ô gần điểm chạm rồi gần người chơi. */
  private snapWalkable(grid: { walkable(x: number, y: number): boolean }, c: Cell, from: Cell): Cell | null {
    let best: Cell | null = null;
    let bd = Infinity;
    for (let dy = -SNAP_RADIUS; dy <= SNAP_RADIUS; dy++)
      for (let dx = -SNAP_RADIUS; dx <= SNAP_RADIUS; dx++) {
        const q = { x: c.x + dx, y: c.y + dy };
        if (!grid.walkable(q.x, q.y)) continue;
        const d = Math.hypot(dx, dy) * 10 + chebyshev(q, from) * 0.1;
        if (d < bd) (bd = d), (best = q);
      }
    return best;
  }

  private serverNow(): number {
    return Date.now() + this.serverOffset;
  }

  private refreshSpawns(): void {
    const map = currentMap.value;
    if (!map) return;
    const now = this.serverNow();
    for (const s of map.wild_spawns) this.engine.setSpawnVisible(s.id, !((this.hidden[s.id] ?? 0) > now));
  }

  private spawnVisible(id: string): boolean {
    return !((this.hidden[id] ?? 0) > this.serverNow());
  }

  private portalAt(c: Cell) {
    const map = currentMap.value;
    return map?.portals.find((p) => p.rect && c.x >= p.rect[0] && c.x < p.rect[0] + p.rect[2] && c.y >= p.rect[1] && c.y < p.rect[1] + p.rect[3]);
  }

  /**
   * Vừa bước vào vùng cổng hoặc kề quái (theo vị trí dự đoán): dừng lại để server xác nhận hết các bước,
   * rồi checkTriggers mới gửi intent (server xét vị trí đã xác nhận).
   */
  private stopAtTrigger(c: Cell): boolean {
    const map = currentMap.value;
    if (!map) return false;
    const portal = this.portalAt(c);
    const hitPortal = portal && !portal.locked && portal.id !== this.portalLatch;
    const hitBeast = map.wild_spawns.some((w) => chebyshev(w, c) <= 1 && this.spawnVisible(w.id) && !this.contactLatch.has(w.id));
    return !!(hitPortal || hitBeast);
  }

  /** Đứng yên đúng vị trí server: tự đi qua cổng hoặc chạm quái kề bên. */
  private checkTriggers(): void {
    const m = this.mover!;
    const map = currentMap.value;
    if (!map || m.paused) return;
    const c = m.cell;
    const portal = this.portalAt(c);
    if (!portal) this.portalLatch = null;
    if (portal && portal.id !== this.portalLatch) {
      this.portalLatch = portal.id;
      if (portal.locked) {
        toast(`${this.content.mapName(portal.to)}: khu vực này chưa mở`);
      } else {
        m.stop();
        void this.intent('world.portal', { portal_id: portal.id });
      }
      return;
    }
    // Cổng khóa: báo khi đứng kề (không có ô đi vào).
    const near = map.portals.find((p) => p.locked && p.rect && rectCells(p.rect).some((q) => chebyshev(q, c) <= 1));
    if (near && near.id !== this.lockedLatch) {
      this.lockedLatch = near.id;
      toast(`${this.content.mapName(near.to)}: khu vực này chưa mở`);
    } else if (!near) this.lockedLatch = null;

    for (const id of [...this.contactLatch]) {
      const s = map.wild_spawns.find((w) => w.id === id);
      if (!s || chebyshev(s, c) > 1) this.contactLatch.delete(id);
    }
    const s = map.wild_spawns.find((w) => chebyshev(w, c) <= 1 && this.spawnVisible(w.id) && !this.contactLatch.has(w.id));
    if (s) {
      this.contactLatch.add(s.id);
      m.stop();
      void this.intent('world.encounter', { spawn_id: s.id });
    }
  }

  private updatePause(overlayOpen: boolean, inBattle: boolean, isLoading: boolean): void {
    this.mover?.setPaused(overlayOpen || inBattle || isLoading || this.hiddenTab);
  }

  // ------------------------------------------------------------ gửi intent
  private async sendMove(dir: Direction) {
    const r = await this.session.send('world.move', { direction: dir });
    return r.ok ? ({ ok: true } as const) : ({ ok: false, message: r.message } as const);
  }

  /** Gửi một intent không phải di chuyển (một cái một lúc). Trả true nếu được chấp nhận. */
  async intent<K extends IntentOp>(op: K, data: IntentMap[K]): Promise<boolean> {
    if (this.busy) return false;
    this.busy = true;
    try {
      const r = await this.session.send(op, data);
      if (!r.ok) {
        toast(r.message);
        return false;
      }
      return true;
    } finally {
      this.busy = false;
    }
  }

  // ------------------------------------------------------------ điều khiển
  setHeld(dir: Direction | null): void {
    if (!this.mover) return;
    if (dir && this.mover.paused && overlay.value.kind !== 'none') toast('Đóng bảng đang mở để tiếp tục di chuyển');
    if (dir) {
      this.mover.path = [];
      this.mover.tap = dir;
    }
    this.mover.held = dir;
  }

  /** Chạm/click vào cảnh. */
  tap(clientX: number, clientY: number): void {
    const p = this.engine.pick(clientX, clientY);
    if (p) this.act(p);
  }

  act(p: Pick): void {
    const m = this.mover;
    const map = currentMap.value;
    if (!m || !map) return;
    if (m.paused) {
      // Menu/hội thoại/trận đang mở: nói rõ vì sao nhân vật không đi (đánh giá T2).
      if (overlay.value.kind !== 'none') toast('Đóng bảng đang mở để tiếp tục di chuyển');
      return;
    }
    const grid = this.content.grid(map.id)!;
    const goTo = (goals: Cell[], then: () => void) => {
      const path = findPath(grid, m.cell, goals);
      if (!path) return toast('Không đi tới được');
      m.walkTo(path, () => {
        // Chờ server xác nhận hết các bước rồi mới tương tác.
        const wait = () => (m.settled ? then() : m.pending > 0 || m.moving ? setTimeout(wait, 40) : then());
        wait();
      });
    };
    switch (p.kind) {
      case 'ground': {
        let target = p.cell;
        if (!grid.walkable(target.x, target.y)) {
          const npcHere = this.content.npcsOn(map.id).find((n) => n.x === p.cell.x && n.y === p.cell.y);
          if (npcHere) return this.act({ kind: 'npc', id: npcHere.id });
          const near = this.snapWalkable(grid, target, m.cell);
          if (!near) return toast('Không đi vào đó được');
          target = near;
        }
        const path = findPath(grid, m.cell, [target]);
        if (!path) return toast('Không đi tới được');
        m.walkTo(path);
        return;
      }
      case 'npc': {
        const n = this.content.cat.npcs[p.id];
        if (!n) return;
        return goTo(around(n), () => void this.talk(p.id));
      }
      case 'pedestal': {
        const ped = map.pedestals.find((q) => q.index === p.index);
        if (!ped) return;
        return goTo(around(ped), () => (overlay.value = { kind: 'pedestal', index: ped.index }));
      }
      case 'pillar': {
        const pl = map.pillar;
        if (!pl) return;
        return goTo(around(pl), () => (overlay.value = { kind: 'pillar' }));
      }
      case 'spawn': {
        const s = map.wild_spawns.find((w) => w.id === p.id);
        if (!s) return;
        this.contactLatch.delete(s.id);
        return goTo([s, ...around(s)], () => undefined);
      }
    }
  }

  /** Nút "Chọn": tương tác với thứ gần nhất trong tầm 1 ô (NPC, bệ, trụ). */
  primary(): void {
    const t = this.nearby();
    if (t) return t.run();
    toast('Không có gì để tương tác ở gần');
  }

  async talk(npcId: string): Promise<void> {
    const ok = await this.intent('npc.interact', { npc_id: npcId });
    if (!ok) return;
    const n = this.content.cat.npcs[npcId]!;
    const line = n.dialogue || '…';
    overlay.value = { kind: 'npc', npcId, line };
  }

  async chooseStarter(index: number): Promise<void> {
    const ok = await this.intent('starter.choose', { pedestal: index });
    if (ok) closeOverlay();
  }

  async travel(mapId: string): Promise<void> {
    const ok = await this.intent('pillar.travel', { map_id: mapId });
    if (ok) closeOverlay();
  }
}
