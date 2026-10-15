import { lang, setLang, tn, type Lang } from '../i18n';
import { signal } from '@preact/signals';
import { useEffect, useState } from 'preact/hooks';
import type { Pet } from '@phimond/protocol';
import type { Game, Page, Confirm } from '../game/controller.ts';
import { petManifest, portraitStyle } from '../render/pets.ts';
type PetManifest = Awaited<ReturnType<typeof petManifest>>;
import { Icon } from './icons.tsx';

const manifest = signal<PetManifest | null>(null);
void petManifest().then((m) => (manifest.value = m));
export const PetIcon = ({ species, size = 48 }: { species: string; size?: number }) => {
  const m = manifest.value; if (!m) return <span style={{ width: size, height: size }} />;
  return <span role="img" aria-label={species} style={portraitStyle(m, species, size)} />;
};

type Rec = Record<string, any>; // eslint-disable-line @typescript-eslint/no-explicit-any
const TITLES: Record<string, string> = { Companions: 'Linh thú', Inventory: 'Túi đồ', Quests: 'Nhiệm vụ', Ranch: 'Nông trại', NPC: 'Trò chuyện', Skills: 'Kỹ năng', Items: 'Vật phẩm', Shop: 'Cửa hàng', Journey: 'Hành trình', Teleport: 'Thủy Tinh Dịch Chuyển', Settings: 'Cài đặt' };
const ROLE_LABEL: Record<string, string> = { shop: 'Cửa hàng', quest: 'Nhiệm vụ', breed: 'Nông trại · Ghép', appraise: 'Giám định', heal: 'Hồi phục linh thú', arena: 'Thách đấu đấu trường', strengthen: 'Cường hóa linh thú', recipe: 'Học công thức', learn: 'Học kỹ năng' };

function Shell({ title, game, children }: { title: string; game: Game; children: preact.ComponentChildren }) {
  useEffect(() => { const b = document.querySelector<HTMLElement>('[data-menu] .body button:not(:disabled), [data-menu] .body select'); b?.focus({ preventScroll: true }); }, [title]);
  return (
    <div class="mwrap" data-ui>
      <section class="sheet" data-menu role="dialog" aria-modal="true" aria-label={title}>
        <div class="band" aria-hidden="true">{title}</div>
        <button class="x" aria-label="Đóng" onClick={() => game.close()}>×</button>
        <div class="body">{children}</div>
      </section>
    </div>
  );
}
const Bar = ({ kind, v, max }: { kind: 'hp' | 'mp' | 'xp'; v: number; max: number }) => (
  <div class={`bar ${kind}`}><div class="fill" style={{ width: `${Math.max(0, Math.min(100, (v / Math.max(1, max)) * 100))}%` }} /><i class="otl">{kind.toUpperCase()} {Math.round(v)}/{Math.round(max)}</i></div>
);
const Seg = ({ items, value, set }: { items: [string, string][]; value: string; set: (v: string) => void }) => (
  <div class="seg" role="tablist">{items.map(([k, l]) => <button role="tab" aria-selected={k === value} onClick={() => set(k)}>{l}</button>)}</div>
);
const Stars = ({ n }: { n: number }) => <span class="stars" aria-label={`${n} sao`}>{'★'.repeat(Math.max(0, n))}</span>;
const nameOf = (cat: Rec | null, group: string, id: string): string => cat?.[group]?.[id]?.name ?? id;

// ---------- Linh thú ----------
function Companions({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  const pets = game.pets();
  const [sel, setSel] = useState(c.active_pet_id || pets[0]?.id || '');
  const [tab, setTab] = useState(() => { const h = game.tabHint.peek(); game.tabHint.value = ''; return h || 'attr'; });
  const [lin, setLin] = useState<Rec | null>(null);
  const [conf, setConf] = useState<Confirm | null>(null);
  const pet: Pet | undefined = pets.find((p) => p.id === sel) ?? pets[0];
  const sp = pet ? cat.species[pet.species_id] : null;
  const active = !!pet && pet.id === c.active_pet_id;
  const learnable: Rec[] = pet && sp ? (sp.skills as string[]).filter((id) => !pet.skills.includes(id)).map((id) => cat.skills[id] as Rec).filter((d) => d && pet.level >= d.learn_level) : [];
  return (
    <Shell title={TITLES.Companions!} game={game}>
      <div class="row" style="align-items:flex-start;flex-wrap:nowrap">
        <div style="flex:1 1 44%;display:flex;flex-direction:column;gap:6px;min-width:0;overflow:auto">
          {pets.map((p) => (
            <button class="pet-row" aria-pressed={p.id === pet?.id} onClick={() => { setSel(p.id); setConf(null); }}>
              <span class="ic"><PetIcon species={p.species_id} size={48} /></span>
              <span><span class="nm">{p.id === c.active_pet_id ? '◆ ' : ''}{tn(p.name)}{p.strengthening ? <span class="plus"> +{p.strengthening}</span> : null}</span><small>Lv.{p.level} · <Stars n={p.star} />{p.appraised ? ' · Đã giám định' : ''}</small></span>
              {p.id === c.active_pet_id && <span class="chip gold">Theo sau</span>}
            </button>
          ))}
          {!pets.length && <p class="msg">Chưa có linh thú.</p>}
        </div>
        {pet && (
          <div style="flex:1 1 56%;display:flex;flex-direction:column;gap:8px;min-width:0">
            <div class="card">
              <b>{tn(pet.name)}</b> <span class="chip">Lv.{pet.level}</span> {pet.gender && <span class="chip">{pet.gender === 'female' ? '♀' : pet.gender === 'male' ? '♂' : pet.gender}</span>}
              <Bar kind="hp" v={pet.hp} max={pet.max_hp} /><Bar kind="mp" v={pet.mp} max={pet.max_mp} />
            </div>
            <Seg items={[['attr', 'Thuộc tính'], ['res', 'Kháng'], ['skill', 'Kỹ năng'], ['grow', 'Phát triển']]} value={tab} set={setTab} />
            <div class="card">
              {tab === 'attr' && <div class="kv">{Object.entries((sp?.base ?? {}) as Rec).map(([k, v]) => <div><span>{ATTR[k] ?? k}</span><b>{String(v)}</b></div>)}</div>}
              {tab === 'res' && <div class="kv"><div><span>Chủng tộc</span><b>{nameOf(cat, 'races', sp?.race)}</b></div><div><span>Nguyên tố</span><b>{ELEM[sp?.element] ?? sp?.element}</b></div><div><span>Sao</span><b>{pet.star}★</b></div><div><span>Bắt được</span><b>{sp?.catchable ? 'Có' : 'Không'}</b></div></div>}
              {tab === 'skill' && <>
                <div class="row">{pet.skills.map((s) => <span class="chip">{nameOf(cat, 'skills', s)}</span>)}</div>
                {learnable.length > 0 && <div style="margin-top:8px;display:flex;flex-direction:column;gap:6px"><span class="msg">Có thể học (phí {(cat.rules as Rec)?.learn_cost ?? 10} vàng, cần đứng gần người dạy)</span>
                  {learnable.map((s) => <div class="row" style="justify-content:space-between"><span>{s.name} <span class="msg">Cấp {s.learn_level} · MP {s.mp_cost}</span></span><button class="btn" onClick={() => void game.send('pet.learn', { pet_id: pet.id, skill_id: s.id })}>Học</button></div>)}</div>}
              </>}
              {tab === 'grow' && <>
                <div class="kv"><div><span>Cấp</span><b>{pet.level}</b></div><div><span>Kinh nghiệm</span><b>{pet.xp}</b></div><div><span>Cường hóa</span><b>+{pet.strengthening}/10</b></div><div><span>Cha mẹ</span><b>{pet.parents.length ? pet.parents.length : 'Hoang dã'}</b></div><div><span>Giám định</span><b>{pet.appraised ? 'Đã' : 'Chưa'}</b></div></div>
                <div class="row" style="margin-top:8px"><button class="btn" onClick={() => { void game.session.fetchLineage(pet.id).then((r) => setLin(r as Rec)).catch(() => game.message('Không tải được phả hệ.')); }}>Xem phả hệ</button></div>
                {lin && <div class="lineage"><Lineage node={lin} cat={cat} /></div>}
              </>}
            </div>
            {conf ? (
              <div class="confirm" role="alertdialog"><span>{conf.message}</span><div class="row"><button class="btn warn" onClick={() => { void game.send('pet.release', { pet_id: pet.id }); setConf(null); }}>Thả</button><button class="btn" onClick={() => setConf(null)}>Hủy</button></div></div>
            ) : (
              <div class="row">
                <button class="btn pri" disabled={active} onClick={() => void game.send('pet.activate', { pet_id: pet.id })}>{active ? 'Đang theo sau' : 'Theo sau'}</button>
                <button class="btn" disabled={pet.appraised} onClick={() => void game.send('pet.appraise', { pet_id: pet.id })}>Giám định</button>
                <button class="btn" onClick={() => game.open('Ranch')}>Nông trại</button>
                <button class="btn warn" disabled={active} onClick={() => setConf({ message: `Thả ${tn(pet.name)} về tự nhiên? Không thể hoàn tác.`, op: 'pet.release', data: { pet_id: pet.id } })}>Thả…</button>
              </div>
            )}
          </div>
        )}
      </div>
    </Shell>
  );
}
const ATTR: Rec = { strength: 'Sức mạnh', agility: 'Nhanh nhẹn', defense: 'Phòng thủ', intelligence: 'Trí tuệ', spirit: 'Tinh thần', stamina: 'Thể lực', critical: 'Chí mạng' };
const ELEM: Rec = { earth: 'Đất', water: 'Nước', wind: 'Gió', fire: 'Lửa', neutral: 'Trung tính', light: 'Sáng', dark: 'Tối' };

function Lineage({ node, cat }: { node: Rec; cat: Rec }) {
  const p = node.pet as Rec;
  return <ul><li><b>{tn(p.name)}</b> <span class="msg">{nameOf(cat, 'species', p.species_id)} · Lv.{p.level}</span>{(node.parents as Rec[] | null)?.length ? <>{(node.parents as Rec[]).map((n) => <Lineage node={n} cat={cat} />)}</> : null}</li></ul>;
}

// ---------- Túi đồ ----------
function Inventory({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  const items = Object.entries(c.inventory).filter(([, n]) => n > 0);
  const [pg, setPg] = useState(0); const [pick, setPick] = useState('');
  const pages = 1; void pg; void setPg; void pages;
  const slots = Array.from({ length: 24 }, (_, i) => items[i]);
  const it = pick ? cat.items[pick] : null;
  return (
    <Shell title={TITLES.Inventory!} game={game}>
      <div class="grid6">{slots.map((s) => s
        ? <button class="slot" aria-pressed={pick === s[0]} style={pick === s[0] ? 'border-color:var(--gold)' : ''} onClick={() => setPick(s[0])}>{nameOf(cat, 'items', s[0])}<b>{s[1]}</b></button>
        : <div class="slot" aria-hidden="true" />)}</div>
      {it && <div class="card"><b>{it.name}</b> · <span class="msg">{KIND[it.kind] ?? it.kind} · Sức mạnh {it.power} · Giá {it.price}</span></div>}
      <p class="msg">Vàng {c.gold} · Pha lê {c.crystals}</p>
    </Shell>
  );
}
const KIND: Rec = { blessing: 'Phước lành', capture: 'Thu phục', heal_hp: 'Hồi HP', heal_mp: 'Hồi MP', soul: 'Linh hồn', hp: 'Hồi HP', mp: 'Hồi MP' };

// ---------- Nhiệm vụ ----------
function Quests({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  const [sel, setSel] = useState('');
  const list = Object.values(cat.quests as Rec);
  const q = list.find((x: Rec) => x.id === sel) ?? null;
  const st = q ? c.quests[q.id] : undefined;
  return (
    <Shell title={TITLES.Quests!} game={game}>
      <div class="row" style="align-items:flex-start;flex-wrap:nowrap">
        <div style="flex:1 1 42%;display:flex;flex-direction:column;gap:6px;min-width:0">
          {list.map((x: Rec) => { const s = c.quests[x.id]; return (
            <button class="pet-row" style="grid-template-columns:1fr auto" aria-pressed={x.id === sel} onClick={() => setSel(x.id)}>
              <span><span class="nm">{x.name}</span><small>{s ? (s.claimed ? 'Đã nhận thưởng' : `${s.progress}/${x.count}`) : 'Chưa nhận'}</small></span>
              {s?.claimed && <span class="chip">✓</span>}
            </button>); })}
        </div>
        <div style="flex:1 1 58%;min-width:0" class="card">
          {!q && <p class="msg">Chọn một nhiệm vụ để xem chi tiết.</p>}
          {q && <>
            <b>{q.name}</b><p class="msg">{q.description}</p>
            <div class="kv"><div><span>Tiến độ</span><b>{st ? `${st.progress}/${q.count}` : `0/${q.count}`}</b></div><div><span>Vàng</span><b>{q.gold}</b></div><div><span>Kinh nghiệm</span><b>{q.xp}</b></div>
              <div><span>Vật phẩm</span><b>{Object.entries(q.items ?? {}).map(([k, n]) => `${nameOf(cat, 'items', k)}×${n}`).join(', ') || '—'}</b></div></div>
            <div class="row" style="margin-top:8px">
              <button class="btn pri" disabled={!!st} onClick={() => void game.send('quest.accept', { quest_id: q.id })}>Nhận</button>
              <button class="btn" disabled={!st || st.claimed || st.progress < q.count} onClick={() => void game.send('quest.claim', { quest_id: q.id })}>Nhận thưởng</button>
            </div></>}
        </div>
      </div>
    </Shell>
  );
}

// ---------- Nông trại ----------
function Ranch({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec; const pets = game.pets();
  const [tab, setTab] = useState(() => { const h = game.tabHint.peek(); game.tabHint.value = ''; return h || 'syn'; }); const [a, setA] = useState(''); const [b, setB] = useState(''); const [rid, setRid] = useState(''); const [bless, setBless] = useState(false);
  const [conf, setConf] = useState<Confirm | null>(null); const [donor, setDonor] = useState(''); const [tgt, setTgt] = useState('');
  const recipes = c.recipes.map((r) => cat.recipes[r]).filter(Boolean) as Rec[];
  const r = recipes.find((x) => x.id === rid) ?? recipes[0];
  const opt = (sel: string) => [<option value="">— chọn —</option>, ...pets.map((p) => <option value={p.id} selected={p.id === sel}>{tn(p.name)} (Lv.{p.level})</option>)];
  const Pick = ({ label, v, set }: { label: string; v: string; set: (x: string) => void }) => <label class="msg">{label}<select value={v} onChange={(e) => set((e.target as HTMLSelectElement).value)}>{opt(v)}</select></label>;
  return (
    <Shell title={TITLES.Ranch!} game={game}>
      <Seg items={[['syn', 'Ghép'], ['str', 'Cường hóa'], ['app', 'Giám định']]} value={tab} set={(t) => { setTab(t); setConf(null); }} />
      {tab === 'syn' && <>
        <Pick label="Cha / Mẹ A" v={a} set={setA} /><Pick label="Cha / Mẹ B" v={b} set={setB} />
        <label class="msg">Công thức<select value={r?.id ?? ''} onChange={(e) => setRid((e.target as HTMLSelectElement).value)}>{recipes.length ? recipes.map((x) => <option value={x.id}>{x.name}</option>) : <option value="">Chưa học công thức</option>}</select></label>
        {(Object.values(cat.recipes as Rec) as Rec[]).filter((x) => !c.recipes.includes(x.id)).map((x) => <div class="card row" style="justify-content:space-between"><span>{x.name} <span class="msg">chưa học</span></span><button class="btn" disabled={c.gold < 30} onClick={() => void game.send('recipe.learn', { recipe_id: x.id })}>Học · 30 vàng</button></div>)}
        {r && <div class="card msg">Yêu cầu: linh thú Lv.{r.min_level} · {r.soul_cost} Linh hồn · {r.gold_cost} vàng{r.opposite_gender ? ' · khác giới' : ''}{r.same_star ? ' · cùng sao' : ''}</div>}
        <label class="chk"><input type="checkbox" checked={bless} onChange={(e) => setBless((e.target as HTMLInputElement).checked)} />Dùng Lá phước lành (có trong túi: {c.inventory['blessing_leaf'] ?? 0})</label>
        {conf ? <div class="confirm"><span>{conf.message}</span><div class="row"><button class="btn pri" onClick={() => { void game.send('breeding.synthesize', conf.data as never); setConf(null); }}>Xác nhận</button><button class="btn" onClick={() => setConf(null)}>Hủy</button></div></div>
          : <button class="btn pri" disabled={!a || !b || a === b || !r} onClick={() => setConf({ message: 'Cả hai linh thú cha mẹ sẽ bị tiêu hao. Tiếp tục ghép?', op: 'breeding.synthesize', data: { parent_a: a, parent_b: b, recipe_id: r!.id, blessing: bless ? 1 : 0 } })}>Ghép linh thú</button>}
      </>}
      {tab === 'str' && (() => {
        const T = pets.find((p) => p.id === tgt); const D = pets.find((p) => p.id === donor);
        const donors = pets.filter((p) => T && p.id !== T.id && p.star === T.star && p.id !== c.active_pet_id);
        const why = !T ? 'Chọn linh thú cần cường hóa.' : (T.strengthening ?? 0) >= 10 ? 'Đã đạt tối đa 10 lần cường hóa.' : !donors.length ? `Cần một linh thú ${T.star}★ khác (không đang theo sau) để hiến tế.` : !D ? 'Chọn linh thú hiến tế cùng số sao.' : '';
        const Card = ({ p, role }: { p?: Pet; role: string }) => (
          <div class="pick" aria-label={role}>
            {p ? <><PetIcon species={p.species_id} size={44} /><span class="big">{tn(p.name)}<span class="plus">{p.strengthening ? ` +${p.strengthening}` : ''}</span></span><small class="msg">Lv.{p.level} · <Stars n={p.star} /></small></> : <small class="msg">{role}</small>}
          </div>
        );
        return <>
          <div class="stepper"><Card p={T} role="Linh thú được cường hóa" /><span class="arr" aria-hidden="true" /><Card p={D} role="Linh thú hiến tế" /></div>
          <div class="pips" role="img" aria-label={`Cường hóa ${T?.strengthening ?? 0}/10`}>{Array.from({ length: 10 }, (_, i) => <b class={i < (T?.strengthening ?? 0) ? 'on' : ''} />)}<span class="otl">+{T?.strengthening ?? 0}/10</span></div>
          <label class="msg">Linh thú được cường hóa<select value={tgt} onChange={(e) => { setTgt((e.target as HTMLSelectElement).value); setDonor(''); }}>{[<option value="">— chọn —</option>, ...pets.map((p) => <option value={p.id} selected={p.id === tgt}>{tn(p.name)} (Lv.{p.level} · {p.star}★{p.strengthening ? ` · +${p.strengthening}` : ''})</option>)]}</select></label>
          <label class="msg">Linh thú hiến tế (cùng số sao, sẽ biến mất)<select value={donor} disabled={!T} onChange={(e) => setDonor((e.target as HTMLSelectElement).value)}>{[<option value="">— chọn —</option>, ...donors.map((p) => <option value={p.id} selected={p.id === donor}>{tn(p.name)} (Lv.{p.level})</option>)]}</select></label>
          {why && <p class="msg">{why}</p>}
          {conf ? <div class="confirm"><span>{conf.message}</span><div class="row"><button class="btn pri" onClick={() => { void game.send('pet.strengthen', conf.data as never); setConf(null); setDonor(''); }}>Xác nhận</button><button class="btn" onClick={() => setConf(null)}>Hủy</button></div></div>
            : <button class="btn pri" disabled={!!why} onClick={() => setConf({ message: `${tn(D?.name ?? 'Linh thú hiến tế')} sẽ biến mất để cường hóa ${tn(T?.name ?? '')}. Tiếp tục?`, op: 'pet.strengthen', data: { pet_id: tgt, donor_id: donor } })}>Cường hóa</button>}
        </>;
      })()}
      {tab === 'app' && <>
        <Pick label="Linh thú cần giám định" v={tgt} set={setTgt} />
        <button class="btn pri" disabled={!tgt} onClick={() => void game.send('pet.appraise', { pet_id: tgt })}>Giám định (phí {(cat.rules as Rec)?.appraisal_cost ?? 5} vàng)</button>
      </>}
    </Shell>
  );
}

// ---------- NPC ----------
function Npc({ game }: { game: Game }) {
  const cat = game.catalog.value as Rec; const n = cat.npcs[game.npcId.value] as Rec | undefined;
  if (!n) return <Shell title="Trò chuyện" game={game}><p class="msg">Không có ai ở đây.</p></Shell>;
  return (
    <Shell title={n.name} game={game}>
      <p class="msg">Chào mừng, lữ khách. Bạn cần gì?</p>
      {(n.roles as string[]).map((role) => <button class="btn" onClick={() => {
        if (role === 'shop') game.open('Shop'); else if (role === 'quest') game.open('Quests');
        else if (role === 'breed' || role === 'recipe') { game.tabHint.value = 'syn'; game.open('Ranch'); }
        else if (role === 'strengthen') { game.tabHint.value = 'str'; game.open('Ranch'); }
        else if (role === 'appraise') { game.tabHint.value = 'app'; game.open('Ranch'); }
        else if (role === 'learn') { game.tabHint.value = 'skill'; game.open('Companions'); }
        else if (role === 'heal') void game.send('pet.heal', {}); else if (role === 'arena') void game.send('arena.challenge', {});
      }}>{ROLE_LABEL[role] ?? role}</button>)}
      <button class="btn" onClick={() => game.close()}>Đóng</button>
    </Shell>
  );
}

// ---------- Cửa hàng ----------
function Shop({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec; const near = game.nearby();
  const list = Object.values(cat.items as Rec).filter((i: Rec) => i.id !== 'synthesis_soul' || true);
  return (
    <Shell title={TITLES.Shop!} game={game}>
      <p class="msg">Vàng: <b style="color:var(--gold)">{c.gold}</b>{!near || !(near.roles as string[]).includes('shop') ? ' · Hãy đến gần người bán hàng.' : ''}</p>
      {list.map((i: Rec) => <div class="card row" style="justify-content:space-between"><span><b>{i.name}</b> <span class="msg">{KIND[i.kind] ?? i.kind} · có {c.inventory[i.id] ?? 0}</span></span><button class="btn pri" disabled={c.gold < i.price} onClick={() => void game.send('shop.buy', { item_id: i.id, quantity: 1 })}>Mua 1 · {i.price}</button></div>)}
    </Shell>
  );
}

// ---------- Kỹ năng / Vật phẩm trong trận ----------
function Skills({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  const unit = c.battle?.units.find((u) => u.side === 'player' && u.id.includes(c.active_pet_id)) ?? c.battle?.units.find((u) => u.side === 'player');
  const pet = game.pets().find((p) => p.id === c.active_pet_id);
  const mp = unit?.mp ?? pet?.mp ?? 0;
  return (
    <Shell title={TITLES.Skills!} game={game}>
      {(pet?.skills ?? []).map((s) => { const d = cat.skills[s] as Rec; return <button class="btn" style="display:flex;justify-content:space-between;width:100%" disabled={mp < d.mp_cost} onClick={() => game.chooseSkill(s)}><span>{d.name}</span><span class="msg">Cấp {d.learn_level} · MP {d.mp_cost}</span></button>; })}
      {!pet && <p class="msg">Không có linh thú đang chiến đấu.</p>}
    </Shell>
  );
}
function Items({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  const usable = Object.entries(c.inventory).filter(([id, n]) => n > 0 && ['potion', 'ether', 'capture_seal'].includes(id));
  return (
    <Shell title={TITLES.Items!} game={game}>
      {usable.map(([id, n]) => <button class="btn" style="display:flex;justify-content:space-between;width:100%" onClick={() => { if (id === 'capture_seal') game.chooseCapture(); else { game.selectedAction.value = { choice: 'item', item_id: id }; game.automatic.value = false; game.close(); } }}><span>{cat.items[id].name}</span><span class="msg">×{n}</span></button>)}
      {!usable.length && <p class="msg">Không có vật phẩm dùng được.</p>}
    </Shell>
  );
}

// ---------- Trụ dịch chuyển (Quảng Trường): chỉ hiện vùng đủ cấp / bậc đấu trường ----------
function Teleport({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  const here = cat.maps[c.map_id]; const ports = (here?.portals ?? []) as Rec[];
  const ok = ports.filter((p) => { const d = cat.maps[p.to]; return d && c.level >= d.min_level && c.arena_tier >= d.arena_required; });
  const locked = ports.length - ok.length;
  return (
    <Shell title={TITLES.Teleport!} game={game}>
      <p class="msg">Chọn nơi muốn đến. Chỉ hiện những vùng phù hợp với cấp của bạn.</p>
      {ok.map((p) => { const d = cat.maps[p.to]; return <button class="btn pri tp" onClick={() => game.approach('portal', p.id)}><b>{d.name}</b><span class="msg">{d.min_level > 1 ? `Từ Lv.${d.min_level}` : 'Mọi cấp'}</span></button>; })}
      {!ok.length && <p class="msg">Chưa có vùng nào phù hợp.</p>}
      {locked > 0 && <p class="msg">Còn {locked} vùng chưa mở (cần thêm cấp hoặc bậc đấu trường).</p>}
    </Shell>
  );
}

// ---------- Hành trình & Cài đặt ----------
function Journey({ game }: { game: Game }) {
  const c = game.character.value!; const cat = game.catalog.value as Rec;
  return <Shell title={TITLES.Journey!} game={game}><div class="kv"><div><span>Nhân vật</span><b>{c.name}</b></div><div><span>Cấp</span><b>{c.level}</b></div><div><span>Khu vực</span><b>{cat.maps[c.map_id]?.name}</b></div><div><span>Linh thú</span><b>{game.pets().length}</b></div><div><span>Nhiệm vụ hoàn thành</span><b>{Object.values(c.quests).filter((q) => q.claimed).length}/{Object.keys(cat.quests).length}</b></div><div><span>Bậc đấu trường</span><b>{c.arena_tier}</b></div></div></Shell>;
}
export const qualityPref = signal<'auto' | 'low' | 'medium' | 'high'>('auto');
export const statsOn = signal(false);
function Settings({ game, onQuality }: { game: Game; onQuality: (q: 'auto' | 'low' | 'medium' | 'high') => void }) {
  const st = game.session.status.value;
  return (
    <Shell title={TITLES.Settings!} game={game}>
      <div class="card row" style="justify-content:space-between"><span>Kết nối: <b>{st === 'online' ? 'Đang trực tuyến' : st === 'connecting' ? 'Đang kết nối…' : 'Ngoại tuyến'}</b></span><button class="btn pri" onClick={() => void game.reconnect()}>Kết nối lại</button></div>
      <div class="card"><span class="msg">Chất lượng đồ họa</span><Seg items={[['auto', 'Tự động'], ['low', 'Thấp'], ['medium', 'Vừa'], ['high', 'Cao']]} value={qualityPref.value} set={(v) => { qualityPref.value = v as never; onQuality(v as never); }} /></div>
      <div class="card"><span class="msg">Ngôn ngữ tên hiển thị</span><Seg items={[['vi', 'Tiếng Việt'], ['en', 'English']]} value={lang.value} set={(v) => { if (v !== lang.value) setLang(v as Lang); }} /></div>
      <label class="chk"><input type="checkbox" checked={statsOn.value} onChange={(e) => (statsOn.value = (e.target as HTMLInputElement).checked)} />Hiện thống kê hiệu năng (F3)</label>
      <button class="btn warn" onClick={() => void game.signOut()}>Đăng xuất</button>
    </Shell>
  );
}

export function MenuHost({ game, onQuality }: { game: Game; onQuality: (q: 'auto' | 'low' | 'medium' | 'high') => void }) {
  const p: Page = game.page.value;
  game.tick.value; // tính lại khi có batch mới
  if (!game.character.value || !game.catalog.value) return null;
  switch (p) {
    case 'Companions': return <Companions game={game} />;
    case 'Inventory': return <Inventory game={game} />;
    case 'Quests': return <Quests game={game} />;
    case 'Ranch': return <Ranch game={game} />;
    case 'NPC': return <Npc game={game} />;
    case 'Skills': return <Skills game={game} />;
    case 'Items': return <Items game={game} />;
    case 'Shop': return <Shop game={game} />;
    case 'Teleport': return <Teleport game={game} />;
    case 'Journey': return <Journey game={game} />;
    case 'Settings': return <Settings game={game} onQuality={onQuality} />;
    default: return null;
  }
}
export const SHORTCUTS: [Page, string, string, string][] = [['Companions', 'Linh thú', 'button_pet', ''], ['Inventory', 'Túi đồ', 'button_inventory', ''], ['Quests', 'Nhiệm vụ', 'button_quest', ''], ['Journey', 'Hành trình', 'button_round', 'map'], ['Shop', 'Cửa hàng', 'button_shop', ''], ['Ranch', 'Nông trại', 'button_guild', ''], ['Settings', 'Cài đặt', 'button_settings', ''], ['World', 'Thế giới', 'button_round', 'world']];
export function Shortcuts({ game }: { game: Game }) {
  return (
    <div class="mwrap" data-ui>
      <section class="sheet short" data-menu role="dialog" aria-label="Lối tắt">
        <div class="band" aria-hidden="true">Menu</div>
        <button class="x" aria-label="Đóng" onClick={() => game.close()}>×</button>
        <div class="body"><div class="grid">
          {SHORTCUTS.map(([p, l, sp, ic]) => <button class="it" onClick={() => game.open(p)}><span class="ci" style={{ backgroundImage: `url(./assets/ui/${sp}.png)` }}>{ic ? <Icon n={ic} /> : null}</span>{l}</button>)}
        </div></div>
      </section>
    </div>
  );
}
