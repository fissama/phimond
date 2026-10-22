import type { Cell, Direction } from './coords.ts';

/** Lưới đi được của một map (ADR-P01-01). Ô ngoài biên luôn bị chặn. Cùng dữ liệu với server. */
export class Grid {
  private constructor(
    readonly w: number,
    readonly h: number,
    private readonly cells: Uint8Array,
  ) {}

  /** Đọc chuỗi RLE: hàng nối bằng '/', mỗi hàng "<số><ký tự>", '.' đi được, '#' chặn. */
  static parse(walk: string, w: number, h: number): Grid {
    const rows = walk.split('/');
    if (rows.length !== h) throw new Error(`lưới có ${rows.length} hàng, cần ${h}`);
    const cells = new Uint8Array(w * h);
    rows.forEach((row, y) => {
      let x = 0;
      for (const m of row.matchAll(/(\d+)([.#])/g)) {
        const n = Number(m[1]);
        if (m[2] === '.') cells.fill(1, y * w + x, y * w + x + n);
        x += n;
      }
      if (x !== w) throw new Error(`hàng ${y} có ${x} ô, cần ${w}`);
    });
    return new Grid(w, h, cells);
  }

  walkable(x: number, y: number): boolean {
    return x >= 0 && y >= 0 && x < this.w && y < this.h && this.cells[y * this.w + x] === 1;
  }
}

export const DIRS: Direction[] = ['up', 'down', 'left', 'right'];

export function stepDir(from: Cell, to: Cell): Direction | null {
  const dx = to.x - from.x;
  const dy = to.y - from.y;
  if (Math.abs(dx) + Math.abs(dy) !== 1) return null;
  return dx === 1 ? 'right' : dx === -1 ? 'left' : dy === 1 ? 'down' : 'up';
}
