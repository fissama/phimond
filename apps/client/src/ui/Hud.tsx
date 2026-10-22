import { useState } from 'preact/hooks';
import type { Character } from '@phimond/protocol';
import { currentMap, type GameWorld } from '../game/world.ts';
import { viName } from '../game/content.ts';
import { settings } from '../state/settings.ts';
import { closeOverlay, log, LOG_TABS, overlay, toasts, type LogTab } from '../state/ui.ts';
import type { Direction } from '../world/coords.ts';
import { session } from '../state/app.ts';
import { PetPortrait } from './PetArt.tsx';

const pct = (a: number, b: number) => `${Math.max(0, Math.min(100, (a / Math.max(1, b)) * 100))}%`;

/** Bố cục HUD gốc (P01-R09): Lv + pet trái trên, menu phải, D-pad trái dưới, Chọn/Trở về phải dưới, chat 6 tab giữa dưới. */
export function Hud({ world, ch }: { world: GameWorld; ch: Character }) {
  const pet = ch.pets.find((p) => p.id === ch.active_pet_id && !p.retired);
  const map = currentMap.value;
  const status = session.status.value;
  return (
    <>
      <div class="hud-status panel" data-testid="hud-status-panel">
        {pet ? <PetPortrait species={pet.species_id} /> : <div class="portrait" />}
        <div>
          <div class="who" data-testid="hud-name">
            <span class="lv">Lv {ch.level}</span>
            {ch.name}
          </div>
          <div class="sub" data-testid="hud-gold">
            {ch.gold} vàng{pet ? ` · ${viName(pet.name)} Lv ${pet.level}` : ' · chưa có linh thú'}
          </div>
          {pet && (
            <div class="bars">
              <div class="bar hp" title={`HP ${pet.hp}/${pet.max_hp}`}>
                <i style={{ width: pct(pet.hp, pet.max_hp) }} />
              </div>
              <div class="bar mp" title={`MP ${pet.mp}/${pet.max_mp}`}>
                <i style={{ width: pct(pet.mp, pet.max_mp) }} />
              </div>
            </div>
          )}
        </div>
      </div>

      {map && (
        <div class="hud-map panel" data-testid="hud-map">
          {map.name}
        </div>
      )}
      <span data-testid="hud-pos" style={{ position: 'absolute', left: -9999 }}>
        {ch.map_id} x {ch.x} · y {ch.y}
      </span>

      {status !== 'online' && (
        <div class="hud-net panel" data-testid="hud-status">
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
        <button class="btn" data-testid="menu-pets" onClick={() => (overlay.value = { kind: 'menu', page: 'pets' })}>
          Linh thú
        </button>
        <button class="btn" data-testid="menu-bag" onClick={() => (overlay.value = { kind: 'menu', page: 'bag' })}>
          Túi đồ
        </button>
        <button class="btn" data-testid="menu-quests" onClick={() => (overlay.value = { kind: 'menu', page: 'quests' })}>
          Nhiệm vụ
        </button>
        <button class="btn" data-testid="menu-open" onClick={() => (overlay.value = { kind: 'menu', page: 'root' })}>
          Menu
        </button>
      </div>

      {settings.value.dpad && <DPad world={world} />}

      <div class="hud-actions">
        <button class="round b" data-testid="btn-back" onClick={() => (overlay.value.kind === 'none' ? (overlay.value = { kind: 'menu', page: 'root' }) : closeOverlay())}>
          Trở về
        </button>
        <button class="round a" data-testid="btn-select" onClick={() => world.primary()}>
          Chọn
        </button>
      </div>

      <Chat />
      <div class="toasts" data-testid="toasts">
        {toasts.value.map((t) => (
          <div key={t.id} class="toast panel">
            {t.text}
          </div>
        ))}
      </div>
    </>
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
      {btn('up', '▲')}
      {btn('left', '◀')}
      {btn('right', '▶')}
      {btn('down', '▼')}
    </div>
  );
}

function Chat() {
  const [tab, setTab] = useState<LogTab>('all');
  const [min, setMin] = useState(false);
  const lines = log.value.filter((l) => tab === 'all' || l.tab === tab).slice(-30);
  return (
    <div class={`chat panel ${min ? 'min' : ''}`} data-testid="chat">
      <div class="tabs">
        {LOG_TABS.map((t) => (
          <button key={t.id} class={tab === t.id ? 'on' : ''} onClick={() => (tab === t.id ? setMin(!min) : setTab(t.id))}>
            {t.label}
          </button>
        ))}
      </div>
      <div
        class="lines"
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
  );
}
