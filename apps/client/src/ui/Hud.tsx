import { useEffect, useRef, useState } from 'preact/hooks';
import type { Character } from '@phimond/protocol';
import { currentMap, interactHint, type GameWorld } from '../game/world.ts';
import { viName } from '../game/content.ts';
import { currentGoal } from '../game/goal.ts';
import { settings } from '../state/settings.ts';
import { battleResultOpen, closeOverlay, log, LOG_TABS, overlay, pushLog, toasts, type LogTab } from '../state/ui.ts';
import type { Direction } from '../world/coords.ts';
import { session } from '../state/app.ts';
import { PetPortrait } from './PetArt.tsx';

/** Cùng công thức server: lên cấp khi XP ≥ cấp × 25 (data/balance/rules.json → xp_per_level). */
const XP_PER_LEVEL = 25;

/** Bố cục HUD gốc (P01-R09): Lv + pet trái trên, menu phải, D-pad trái dưới, Chọn/Trở về phải dưới, chat 6 tab giữa dưới. */
export function Hud({ world, ch }: { world: GameWorld; ch: Character }) {
  const pet = ch.pets.find((p) => p.id === ch.active_pet_id && !p.retired);
  const map = currentMap.value;
  const status = session.status.value;
  // Trong trận, giao diện trận đấu lo hết: ẩn điều khiển thế giới để không đè lên nhau (đánh giá T5).
  const inBattle = !!ch.battle || battleResultOpen.value;
  const compact = settings.value.hud === 'compact';
  const goal = currentGoal(ch, world.content);
  const hint = interactHint.value;
  // Cảnh báo máu thấp (đánh giá P0-2): viền thẻ pet nháy đỏ dưới 30%, nhắc một lần mỗi khi tụt qua ngưỡng.
  const low = !!pet && pet.hp > 0 && pet.hp < pet.max_hp * 0.3;
  const down = !!pet && pet.hp <= 0;
  const warned = useRef(false);
  useEffect(() => {
    if ((low || down) && !inBattle && !warned.current) {
      warned.current = true;
      pushLog(down ? `${viName(pet!.name)} đã kiệt sức — tới Kiểm Lâm Lio (Bìa Rừng) hoặc Y Sư Selka (Quảng Trường) để hồi phục.` : `${viName(pet!.name)} còn ít máu — nên hồi phục trước khi đụng quái.`, 'system');
    }
    if (!low && !down) warned.current = false;
  }, [low, down, inBattle]);
  return (
    <div class={`hud ${compact ? 'compact' : ''} ${inBattle ? 'in-battle' : ''}`}>
      <div class="hud-status" data-testid="hud-status-panel">
        <div class={`pet-row hud-card ${low ? 'danger' : ''} ${down ? 'danger down' : ''}`}>
          <div class="ring" role="button" aria-label="Linh thú" onClick={() => (overlay.value = { kind: 'menu', page: 'pets' })}>
            {pet ? <PetPortrait species={pet.species_id} /> : <div class="portrait" />}
            {pet && <div class="badge" title="Cấp linh thú">{pet.level}</div>}
          </div>
          <div class="stack">
            <div class="nm">{pet ? <b>{viName(pet.name)}</b> : <span class="muted">Chưa có linh thú</span>}</div>
            {pet && (
              <>
                <FrameBar kind="hp" row={0} v={pet.hp} max={pet.max_hp} label="HP" />
                <FrameBar kind="mp" row={1} v={pet.mp} max={pet.max_mp} label="MP" />
                <FrameBar kind="xp" row={2} v={pet.xp} max={pet.level * XP_PER_LEVEL} label="EXP" />
              </>
            )}
          </div>
        </div>
        <div class="me-row hud-card">
          <div class="lvl" title="Cấp nhân vật">
            Lv {ch.level}
          </div>
          <div class="who" data-testid="hud-name">
            {ch.name}
          </div>
          <FrameBar kind="xp" row={2} v={ch.xp} max={ch.level * XP_PER_LEVEL} label="EXP" slim />
          <div class="gold" data-testid="hud-gold">
            <i class="coin" />
            {ch.gold}
            <span class="vh"> · Lv {ch.level}</span>
          </div>
        </div>
      </div>

      {map && (
        <div class="hud-map" data-testid="hud-map">
          {map.name}
        </div>
      )}
      {goal && !compact && !inBattle && (
        <div class="hud-goal" data-testid="hud-goal">
          <b>{goal.title}</b>
          <span>{goal.detail}</span>
        </div>
      )}
      {map && !compact && !inBattle && <Minimap world={world} ch={ch} />}
      <span data-testid="hud-pos" style={{ position: 'absolute', left: -9999 }}>
        {ch.map_id} x {ch.x} · y {ch.y}
      </span>

      {status !== 'online' && (
        <div class="hud-net" data-testid="hud-status">
          {status === 'connecting' ? 'Đang kết nối…' : 'Mất kết nối máy chủ'}
          {status === 'offline' && (
            <button class="btn small" onClick={() => void session.connect().catch(() => undefined)}>
              Kết nối lại
            </button>
          )}
        </div>
      )}
      {status === 'online' && (
        <span data-testid="hud-status" style={{ position: 'absolute', left: -9999 }}>
          Trực tuyến
        </span>
      )}

      <MenuFan />
      <div class="hud-bar" aria-hidden="true" />

      {settings.value.dpad && <DPad world={world} />}

      <div class="hud-actions">
        <button class="round b" data-testid="btn-back" onClick={() => (overlay.value.kind === 'none' ? (overlay.value = { kind: 'menu', page: 'root' }) : closeOverlay())}>
          Trở về
        </button>
        <button class={`round a ${hint ? 'ready' : ''}`} data-testid="btn-select" onClick={() => world.primary()}>
          <span class={`lbl ${(hint ?? 'Chọn').length > 6 ? 'long' : ''}`}>{hint ?? 'Chọn'}</span>
        </button>
      </div>

      {!compact && <Chat />}
      <div class="toasts" data-testid="toasts">
        {toasts.value.map((t) => (
          <div key={t.id} class="toast">
            {t.text}
          </div>
        ))}
      </div>
    </div>
  );
}

/** Thanh chỉ số khung vàng (frame-bars) + ruột tô theo tỉ lệ; chữ số nằm trên thanh. */
export function FrameBar({ kind, row, v, max, label, slim }: { kind: 'hp' | 'mp' | 'xp'; row: number; v: number; max: number; label: string; slim?: boolean }) {
  const p = Math.max(0, Math.min(100, (v / Math.max(1, max)) * 100));
  return (
    <div class={`fb ${slim ? 'slim' : ''}`} data-testid={`fbar-${kind}`}>
      <em class={kind}>{label}</em>
      <div class={`fbar ${kind} r${row} ${slim ? 'slim' : ''} ${kind === 'hp' && p < 25 ? 'low' : ''}`} title={`${label} ${Math.floor(v)}/${max}`}>
        <div class="track">
          <i class="fill" style={{ clipPath: `inset(0 ${100 - p}% 0 0)` }} />
        </div>
        <span>
          {Math.floor(v)}/{max}
        </span>
      </div>
    </div>
  );
}

/** Bản đồ nhỏ: ô đi được, cổng, NPC và vị trí người chơi (vẽ từ lưới đi được, không cần ảnh). */
function Minimap({ world, ch }: { world: GameWorld; ch: Character }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const map = currentMap.value!;
  const grid = world.content.grid(map.id);
  useEffect(() => {
    const cv = ref.current;
    if (!cv || !grid) return;
    const k = Math.max(4, Math.min(10, Math.floor(220 / Math.max(grid.w, grid.h * 1.6))));
    cv.width = grid.w * k;
    cv.height = grid.h * k;
    const g = cv.getContext('2d')!;
    g.fillStyle = '#0d1420';
    g.fillRect(0, 0, cv.width, cv.height);
    for (let y = 0; y < grid.h; y++)
      for (let x = 0; x < grid.w; x++)
        if (grid.walkable(x, y)) {
          g.fillStyle = (x + y) % 2 ? '#6f8f62' : '#78996a';
          g.fillRect(x * k, y * k, k, k);
        }
    const dot = (x: number, y: number, c: string, r = k) => {
      g.fillStyle = c;
      g.fillRect(Math.round(x * k + (k - r) / 2), Math.round(y * k + (k - r) / 2), r, r);
    };
    for (const p of map.portals) if (p.rect) for (let y = 0; y < p.rect[3]; y++) for (let x = 0; x < p.rect[2]; x++) dot(p.rect[0] + x, p.rect[1] + y, p.locked ? '#7a6a4a' : '#e8c36a');
    for (const n of world.content.npcsOn(map.id)) dot(n.x, n.y, '#7fd6e8', Math.max(3, k));
    for (const q of map.pedestals) dot(q.x, q.y, '#c98ae8', Math.max(3, k));
    if (map.pillar) dot(map.pillar.x, map.pillar.y, '#c98ae8', Math.max(3, k));
    // Quái đang hiện trên đồng (chấm đỏ) để người chơi chủ động tránh hoặc tìm đánh.
    const hidden = ch.spawn_hidden ?? {};
    for (const w of map.wild_spawns ?? []) if (!(hidden as Record<string, number>)[w.id]) dot(w.x, w.y, '#ff6b5a', Math.max(3, k));
    dot(ch.x, ch.y, '#ffffff', Math.max(4, k + 1));
  }, [map.id, ch.x, ch.y, grid, JSON.stringify(ch.spawn_hidden ?? {})]);
  return (
    <div class="hud-minimap" data-testid="hud-minimap" aria-label="Bản đồ nhỏ">
      <canvas ref={ref} />
    </div>
  );
}

/** Một nút Menu; bấm mới sổ các nút Linh thú, Túi đồ, Nhiệm vụ, Cài đặt (như bản runtime). */
function MenuFan() {
  const [open, setOpen] = useState(false);
  const go = (page: 'pets' | 'bag' | 'quests' | 'settings') => {
    setOpen(false);
    overlay.value = { kind: 'menu', page };
  };
  return (
    <div class={`hud-menu ${open ? 'open' : ''}`}>
      <button class="rbtn main" data-testid="menu-open" aria-label="Menu" aria-expanded={open} onClick={() => setOpen(!open)}>
        <span>Menu</span>
      </button>
      {open && (
        <div class="fan">
          <button class="rbtn pet" data-testid="menu-pets" aria-label="Linh thú" onClick={() => go('pets')}>
            <span>Linh thú</span>
          </button>
          <button class="rbtn bag" data-testid="menu-bag" aria-label="Túi đồ" onClick={() => go('bag')}>
            <span>Túi đồ</span>
          </button>
          <button class="rbtn quest" data-testid="menu-quests" aria-label="Nhiệm vụ" onClick={() => go('quests')}>
            <span>Nhiệm vụ</span>
          </button>
          <button class="rbtn settings" data-testid="menu-settings" aria-label="Cài đặt" onClick={() => go('settings')}>
            <span>Cài đặt</span>
          </button>
        </div>
      )}
    </div>
  );
}

function DPad({ world }: { world: GameWorld }) {
  const [on, setOn] = useState<Direction | null>(null);
  const press = (d: Direction | null) => {
    setOn(d);
    world.setHeld(d);
  };
  const btn = (d: Direction, label: string) => (
    <button
      class={`${d} ${on === d ? 'on' : ''}`}
      aria-label={label}
      data-testid={`dpad-${d}`}
      onPointerDown={(e) => {
        (e.currentTarget as HTMLElement).setPointerCapture(e.pointerId);
        press(d);
      }}
      onPointerUp={() => press(null)}
      onPointerCancel={() => press(null)}
      onLostPointerCapture={() => on === d && press(null)}
      onContextMenu={(e) => e.preventDefault()}
    >
      {label}
    </button>
  );
  return (
    <div class="dpad">
      <div class="center" />
      {btn('up', '▲')}
      {btn('left', '◀')}
      {btn('right', '▶')}
      {btn('down', '▼')}
    </div>
  );
}

function Chat() {
  const [tab, setTab] = useState<LogTab>('all');
  const [open, setOpen] = useState(false);
  const [idle, setIdle] = useState(false);
  const all = log.value;
  const lines = all.filter((l) => tab === 'all' || l.tab === tab).slice(open ? -30 : -3);
  const last = all.length ? all[all.length - 1]!.id : 0;
  // Tự mờ khi lâu không có tin mới (không che cảnh); có tin mới hoặc mở ra thì hiện lại.
  useEffect(() => {
    setIdle(false);
    const t = setTimeout(() => setIdle(true), 7000);
    return () => clearTimeout(t);
  }, [last, open]);
  return (
    <div class={`chat ${open ? 'open' : 'min'} ${idle && !open ? 'idle' : ''}`} data-testid="chat">
      <div class="tabs">
        {LOG_TABS.filter((t) => t.id === 'all' || t.id === 'system' || t.id === 'area').map((t) => (
          <button key={t.id} class={tab === t.id ? 'on' : ''} onClick={() => (setTab(t.id), setOpen(true))}>
            {t.label}
          </button>
        ))}
        <button class="fold" aria-label={open ? 'Thu gọn chat' : 'Mở rộng chat'} onClick={() => setOpen(!open)}>
          {open ? '▾' : '▴'}
        </button>
      </div>
      <div class="body">
        <div
          class="lines"
          onClick={() => !open && setOpen(true)}
          ref={(el) => {
            if (el) el.scrollTop = el.scrollHeight;
          }}
        >
          {lines.length === 0 && <div class="muted">{tab === 'all' || tab === 'system' || tab === 'area' ? 'Chưa có tin nhắn' : 'Kênh trò chuyện sẽ mở ở bản sau'}</div>}
          {lines.map((l) => (
            <div key={l.id} class={l.tab}>
              {l.text}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
