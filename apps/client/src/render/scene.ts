import * as THREE from 'three';
import type { MapDef } from '@phimond/protocol';
import { PRESETS, type Quality } from '../state/settings.ts';
import { asset, hd2dUrl, textures } from './assets.ts';
import { animate, blobShadow, propSprite } from './sprites.ts';
import { spawnAmbient, type Ambient } from './ambient.ts';
import type { Light } from './daylight.ts';
import { makeAtmosphere, type Lamp } from './atmosphere.ts';
import { makeLightMask } from './lightmask.ts';
import { paintedShadow, type ShadowKind } from './shadows.ts';
import { buildForeground, type Foreground, type FgItem } from './foreground.ts';

/** Ánh sáng/không khí theo chủ đề map. */
export const THEMES: Record<string, { indoor?: boolean; sky: number; fog: [number, number, number] | null; ambient: number; sun: number; sunColor: number; tint: number; ground: number; camBias?: number }> = {
  // Sảnh là sân đá mở nhìn ra thành phố (bản vẽ lại 2026-10-28): ánh sáng ban ngày cố định, không còn nội thất gỗ tối.
  hall: { indoor: true, sky: 0x2f7be8, fog: null, ambient: 0.95, sun: 1.1, sunColor: 0xfff4de, tint: 0xffffff, ground: 0xffffff, camBias: -1.5 },
  forest: { sky: 0x9cc6e8, fog: [0xb9d8c4, 26, 60], ambient: 1.0, sun: 1.3, sunColor: 0xfff2d6, tint: 0xffffff, ground: 0xffffff },
  deep_forest: { sky: 0x4f6b58, fog: [0x5d7a66, 14, 44], ambient: 0.7, sun: 0.85, sunColor: 0xd6f0d0, tint: 0xc8dcc4, ground: 0xb5c9b0 },
  city: { sky: 0x8ec3ef, fog: [0xc4dcef, 30, 70], ambient: 1.0, sun: 1.25, sunColor: 0xfff4e2, tint: 0xffffff, ground: 0xffffff },
};

/** Ký tự bố cục → nền (tile sàn). */
function floorFor(theme: string, ch: string, x: number, y: number): string {
  const grass = 'grass-floor-01'; // một loại cỏ để không lộ ô 4×4; đa dạng nhờ decal/cỏ/hoa
  switch (theme) {
    case 'hall':
      void ch;
      // Hai mẫu sàn đá xen kẽ theo khối 4×4 ô (hai mẫu khớp biên với nhau) để phá nhịp lặp.
      return (((x >> 2) + (y >> 2)) & 1) === 0 ? 'hall-floor-marble' : 'hall-floor-marble-b';
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
      return hall ? ['hall-column'] : city ? ['city-carved-pillar'] : ['palace-column'];
    case 'K':
      return hall ? ['hall-lectern'] : ['hall-bookshelf'];
    case 'L':
      return hall ? ['hall-brazier'] : ['streetlamp-unlit'];
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
      return ['summon-pedestal-01'];
    case '2':
      return ['summon-pedestal-02'];
    case '3':
      return ['summon-pedestal-03'];
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
  /** Có vật ở lớp tiền cảnh (cần bước làm mờ trong hậu kỳ). */
  readonly hasFg: boolean;
  /** Gốc của tiền cảnh: engine gắn vào camera. */
  fgRoot: THREE.Group | null;
  update(dt: number, player?: THREE.Vector3 | null, cam?: THREE.PerspectiveCamera): void;
  /** Đèn lồng/tia nắng/bụi theo giờ trong ngày. */
  setLight(l: Light): void;
  dispose(): void;
}

/** Dựng cảnh HD-2D từ bố cục map (layout) và kit đã duyệt. Lưới đi là của server; cảnh chỉ để nhìn. */
export async function buildScene(map: MapDef, quality: Quality): Promise<BuiltScene> {
  const P = PRESETS[quality];
  const theme = THEMES[map.theme] ? map.theme : 'forest';
  const T = THEMES[theme]!;
  const group = new THREE.Group();
  const animated: THREE.Object3D[] = [];
  const lamps: Lamp[] = [];
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
  // Vật cao phía trước người chơi (cây, nhà) mờ đi khi che nhân vật, như HD-2D (đánh giá: nhân vật mất sau tán cây).
  const occluders: { obj: THREE.Object3D; mats: THREE.MeshBasicMaterial[]; hw: number; h: number; cur: number }[] = [];
  const addOccluder = (obj: THREE.Object3D, hw: number, h: number) => {
    const mats: THREE.MeshBasicMaterial[] = [];
    obj.traverse((o) => {
      const m = (o as THREE.Mesh).material as THREE.MeshBasicMaterial | undefined;
      if ((o as THREE.Mesh).isMesh && m && m.map) mats.push(m);
    });
    if (mats.length) occluders.push({ obj, mats, hw, h, cur: 1 });
  };
  const place = (id: string, x: number, y: number, opts: { decor?: boolean; pick?: Record<string, unknown>; jitter?: boolean; scaleX?: number } = {}) => {
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
          if (P.shadows === 'blob') {
            const sh = await paintedShadow('canopy', Math.min(3.2, (asset(id + '-canopy')?.px[0] ?? 256) / 128 * 0.95));
            g.add(sh ?? blobShadow(0.9));
          }
          g.position.set(x + 0.5, 0, y + 0.6);
          group.add(g);
          const cw = (asset(id + '-canopy')?.px[0] ?? 256) / 128;
          const th = (asset(id + '-trunk')?.px[1] ?? 236) / 128;
          addOccluder(g, cw * 0.5, th * 0.62 + (asset(id + '-canopy')?.px[1] ?? 256) / 128);
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
        if (opts.scaleX) s.scale.x *= opts.scaleX;
        if (opts.pick) {
          s.userData = { ...s.userData, ...opts.pick };
          pickables.push(s);
        }
        if (s.userData.anim) animated.push(s);
        group.add(s);
        const ah = (asset(id)?.px[1] ?? 0) / 128;
        if (ah >= 1.8 && !opts.decor) addOccluder(s, ((asset(id)?.px[0] ?? 128) / 128) * 0.45, ah);
        if (P.shadows === 'blob' && !opts.decor) {
          const aw = (asset(id)?.px[0] ?? 128) / 128;
          const boxy = /market|awning|cart|bench|well|fountain|crate|barrel|sack|stall|booth|bookshelf/.test(id);
          const kind: ShadowKind = boxy ? 'rect' : ah >= 1.4 ? 'large' : 'small';
          const sh = await paintedShadow(kind, boxy ? Math.min(3.2, aw * 0.95) : Math.min(2.2, Math.max(0.8, aw * 0.8)));
          const b = sh ?? blobShadow(Math.min(1.1, aw / 2));
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
      const pickId = theme === 'hall' && ch === 'K' && x > W / 2 ? 'hall-globe' : opts[Math.floor(hash(x, y) * opts.length)]!;
      place(pickId, x, y, { decor, jitter: decor || ch === 'b' || ch === 'r', ...(pick ? { pick } : {}) });
      if (ch === 'L' && P.fx) {
        const lid = opts[0]!;
        const a = asset(lid);
        const h = a ? a.px[1] / 128 : 2;
        lamps.push({ x: x + 0.5, y: h * (theme === 'hall' ? 0.5 : 0.92), z: y + 0.5, size: theme === 'hall' ? 1.3 : 3.2, color: theme === 'hall' ? 0xffa850 : 0xffc878 });
      }
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
        // Hàng sát camera (3 hàng dưới): chỉ bụi và cây nhỏ. Cây lớn ở phía trước che nửa màn và lối ra (đánh giá map v1.0.0).
        const front = y >= H - 3;
        if (nearOpen && r < 0.55) place(!front && r < 0.2 ? 'tree-large-0' + (1 + Math.floor(r * 15)) : r < (front ? 0.2 : 0.4) ? 'tree-small-0' + (1 + (x % 2)) : 'bush-0' + (1 + (y % 3)), x, y, { jitter: true });
        else if (!nearOpen && !front && r < 0.12) place('tree-large-0' + (1 + (x % 3)), x, y);
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
  // Điện: nối sàn đá tối ra ngoài lan can để 1/3 dưới màn không còn là khoảng đen (đánh giá v1.0.0 P1).
  const skirtFloor = theme === 'hall' ? 'hall-floor-marble' : theme === 'city' ? 'city-paving-03' : 'grass-floor-01';
  if (skirtFloor && asset(skirtFloor)) {
    propJobs.push(
      (async () => {
        const tex = await textures.get(hd2dUrl(skirtFloor), { repeat: true });
        const M = 24;
        // Phố: sàn lát chỉ chạy từ chân dãy nhà trở ra; phía sau nhà là tường hậu, không còn mặt sàn kéo xa nhìn xuyên qua cổng vòm.
        const zN = theme === 'city' ? 1.0 : theme === 'hall' ? -1.9 : -M; // sảnh: sân thượng sau hàng cột sâu ~2,5 ô rồi tới tường thành
        const depth = H + M - zN;
        const geo = new THREE.PlaneGeometry(W + 2 * M, depth);
        const uv = geo.getAttribute('uv') as THREE.BufferAttribute;
        for (let i = 0; i < uv.count; i++) uv.setXY(i, (uv.getX(i) * (W + 2 * M)) / 4, (uv.getY(i) * depth) / 4);
        const shade = theme === 'hall' ? 0xd2c8b4 : theme === 'deep_forest' ? T.ground : theme === 'city' ? 0xc8c0b0 : 0xe4ebdc;
        const mat = P.shadows === 'none' ? new THREE.MeshBasicMaterial({ map: tex, color: shade }) : new THREE.MeshLambertMaterial({ map: tex, color: shade });
        const m = new THREE.Mesh(geo, mat);
        m.rotation.x = -Math.PI / 2;
        m.position.set(W / 2, -0.02, zN + depth / 2);
        group.add(m);
        disposables.push(geo, mat);
      })(),
    );
  }
  if (theme === 'city') backWall();
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

  /**
   * Tường hậu sau dãy nhà: mặt tường gạch sẫm cao ngang mặt tiền, tối dần xuống chân. Cổng vòm, ngõ và khe giữa các mặt tiền
   * nhìn vào thấy một bức tường/sân sau thay vì mặt sàn kéo ra xa hay nền trống (đánh giá map v1.0.0).
   */
  function backWall(): void {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const g = c.getContext('2d')!;
    const base: [number, number, number] = map.id === 'city_palace_gate' ? [112, 104, 96] : [118, 98, 80];
    g.fillStyle = `rgb(${base[0]},${base[1]},${base[2]})`;
    g.fillRect(0, 0, 128, 128);
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 4; col++) {
        const off = row % 2 ? 16 : 0;
        const k = hash(col + 3, row + 7);
        const v = Math.round((k - 0.5) * 26);
        g.fillStyle = `rgb(${base[0] + v},${base[1] + v},${base[2] + v})`;
        g.fillRect(col * 32 + off + 1, row * 16 + 1, 30, 14);
      }
    }
    g.fillStyle = 'rgba(40,30,24,0.55)';
    for (let row = 0; row <= 8; row++) g.fillRect(0, row * 16, 128, 1);
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.magFilter = THREE.NearestFilter;
    const wWall = W + 30;
    const hWall = 4.4;
    tex.repeat.set(wWall / 2, hWall / 2);
    const geo = new THREE.PlaneGeometry(wWall, hWall);
    const col = document.createElement('canvas');
    col.width = 4;
    col.height = 64;
    const cg = col.getContext('2d')!;
    const grad = cg.createLinearGradient(0, 0, 0, 64);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(10,6,4,0.78)');
    cg.fillStyle = grad;
    cg.fillRect(0, 0, 4, 64);
    const shade = new THREE.CanvasTexture(col);
    const mat = new THREE.MeshBasicMaterial({ map: tex, fog: false, color: 0xe8e2da });
    const wall = new THREE.Mesh(geo, mat);
    wall.position.set(W / 2, hWall / 2 - 0.02, 0.9);
    group.add(wall);
    // Bóng đổ xuống chân tường (tối dần về phía sàn): lớp gradient đặt sát mặt tường.
    const sgeo = new THREE.PlaneGeometry(wWall, hWall);
    const smat = new THREE.MeshBasicMaterial({ map: shade, transparent: true, depthWrite: false, fog: false });
    const sh = new THREE.Mesh(sgeo, smat);
    sh.position.set(W / 2, hWall / 2 - 0.02, 0.92);
    sh.renderOrder = 1;
    group.add(sh);
    disposables.push(geo, mat, tex, sgeo, smat, shade);
  }

  if (theme === 'forest' || theme === 'deep_forest') dressForest();

  /**
   * Bộ viền rừng theo lớp + chuyển tiếp đường đất (artwork phát hành, batch-13-release). Có asset mới thì dùng, thiếu thì
   * cảnh vẫn dựng như cũ (cây rải ở rìa). Tán xa → thân giữa → bờ bụi gần camera; mảnh rìa đất phủ lên mép đường.
   */
  function dressForest(): void {
    const has = (id: string) => !!asset(id);
    const wOf = (id: string) => asset(id)?.world?.[0] ?? 4;
    const put = (id: string, x: number, z: number, o: { flip?: boolean; tint?: number; scale?: number } = {}) => {
      propJobs.push(
        (async () => {
          const s = await propSprite(id, { tint: o.tint ?? T.tint });
          if (!s) return;
          s.position.set(x, 0, z);
          if (o.scale) s.scale.setScalar(o.scale);
          if (o.flip) s.scale.x *= -1;
          group.add(s);
          const ph = ((asset(id)?.px[1] ?? 0) / 128) * (o.scale ?? 1);
          if (ph >= 1.2) addOccluder(s, ((asset(id)?.px[0] ?? 128) / 128) * 0.5 * (o.scale ?? 1), ph);
        })(),
      );
    };
    const deep = theme === 'deep_forest';
    const rects = (map.portals ?? []).map((p) => p.rect).filter((r): r is [number, number, number, number] => !!r);
    // 1) Mép trên: tán xa mờ xanh + hàng thân cây giữa, hai lớp lệch nhịp, lật xen kẽ để không lặp.
    if (has('forest-far-canopy')) {
      const w = wOf('forest-far-canopy') * 0.95;
      for (let x = -5, i = 0; x < W + 6; x += w - 0.5, i++) put('forest-far-canopy', x + w / 2, 0.4 + (hash(i, 3) - 0.5) * 0.3, { flip: i % 2 === 1, tint: deep ? 0x8fa896 : 0xc9dccf });
    }
    if (has('forest-mid-trunks')) {
      const w = wOf('forest-mid-trunks');
      for (let x = -3, i = 0; x < W + 4; x += w * 0.78 + hash(i, 5) * 0.9, i++) {
        // Chừa chỗ cho cổng (không chắn lối ra).
        if (rects.some((r) => Math.abs(r[0] + r[2] / 2 - x) < w * 0.7 && r[1] < 3)) continue;
        put('forest-mid-trunks', x, 1.25 + hash(i, 9) * 0.3, { flip: hash(i, 2) < 0.5 });
      }
    }
    // 2) Mép dưới (phía camera): bờ bụi/đá thấp, xen hai kiểu, để không lộ khoảng trống mà vẫn thấy lối đi.
    const banks = ['forest-fg-bank', 'forest-cam-bank'].filter(has);
    if (banks.length) {
      for (let x = -3, i = 0; x < W + 3; x += 3.2 + hash(i, 7) * 0.6, i++) {
        if (rects.some((r) => r[1] > H - 4 && Math.abs(r[0] + r[2] / 2 - x) < 2.5)) continue;
        put(banks[i % banks.length]!, x, H - 0.15 + hash(i, 4) * 0.25, { flip: hash(i, 6) < 0.5, scale: 0.9 });
      }
    }
    // 3) Hai góc dưới: góc rễ + đá (lật ngang cho góc phải).
    if (has('forest-corner')) {
      put('forest-corner', 0.4, H - 0.3, { scale: 0.95 });
      put('forest-corner', W - 0.4, H - 0.3, { scale: 0.95, flip: true });
    }
    // 4) Cổng ra: vòng thân cây ôm lối đi ở mỗi cổng sát mép.
    if (has('forest-portal-arch'))
      for (const [rx, ry, rw, rh] of rects) {
        const edgeX = rx <= 1 || rx + rw >= W - 1;
        const edgeY = ry <= 1 || ry + rh >= H - 1;
        if (!edgeX && !edgeY) continue;
        put('forest-portal-arch', rx + rw / 2 + (rx > W / 2 ? 0.4 : -0.4), ry + rh + 0.4, { scale: 0.95 });
      }
    // 5) Chuyển tiếp đường đất ↔ cỏ: mảnh rìa phủ lên mép (cỏ lấn vào đất, không còn cạnh chữ nhật).
    const dirt = (x: number, y: number) => (layout[y]?.[x] ?? '#') === ',';
    const grassy = (x: number, y: number) => /[.TbtfgmrsF]/.test(layout[y]?.[x] ?? '#');
    const fringe = (id: string, x: number, z: number, flipX: boolean, flipZ: boolean) => {
      if (!has(id)) return;
      propJobs.push(
        (async () => {
          const a = asset(id)!;
          const tex = await textures.get(hd2dUrl(id));
          const k = 0.8; // mảnh vẽ 4 ô → thu còn ~3.2 ô để bám theo mép
          const geo = new THREE.PlaneGeometry((a.px[0] / 128) * k, (a.px[1] / 128) * k);
          const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, alphaTest: 0.35, depthWrite: false, color: T.ground });
          const m = new THREE.Mesh(geo, mat);
          m.rotation.x = -Math.PI / 2;
          m.position.set(x, 0.012, z);
          m.scale.set(flipX ? -1 : 1, flipZ ? -1 : 1, 1);
          m.renderOrder = 0;
          group.add(m);
          disposables.push(geo, mat);
        })(),
      );
    };
    // Mép bắc/nam: chạy dọc theo hàng; mép tây/đông: chạy dọc theo cột. Bước 2.6 ô, lệch nhịp theo hash.
    for (let y = 1; y < H - 1; y++) {
      let n = 0;
      let s = 0;
      for (let x = 1; x < W - 1; x++) {
        if (dirt(x, y) && grassy(x, y - 1) && n++ % 3 === 1) fringe('path-fringe-gn', x + 0.5, y + 0.05 + (hash(x, y) - 0.5) * 0.3, hash(x, y) < 0.5, false);
        if (dirt(x, y) && grassy(x, y + 1) && s++ % 3 === 1) fringe('path-fringe-gs', x + 0.5, y + 0.95 + (hash(y, x) - 0.5) * 0.3, hash(y, x) < 0.5, false);
      }
    }
    for (let x = 1; x < W - 1; x++) {
      let w = 0;
      let e = 0;
      for (let y = 1; y < H - 1; y++) {
        if (dirt(x, y) && grassy(x - 1, y) && w++ % 3 === 1) fringe('path-fringe-gw', x + 0.05, y + 0.5, false, hash(x, y) < 0.5);
        if (dirt(x, y) && grassy(x + 1, y) && e++ % 3 === 1) fringe('path-fringe-ge', x + 0.95, y + 0.5, false, hash(y, x) < 0.5);
      }
    }
  }

  // Điểm nhấn sàn.
  if (theme === 'hall') {
    // Tâm vòng = ô xuất hiện của nhân vật. Vòng triệu hồi (4 khung) nằm phẳng trên sàn, bụi linh khí bay lên phía trên.
    const cx = (map.spawn_default?.x ?? 9) + 0.5;
    const cz = (map.spawn_default?.y ?? 5) + 0.5;
    propJobs.push(
      (async () => {
        const s = await propSprite('summon-circle-fx', { tilt: -Math.PI / 2, ppu: 62, castShadow: false });
        if (!s) return;
        s.position.set(cx, 0.015, cz);
        animated.push(s);
        group.add(s);
      })(),
    );
    if (P.fx) propJobs.push(fx('summon-motes-fx', cx, cz + 0.2, 1.1));
  }
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
  // Tiền cảnh sát camera (neo theo màn hình, làm mờ trong hậu kỳ). Mức Thấp không có hậu kỳ nên bỏ.
  let fg: Foreground | null = null;
  const fgItems: FgItem[] = [];
  if (P.post !== 'none') {
    const has = (id: string) => !!asset(id);
    const add = (it: FgItem) => has(it.id) && fgItems.push(it);
    if (theme === 'forest' || theme === 'deep_forest') {
      const deep = theme === 'deep_forest';
      const tint = deep ? 0x8fa896 : 0xffffff;
      const dark = deep ? 0x5d7766 : 0x7d9a6c; // cành gần camera tối hơn tán phía sau để tách lớp
      add({ id: 'fg-forest-branch-a', ax: -0.8, ay: 0.74, h: 0.52, maxW: 0.46, tint: dark, rot: 0.04 });
      add({ id: 'fg-forest-branch-b', ax: 0.82, ay: 0.82, h: 0.46, maxW: 0.42, tint: dark, rot: -0.03, par: 0.1 });
      add({ id: 'fg-forest-bush-a', ax: -0.72, ay: -0.98, h: 0.3, maxW: 0.34, tint });
      add({ id: 'fg-forest-bush-c', ax: 0.08, ay: -1.04, h: 0.24, maxW: 0.3, tint, flip: true, par: 0.12 });
      add({ id: 'fg-forest-bush-b', ax: 0.82, ay: -0.99, h: 0.3, maxW: 0.34, tint, par: 0.06 });
    } else if (theme === 'city') {
      add({ id: 'fg-city-bunting', ax: -0.1, ay: 0.9, h: 0.17, maxW: 0.75, sway: 0.006, par: 0.05 });
      add({ id: 'fg-city-lantern-pair', ax: -0.93, ay: 0.46, h: 0.5, maxW: 0.22, rot: -0.02 });
      add({ id: 'fg-city-lantern-pair', ax: 0.93, ay: 0.46, h: 0.5, maxW: 0.22, flip: true, rot: 0.02 });
    } else if (theme === 'hall') {
      add({ id: 'fg-hall-curtain', ax: -1.03, ay: 0.55, h: 0.46, maxW: 0.14 });
      add({ id: 'fg-hall-curtain', ax: 1.03, ay: 0.55, h: 0.46, maxW: 0.14, flip: true });
    }
  }
  if (fgItems.length) fg = await buildForeground(fgItems);

  function dressCity(): void {
    const isGate = map.id === 'city_palace_gate';
    const has = (id: string) => !!asset(id);
    const wOf = (id: string, d = 4) => asset(id)?.world?.[0] ?? d;
    // 1) Dãy nhà liền: lấp khoảng giữa các mặt tiền đã đặt. Đơn 10: thêm 6 kiểu nhà + mảnh nối (ngõ vòm,
    //    cột ống máng, tường hộp hoa) để không lặp; Hoàng Môn dùng tường thành có lỗ châu mai.
    const houses = isGate
      ? ['palace-crenel-wall', 'palace-wall-section', 'palace-crenel-wall'].filter(has)
      : ['city-facade-inn', 'city-facade-warehouse', 'city-facade-bakery', 'city-facade-corner', 'city-facade-belltower', 'city-facade-townhouse', 'city-facade-artisan'].filter(has);
    const connectors = isGate ? ['palace-tower'] : ['city-alley-arch', 'city-facade-alley', 'city-wall-flowerbox', 'city-facade-gutter', 'city-pillar-drainpipe', 'city-facade-column'].filter(has);
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
      // Hoàng Môn: tường thành kéo giãn lấp hết khe, tháp đứng chồng lên trước (không còn mảng tường hậu phẳng hở giữa các khối).
      if (isGate && has('palace-wall-section') && r - l > 0.6) place('palace-wall-section', (l + r) / 2 - 0.5, 0.6, { scaleX: Math.min(2.4, (r - l) / wOf('palace-wall-section', 4.6) + 0.25) });
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
    // Hoàng Môn: sân trong thấp thoáng sau vòm cổng (thay mảng tường xám); trụ dịch chuyển đặt trên bệ tròn.
    if (isGate && has('palace-courtyard-passage')) {
      propJobs.push(
        (async () => {
          const m = await propSprite('palace-courtyard-passage', { tint: T.tint, castShadow: false });
          if (!m) return;
          m.scale.multiplyScalar(0.52);
          m.position.set(13.5, 0, 1.55);
          group.add(m);
        })(),
      );
    }
    if (!isGate && has('stone-plinth-round'))
      for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (layout[y]![x] === 'O') place('stone-plinth-round', x, y - 0.05, { decor: true });
    // 4) Thảm đỏ trên lối gạch ở Hoàng Môn.
    if (isGate) propJobs.push(decal('palace-carpet-strip', 13.5, 5.6, 2, Math.PI / 2)); // chạy dọc trục cổng cung điện, từ chân cổng xuống sân
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

  // Sảnh: sân đá mở ra thành phố. Từ xa tới gần: tường thành + thành phố, hàng cột + xà ngang, cột bên hông, ngưỡng cửa phía trước.
  if (theme === 'hall') {
    propJobs.push(
      (async () => {
        const tex = await textures.get(hd2dUrl('hall-city-backdrop'));
        const w = W + 18;
        const ap = asset('hall-city-backdrop')?.px ?? [2432, 486];
        const h = (w * ap[1]) / ap[0];
        const geo = new THREE.PlaneGeometry(w, h);
        const mat = new THREE.MeshBasicMaterial({ map: tex, fog: false });
        const m = new THREE.Mesh(geo, mat);
        m.position.set(W / 2, h / 2 - 0.4, -2.0);
        group.add(m);
        disposables.push(geo, mat);
      })(),
    );
    // Dải mái nhà gần: đứng ngay trước nền thành phố, đáy chạm đỉnh tường thành, cho cảnh có hai lớp xa.
    propJobs.push(
      (async () => {
        const a = asset('hall-city-roofs');
        if (!a) return;
        const tex = await textures.get(hd2dUrl('hall-city-roofs'));
        const w = W + 18;
        const h = (w * a.px[1]) / a.px[0];
        const geo = new THREE.PlaneGeometry(w, h);
        const mat = new THREE.MeshBasicMaterial({ map: tex, alphaTest: 0.5, fog: false });
        const m = new THREE.Mesh(geo, mat);
        m.position.set(W / 2, h / 2 + 1.0, -1.95);
        group.add(m);
        disposables.push(geo, mat);
      })(),
    );
    // Vệt sáng kính màu rơi xuống sàn từ các ô kính hai hông (cộng sáng, mờ vừa phải để đọc là ánh sáng chứ không phải miếng dán).
    const lightPatch = (variant: number, x: number, z: number, mirror: boolean) =>
      propJobs.push(
        (async () => {
          const id = `hall-floor-light-${variant}`;
          if (!asset(id)) return;
          const tex = await textures.get(hd2dUrl(id));
          const geo = new THREE.PlaneGeometry(2.2, 2.2);
          const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, opacity: 0.5, fog: false });
          const m = new THREE.Mesh(geo, mat);
          m.rotation.x = -Math.PI / 2;
          if (mirror) m.scale.x = -1;
          m.position.set(x, 0.012, z);
          group.add(m);
          disposables.push(geo, mat);
        })(),
      );
    [3.6, 5.6, 7.6].forEach((z, i) => {
      lightPatch(i + 1, 2.6, z + 0.5, false);
      lightPatch(((i + 1) % 3) + 1, W - 2.6, z + 0.5, true);
    });
    const stand = (id: string, x: number, z: number, y = 0, ppu?: number, flipX = false) =>
      propJobs.push(
        (async () => {
          const s = await propSprite(id, { tint: T.tint, castShadow: real, ...(ppu ? { ppu } : {}) });
          if (!s) return;
          s.position.set(x, y, z);
          if (flipX) s.scale.x *= -1;
          if (s.userData.anim) animated.push(s);
          group.add(s);
        })(),
      );
    const COL_PPU = 175; // cột 224×560 px → 1,28×3,2 ô
    for (const x of [1.5, 5.5, 9.5, 13.5, 17.5]) stand('hall-column', x, 0.5, 0, COL_PPU);
    stand('hall-lintel', W / 2, 0.42, 2.92, 1942 / (W + 1));
    for (const x of [7.5, 11.5]) stand('hall-lantern', x, 0.9, 2.9, 233);
    for (const x of [3.5, 15.5]) stand('hall-banner', x, 0.85, 2.88, 150); // cờ treo từ xà, hai bên cặp đèn
    // Hai bên: lan can đá + trụ đầu + ô kính gắn tường, xoay 90° quanh trục đứng để chạy dọc chiều sâu (bên phải đối xứng).
    const side = (id: string, x: number, z: number, rotY: number, ppu: number) =>
      propJobs.push(
        (async () => {
          const s = await propSprite(id, { tint: T.tint, castShadow: false, ppu, tilt: 0 });
          if (!s) return;
          s.position.set(x, 0, z);
          s.rotation.y = rotY;
          group.add(s);
        })(),
      );
    for (const [x, rot] of [[0.35, Math.PI / 2], [W - 0.35, -Math.PI / 2]] as const) {
      for (const z of [3.8, 7.8]) side('hall-side-balustrade', x, z, rot, 128);
      for (const z of [1.8, 5.8, 9.8]) side('hall-side-pier', x, z, rot, 190);
      for (const z of [3.8, 7.8]) side('hall-side-window', x + (x < 1 ? 0.15 : -0.15), z, rot, 120);
    }
    // Ngưỡng cửa phía trước: hai nửa chừa lối ra x = 8..11 (khớp cổng hall_exit rộng 3 ô).
    stand('hall-threshold-left', 8.04 / 2, H - 0.05);
    stand('hall-threshold-right', W - 8.04 / 2, H - 0.05);
  }

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

  async function decal(id: string, x: number, z: number, scale = 1, spin = 0) {
    const a = asset(id);
    if (!a) return;
    const tex = await textures.get(hd2dUrl(id));
    const geo = new THREE.PlaneGeometry((a.px[0] / 128) * scale, (a.px[1] / 128) * scale);
    const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, color: T.ground });
    const m = new THREE.Mesh(geo, mat);
    m.rotation.x = -Math.PI / 2;
    m.rotation.z = spin;
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

  const atmo = P.fx ? makeAtmosphere(group, { theme, W, H, lamps, shafts: theme === 'forest' || theme === 'deep_forest' || theme === 'city', motes: Math.round((theme === 'hall' ? 40 : 70) * P.decor) }) : null;
  const lmask = P.fx ? makeLightMask(group, { theme, W, H, lamps, seed: W * 131 + H * 7 }) : null;
  let time = 0;
  return {
    group,
    pickables,
    fgRoot: fg?.root ?? null,
    hasFg: !!fg,
    setLight(l: Light) {
      atmo?.setLight(l);
      lmask?.setLight(l);
    },
    update(dt: number, player?: THREE.Vector3 | null, cam?: THREE.PerspectiveCamera) {
      time += dt;
      if (fg && cam) fg.update(dt, cam, cam.position.x, W / 2);
      atmo?.update(dt);
      if (player) lmask?.update(player.x, player.z);
      for (const a of ambient) a.update(dt, player ?? null);
      if (player)
        for (const o of occluders) {
          const dz = o.obj.position.z - player.z; // vật ở hàng trước (gần camera hơn) người chơi
          // Camera nhìn xuống ~38° và sprite nghiêng: vật cao h che được các ô phía sau tới khoảng h·1.6.
          const hide = dz > 0.05 && dz < o.h * 1.6 && Math.abs(o.obj.position.x - player.x) < o.hw + 0.4;
          const want = hide ? 0.38 : 1;
          if (Math.abs(o.cur - want) < 0.01) continue;
          o.cur += (want - o.cur) * Math.min(1, dt * 8);
          for (const m of o.mats) {
            const tr = o.cur < 0.99;
            if (m.transparent !== tr) m.needsUpdate = true; // three biên dịch lại: vật liệu đục ép alpha = 1 (OPAQUE)
            m.transparent = tr;
            m.opacity = o.cur;
            m.alphaTest = 0.5 * o.cur; // alphaTest so với alpha đã nhân opacity: hạ theo để tán cây mờ chứ không biến mất
            m.depthWrite = o.cur >= 0.99;
          }
        }
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
      atmo?.dispose();
      lmask?.dispose();
      fg?.dispose();
    },
  };
}

