import { hd2dUrl } from '../render/assets.ts';

const bg = (id: string) => ({ backgroundImage: `url(${hd2dUrl(id)})` });
/** Hạt sáng bay lên: vị trí/độ trễ cố định theo chỉ số để không nhảy khi render lại. */
const MOTES = Array.from({ length: 16 }, (_, i) => ({ left: (i * 37 + 11) % 100, delay: -((i * 53) % 19), dur: 12 + ((i * 7) % 9), size: 2 + (i % 3) }));

/**
 * Nền động cho màn đăng nhập, một cảnh thống nhất: trời hoàng hôn, kinh thành trôi chậm, sương ở chân trời,
 * thềm đá phía trước nơi ba linh thú đứng chung một mặt phẳng (có bóng), chim bay, mây trôi và hạt sáng.
 * Chỉ dùng ảnh có sẵn; tắt chuyển động khi hệ thống yêu cầu giảm chuyển động.
 */
export function LoginBackdrop() {
  return (
    <div class="lb" aria-hidden="true">
      <div class="lb-sky" />
      <div class="lb-far" style={bg('hall-city-backdrop')} />
      <div class="lb-glow" />
      <div class="lb-haze" />
      <img class="lb-bird b1" src={hd2dUrl('ambient-birds')} alt="" />
      <img class="lb-bird b2" src={hd2dUrl('ambient-birds')} alt="" />
      {MOTES.map((m, i) => (
        <i key={i} class="lb-mote" style={{ left: `${m.left}%`, width: m.size, height: m.size, animationDelay: `${m.delay}s`, animationDuration: `${m.dur}s` }} />
      ))}
      <div class="lb-terrace" />
      <div class="lb-shadow left" />
      <div class="lb-shadow right" />
      <div class="lb-shadow far" />
      <img class="lb-pet left" src={hd2dUrl('showcase-unicorn')} alt="" />
      <img class="lb-pet right" src={hd2dUrl('showcase-scorpion')} alt="" />
      <img class="lb-pet far" src={hd2dUrl('showcase-flower')} alt="" />
      <div class="lb-vignette" />
    </div>
  );
}
