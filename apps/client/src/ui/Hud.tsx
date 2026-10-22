import { useEffect, useRef, useState } from 'preact/hooks';
import type { Character } from '@phimond/protocol';
import { currentMap, interactHint, type GameWorld } from '../game/world.ts';
import { viName } from '../game/content.ts';
import { currentGoal } from '../game/goal.ts';
import { settings } from '../state/settings.ts';
import { battleResultOpen, closeOverlay, log, LOG_TABS, overlay, toasts, type LogTab } from '../state/ui.ts';
import type { Direction } from '../world/coords.ts';
import { session } from '../state/app.ts';
import { PetPortrait } from './PetArt.tsx';

const pct = (a: number, b: number) => `${Math.max(0, Math.min(100, (a / Math.max(1, b)) * 100))}%`;

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
  return (
    <div class={`hud ${compact ? 'compact' : ''} ${inBattle ? 'in-battle' : ''}`}>
      <div class="hud-status" data-testid="hud-status-panel">
        <div class="ring">
          {pet ? <PetPortrait species={pet.species_id} /> : <div class="portrait" />}
          <div class="badge" title="Cấp nhân vật">{ch.level}</div>
        </div>
        <div class="plate">
          <div class="who" data-testid="hud-name">
            {ch.name}
          </div>
          <div class="sub" data-testid="hud-gold">
            <i class="coin" />
            {ch.gold}
            {pet ? ` · ${viName(pet.name)} Lv ${pet.level}` : ' · chưa có linh thú'}
          </div>
          {pet && (
            <div class="bars">
              <div class="uibar hp" title={`HP ${pet.hp}/${pet.max_hp}`}>
                <i style={{ width: pct(pet.hp, pet.max_hp) }} />
              </div>
              <div class="uibar mp" title={`MP ${pet.mp}/${pet.max_mp}`}>
                <i style={{ width: pct(pet.mp, pet.max_mp) }} />
              </div>
            </div>
          )}
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

      <div class="hud-menu">
        <button class="rbtn pet" data-testid="menu-pets" aria-label="Linh thú" onClick={() => (overlay.value = { kind: 'menu', page: 'pets' })}>
          <span>Linh thú</span>
        </button>
        <button class="rbtn bag" data-testid="menu-bag" aria-label="Túi đồ" onClick={() => (overlay.value = { kind: 'menu', page: 'bag' })}>
          <span>Túi đồ</span>
        </button>
        <button class="rbtn quest" data-testid="menu-quests" aria-label="Nhiệm vụ" onClick={() => (overlay.value = { kind: 'menu', page: 'quests' })}>
          <span>Nhiệm vụ</span>
        </button>
        <button class="rbtn settings" data-testid="menu-open" aria-label="Menu" onClick={() => (overlay.value = { kind: 'menu', page: 'root' })}>
          <span>Menu</span>
        </button>
      </div>

      {settings.value.dpad && <DPad world={world} />}

      <div class="hud-actions">
        <button class="round b" data-testid="btn-back" onClick={() => (overlay.value.kind === 'none' ? (overlay.value = { kind: 'menu', page: 'root' }) : closeOverlay())}>
          Trở về
        </button>
        <button class={`round a ${hint ? 'ready' : ''}`} data-testid="btn-select" onClick={() => world.primary()}>
          {hint ?? 'Chọn'}
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

/** Bản đồ nhỏ: ô đi được, cổng, NPC và vị trí người chơi (vẽ từ lưới đi được, không cần ảnh). */
function Minimap({ world, ch }: { world: GameWorld; ch: Character }) {
  const ref = useRef<HTMLCanvasElement>(null);
  const map = currentMap.value!;
  const grid = world.content.grid(map.id);
  useEffect(() => {
    const cv = ref.current;
    if (!cv || !grid) return;
    const k = Math.max(3, Math.min(8, Math.floor(160 / Math.max(grid.w, grid.h))));
    cv.width = grid.w * k;
    cv.height = grid.h * k;
    const g = cv.getContext('2d')!;
    g.fillStyle = '#0d1420';
    g.fillRect(0, 0, cv.width, cv.height);
    for (let y = 0; y < grid.h; y++)
      for (let x = 0; x < grid.w; x++)
        if (grid.walkable(x, y)) {
          g.fillStyle = (x + y) % 2 ? '#3c4a3a' : '#435342';
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
    dot(ch.x, ch.y, '#ffffff', Math.max(4, k + 1));
  }, [map.id, ch.x, ch.y, grid]);
  return (
    <div class="hud-minimap" data-testid="hud-minimap" aria-label="Bản đồ nhỏ">
      <canvas ref={ref} />
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
  const lines = all.filter((l) => tab === 'all' || l.tab === tab).slice(open ? -30 : -2);
  const last = all.length ? all[all.length - 1]!.id : 0;
  // Tự mờ khi lâu không có tin mới (không che cảnh); có tin mới hoặc mở ra thì hiện lại.
  useEffect(() => {
    setIdle(false);
    const t = setTimeout(() => setIdle(true), 7000);
    return () => clearTimeout(t);
  }, [last, open]);
  return (
    <div class={`chat ${open ? 'open' : 'min'} ${idle && !open ? 'idle' : ''}`} data-testid="chat">
      {open && (
        <div class="tabs">
          {LOG_TABS.map((t) => (
            <button key={t.id} class={tab === t.id ? 'on' : ''} onClick={() => setTab(t.id)}>
              {t.label}
            </button>
          ))}
          <button class="fold" aria-label="Thu gọn chat" onClick={() => setOpen(false)}>
            ▾
          </button>
        </div>
      )}
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
        {!open && <span class="expand" aria-hidden="true">▴ Trò chuyện</span>}
      </div>
    </div>
  );
}
