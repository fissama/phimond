import type { Cell } from './coords.ts';
import type { Grid } from './grid.ts';

const key = (x: number, y: number) => y * 4096 + x;

/**
 * A* 4 hướng trên lưới đi được (cùng lưới server dùng nên đường đi luôn hợp lệ với server).
 * `goals` là tập ô đích chấp nhận được (ví dụ mọi ô kề NPC). Trả danh sách ô KHÔNG gồm ô xuất phát,
 * [] nếu đã đứng ở đích, null nếu không tới được. Giới hạn `maxNodes` để không treo khung hình.
 */
export function findPath(grid: Grid, start: Cell, goals: Cell[], maxNodes = 6000): Cell[] | null {
  const goalSet = new Set(goals.filter((g) => grid.walkable(g.x, g.y)).map((g) => key(g.x, g.y)));
  if (goalSet.size === 0) return null;
  if (goalSet.has(key(start.x, start.y))) return [];
  const h = (x: number, y: number) => {
    let best = Infinity;
    for (const g of goals) best = Math.min(best, Math.abs(g.x - x) + Math.abs(g.y - y));
    return best;
  };
  const open: { x: number; y: number; f: number; g: number }[] = [{ x: start.x, y: start.y, g: 0, f: h(start.x, start.y) }];
  const came = new Map<number, number>();
  const gScore = new Map<number, number>([[key(start.x, start.y), 0]]);
  let visited = 0;
  while (open.length > 0 && visited < maxNodes) {
    let bi = 0;
    for (let i = 1; i < open.length; i++) if (open[i]!.f < open[bi]!.f) bi = i;
    const cur = open.splice(bi, 1)[0]!;
    visited++;
    const ck = key(cur.x, cur.y);
    if (goalSet.has(ck)) {
      const path: Cell[] = [];
      let k: number | undefined = ck;
      while (k !== undefined && k !== key(start.x, start.y)) {
        path.push({ x: k % 4096, y: Math.floor(k / 4096) });
        k = came.get(k);
      }
      return path.reverse();
    }
    for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]] as const) {
      const nx = cur.x + dx;
      const ny = cur.y + dy;
      if (!grid.walkable(nx, ny)) continue;
      const nk = key(nx, ny);
      const g = cur.g + 1;
      if (g < (gScore.get(nk) ?? Infinity)) {
        gScore.set(nk, g);
        came.set(nk, ck);
        open.push({ x: nx, y: ny, g, f: g + h(nx, ny) });
      }
    }
  }
  return null;
}

/** Các ô kề (kể cả chéo) quanh một ô — nơi đứng để tương tác (Chebyshev ≤ 1). */
export function around(c: Cell): Cell[] {
  const out: Cell[] = [];
  for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if (dx || dy) out.push({ x: c.x + dx, y: c.y + dy });
  return out;
}

/** Các ô trong vùng chữ nhật [x, y, w, h]. */
export function rectCells(r: readonly [number, number, number, number]): Cell[] {
  const out: Cell[] = [];
  for (let y = r[1]; y < r[1] + r[3]; y++) for (let x = r[0]; x < r[0] + r[2]; x++) out.push({ x, y });
  return out;
}
