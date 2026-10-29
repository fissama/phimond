import * as THREE from 'three';
import { asset, hd2dUrl, textures } from './assets.ts';
import { FG_LAYER } from './layers.ts';

/**
 * Tiền cảnh sát camera kiểu Octopath: cành lá, cờ, đèn, rèm đóng khung mép màn hình. Mỗi vật được neo theo tọa độ màn hình
 * (ax, ay ∈ [−1, 1], chiều cao `h` tính theo tỉ lệ chiều cao khung nhìn) và gắn vào camera, nên luôn nằm ở mép dù người chơi
 * đi đâu; dịch nhẹ ngược chiều camera để có thị sai, đung đưa chậm. Vẽ ở lớp FG_LAYER và được làm mờ trong hậu kỳ (post.ts).
 */
export interface FgItem {
  id: string;
  ax: number;
  ay: number;
  /** Chiều cao theo tỉ lệ chiều cao khung nhìn (0..1). */
  h: number;
  /** Bề rộng tối đa theo tỉ lệ bề rộng khung nhìn (mặc định 0.5), để màn dọc không bị vật che hết. */
  maxW?: number;
  flip?: boolean;
  tint?: number;
  /** Góc xoay (rad). */
  rot?: number;
  /** Biên độ đung đưa (rad). */
  sway?: number;
  /** Hệ số thị sai theo vị trí camera (đơn vị/đơn vị), nhỏ để vật không trôi khỏi mép. */
  par?: number;
  opacity?: number;
}

const DEPTH = 9;

export interface Foreground {
  root: THREE.Group;
  count: number;
  update(dt: number, cam: THREE.PerspectiveCamera, camX: number, mapMid: number): void;
  dispose(): void;
}

export async function buildForeground(items: FgItem[]): Promise<Foreground> {
  const root = new THREE.Group();
  root.name = 'fg-root';
  const parts: { item: FgItem; mesh: THREE.Mesh; aspect: number; phase: number }[] = [];
  const disposables: { dispose(): void }[] = [];
  await Promise.all(
    items.map(async (item, i) => {
      const a = asset(item.id);
      if (!a) return;
      const tex = await textures.get(hd2dUrl(item.id));
      const geo = new THREE.PlaneGeometry(1, 1);
      const mat = new THREE.MeshBasicMaterial({ map: tex, alphaTest: 0.5, color: item.tint ?? 0xffffff, fog: false, transparent: item.opacity !== undefined, opacity: item.opacity ?? 1 });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.layers.set(FG_LAYER);
      mesh.position.z = -DEPTH;
      root.add(mesh);
      parts.push({ item, mesh, aspect: a.px[0] / a.px[1], phase: i * 1.7 });
      disposables.push(geo, mat);
    }),
  );
  root.traverse((o) => o.layers.set(FG_LAYER));
  let t = 0;
  return {
    root,
    count: parts.length,
    update(dt, cam, camX, mapMid) {
      t += dt;
      const viewH = 2 * DEPTH * Math.tan(THREE.MathUtils.degToRad(cam.fov / 2));
      const viewW = viewH * cam.aspect;
      for (const p of parts) {
        const { item, mesh, aspect } = p;
        let h = item.h * viewH;
        let w = h * aspect;
        const maxW = (item.maxW ?? 0.5) * viewW;
        if (w > maxW) {
          w = maxW;
          h = w / aspect;
        }
        mesh.scale.set(item.flip ? -w : w, h, 1);
        const shift = -(camX - mapMid) * (item.par ?? 0.08);
        // Neo theo mép: ax = ±1 là mép màn; để vật không lòi khỏi khung, vị trí tâm tính từ mép tương ứng.
        const cx = item.ax * (viewW / 2) + shift;
        const cy = item.ay * (viewH / 2);
        mesh.position.set(cx, cy, -DEPTH);
        mesh.rotation.z = (item.rot ?? 0) + Math.sin(t * 0.7 + p.phase) * (item.sway ?? 0.012);
      }
    },
    dispose() {
      disposables.forEach((d) => d.dispose());
    },
  };
}
