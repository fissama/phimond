import { computed, signal } from '@preact/signals';
import type { Catalog, Character, Pet } from '@phimond/protocol';
import { FriendlyError, type Batch, type Session } from '../net/session.ts';
import { Presentation, STEP_SECONDS } from './presentation.ts';

export type Page = 'World' | 'Companions' | 'Inventory' | 'Quests' | 'Ranch' | 'NPC' | 'Skills' | 'Items' | 'Shop' | 'Journey' | 'Teleport' | 'Settings';
export type Channel = 'all' | 'sys' | 'pm' | 'party' | 'world' | 'guild';
export interface ChatMsg { id: number; channel: Exclude<Channel, 'all'>; text: string; at: number }
export type Screen = 'login' | 'loading' | 'game';
export type Dir = 'left' | 'right' | 'up' | 'down';
export interface Confirm { message: string; op: 'pet.release' | 'pet.strengthen' | 'breeding.synthesize'; data: Record<string, unknown> }
export type Action = { choice: string; skill_id?: string; item_id?: string };

/**
 * Luật phía client (port từ reference_game.gd): đi liên tục theo nhịp 0,18 s, approach NPC/cổng/quái, contact có latch,
 * lệnh Chọn/Trở về, menu, trận đấu (tự động, chọn kỹ năng/vật phẩm). Không tính kết quả; mọi thứ do server quyết định.
 */
export class Game {
  readonly pres = new Presentation();
  readonly screen = signal<Screen>('login');
  readonly page = signal<Page>('World');
  readonly shortcuts = signal(false);
  readonly npcId = signal('');
  readonly automatic = signal(false);
  readonly selectedAction = signal<Action | null>(null);
  readonly chat = signal<ChatMsg[]>([]);
  readonly notice = signal('');
  /** Tab mở sẵn cho trang kế tiếp (vd. NPC role strengthen → Nông trại/Cường hóa). */
  readonly tabHint = signal('');
  readonly debugOn = signal(false);
  readonly revisionSig = signal(-1);
  /** Tăng mỗi khi có batch mới để UI tính lại các phần phụ thuộc Presentation. */
  readonly tick = signal(0);
  readonly isAnimating = signal(false);

  held: Dir | '' = '';
  destination: { kind: 'npc' | 'portal' | 'enemy'; id: string; x: number; y: number } | null = null;
  private moveDelay = 0;
  private actionDelay = 0;
  private contactLatch = '';
  private contactMap = '';
  private lastBattle = '';
  private chatId = 0;
  private hudDelay = 0;
  private offs: (() => void)[] = [];

  readonly character = computed<Character | null>(() => this.session.character.value);
  readonly catalog = computed<Catalog | null>(() => this.session.catalog.value);
  readonly hasBattle = computed(() => !!this.session.character.value?.battle);

  constructor(readonly session: Session) {
    this.offs.push(session.onBatch((b) => this.onBatch(b)));
    this.offs.push(session.onLog((t) => this.message(t)));
    this.offs.push(session.onStatus((s) => {
      if (s !== 'online') { this.held = ''; this.destination = null; this.automatic.value = false; this.selectedAction.value = null; this.pres.cancelPreview(); }
      if (s === 'offline') this.pres.resetPresentation();
    }));
  }
  dispose(): void { for (const o of this.offs) o(); }

  // ---------- đăng nhập / phiên ----------
  async signIn(kind: 'login' | 'register', user: string, pass: string): Promise<string> {
    try {
      await this.session.authenticate(kind, user, pass);
      this.screen.value = 'loading';
      await this.session.loadContent();
      this.pres.resetPresentation();
      await this.session.connect();
      this.screen.value = 'game';
      this.message('Mũi tên / WASD: di chuyển · E: tương tác · Esc: menu');
      return '';
    } catch (e) {
      this.screen.value = 'login';
      return e instanceof FriendlyError ? e.message : 'Không thể kết nối máy chủ. Vui lòng thử lại.';
    }
  }
  async reconnect(): Promise<void> {
    try { await this.session.connect(); } catch { /* thông điệp đã vào chat */ }
  }
  async signOut(): Promise<void> {
    this.held = ''; this.destination = null; this.automatic.value = false; this.selectedAction.value = null;
    this.close(); this.pres.resetPresentation();
    await this.session.logout();
    this.screen.value = 'login';
  }

  // ---------- chat ----------
  message(text: string): void {
    if (!text) return;
    this.chat.value = [...this.chat.value.slice(-59), { id: ++this.chatId, channel: 'sys', text, at: Date.now() }];
    if (text.startsWith('Không') || text.startsWith('Hãy')) { this.automatic.value = false; this.destination = null; this.held = ''; }
  }

  // ---------- batch ----------
  private onBatch(b: Batch): void {
    const catalog = this.session.catalog.value; if (!catalog) return;
    this.pres.applyStateBatch(b.revision, b.character, catalog, b.events, b.presentation as never);
    this.revisionSig.value = b.revision;
    const battleId = b.character.battle?.id ?? '';
    if (battleId !== this.lastBattle) {
      this.close(); this.held = ''; this.destination = null; this.selectedAction.value = null; this.lastBattle = battleId;
    }
    if (!battleId) this.automatic.value = false;
    this.actionDelay = 0.8;
    this.tick.value++;
    if (this.page.value !== 'World' && this.page.value !== 'NPC') { /* giữ trang; UI tự tính lại từ signal */ }
  }

  // ---------- vòng lặp ----------
  update(dt: number): void {
    this.moveDelay -= dt; this.actionDelay -= dt; this.hudDelay -= dt;
    this.isAnimating.value = this.pres.isAnimating();
    const s = this.session;
    if (s.busy.value || s.status.value !== 'online' || this.page.value !== 'World') return;
    if (this.character.value?.battle) {
      if (this.automatic.value && this.actionDelay <= 0 && !this.pres.isAnimating()) this.battleSend('auto');
      return;
    }
    if (this.pres.isAnimating()) return;
    if (this.checkContact()) return;
    if (this.destination && this.moveDelay <= 0) this.travelStep();
    else if (this.held && this.moveDelay <= 0) this.move(this.held);
  }

  // ---------- di chuyển ----------
  startWalk(dir: Dir): void {
    if (this.page.value !== 'World') { this.menuDirection(dir); return; }
    this.held = dir; this.destination = null; this.move(dir);
  }
  stopWalk(dir?: Dir): void { if (!dir || dir === this.held) this.held = ''; }

  move(direction: Dir): void {
    const s = this.session; const c = s.character.value; const cat = s.catalog.value;
    if (!c || !cat) return;
    if (this.page.value !== 'World' || c.battle || s.busy.value || this.pres.isAnimating() || this.moveDelay > 0) return;
    const map = cat.maps[c.map_id]; let x = c.x, y = c.y;
    if (direction === 'left') x -= 1; else if (direction === 'right') x += 1; else if (direction === 'up') y -= 1; else y += 1;
    this.moveDelay = STEP_SECONDS;
    const w = map?.width || 40, h = map?.height || map?.width || 40;
    if (x < 0 || y < 0 || x >= w || y >= h) { this.held = ''; return; }
    void s.send('world.move', { direction });
    if (s.busy.value) this.pres.previewMove(direction);
  }

  approach(kind: 'npc' | 'portal' | 'enemy', id: string): void {
    const s = this.session; const c = s.character.value; const cat = s.catalog.value; if (!c || !cat) return;
    if (c.battle || this.pres.isAnimating() || s.busy.value) return;
    let pt: { x: number; y: number } | null = null;
    if (kind === 'npc') { const n = cat.npcs[id]; if (n) pt = { x: n.x, y: n.y ?? 12 }; }
    else if (kind === 'portal') { const p = cat.maps[c.map_id]?.portals.find((q) => q.id === id); if (p) pt = { x: p.x ?? p.rect?.[0] ?? 0, y: 12 }; }
    else { const sp = cat.maps[c.map_id]?.wild_spawns.find((q) => q.id === id); if (sp) pt = { x: sp.x, y: sp.y }; }
    if (!pt) return;
    this.close();
    this.destination = { kind, id, x: Math.trunc(pt.x), y: Math.trunc(pt.y) };
    this.travelStep();
  }

  private travelStep(): void {
    const s = this.session; const d = this.destination; const c = s.character.value; if (!d || !c) return;
    if (s.busy.value || this.pres.isAnimating()) return;
    const dx = d.x - c.x, dy = d.y - c.y;
    if (Math.abs(dx) > 1) this.move(dx > 0 ? 'right' : 'left');
    else if (Math.abs(dy) > 1) this.move(dy > 0 ? 'down' : 'up');
    else {
      this.destination = null;
      if (d.kind === 'portal') void s.send('world.portal', { portal_id: d.id });
      else if (d.kind === 'enemy') this.encounter(d.id);
      else { this.npcId.value = d.id; void s.send('npc.interact', { npc_id: d.id }); this.open('NPC'); }
    }
  }

  private nearestNpc() {
    const c = this.session.character.value; const cat = this.session.catalog.value; if (!c || !cat) return null;
    let best = null as null | (typeof cat.npcs)[string]; let dist = 999;
    for (const n of Object.values(cat.npcs)) {
      if (n.map_id !== c.map_id) continue;
      const d = Math.abs(n.x - c.x) + Math.abs((n.y ?? 12) - c.y);
      if (d < dist) { best = n; dist = d; }
    }
    return dist <= 5 ? best : null;
  }

  private checkContact(): boolean {
    const c = this.session.character.value; if (!c) return false;
    if (c.map_id !== this.contactMap) { this.contactMap = c.map_id; this.contactLatch = ''; }
    const sp = this.pres.contactSpawn(c.x, c.y);
    if (!sp) { this.contactLatch = ''; return false; }
    if (sp.id === this.contactLatch) return false;
    this.encounter(sp.id);
    return true;
  }

  encounter(spawnId = ''): void {
    const s = this.session;
    if (this.page.value !== 'World' || s.character.value?.battle || s.busy.value || this.pres.isAnimating()) return;
    this.contactLatch = spawnId; this.held = ''; this.destination = null;
    void s.send('world.encounter', spawnId ? { spawn_id: spawnId } : {});
  }

  // ---------- lệnh Chọn / Trở về ----------
  command(cmd: string): void {
    if (!this.character.value) return;
    const c = this.character.value;
    if (cmd === 'back') {
      if (this.selectedAction.value) this.selectedAction.value = null;
      else if (this.page.value !== 'World' || this.shortcuts.value) this.close();
      else this.open('Menu');
      return;
    }
    if (this.page.value !== 'World' && (cmd === 'confirm' || cmd === 'interact')) {
      const f = document.activeElement as HTMLButtonElement | null;
      if (f && f.tagName === 'BUTTON' && !f.disabled && f.closest('[data-menu]')) f.click();
      return;
    }
    if (c.battle) {
      switch (cmd) {
        case 'Skills': case 'Items': this.open(cmd); break;
        case 'auto': this.automatic.value = !this.automatic.value; this.actionDelay = 0; this.close(); break;
        case 'attack': case 'capture': this.selectedAction.value = { choice: cmd }; this.automatic.value = false; this.close(); break;
        case 'defend': case 'flee': this.automatic.value = false; this.battleSend(cmd); break;
        case 'confirm': case 'interact': this.confirmTarget(); break;
      }
    } else if (cmd === 'confirm' || cmd === 'interact') {
      if (this.page.value !== 'World') return;
      const npc = this.nearestNpc();
      if (npc) { this.approach('npc', npc.id); return; }
      const cat = this.catalog.value;
      const near = (cat?.maps[c.map_id]?.portals ?? []).filter((p) => Math.abs((p.x ?? p.rect?.[0] ?? -99) - c.x) <= 2);
      if (near.length > 1) { this.open('Teleport'); return; }
      if (near[0]) { this.approach('portal', near[0].id); return; }
      this.message('Hãy chọn người hướng dẫn, cổng hoặc linh thú trên bản đồ.');
    }
  }

  // ---------- trận đấu ----------
  confirmTarget(): void {
    if (!this.session.character.value?.battle) return;
    const a = this.selectedAction.value;
    this.battleSend(a?.choice ?? 'attack', a?.skill_id ?? '', a?.item_id ?? '');
  }
  battleSend(choice: string, skill = '', item = ''): void {
    const s = this.session; const b = s.character.value?.battle;
    if (!b || s.busy.value || this.pres.isAnimating()) return;
    this.selectedAction.value = null; this.close(); this.actionDelay = 0.8;
    const data: Record<string, unknown> = { battle_id: b.id, turn: Math.trunc(b.turn), choice };
    if (skill) data.skill_id = skill; if (item) data.item_id = item;
    void s.send('battle.action', data as never);
  }
  chooseSkill(skillId: string): void { this.selectedAction.value = { choice: 'skill', skill_id: skillId }; this.automatic.value = false; this.close(); }
  chooseCapture(): void { this.selectedAction.value = { choice: 'capture' }; this.automatic.value = false; this.close(); }

  // ---------- menu ----------
  open(p: Page | 'Menu' | 'Supplies'): void {
    this.held = ''; this.destination = null;
    if (p === 'Menu') { this.shortcuts.value = !this.shortcuts.value; return; }
    this.shortcuts.value = false;
    if (p === 'World') { this.close(); return; }
    this.page.value = p === 'Supplies' ? 'Inventory' : p;
    this.tick.value++;
  }
  close(): void { this.page.value = 'World'; this.shortcuts.value = false; }

  menuDirection(dir: Dir): void {
    const root = document.querySelector('[data-menu]'); if (!root) return;
    const list = [...root.querySelectorAll<HTMLElement>('button:not(:disabled),select,input,[tabindex="0"]')].filter((e) => e.offsetParent !== null);
    if (!list.length) return;
    const i = list.indexOf(document.activeElement as HTMLElement);
    const next = i < 0 ? 0 : (i + (dir === 'up' || dir === 'left' ? -1 : 1) + list.length) % list.length;
    list[next]!.focus();
  }

  // ---------- thao tác từ cảnh ----------
  pick(h: { kind: string; id?: string; dir?: Dir }): void {
    if (h.kind === 'pillar') this.open('Teleport');
    else if (h.kind === 'npc' && h.id) this.approach('npc', h.id);
    else if (h.kind === 'portal' && h.id) this.approach('portal', h.id);
    else if (h.kind === 'enemy' && h.id) this.approach('enemy', h.id);
    else if (h.kind === 'target' && h.id) { this.pres.selectedTarget = h.id; this.confirmTarget(); }
    else if (h.kind === 'ground' && h.dir) this.move(h.dir);
  }

  // ---------- dữ liệu cho UI ----------
  pets(): Pet[] { return (this.session.character.value?.pets ?? []).filter((p) => !p.retired); }
  nearby(): ReturnType<Game['nearestNpc']> { return this.nearestNpc(); }
  send<K extends Parameters<Session['send']>[0]>(op: K, data: Parameters<Session['send']>[1]): Promise<unknown> { return this.session.send(op, data as never); }
}
