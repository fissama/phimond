import * as THREE from 'three';
import { describe, expect, it } from 'vitest';
import { groupBySignature, packShelves } from '../../vite-atlas.ts';
import { setFrame, uvRect } from '../../src/render/assets.ts';

// AD3: xếp atlas không chồng ô, có viền; gom ảnh theo tập map; chọn khung đúng trong ô atlas.
describe('packShelves', () => {
  it('không chồng nhau, nằm trong trang, chừa viền', () => {
    const items = Array.from({ length: 60 }, (_, i) => ({ id: `a${i}`, w: 40 + ((i * 37) % 300), h: 30 + ((i * 53) % 200) }));
    const pad = 2;
    const { placed, pages } = packShelves(items, 1024, pad);
    expect(placed).toHaveLength(60);
    for (const p of placed) {
      const pg = pages[p.page]!;
      expect(p.x - pad).toBeGreaterThanOrEqual(0);
      expect(p.y - pad).toBeGreaterThanOrEqual(0);
      expect(p.x + p.w + pad).toBeLessThanOrEqual(pg.w);
      expect(p.y + p.h + pad).toBeLessThanOrEqual(pg.h);
      expect(pg.w).toBeLessThanOrEqual(1024);
      expect(pg.h).toBeLessThanOrEqual(1024);
    }
    for (const a of placed)
      for (const b of placed) {
        if (a === b || a.page !== b.page) continue;
        const sep = a.x + a.w + pad <= b.x - pad || b.x + b.w + pad <= a.x - pad || a.y + a.h + pad <= b.y - pad || b.y + b.h + pad <= a.y - pad;
        expect(sep, `${a.id} chồng ${b.id}`).toBe(true);
      }
  });

  it('ảnh lớn hơn trang thì báo lỗi', () => {
    expect(() => packShelves([{ id: 'x', w: 2100, h: 10 }])).toThrow();
  });
});

describe('groupBySignature', () => {
  it('ảnh chỉ một map dùng ở nhóm riêng; ảnh dùng chung ở nhóm đúng các map@preset đó', () => {
    const g = groupBySignature({
      a: { low: ['bush', 'tree'], high: ['bush', 'lamp', 'tree'] },
      b: { low: ['tree', 'well'], high: ['tree', 'well'] },
    });
    expect(g.get('a@high+a@low')).toEqual(['bush']);
    expect(g.get('a@high')).toEqual(['lamp']); // chỉ preset cao dùng: preset thấp không tải
    expect(g.get('b@high+b@low')).toEqual(['well']);
    expect(g.get('a@high+a@low+b@high+b@low')).toEqual(['tree']);
  });
});

describe('setFrame', () => {
  it('ảnh lẻ: như repeat 1/n + offset f/n', () => {
    const t = new THREE.Texture();
    setFrame(t, 2, 4);
    expect([t.repeat.x, t.repeat.y, t.offset.x, t.offset.y]).toEqual([0.25, 1, 0.5, 0]);
  });
  it('ô atlas: khung nằm trong ô', () => {
    const t = new THREE.Texture();
    t.userData.rect = { u: 0.5, v: 0.25, w: 0.4, h: 0.2 };
    setFrame(t, 1, 4);
    expect(t.repeat.x).toBeCloseTo(0.1);
    expect(t.repeat.y).toBeCloseTo(0.2);
    expect(t.offset.x).toBeCloseTo(0.6);
    expect(t.offset.y).toBeCloseTo(0.25);
    expect(uvRect(t).w).toBeCloseTo(0.4);
  });
});
