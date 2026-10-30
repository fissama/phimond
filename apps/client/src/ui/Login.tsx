import { useEffect, useState } from 'preact/hooks';
import { session } from '../state/app.ts';
import { LoginBackdrop } from './LoginBackdrop.tsx';
import { uiUrl } from './skin.ts';

/** Biểu tượng pixel 1 màu (currentColor): mỗi dòng là một hàng, `#` = ô đặc, `x` = ô gạch chéo (vẽ đè, màu sáng). */
const ICONS = {
  user: ['...####...', '..######..', '..######..', '...####...', '..........', '.########.', '##########', '##########'],
  lock: ['..######..', '.##....##.', '.##....##.', '##########', '##########', '####..####', '####..####', '####..####', '##########'],
  mail: ['############', '##........##', '###......###', '#.##....##.#', '#..##..##..#', '#...####...#', '#..........#', '############'],
  eye: ['....######....', '..##......##..', '.#...####...#.', '#...######...#', '#...######...#', '.#...####...#.', '..##......##..', '....######....'],
  eyeOff: ['..........xx..', '....#####xx...', '..##....xx##..', '.#...##xx...#.', '#...##xx##...#', '#...#xx###...#', '.#..xx###...#.', '..#xx.....##..', '..xx######....', '.xx...........'],
} as const;
function Pix({ name, size = 16 }: { name: keyof typeof ICONS; size?: number }) {
  const rows = ICONS[name];
  const w = rows[0]!.length;
  return (
    <svg class="pix" width={size} height={(size * rows.length) / w} viewBox={`0 0 ${w} ${rows.length}`} shape-rendering="crispEdges" aria-hidden="true">
      {rows.flatMap((r, y) => [...r].map((c, x) => (c === '#' ? <rect key={`${x}-${y}`} x={x} y={y} width="1" height="1" fill="currentColor" /> : c === 'x' ? <rect key={`${x}-${y}`} x={x} y={y} width="1" height="1" fill="#fff4d0" /> : null)))}
    </svg>
  );
}

type Mode = 'login' | 'register' | 'forgot' | 'reset';

/** Mã đặt lại mật khẩu nằm ở phần # của liên kết trong thư (không gửi lên máy chủ khi tải trang, không vào log truy cập). */
function resetTokenFromHash(): string {
  const m = /[#&]reset=([0-9a-f]{64})/.exec(location.hash);
  return m?.[1] ?? '';
}

export function Login() {
  const [mode, setMode] = useState<Mode>(() => (resetTokenFromHash() ? 'reset' : 'login'));
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [email, setEmail] = useState('');
  const [terms, setTerms] = useState(false);
  const [remember, setRemember] = useState(true);
  const [show, setShow] = useState(false);
  const [caps, setCaps] = useState(false);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [info, setInfo] = useState('');

  useEffect(() => {
    setErr('');
  }, [mode]);

  const run = async (fn: () => Promise<void>) => {
    setBusy(true);
    setErr('');
    setInfo('');
    try {
      await fn();
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  const submit = () => {
    if (mode === 'login') return run(() => session.signIn(user.trim(), pass, false, { remember }));
    if (mode === 'register') return run(() => session.signIn(user.trim(), pass, true, { email: email.trim(), terms, remember }));
    if (mode === 'forgot')
      return run(async () => {
        await session.requestPasswordReset(email.trim());
        setInfo('Nếu email này đã gắn với một tài khoản, thư đặt lại mật khẩu sẽ đến trong ít phút (kiểm tra cả mục Spam). Liên kết có hiệu lực 30 phút.');
      });
    return run(async () => {
      await session.resetPassword(resetTokenFromHash(), pass);
      history.replaceState(null, '', location.pathname + location.search);
      setPass('');
      setMode('login');
      setInfo('Đã đổi mật khẩu. Hãy đăng nhập bằng mật khẩu mới.');
    });
  };

  const needUser = mode === 'login' || mode === 'register';
  const needPass = mode !== 'forgot';
  const canSubmit = !busy && (!needUser || !!user) && (!needPass || !!pass) && (mode !== 'register' || terms) && (mode !== 'forgot' || !!email.trim());
  const title = { login: '', register: 'Tạo tài khoản', forgot: 'Quên mật khẩu', reset: 'Đặt mật khẩu mới' }[mode];

  return (
    <>
    <LoginBackdrop />
    <form
      class="login-box"
      style={box}
      onSubmit={(e) => {
        e.preventDefault();
        if (canSubmit) void submit();
      }}
    >
      <img src={uiUrl('logo-horizontal')} alt="PHIMOND" style={{ width: '100%', maxWidth: 300, alignSelf: 'center', imageRendering: 'pixelated', margin: '-4px 0 6px' }} />
      {title && <h2 style={{ margin: 0, fontSize: 18, textAlign: 'center' }}>{title}</h2>}
      {needUser && (
        <div class="fld">
          <Pix name="user" />
          <input data-testid="username" class="input" placeholder="Tài khoản" autoComplete="username" autoCapitalize="none" value={user} onInput={(e) => setUser(e.currentTarget.value)} />
        </div>
      )}
      {needPass && (
        <div class="fld">
          <Pix name="lock" />
          <input
            data-testid="password"
            class="input"
            placeholder={mode === 'reset' ? 'Mật khẩu mới' : 'Mật khẩu'}
            type={show ? 'text' : 'password'}
            autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            value={pass}
            onInput={(e) => setPass(e.currentTarget.value)}
            onKeyUp={(e) => setCaps(e.getModifierState('CapsLock'))}
            onKeyDown={(e) => setCaps(e.getModifierState('CapsLock'))}
            onBlur={() => setCaps(false)}
          />
          <button type="button" data-testid="toggle-password" class="eye" aria-label={show ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'} title={show ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'} aria-pressed={show} onClick={() => setShow(!show)}>
            <Pix name={show ? 'eye' : 'eyeOff'} size={20} />
          </button>
        </div>
      )}
      {caps && needPass && <p data-testid="caps-hint" style={hint}>Caps Lock đang bật.</p>}
      {(mode === 'register' || mode === 'reset') && <p style={hint}>Mật khẩu từ 8 ký tự, không dùng mật khẩu quá phổ biến (như 12345678) hoặc trùng tên tài khoản.</p>}
      {(mode === 'register' || mode === 'forgot') && (
        <div class="fld">
          <Pix name="mail" />
          <input data-testid="email" class="input" type="email" placeholder={mode === 'register' ? 'Email (tuỳ chọn, để lấy lại mật khẩu)' : 'Email đã gắn với tài khoản'} autoComplete="email" value={email} onInput={(e) => setEmail(e.currentTarget.value)} />
        </div>
      )}
      {mode === 'register' && (
        <label style={check}>
          <input data-testid="terms" type="checkbox" checked={terms} onChange={(e) => setTerms(e.currentTarget.checked)} />
          <span>
            Tôi đã đọc và đồng ý <a href="/terms.html" target="_blank" rel="noopener">Điều khoản sử dụng</a> và <a href="/privacy.html" target="_blank" rel="noopener">Chính sách quyền riêng tư</a>.
          </span>
        </label>
      )}
      {(mode === 'login' || mode === 'register') && (
        <label style={check}>
          <input data-testid="remember" type="checkbox" checked={remember} onChange={(e) => setRemember(e.currentTarget.checked)} />
          <span>Ghi nhớ đăng nhập trên thiết bị này</span>
        </label>
      )}

      {mode === 'login' && (
        <div style={{ display: 'flex', gap: 8 }}>
          <button data-testid="login" class="btn primary" style={{ flex: 1 }} disabled={!canSubmit} type="submit">Đăng nhập</button>
          <button data-testid="register" class="btn" style={{ flex: 1 }} disabled={busy} type="button" onClick={() => setMode('register')}>Đăng ký</button>
        </div>
      )}
      {mode !== 'login' && (
        <div style={{ display: 'flex', gap: 8 }}>
          <button data-testid={mode === 'register' ? 'register-submit' : 'submit'} class="btn primary" style={{ flex: 1 }} disabled={!canSubmit} type="submit">
            {mode === 'register' ? 'Tạo tài khoản' : mode === 'forgot' ? 'Gửi thư đặt lại' : 'Đổi mật khẩu'}
          </button>
          <button data-testid="back-to-login" class="btn" style={{ flex: 1 }} disabled={busy} type="button" onClick={() => setMode('login')}>Quay lại</button>
        </div>
      )}
      {mode === 'login' && (
        <button data-testid="forgot-link" type="button" class="linkbtn" style={linkBtn} onClick={() => setMode('forgot')}>Quên mật khẩu?</button>
      )}
      {err && <p data-testid="login-error" style={{ color: '#ff8a80', margin: 0 }}>{err}</p>}
      {info && <p data-testid="login-info" style={{ color: '#a8e6a1', margin: 0 }}>{info}</p>}
      <p style={{ ...hint, textAlign: 'center' }}>
        <a href="/terms.html" target="_blank" rel="noopener">Điều khoản</a> · <a href="/privacy.html" target="_blank" rel="noopener">Quyền riêng tư</a>
      </p>
    </form>
    </>
  );
}

const box = { position: 'absolute', zIndex: 5, inset: 0, margin: 'auto', width: 'min(400px, calc(100% - 32px))', height: 'fit-content', maxHeight: 'calc(100% - 16px)', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 10 } as const;
const hint = { margin: 0, fontSize: 12, color: '#cdbd90' } as const;
const check = { display: 'flex', gap: 8, alignItems: 'flex-start', fontSize: 13, color: '#e8dcc0', lineHeight: 1.35 } as const;
const linkBtn = { background: 'none', border: 0, color: '#9fc7ff', textDecoration: 'underline', cursor: 'pointer', fontSize: 13, padding: 0, alignSelf: 'center' } as const;
