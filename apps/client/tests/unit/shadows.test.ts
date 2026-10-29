import { describe, expect, it } from 'vitest';
import { sunFor } from '../../src/render/shadows.ts';

describe('sunFor (hướng và độ dài bóng theo giờ)', () => {
  it('sáng bóng đổ về tây (−x), chiều đổ về đông (+x), luôn lùi ra sau (−z)', () => {
    const am = sunFor(7, 0);
    const pm = sunFor(17, 0);
    expect(am.dx).toBeLessThan(-0.5);
    expect(pm.dx).toBeGreaterThan(0.5);
    expect(am.dz).toBeLessThan(0);
    expect(pm.dz).toBeLessThan(0);
    expect(Math.hypot(am.dx, am.dz)).toBeCloseTo(1, 5);
  });
  it('trưa bóng ngắn nhất, sáng sớm/chiều muộn dài hơn nhưng có trần', () => {
    const noon = sunFor(12, 0).stretch;
    expect(noon).toBeGreaterThanOrEqual(1);
    expect(sunFor(7, 0).stretch).toBeGreaterThan(noon);
    expect(sunFor(17.5, 0).stretch).toBeGreaterThan(noon);
    for (const h of [0, 5, 6, 12, 18, 24]) expect(sunFor(h, 0).stretch).toBeLessThanOrEqual(2.6);
  });
  it('về đêm bóng mờ đi nhưng vẫn còn một chút', () => {
    expect(sunFor(12, 0).alpha).toBeGreaterThan(sunFor(23, 1).alpha);
    expect(sunFor(23, 1).alpha).toBeGreaterThan(0);
    expect(sunFor(23, 1).alpha).toBeLessThan(0.2);
  });
});
