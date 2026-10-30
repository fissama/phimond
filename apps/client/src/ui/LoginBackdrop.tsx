import { hd2dUrl } from '../render/assets.ts';

const bg = (id: string) => ({ backgroundImage: `url(${hd2dUrl(id)})` });
/** Hạt sáng bay lên: vị trí/độ trễ cố định theo chỉ số để không nhảy khi render lại. */
const MOTES = Array.from({ length: 14 }, (_, i) => ({ left: (i * 37 + 11) % 100, delay: -((i * 53) % 19), dur: 12 + ((i * 7) % 9), size: 2 + (i % 3) }));

const EMBERS = Array.from({ length: 12 }, (_, i) => ({ side: i % 2 ? 'right' : 'left', dx: ((i * 13) % 17) - 8, delay: -((i * 0.83) % 5), dur: 3.2 + ((i * 7) % 5) * 0.5 }));

/**
 * Linh thú 5 sao: mỗi con một dải idle 4 khung (`idle-*.png`). `c` = cạnh một khung, `h` = cao thật của thân ở khung 1, `b` = hàng pixel đáy thân
 * (để chân chạm bệ và mọi con cao bằng nhau dù khung ảnh khác nhau).
 */
const POOL: { id: string; c: number; h: number; b: number }[] = [
  { id: 'idle-unicorn', c: 192, h: 152, b: 184 },
  { id: 'idle-scorpion', c: 192, h: 158, b: 184 },
  { id: 'idle-flower', c: 192, h: 165, b: 184 },
  { id: 'idle-species_0052', c: 256, h: 232, b: 248 },
  { id: 'idle-species_0107', c: 256, h: 228, b: 248 },
  { id: 'idle-species_0088', c: 256, h: 215, b: 248 },
  { id: 'idle-species_0150', c: 256, h: 210, b: 248 },
  { id: 'idle-species_0153', c: 256, h: 232, b: 248 },
  { id: 'idle-species_0155', c: 256, h: 183, b: 248 },
];

/** Sáu chỗ đứng: 4 hàng trước (to, trên bệ lớn) + 2 hàng sau (nhỏ, trên bệ nhỏ). `x` = tâm (% chiều rộng), `w` = cỡ tương đối. Giữa trống cho hộp đăng nhập. */
const SLOTS = [
  { x: 8.5, w: 0.82, back: false },
  { x: 23, w: 0.82, back: false },
  { x: 77, w: 0.82, back: false },
  { x: 91.5, w: 0.82, back: false },
  { x: 16, w: 0.72, back: true },
  { x: 84, w: 0.72, back: true },
];

/** Mỗi lần mở màn hình, chọn ngẫu nhiên 6 thú trong bể (xáo trộn Fisher–Yates). */
function roster() {
  const p = POOL.slice();
  for (let i = p.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const t = p[i]!;
    p[i] = p[j]!;
    p[j] = t;
  }
  return SLOTS.map((s, i) => ({ ...s, ...p[i]!, slot: i, delay: -((i * 1.37) % 5) }));
}

/**
 * Nền động cho màn đăng nhập, một cảnh thống nhất: trời hoàng hôn, kinh thành trôi chậm, sương ở chân trời,
 * thềm đá phía trước với bệ tròn, lư đồng và ánh nắng; sáu linh thú 5 sao (xoay vòng mỗi lần mở) đứng trên bệ,
 * chim bay, hạt sáng. Chỉ dùng ảnh có sẵn; tắt chuyển động khi hệ thống yêu cầu giảm chuyển động.
 */
export function LoginBackdrop() {
  const beasts = roster();
  return (
    <div class="lb" aria-hidden="true">
      <div class="lb-sky" style={bg('login-sky')} />
      <div class="lb-cloud c1" style={bg('login-clouds')} />
      <div class="lb-cloud c2" style={bg('login-clouds')} />
      <div class="lb-far" style={bg('login-city-far')} />
      <div class="lb-near" style={bg('login-city-near')} />
      <div class="lb-glow" />
      <div class="lb-haze" />
      <img class="lb-bird b1" src={hd2dUrl('ambient-birds')} alt="" />
      <img class="lb-bird b2" src={hd2dUrl('ambient-birds')} alt="" />
      <div class="lb-rail" style={bg('stage-balustrade')} />
      <div class="lb-terrace" style={bg('stage-floor')} />
      <img class="lb-banner left" src={hd2dUrl('stage-prop-banner')} alt="" />
      <img class="lb-banner right" src={hd2dUrl('stage-prop-banner')} alt="" />
      <img class="lb-prop left" src={hd2dUrl('stage-prop-brazier')} alt="" />
      <img class="lb-prop right" src={hd2dUrl('stage-prop-brazier')} alt="" />
      <div class="lb-bloom left" />
      <div class="lb-bloom right" />
      {EMBERS.map((e, i) => (
        <i key={i} class={`lb-ember ${e.side}`} style={{ '--ox': `${e.dx}px`, animationDelay: `${e.delay}s`, animationDuration: `${e.dur}s` }} />
      ))}
      {MOTES.map((m, i) => (
        <i key={i} class="lb-mote" style={{ left: `${m.left}%`, width: m.size, height: m.size, animationDelay: `${m.delay}s`, animationDuration: `${m.dur}s` }} />
      ))}
      {[...beasts].sort((a, b) => Number(b.back) - Number(a.back)).map((b, i) => (
        <div key={i} class={`lb-beast s${b.slot}${b.back ? ' back' : ''}`} style={{ '--x': `${b.x}%`, '--w': b.w, '--d': `${b.delay}s`, '--k': b.c / b.h, '--pad': (b.c - b.b) / b.h }}>
          <img class="dais" src={hd2dUrl(b.back ? 'stage-dais-small' : 'stage-dais-large')} alt="" />
          <div class="pet" style={bg(b.id)} />
        </div>
      ))}
      <div class="lb-light" style={bg('stage-light')} />
      <img class="lb-fg vines" src={hd2dUrl('fg-deep-vines')} alt="" />
      <img class="lb-fg vines r" src={hd2dUrl('fg-deep-vines')} alt="" />
      <div class="lb-fg bunting" style={bg('fg-city-bunting')} />
      <div class="lb-tilt top" />
      <div class="lb-tilt bottom" />
      <div class="lb-vignette" />
    </div>
  );
}
