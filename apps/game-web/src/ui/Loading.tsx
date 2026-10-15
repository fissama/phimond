import { useEffect, useState } from 'preact/hooks';

/** Mẹo chơi: lấy từ ui_loading của JAR (tiếng Việt), chỉnh thuật ngữ về cách gọi của Phimond và chỉ giữ mẹo còn đúng với bản hiện tại. */
export const TIPS = [
  'Bạn không nên nói cho người lạ biết mật khẩu tài khoản của mình, tránh bị đánh cắp tài khoản.',
  'Trong chiến đấu, dùng thẻ bắt để bắt linh thú. Khi đối phương càng ít máu thì xác suất bắt được càng cao.',
  'Bạn có thể gửi linh thú còn thừa ở Nông trại, khi cần có thể đến lấy lại.',
  'Tìm Quản trang trong nhà nhỏ của Nông trại để hợp thành hoặc cường hóa linh thú.',
  'Cấp sao của linh thú có từ 1 đến 5 sao, mạnh nhất là Thần Thú 5 sao.',
  'Linh thú chia làm 8 họ: Chim, Sâu, Thực vật, Dã thú, Linh thể, Bất tử, Ác ma, Rồng.',
  'Thuộc tính và kháng tính tấn công phép chia làm 6 loại: Địa, Thủy, Phong, Hỏa, Quang, Âm.',
  'Bạn có thể đi bất cứ nơi nào thông qua Thủy tinh dịch chuyển ở phía Đông Quảng Trường.',
  'Chỉ có thể mang theo linh thú không cao hơn 5 cấp so với cấp độ của nhân vật để tham chiến.',
  'Linh thú được hợp thành hoặc cường hóa có thể thừa hưởng nhiều thuộc tính; cường hóa là cách chính để nâng cao thuộc tính.',
  'Trong phần Cài đặt của menu chính, bạn có thể chỉnh chất lượng đồ họa để game chạy trôi chảy hơn.',
  'Sức mạnh ảnh hưởng tấn công vật lý. Nhanh nhẹn ảnh hưởng tốc độ, trúng đích và né tránh.',
];

export function Wordmark({ small }: { small?: boolean }) {
  return <div class={`wm ${small ? 'sm' : ''}`} aria-label="Phimond"><span class="wm-t">Phimond</span><span class="wm-s">Thế Giới Linh Thú</span></div>;
}

/** Màn loading theo JAR/video gốc: nền đen, logo, dải trang trí + thanh tiến trình (sprite APK), "loading…" và một mẹo chơi. */
export function LoadingScreen({ done, label }: { done?: boolean; label?: string }) {
  const [tip] = useState(() => TIPS[Math.floor(Math.random() * TIPS.length)]!);
  const [p, setP] = useState(0.06);
  useEffect(() => { const i = setInterval(() => setP((v) => Math.min(0.92, v + (0.92 - v) * 0.09)), 80); return () => clearInterval(i); }, []);
  const v = done ? 1 : p;
  return (
    <div class="ld" role="status" aria-live="polite" aria-label="Đang tải">
      <div class="ld-in">
        <Wordmark />
        <div class="ld-bar" aria-hidden="true"><div class="ld-fill" style={`--v:${(v * 100).toFixed(1)}%`} /></div>
        <div class="ld-txt">{label ?? 'loading…'}</div>
        <p class="ld-tip">{tip}</p>
      </div>
      <div class="ld-foot">Phimond · dự án khôi phục phi thương mại</div>
    </div>
  );
}
