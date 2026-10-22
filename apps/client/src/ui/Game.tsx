import { useEffect, useRef, useState } from 'preact/hooks';
import { Content } from '../game/content.ts';
import { GameWorld } from '../game/world.ts';
import { Engine } from '../render/engine.ts';
import { session } from '../state/app.ts';
import { closeOverlay, loading, overlay } from '../state/ui.ts';
import type { Direction } from '../world/coords.ts';
import { Battle } from './Battle.tsx';
import { Hud } from './Hud.tsx';
import { Overlays } from './Overlays.tsx';

const KEYS: Record<string, Direction> = {
  ArrowLeft: 'left', ArrowRight: 'right', ArrowUp: 'up', ArrowDown: 'down',
  KeyA: 'left', KeyD: 'right', KeyW: 'up', KeyS: 'down',
};

/** Màn chơi: canvas world + HUD + lớp phủ + trận đấu. Một GameWorld cho mỗi lần đăng nhập. */
export function Game() {
  const host = useRef<HTMLDivElement>(null);
  const [world, setWorld] = useState<GameWorld | null>(null);
  const ch = session.character.value;

  useEffect(() => {
    const cat = session.catalog.value!;
    const w = new GameWorld(new Engine(host.current!), new Content(cat), session, 'player-male');
    setWorld(w);
    void w.start();
    // Móc gỡ lỗi/E2E: chỉ có ở bản dev hoặc khi mở với ?debug.
    if (import.meta.env.DEV || location.search.includes('debug')) (window as unknown as { __phimond?: unknown }).__phimond = { world: w, session };

    const held: Direction[] = [];
    const sync = () => w.setHeld(held.at(-1) ?? null);
    const down = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement)?.tagName === 'INPUT') return;
      const d = KEYS[e.code];
      if (d) {
        e.preventDefault();
        if (!held.includes(d)) held.push(d);
        sync();
        return;
      }
      if (e.repeat) return;
      if (e.code === 'Enter' || e.code === 'Space' || e.code === 'KeyE') {
        e.preventDefault();
        if (overlay.value.kind === 'none' && !session.character.value?.battle) w.primary();
      } else if (e.code === 'Escape' || e.code === 'Backspace') {
        if (overlay.value.kind !== 'none') closeOverlay();
        else overlay.value = { kind: 'menu', page: 'root' };
      } else if (e.code === 'KeyM') {
        overlay.value = overlay.value.kind === 'none' ? { kind: 'menu', page: 'root' } : { kind: 'none' };
      }
    };
    const up = (e: KeyboardEvent) => {
      const d = KEYS[e.code];
      if (!d) return;
      const i = held.indexOf(d);
      if (i >= 0) held.splice(i, 1);
      sync();
    };
    const blur = () => {
      held.length = 0;
      sync();
    };
    window.addEventListener('keydown', down);
    window.addEventListener('keyup', up);
    window.addEventListener('blur', blur);
    return () => {
      window.removeEventListener('keydown', down);
      window.removeEventListener('keyup', up);
      window.removeEventListener('blur', blur);
      w.dispose();
    };
  }, []);

  // Chạm/click lên cảnh: chạm ngắn (không kéo) mới tính là chọn.
  const start = useRef<{ x: number; y: number; t: number } | null>(null);
  return (
    <div class="game">
      <div
        ref={host}
        data-testid="world"
        style={{ position: 'absolute', inset: 0 }}
        onPointerDown={(e) => (start.current = { x: e.clientX, y: e.clientY, t: performance.now() })}
        onPointerUp={(e) => {
          const s = start.current;
          start.current = null;
          if (!s || !world) return;
          if (Math.hypot(e.clientX - s.x, e.clientY - s.y) < 12 && performance.now() - s.t < 600) world.tap(e.clientX, e.clientY);
        }}
      />
      {world && ch && <Hud world={world} ch={ch} />}
      {world && ch && <Battle world={world} ch={ch} />}
      {world && ch && <Overlays world={world} ch={ch} />}
      {loading.value && (
        <div class="loading" data-testid="loading">
          {loading.value}
        </div>
      )}
    </div>
  );
}
