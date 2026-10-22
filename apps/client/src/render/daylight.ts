export type TimeMode = 'auto' | 'day' | 'dusk' | 'night';

/**
 * Ánh sáng theo giờ (hậu kỳ phối màu kiểu Octopath): màu nhân (tint), độ bão hòa, độ sáng, tương phản,
 * và tách tông — `shade` cộng vào vùng tối (xanh tím về đêm), `hi` cộng vào vùng sáng (cam vàng lúc hoàng hôn).
 * `night`/`day` (0..1) điều khiển đèn lồng, tia nắng...
 */
export type Vec3 = [number, number, number];
export interface Light {
  tint: Vec3;
  sat: number;
  bright: number;
  contrast: number;
  shade: Vec3;
  hi: Vec3;
  night: number;
  day: number;
}

// [giờ, Light] — nội suy tuyến tính, vòng 24 giờ.
const L = (tint: Vec3, sat: number, bright: number, contrast: number, shade: Vec3, hi: Vec3, night: number, day: number): Light => ({ tint, sat, bright, contrast, shade, hi, night, day });
const NIGHT = L([0.42, 0.56, 1.0], 0.95, 0.76, 1.12, [0.01, 0.03, 0.12], [0.05, 0.1, 0.2], 1, 0);
const KEYS: [number, Light][] = [
  [0, NIGHT],
  [5, NIGHT],
  [6.5, L([1.1, 0.9, 0.92], 1.16, 0.97, 1.07, [0.07, 0.03, 0.12], [0.2, 0.12, 0.03], 0.35, 0.3)], // bình minh hồng tím
  [8, L([1.02, 1.0, 0.97], 1.12, 1, 1.05, [0.0, 0.02, 0.06], [0.06, 0.04, 0.0], 0, 1)],
  [16.5, L([1.04, 0.99, 0.94], 1.12, 1, 1.05, [0.0, 0.02, 0.06], [0.08, 0.05, 0.0], 0, 1)],
  [18, L([1.14, 0.88, 0.7], 1.14, 0.96, 1.08, [0.07, 0.03, 0.1], [0.24, 0.12, 0.0], 0.3, 0.35)], // giờ vàng cam
  [19.5, L([0.74, 0.68, 1.0], 1.0, 0.8, 1.1, [0.05, 0.02, 0.14], [0.14, 0.07, 0.08], 0.9, 0)], // chạng vạng tím
  [24, NIGHT],
];
const FIXED: Record<Exclude<TimeMode, 'auto'>, number> = { day: 12, dusk: 17.9, night: 22 };


const mix = (a: number, b: number, t: number) => a + (b - a) * t;
const mixV = (a: Vec3, b: Vec3, t: number): Vec3 => [mix(a[0], b[0], t), mix(a[1], b[1], t), mix(a[2], b[2], t)];

export function lightAt(mode: TimeMode, now: Date = new Date()): Light {
  const h = mode === 'auto' ? now.getHours() + now.getMinutes() / 60 : FIXED[mode];
  let i = 0;
  while (i < KEYS.length - 2 && h >= KEYS[i + 1]![0]) i++;
  const [h0, a] = KEYS[i]!;
  const [h1, b] = KEYS[i + 1]!;
  const t = Math.min(1, Math.max(0, (h - h0) / (h1 - h0)));
  return {
    tint: mixV(a.tint, b.tint, t),
    sat: mix(a.sat, b.sat, t),
    bright: mix(a.bright, b.bright, t),
    contrast: mix(a.contrast, b.contrast, t),
    shade: mixV(a.shade, b.shade, t),
    hi: mixV(a.hi, b.hi, t),
    night: mix(a.night, b.night, t),
    day: mix(a.day, b.day, t),
  };
}

/** Trong nhà (Triệu Linh Điện): ánh nến ấm cố định, không theo giờ. */
export const INDOOR: Light = L([1.08, 0.96, 0.84], 1.1, 1, 1.14, [0.06, 0.02, 0.0], [0.26, 0.12, 0.0], 0.85, 0);
