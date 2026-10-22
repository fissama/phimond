import { useEffect, useRef } from 'preact/hooks';
import { session } from '../state/app.ts';
import { Engine } from '../render/engine.ts';
import type { Direction } from '../world/coords.ts';

const KEYS: Record<string, Direction> = {
  ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down',
  KeyA: 'left', KeyD: 'right', KeyW: 'up', KeyS: 'down',
};

/** Màn world khung S0: canvas + thông tin tối thiểu. Input/HUD thật thay ở S2/S3. */
export function World() {
  const host = useRef<HTMLDivElement>(null);
  const engine = useRef<Engine | null>(null);
  const ch = session.character.value!;
  const status = session.status.value;
  const map = session.catalog.value?.maps[ch.map_id];

  useEffect(() => {
    const e = new Engine(host.current!);
    engine.current = e;
    e.start();
    const onKey = (ev: KeyboardEvent) => {
      const dir = KEYS[ev.code];
      if (!dir || ev.repeat && session.inFlight.value >= 4) return;
      ev.preventDefault();
      if (session.inFlight.value < 4) void session.send('world.move', { direction: dir });
    };
    window.addEventListener('keydown', onKey);
    return () => {
      window.removeEventListener('keydown', onKey);
      e.dispose();
    };
  }, []);

  useEffect(() => {
    if (!engine.current || !map) return;
    const cat = session.catalog.value!;
    engine.current.loadMap({
      id: map.id,
      width: map.width,
      height: map.height || map.width,
      portals: map.portals.map((p) => ({ x: p.x, y: 0 })),
      npcs: Object.values(cat.npcs).filter((n) => n.map_id === map.id).map((n) => ({ x: n.x, y: n.y })),
    });
  }, [map?.id]);

  useEffect(() => {
    engine.current?.setPlayer({ x: ch.x, y: ch.y });
  }, [ch.x, ch.y]);

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <div ref={host} style={{ position: 'absolute', inset: 0 }} />
      <div style={hud}>
        <div data-testid="hud-name">{ch.name} · Lv {ch.level}</div>
        <div data-testid="hud-map">{map?.name ?? ch.map_id}</div>
        <div data-testid="hud-pos">x {ch.x} · y {ch.y}</div>
        <div data-testid="hud-status">{status === 'online' ? 'Trực tuyến' : status === 'connecting' ? 'Đang kết nối…' : 'Mất kết nối'}</div>
        {status === 'offline' && <button onClick={() => void session.connect().catch(() => undefined)}>Kết nối lại</button>}
        <button data-testid="logout" onClick={() => void session.logout()}>Đăng xuất</button>
      </div>
    </div>
  );
}

const hud = {
  position: 'absolute', top: 'max(8px, env(safe-area-inset-top))', left: 'max(8px, env(safe-area-inset-left))',
  display: 'flex', flexDirection: 'column', gap: 4, padding: 8, borderRadius: 6, background: 'rgba(10,14,24,0.7)', fontSize: 14,
} as const;
