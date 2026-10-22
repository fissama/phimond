import { STEP, type Cell, type Direction } from './coords.ts';
import type { Grid } from './grid.ts';
import { stepDir } from './grid.ts';

export type MoveResult = { ok: true } | { ok: false; message: string };
export type MoveSender = (dir: Direction) => Promise<MoveResult>;

/** Tối đa số bước đã gửi mà server chưa xác nhận (P01 §9 D1: pipeline). */
export const MAX_PENDING = 4;
/** Tốc độ đi khởi đầu (ô/giây), chỉnh trong review gameplay R06. */
export const WALK_SPEED = 4;

/**
 * Điều khiển di chuyển phía client (P01-R03):
 * - Đi mượt giữa các ô; mỗi lần bắt đầu sang ô mới gửi một `world.move`, không chờ ack ô trước (tối đa MAX_PENDING).
 * - Chỉ bước vào ô đi được theo cùng lưới với server, nên không xuyên vật cản.
 * - Server từ chối hoặc lệch: khi không còn bước chờ, kéo về vị trí server xác nhận (đối soát).
 * - `paused` (menu/hội thoại/trận/mất focus) dừng ngay ở ô hiện tại, bỏ hướng giữ và đường đi.
 */
export class Mover {
  /** Ô logic hiện tại (đích của bước đang đi, hoặc ô đang đứng). */
  cell: Cell;
  /** Ô xuất phát của bước đang đi. */
  private from: Cell;
  private progress = 1;
  /** Vị trí server đã xác nhận. */
  auth: Cell;
  mapId: string;
  facing: Direction = 'down';
  held: Direction | null = null;
  /** Bước lẻ từ một lần nhấn nhanh (nhấn và nhả trước khung hình kế tiếp vẫn đi một ô). */
  tap: Direction | null = null;
  path: Cell[] = [];
  pending = 0;
  paused = false;
  speed = WALK_SPEED;
  private holdUntil = 0;
  private clock = 0;
  /** Gọi khi đi hết đường đi (để tương tác với đích). */
  onPathDone: (() => void) | null = null;
  /** Kiểm khi vừa tới một ô: trả true để dừng tại đó (vào vùng cổng, kề quái). */
  stopAt: ((c: Cell) => boolean) | null = null;
  /** Gọi khi bị chặn/từ chối, kèm lý do để hiển thị. */
  onBlocked: ((message: string) => void) | null = null;

  constructor(
    private grid: Grid,
    mapId: string,
    at: Cell,
    private readonly send: MoveSender,
  ) {
    this.mapId = mapId;
    this.cell = { ...at };
    this.from = { ...at };
    this.auth = { ...at };
  }

  get moving(): boolean {
    return this.progress < 1;
  }

  /** Vị trí hiển thị (số thực, theo ô). */
  get pos(): { x: number; y: number } {
    const t = Math.min(1, this.progress);
    return { x: this.from.x + (this.cell.x - this.from.x) * t, y: this.from.y + (this.cell.y - this.from.y) * t };
  }

  /** Đứng yên đúng ở vị trí server đã xác nhận, không còn bước chờ: an toàn để gửi intent khác. */
  get settled(): boolean {
    return !this.moving && this.pending === 0 && this.cell.x === this.auth.x && this.cell.y === this.auth.y;
  }

  /** Trạng thái server mới (mỗi lô state). Đổi map/vị trí ngoài dự đoán khi không chờ bước nào → đặt lại. */
  setAuthoritative(mapId: string, at: Cell, grid?: Grid): void {
    const teleported = mapId !== this.mapId;
    this.auth = { ...at };
    if (teleported) {
      this.mapId = mapId;
      if (grid) this.grid = grid;
      this.place(at);
      return;
    }
    this.reconcile();
  }

  /** Đặt ngay vào ô (dịch chuyển), bỏ mọi kế hoạch đi. */
  place(at: Cell): void {
    this.cell = { ...at };
    this.from = { ...at };
    this.auth = { ...at };
    this.progress = 1;
    this.path = [];
  }

  walkTo(path: Cell[], onDone: (() => void) | null = null): void {
    this.path = path.slice();
    this.onPathDone = onDone;
    if (path.length === 0 && onDone) {
      this.onPathDone = null;
      onDone();
    }
  }

  stop(): void {
    this.held = null;
    this.tap = null;
    this.path = [];
    this.onPathDone = null;
  }

  setPaused(p: boolean): void {
    this.paused = p;
    if (p) this.stop();
  }

  update(dt: number): void {
    this.clock += dt;
    if (this.moving) {
      this.progress += dt * this.speed;
      if (this.progress < 1) return;
      // Đến ô: phần dư dùng cho bước kế tiếp để chuyển động liền mạch khi giữ phím.
      const carry = Math.min(0.5, this.progress - 1);
      this.progress = 1;
      this.from = { ...this.cell };
      if (this.stopAt?.(this.cell)) this.stop();
      if (this.path.length === 0 && this.onPathDone) {
        const done = this.onPathDone;
        this.onPathDone = null;
        done();
      }
      if (this.tryStep()) this.progress = carry;
      return;
    }
    this.reconcile();
    this.tryStep();
  }

  private tryStep(): boolean {
    if (this.paused || this.clock < this.holdUntil) return false;
    let dir: Direction | null = null;
    let fromPath = false;
    if (this.path.length > 0) {
      dir = stepDir(this.cell, this.path[0]!);
      fromPath = true;
      if (!dir) {
        this.path = [];
        return false;
      }
    } else if (this.held || this.tap) {
      dir = this.held ?? this.tap;
    }
    if (!dir) return false;
    this.facing = dir;
    const next = { x: this.cell.x + STEP[dir].x, y: this.cell.y + STEP[dir].y };
    if (!this.grid.walkable(next.x, next.y)) {
      if (fromPath) {
        this.path = [];
        this.onPathDone = null;
        this.onBlocked?.('Không đi tới được');
      }
      return false;
    }
    if (this.pending >= MAX_PENDING) return false;
    if (fromPath) this.path.shift();
    this.tap = null;
    this.from = { ...this.cell };
    this.cell = next;
    this.progress = 0;
    this.pending++;
    const mapAtSend = this.mapId;
    void this.send(dir).then((r) => {
      this.pending = Math.max(0, this.pending - 1);
      if (mapAtSend !== this.mapId) return;
      if (!r.ok) {
        // Server từ chối: bỏ kế hoạch, dừng ngắn rồi kéo về vị trí xác thực khi hết bước chờ.
        this.path = [];
        this.onPathDone = null;
        this.holdUntil = this.clock + 0.25;
        this.onBlocked?.(r.message);
      }
      this.reconcile();
    });
    return true;
  }

  private reconcile(): void {
    if (this.pending > 0 || this.moving) return;
    if (this.cell.x !== this.auth.x || this.cell.y !== this.auth.y) this.place(this.auth);
  }
}
