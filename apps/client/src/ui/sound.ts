import { settings } from '../state/settings.ts';

/**
 * Hiệu ứng âm thanh tổng hợp bằng WebAudio (chưa có file âm thanh vẽ riêng): đòn đánh, phép, trượt, thắng/thua,
 * nhặt tiền, bấm nút, mở bảng. AudioContext chỉ tạo sau thao tác đầu tiên của người chơi (chính sách autoplay).
 * Âm lượng theo Cài đặt (0 = tắt). Nợ: thay bằng bộ âm thanh thật + nhạc nền theo map.
 */
export type Sfx = 'hit' | 'magic' | 'miss' | 'win' | 'lose' | 'flee' | 'coin' | 'click' | 'open' | 'level';

let ctx: AudioContext | null = null;
let unlocked = false;

function audio(): AudioContext | null {
  if (!unlocked) return null;
  if (!ctx) {
    try {
      const AC = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
      ctx = AC ? new AC() : null;
    } catch {
      ctx = null;
    }
  }
  if (ctx?.state === 'suspended') void ctx.resume();
  return ctx;
}

if (typeof window !== 'undefined') {
  const unlock = () => {
    unlocked = true;
    audio();
  };
  window.addEventListener('pointerdown', unlock, { once: true, capture: true });
  window.addEventListener('keydown', unlock, { once: true, capture: true });
  // Tiếng bấm nhẹ cho mọi nút giao diện (không gồm canvas cảnh).
  window.addEventListener(
    'click',
    (e) => {
      const t = e.target as HTMLElement | null;
      if (t?.closest?.('button:not(:disabled)')) sfx('click');
    },
    { capture: true },
  );
}

function tone(a: AudioContext, out: GainNode, type: OscillatorType, f0: number, f1: number, t0: number, dur: number, vol: number) {
  const o = a.createOscillator();
  const g = a.createGain();
  o.type = type;
  o.frequency.setValueAtTime(f0, t0);
  o.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t0 + dur);
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(vol, t0 + 0.012);
  g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
  o.connect(g).connect(out);
  o.start(t0);
  o.stop(t0 + dur + 0.02);
}

function noise(a: AudioContext, out: GainNode, t0: number, dur: number, vol: number, hp = 800) {
  const len = Math.floor(a.sampleRate * dur);
  const buf = a.createBuffer(1, len, a.sampleRate);
  const d = buf.getChannelData(0);
  for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * (1 - i / len);
  const src = a.createBufferSource();
  src.buffer = buf;
  const f = a.createBiquadFilter();
  f.type = 'highpass';
  f.frequency.value = hp;
  const g = a.createGain();
  g.gain.value = vol;
  src.connect(f).connect(g).connect(out);
  src.start(t0);
}

export function sfx(kind: Sfx): void {
  const vol = settings.value.sound;
  if (vol <= 0) return;
  const a = audio();
  if (!a) return;
  const out = a.createGain();
  out.gain.value = vol * 0.5;
  out.connect(a.destination);
  const t = a.currentTime + 0.005;
  switch (kind) {
    case 'hit':
      noise(a, out, t, 0.12, 0.9, 1200);
      tone(a, out, 'square', 180, 60, t, 0.12, 0.35);
      break;
    case 'magic':
      tone(a, out, 'sine', 520, 1400, t, 0.25, 0.35);
      tone(a, out, 'triangle', 780, 2100, t + 0.04, 0.22, 0.2);
      break;
    case 'miss':
      noise(a, out, t, 0.16, 0.35, 3000);
      break;
    case 'win':
      [523, 659, 784, 1047].forEach((f, i) => tone(a, out, 'triangle', f, f, t + i * 0.09, 0.22, 0.35));
      break;
    case 'level':
      [659, 784, 988, 1319].forEach((f, i) => tone(a, out, 'square', f, f, t + i * 0.07, 0.18, 0.18));
      break;
    case 'lose':
      [392, 330, 262].forEach((f, i) => tone(a, out, 'triangle', f, f * 0.97, t + i * 0.16, 0.3, 0.3));
      break;
    case 'flee':
      tone(a, out, 'sine', 700, 250, t, 0.25, 0.25);
      break;
    case 'coin':
      tone(a, out, 'square', 988, 988, t, 0.06, 0.18);
      tone(a, out, 'square', 1319, 1319, t + 0.06, 0.16, 0.18);
      break;
    case 'click':
      tone(a, out, 'triangle', 900, 600, t, 0.05, 0.18);
      break;
    case 'open':
      tone(a, out, 'sine', 400, 800, t, 0.12, 0.2);
      break;
  }
}
