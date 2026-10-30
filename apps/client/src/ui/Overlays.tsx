import { useEffect, useState } from 'preact/hooks';
import type { Character, Pet } from '@phimond/protocol';
import type { GameWorld } from '../game/world.ts';
import { currentMap } from '../game/world.ts';
import { ELEMENT_VI, ITEM_DESC, RACE_VI, ROLE_LABEL, ROLE_NOT_OPEN, STARTERS, viName } from '../game/content.ts';
import { asset, hd2dUrl } from '../render/assets.ts';
import { PRESETS, settings, settingsVolatile, updateSettings, type Quality } from '../state/settings.ts';
import { closeOverlay, overlay } from '../state/ui.ts';
import { session } from '../state/app.ts';
import { PetPortrait } from './PetArt.tsx';
import { iconFor } from './skin.ts';
import { sfx } from './sound.ts';
import { MAX_PARTY, partyOf } from '../game/party.ts';
import { npcLabel, questHint, questViews, type QuestDef } from '../game/quests.ts';
import { useSignal } from '@preact/signals';

type Rules = { heal_cost?: number; learn_cost?: number; appraisal_cost?: number };

export function Overlays({ world, ch }: { world: GameWorld; ch: Character }) {
  const o = overlay.value;
  const npcTab = useSignal<string | null>(null);
  useEffect(() => {
    if (o.kind !== 'none') sfx('open');
  }, [o.kind]);
  if (o.kind === 'none') return null;
  // Một bộ khung cho mọi bảng (đánh giá P1: trước đây 5 kiểu khung khác nhau). Bảng chỉ khác tiêu đề và biểu tượng.
  const skin = 'dialogue';
  // Hội thoại NPC mở bằng khung thấp ở đáy (cảnh vẫn nhìn thấy); chọn một dịch vụ thì mở bảng giữa như mọi bảng khác.
  const bottom = o.kind === 'npc' && npcTab.value === null;
  return (
    <div class={`scrim ${bottom ? 'bottom' : ''}`} data-testid="overlay" onPointerDown={(e) => !bottom && e.target === e.currentTarget && closeOverlay()}>
      <div class={`dialog skin-${skin} ${bottom ? 'bottom' : ''}`} role="dialog">
        {!bottom && <button class="btn-close" aria-label="Đóng" data-testid="overlay-close" style={{ position: 'absolute', top: 2, right: 2, zIndex: 2 }} onClick={closeOverlay} />}
        {o.kind === 'menu' && <Menu page={o.page} world={world} ch={ch} />}
        {o.kind === 'npc' && <NpcDialog key={o.npcId} npcId={o.npcId} line={o.line} world={world} ch={ch} onTab={(t) => (npcTab.value = t)} />}
        {o.kind === 'pedestal' && <PedestalConfirm index={o.index} world={world} />}
        {o.kind === 'pillar' && <PillarMenu world={world} ch={ch} />}
      </div>
    </div>
  );
}

// ------------------------------------------------------------------ Menu
function Menu({ page, world, ch }: { page: 'root' | 'pets' | 'bag' | 'quests' | 'settings'; world: GameWorld; ch: Character }) {
  const go = (p: typeof page) => (overlay.value = { kind: 'menu', page: p });
  if (page === 'pets') return <Pets world={world} ch={ch} />;
  if (page === 'bag') return <Bag world={world} ch={ch} />;
  if (page === 'quests') return <Quests world={world} ch={ch} />;
  if (page === 'settings') return <Settings />;
  return (
    <>
      <h2>Menu</h2>
      <div class="list">
        <button class="btn" onClick={() => go('pets')}>Linh thú</button>
        <button class="btn" onClick={() => go('bag')}>Túi đồ</button>
        <button class="btn" onClick={() => go('quests')}>Nhiệm vụ</button>
        <button class="btn" data-testid="menu-settings" onClick={() => go('settings')}>Cài đặt</button>
        <button class="btn" data-testid="switch-char" onClick={() => { closeOverlay(); void session.leave(); }}>
          Đổi nhân vật
        </button>
        <button class="btn danger" data-testid="logout" onClick={() => void session.logout().then(() => location.reload())}>
          Đăng xuất
        </button>
      </div>
    </>
  );
}

function Back({ to = 'root' }: { to?: 'root' }) {
  return (
    <div class="row">
      <button class="btn" data-testid="overlay-back" onClick={() => (overlay.value = { kind: 'menu', page: to })}>
        Trở về menu
      </button>
    </div>
  );
}

function PartyRow({ p, children }: { p: Pet; children?: preact.ComponentChildren }) {
  return (
    <div class="prow item-flat">
      <PetPortrait species={p.species_id} bust size={52} />
      <div class="pinfo">
        <b>{viName(p.name)}</b>
        <span class="muted">
          Lv {p.level} · {'★'.repeat(Math.max(1, p.star ?? 1))} · HP {p.hp}/{p.max_hp} · MP {p.mp}/{p.max_mp}
        </span>
      </div>
      <div class="pact">{children}</div>
    </div>
  );
}

function Pets({ world, ch }: { world: GameWorld; ch: Character }) {
  const pets = ch.pets.filter((p) => !p.retired);
  const party = partyOf(ch);
  const reserve = pets.filter((p) => !party.includes(p));
  const o = overlay.value;
  const [sel, setSel] = useState<string | null>(o.kind === 'menu' && o.pet ? o.pet : null);
  const p = pets.find((x) => x.id === sel);
  if (p) return <PetDetail world={world} ch={ch} p={p} onBack={() => setSel(null)} />;
  const setParty = (list: Pet[]) => void world.intent('pet.party_set', { pet_ids: list.map((x) => x.id) });
  const move = (i: number, d: -1 | 1) => {
    const next = party.slice();
    [next[i], next[i + d]] = [next[i + d]!, next[i]!];
    setParty(next);
  };
  const detail = (x: Pet) => (
    <button class="btn small" data-testid={`pet-detail-${x.id}`} onClick={() => setSel(x.id)}>
      Chi tiết
    </button>
  );
  return (
    <>
      <h2>Linh thú ({pets.length})</h2>
      {pets.length === 0 && <p class="muted">Bạn chưa có linh thú. Hãy chọn một bệ đá ở Triệu Linh Điện.</p>}
      {party.length > 0 && (
        <>
          <h3 class="pd-h">Đội hình mang theo ({party.length}/{MAX_PARTY})</h3>
          <p class="muted party-note" data-testid="party-note">Chỉ linh thú ở vị trí đầu ra trận. Các con còn lại là dự bị, mang theo nhưng không chiến đấu.</p>
          <div class="prows" data-testid="party-list">
            {party.map((x, i) => (
              <PartyRow key={x.id} p={x}>
                <span class={`party-role ${i === 0 ? 'main' : ''}`}>{i === 0 ? 'Ra trận' : 'Dự bị'}</span>
                <button class="btn small ico" data-testid={`party-up-${x.id}`} disabled={i === 0} aria-label="Đẩy lên" onClick={() => move(i, -1)}>
                  ▲
                </button>
                <button class="btn small ico" data-testid={`party-down-${x.id}`} disabled={i === party.length - 1} aria-label="Đẩy xuống" onClick={() => move(i, 1)}>
                  ▼
                </button>
                <button class="btn small" data-testid={`party-remove-${x.id}`} disabled={party.length <= 1} onClick={() => setParty(party.filter((y) => y !== x))}>
                  Gỡ
                </button>
                {detail(x)}
              </PartyRow>
            ))}
          </div>
        </>
      )}
      {reserve.length > 0 && (
        <>
          <h3 class="pd-h">Linh thú ở nhà</h3>
          <div class="prows">
            {reserve.map((x) => (
              <PartyRow key={x.id} p={x}>
                <button class="btn small" data-testid={`party-add-${x.id}`} disabled={party.length >= MAX_PARTY} onClick={() => setParty([...party, x])}>
                  Thêm vào đội
                </button>
                {detail(x)}
              </PartyRow>
            ))}
          </div>
        </>
      )}
      <Back />
    </>
  );
}

/** Màn chi tiết linh thú: chỉ số, hệ, tộc, kỹ năng, kháng (khi đã giám định). */
function PetDetail({ world, ch, p, onBack }: { world: GameWorld; ch: Character; p: Pet; onBack: () => void }) {
  const sp = world.content.cat.species[p.species_id] as unknown as { element?: string; race?: string; archetype?: string } | undefined;
  const x = p as unknown as Record<string, number | Record<string, number> | undefined>;
  const stat = (k: string) => (typeof x[k] === 'number' ? Math.round(x[k] as number) : '—');
  const grades = p.grades as Record<string, string> | undefined;
  const grade = (k: string) => (p.appraised && grades?.[k] ? <small class={`grade g-${grades[k]}`}> {grades[k]}</small> : null);
  return (
    <>
      <h2>{viName(p.name)}</h2>
      <div class="pet-detail">
        <div class="pd-art">
          <PetPortrait species={p.species_id} size={112} bust />
          <div class="pd-tags">
            <span>Lv {p.level}</span>
            <span>{'★'.repeat(Math.max(1, p.star ?? 1))}</span>
            {sp?.element && <span>Hệ {ELEMENT_VI[sp.element] ?? sp.element}</span>}
            {sp?.race && <span>{RACE_VI[sp.race] ?? sp.race}</span>}
            {p.gender && <span>{p.gender === 'male' ? '♂ Đực' : p.gender === 'female' ? '♀ Cái' : p.gender}</span>}
            {(p.strengthening ?? 0) > 0 && <span>Cường hóa +{p.strengthening}</span>}
            <span>{p.appraised ? 'Đã giám định' : 'Chưa giám định'}</span>
            {p.id === ch.active_pet_id && <span class="on">Con chính</span>}
          </div>
        </div>
        <div class="pd-stats">
          <div><em>HP</em><b>{p.hp}/{p.max_hp}{grade('hp')}</b></div>
          <div><em>MP</em><b>{p.mp}/{p.max_mp}</b></div>
          <div><em>Tấn công</em><b>{stat('attack')}{grade('atk')}</b></div>
          <div><em>Phép</em><b>{stat('magic')}{grade('mag')}</b></div>
          <div><em>Phòng thủ</em><b>{stat('defense')}{grade('def')}</b></div>
          <div><em>Tốc độ</em><b>{stat('speed')}{grade('spd')}</b></div>
          <div><em>Kháng trạng thái</em><b>{stat('status_resistance')}{grade('status_resistance')}</b></div>
          <div><em>EXP</em><b>{p.level >= levelCapOf(world, p) ? 'Tối đa' : `${p.xp ?? 0}/${p.level * 25}`}</b></div>
        </div>
      </div>
      <h3 class="pd-h">Kỹ năng</h3>
      <div class="pd-skills">
        {p.skills.length === 0 && <p class="muted">Chưa học kỹ năng nào (đòn thường luôn dùng được). Học ở NPC dạy kỹ năng.</p>}
        {p.skills.map((id) => {
          const sk = world.content.cat.skills[id] as unknown as SkillDef | undefined;
          const rank = p.skill_ranks?.[id] ?? 1;
          return (
            <div key={id} class="pd-skill">
              <b>
                {sk?.name ?? id} {rank > 1 ? '★'.repeat(rank - 1) : ''}
              </b>
              <span class="muted">{skillLine(sk)}</span>
            </div>
          );
        })}
      </div>
      {!p.appraised && <p class="muted">Chưa giám định: bậc tăng trưởng (D → Perfect) của từng chỉ số còn ẩn.</p>}
      <div class="row">
        <button class="btn" data-testid="pet-detail-back" onClick={onBack}>
          Danh sách linh thú
        </button>
      </div>
    </>
  );
}

function Bag({ world, ch }: { world: GameWorld; ch: Character }) {
  const items = Object.entries(ch.inventory).filter(([, n]) => n > 0);
  const pet = ch.pets.find((p) => p.id === ch.active_pet_id);
  const usable = (id: string) => {
    const it = world.content.cat.items[id] as unknown as { kind?: string } | undefined;
    if (!pet || !it) return null;
    if (it.kind === 'heal') return pet.hp < pet.max_hp ? '' : 'HP đầy';
    if (it.kind === 'mp') return pet.mp < pet.max_mp ? '' : 'MP đầy';
    return null;
  };
  return (
    <>
      <h2>Túi đồ</h2>
      <div class="list">
        {items.length === 0 && <p class="muted">Túi trống.</p>}
        {items.map(([id, n]) => {
          const u = usable(id);
          return (
            <div class="item" key={id}>
              {iconFor(id) && <img class="icon" src={iconFor(id)!} alt="" />}
              <div class="grow">
                <b>{world.content.itemName(id)}</b> <span class="muted">×{n}</span>
                <div class="muted">{ITEM_DESC[id] ?? ''}</div>
              </div>
              {u !== null && (
                <button class="btn small" data-testid={`use-${id}`} disabled={u !== ''} title={u || undefined} onClick={() => void world.intent('item.use', { item_id: id })}>
                  {u || 'Dùng'}
                </button>
              )}
            </div>
          );
        })}
      </div>
      <p class="muted bag-gold">
        <i class="coin" /> {ch.gold} vàng
      </p>
      <Back />
    </>
  );
}

function Quests({ world, ch }: { world: GameWorld; ch: Character }) {
  const views = questViews(ch, world.content);
  const mine = views.filter((v) => v.s && !v.s.claimed);
  const done = views.filter((v) => v.s?.claimed);
  const next = views.find((v) => v.available);
  return (
    <>
      <h2>Nhiệm vụ</h2>
      <div class="list">
        {mine.map((v) => (
          <div class="item quest" key={v.q.id}>
            <div class="grow">
              <b>{v.q.name}</b>
              <div class="muted">{v.q.description}</div>
              <div class="qhint">{v.ready ? 'Xong — báo cáo ở NPC nhiệm vụ để nhận thưởng' : questHint(v, world.content)}</div>
              <QuestReward world={world} q={v.q} />
            </div>
          </div>
        ))}
        {next && (
          <div class="item quest next" key={next.q.id}>
            <div class="grow">
              <b>Tiếp theo: {next.q.name}</b>
              <div class="muted">Gặp {npcLabel(world.content, next.q.giver) || 'NPC nhiệm vụ'} để nhận.</div>
            </div>
          </div>
        )}
        {mine.length === 0 && !next && <p class="muted">Đã xong mọi nhiệm vụ hiện có.</p>}
        {done.length > 0 && <div class="muted">Đã hoàn thành: {done.map((v) => v.q.name).join(' · ')}</div>}
      </div>
      <Back />
    </>
  );
}

function QuestReward({ world, q }: { world: GameWorld; q: QuestDef }) {
  const items = Object.entries(q.items ?? {});
  return (
    <div class="qrw">
      {q.gold ? <span>{q.gold} vàng</span> : null}
      {q.xp ? <span>{q.xp} EXP</span> : null}
      {items.map(([id, n]) => (
        <span key={id}>
          {world.content.itemName(id)} ×{n}
        </span>
      ))}
    </div>
  );
}

/** Tài khoản: email khôi phục (tuỳ chọn) và xoá tài khoản vĩnh viễn. */
function AccountSection() {
  const [acc, setAcc] = useState<{ username: string; has_email: boolean; email: string } | null>(null);
  const [email, setEmail] = useState('');
  const [msg, setMsg] = useState('');
  const [err, setErr] = useState('');
  const [del, setDel] = useState(false);
  const [pw, setPw] = useState('');
  const [busy, setBusy] = useState(false);
  const load = () => session.accountInfo().then(setAcc).catch(() => setAcc(null));
  useEffect(() => {
    void load();
  }, []);
  if (!acc) return null;
  const run = async (fn: () => Promise<void>) => {
    setBusy(true);
    setErr('');
    setMsg('');
    try {
      await fn();
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  };
  return (
    <>
      <h3 class="set-h">Tài khoản</h3>
      <p class="muted set-note" data-testid="account-name">Tài khoản: <b>{acc.username}</b> · Email khôi phục: {acc.has_email ? acc.email : 'chưa có'}</p>
      <div class="set-row">
        <input class="input" data-testid="account-email" type="email" placeholder={acc.has_email ? 'Đổi email (để trống để gỡ)' : 'Thêm email để lấy lại mật khẩu'} value={email} onInput={(e) => setEmail(e.currentTarget.value)} />
        <button
          class="btn small"
          data-testid="account-email-save"
          disabled={busy || (!email.trim() && !acc.has_email)}
          onClick={() =>
            void run(async () => {
              await session.setEmail(email.trim());
              setEmail('');
              setMsg(email.trim() ? 'Đã lưu email.' : 'Đã gỡ email.');
              await load();
            })
          }
        >
          Lưu
        </button>
      </div>
      {!del ? (
        <button class="btn danger" data-testid="account-delete-open" onClick={() => setDel(true)}>Xoá tài khoản…</button>
      ) : (
        <div class="set-row" style={{ flexDirection: 'column', alignItems: 'stretch', gap: 6 }}>
          <p class="muted set-note">Xoá vĩnh viễn tài khoản, cả 3 nhân vật, linh thú và vật phẩm. Không khôi phục được. Nhập mật khẩu để xác nhận.</p>
          <input class="input" data-testid="account-delete-password" type="password" autoComplete="current-password" placeholder="Mật khẩu" value={pw} onInput={(e) => setPw(e.currentTarget.value)} />
          <div style={{ display: 'flex', gap: 8 }}>
            <button class="btn danger" data-testid="account-delete-confirm" disabled={busy || !pw} onClick={() => void run(async () => { await session.deleteAccount(pw); location.reload(); })}>Xoá vĩnh viễn</button>
            <button class="btn" disabled={busy} onClick={() => { setDel(false); setPw(''); }}>Huỷ</button>
          </div>
        </div>
      )}
      {msg && <p class="muted set-note" data-testid="account-msg" style={{ color: '#a8e6a1' }}>{msg}</p>}
      {err && <p class="muted set-note" data-testid="account-error" style={{ color: '#ff8a80' }}>{err}</p>}
      <p class="muted set-note"><a href="/terms.html" target="_blank" rel="noopener">Điều khoản</a> · <a href="/privacy.html" target="_blank" rel="noopener">Quyền riêng tư</a></p>
    </>
  );
}

function Settings() {
  const s = settings.value;
  const row = (label: string, testid: string | undefined, opts: [string, string, boolean, () => void, string?][]) => (
    <div class="set-row">
      <span class="set-l">{label}</span>
      <div class="seg" data-testid={testid}>
        {opts.map(([k, text, on, fn, tid]) => (
          <button key={k} class={`btn ${on ? 'on' : ''}`} data-testid={tid} onClick={fn}>
            {text}
          </button>
        ))}
      </div>
    </div>
  );
  return (
    <>
      <h2>Cài đặt</h2>
      <div class="set-grid">
        <h3 class="set-h">Đồ họa</h3>
        {row('Đồ họa', 'quality', (['low', 'medium', 'high'] as Quality[]).map((q) => [q, PRESETS[q].label, s.quality === q, () => updateSettings({ quality: q }), `quality-${q}`]))}
        <p class="muted set-note">{s.quality === 'low' ? 'Nhẹ nhất: tắt bóng, hậu kỳ và hiệu ứng phụ.' : s.quality === 'medium' ? 'Chỉnh màu theo giờ, làm mờ HD-2D, đèn và tia nắng.' : 'Thêm bloom và bóng đổ thật; tốn pin hơn.'}</p>
        {row('Khung hình', undefined, ([30, 60] as const).map((f) => [String(f), `${f} FPS`, s.fps === f, () => updateSettings({ fps: f }), `fps-${f}`]))}
        {row('Thời gian', 'time-mode', ([['auto', 'Theo máy'], ['day', 'Ngày'], ['dusk', 'Hoàng hôn'], ['night', 'Đêm']] as const).map(([k, t]) => [k, t, s.time === k, () => updateSettings({ time: k }), `time-${k}`]))}
        <h3 class="set-h">Âm thanh</h3>
        <div class="set-row">
          <span class="set-l">Hiệu ứng</span>
          <label class="slider" data-testid="sound">
            <input type="range" min="0" max="100" step="5" value={Math.round(s.sound * 100)} data-testid="sound-slider" onInput={(e) => updateSettings({ sound: Number((e.currentTarget as HTMLInputElement).value) / 100 })} />
            <b>{s.sound === 0 ? 'Tắt' : `${Math.round(s.sound * 100)}%`}</b>
          </label>
        </div>
        <div class="set-row">
          <span class="set-l">Nhạc nền</span>
          <label class="slider" data-testid="music">
            <input type="range" min="0" max="100" step="5" value={Math.round(s.music * 100)} data-testid="music-slider" onInput={(e) => updateSettings({ music: Number((e.currentTarget as HTMLInputElement).value) / 100 })} />
            <b>{s.music === 0 ? 'Tắt' : `${Math.round(s.music * 100)}%`}</b>
          </label>
        </div>
        <h3 class="set-h">Giao diện</h3>
        {row('Phím điều hướng', undefined, [['on', 'Hiện', s.dpad, () => updateSettings({ dpad: true })], ['off', 'Ẩn', !s.dpad, () => updateSettings({ dpad: false })]])}
        {row('Giao diện', 'hud-density', [['full', 'Đầy đủ', s.hud === 'full', () => updateSettings({ hud: 'full' }), 'hud-full'], ['compact', 'Gọn', s.hud === 'compact', () => updateSettings({ hud: 'compact' }), 'hud-compact']])}
        {settingsVolatile.value && <p class="muted">Trình duyệt không cho lưu cài đặt; lựa chọn chỉ giữ tới khi tải lại trang.</p>}
        <AccountSection />
      </div>
      <Back />
    </>
  );
}

// ------------------------------------------------------------------ NPC
const ROLE_ICON: Record<string, string> = { heal: 'npc_healer', shop: 'npc_shop', learn: 'npc_skill', quest: 'npc_quest', teleport: 'npc_teleport', guild: 'npc_guild', arena_info: 'npc_arena' };

function NpcDialog({ npcId, line, world, ch, onTab }: { npcId: string; line: string; world: GameWorld; ch: Character; onTab: (t: string | null) => void }) {
  const n = world.content.cat.npcs[npcId];
  const [tab, setTabState] = useState<string | null>(null);
  const setTab = (t: string | null) => {
    setTabState(t);
    onTab(t);
  };
  useEffect(() => onTab(null), []);
  if (!n) return null;
  const rules = (world.content.cat as unknown as { rules?: Rules }).rules ?? {};
  const roles = n.roles.filter((r) => r !== 'free' && r !== 'guide');
  const img = asset(`npc-${npcId}`) ? hd2dUrl(`npc-${npcId}`) : asset('city-mailbox') && npcId === 'sq_mailbox' ? hd2dUrl('city-mailbox') : null;
  if (tab === null) {
    return (
      <div class="npc-bottom" data-testid="npc-bottom">
        <div class="nb-portrait"><div class="nb-sock">{img ? <img src={img} alt="" /> : <div class="nb-ph" />}</div></div>
        <div class="nb-main">
          <div class="nb-name" data-testid="npc-name">{n.name}</div>
          <Typed text={line} />
        </div>
        <div class="nb-choices">
          {roles.map((r) => (
            <button key={r} class="nb-choice" data-testid={`npc-role-${r}`} onClick={() => (r === 'teleport' ? (overlay.value = { kind: 'pillar' }) : setTab(r))}>
              {ROLE_ICON[r] && iconFor(ROLE_ICON[r]) && <img class="icon" src={iconFor(ROLE_ICON[r])!} alt="" />}
              {ROLE_LABEL[r] ?? r}
            </button>
          ))}
          <button class="nb-choice bye" data-testid="npc-close" onClick={closeOverlay}>
            Tạm biệt
          </button>
        </div>
      </div>
    );
  }
  return (
    <>
      <div class="npc-head">
        {img && <img src={img} alt="" />}
        <div>
          <h2 data-testid="npc-name">{n.name}</h2>
          <p data-testid="npc-line">{line}</p>
        </div>
      </div>
      {roles.length > 0 && (
        <div class="seg" style={{ marginBottom: 10 }}>
          {roles.map((r) => (
            <button key={r} class={`tab ${tab === r ? 'on' : ''}`} data-testid={`npc-role-${r}`} onClick={() => (r === 'teleport' ? (overlay.value = { kind: 'pillar' }) : setTab(r))}>
              {ROLE_ICON[r] && iconFor(ROLE_ICON[r]) && <img class="icon" style={{ width: 22, height: 22, verticalAlign: -5, marginRight: 4 }} src={iconFor(ROLE_ICON[r])!} alt="" />}
              {ROLE_LABEL[r] ?? r}
            </button>
          ))}
        </div>
      )}
      {tab && ROLE_NOT_OPEN.has(tab) && <p class="muted">Chức năng {ROLE_LABEL[tab]} chưa mở ở bản này.</p>}
      {tab === 'heal' && (
        <div class="list">
          <button class="btn primary" data-testid="do-heal" onClick={() => void world.intent('pet.heal', {})}>
            Hồi phục toàn đội ({rules.heal_cost ?? 0} vàng)
          </button>
        </div>
      )}
      {tab === 'shop' && <Shop world={world} ch={ch} />}
      {tab === 'learn' && <Learn world={world} ch={ch} />}
      {tab === 'quest' && <QuestDesk world={world} ch={ch} npcId={npcId} />}
      <div class="row">
        <button class="btn" data-testid="npc-close" onClick={closeOverlay}>
          Tạm biệt
        </button>
      </div>
    </>
  );
}

/** Chữ hiện dần; toàn bộ câu luôn nằm trong DOM (phần chưa hiện bị ẩn) để đọc/kiểm thử không phụ thuộc nhịp gõ. Bấm để hiện hết. */
function Typed({ text }: { text: string }) {
  const [n, setN] = useState(0);
  useEffect(() => {
    setN(0);
    const reduce = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
    if (reduce) {
      setN(text.length);
      return;
    }
    const t = window.setInterval(() => setN((v) => (v >= text.length ? v : v + 1)), 22);
    return () => window.clearInterval(t);
  }, [text]);
  return (
    <p class="nb-line" data-testid="npc-line" onClick={() => setN(text.length)}>
      <span>{text.slice(0, n)}</span>
      <span class="rest">{text.slice(n)}</span>
      {n >= text.length && <span class="more" aria-hidden="true">▼</span>}
    </p>
  );
}

function Shop({ world, ch }: { world: GameWorld; ch: Character }) {
  const items = Object.values(world.content.cat.items) as { id: string; name: string; price?: number; kind?: string }[];
  return (
    <div class="list">
      {items
        .filter((i) => (i.price ?? 0) > 0)
        .map((i) => (
          <div class="item" key={i.id}>
            {iconFor(i.id) && <img class="icon" src={iconFor(i.id)!} alt="" />}
            <div class="grow">
              {i.name}
              <div class="muted">
                {i.price} vàng · đang có {ch.inventory[i.id] ?? 0}
              </div>
            </div>
            <button class="btn small" disabled={ch.gold < (i.price ?? 0)} data-testid={`buy-${i.id}`} onClick={() => void world.intent('shop.buy', { item_id: i.id, quantity: 1 })}>
              Mua 1
            </button>
            <button class="btn small" disabled={ch.gold < (i.price ?? 0) * 5} onClick={() => void world.intent('shop.buy', { item_id: i.id, quantity: 5 })}>
              Mua 5
            </button>
          </div>
        ))}
    </div>
  );
}

/** Cấp tối đa theo Sao (P11: 60/70/80/90/100). */
const levelCapOf = (world: GameWorld, p: Pet) => [60, 70, 80, 90, 100][Math.max(1, Math.min(5, (world.content.cat.species[p.species_id] as unknown as { star?: number } | undefined)?.star ?? p.star ?? 1)) - 1]!;
type SkillDef = { name: string; kind?: string; element?: string; mp?: number; cooldown?: number; learn_level?: number; power_pm?: number; description?: string; rank_policy?: string };
/** Kỹ năng dùng chung mọi loài học được (đồng bộ server: skills_learn.go). */
const COMMON_SKILLS = ['strike', 'heal', 'guard'];
const KIND_VI: Record<string, string> = { physical: 'Vật lý', magic: 'Phép', heal: 'Hồi máu', shield: 'Khiên', buff: 'Cường hóa', control: 'Khống chế', debuff: 'Suy yếu', cleanse: 'Giải trừ', dispel: 'Xua tan', resource: 'Hồi MP', revive: 'Hồi sinh' };
/** Giá học bậc 1 = 20 + 10 × cấp học; học lại kỹ năng cũ của chính pet còn 20% (làm tròn lên). */
const learnPrice = (s: SkillDef | undefined, relearn: boolean) => {
  const base = 20 + 10 * (s?.learn_level ?? 1);
  return relearn ? Math.ceil((base * 20) / 100) : base;
};
/** Nâng bậc: bậc 2 cần Lv ≥ max(20, cấp học+15), giá 3×; bậc 3 cần Lv ≥ max(40, cấp học+30), giá 6×. */
const upgradeInfo = (s: SkillDef | undefined, rank: number) => {
  const lv = s?.learn_level ?? 1;
  const base = 20 + 10 * lv;
  return rank === 1 ? { gate: Math.max(20, lv + 15), price: base * 3 } : { gate: Math.max(40, lv + 30), price: base * 6 };
};
const skillLine = (s: SkillDef | undefined) =>
  `${KIND_VI[s?.kind ?? ''] ?? 'Hiệu ứng'}${s?.element && s.element !== 'neutral' ? ` · ${ELEMENT_VI[s.element] ?? s.element}` : ''}${s?.power_pm ? ` · Uy lực ${(s.power_pm / 1000).toFixed(2)}` : ''} · ${s?.mp ?? 0} MP${s?.cooldown ? ` · hồi ${s.cooldown} lượt` : ''}`;

function Learn({ world, ch }: { world: GameWorld; ch: Character }) {
  const [replacing, setReplacing] = useState<string | null>(null);
  const pet = ch.pets.find((p) => p.id === ch.active_pet_id);
  if (!pet) return <p class="muted">Bạn chưa có linh thú.</p>;
  const sp = world.content.cat.species[pet.species_id] as unknown as { skills?: string[] };
  const defs = world.content.cat.skills as unknown as Record<string, SkillDef>;
  const slots = 6;
  const full = pet.skills.length >= slots;
  const pool = [...new Set([...(sp?.skills ?? []), ...(pet.inherited_pool ?? []), ...COMMON_SKILLS])].filter((id) => defs[id] && !pet.skills.includes(id));
  const learn = (id: string, replace?: string) => {
    setReplacing(null);
    void world.intent('pet.learn', replace ? { pet_id: pet.id, skill_id: id, replace_id: replace } : { pet_id: pet.id, skill_id: id });
  };
  return (
    <div class="list" data-testid="learn-panel">
      <div class="muted">
        Dạy cho {viName(pet.name)} (Lv {pet.level}) · đã học {pet.skills.length}/{slots} kỹ năng · đòn thường không chiếm ô
      </div>
      {pet.skills.length > 0 && <h3 class="pd-h">Đã học</h3>}
      {pet.skills.map((id) => {
        const s = defs[id];
        const rank = pet.skill_ranks?.[id] ?? 1;
        const up = s?.rank_policy === 'damage_heal_3_ranks' && rank < 3 ? upgradeInfo(s, rank) : null;
        return (
          <div class="item" key={id} data-testid={`learned-${id}`}>
            {iconFor(`skill_${id}`) && <img class="icon" src={iconFor(`skill_${id}`)!} alt="" />}
            <div class="grow">
              {s?.name ?? id} {rank > 1 ? '★'.repeat(rank - 1) : ''}
              <div class="muted">{skillLine(s)}</div>
            </div>
            {up && (
              <button class="btn small" data-testid={`upgrade-${id}`} disabled={pet.level < up.gate || ch.gold < up.price} title={pet.level < up.gate ? `Cần Lv ${up.gate}` : ''} onClick={() => void world.intent('pet.skill_upgrade', { pet_id: pet.id, skill_id: id })}>
                Nâng bậc {rank + 1} · {up.price} vàng{pet.level < up.gate ? ` (Lv ${up.gate})` : ''}
              </button>
            )}
          </div>
        );
      })}
      <h3 class="pd-h">Có thể học</h3>
      {pool.length === 0 && <p class="muted">Linh thú đã học hết kỹ năng được phép.</p>}
      {pool.map((id) => {
        const s = defs[id];
        const lv = s?.learn_level ?? 1;
        const relearn = (pet.learned ?? []).includes(id);
        const price = learnPrice(s, relearn);
        return (
          <div class="item" key={id}>
            {iconFor(`skill_${id}`) && <img class="icon" src={iconFor(`skill_${id}`)!} alt="" />}
            <div class="grow">
              {s?.name ?? id}
              <div class="muted">
                Cần Lv {lv} · {skillLine(s)}
              </div>
              {s?.description && <div class="muted">{s.description}</div>}
            </div>
            <button class="btn small" data-testid={`learn-${id}`} disabled={pet.level < lv || ch.gold < price} onClick={() => (full ? setReplacing(id) : learn(id))}>
              {full ? 'Thay thế…' : 'Học'} · {price} vàng{relearn ? ' (học lại)' : ''}
            </button>
          </div>
        );
      })}
      {replacing && (
        <div class="item" data-testid="learn-replace">
          <div class="grow">
            <b>Đã đủ {slots} kỹ năng.</b> Chọn kỹ năng bị quên để học {defs[replacing]?.name ?? replacing} (kỹ năng quên đi mất cả bậc nâng):
            <div class="row">
              {pet.skills.map((id) => (
                <button key={id} class="btn small" onClick={() => learn(replacing, id)}>
                  {defs[id]?.name ?? id}
                </button>
              ))}
              <button class="btn small" onClick={() => setReplacing(null)}>
                Hủy
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function QuestDesk({ world, ch, npcId }: { world: GameWorld; ch: Character; npcId: string }) {
  // Người giao: chỉ nhiệm vụ của NPC này (đủ điều kiện). Báo cáo: nhiệm vụ đã xong nhận thưởng ở bất kỳ NPC nhiệm vụ nào.
  const views = questViews(ch, world.content).filter((v) => v.ready || (v.s && !v.s.claimed && v.q.giver === npcId) || (v.available && (v.q.giver ?? npcId) === npcId));
  if (views.length === 0) {
    const next = questViews(ch, world.content).find((v) => v.available);
    return <p class="muted">{next ? `Hiện ta không có việc cho bạn. ${next.q.name}: gặp ${npcLabel(world.content, next.q.giver)}.` : 'Hiện ta không có việc cho bạn.'}</p>;
  }
  return (
    <div class="list">
      {views.map(({ q, s, ready }) => (
        <div class="item quest" key={q.id}>
          <div class="grow">
            <b>{q.name}</b>
            <div class="muted">{q.description}</div>
            <QuestReward world={world} q={q} />
          </div>
          {!s && (
            <button class="btn small" data-testid={`quest-accept-${q.id}`} onClick={() => void world.intent('quest.accept', { quest_id: q.id })}>
              Nhận
            </button>
          )}
          {s && ready && (
            <button class="btn small primary" data-testid={`quest-claim-${q.id}`} onClick={() => void world.intent('quest.claim', { quest_id: q.id })}>
              Nhận thưởng
            </button>
          )}
          {s && !ready && <span class="muted">{s.claimed ? 'Đã xong' : `${s.progress}/${q.count ?? 1}`}</span>}
        </div>
      ))}
    </div>
  );
}

// ------------------------------------------------------------------ Bệ đá, trụ
function PedestalConfirm({ index, world }: { index: number; world: GameWorld }) {
  const map = currentMap.value;
  const ped = map?.pedestals.find((p) => p.index === index);
  if (!ped) return null;
  const st = STARTERS[ped.starter] ?? { name: ped.starter, blurb: '' };
  const sp = world.content.cat.species[ped.starter] as unknown as { element?: string; race?: string; base?: Record<string, number>; skills?: string[] } | undefined;
  const b = sp?.base ?? {};
  // Thang thanh: HP/10 cho cùng thang với các chỉ số khác; tối đa ~50.
  const bar = (label: string, v = 0) => (
    <div class="st-bar">
      <em>{label}</em>
      <i style={{ width: `${Math.min(100, v * 2)}%` }} />
    </div>
  );
  return (
    <>
      <h2>Bệ triệu hồi: {st.name}</h2>
      <div class="item starter-card" style={{ marginBottom: 12 }}>
        <PetPortrait species={ped.species} size={88} />
        <div class="grow">
          <div class="pd-tags">
            {sp?.element && <span>Hệ {ELEMENT_VI[sp.element] ?? sp.element}</span>}
            {sp?.race && <span>{RACE_VI[sp.race] ?? sp.race}</span>}
          </div>
          <p style={{ margin: '6px 0' }}>{st.blurb}</p>
          <div class="st-bars">
            {bar('Máu', (b.hp ?? 0) / 10)}
            {bar('Tấn công', b.atk)}
            {bar('Phép', b.mag)}
            {bar('Phòng thủ', b.def)}
            {bar('Tốc độ', b.spd)}
          </div>
          <div class="muted">Linh thú mới chưa biết kỹ năng nào: nhận nhiệm vụ đầu ở Kiểm Lâm Lio trong Bìa Rừng Lục Bảo, ông sẽ tặng một đòn đầu tiên. Sau khi chọn, bạn được đưa thẳng tới đó.</div>
        </div>
      </div>
      <div class="row">
        <button class="btn primary" data-testid="starter-confirm" onClick={() => void world.chooseStarter(index)}>
          Chọn {st.name}
        </button>
        <button class="btn" onClick={closeOverlay}>
          Xem bệ khác
        </button>
      </div>
    </>
  );
}

function PillarMenu({ world, ch }: { world: GameWorld; ch: Character }) {
  const pillar = currentMap.value?.pillar;
  if (!pillar) return <p>Không có trụ dịch chuyển ở đây.</p>;
  return (
    <>
      <h2>Trụ Thạch dịch chuyển</h2>
      <p class="muted">Chọn nơi muốn tới.</p>
      <div class="list">
        {pillar.dest.map((d) => {
          const low = (d.min_level ?? 0) > ch.level;
          return (
            <div class="item" key={d.map}>
              <div class="grow">
                {world.content.mapName(d.map)}
                {d.locked && <div class="muted">Chưa mở</div>}
                {low && <div class="muted">Cần cấp {d.min_level}</div>}
              </div>
              <button class="btn small" disabled={d.locked || low} data-testid={`travel-${d.map}`} onClick={() => void world.travel(d.map)}>
                Đi
              </button>
            </div>
          );
        })}
      </div>
    </>
  );
}
