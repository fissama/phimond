import { useState } from 'preact/hooks';
import { session } from '../state/app.ts';

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
      style={box}
      onSubmit={(e) => {
        e.preventDefault();
        void go(false);
      }}
    >
      <h1 style={{ margin: '0 0 12px', fontSize: 28, letterSpacing: 2 }}>PHIMOND</h1>
      <input data-testid="username" style={input} placeholder="Tài khoản" autoComplete="username" value={user} onInput={(e) => setUser(e.currentTarget.value)} />
      <input data-testid="password" style={input} placeholder="Mật khẩu" type="password" autoComplete="current-password" value={pass} onInput={(e) => setPass(e.currentTarget.value)} />
      <div style={{ display: 'flex', gap: 8 }}>
        <button data-testid="login" style={btn} disabled={busy || !user || !pass} type="submit">Đăng nhập</button>
        <button data-testid="register" style={btn} disabled={busy || !user || !pass} type="button" onClick={() => void go(true)}>Đăng ký</button>
      </div>
      {err && <p data-testid="login-error" style={{ color: '#ff8a80', margin: 0 }}>{err}</p>}
    </form>
  );
}

const box = { position: 'absolute', inset: 0, margin: 'auto', width: 'min(320px, calc(100% - 32px))', height: 'fit-content', display: 'flex', flexDirection: 'column', gap: 10 } as const;
const input = { padding: '10px 12px', fontSize: 16, borderRadius: 6, border: '1px solid #3a4560', background: '#1a2133', color: 'inherit' } as const;
const btn = { flex: 1, padding: '10px 12px', fontSize: 16, borderRadius: 6, border: 0, background: '#c9a24a', color: '#1a1408', fontWeight: 600 } as const;
