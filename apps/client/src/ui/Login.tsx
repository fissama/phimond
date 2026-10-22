import { useState } from 'preact/hooks';
import { session } from '../state/app.ts';
import { uiUrl } from './skin.ts';

export function Login() {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');

  const go = async (register: boolean) => {
    setBusy(true);
    setErr('');
    try {
      await session.login(user.trim(), pass, register);
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <form
      class="login-box"
      style={box}
      onSubmit={(e) => {
        e.preventDefault();
        void go(false);
      }}
    >
      <img src={uiUrl('logo-horizontal')} alt="PHIMOND" style={{ width: '100%', maxWidth: 300, alignSelf: 'center', imageRendering: 'pixelated', margin: '-4px 0 6px' }} />
      <input data-testid="username" class="input" placeholder="Tài khoản" autoComplete="username" value={user} onInput={(e) => setUser(e.currentTarget.value)} />
      <input data-testid="password" class="input" placeholder="Mật khẩu" type="password" autoComplete="current-password" value={pass} onInput={(e) => setPass(e.currentTarget.value)} />
      <div style={{ display: 'flex', gap: 8 }}>
        <button data-testid="login" class="btn primary" style={{ flex: 1 }} disabled={busy || !user || !pass} type="submit">Đăng nhập</button>
        <button data-testid="register" class="btn" style={{ flex: 1 }} disabled={busy || !user || !pass} type="button" onClick={() => void go(true)}>Đăng ký</button>
      </div>
      {err && <p data-testid="login-error" style={{ color: '#ff8a80', margin: 0 }}>{err}</p>}
    </form>
  );
}

const box = { position: 'absolute', inset: 0, margin: 'auto', width: 'min(400px, calc(100% - 32px))', height: 'fit-content', display: 'flex', flexDirection: 'column', gap: 10 } as const;
