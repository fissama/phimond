import * as THREE from 'three';
import type { MapDef } from '@phimond/protocol';
import { PRESETS, type Quality } from '../state/settings.ts';
import { asset, hd2dUrl, textures } from './assets.ts';
import { animate, blobShadow, propSprite } from './sprites.ts';
import { spawnAmbient, type Ambient } from './ambient.ts';

/** Ánh sáng/không khí theo chủ đề map. */
export const THEMES: Record<string, { sky: number; fog: [number, number, number] | null; ambient: number; sun: number; sunColor: number; tint: number; ground: number }> = {
  hall: { sky: 0x1a1410, fog: null, ambient: 0.75, sun: 0.9, sunColor: 0xffd9a8, tint: 0xfff0dc, ground: 0xffffff },
  forest: { sky: 0x9cc6e8, fog: [0xb9d8c4, 26, 60], ambient: 1.0, sun: 1.3, sunColor: 0xfff2d6, tint: 0xffffff, ground: 0xffffff },
  deep_forest: { sky: 0x4f6b58, fog: [0x5d7a66, 14, 44], ambient: 0.7, sun: 0.85, sunColor: 0xd6f0d0, tint: 0xc8dcc4, ground: 0xb5c9b0 },
  city: { sky: 0x8ec3ef, fog: [0xc4dcef, 30, 70], ambient: 1.0, sun: 1.25, sunColor: 0xfff4e2, tint: 0xffffff, ground: 0xffffff },
};

/** Ký tự bố cục → nền (tile sàn). */
function floorFor(theme: string, ch: string, x: number, y: number): string {
  void x;
  void y;
  const grass = 'grass-floor-01'; // một loại cỏ để không lộ ô 4×4; đa dạng nhờ decal/cỏ/hoa
  switch (theme) {
    case 'hall':
      return ch === '=' || /[1-3KCL]/.test(ch) ? 'hall-floor-wood' : 'hall-floor-stone';
    case 'city':
      if (ch === '+') return 'city-brick-path';
      if (ch === '#' || ch === 'H') return 'city-paving-03';
      return 'city-paving-02';
    default:
      if (ch === ',') return 'dirt-floor-01';
      return grass;
  }
}

/** Ký tự bố cục → danh sách asset có thể dùng (chọn ổn định theo vị trí). */
function propsFor(theme: string, ch: string): string[] {
  const city = theme === 'city';
  const hall = theme === 'hall';
  switch (ch) {
    case 'T':
      return ['tree-large-01', 'tree-large-02', 'tree-large-03'];
    case 't':
      return city ? ['city-tree-01', 'city-tree-02'] : ['tree-small-01', 'tree-small-02'];
    case 'b':
      return city ? ['flowerpot-red', 'flowerpot-cream', 'flowerpot-violet'] : ['bush-01', 'bush-02', 'bush-03', 'fern-01'];
    case 'r':
      return ['rock-small', 'rock-medium', 'rock-large', 'stump'];
    case 'f':
      return ['flower-red', 'flower-yellow', 'flower-purple', 'flower-white', 'flower-bush'];
    case 'g':
      return ['grass-01', 'grass-02', 'grass-03', 'grass-04'];
    case 'm':
      return ['mushroom-ochre', 'mushroom-violet'];
    case 's':
      return ['market-produce'];
    case 'F':
      return ['fountain-body'];
    case 'C':
      return hall ? ['palace-marble-pillar'] : city ? ['city-carved-pillar'] : ['palace-column'];
    case 'K':
      return ['hall-bookshelf'];
    case 'L':
      return hall ? ['hall-torch'] : ['streetlamp-unlit'];
    case 'B':
      return ['bench'];
    case 'S':
      return ['palace-guard-statue'];
    case 'Q':
      return ['hall-quest-board'];
    case 'O':
      return ['city-teleport-active'];
    case 'x':
      return ['barrel', 'wooden-crate'];
    case 'A':
      return ['awning-red', 'awning-green', 'awning-blue'];
    case 'W':
      return ['well'];
    case 'n':
      return ['banner-red', 'banner-blue'];
    case 'k':
      return ['handcart'];
    case '1':
      return ['summon-pedestal-01-dormant'];
    case '2':
      return ['summon-pedestal-02-dormant'];
    case '3':
      return ['summon-pedestal-03-dormant'];
    // Đơn 10.
    case 'P':
      return ['city-lion-fountain'];
    case 'V':
      return ['city-vendor-cart'];
    case 'X':
      return ['city-sacks'];
    case 'Y':
      return ['city-topiary'];
    case 'G':
      return ['city-hanging-sign'];
    case 'J':
      return ['palace-lion-r'];
    case 'j':
      return ['palace-lion-l'];
    case 'Z':
      return ['palace-flagpole'];
    default:
      return [];
  }
}

const DECOR = new Set(['f', 'g', 'm']);
/** Asset đơn 10 chưa có (chưa đồng bộ) → dùng đồ cũ tương đương. */
const FALLBACK: Record<string, string> = {
  'city-lion-fountain': 'well',
  'city-vendor-cart': 'handcart',
  'city-sacks': 'wooden-crate',
  'city-topiary': 'flowerpot-cream',
  'city-hanging-sign': 'streetlamp-unlit',
  'palace-lion-r': 'palace-guard-statue',
  'palace-lion-l': 'palace-guard-statue',
  'palace-flagpole': 'banner-blue',
};
const hash = (x: number, y: number) => {
  let h = (x * 374761393 + y * 668265263) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
};

export interface BuiltScene {
  group: THREE.Group;
  /** Đối tượng bấm được (bệ đá, trụ) — userData {kind, id}. */
  pickables: THREE.Object3D[];
  update(dt: number, player?: THREE.Vector3 | null): void;
  dispose(): void;
}

/** Dựng cảnh HD-2D từ bố cục map (layout) và kit đã duyệt. Lưới đi là của server; cảnh chỉ để nhìn. */
export async function buildScene(map: MapDef, quality: Quality): Promise<BuiltScene> {
  const P = PRESETS[quality];
  const theme = THEMES[map.theme] ? map.theme : 'forest';
  const T = THEMES[theme]!;
  const group = new THREE.Group();
  const animated: THREE.Object3D[] = [];
  const pickables: THREE.Object3D[] = [];
  const disposables: { dispose(): void }[] = [];
  const W = map.width;
  const H = map.height || map.width;
  const layout = map.layout.length === H ? map.layout : Array.from({ length: H }, () => '.'.repeat(W));
  const real = P.shadows === 'real';

  // --- Mặt đất: gộp ô theo loại sàn thành một mesh mỗi texture.
  const byFloor = new Map<string, number[]>();
  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++) {
      const id = floorFor(theme, layout[y]![x] ?? '.', x, y);
      if (!byFloor.has(id)) byFloor.set(id, []);
      byFloor.get(id)!.push(x, y);
    }
  const groundJobs = [...byFloor.entries()].map(async ([id, cells]) => {
    const tex = asset(id) ? await textures.get(hd2dUrl(id), { repeat: true }) : null;
    const pos: number[] = [];
    const uv: number[] = [];
    for (let i = 0; i < cells.length; i += 2) {
      const x = cells[i]!;
      const y = cells[i + 1]!;
      const quad = [[x, y], [x, y + 1], [x + 1, y + 1], [x, y], [x + 1, y + 1], [x + 1, y]] as const;
      for (const [qx, qz] of quad) {
        pos.push(qx, 0, qz);
        uv.push(qx / 4, -qz / 4);
      }
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    geo.computeVertexNormals();
    const darken = theme === 'hall' && id === 'hall-floor-stone' ? 0x4a4038 : T.ground;
    const mat = P.shadows === 'none'
      ? new THREE.MeshBasicMaterial({ map: tex, color: tex ? darken : 0x6a8a58 })
      : new THREE.MeshLambertMaterial({ map: tex, color: tex ? darken : 0x6a8a58 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.receiveShadow = real;
    mesh.userData.ground = true;
    group.add(mesh);
    disposables.push(geo, mat);
  });

  // --- Vật thể theo ký tự bố cục.
  const propJobs: Promise<void>[] = [];
  const place = (id: string, x: number, y: number, opts: { decor?: boolean; pick?: Record<string, unknown>; jitter?: boolean } = {}) => {
    propJobs.push(
      (async () => {
        if (id.startsWith('tree-large-')) {
          const trunk = await propSprite(id + '-trunk', { tint: T.tint, castShadow: real });
          const canopy = await propSprite(id + '-canopy', { tint: T.tint, castShadow: real });
          if (!trunk) return;
          const g = new THREE.Group();
          g.add(trunk);
          if (canopy) {
            const th = (asset(id + '-trunk')?.px[1] ?? 236) / 128;
            canopy.position.set(0, th * 0.62, -0.05);
            canopy.rotation.x = trunk.rotation.x;
            g.add(canopy);
            if (asset(id + '-canopy')?.sway) {
              canopy.userData.sway = hash(x, y) * 6;
              animated.push(canopy);
            }
          }
          if (P.shadows === 'blob') g.add(blobShadow(0.9));
          g.position.set(x + 0.5, 0, y + 0.6);
          group.add(g);
          return;
        }
        if (!asset(id) && FALLBACK[id]) id = FALLBACK[id]!;
        const s = await propSprite(id, { tint: T.tint, castShadow: real && !opts.decor });
        if (!s) return;
        if (asset(id)?.sway) {
          s.userData.sway = hash(x, y) * 6;
          if (!s.userData.anim) animated.push(s);
        }
        const jx = opts.jitter ? (hash(x, y) - 0.5) * 0.5 : 0;
        const jz = opts.jitter ? (hash(y, x) - 0.5) * 0.4 : 0;
        s.position.set(x + 0.5 + jx, 0, y + 0.55 + jz);
        if (opts.pick) {
          s.userData = { ...s.userData, ...opts.pick };
          pickables.push(s);
        }
        if (s.userData.anim) animated.push(s);
        group.add(s);
        if (P.shadows === 'blob' && !opts.decor) {
          const b = blobShadow(Math.min(1.1, (asset(id)?.px[0] ?? 128) / 256));
          b.position.set(s.position.x, 0.02, s.position.z);
          group.add(b);
        }
      })(),
    );
  };

  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++) {
      const ch = layout[y]![x] ?? '.';
      const opts = propsFor(theme, ch);
      if (opts.length === 0) continue;
      const decor = DECOR.has(ch);
      if (decor && hash(x, y) > P.decor) continue;
      const pick = /[1-3]/.test(ch) ? { kind: 'pedestal', index: Number(ch) - 1 } : ch === 'O' ? { kind: 'pillar' } : undefined;
      place(opts[Math.floor(hash(x, y) * opts.length)]!, x, y, { decor, jitter: decor || ch === 'b' || ch === 'r', ...(pick ? { pick } : {}) });
      if (ch === 'A') place(['market-produce', 'market-cloth', 'market-weapons'][Math.floor(hash(y, x) * 3)]!, x, y + 0.35);
      if (ch === 'F' && P.fx) propJobs.push(fx('fountain-water', x + 0.5, y + 0.3, 1.2));
      if (ch === 'O' && P.fx) propJobs.push(fx('city-teleport-ring', x + 0.5, y + 0.6, 0.05));
    }

  // Rìa rừng: cây/bụi dày trên các ô chặn kề vùng đi được để không lộ khoảng trống.
  if (theme === 'forest' || theme === 'deep_forest') {
    for (let y = 0; y < H; y++)
      for (let x = 0; x < W; x++) {
        if (layout[y]![x] !== '#') continue;
        const nearOpen = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => /[.,fgm]/.test(layout[y + dy!]?.[x + dx!] ?? ''));
        const r = hash(x, y);
        if (nearOpen && r < 0.55) place(r < 0.2 ? 'tree-large-0' + (1 + Math.floor(r * 15)) : r < 0.4 ? 'tree-small-0' + (1 + (x % 2)) : 'bush-0' + (1 + (y % 3)), x, y, { jitter: true });
        else if (!nearOpen && r < 0.12) place('tree-large-0' + (1 + (x % 3)), x, y);
      }
    // Trang trí mặt đất (đặt nằm): lá rụng, đá cuội, rêu.
    const decals = ['fallen-leaves-01', 'fallen-leaves-02', 'pebbles-01', 'moss-patch-01', 'moss-patch-02'];
    for (let y = 0; y < H; y++)
      for (let x = 0; x < W; x++)
        if (/[.,]/.test(layout[y]![x] ?? '') && hash(x * 3, y * 5) < 0.06 * P.decor) propJobs.push(decal(decals[Math.floor(hash(y, x) * decals.length)]!, x + 0.5, y + 0.5));
    if (P.fx && theme === 'deep_forest')
      for (let i = 0; i < 10; i++) propJobs.push(fx('firefly', 4 + hash(i, 9) * (W - 8), 3 + hash(9, i) * (H - 6), 0.8 + hash(i, i) * 0.8));
  }

  // Viền ngoài map: nền kéo dài + cây (rừng) để camera không lộ khoảng trống ở mép.
  const skirtFloor = theme === 'hall' ? null : theme === 'city' ? 'city-paving-03' : 'grass-floor-01';
  if (skirtFloor && asset(skirtFloor)) {
    propJobs.push(
      (async () => {
        const tex = await textures.get(hd2dUrl(skirtFloor), { repeat: true });
        const M = 24;
        const geo = new THREE.PlaneGeometry(W + 2 * M, H + 2 * M);
        const uv = geo.getAttribute('uv') as THREE.BufferAttribute;
        for (let i = 0; i < uv.count; i++) uv.setXY(i, (uv.getX(i) * (W + 2 * M)) / 4, (uv.getY(i) * (H + 2 * M)) / 4);
        const shade = theme === 'deep_forest' ? T.ground : theme === 'city' ? 0xc8c0b0 : 0xe4ebdc;
        const mat = P.shadows === 'none' ? new THREE.MeshBasicMaterial({ map: tex, color: shade }) : new THREE.MeshLambertMaterial({ map: tex, color: shade });
        const m = new THREE.Mesh(geo, mat);
        m.rotation.x = -Math.PI / 2;
        m.position.set(W / 2, -0.02, H / 2);
        group.add(m);
        disposables.push(geo, mat);
      })(),
    );
  }
  if (theme === 'forest' || theme === 'deep_forest') {
    const ring = 6;
    for (let y = -ring; y < H + ring; y++)
      for (let x = -ring; x < W + ring; x++) {
        if (x >= 0 && y >= 0 && x < W && y < H) continue;
        if (y >= H) continue; // phía camera: để trống cho dễ nhìn
        const r = hash(x + 101, y + 57);
        if (r < 0.2 * Math.max(0.5, P.decor)) place(r < 0.12 ? 'tree-large-0' + (1 + (Math.abs(x + y) % 3)) : 'tree-small-0' + (1 + (Math.abs(x) % 2)), x, y, { jitter: true });
      }
  }

  // Điểm nhấn sàn.
  if (theme === 'hall') propJobs.push(decal('summon-floor-emblem', W / 2, 5.5, 1.2));
  if (map.id === 'city_square') propJobs.push(decal('city-plaza-medallion', 20, 16, 1.4));

  // Mặt tiền nhà (H) theo map.facades "x,y" → asset; thành phố: lấp kín dãy nhà phía trên (không để khe trống).
  const facadeSpans: [number, number][] = [];
  for (const [k, id] of Object.entries(map.facades ?? {})) {
    const [fx_, fy] = k.split(',').map(Number);
    if (!Number.isFinite(fx_) || !Number.isFinite(fy)) continue;
    place(id, fx_!, fy! + 0.4);
    const w = asset(id)?.world?.[0] ?? 5;
    facadeSpans.push([fx_! + 0.5 - w / 2, fx_! + 0.5 + w / 2]);
  }
  if (theme === 'city') dressCity();

  function dressCity(): void {
    const isGate = map.id === 'city_palace_gate';
    const has = (id: string) => !!asset(id);
    const wOf = (id: string, d = 4) => asset(id)?.world?.[0] ?? d;
    // 1) Dãy nhà liền: lấp khoảng giữa các mặt tiền đã đặt. Đơn 10: thêm 6 kiểu nhà + mảnh nối (ngõ vòm,
    //    cột ống máng, tường hộp hoa) để không lặp; Hoàng Môn dùng tường thành có lỗ châu mai.
    const houses = isGate
      ? ['palace-crenel-wall', 'palace-wall-section', 'palace-crenel-wall'].filter(has)
      : ['city-facade-inn', 'city-facade-warehouse', 'city-facade-bakery', 'city-facade-corner', 'city-facade-belltower', 'city-facade-townhouse', 'city-facade-artisan'].filter(has);
    const connectors = isGate ? ['palace-tower'] : ['city-alley-arch', 'city-wall-flowerbox', 'city-pillar-drainpipe'].filter(has);
    const fillerHouses = houses.length ? houses : ['city-facade-townhouse', 'city-facade-artisan', 'city-facade-shop', 'city-facade-guild'];
    const fillerConn = connectors.length ? connectors : ['palace-tower'];
    const spans = facadeSpans.sort((p, q) => p[0] - q[0]);
    const gaps: [number, number][] = [];
    let cur = -4;
    for (const [l, r] of spans) {
      if (l - cur > 0.6) gaps.push([cur, l]);
      cur = Math.max(cur, r);
    }
    if (W + 4 - cur > 0.6) gaps.push([cur, W + 4]);
    let k = 0;
    let c = 0;
    for (const [l, r] of gaps) {
      let x = l;
      while (r - x > 0.5) {
        const room = r - x;
        // Nhà nếu đủ chỗ, không thì mảnh nối hẹp vừa nhất.
        let id = fillerHouses[k % fillerHouses.length]!;
        if (wOf(id) > room + 0.6) {
          const fits = fillerConn.filter((cid) => wOf(cid, 2) <= room + 0.5);
          id = fits.length ? fits[c++ % fits.length]! : fillerConn.reduce((m, cid) => (wOf(cid, 2) < wOf(m, 2) ? cid : m), fillerConn[0]!);
        } else k++;
        const w = wOf(id, 2);
        // Nhà lấp đứng lùi sau một chút để mặt tiền chính (có cửa) nổi lên trước.
        place(id, x + w / 2 - 0.5, 1.15);
        x += w - 0.15;
      }
    }
    // 2) Dải mái lớp giữa sau dãy nhà (chiều sâu giữa phố và nền xa).
    if (P.backdrop && has('city-roofline-mid')) {
      const rw = wOf('city-roofline-mid', 15);
      for (let x = -6; x < W + 6; x += rw - 0.05)
        propJobs.push(
          (async () => {
            const m = await propSprite('city-roofline-mid', { tint: 0xe6ecf2 });
            if (!m) return;
            m.position.set(x + rw / 2, 2.55, -0.35);
            group.add(m);
          })(),
        );
    }
    // 3) Viền dưới: vườn hoa (phố) / bồn cây dài (Hoàng Môn); hai mép bên có cây, chậu, cờ.
    const border = isGate && has('palace-long-planter') ? 'palace-long-planter' : 'city-garden-border';
    const gb = wOf(border, 4.5);
    for (let x = -1; x < W + 1; x += gb - 0.1) place(border, x + gb / 2 - 0.5, H - 0.75);
    for (const side of [0, W - 1]) {
      for (let y = 2; y < H - 1; y++) {
        const open = /[:+,.]/.test(layout[y]![side] ?? '#');
        if (open) continue;
        if (y % 3 === 0) place(hash(side, y) < 0.5 ? 'city-tree-01' : 'city-tree-02', side + (side === 0 ? -0.3 : 0.3), y);
        else if (y % 3 === 2) place(isGate ? 'palace-guard-booth' : 'flowerpot-' + ['red', 'cream', 'violet'][y % 3]!, side + (side === 0 ? -0.2 : 0.2), y);
      }
      for (let y = 2; y < H - 1; y++) {
        const open = /[:+,.]/.test(layout[y]![side] ?? '#');
        const prevOpen = /[:+,.]/.test(layout[y - 1]?.[side] ?? '#');
        const nextOpen = /[:+,.]/.test(layout[y + 1]?.[side] ?? '#');
        if (!open && (prevOpen || nextOpen)) place(side === 0 ? 'banner-blue' : 'banner-red', side, y);
      }
    }
    // 4) Thảm đỏ trên lối gạch ở Hoàng Môn.
    if (isGate) for (let x = 9; x < 18; x += 3.3) propJobs.push(decal('palace-carpet-strip', x + 1.6, 6.5, 1));
    // 5) Dây cờ trên khu chợ, hàng rào sắt cạnh lối ra.
    if (!isGate && has('city-bunting')) place('city-bunting', 19.5, 8.75, { decor: true });
    // 6) Decal mặt đất rải thưa trên đá lát (không phủ lối gạch).
    const decals = ['decal-cracks', 'decal-drain', 'decal-puddle', 'decal-petals', 'decal-hopscotch', 'decal-ruts'].filter(has);
    if (decals.length) {
      const fixed: [string, number, number][] = isGate
        ? [['decal-cracks', 4.5, 6.5], ['decal-drain', 21.5, 4.5], ['decal-petals', 3.5, 8.6], ['decal-puddle', 20.5, 7.4]]
        : [['decal-hopscotch', 22.5, 6.2], ['decal-drain', 10.5, 4.5], ['decal-puddle', 6.5, 6.6], ['decal-ruts', 27.0, 9.2],
           ['decal-cracks', 15.0, 8.4], ['decal-petals', 12.5, 3.6], ['decal-cracks', 25.5, 4.4], ['decal-petals', 29.3, 8.4]];
      for (const [id, x, z] of fixed) if (has(id) && hash(x * 7, z * 3) < 0.35 + P.decor) propJobs.push(decal(id, x, z, 1));
    }
  }

  // Tường điện (hall): dải tường ở mép trên.
  if (theme === 'hall')
    for (let x = 1; x < W - 1; x += 3) place('hall-wall-stone', x, 1.6);

  // Nền xa (dải 64 px/đơn vị) sau mép trên map.
  if (P.backdrop && map.backdrop && asset(map.backdrop)) {
    propJobs.push(
      (async () => {
        const a = asset(map.backdrop!)!;
        const tex = (await textures.get(hd2dUrl(map.backdrop!), { repeat: true })).clone();
        const wWorld = a.px[0] / 64;
        const hWorld = a.px[1] / 64;
        const span = W + 30;
        tex.repeat.set(span / wWorld, 1);
        tex.wrapT = THREE.ClampToEdgeWrapping;
        tex.needsUpdate = true;
        const geo = new THREE.PlaneGeometry(span, hWorld);
        const mat = new THREE.MeshBasicMaterial({ map: tex, alphaTest: 0.5, color: theme === 'deep_forest' ? 0x9db39f : 0xdde6ee, fog: false });
        const m = new THREE.Mesh(geo, mat);
        m.position.set(W / 2, hWorld / 2 - 0.8, -3.5);
        group.add(m);
        disposables.push(geo, mat);
      })(),
    );
  }

  async function decal(id: string, x: number, z: number, scale = 1) {
    const a = asset(id);
    if (!a) return;
    const tex = await textures.get(hd2dUrl(id));
    const geo = new THREE.PlaneGeometry((a.px[0] / 128) * scale, (a.px[1] / 128) * scale);
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, color: T.ground });
    const m = new THREE.Mesh(geo, mat);
    m.rotation.x = -Math.PI / 2;
    m.position.set(x, 0.01, z);
    m.renderOrder = 0;
    group.add(m);
    disposables.push(geo, mat);
  }

  async function fx(id: string, x: number, z: number, y: number) {
    const s = await propSprite(id, { tilt: -0.42 });
    if (!s) return;
    s.position.set(x, y - 0.5, z);
    animated.push(s);
    group.add(s);
  }

  await Promise.all([...groundJobs, ...propJobs]);
  // Sự sống trong thành nạp sau khi cảnh đã sẵn sàng: không làm chậm lúc vào map.
  const ambient: Ambient[] = [];
  if (theme === 'city') void spawnAmbient(map, group, P.shadows === 'blob', P.decor).then((a) => ambient.push(...a)).catch(() => {});

  let time = 0;
  return {
    group,
    pickables,
    update(dt: number, player?: THREE.Vector3 | null) {
      time += dt;
      for (const a of ambient) a.update(dt, player ?? null);
      for (const o of animated) {
        animate(o, dt);
        if (o.userData.sway !== undefined) o.rotation.z = Math.sin(time * 0.8 + (o.userData.sway as number)) * 0.015;
      }
    },
    dispose() {
      group.traverse((o) => {
        const m = o as THREE.Mesh;
        if (m.isMesh) {
          m.geometry?.dispose();
          const mat = m.material as THREE.Material;
          mat.dispose();
          (m.customDepthMaterial as THREE.Material | undefined)?.dispose();
        }
      });
      disposables.forEach((d) => d.dispose());
    },
  };
}

