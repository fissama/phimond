import { describe, expect, it } from 'vitest';
import { Grid, stepDir } from '../../src/world/grid.ts';
import { around, findPath, rectCells } from '../../src/world/path.ts';
import { MAX_PENDING, Mover, type MoveResult } from '../../src/world/mover.ts';
import type { Direction } from '../../src/world/coords.ts';

// 6×5, tường giữa có một khe ở (3,3).
//   ######
//   #..#.#
//   #..#.#
//   #....#
//   ######
const WALK = '6#/1#2.1#1.1#/1#2.1#1.1#/1#4.1#/6#';
const grid = () => Grid.parse(WALK, 6, 5);

describe('Grid', () => {
  it('đọc RLE giống server', () => {
    const g = grid();
    expect(g.walkable(1, 1)).toBe(true);
    expect(g.walkable(3, 1)).toBe(false);
    expect(g.walkable(3, 3)).toBe(true);
    expect(g.walkable(-1, 0)).toBe(false);
    expect(() => Grid.parse('3./3.', 4, 2)).toThrow();
  });
  it('stepDir chỉ nhận bước kề 4 hướng', () => {
    expect(stepDir({ x: 1, y: 1 }, { x: 2, y: 1 })).toBe('right');
    expect(stepDir({ x: 1, y: 1 }, { x: 2, y: 2 })).toBeNull();
  });
});

describe('findPath', () => {
  it('đi vòng qua tường theo đường ngắn nhất', () => {
    const p = findPath(grid(), { x: 1, y: 1 }, [{ x: 4, y: 1 }])!;
    expect(p.at(-1)).toEqual({ x: 4, y: 1 });
    expect(p).toHaveLength(7);
    for (const c of p) expect(grid().walkable(c.x, c.y)).toBe(true);
  });
  it('đích bị chặn → null; đã ở đích → []', () => {
    expect(findPath(grid(), { x: 1, y: 1 }, [{ x: 3, y: 1 }])).toBeNull();
    expect(findPath(grid(), { x: 1, y: 1 }, [{ x: 1, y: 1 }])).toEqual([]);
  });
  it('đi tới ô kề NPC (đích nhiều ô)', () => {
    const p = findPath(grid(), { x: 1, y: 3 }, around({ x: 3, y: 1 }))!;
    expect(p.at(-1)).toEqual({ x: 2, y: 2 });
    expect(rectCells([1, 1, 2, 1])).toEqual([{ x: 1, y: 1 }, { x: 2, y: 1 }]);
  });
});

function harness(at = { x: 1, y: 3 }) {
  const sent: { dir: Direction; resolve: (r: MoveResult) => void }[] = [];
  const m = new Mover(grid(), 'm', at, (dir) => new Promise((resolve) => sent.push({ dir, resolve })));
  const blocked: string[] = [];
  m.onBlocked = (msg) => blocked.push(msg);
  return { m, sent, blocked };
}
const flush = () => new Promise((r) => setTimeout(r, 0));

describe('Mover', () => {
  it('giữ phím: gửi một move mỗi ô, không chờ ack, tối đa MAX_PENDING', () => {
    const { m, sent } = harness({ x: 1, y: 3 });
    m.held = 'right';
    for (let i = 0; i < 40; i++) m.update(0.05);
    expect(sent.map((s) => s.dir)).toEqual(['right', 'right', 'right']); // tới (4,3) thì đụng tường
    expect(m.cell).toEqual({ x: 4, y: 3 });
    expect(sent.length).toBeLessThanOrEqual(MAX_PENDING);
  });

  it('không bước vào ô chặn, chỉ quay mặt', () => {
    const { m, sent } = harness({ x: 1, y: 1 });
    m.held = 'up';
    m.update(0.1);
    expect(sent).toHaveLength(0);
    expect(m.facing).toBe('up');
    expect(m.cell).toEqual({ x: 1, y: 1 });
  });

  it('dừng ngay khi mở menu/vào trận (paused)', () => {
    const { m, sent } = harness();
    m.held = 'right';
    m.update(0.01);
    m.setPaused(true);
    for (let i = 0; i < 20; i++) m.update(0.05);
    expect(sent).toHaveLength(1);
    expect(m.moving).toBe(false);
    expect(m.held).toBeNull();
  });

  it('server từ chối → kéo về vị trí xác thực, báo lý do', async () => {
    const { m, sent, blocked } = harness({ x: 1, y: 3 });
    m.held = 'right';
    for (let i = 0; i < 6; i++) m.update(0.05);
    m.held = null;
    for (let i = 0; i < 10; i++) m.update(0.05);
    sent[0]!.resolve({ ok: false, message: 'Không đi được vào đó' });
    for (const s of sent.slice(1)) s.resolve({ ok: false, message: 'x' });
    await flush();
    m.update(0.01);
    expect(blocked[0]).toBe('Không đi được vào đó');
    expect(m.cell).toEqual({ x: 1, y: 3 });
  });

  it('server xác nhận → giữ vị trí dự đoán, settled', async () => {
    const { m, sent } = harness({ x: 1, y: 3 });
    m.walkTo([{ x: 2, y: 3 }, { x: 3, y: 3 }]);
    for (let i = 0; i < 20; i++) m.update(0.05);
    m.setAuthoritative('m', { x: 2, y: 3 });
    m.setAuthoritative('m', { x: 3, y: 3 });
    sent.forEach((s) => s.resolve({ ok: true }));
    await flush();
    m.update(0.01);
    expect(m.cell).toEqual({ x: 3, y: 3 });
    expect(m.settled).toBe(true);
  });

  it('đi theo đường rồi gọi onPathDone; đường bị chặn thì báo', () => {
    const { m, blocked } = harness({ x: 1, y: 3 });
    let done = false;
    m.walkTo([{ x: 2, y: 3 }], () => (done = true));
    for (let i = 0; i < 10; i++) m.update(0.05);
    expect(done).toBe(true);
    m.walkTo([{ x: 2, y: 2 }, { x: 3, y: 2 }]);
    for (let i = 0; i < 10; i++) m.update(0.05);
    expect(blocked).toContain('Không đi tới được');
  });

  it('đổi map (dịch chuyển) đặt lại vị trí và lưới', () => {
    const { m } = harness();
    m.path = [{ x: 2, y: 3 }];
    m.setAuthoritative('other', { x: 4, y: 1 }, grid());
    expect(m.mapId).toBe('other');
    expect(m.cell).toEqual({ x: 4, y: 1 });
    expect(m.path).toHaveLength(0);
  });
});

describe('Mover nhấn nhanh', () => {
  it('nhấn và nhả phím trước khung hình kế tiếp vẫn đi đúng một ô', () => {
    const sent: Direction[] = [];
    const m = new Mover(grid(), 'm', { x: 1, y: 3 }, (d) => (sent.push(d), new Promise(() => undefined)));
    m.tap = 'right';
    m.held = null;
    for (let i = 0; i < 20; i++) m.update(0.05);
    expect(sent).toEqual(['right']);
    expect(m.cell).toEqual({ x: 2, y: 3 });
  });
});
