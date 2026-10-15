import { useEffect, useRef, useState } from 'preact/hooks';
import { signal } from '@preact/signals';
import type { Game, Channel, Dir } from '../game/controller.ts';
import { Engine } from '../render/engine.ts';
import { Stage } from '../render/stage.ts';
import { T, watchScale } from './scale.ts';
import { MenuHost, PetIcon, Shortcuts, statsOn } from './Menus.tsx';
import { runBench } from '../dev/bench.ts';
import { LoadingScreen, Wordmark } from './Loading.tsx';

declare global { interface Window { __game?: unknown } }

// ---------- Đăng nhập (bố cục theo JAR: nền slideshow intro, Vào game / Đăng ký, trạng thái server) ----------
const INTRO = ['intro1', 'intro2', 'intro3'];
function savedUser(): string { try { return localStorage.getItem('phimond.user') ?? ''; } catch { return ''; } }
export function Login({ game, local }: { game: Game; local?: boolean }) {
  const [u, setU] = useState(savedUser); const [p, setP] = useState(''); const [err, setErr] = useState(''); const [busy, setBusy] = useState(false);
  const [remember, setRemember] = useState(() => savedUser() !== ''); const [slide, setSlide] = useState(0);
  useEffect(() => { const i = setInterval(() => setSlide((n) => (n + 1) % INTRO.length), 6500); return () => clearInterval(i); }, []);
  const nameOk = /^[a-z0-9_]{3,24}$/.test(u.trim()); const passOk = p.length >= 10 && p.length <= 72;
  const go = async (kind: 'login' | 'register') => {
    if (busy) return; setBusy(true); setErr('');
    const m = await game.signIn(kind, u.trim(), p); setBusy(false);
    try { if (!m) { if (remember) localStorage.setItem('phimond.user', u.trim()); else localStorage.removeItem('phimond.user'); } } catch { /* ignore */ }
    if (m) setErr(m);
  };
  const online = game.session.status.value === 'online';
  return (
    <main class="login">
      <div class="slides" aria-hidden="true">{INTRO.map((n, i) => <div class={`sl ${i === slide ? 'on' : ''}`} style={`background-image:url(./assets/login/${n}.webp)`} />)}</div>
      <div class="vig" aria-hidden="true" />
      <div class="lcol">
        <Wordmark />
        <form class="box" onSubmit={(e) => { e.preventDefault(); void go('login'); }}>
          {local && <div class="msg" style="text-align:center">Bản thử chạy ngay trong trình duyệt — dữ liệu mất khi đóng trang.</div>}
          <label>Tên tài khoản<input type="text" autocomplete="username" autocapitalize="off" spellcheck={false} value={u} onInput={(e) => setU((e.target as HTMLInputElement).value)} /></label>
          <label>Mật khẩu<input type="password" autocomplete="current-password" value={p} onInput={(e) => setP((e.target as HTMLInputElement).value)} /></label>
          <label class="chk"><input type="checkbox" checked={remember} onChange={(e) => setRemember((e.target as HTMLInputElement).checked)} />Nhớ tên tài khoản</label>
          <div class="err" role="alert">{err}</div>
          <div class="lrow">
            <button class="lbtn ok otl" type="submit" disabled={busy || !u || !p}><span class="rt">{busy ? 'Đang vào…' : 'Vào game'}</span></button>
            <button class="lbtn bk otl" type="button" disabled={busy || !nameOk || !passOk} onClick={() => void go('register')}><span class="rt">Đăng ký</span></button>
          </div>
          <ul class="rules" aria-label="Quy tắc tài khoản"><li class={nameOk ? 'ok' : u ? 'bad' : ''}>Tên: 3–24 ký tự, chỉ a–z thường, số 0–9 và dấu _</li><li class={passOk ? 'ok' : p ? 'bad' : ''}>Mật khẩu: 10–72 ký tự</li></ul>
        </form>
        <div class="srv"><span>Server: <b>Phimond</b></span><span>Trạng thái: <b class={online ? 'g' : 'o'}>{online ? 'Trôi chảy' : 'Sẵn sàng'}</b></span></div>
      </div>
      <div class="ver">Phiên bản: bản thử web · Phimond, dự án khôi phục phi thương mại</div>
    </main>
  );
}

// ---------- D-pad (sprite APK: dpad.png, vùng chạm theo toạ độ gốc) ----------
function Dpad({ game }: { game: Game }) {
  const held = signal<Dir | ''>('');
  const bind = (d: Dir) => ({
    onPointerDown: (e: PointerEvent) => { e.preventDefault(); (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId); held.value = d; game.startWalk(d); },
    onPointerUp: () => { held.value = ''; game.stopWalk(d); },
    onPointerCancel: () => { held.value = ''; game.stopWalk(d); },
    onLostPointerCapture: () => { held.value = ''; game.stopWalk(d); },
  });
  const label: Record<Dir, string> = { up: 'Lên', down: 'Xuống', left: 'Trái', right: 'Phải' };
  return (
    <div class="dpad" data-ui role="group" aria-label="Điều hướng">
      <button class="core" aria-label="Menu nhanh" onClick={() => game.open('Menu')} />
      {(['up', 'down', 'left', 'right'] as Dir[]).map((d) => (
        <button class={`${d[0]} ${held.value === d ? 'on' : ''}`} aria-label={label[d]} {...bind(d)} />
      ))}
    </div>
  );
}

// ---------- Chat (dải giữa, nền xanh nhạt như bản gốc) ----------
const TABS: [Channel, string][] = [['all', 'Chung'], ['sys', 'Hệ thống'], ['pm', 'Riêng'], ['party', 'Đội'], ['world', 'Thế giới'], ['guild', 'Hội']];
const EMPTY: Record<string, string> = { pm: 'Chưa có tin nhắn riêng. Máy chủ hiện chưa hỗ trợ trò chuyện.', party: 'Chưa có đội. Tính năng đội sẽ có sau.', world: 'Kênh thế giới chưa mở ở máy chủ này.', guild: 'Bạn chưa tham gia hội.' };
function Chat({ game }: { game: Game }) {
  const [tab, setTab] = useState<Channel>('all'); const ref = useRef<HTMLDivElement>(null);
  const list = game.chat.value.filter((m) => tab === 'all' || m.channel === tab);
  useEffect(() => { const el = ref.current; if (el) el.scrollTop = el.scrollHeight; }, [list.length, tab]);
  return (
    <section class="chat" data-ui aria-label="Trò chuyện">
      <div class="tabs" role="tablist">{TABS.map(([k, l]) => <button class="tab" role="tab" aria-selected={tab === k} onClick={() => setTab(k)}>{l}</button>)}</div>
      <div class="log" ref={ref} role="log" aria-live="polite" tabIndex={0}>
        {list.length ? list.map((m) => <p class={`ch-${m.channel}`}><span class="t">{new Date(m.at).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}</span>{m.text}</p>) : <p class="empty">{EMPTY[tab] ?? 'Chưa có tin nhắn.'}</p>}
      </div>
      <div class="dtl">WASD / mũi tên: di chuyển · E: tương tác · Esc: menu</div>
    </section>
  );
}

// ---------- Thanh trận đấu (battle_actions + icon APK) ----------
const BB: [string, string, string][] = [['auto', 'Tự động', 'icon_auto'], ['attack', 'Đánh', 'icon_attack'], ['Skills', 'Kỹ năng', 'icon_magic'], ['Items', 'Vật phẩm', 'icon_inventory'], ['defend', 'Thủ', 'button_round'], ['flee', 'Chạy', 'icon_run']];
function BattleBar({ game }: { game: Game }) {
  const b = game.character.value?.battle; const sel = game.selectedAction.value?.choice ?? ''; const auto = game.automatic.value;
  if (!b) return null;
  const over = b.phase !== 'active' && b.phase !== 'choose' && !!b.result;
  const busy = game.session.busy.value || game.isAnimating.value;
  const cls = (cmd: string) => (cmd === 'auto' ? (auto ? 'on' : '') : cmd === 'attack' ? (sel === 'attack' ? 'sel' : '') : cmd === 'Skills' ? (sel === 'skill' ? 'sel' : '') : cmd === 'Items' ? (sel === 'item' || sel === 'capture' ? 'sel' : '') : '');
  const hint = auto ? 'Tự động chiến đấu' : sel === 'attack' ? 'Chạm kẻ địch để đánh' : sel === 'capture' ? 'Chạm kẻ địch để thu phục' : sel === 'skill' ? 'Chạm kẻ địch để dùng kỹ năng' : sel === 'item' ? 'Chạm mục tiêu để dùng vật phẩm' : 'Chọn hành động';
  return (
    <div class="battlebar" data-ui role="toolbar" aria-label="Hành động trận đấu">
      <div class="pic oval" />
      {BB.map(([cmd, label, ic], i) => (
        <button class={`bb ${cls(cmd)}`} style={{ left: `calc(var(--t) * ${i * 70 + 14}px)` }} disabled={busy || over} aria-label={label} onClick={() => game.command(cmd)}>
          <i style={{ backgroundImage: `url(./assets/ui/${ic}.png)` }} /><span>{label}</span>
        </button>
      ))}
      <div class="turn otl">Lượt {b.turn}<small>{hint}</small></div>
    </div>
  );
}

// ---------- HUD ----------
function Hud({ game }: { game: Game }) {
  const c = game.character.value; const cat = game.catalog.value; game.tick.value;
  const [hint, setHint] = useState(true);
  useEffect(() => { const t = setTimeout(() => setHint(false), 9000); return () => clearTimeout(t); }, []);
  if (!c || !cat) return null;
  const pet = c.pets.find((p) => p.id === c.active_pet_id);
  const st = game.session.status.value; const battle = !!c.battle;
  const pct = (v: number, m: number) => `${Math.max(0, Math.min(100, (v / Math.max(1, m)) * 100))}%`;
  const needXp = 25 * c.level; // xp_per_level (rules) × cấp
  const t = T.value;
  return (
    <div id="hud">
      <div class="tl">
        <div class="pic frm" />
        <div class="pic hpb"><div class="fill" style={{ width: pct(pet?.hp ?? 0, pet?.max_hp ?? 1) }} /></div>
        <div class="pic mpb"><div class="fill" style={{ width: pct(pet?.mp ?? 0, pet?.max_mp ?? 1) }} /></div>
        <div class="pic xpb"><div class="fill" style={{ width: pct(c.xp, needXp) }} /></div>
        <div class="num otl" style={{ top: `${t * 37}px` }}>{pet ? `${Math.round(pet.hp)}/${Math.round(pet.max_hp)}` : '—'}</div>
        <div class="num otl" style={{ top: `${t * 54}px` }}>{pet ? `${Math.round(pet.mp)}/${Math.round(pet.max_mp)}` : '—'}</div>
        <div class="pic prt" />
        <div class="ico">{pet ? <PetIcon species={pet.species_id} size={Math.round(40 * t)} /> : null}</div>
        <div class="nm otl">Lv.{c.level} · {c.name}</div>
        {!battle && <>
          <button class="sbtn pet" data-ui aria-label="Linh thú" onClick={() => game.open('Companions')}><i /><span class="cap otl">Linh thú</span></button>
          <button class="sbtn quest" data-ui aria-label="Nhiệm vụ" onClick={() => game.open('Quests')}><i /><span class="cap otl">Nhiệm vụ</span></button>
        </>}
      </div>
      <div class="tr">
        <div class="title otl">{cat.maps[c.map_id]?.name ?? c.map_id}</div>
        <div class="meta otl"><b>{c.gold}</b><b>{c.crystals}</b></div>
        <button class="sbtn menu" data-ui aria-label="Menu" aria-expanded={game.shortcuts.value} onClick={() => game.open('Menu')}><i /></button>
      </div>
      {st !== 'online' && <div class="conn" data-ui role="status">{st === 'connecting' ? 'Đang kết nối…' : 'Mất kết nối'}{st === 'offline' && <button onClick={() => void game.reconnect()}>Kết nối lại</button>}</div>}
      {hint && !battle && <div class="hint">Chạm vào người, cổng hoặc linh thú để đi tới · hoặc dùng nút điều hướng</div>}
      {battle && <BattleBar game={game} />}
      <div class="strip" data-ui-wrap>
        <div class="cp l"><Dpad game={game} /></div>
        <Chat game={game} />
        <div class="cp r">
          <button class="obtn ok otl" data-ui aria-label="Chọn" onClick={() => game.command('confirm')}><span class="rt">Chọn</span></button>
          <button class="obtn bk otl" data-ui aria-label="Trở về" onClick={() => game.command('back')}><span class="rt">Trở về</span></button>
        </div>
      </div>
      {game.shortcuts.value && <Shortcuts game={game} />}
      <MenuHost game={game} onQuality={(q) => engineRef.current?.setQuality(q)} />
    </div>
  );
}
const engineRef: { current: { setQuality: (q: 'auto' | 'low' | 'medium' | 'high') => void } | null } = { current: null };

const STAT_ENGINE: { e: Engine | null } = { e: null };
function Stats() {
  const [t, setT] = useState('');
  useEffect(() => { const i = setInterval(() => { const e = STAT_ENGINE.e; if (!e) return; const s = e.stats(); const gm = (window.__game as { game?: Game } | undefined)?.game; const c = gm?.pres.character; setT(`${c ? `${c.map_id} (${c.x},${c.y}) rev ${c.revision}\n` : ''}${s.fps.toFixed(0)} fps · ${s.frameMs.toFixed(1)} ms (p95 ${s.p95Ms.toFixed(1)})\nbản vẽ ${s.draws} · tam giác ${s.triangles} · texture ${s.textures}\nchất lượng ${s.tier} · pr ${s.pixelRatio.toFixed(2)} · ${s.width}×${s.height}${s.heapMB ? `\nheap ${s.heapMB.toFixed(0)} MB` : ''} · long ${s.longTasks}`); }, 500); return () => clearInterval(i); }, []);
  return <div class="stats" aria-hidden="true">{t}</div>;
}

// ---------- Game ----------
export function GameView({ game }: { game: Game }) {
  const host = useRef<HTMLDivElement>(null); const cv = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const engine = new Engine(cv.current!, host.current!); STAT_ENGINE.e = engine;
    const stage = new Stage(engine, host.current!, game.pres);
    stage.onPick = (h) => game.pick(h as never);
    engine.onFrame((dt) => game.update(dt));
    engineRef.current = { setQuality: (q) => { if (q === 'auto') { engine.auto = true; engine.setTier(window.innerWidth < 900 ? 'medium' : 'high'); } else { engine.auto = false; engine.setTier(q); } void engine.reloadMap(); } };
    engine.start();
    if (new URLSearchParams(location.search).has('bench')) { statsOn.value = true; void runBench(game, engine, (t) => game.message(t)); }
    window.__game = { game, engine, stage, state: () => ({ map: game.pres.mapId, x: game.pres.character?.x, y: game.pres.character?.y, battle: !!game.pres.battle, page: game.page.value, banner: stage.banner, animating: game.pres.isAnimating(), revision: game.revisionSig.value, debug: stage.debug(), stats: engine.stats() }) };
    const kd = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.matches?.('input,select,textarea')) return;
      const m: Record<string, Dir> = { ArrowLeft: 'left', a: 'left', A: 'left', ArrowRight: 'right', d: 'right', D: 'right', ArrowUp: 'up', w: 'up', W: 'up', ArrowDown: 'down', s: 'down', S: 'down' };
      const d = m[e.key];
      if (d) { e.preventDefault(); if (!e.repeat) game.startWalk(d); }
      else if (e.key === 'Escape') { e.preventDefault(); game.command('back'); }
      else if (e.key === 'e' || e.key === 'E' || e.key === ' ' || e.key === 'Enter') { if ((e.target as HTMLElement)?.tagName === 'BUTTON') return; e.preventDefault(); game.command('interact'); }
      else if (e.key === 'F3') { e.preventDefault(); statsOn.value = !statsOn.value; }
    };
    const ku = (e: KeyboardEvent) => { const m: Record<string, Dir> = { ArrowLeft: 'left', a: 'left', A: 'left', ArrowRight: 'right', d: 'right', D: 'right', ArrowUp: 'up', w: 'up', W: 'up', ArrowDown: 'down', s: 'down', S: 'down' }; const d = m[e.key]; if (d) game.stopWalk(d); };
    const blur = () => { game.held = ''; game.destination = null; };
    window.addEventListener('keydown', kd); window.addEventListener('keyup', ku); window.addEventListener('blur', blur);
    document.addEventListener('visibilitychange', blur);
    return () => { window.removeEventListener('keydown', kd); window.removeEventListener('keyup', ku); window.removeEventListener('blur', blur); document.removeEventListener('visibilitychange', blur); stage.dispose(); engine.dispose(); STAT_ENGINE.e = null; };
  }, []);
  const [cover, setCover] = useState<'on' | 'done' | 'off'>('on'); const since = useRef(Date.now()); const full = useRef(true);
  useEffect(() => {
    const i = setInterval(() => {
      const w = (window.__game as { stage?: { loadedMap: string } } | undefined)?.stage; const want = game.character.value?.map_id ?? '';
      if (!w) return;
      const loaded = !want || w.loadedMap === want; const age = Date.now() - since.current;
      if (!loaded) { if (cover === 'off') { since.current = Date.now(); setCover('on'); } else if (cover === 'on' && age > 20000) { setCover('done'); setTimeout(() => { full.current = false; setCover('off'); }, 380); } }
      else if (cover === 'on' && age > 900) { setCover('done'); setTimeout(() => { full.current = false; setCover('off'); }, 380); }
    }, 90);
    return () => clearInterval(i);
  }, [cover]);
  return (
    <>
      <div id="stage" ref={host}><canvas ref={cv} /></div>
      {cover !== 'off' && !full.current && <div class={`mapcover ${cover === 'done' ? 'out' : ''}`}><div class="sysmsg" role="status"><b>Thông báo hệ thống</b><span>Đang tải…</span></div></div>}
      <Hud game={game} />
      {statsOn.value && <Stats />}
      {cover !== 'off' && full.current && <div class={`ld-wrap ${cover === 'done' ? 'out' : ''}`}><LoadingScreen done={cover === 'done'} /></div>}
      <div class="rotate show" role="note"><div><b style="font-size:18px">Xoay ngang màn hình</b><p class="msg">Phimond chơi tốt nhất ở chế độ ngang.</p></div></div>
    </>
  );
}

export function App({ game, local }: { game: Game; local?: boolean }) {
  useEffect(() => watchScale(), []);
  const s = game.screen.value;
  if (s === 'login') return <Login game={game} local={local} />;
  if (s === 'loading') return <LoadingScreen />;
  return <GameView game={game} />;
}
