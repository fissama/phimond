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
  void npcTab;
  return (
    <div class="scrim" data-testid="overlay" onPointerDown={(e) => e.target === e.currentTarget && closeOverlay()}>
      <div class={`dialog skin-${skin}`} role="dialog">
        <button class="btn-close" aria-label="Đóng" data-testid="overlay-close" style={{ position: 'absolute', top: 2, right: 2, zIndex: 2 }} onClick={closeOverlay} />
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

function PetRow({ p, children }: { p: Pet; children?: preact.ComponentChildren }) {
  return (
    <div class="item">
      <PetPortrait species={p.species_id} />
      <div class="grow">
        <div>
          <b>{viName(p.name)}</b> · Lv {p.level} · {'★'.repeat(Math.max(1, p.star ?? 1))}
        </div>
        <div class="muted">
          HP {p.hp}/{p.max_hp} · MP {p.mp}/{p.max_mp}
        </div>
      </div>
      {children}
    </div>
  );
}

function Pets({ world, ch }: { world: GameWorld; ch: Character }) {
  const pets = ch.pets.filter((p) => !p.retired);
  const [sel, setSel] = useState<string | null>(null);
  const p = pets.find((x) => x.id === sel);
  if (p) return <PetDetail world={world} ch={ch} p={p} onBack={() => setSel(null)} />;
  return (
    <>
      <h2>Linh thú ({pets.length})</h2>
      {pets.length === 0 && <p class="muted">Bạn chưa có linh thú. Hãy chọn một bệ đá ở Triệu Linh Điện.</p>}
      <div class="list">
        {pets.map((p) => (
          <PetRow key={p.id} p={p}>
            <button class="btn small" data-testid={`pet-detail-${p.id}`} onClick={() => setSel(p.id)}>
              Chi tiết
            </button>
            {p.id === ch.active_pet_id ? (
              <span class="muted">Đang theo</span>
            ) : (
              <button class="btn small" onClick={() => void world.intent('pet.activate', { pet_id: p.id })}>
                Cho đi theo
              </button>
            )}
          </PetRow>
        ))}
      </div>
      <Back />
    </>
  );
}

/** Màn chi tiết linh thú: chỉ số, hệ, tộc, kỹ năng, kháng (khi đã giám định). */
function PetDetail({ world, ch, p, onBack }: { world: GameWorld; ch: Character; p: Pet; onBack: () => void }) {
  const sp = world.content.cat.species[p.species_id] as unknown as { element?: string; race?: string; archetype?: string } | undefined;
  const x = p as unknown as Record<string, number | Record<string, number> | undefined>;
  const stat = (k: string) => (typeof x[k] === 'number' ? Math.round((x[k] as number) * (k === 'critical' ? 100 : 1)) : '—');
  const res = (x.resistances as Record<string, number> | undefined) ?? undefined;
  return (
    <>
      <h2>{viName(p.name)}</h2>
      <div class="pet-detail">
        <div class="pd-art">
          <PetPortrait species={p.species_id} size={112} />
          <div class="pd-tags">
            <span>Lv {p.level}</span>
            <span>{'★'.repeat(Math.max(1, p.star ?? 1))}</span>
            {sp?.element && <span>Hệ {ELEMENT_VI[sp.element] ?? sp.element}</span>}
            {sp?.race && <span>{RACE_VI[sp.race] ?? sp.race}</span>}
            {p.id === ch.active_pet_id && <span class="on">Đang theo</span>}
          </div>
        </div>
        <div class="pd-stats">
          <div><em>HP</em><b>{p.hp}/{p.max_hp}</b></div>
          <div><em>MP</em><b>{p.mp}/{p.max_mp}</b></div>
          <div><em>Tấn công</em><b>{stat('attack')}</b></div>
          <div><em>Phép</em><b>{stat('magic')}</b></div>
          <div><em>Phòng thủ</em><b>{stat('defense')}</b></div>
          <div><em>Tốc độ</em><b>{stat('speed')}</b></div>
          <div><em>Chí mạng</em><b>{stat('critical')}%</b></div>
          <div><em>EXP</em><b>{p.xp ?? 0}/{p.level * 25}</b></div>
        </div>
      </div>
      <h3 class="pd-h">Kỹ năng</h3>
      <div class="pd-skills">
        {p.skills.map((id) => {
          const sk = world.content.cat.skills[id] as unknown as { name: string; mp_cost?: number; power?: number; kind?: string; element?: string } | undefined;
          return (
            <div key={id} class="pd-skill">
              <b>{sk?.name ?? id}</b>
              <span class="muted">
                {sk?.kind === 'magic' ? 'Phép' : sk?.kind === 'physical' ? 'Vật lý' : sk?.kind === 'heal' ? 'Hồi máu' : 'Hiệu ứng'}
                {sk?.element ? ` · ${ELEMENT_VI[sk.element] ?? sk.element}` : ''}
                {sk?.power ? ` · Uy lực ${sk.power}` : ''} · {sk?.mp_cost ?? 0} MP
              </span>
            </div>
          );
        })}
      </div>
      {res && (
        <>
          <h3 class="pd-h">Kháng hệ</h3>
          <div class="pd-res">
            {Object.entries(res).map(([k, v]) => (
              <span key={k}>
                {ELEMENT_VI[k] ?? k} {v}%
              </span>
            ))}
          </div>
        </>
      )}
      {!p.appraised && <p class="muted">Chưa giám định: tiềm năng và kháng còn ẩn.</p>}
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
        {row('Đồ họa', 'quality', (['low', 'medium', 'high'] as Quality[]).map((q) => [q, PRESETS[q].label, s.quality === q, () => updateSettings({ quality: q }), `quality-${q}`]))}
        <p class="muted set-note">{s.quality === 'low' ? 'Nhẹ nhất: tắt bóng, hậu kỳ và hiệu ứng phụ.' : s.quality === 'medium' ? 'Chỉnh màu theo giờ, làm mờ HD-2D, đèn và tia nắng.' : 'Thêm bloom và bóng đổ thật; tốn pin hơn.'}</p>
        {row('Khung hình', undefined, ([30, 60] as const).map((f) => [String(f), `${f} FPS`, s.fps === f, () => updateSettings({ fps: f }), `fps-${f}`]))}
        {row('Âm thanh', 'sound', ([[0, 'Tắt'], [0.3, 'Nhỏ'], [0.6, 'Vừa'], [1, 'To']] as const).map(([v, t]) => [String(v), t, s.sound === v, () => updateSettings({ sound: v }), `sound-${v}`]))}
        {row('Thời gian', 'time-mode', ([['auto', 'Theo máy'], ['day', 'Ngày'], ['dusk', 'Hoàng hôn'], ['night', 'Đêm']] as const).map(([k, t]) => [k, t, s.time === k, () => updateSettings({ time: k }), `time-${k}`]))}
        {row('Phím điều hướng', undefined, [['on', 'Hiện', s.dpad, () => updateSettings({ dpad: true })], ['off', 'Ẩn', !s.dpad, () => updateSettings({ dpad: false })]])}
        {row('Giao diện', 'hud-density', [['full', 'Đầy đủ', s.hud === 'full', () => updateSettings({ hud: 'full' }), 'hud-full'], ['compact', 'Gọn', s.hud === 'compact', () => updateSettings({ hud: 'compact' }), 'hud-compact']])}
        {settingsVolatile.value && <p class="muted">Trình duyệt không cho lưu cài đặt; lựa chọn chỉ giữ tới khi tải lại trang.</p>}
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
      {tab === 'learn' && <Learn world={world} ch={ch} cost={rules.learn_cost ?? 0} />}
      {tab === 'quest' && <QuestDesk world={world} ch={ch} npcId={npcId} />}
      <div class="row">
        <button class="btn" data-testid="npc-close" onClick={closeOverlay}>
          Tạm biệt
        </button>
      </div>
    </>
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

function Learn({ world, ch, cost }: { world: GameWorld; ch: Character; cost: number }) {
  const pet = ch.pets.find((p) => p.id === ch.active_pet_id);
  if (!pet) return <p class="muted">Bạn chưa có linh thú.</p>;
  const sp = world.content.cat.species[pet.species_id] as unknown as { skills?: string[] };
  const skills = (sp?.skills ?? []).filter((s) => !pet.skills.includes(s));
  return (
    <div class="list">
      <div class="muted">
        Dạy cho {viName(pet.name)} (Lv {pet.level}) · {cost} vàng mỗi kỹ năng
      </div>
      {skills.length === 0 && <p class="muted">Linh thú đã học hết kỹ năng của loài.</p>}
      {skills.map((id) => {
        const s = world.content.cat.skills[id] as unknown as { name: string; learn_level?: number; mp_cost?: number };
        const lv = s?.learn_level ?? 1;
        return (
          <div class="item" key={id}>
            {iconFor(`skill_${id}`) && <img class="icon" src={iconFor(`skill_${id}`)!} alt="" />}
            <div class="grow">
              {s?.name ?? id}
              <div class="muted">
                Cần Lv {lv} · {s?.mp_cost ?? 0} MP
              </div>
            </div>
            <button class="btn small" disabled={pet.level < lv || ch.gold < cost} onClick={() => void world.intent('pet.learn', { pet_id: pet.id, skill_id: id })}>
              Học
            </button>
          </div>
        );
      })}
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
  const bar = (label: string, v = 0) => (
    <div class="st-bar">
      <em>{label}</em>
      <i style={{ width: `${Math.min(100, v * 8)}%` }} />
    </div>
  );
  const strike = (sp?.skills ?? []).find((id) => id !== 'attack' && /strike$/.test(id));
  return (
    <>
      <h2>Bệ triệu hồi: {st.name}</h2>
      <div class="item starter-card" style={{ marginBottom: 12 }}>
        <PetPortrait species={ped.species} size={88} />
        <div class="grow">
          <div class="pd-tags">
            {sp?.element && <span>Hệ {ELEMENT_VI[sp.element] ?? sp.element}</span>}
            {sp?.race && <span>{RACE_VI[sp.race] ?? sp.race}</span>}
            {strike && <span>Biết sẵn: {world.content.skillName(strike)}</span>}
          </div>
          <p style={{ margin: '6px 0' }}>{st.blurb}</p>
          <div class="st-bars">
            {bar('Sức mạnh', b.strength)}
            {bar('Phép', b.intelligence)}
            {bar('Thể lực', b.stamina)}
            {bar('Tốc độ', b.agility)}
          </div>
          <div class="muted">Linh thú sẽ theo bạn suốt hành trình. Sau khi chọn, bạn được đưa thẳng tới Bìa Rừng Lục Bảo.</div>
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
