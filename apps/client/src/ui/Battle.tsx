import { useEffect, useRef, useState } from 'preact/hooks';
import type { Battle as BattleT, BattleEvent, Character } from '@phimond/protocol';
import type { GameWorld } from '../game/world.ts';
import { eventText, viName } from '../game/content.ts';
import { session } from '../state/app.ts';
import { PetAnimated } from './PetArt.tsx';
import { battleResultOpen } from '../state/ui.ts';
import { damageGlyphs, iconFor, uiUrl } from './skin.ts';

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
  const [floats, setFloats] = useState<{ id: number; unit: string; text: string; heal: boolean }[]>([]);
  const [menu, setMenu] = useState<'skill' | 'item' | null>(null);
  const [sending, setSending] = useState(false);
  const [playing, setPlaying] = useState(false);
  const last = useRef<BattleT | null>(null);
  const logRef = useRef<HTMLDivElement>(null);

  const live = ch.battle;
  if (live) last.current = live;
  const view = live ?? finished?.battle ?? null;

  useEffect(
    () =>
      session.onBatch((b) => {
        const battle = b.character.battle ?? (b.presentation?.completed_battle as BattleT | undefined) ?? null;
        if (!battle || b.events.length === 0) return;
        const unitName = (id?: string) => viName(battle.units.find((u) => u.id === id)?.name ?? '');
        const evs = b.events as BattleEvent[];
        setPlaying(true);
        evs.forEach((e, i) =>
          setTimeout(() => {
            setLines((l) => [...l.slice(-40), eventText(e, unitName)]);
            if ((e.type === 'damage' || e.type === 'heal') && e.target_id) {
              setHit(e.type === 'damage' ? e.target_id : null);
              const id = Math.random();
              setFloats((f) => [...f, { id, unit: e.target_id!, text: `${e.type === 'heal' ? '+' : '-'}${e.amount ?? 0}`, heal: e.type === 'heal' }]);
              setTimeout(() => setFloats((f) => f.filter((x) => x.id !== id)), 900);
            }
            if (i === evs.length - 1) {
              setPlaying(false);
              setTimeout(() => setHit(null), 250);
              if (!b.character.battle && b.presentation?.completed_battle) {
                setFinished({ battle: b.presentation.completed_battle as BattleT, lines: evs.filter((x) => /currency|pet_capture|respawn|item_gain/.test(x.type)).map((x) => eventText(x, unitName)) });
              }
            }
          }, i * 320),
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
    if (live && lines.length === 0) setLines([`Một linh thú hoang xuất hiện!`]);
    if (!live && !finished) setLines([]);
  }, [live?.id]);

  if (!view) return null;
  const me = view.units.find((u) => u.side === 'player');
  const foe = view.units.find((u) => u.side === 'enemy');
  const pet = ch.pets.find((p) => p.id === me?.id);
  const busy = sending || playing || !live;

  const act = async (choice: Choice, extra: { skill_id?: string; item_id?: string } = {}) => {
    if (!live) return;
    setMenu(null);
    setSending(true);
    await session.send('battle.action', { battle_id: live.id, turn: live.turn, choice, ...extra }).then((r) => {
      if (!r.ok) setLines((l) => [...l, r.message]);
    });
    setSending(false);
  };

  const unitCard = (u: typeof me, side: 'player' | 'enemy') =>
    u && (
      <div class={`unit ${side} ${hit === u.id ? 'hit' : ''}`} data-testid={`battle-${side}`}>
        <div class="card panel">
          <b>{viName(u.name)}</b>
          <div class="bars">
            <div class="uibar hp" title={`HP ${u.hp}/${u.max_hp}`}>
              <i style={{ width: `${(100 * u.hp) / Math.max(1, u.max_hp)}%` }} />
            </div>
            <div class="uibar mp" title={`MP ${u.mp}/${u.max_mp}`}>
              <i style={{ width: `${(100 * u.mp) / Math.max(1, u.max_mp)}%` }} />
            </div>
          </div>
          <div class="muted" style={{ fontSize: 12 }}>
            HP {u.hp}/{u.max_hp}
            {u.statuses.length > 0 && ` · ${u.statuses.map((s) => world.content.cat.statuses[s.id]?.name ?? s.id).join(', ')}`}
          </div>
        </div>
        <div style={{ position: 'relative' }}>
          <PetAnimated species={u.species_id} size={180} row={u.hp <= 0 ? 'down' : 'idle'} />
          {floats
            .filter((f) => f.unit === u.id)
            .map((f) => (
              <span key={f.id} class={`float dmg ${f.heal ? 'heal' : 'hurt'}`} style={{ left: '35%', top: '20%' }}>
                {damageGlyphs(f.text).map((src, i) => (
                  <img key={i} src={src} alt={i === 0 ? f.text : ''} />
                ))}
              </span>
            ))}
        </div>
      </div>
    );

  const cmd = (id: string, label: string, icon: string, disabled: boolean, onClick: () => void) => (
    <button class="bbtn" disabled={disabled} data-testid={`act-${id}`} aria-label={label} onClick={onClick}>
      {iconFor(icon) ? <img src={iconFor(icon)!} alt="" /> : label}
      <span>{label}</span>
    </button>
  );
  const seals = ch.inventory['capture_seal'] ?? 0;
  const skills = (pet?.skills ?? []).filter((s) => s !== 'attack');
  const consumables = Object.entries(ch.inventory).filter(([id, n]) => n > 0 && /potion|ether/.test(id));

  return (
    <div class="battle" data-testid="battle">
      <div class="field">
        {unitCard(me, 'player')}
        {unitCard(foe, 'enemy')}
        {finished && !live && (
          <div class="result">
            <div class="dialog skin-confirm" style={{ width: 'min(460px, 92vw)', textAlign: 'center' }} data-testid="battle-result">
              {BANNER[finished.battle.result] ? (
                <div class="banner" style={{ backgroundImage: `url(${uiUrl(BANNER[finished.battle.result]!)})`, backgroundSize: '100% 100%', margin: '0 auto 8px' }}>
                  <b style={{ fontSize: 20, color: '#3a2508', marginTop: '6%' }}>{RESULT[finished.battle.result]}</b>
                </div>
              ) : (
                <h2>{RESULT[finished.battle.result] ?? 'Trận đấu kết thúc'}</h2>
              )}
              <div class="list">
                {finished.lines.map((l, i) => (
                  <div key={i}>{l}</div>
                ))}
              </div>
              <button class="btn primary" style={{ marginTop: 10 }} data-testid="battle-continue" onClick={() => (setFinished(null), setLines([]))}>
                Tiếp tục
              </button>
            </div>
          </div>
        )}
      </div>
      <div class="bottom">
        <div class="log skin-dialogue" ref={logRef} data-testid="battle-log">
          {lines.map((l, i) => (
            <div key={i}>{l}</div>
          ))}
        </div>
        {live && (
          <div class={`cmds ${menu ? 'sub' : ''}`}>
            {menu === null && (
              <>
                {cmd('attack', 'Tấn công', 'icon_attack', busy, () => void act('attack'))}
                {cmd('skill', 'Kỹ năng', 'icon_magic', busy || skills.length === 0, () => setMenu('skill'))}
                {cmd('capture', `Bắt (${seals})`, 'capture_seal', busy || seals === 0, () => void act('capture'))}
                {cmd('defend', 'Phòng thủ', 'icon_defend', busy, () => void act('defend'))}
                {cmd('item', 'Vật phẩm', 'icon_inventory', busy || consumables.length === 0, () => setMenu('item'))}
                {cmd('auto', 'Tự động', 'icon_auto', busy, () => void act('auto'))}
                {cmd('flee', 'Chạy', 'icon_run', busy, () => void act('flee'))}
              </>
            )}
            {menu === 'skill' &&
              skills.map((id) => {
                const s = world.content.cat.skills[id] as unknown as { name: string; mp_cost?: number };
                return (
                  <button key={id} class="btn" disabled={busy || (me?.mp ?? 0) < (s?.mp_cost ?? 0)} onClick={() => void act('skill', { skill_id: id })}>
                    {s?.name ?? id} · {s?.mp_cost ?? 0} MP
                  </button>
                );
              })}
            {menu === 'item' &&
              consumables.map(([id, n]) => (
                <button key={id} class="btn" disabled={busy} onClick={() => void act('item', { item_id: id })}>
                  {world.content.itemName(id)} ×{n}
                </button>
              ))}
            {menu !== null && (
              <button class="btn" onClick={() => setMenu(null)}>
                Trở về
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
