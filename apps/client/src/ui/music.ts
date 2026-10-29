import { effect } from '@preact/signals';
import { settings } from '../state/settings.ts';
import { session } from '../state/app.ts';

/**
 * Nhạc nền theo ngữ cảnh (map / trận) bằng thẻ <audio> lặp, chuyển bài mờ dần. File nhạc nằm ở
 * `public/audio/music/` và khai báo trong `manifest.json` (xem AUDIO-MUSIC.md). Thiếu file thì im lặng — không lỗi, không
 * chặn gameplay. Chỉ bắt đầu sau thao tác đầu tiên của người chơi (chính sách autoplay). Âm lượng theo Cài đặt → Nhạc nền.
 */
interface Manifest {
  /** khóa bài → danh sách file thử lần lượt (ogg trước, mp3 sau) */
  tracks: Record<string, string[]>;
  /** id map hoặc 'battle' → khóa bài (hoặc danh sách ưu tiên: bài đầu thiếu file thì dùng bài sau) */
  contexts: Record<string, string | string[]>;
  /** hiệu ứng ngắn phát một lần (victory) → file */
  jingles?: Record<string, string[]>;
  /** hệ số âm lượng riêng từng bài (0..1) để cân âm giữa các bài */
  gain?: Record<string, number>;
}

const BASE = `${import.meta.env.BASE_URL}audio/music/`;
const FADE_MS = 900;
let manifest: Manifest | null = null;
let manifestTried = false;
let unlocked = false;
let wantList: string[] = []; // khóa bài muốn phát theo thứ tự ưu tiên
let cur: { key: string; el: HTMLAudioElement } | null = null;
let duck = 1;
const dead = new Set<string>(); // bài không tải được → không thử lại

async function loadManifest(): Promise<Manifest | null> {
  if (manifest || manifestTried) return manifest;
  manifestTried = true;
  try {
    const r = await fetch(`${BASE}manifest.json`);
    if (!r.ok || !(r.headers.get('content-type') ?? '').includes('json')) return null;
    manifest = (await r.json()) as Manifest;
  } catch {
    manifest = null;
  }
  return manifest;
}

const vol = (key: string) => Math.min(1, Math.max(0, settings.value.music * 0.8 * (manifest?.gain?.[key] ?? 1) * duck));

function open(files: string[], loop: boolean): HTMLAudioElement | null {
  const el = new Audio();
  el.loop = loop;
  el.preload = 'auto';
  const ok = files.find((f) => el.canPlayType(f.endsWith('.ogg') ? 'audio/ogg; codecs="vorbis"' : f.endsWith('.mp3') ? 'audio/mpeg' : 'audio/wav') !== '');
  if (!ok) return null;
  el.src = `${BASE}${ok}`;
  el.volume = 0;
  return el;
}

function ramp(el: HTMLAudioElement, to: number, ms: number, done?: () => void): void {
  const from = el.volume;
  const t0 = performance.now();
  const step = () => {
    const k = Math.min(1, (performance.now() - t0) / ms);
    el.volume = Math.min(1, Math.max(0, from + (to - from) * k));
    if (k < 1) requestAnimationFrame(step);
    else done?.();
  };
  step();
}

async function apply(): Promise<void> {
  if (!unlocked) return;
  const m = await loadManifest();
  if (!m) return;
  const key = wantList.find((k) => !dead.has(k)) ?? null;
  if (cur && cur.key === key) {
    if (settings.value.music <= 0) cur.el.pause();
    else {
      if (cur.el.paused) void cur.el.play().catch(() => undefined);
      cur.el.volume = vol(cur.key);
    }
    return;
  }
  const old = cur;
  cur = null;
  if (old) ramp(old.el, 0, FADE_MS, () => old.el.pause());
  if (!key || dead.has(key) || settings.value.music <= 0) return;
  const files = m.tracks[key];
  const el = files ? open(files, true) : null;
  if (!el) {
    dead.add(key);
    return;
  }
  el.addEventListener('error', () => {
    dead.add(key);
    if (cur?.el === el) cur = null;
    void apply(); // thử bài kế tiếp trong danh sách ưu tiên
  });
  cur = { key, el };
  try {
    await el.play();
    if (cur?.el === el) ramp(el, vol(key), FADE_MS);
  } catch {
    /* autoplay bị chặn: thử lại ở lần thao tác sau */
  }
}

/** Đặt ngữ cảnh nhạc (id map hoặc 'battle'); null = tắt. */
export function setMusicContext(ctx: string | null): void {
  void loadManifest().then((m) => {
    const c = ctx && m ? m.contexts[ctx] : undefined;
    wantList = c ? (Array.isArray(c) ? c : [c]) : [];
    void apply();
  });
}

/** Phát một đoạn ngắn (victory) một lần, hạ nhạc nền trong lúc phát. */
export function playJingle(name: string): void {
  if (!unlocked || settings.value.music <= 0) return;
  void loadManifest().then((m) => {
    const files = m?.jingles?.[name];
    const el = files ? open(files, false) : null;
    if (!el) return;
    duck = 0.25;
    if (cur) cur.el.volume = vol(cur.key);
    const end = () => {
      duck = 1;
      if (cur) ramp(cur.el, vol(cur.key), 600);
    };
    el.addEventListener('ended', end);
    el.addEventListener('error', end);
    el.volume = Math.min(1, settings.value.music);
    void el.play().catch(end);
  });
}

if (typeof window !== 'undefined') {
  const unlock = () => {
    unlocked = true;
    void apply();
  };
  window.addEventListener('pointerdown', unlock, { once: true, capture: true });
  window.addEventListener('keydown', unlock, { once: true, capture: true });
  document.addEventListener('visibilitychange', () => {
    if (!cur) return;
    if (document.hidden) cur.el.pause();
    else if (settings.value.music > 0) void cur.el.play().catch(() => undefined);
  });
}

/** Gắn nhạc với trạng thái nhân vật: trận → 'battle', còn lại theo map. Trả hàm gỡ. */
export function bindMusic(): () => void {
  const stop = effect(() => {
    const ch = session.character.value;
    setMusicContext(ch ? (ch.battle ? 'battle' : ch.map_id) : null);
  });
  const stopVol = effect(() => {
    void settings.value.music;
    void apply();
  });
  return () => {
    stop();
    stopVol();
    setMusicContext(null);
  };
}
