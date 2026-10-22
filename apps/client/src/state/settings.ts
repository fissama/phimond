import { signal } from '@preact/signals';
import type { TimeMode } from '../render/daylight.ts';

export type Quality = 'low' | 'medium' | 'high';
export type FpsCap = 30 | 60;

export interface Settings {
  quality: Quality;
  fps: FpsCap;
  dpad: boolean;
  /** Mật độ HUD: 'full' có mục tiêu, bản đồ nhỏ, chat; 'compact' chỉ giữ điều khiển và trạng thái. */
  hud: 'full' | 'compact';
  /** Thời gian trong game: theo giờ máy hoặc cố định ngày/hoàng hôn/đêm. */
  time: TimeMode;
  /** Âm lượng hiệu ứng 0–1 (0 = tắt). */
  sound: number;
}

/**
 * Thông số thực của từng mức (P01-R10): Low phải nhẹ hơn thật, không chỉ đổi nhãn.
 * Không mức nào ẩn quái/NPC/tín hiệu gameplay.
 */
export const PRESETS: Record<Quality, {
  label: string;
  /** Tỷ lệ độ phân giải render so với màn hình (nhân devicePixelRatio, có trần). */
  renderScale: number;
  maxPixelRatio: number;
  /** Bóng đổ thật từ đèn (shadow map) hay chỉ bóng tròn dưới chân. */
  shadows: 'none' | 'blob' | 'real';
  shadowMapSize: number;
  /** Tỷ lệ trang trí phụ (cỏ, hoa, lá rụng) được dựng. */
  decor: number;
  /** Hiệu ứng phụ: đom đóm, nước, đèn lửa. */
  fx: boolean;
  /** Nền xa và lớp sương. */
  backdrop: boolean;
  antialias: boolean;
  /** Hậu kỳ HD-2D: none = không; grade = tilt-shift + chỉnh màu theo giờ + tối góc; full = thêm bloom. */
  post: 'none' | 'grade' | 'full';
  textureBudgetMB: number;
}> = {
  low: { label: 'Thấp', renderScale: 0.75, maxPixelRatio: 1, shadows: 'none', shadowMapSize: 0, decor: 0.35, fx: false, backdrop: true, antialias: false, post: 'none', textureBudgetMB: 96 },
  medium: { label: 'Trung bình', renderScale: 1, maxPixelRatio: 1.5, shadows: 'blob', shadowMapSize: 0, decor: 0.8, fx: true, backdrop: true, antialias: false, post: 'grade', textureBudgetMB: 160 },
  high: { label: 'Cao', renderScale: 1, maxPixelRatio: 2, shadows: 'real', shadowMapSize: 2048, decor: 1, fx: true, backdrop: true, antialias: true, post: 'full', textureBudgetMB: 256 },
};

const KEY = 'phimond.settings.v1';
const DEFAULTS: Settings = { quality: 'medium', fps: 60, dpad: true, hud: 'full', time: 'auto', sound: 0.6 };

function load(): Settings {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return { ...DEFAULTS };
    const v = JSON.parse(raw) as Partial<Settings>;
    return {
      quality: v.quality === 'low' || v.quality === 'high' || v.quality === 'medium' ? v.quality : DEFAULTS.quality,
      fps: v.fps === 30 ? 30 : 60,
      dpad: v.dpad !== false,
      hud: v.hud === 'compact' ? 'compact' : 'full',
      time: v.time === 'day' || v.time === 'dusk' || v.time === 'night' ? v.time : 'auto',
      sound: typeof v.sound === 'number' && v.sound >= 0 && v.sound <= 1 ? v.sound : DEFAULTS.sound,
    };
  } catch {
    return { ...DEFAULTS };
  }
}

export const settings = signal<Settings>(load());
/** true nếu lưu cài đặt thất bại (chế độ riêng tư, storage bị chặn): lựa chọn chỉ giữ trong phiên. */
export const settingsVolatile = signal(false);

export function updateSettings(patch: Partial<Settings>): void {
  settings.value = { ...settings.value, ...patch };
  try {
    localStorage.setItem(KEY, JSON.stringify(settings.value));
    settingsVolatile.value = false;
  } catch {
    settingsVolatile.value = true;
  }
}
