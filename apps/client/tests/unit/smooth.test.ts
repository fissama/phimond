import { describe, expect, it } from 'vitest';
import { approach, follow, walkSpeed } from '../../src/world/smooth.ts';

describe('làm mượt chuyển động', () => {
  it('follow hội tụ về đích và không phụ thuộc nhịp khung hình', () => {
    let a = 0;
    for (let i = 0; i < 60; i++) a = follow(a, 1, 1 / 60, 24);
    let b = 0;
    for (let i = 0; i < 30; i++) b = follow(b, 1, 1 / 30, 24);
    expect(a).toBeGreaterThan(0.99);
    expect(Math.abs(a - b)).toBeLessThan(1e-9);
  });

  it('approach không vượt đích', () => {
    expect(approach(0, 1, 0.4)).toBeCloseTo(0.4);
    expect(approach(0.9, 1, 0.4)).toBe(1);
    expect(approach(1, 0, 0.4)).toBeCloseTo(0.6);
  });

  it('người đi bộ tăng tốc dần rồi giảm tốc khi gần đích', () => {
    let v = 0;
    const dt = 1 / 60;
    let remaining = 6;
    const trace: number[] = [];
    while (remaining > 0.02 && trace.length < 2000) {
      v = walkSpeed(v, 1.3, remaining, dt);
      remaining -= v * dt;
      trace.push(v);
    }
    expect(trace[0]).toBeLessThan(0.6); // không xuất phát hết tốc
    expect(Math.max(...trace)).toBeCloseTo(1.3, 1);
    expect(trace.at(-1)!).toBeLessThan(0.8); // chậm lại khi tới nơi
    for (let i = 1; i < trace.length; i++) expect(Math.abs(trace[i]! - trace[i - 1]!)).toBeLessThan(0.1); // không đổi vọt
  });
});
