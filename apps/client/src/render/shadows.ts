import * as THREE from 'three';
import { asset, hd2dUrl, textures } from './assets.ts';

/**
 * Bóng đổ vẽ tay (GPT S01–S27: shadow-round-small/large, shadow-rect, shadow-canopy) đặt phẳng dưới chân vật thể và
 * kéo dài theo hướng nắng của giờ trong ngày (mức Trung bình; mức Cao dùng shadow map thật). Mỗi bóng là một Group
 * có `userData.shadow`; `applySun` duyệt cả cảnh để cập nhật hướng/độ dài/độ đậm khi giờ đổi.
 */
export type ShadowKind = 'small' | 'large' | 'rect' | 'canopy';
const FILE: Record<ShadowKind, string> = { small: 'shadow-round-small', large: 'shadow-round-large', rect: 'shadow-rect', canopy: 'shadow-canopy' };

export interface Sun {
  /** Hướng bóng trên mặt đất (đơn vị). */
  dx: number;
  dz: number;
  /** Hệ số kéo dài (1 = bóng gần tròn dưới chân). */
  stretch: number;
  /** Độ đậm 0..1 (mờ dần về đêm). */
  alpha: number;
}

/** Mặt trời mọc hướng đông (+x), lặn hướng tây (−x), ở phía nam (phía camera) nên bóng đổ sang bên và lùi ra sau. */
export function sunFor(hour: number, night: number): Sun {
  const a = Math.min(Math.PI, Math.max(0, ((hour - 6) / 12) * Math.PI));
  // Trưa bóng gần tròn dưới chân (1), sáng sớm/chiều muộn kéo dài dần, trần 2.6.
  const stretch = Math.min(2.6, 1 + 1.6 * Math.pow(1 - Math.sin(a), 1.3));
  const dx = -Math.cos(a);
  const dz = -0.42;
  const n = Math.hypot(dx, dz);
  return { dx: dx / n, dz: dz / n, stretch, alpha: 0.6 * (1 - 0.8 * night) };
}

/** Tạo bóng rộng ~w ô. Thiếu asset → null (nơi gọi dùng bóng tròn mờ cũ). */
export async function paintedShadow(kind: ShadowKind, w: number): Promise<THREE.Group | null> {
  const id = FILE[kind];
  const a = asset(id);
  if (!a) return null;
  const tex = await textures.get(hd2dUrl(id));
  const bw = a.world?.[0] ?? a.px[0] / 128;
  const bh = a.world?.[1] ?? a.px[1] / 128;
  const k = w / bw;
  const geo = new THREE.PlaneGeometry(bw * k, bh * k);
  const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, opacity: 0.8, fog: false });
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI / 2;
  mesh.renderOrder = 1;
  const g = new THREE.Group();
  g.position.y = 0.02;
  g.add(mesh);
  g.userData.shadow = { w: bw * k, kind };
  applyOne(g, sunFor(15, 0));
  return g;
}

function applyOne(g: THREE.Object3D, s: Sun): void {
  const info = g.userData.shadow as { w: number; kind: ShadowKind } | undefined;
  const mesh = g.children[0] as THREE.Mesh | undefined;
  if (!info || !mesh) return;
  g.rotation.y = Math.atan2(-s.dz, s.dx);
  // Bóng tròn/chữ nhật kéo dài ra phía xa chân; bóng tán giữ nguyên hình, chỉ dịch đi.
  const stretch = info.kind === 'canopy' ? 1 + (s.stretch - 1) * 0.35 : s.stretch;
  mesh.scale.set(stretch, info.kind === 'canopy' ? 1 : 1 / Math.sqrt(stretch), 1);
  mesh.position.x = info.w * (info.kind === 'canopy' ? 0.15 + 0.12 * s.stretch : 0.08 + 0.22 * (stretch - 1));
  (mesh.material as THREE.MeshBasicMaterial).opacity = s.alpha;
  (g as THREE.Object3D).visible = s.alpha > 0.02;
}

/** Cập nhật mọi bóng vẽ trong `root` theo giờ. */
export function applySun(root: THREE.Object3D, hour: number, night: number): void {
  const s = sunFor(hour, night);
  root.traverse((o) => {
    if (o.userData.shadow) applyOne(o, s);
  });
}
