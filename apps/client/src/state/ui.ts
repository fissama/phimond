import { signal } from '@preact/signals';

export type LogTab = 'all' | 'system' | 'world' | 'area' | 'party' | 'private';
export const LOG_TABS: { id: LogTab; label: string }[] = [
  { id: 'all', label: 'Tất cả' },
  { id: 'system', label: 'Hệ thống' },
  { id: 'world', label: 'Thế giới' },
  { id: 'area', label: 'Khu vực' },
  { id: 'party', label: 'Đội' },
  { id: 'private', label: 'Riêng' },
];

export interface LogLine {
  id: number;
  tab: Exclude<LogTab, 'all'>;
  text: string;
}

let nextId = 1;
export const log = signal<LogLine[]>([]);
export function pushLog(text: string, tab: LogLine['tab'] = 'system'): void {
  log.value = [...log.value.slice(-79), { id: nextId++, tab, text }];
}

export interface Toast {
  id: number;
  text: string;
}
export const toasts = signal<Toast[]>([]);
export function toast(text: string, ms = 2200): void {
  const id = nextId++;
  // Không lặp cùng thông báo đang hiện.
  if (toasts.value.some((t) => t.text === text)) return;
  toasts.value = [...toasts.value, { id, text }];
  setTimeout(() => (toasts.value = toasts.value.filter((t) => t.id !== id)), ms);
}

/** Lớp phủ đang mở trên world. Mọi lớp phủ đều dừng di chuyển (P01-R03). */
export type Overlay =
  | { kind: 'none' }
  | { kind: 'menu'; page: 'root' | 'pets' | 'bag' | 'quests' | 'settings' }
  | { kind: 'npc'; npcId: string; line: string }
  | { kind: 'pedestal'; index: number }
  | { kind: 'pillar' };

export const overlay = signal<Overlay>({ kind: 'none' });
export function closeOverlay(): void {
  overlay.value = { kind: 'none' };
}

/** Màn tải khi đổi map (null = ẩn). */
export const loading = signal<string | null>(null);

/** Bảng kết quả trận còn mở (world vẫn dừng di chuyển tới khi người chơi bấm Tiếp tục). */
export const battleResultOpen = signal(false);
