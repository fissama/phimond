// Hệ tọa độ chung (P01-R01, ADR-P01-01):
// - Gameplay: ô nguyên (x, y), x tăng sang phải, y tăng xuống dưới màn hình (về phía camera). 1 ô = 1 đơn vị world.
// - Three.js: X world = x, Z world = y, mặt đất ở Y = 0. Tâm ô (x, y) nằm ở (x + 0.5, 0, y + 0.5).
// - Art: 128 px = 1 đơn vị (nền xa 64 px/đơn vị).

export const PX_PER_UNIT = 128;

export interface Cell {
  x: number;
  y: number;
}

export function cellCenter(c: Cell): { x: number; z: number } {
  return { x: c.x + 0.5, z: c.y + 0.5 };
}

/** Khoảng cách Chebyshev: tầm tương tác xét cả hai trục (P01-R04). */
export function chebyshev(a: Cell, b: Cell): number {
  return Math.max(Math.abs(a.x - b.x), Math.abs(a.y - b.y));
}

export type Direction = 'left' | 'right' | 'up' | 'down';

export const STEP: Record<Direction, Cell> = {
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 },
};
