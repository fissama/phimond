import { useState } from 'preact/hooks';
import { hd2dUrl } from '../render/assets.ts';
import { session } from '../state/app.ts';
import type { SlotSummary } from '../net/session.ts';
import { LoginBackdrop } from './LoginBackdrop.tsx';

type Gender = 'male' | 'female';
const GENDER_VI: Record<Gender, string> = { male: 'Nam', female: 'Nữ' };

/** Hình đứng chờ 4 khung của nhân vật (dải idle), chạy bằng CSS. */
function Portrait({ gender, dim }: { gender: Gender; dim?: boolean }) {
  return <span class={`cs-pv${dim ? ' dim' : ''}`} style={{ backgroundImage: `url(${hd2dUrl(`player-${gender}`, 'idle')})` }} aria-hidden="true" />;
}

/** Màn chọn nhân vật: 3 ô độc lập mỗi tài khoản. Ô trống mở ra bước tạo nhân vật. */
export function SlotSelect() {
  const slots = session.slots.value ?? [];
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const go = async (slot: number) => {
    setBusy(true);
    setErr('');
    try {
      await session.enter(slot);
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
      setBusy(false);
    }
  };
  return (
    <>
    <LoginBackdrop />
    <div class="cs-root" data-testid="slot-select">
      <div class="cs-box">
        <h2 class="cs-title">Chọn nhân vật</h2>
        <div class="cs-slots">
          {slots.map((s) => (
            <SlotCard key={s.slot} s={s} busy={busy} onPick={() => void go(s.slot)} />
          ))}
        </div>
        {err && <p class="cs-err">{err}</p>}
        <button class="btn" data-testid="slot-logout" onClick={() => void session.logout()}>Đăng xuất</button>
      </div>
    </div>
    </>
  );
}

function SlotCard({ s, busy, onPick }: { s: SlotSummary; busy: boolean; onPick: () => void }) {
  const g: Gender = s.gender === 'female' ? 'female' : 'male';
  return (
    <button class={`cs-slot${s.empty ? ' empty' : ''}`} data-testid={`slot-${s.slot + 1}`} disabled={busy} onClick={onPick}>
      <span class="cs-no">Ô {s.slot + 1}</span>
      {s.empty ? (
        <>
          <span class="cs-plus">＋</span>
          <span class="cs-name">Ô trống</span>
          <span class="cs-sub">Tạo nhân vật mới</span>
        </>
      ) : (
        <>
          <Portrait gender={g} />
          <span class="cs-name">{s.name}</span>
          <span class="cs-sub">{GENDER_VI[g]} · Lv {s.level ?? 1}</span>
          <span class="cs-sub">{s.pet ? `Linh thú: ${s.pet}` : 'Chưa có linh thú'}</span>
        </>
      )}
    </button>
  );
}

/** Bước tạo nhân vật cho ô nháp: chọn nam/nữ, đặt tên, rồi xuất hiện giữa vòng triệu hồi. */
export function CreateCharacter() {
  const [gender, setGender] = useState<Gender>('male');
  const [name, setName] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const ok = [...name.trim()].length >= 2;
  const create = async () => {
    setBusy(true);
    setErr('');
    const r = await session.send('character.create', { name: name.trim(), gender });
    if (!r.ok) {
      setErr(r.message);
      setBusy(false);
    }
  };
  return (
    <>
    <LoginBackdrop />
    <div class="cs-root" data-testid="create-character">
      <form
        class="cs-box"
        onSubmit={(e) => {
          e.preventDefault();
          if (ok && !busy) void create();
        }}
      >
        <h2 class="cs-title">Tạo nhân vật</h2>
        <div class="cs-genders" role="radiogroup" aria-label="Giới tính">
          {(['male', 'female'] as const).map((g) => (
            <button
              type="button"
              role="radio"
              aria-checked={gender === g}
              class={`cs-gender${gender === g ? ' on' : ''}`}
              data-testid={`gender-${g}`}
              onClick={() => setGender(g)}
            >
              <Portrait gender={g} dim={gender !== g} />
              <span class="cs-name">{GENDER_VI[g]}</span>
            </button>
          ))}
        </div>
        <input data-testid="char-name" class="input" placeholder="Tên nhân vật (2–16 ký tự)" maxLength={16} value={name} onInput={(e) => setName(e.currentTarget.value)} />
        {err && <p class="cs-err" data-testid="create-error">{err}</p>}
        <div style={{ display: 'flex', gap: 8 }}>
          <button type="button" class="btn" style={{ flex: 1 }} disabled={busy} onClick={() => void session.leave()}>Quay lại</button>
          <button type="submit" class="btn primary" data-testid="char-create" style={{ flex: 1 }} disabled={busy || !ok}>Bắt đầu</button>
        </div>
      </form>
    </div>
    </>
  );
}
