export type TimeMode = 'auto' | 'day' | 'dusk' | 'night';

/** Ánh sáng theo giờ: màu nhân (tint), độ bão hòa, độ sáng; `night`/`day` (0..1) điều khiển đèn lồng, tia nắng... */
export interface Light {
  tint: [number, number, number];
  sat: number;
  bright: number;
  night: number;
  day: number;
}

// [giờ, tint, sat, bright, night, day] — nội suy tuyến tính, vòng 24 giờ.
const KEYS: [number, [number, number, number], number, number, number, number][] = [
  [0, [0.4, 0.52, 1.0], 0.8, 0.56, 1, 0],
  [5, [0.4, 0.52, 1.0], 0.8, 0.56, 1, 0],
  [6.5, [1.08, 0.9, 0.84], 1.12, 0.94, 0.35, 0.3],
  [8, [1, 1, 1], 1.06, 1, 0, 1],
  [16.5, [1, 0.99, 0.96], 1.06, 1, 0, 1],
  [18, [1.1, 0.8, 0.68], 1.18, 0.9, 0.3, 0.35],
  [19.5, [0.5, 0.58, 0.95], 0.88, 0.66, 0.9, 0],
  [24, [0.4, 0.52, 1.0], 0.8, 0.56, 1, 0],
];
const FIXED: Record<Exclude<TimeMode, 'auto'>, number> = { day: 12, dusk: 17.9, night: 22 };

const mix = (a: number, b: number, t: number) => a + (b - a) * t;

export function lightAt(mode: TimeMode, now: Date = new Date()): Light {
  const h = mode === 'auto' ? now.getHours() + now.getMinutes() / 60 : FIXED[mode];
  let i = 0;
  while (i < KEYS.length - 2 && h >= KEYS[i + 1]![0]) i++;
  const a = KEYS[i]!;
  const b = KEYS[i + 1]!;
  const t = Math.min(1, Math.max(0, (h - a[0]) / (b[0] - a[0])));
  return {
    tint: [mix(a[1][0], b[1][0], t), mix(a[1][1], b[1][1], t), mix(a[1][2], b[1][2], t)],
    sat: mix(a[2], b[2], t),
    bright: mix(a[3], b[3], t),
    night: mix(a[4], b[4], t),
    day: mix(a[5], b[5], t),
  };
}

/** Trong nhà (Triệu Linh Điện): ánh nến ấm cố định, không theo giờ. */
export const INDOOR: Light = { tint: [1.06, 0.97, 0.88], sat: 1.05, bright: 1, night: 0.85, day: 0 };
