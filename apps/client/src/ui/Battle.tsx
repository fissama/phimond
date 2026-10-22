import { useEffect, useRef, useState } from 'preact/hooks';
import type { Battle as BattleT, BattleEvent, Character } from '@phimond/protocol';
import type { GameWorld } from '../game/world.ts';
import { eventText, viName } from '../game/content.ts';
import { session } from '../state/app.ts';
import { PetAnimated, PetPortrait } from './PetArt.tsx';
import { FrameBar } from './Hud.tsx';
import { battleResultOpen, pushLog } from '../state/ui.ts';
import { damageGlyphs, iconFor, uiUrl } from './skin.ts';

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
                }
                if (s0 && after.level > s0.me) {
                  const t = `Bạn lên cấp ${after.level}!`;
                  rewards.push(t);
                  pushLog(t, 'system');
                }
                startLv.current = null;
                setFinished({ battle: done, lines: rewards });
                const long = rewards.some((l) => /lên cấp|Lv|Bắt được|Học được/.test(l)) || done.result === 'capture' || done.result === 'win';
                closeTimer.current = window.setTimeout(close, long ? 4200 : 1700);
              }
            }
          }, i * 300),
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
    if (!live && !finished) setLines([]);
  }, [live?.id]);

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
          <em>{lvOf(u) ? `Lv ${lvOf(u)}` : 'Hoang dã'}</em>
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
      <div class="my-plate hud-card" data-testid="battle-player" key={u.id} style={{ top: `calc(${8 + idx * 82}px + var(--safe-t))` }}>
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
          {pet && <FrameBar kind="xp" row={2} v={pet.xp} max={pet.level * 25} label="EXP" />}
        </div>
      </div>
    );
  };

  const fighter = (u: typeof me, side: 'player' | 'enemy', n = 1) => {
    if (!u) return null;
    const row = u.hp <= 0 ? 'down' : acting === u.id ? 'attack' : 'idle';
    const targetable = side === 'enemy' && pending !== null && u.hp > 0;
    // Đội hình 1–3 quái: sprite nhỏ dần theo số lượng và không vượt nửa bề ngang màn hình.
    const size = Math.max(96, Math.min(260 - (n - 1) * 52, (window.innerWidth * (window.innerWidth < 700 ? 0.86 : 0.46)) / n)) * (window.innerHeight < 500 ? 0.62 : 1);
    return (
      <div
        class={`fighter ${side} ${hit === u.id ? 'hit' : ''} ${row} ${targetable ? 'targetable' : ''} ${targetable && aimed === u.id ? 'aimed' : ''}`}
        data-testid={targetable ? 'foe-target' : undefined}
        data-unit={u.id}
        onClick={targetable ? () => pick(u.id) : undefined}
        onMouseEnter={targetable ? () => setAim(u.id) : undefined}
      >
        {side === 'enemy' && enemyPlate(u)}
        <div class="sprite-wrap">
          {targetable && <div class="tmark" aria-hidden="true" />}
          <div class="shadow" />
          <PetAnimated species={u.species_id} size={size} row={row} />
          {floats
            .filter((f) => f.unit === u.id)
            .map((f) => (
              <span key={f.id} class={`float dmg ${f.heal ? 'heal' : 'hurt'}`}>
                {damageGlyphs(f.text).map((src, i) => (
                  <img key={i} src={src} alt={i === 0 ? f.text : ''} />
                ))}
              </span>
            ))}
        </div>
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
        <div class="turn" style={{ backgroundImage: `url(${uiUrl('battle_turn_banner')})` }}>
          <b>{finished ? 'Kết thúc' : `Lượt ${view.turn}`}</b>
        </div>
        {allies.map((u, i) => myPlate(u, i))}
        <div class="stage">
          <div class={`side left n${foes.length}`}>{foes.map((u) => fighter(u, 'enemy', foes.length))}</div>
          <div class={`side right n${allies.length}`}>{allies.map((u) => fighter(u, 'player', allies.length))}</div>
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
                    {round('auto', 'Tự động', 'icon_auto', busy, '', () => (setMore(false), void act('auto')))}
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
              {round('attack', 'Tấn công', 'icon_attack', busy, '', () => begin('attack'))}
              {round('skill', 'Kỹ năng', 'icon_magic', busy || skills.length === 0, skills.length === 0 ? 'Chưa có' : '', () => (setMore(false), setMenu('skill')))}
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
        <div class="log skin-dialogue" ref={logRef} data-testid="battle-log">
          {lines.slice(-3).map((l, i) => (
            <div key={l + i}>{l}</div>
          ))}
        </div>
      </div>
    </div>
  );
}
