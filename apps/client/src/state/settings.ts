import { signal } from '@preact/signals';

export type Quality = 'low' | 'medium' | 'high';
export type FpsCap = 30 | 60;

export interface Settings {
  quality: Quality;
  fps: FpsCap;
  dpad: boolean;
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
  textureBudgetMB: number;
}> = {
  low: { label: 'Thấp', renderScale: 0.75, maxPixelRatio: 1, shadows: 'none', shadowMapSize: 0, decor: 0.35, fx: false, backdrop: true, antialias: false, textureBudgetMB: 96 },
  medium: { label: 'Trung bình', renderScale: 1, maxPixelRatio: 1.5, shadows: 'blob', shadowMapSize: 0, decor: 0.8, fx: true, backdrop: true, antialias: false, textureBudgetMB: 160 },
  high: { label: 'Cao', renderScale: 1, maxPixelRatio: 2, shadows: 'real', shadowMapSize: 2048, decor: 1, fx: true, backdrop: true, antialias: true, textureBudgetMB: 256 },
};

const KEY = 'phimond.settings.v1';
const DEFAULTS: Settings = { quality: 'medium', fps: 60, dpad: true };

function load(): Settings {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return { ...DEFAULTS };
    const v = JSON.parse(raw) as Partial<Settings>;
    return {
      quality: v.quality === 'low' || v.quality === 'high' || v.quality === 'medium' ? v.quality : DEFAULTS.quality,
      fps: v.fps === 30 ? 30 : 60,
      dpad: v.dpad !== false,
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
