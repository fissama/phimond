import { hd2dUrl } from '../render/assets.ts';

const bg = (id: string) => ({ backgroundImage: `url(${hd2dUrl(id)})` });
/** Hạt sáng bay lên: vị trí/độ trễ cố định theo chỉ số để không nhảy khi render lại. */
const MOTES = Array.from({ length: 14 }, (_, i) => ({ left: (i * 37 + 11) % 100, delay: -((i * 53) % 19), dur: 12 + ((i * 7) % 9), size: 2 + (i % 3) }));

/** Linh thú 5 sao có ảnh trưng bày. `idle` = ảnh thứ hai của cùng thú để xen kẽ làm nhịp thở. */
const POOL: { id: string; idle?: string }[] = [
  { id: 'showcase-unicorn' },
  { id: 'showcase-scorpion' },
  { id: 'showcase-flower' },
  { id: 'stage-species_0052', idle: 'stage-species_0052-idle' },
  { id: 'stage-species_0107', idle: 'stage-species_0107-idle' },
  { id: 'stage-species_0088', idle: 'stage-species_0088-idle' },
  { id: 'stage-species_0150', idle: 'stage-species_0150-idle' },
  { id: 'stage-species_0153', idle: 'stage-species_0153-idle' },
  { id: 'stage-species_0155', idle: 'stage-species_0155-idle' },
];

/** Sáu chỗ đứng: 4 hàng trước (to, trên bệ lớn) + 2 hàng sau (nhỏ, trên bệ nhỏ). `x` = tâm (% chiều rộng), `w` = cỡ tương đối. Giữa trống cho hộp đăng nhập. */
const SLOTS = [
  { x: 8.5, w: 0.82, back: false },
  { x: 23, w: 0.82, back: false },
  { x: 77, w: 0.82, back: false },
  { x: 91.5, w: 0.82, back: false },
  { x: 16, w: 0.5, back: true },
  { x: 84, w: 0.5, back: true },
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
      <div class="lb-sky" />
      <div class="lb-far" style={bg('hall-city-backdrop')} />
      <div class="lb-glow" />
      <div class="lb-haze" />
      <img class="lb-bird b1" src={hd2dUrl('ambient-birds')} alt="" />
      <img class="lb-bird b2" src={hd2dUrl('ambient-birds')} alt="" />
      <div class="lb-terrace" style={bg('stage-floor')} />
      <img class="lb-prop left" src={hd2dUrl('stage-prop-brazier')} alt="" />
      <img class="lb-prop right" src={hd2dUrl('stage-prop-brazier')} alt="" />
      {MOTES.map((m, i) => (
        <i key={i} class="lb-mote" style={{ left: `${m.left}%`, width: m.size, height: m.size, animationDelay: `${m.delay}s`, animationDuration: `${m.dur}s` }} />
      ))}
      {[...beasts].sort((a, b) => Number(b.back) - Number(a.back)).map((b, i) => (
        <div key={i} class={`lb-beast s${b.slot}${b.back ? ' back' : ''}`} style={{ '--x': `${b.x}%`, '--w': b.w, '--d': `${b.delay}s` }}>
          <img class="dais" src={hd2dUrl(b.back ? 'stage-dais-small' : 'stage-dais-large')} alt="" />
          <img class="pet a" src={hd2dUrl(b.id)} alt="" />
          {b.idle && <img class="pet b" src={hd2dUrl(b.idle)} alt="" />}
        </div>
      ))}
      <div class="lb-light" style={bg('stage-light')} />
      <div class="lb-vignette" />
    </div>
  );
}
