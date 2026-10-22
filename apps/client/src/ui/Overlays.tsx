import { useEffect, useState } from 'preact/hooks';
import type { Character, Pet } from '@phimond/protocol';
import type { GameWorld } from '../game/world.ts';
import { currentMap } from '../game/world.ts';
import { ROLE_LABEL, ROLE_NOT_OPEN, STARTERS, viName } from '../game/content.ts';
import { asset, hd2dUrl } from '../render/assets.ts';
import { PRESETS, settings, settingsVolatile, updateSettings, type Quality } from '../state/settings.ts';
import { closeOverlay, overlay } from '../state/ui.ts';
import { session } from '../state/app.ts';
import { PetPortrait } from './PetArt.tsx';
import { iconFor } from './skin.ts';
import { useSignal } from '@preact/signals';

type Rules = { heal_cost?: number; learn_cost?: number; appraisal_cost?: number };

export function Overlays({ world, ch }: { world: GameWorld; ch: Character }) {
  const o = overlay.value;
  const npcTab = useSignal<string | null>(null);
  if (o.kind === 'none') return null;
  // Khung panel theo loại nội dung (bộ UI batch 08).
  const skin =
    o.kind === 'menu'
      ? ({ root: 'large', pets: 'pets', bag: 'bag', quests: 'quest', settings: 'settings' } as const)[o.page]
      : o.kind === 'npc'
        ? npcTab.value === 'shop'
          ? 'shop'
          : npcTab.value === 'learn'
            ? 'learn'
            : npcTab.value === 'quest'
              ? 'quest'
              : 'dialogue'
        : 'confirm';
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
      <div class="row">
        <button class="btn" onClick={closeOverlay}>Đóng</button>
      </div>
    </>
  );
}

function Back({ to = 'root' }: { to?: 'root' }) {
  return (
    <div class="row">
      <button class="btn" data-testid="overlay-back" onClick={() => (overlay.value = { kind: 'menu', page: to })}>
        Trở về
      </button>
      <button class="btn" onClick={closeOverlay}>Đóng</button>
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
  return (
    <>
      <h2>Linh thú ({pets.length})</h2>
      {pets.length === 0 && <p class="muted">Bạn chưa có linh thú. Hãy chọn một bệ đá ở Triệu Linh Điện.</p>}
      <div class="list">
        {pets.map((p) => (
          <PetRow key={p.id} p={p}>
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

function Bag({ world, ch }: { world: GameWorld; ch: Character }) {
  const items = Object.entries(ch.inventory).filter(([, n]) => n > 0);
  return (
    <>
      <h2>Túi đồ</h2>
      <div class="list">
        {items.length === 0 && <p class="muted">Túi trống.</p>}
        {items.map(([id, n]) => (
          <div class="item" key={id}>
            {iconFor(id) && <img class="icon" src={iconFor(id)!} alt="" />}
            <div class="grow">{world.content.itemName(id)}</div>
            <b>×{n}</b>
          </div>
        ))}
      </div>
      <p class="muted">{ch.gold} vàng</p>
      <Back />
    </>
  );
}

function questState(world: GameWorld, ch: Character) {
  const quests = Object.values(world.content.cat.quests) as { id: string; name: string; description?: string; count?: number }[];
  return quests.map((q) => {
    const s = ch.quests[q.id];
    return { q, s, ready: !!s && !s.claimed && s.progress >= (q.count ?? 1) };
  });
}

function Quests({ world, ch }: { world: GameWorld; ch: Character }) {
  const list = questState(world, ch).filter((x) => x.s);
  return (
    <>
      <h2>Nhiệm vụ</h2>
      <div class="list">
        {list.length === 0 && <p class="muted">Chưa nhận nhiệm vụ nào. Hỏi Kiểm Lâm Lio ở Bìa Rừng hoặc Quản Sự Tessa ở Quảng Trường.</p>}
        {list.map(({ q, s, ready }) => (
          <div class="item" key={q.id}>
            <div class="grow">
              <b>{q.name}</b>
              <div class="muted">{q.description}</div>
            </div>
            <span>{s!.claimed ? 'Đã xong' : ready ? 'Báo cáo được' : `${s!.progress}/${q.count ?? 1}`}</span>
          </div>
        ))}
      </div>
      <Back />
    </>
  );
}

function Settings() {
  const s = settings.value;
  return (
    <>
      <h2>Cài đặt · Đồ họa</h2>
      <p class="muted">Thấp: giảm độ phân giải, tắt bóng đổ, hiệu ứng và hậu kỳ. Trung bình: thêm chỉnh màu theo giờ, làm mờ dải trên/dưới kiểu HD-2D, đèn và tia nắng. Cao: thêm bloom và bóng thật. Quái, NPC và thông tin trận giữ nguyên ở mọi mức.</p>
      <div class="list">
        <div>
          <div class="muted">Chất lượng</div>
          <div class="seg" data-testid="quality">
            {(['low', 'medium', 'high'] as Quality[]).map((q) => (
              <button key={q} class={`btn ${s.quality === q ? 'on' : ''}`} data-testid={`quality-${q}`} onClick={() => updateSettings({ quality: q })}>
                {PRESETS[q].label}
              </button>
            ))}
          </div>
        </div>
        <div>
          <div class="muted">Giới hạn khung hình</div>
          <div class="seg">
            {([30, 60] as const).map((f) => (
              <button key={f} class={`btn ${s.fps === f ? 'on' : ''}`} data-testid={`fps-${f}`} onClick={() => updateSettings({ fps: f })}>
                {f} FPS
              </button>
            ))}
          </div>
        </div>
        <div>
          <div class="muted">Phím điều hướng trên màn hình</div>
          <div class="seg">
            <button class={`btn ${s.dpad ? 'on' : ''}`} onClick={() => updateSettings({ dpad: true })}>Hiện</button>
            <button class={`btn ${!s.dpad ? 'on' : ''}`} onClick={() => updateSettings({ dpad: false })}>Ẩn</button>
          </div>
        </div>
        <div>
          <div class="muted">Mật độ giao diện</div>
          <div class="seg" data-testid="hud-density">
            <button class={`btn ${s.hud === 'full' ? 'on' : ''}`} data-testid="hud-full" onClick={() => updateSettings({ hud: 'full' })}>Đầy đủ</button>
            <button class={`btn ${s.hud === 'compact' ? 'on' : ''}`} data-testid="hud-compact" onClick={() => updateSettings({ hud: 'compact' })}>Gọn</button>
          </div>
        </div>
        <div>
          <div class="muted">Thời gian trong game (ánh sáng ngoài trời)</div>
          <div class="seg" data-testid="time-mode">
            {([['auto', 'Theo giờ máy'], ['day', 'Ban ngày'], ['dusk', 'Hoàng hôn'], ['night', 'Ban đêm']] as const).map(([k, label]) => (
              <button key={k} class={`btn ${s.time === k ? 'on' : ''}`} data-testid={`time-${k}`} onClick={() => updateSettings({ time: k })}>{label}</button>
            ))}
          </div>
        </div>
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
      {tab === 'quest' && <QuestDesk world={world} ch={ch} />}
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

function QuestDesk({ world, ch }: { world: GameWorld; ch: Character }) {
  return (
    <div class="list">
      {questState(world, ch).map(({ q, s, ready }) => (
        <div class="item" key={q.id}>
          <div class="grow">
            <b>{q.name}</b>
            <div class="muted">{q.description}</div>
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
  return (
    <>
      <h2>Bệ triệu hồi: {st.name}</h2>
      <div class="item" style={{ marginBottom: 12 }}>
        <PetPortrait species={ped.species} size={72} />
        <div class="grow">
          <p style={{ margin: 0 }}>{st.blurb}</p>
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
      <div class="row">
        <button class="btn" onClick={closeOverlay}>Đóng</button>
      </div>
    </>
  );
}
