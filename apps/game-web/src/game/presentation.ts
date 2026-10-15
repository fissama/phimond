import type { Battle, BattleEvent, BattleUnit, Catalog, Character } from '@phimond/protocol';

/**
 * Trạng thái trình diễn thuần logic (port từ room.gd): vị trí hiển thị nội suy 0,18 s/ô, xem trước bước đi,
 * chọn trận, hàng đợi hiệu ứng từ events (mỗi revision đúng một lần), HP hiển thị, đếm ngược kết thúc trận.
 * Không phụ thuộc WebGL nên kiểm thử được bằng vitest.
 */
export const STEP_SECONDS = 0.18;
export type FxKind = 'skill_cast' | 'damage' | 'heal' | 'status_applied' | 'miss';
export interface Fx { type: FxKind; actor_id: string; target_id: string; amount: number; start: number; end: number; message: string }
export type Spawn = { id: string; species_id: string; x: number; y: number };

const FX_KINDS: ReadonlySet<string> = new Set(['skill_cast', 'damage', 'heal', 'status_applied', 'miss']);

export class Presentation {
  elapsed = 0;
  character: Character | null = null;
  catalog: Catalog | null = null;
  displayedX = -1;
  displayedY = 12;
  lastPosition = -1;
  lastMap = '';
  walkingUntil = 0;
  facingLeft = false;
  selectedTarget = '';
  battle: Battle | null = null;
  battleId = '';
  batchRevision = -1;
  finishUntil = 0;
  effects: Fx[] = [];
  hpDisplay = new Map<string, number>();
  deathStarted = new Map<string, number>();
  transition = 0;
  private previewX = -1;
  private previewY = -1;
  private previewUntil = 0;
  mapChanged: ((mapId: string) => void) | null = null;

  get mapId(): string { return this.character?.map_id ?? 'severa'; }
  get definition() { return this.catalog?.maps[this.mapId]; }

  setSnapshot(character: Character, catalog: Catalog): void {
    const oldMap = this.character?.map_id ?? '';
    this.character = character; this.catalog = catalog;
    this.cancelPreview();
    if (oldMap !== character.map_id) this.syncMap();
    this.syncBattle();
  }

  previewMove(direction: string): void {
    if (this.battle || !this.character) return;
    if (!['left', 'right', 'up', 'down'].includes(direction)) return;
    const step = direction === 'left' || direction === 'up' ? -1 : 1;
    const def = this.definition;
    this.previewX = this.character.x; this.previewY = this.character.y;
    if (direction === 'up' || direction === 'down') this.previewY = clamp(this.previewY + step, 0, (def?.height || 24) - 1);
    else { this.previewX = clamp(this.previewX + step, 0, (def?.width || 40) - 1); this.facingLeft = step < 0; }
    this.previewUntil = this.elapsed + 1.5;
    this.walkingUntil = this.elapsed + 0.3;
  }

  cancelPreview(): void { this.previewX = -1; this.previewY = -1; this.previewUntil = 0; }

  syncMap(): void {
    const c = this.character; if (!c) return;
    if (c.map_id !== this.lastMap) {
      this.displayedX = c.x; this.displayedY = c.y; this.lastPosition = c.x; this.lastMap = c.map_id; this.transition = 0.2;
      this.mapChanged?.(c.map_id);
    }
  }

  private syncBattle(): void { this.selectBattle(this.character?.battle ?? null); }

  resetPresentation(): void {
    this.batchRevision = -1; this.finishUntil = 0; this.effects = []; this.hpDisplay.clear(); this.deathStarted.clear();
    this.battle = null; this.battleId = ''; this.selectedTarget = ''; this.character = null; this.cancelPreview();
  }

  /** Mỗi revision chỉ áp một lần; revision cũ bị bỏ. */
  applyStateBatch(revision: number, character: Character, catalog: Catalog, events: BattleEvent[], presentation: { battle_id?: string; completed_battle?: Battle } | undefined): void {
    if (revision <= this.batchRevision) return;
    this.batchRevision = revision;
    this.character = character; this.catalog = catalog;
    this.cancelPreview();
    this.syncMap();
    const next = character.battle ?? null;
    const completed = presentation?.completed_battle;
    const terminal = !next && !!completed && !!presentation?.battle_id && completed.id === presentation.battle_id && Array.isArray(completed.units);
    if (terminal) this.selectBattle(completed!);
    else if (next || this.finishUntil <= this.elapsed) this.selectBattle(next);
    if (this.battle && (presentation?.battle_id ?? '') === this.battleId) this.queueEvents(events);
    if (terminal) {
      this.finishUntil = this.elapsed + 0.6;
      for (const e of this.effects) this.finishUntil = Math.max(this.finishUntil, e.end + 0.2);
    }
  }

  private selectBattle(next: Battle | null): void {
    const id = next?.id ?? '';
    if (id !== this.battleId) {
      this.battleId = id; this.finishUntil = 0; this.effects = []; this.hpDisplay.clear(); this.deathStarted.clear(); this.selectedTarget = '';
      for (const u of next?.units ?? []) if (u.side !== 'player' && u.hp > 0) { this.selectedTarget = u.id; break; }
    }
    this.battle = next;
    for (const u of next?.units ?? []) if (u.hp > 0) this.deathStarted.delete(u.id);
  }

  private queueEvents(events: BattleEvent[]): void {
    let start = this.elapsed;
    for (const e of this.effects) start = Math.max(start, e.end);
    const ids = new Set((this.battle?.units ?? []).map((u) => u.id));
    let available = start;
    for (const ev of events) {
      if (!FX_KINDS.has(ev.type)) continue;
      if (!ids.has(ev.target_id)) continue;
      if (ev.type === 'skill_cast') start = Math.max(start, available) + 0.12;
      const fx: Fx = { type: ev.type as FxKind, actor_id: ev.actor_id, target_id: ev.target_id, amount: ev.amount, message: ev.message, start, end: start + (ev.type === 'skill_cast' ? 0.65 : 1.1) };
      this.effects.push(fx);
      available = Math.max(available, fx.end);
      if (ev.type === 'damage') start += 0.28;
    }
  }

  update(dt: number): void {
    this.elapsed += dt;
    this.syncMap();
    const c = this.character;
    if (c?.battle && c.battle.id !== this.battleId) this.syncBattle();
    if (this.finishUntil > 0 && this.elapsed >= this.finishUntil) { this.battle = null; this.battleId = ''; this.finishUntil = 0; this.selectedTarget = ''; }
    if (!c) return;
    let target = c.x;
    if (this.previewX >= 0 && this.elapsed < this.previewUntil) target = this.previewX;
    if (target !== this.lastPosition) { this.facingLeft = target < this.lastPosition; this.walkingUntil = this.elapsed + 0.25; this.lastPosition = target; }
    this.displayedX = moveToward(this.displayedX, target, dt / STEP_SECONDS);
    const ty = this.previewY >= 0 && this.elapsed < this.previewUntil ? this.previewY : c.y;
    if (Math.abs(this.displayedY - ty) > 0.01) this.walkingUntil = this.elapsed + 0.15;
    this.displayedY = moveToward(this.displayedY, ty, dt / STEP_SECONDS);
    this.transition = Math.max(0, this.transition - dt);
    this.effects = this.effects.filter((e) => this.elapsed < e.end);
    for (const u of this.battle?.units ?? []) {
      const cur = this.hpDisplay.get(u.id) ?? u.hp; const max = Math.max(u.max_hp, 1);
      this.hpDisplay.set(u.id, moveToward(cur, u.hp, (max / 12) * (dt * 60)));
    }
  }

  isAnimating(): boolean { return this.effects.length > 0 || this.finishUntil > this.elapsed; }

  /** Quái hoang chạm người chơi: |dx|<=1 và |dy|<=1 (cùng ô hitbox server kiểm tra). */
  contactSpawn(x: number, y: number): Spawn | null {
    for (const s of this.definition?.wild_spawns ?? []) if (Math.abs(x - s.x) <= 1 && Math.abs(y - s.y) <= 1) return s as Spawn;
    return null;
  }

  get walking(): boolean { return this.elapsed < this.walkingUntil; }
  unitById(id: string): BattleUnit | undefined { return this.battle?.units.find((u) => u.id === id); }
}

export const clamp = (v: number, a: number, b: number): number => Math.max(a, Math.min(b, v));
export function moveToward(from: number, to: number, delta: number): number {
  if (Math.abs(to - from) <= delta) return to;
  return from + Math.sign(to - from) * delta;
}
