import { useEffect, useRef, useState } from 'preact/hooks';
import type { Battle as BattleT, BattleEvent, Character } from '@phimond/protocol';
import type { GameWorld } from '../game/world.ts';
import { eventText, viName } from '../game/content.ts';
import { session } from '../state/app.ts';
import { PetAnimated, PetPortrait } from './PetArt.tsx';
import { petArt, petAtlas } from '../render/assets.ts';
import { FrameBar } from './Hud.tsx';
import { battleResultOpen, pushLog } from '../state/ui.ts';
import { damageGlyphs, iconFor, uiUrl } from './skin.ts';
import { sfx } from './sound.ts';

/** Tên hiển thị của đơn vị; quái cùng tên (encounter 2–3 quái giống nhau) có hậu tố A/B/C theo thứ tự đội hình. */
function labelOf(units: BattleT['units'], id?: string): string {
  const u = units.find((x) => x.id === id);
  if (!u) return '';
  const base = viName(u.name);
  const same = units.filter((x) => x.side === u.side && viName(x.name) === base);
  return same.length > 1 ? `${base} ${String.fromCharCode(65 + same.indexOf(u))}` : base;
}

type Choice = 'attack' | 'skill' | 'capture' | 'defend' | 'item' | 'auto' | 'flee';
const BANNER: Record<string, string> = { win: 'battle_win_banner', loss: 'battle_loss_banner', capture: 'battle_capture_banner' };
const RESULT: Record<string, string> = { win: 'Chiến thắng!', loss: 'Thất bại', capture: 'Bắt thành công!', flee: 'Đã chạy thoát', draw: 'Hòa' };

/**
 * Màn trận đấu: hiển thị theo trạng thái server (client không tính toán kết quả). Sự kiện mỗi lượt được phát lần lượt;
 * khi trận xong, giữ bản kết thúc (presentation.completed_battle) để xem kết quả rồi quay lại world.
 */
export function Battle({ world, ch }: { world: GameWorld; ch: Character }) {
  const [finished, setFinished] = useState<{ battle: BattleT; lines: string[] } | null>(null);
  const [lines, setLines] = useState<string[]>([]);
  const [hit, setHit] = useState<string | null>(null);
  const [acting, setActing] = useState<string | null>(null);
  const [floats, setFloats] = useState<{ id: number; unit: string; text: string; heal: boolean }[]>([]);
  const [menu, setMenu] = useState<'skill' | 'item' | null>(null);
  // Chế độ chọn mục tiêu (khi còn ≥2 quái sống): hành động chờ xác nhận bằng cách chạm vào quái.
  const [pending, setPending] = useState<{ choice: Choice; extra: { skill_id?: string } } | null>(null);
  const [aim, setAim] = useState<string | null>(null);
  // Tự động (PvE): bật thì mỗi lượt tự gửi 'auto' tới khi tắt hoặc hết trận; chạm lại để dừng và về lệnh tay.
  const [autoOn, setAutoOn] = useState(false);
  // Tốc độ ×2 (nhớ theo trình duyệt): phát sự kiện và tự động nhanh gấp đôi.
  const [fast, setFast] = useState(() => {
    try {
      return localStorage.getItem('phimond.battle.fast') === '1';
    } catch {
      return false;
    }
  });
  const fastRef = useRef(fast);
  fastRef.current = fast;
  const actRef = useRef<(c: Choice) => Promise<void>>(async () => undefined);
  // Hiệu ứng đòn đánh trên mục tiêu (vệt chém / quả cầu phép), theo loại kỹ năng vừa dùng.
  const [fx, setFx] = useState<{ id: number; unit: string; kind: string }[]>([]);
  const lastKind = useRef('physical');
  const [sending, setSending] = useState(false);
  const [playing, setPlaying] = useState(false);
  const last = useRef<BattleT | null>(null);
  const logRef = useRef<HTMLDivElement>(null);
  const closeTimer = useRef(0);
  const startLv = useRef<{ pet: number; me: number; id: string } | null>(null);
  const chRef = useRef(ch);
  chRef.current = ch;
  const [more, setMore] = useState(false);
  const [shake, setShake] = useState(false);
  const close = () => {
    window.clearTimeout(closeTimer.current);
    setFinished(null);
    setLines([]);
  };

  const live = ch.battle;
  if (live) last.current = live;
  const view = live ?? finished?.battle ?? null;

  useEffect(
    () =>
      session.onBatch((b) => {
        const battle = b.character.battle ?? (b.presentation?.completed_battle as BattleT | undefined) ?? null;
        if (!battle || b.events.length === 0) return;
        const unitName = (id?: string) => labelOf(battle.units, id);
        const evs = b.events as BattleEvent[];
        setPlaying(true);
        evs.forEach((e, i) =>
          setTimeout(() => {
            setLines((l) => {
              const t = e.type === 'damage' && e.actor_id && e.actor_id !== e.target_id ? `${unitName(e.actor_id)} → ${unitName(e.target_id)}: −${e.amount ?? 0} HP` : eventText(e, unitName);
              return l[l.length - 1] === t ? l : [...l.slice(-40), t];
            });
            if (e.type === 'skill_cast') {
              const sk = Object.values(world.content.cat.skills).find((x) => e.message?.endsWith(' used ' + (x as { name: string }).name)) as { kind?: string } | undefined;
              lastKind.current = sk?.kind ?? 'physical';
            }
            if (e.type === 'damage' && e.target_id) {
              const fid = Math.random();
              const kind = lastKind.current === 'magic' ? 'magic' : 'slash';
              setFx((f) => [...f, { id: fid, unit: e.target_id!, kind }]);
              setTimeout(() => setFx((f) => f.filter((x) => x.id !== fid)), 520);
              sfx(kind === 'magic' ? 'magic' : 'hit');
            }
            if (e.type === 'miss') sfx('miss');
            if (e.type === 'skill_cast' || e.type === 'miss' || (e.type === 'damage' && e.actor_id)) {
              setActing(e.actor_id || null);
              setTimeout(() => setActing(null), 420);
            }
            if ((e.type === 'damage' || e.type === 'heal') && e.target_id) {
              setHit(e.type === 'damage' ? e.target_id : null);
              if (e.type === 'damage') {
                setShake(true);
                setTimeout(() => setShake(false), 220);
              }
              const id = Math.random();
              setFloats((f) => [...f, { id, unit: e.target_id!, text: `${e.type === 'heal' ? '+' : '-'}${e.amount ?? 0}`, heal: e.type === 'heal' }]);
              setTimeout(() => setFloats((f) => f.filter((x) => x.id !== id)), 900);
            }
            if (i === evs.length - 1) {
              setPlaying(false);
              setTimeout(() => setHit(null), 250);
              if (!b.character.battle && b.presentation?.completed_battle) {
                const done = b.presentation.completed_battle as BattleT;
                const rewards = evs.filter((x) => /currency|pet_capture|respawn|item_gain|level_up|pet_learn/.test(x.type)).map((x) => eventText(x, unitName));
                // Kết quả, vàng, EXP, vật phẩm do world ghi vào khung chat (không popup chặn); cảnh trận tự đóng sau một nhịp.
                // Server không gửi sự kiện lên cấp: so cấp trước/sau trận để báo (cả khung thưởng lẫn chat).
                const s0 = startLv.current;
                const after = b.character;
                const petAfter = after.pets.find((p) => p.id === after.active_pet_id);
                if (s0 && petAfter && petAfter.level > s0.pet) {
                  const t = `${viName(petAfter.name)} lên cấp ${petAfter.level}!`;
                  rewards.push(t);
                  pushLog(t, 'system');
                  setTimeout(() => sfx('level'), 500);
                }
                if (s0 && after.level > s0.me) {
                  const t = `Bạn lên cấp ${after.level}!`;
                  rewards.push(t);
                  pushLog(t, 'system');
                }
                startLv.current = null;
                // Thua: giữ bảng tới khi chạm, kèm gợi ý; thắng/bắt/lên cấp: tự đóng sau một nhịp.
                if (done.result === 'loss') rewards.push('Gợi ý: hồi phục ở Kiểm Lâm Lio (Bìa Rừng) hoặc Y Sư Selka (Quảng Trường), dùng Thuốc Rễ Dại trong trận, hoặc luyện cấp ở Bìa Rừng trước khi vào Rừng Sâu.');
                setFinished({ battle: done, lines: rewards });
                sfx(done.result === 'loss' ? 'lose' : done.result === 'flee' ? 'flee' : 'win');
                const long = rewards.some((l) => /lên cấp|Lv|Bắt được|Học được/.test(l)) || done.result === 'capture';
                if (done.result !== 'loss') closeTimer.current = window.setTimeout(close, long ? 3600 : done.result === 'win' ? 2400 : 1400);
              }
            }
          }, i * (fastRef.current ? 150 : 300)),
        );
      }),
    [],
  );
  useEffect(() => {
    battleResultOpen.value = finished !== null;
  }, [finished]);
  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [lines]);
  useEffect(() => {
    if (live && !startLv.current) startLv.current = { pet: chRef.current.pets.find((p) => p.id === chRef.current.active_pet_id)?.level ?? 0, me: chRef.current.level, id: live.id };
    if (live && lines.length === 0) {
      const n = live.units.filter((u) => u.side === 'enemy').length;
      setLines([n > 1 ? `${n} linh thú hoang xuất hiện!` : `Một linh thú hoang xuất hiện!`]);
    }
    setPending(null);
    setAim(null);
    setAutoOn(false);
    if (!live && !finished) setLines([]);
  }, [live?.id]);

  // Tự động: đợi lượt rảnh rồi gửi 'auto' (đặt trước mọi return để giữ thứ tự hook).
  const idle = !!live && !sending && !playing && !pending;
  useEffect(() => {
    if (!autoOn || !idle) return;
    const t = window.setTimeout(() => void actRef.current('auto'), fast ? 250 : 600);
    return () => window.clearTimeout(t);
  }, [autoOn, idle, live?.turn, fast]);

  if (!view) return null;
  const me = view.units.find((u) => u.side === 'player');
  const foes = view.units.filter((u) => u.side === 'enemy');
  const allies = view.units.filter((u) => u.side === 'player');
  const aliveFoes = foes.filter((u) => u.hp > 0);
  const foe = foes[0];
  const pet = ch.pets.find((p) => p.id === me?.id);
  const busy = sending || playing || !live;

  const act = async (choice: Choice, extra: { skill_id?: string; item_id?: string; target_id?: string } = {}) => {
    if (!live) return;
    setMenu(null);
    setPending(null);
    setSending(true);
    await session.send('battle.action', { battle_id: live.id, turn: live.turn, choice, ...extra }).then((r) => {
      if (!r.ok) setLines((l) => [...l, r.message]);
    });
    setSending(false);
  };

  actRef.current = act;
  // Hành động nhắm 1 mục tiêu: một quái sống → gửi thẳng; nhiều quái → vào chế độ chọn (mặc định mục tiêu lần trước).
  const aimed = aim && aliveFoes.some((u) => u.id === aim) ? aim : aliveFoes[0]?.id;
  const begin = (choice: Choice, extra: { skill_id?: string } = {}) => {
    if (aliveFoes.length <= 1) return void act(choice, { ...extra, target_id: aliveFoes[0]?.id });
    setMenu(null);
    setMore(false);
    setPending({ choice, extra });
  };
  const pick = (id: string) => {
    if (!pending) return;
    setAim(id);
    void act(pending.choice, { ...pending.extra, target_id: id });
  };
  const bgKey = ch.map_id.includes('deep') ? 'deep_forest' : ch.map_id.includes('gate') ? 'gate' : ch.map_id.startsWith('city') ? 'city' : ch.map_id.includes('hall') ? 'hall' : 'forest';
  const lvOf = (u: typeof foe) => (u as unknown as { level?: number } | undefined)?.level;
  const seals = ch.inventory['capture_seal'] ?? 0;
  const skills = (pet?.skills ?? []).filter((s) => s !== 'attack');
  const consumables = Object.entries(ch.inventory).filter(([id, n]) => n > 0 && /potion|ether/.test(id));

  const enemyPlate = (u: typeof foe) =>
    u && (
      <div class="foe-plate" data-testid="battle-enemy">
        <div class="nm">
          <b>{labelOf(view.units, u.id)}</b>
          {lvOf(u) ? <em>Lv {lvOf(u)}</em> : null}
        </div>
        <div class="fb">
          <em class="hp">HP</em>
          <div class="fbar hp r0" title={`HP ${u.hp}/${u.max_hp}`}>
            <div class="track">
              <i class="fill" style={{ clipPath: `inset(0 ${100 - (100 * u.hp) / Math.max(1, u.max_hp)}% 0 0)` }} />
            </div>
            <span>
              {u.hp}/{u.max_hp}
            </span>
          </div>
        </div>
        {u.statuses.length > 0 && <div class="st">{u.statuses.map((s) => world.content.cat.statuses[s.id]?.name ?? s.id).join(' · ')}</div>}
      </div>
    );

  const myPlate = (u: typeof me, idx: number) => {
    if (!u) return null;
    const pet = ch.pets.find((p) => p.id === u.id);
    return (
      <div class={`my-plate hud-card ${allies.length > 1 ? 'compact' : ''}`} data-testid="battle-player" key={u.id} style={{ top: `calc(${8 + idx * (allies.length > 1 ? 70 : 82)}px + var(--safe-t))` }}>
        <div class="ring">
          <PetPortrait species={u.species_id} size={46} />
          {pet && <div class="badge">{pet.level}</div>}
        </div>
        <div class="stack">
          <div class="nm">
            <b>{labelOf(view.units, u.id)}</b>
            {u.statuses.length > 0 && <span class="st">{u.statuses.map((s) => world.content.cat.statuses[s.id]?.name ?? s.id).join(' · ')}</span>}
          </div>
          <FrameBar kind="hp" row={0} v={u.hp} max={u.max_hp} label="HP" />
          <FrameBar kind="mp" row={1} v={u.mp} max={u.max_mp} label="MP" />
          {pet && allies.length === 1 && <FrameBar kind="xp" row={2} v={pet.xp} max={pet.level * 25} label="EXP" />}
        </div>
      </div>
    );
  };

  // Đội hình trên mặt đất phối cảnh (kiểu Octopath): mỗi đơn vị đặt theo điểm chân (x%, y%) trong cảnh;
  // càng thấp càng gần camera nên to hơn và đè lên con phía sau. Quái bên trái, phe mình bên phải.
  const portrait = window.innerWidth < 700;
  const slotOf = (side: 'player' | 'enemy', i: number, n: number): { x: number; y: number } => {
    if (portrait) {
      if (side === 'enemy') return n === 1 ? { x: 50, y: 50 } : n === 2 ? [{ x: 30, y: 44 }, { x: 70, y: 52 }][i]! : [{ x: 22, y: 44 }, { x: 50, y: 53 }, { x: 78, y: 44 }][i]!;
      return n === 1 ? { x: 50, y: 80 } : [{ x: 25, y: 78 }, { x: 50, y: 84 }, { x: 75, y: 78 }][i]!;
    }
    // Đội hình chữ V đối xứng hai phe ("> <"): A và C cùng cột phía ngoài, B ở giữa nhô vào trong về phía đối thủ.
    // Phe mình lật gương (x → 100 − x). 1 đơn vị đứng ở tâm, 2 đơn vị là A và C.
    const V = n === 1 ? [{ x: 26, y: 67 }] : n === 2 ? [{ x: 17, y: 54 }, { x: 17, y: 80 }] : [{ x: 15, y: 51 }, { x: 29, y: 67 }, { x: 15, y: 83 }];
    const slot = V[i] ?? { x: 26, y: 67 };
    return side === 'enemy' ? slot : { x: 100 - slot.x, y: slot.y };
  };
  const sceneH = Math.max(240, window.innerHeight - (portrait ? 170 : window.innerHeight < 500 ? 70 : 110));
  const fighter = (u: typeof me, side: 'player' | 'enemy', i: number, n: number) => {
    if (!u) return null;
    const row = u.hp <= 0 ? 'down' : acting === u.id ? 'attack' : 'idle';
    const targetable = side === 'enemy' && pending !== null && u.hp > 0;
    const at = slotOf(side, i, n);
    const art = petArt(u.species_id) as (ReturnType<typeof petArt> & { footPad?: number; bodyH?: number; bodyW?: number }) | null;
    const cell = petAtlas()?.cell ?? 281;
    // Kích thước theo chiều cao cảnh × độ sâu (gần to, xa nhỏ); đông quân thì nhỏ bớt để không chen nhau.
    const depth = portrait ? Math.min(1.05, 0.85 + (at.y - 44) / 90) : 0.84 + (at.y - 51) / 100;
    const crowd = portrait ? (n === 1 ? 1 : n === 2 ? 0.86 : 0.76) : n === 1 ? 1 : n === 2 ? 0.8 : 0.7;
    const size = Math.round(sceneH * (portrait ? 0.36 : 0.44) * depth * crowd);
    const k = size / cell;
    const foot = (art?.footPad ?? cell * 0.2) * k; // khoảng trống trong khung dưới chân
    const bodyH = (art?.bodyH ?? cell * 0.6) * k;
    const bodyW = (art?.bodyW ?? cell * 0.55) * k;
    return (
      <div
        key={u.id}
        class={`fighter ${side} ${hit === u.id ? 'hit' : ''} ${row} ${targetable ? 'targetable' : ''} ${targetable && aimed === u.id ? 'aimed' : ''}`}
        data-testid={targetable ? 'foe-target' : undefined}
        data-unit={u.id}
        style={{ left: `${at.x}%`, top: `${at.y}%`, zIndex: Math.round(at.y), ['--bw' as string]: `${bodyW}px` }}
        onClick={targetable ? () => pick(u.id) : undefined}
        onMouseEnter={targetable ? () => setAim(u.id) : undefined}
      >
        {targetable && <div class="tmark" aria-hidden="true" />}
        <div class="shadow" style={{ width: bodyW * 0.95, height: Math.max(10, bodyW * 0.22) }} />
        <div class="sprite-wrap" style={{ marginBottom: -foot }}>
          <PetAnimated species={u.species_id} size={size} row={row} />
          {fx
            .filter((f) => f.unit === u.id)
            .map((f) => (
              <span key={f.id} class={`fx ${f.kind}`} style={{ bottom: foot + bodyH * 0.25, width: bodyW * 1.1, height: bodyH * 0.8 }} aria-hidden="true" />
            ))}
          {floats
            .filter((f) => f.unit === u.id)
            .map((f) => (
              <span key={f.id} class={`float dmg ${f.heal ? 'heal' : 'hurt'}`} style={{ bottom: foot + bodyH * 0.8 }}>
                {damageGlyphs(f.text).map((src, j) => (
                  <img key={j} src={src} alt={j === 0 ? f.text : ''} />
                ))}
              </span>
            ))}
        </div>
        {side === 'enemy' &&
          (portrait ? (
            <div class="plate-anchor" style={{ bottom: bodyH + 10 }}>
              {enemyPlate(u)}
            </div>
          ) : (
            // Màn ngang: khung tên đặt cạnh thân, phía trong (hướng đối thủ), để A/C cùng cột không che nhau.
            <div class="plate-anchor side" style={{ left: `calc(50% + ${Math.round(bodyW * 0.42)}px)`, bottom: Math.round(bodyH * 0.38) }}>
              {enemyPlate(u)}
            </div>
          ))}
      </div>
    );
  };

  const round = (id: string, label: string, icon: string, disabled: boolean, why: string, onClick: () => void) => (
    <button class="bbtn" disabled={disabled} data-testid={`act-${id}`} aria-label={label} title={disabled ? why : label} onClick={onClick}>
      {iconFor(icon) ? <img src={iconFor(icon)!} alt="" /> : label}
      <span>{disabled && why ? why : label}</span>
    </button>
  );
  const sub = menu !== null || more;

  return (
    <div class={`battle ${shake ? 'shake' : ''}`} data-testid="battle">
      <div class="scene">
        <img class="bg" src={`${import.meta.env.BASE_URL}battle/battle-bg-${bgKey}.png`} alt="" onError={(e) => ((e.currentTarget as HTMLImageElement).style.display = 'none')} />
        <div class="vignette" />
        <div class="ground" />
        <div class="motes" aria-hidden="true" />
        {live && (
          <button
            class={`speed ${fast ? 'on' : ''}`}
            data-testid="battle-speed"
            aria-pressed={fast}
            onClick={() => {
              setFast(!fast);
              try {
                localStorage.setItem('phimond.battle.fast', fast ? '0' : '1');
              } catch {
                /* trình duyệt chặn lưu: chỉ đổi trong phiên */
              }
            }}
          >
            {fast ? '×2' : '×1'}
          </button>
        )}
        <div class="turn" style={{ backgroundImage: `url(${uiUrl('battle_turn_banner')})` }}>
          <b>{finished ? 'Kết thúc' : `Lượt ${view.turn}`}</b>
        </div>
        {allies.map((u, i) => myPlate(u, i))}
        <div class={`stage ${foes.length > 1 ? 'multi' : ''}`}>
          {foes.map((u, i) => fighter(u, 'enemy', i, foes.length))}
          {allies.map((u, i) => fighter(u, 'player', i, allies.length))}
        </div>
        {finished && !live && (
          <div class="result" onClick={close}>
            <div class="rwd" data-testid="battle-result">
              {BANNER[finished.battle.result] ? (
                <div class="banner" style={{ backgroundImage: `url(${uiUrl(BANNER[finished.battle.result]!)})`, backgroundSize: '100% 100%' }}>
                  <b>{RESULT[finished.battle.result]}</b>
                </div>
              ) : (
                <div class="banner plain">
                  <b>{RESULT[finished.battle.result] ?? 'Trận đấu kết thúc'}</b>
                </div>
              )}
              {finished.lines.length > 0 && (
                <div class="lines">
                  {finished.lines.map((l, i) => (
                    <div key={i}>{l}</div>
                  ))}
                </div>
              )}
              <small>Chạm để tiếp tục</small>
            </div>
          </div>
        )}
        {live && pending && (
          <div class="cmdwrap">
            <div class="aimbar" data-testid="aim-bar">
              <span>Chọn mục tiêu</span>
              <button class="btn" data-testid="aim-cancel" onClick={() => setPending(null)}>
                Hủy
              </button>
            </div>
          </div>
        )}
        {live && !pending && (
          <div class="cmdwrap">
            {sub && (
              <div class="cmdsub">
                {menu === 'skill' &&
                  skills.map((id) => {
                    const sk = world.content.cat.skills[id] as unknown as { name: string; mp_cost?: number; target?: string };
                    return (
                      <button key={id} class="btn" disabled={busy || (me?.mp ?? 0) < (sk?.mp_cost ?? 0)} onClick={() => (sk?.target === 'self' ? void act('skill', { skill_id: id }) : begin('skill', { skill_id: id }))}>
                        {sk?.name ?? id} · {sk?.mp_cost ?? 0} MP
                      </button>
                    );
                  })}
                {menu === 'item' &&
                  consumables.map(([id, n]) => (
                    <button key={id} class="btn" disabled={busy} onClick={() => void act('item', { item_id: id })}>
                      {world.content.itemName(id)} ×{n}
                    </button>
                  ))}
                {menu === null && more && (
                  <>
                    {round('defend', 'Phòng thủ', 'icon_defend', busy, '', () => (setMore(false), void act('defend')))}
                    {round('item', 'Vật phẩm', 'icon_inventory', busy || consumables.length === 0, 'Trống', () => (setMore(false), setMenu('item')))}
                  </>
                )}
                {menu !== null && (
                  <button class="btn" onClick={() => setMenu(null)}>
                    Trở về
                  </button>
                )}
              </div>
            )}
            <div class="cmds">
              <button class={`bbtn auto ${autoOn ? 'on' : ''}`} data-testid="act-auto" aria-pressed={autoOn} aria-label="Tự động" disabled={!live || (!autoOn && busy)} onClick={() => (setMore(false), setMenu(null), setAutoOn(!autoOn))}>
                {iconFor('icon_auto') ? <img src={iconFor('icon_auto')!} alt="" /> : null}
                <span>{autoOn ? 'Dừng' : 'Tự động'}</span>
              </button>
              {round('attack', 'Tấn công', 'icon_attack', busy, '', () => begin('attack'))}
              {skills.length > 0 && round('skill', 'Kỹ năng', 'icon_magic', busy, '', () => (setMore(false), setMenu('skill')))}
              {round('capture', `Bắt (${seals})`, 'capture_seal', busy || seals === 0, seals === 0 ? 'Hết Phù' : '', () => begin('capture'))}
              {round('flee', 'Chạy', 'icon_run', busy, '', () => void act('flee'))}
              <button class={`bbtn more ${more ? 'on' : ''}`} aria-label="Thêm" data-testid="act-more" onClick={() => (setMenu(null), setMore(!more))}>
                <b>⋯</b>
                <span>Thêm</span>
              </button>
            </div>
          </div>
        )}
      </div>
      <div class="bottom">
        <div class="log" ref={logRef} data-testid="battle-log">
          {lines.slice(-3).map((l, i) => (
            <div key={l + i}>{l}</div>
          ))}
        </div>
      </div>
    </div>
  );
}
