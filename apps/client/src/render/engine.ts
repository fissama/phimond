import * as THREE from 'three';
import { cellCenter, type Cell } from '../world/coords.ts';

export type FpsCap = 30 | 60;

export interface MapView {
  id: string;
  width: number;
  height: number;
  portals: Cell[];
  npcs: Cell[];
}

/**
 * Renderer khung S0: mặt đất dạng lưới theo kích thước map, điểm đánh dấu người chơi/NPC/cổng.
 * Cảnh HD-2D thật (kit, ánh sáng, bóng, sprite) thay thế phần này ở S2/S5; API công khai giữ nguyên.
 */
export class Engine {
  readonly renderer: THREE.WebGLRenderer;
  private readonly scene = new THREE.Scene();
  private readonly camera = new THREE.PerspectiveCamera(30, 1, 0.1, 200);
  private readonly mapGroup = new THREE.Group();
  private readonly player: THREE.Mesh;
  private readonly target = new THREE.Vector3();
  private raf = 0;
  private last = 0;
  private cap: FpsCap = 60;
  private readonly resizeObs: ResizeObserver;
  frames = 0;

  constructor(private readonly host: HTMLElement) {
    this.renderer = new THREE.WebGLRenderer({ antialias: false, powerPreference: 'high-performance' });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setClearColor(0x0f1420);
    this.renderer.domElement.dataset.testid = 'world-canvas';
    host.appendChild(this.renderer.domElement);

    this.scene.add(new THREE.HemisphereLight(0xfff4e0, 0x404858, 1.2));
    const sun = new THREE.DirectionalLight(0xffffff, 1.4);
    sun.position.set(-6, 12, 8);
    this.scene.add(sun, this.mapGroup);

    this.player = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.3, 0.7), new THREE.MeshLambertMaterial({ color: 0x3355cc }));
    this.player.position.y = 0.65;
    this.scene.add(this.player);

    this.resizeObs = new ResizeObserver(() => this.resize());
    this.resizeObs.observe(host);
    this.resize();
  }

  setFpsCap(cap: FpsCap): void {
    this.cap = cap;
  }

  loadMap(m: MapView): void {
    this.mapGroup.clear();
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(m.width, m.height),
      new THREE.MeshLambertMaterial({ color: 0x5c7a4a }),
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(m.width / 2, 0, m.height / 2);
    const grid = new THREE.GridHelper(Math.max(m.width, m.height), Math.max(m.width, m.height), 0x2c3a24, 0x46603a);
    grid.position.set(Math.max(m.width, m.height) / 2, 0.01, Math.max(m.width, m.height) / 2);
    this.mapGroup.add(ground, grid);
    const marker = (c: Cell, color: number, h: number) => {
      const mesh = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, h, 12), new THREE.MeshLambertMaterial({ color }));
      const p = cellCenter(c);
      mesh.position.set(p.x, h / 2, p.z);
      this.mapGroup.add(mesh);
    };
    m.portals.forEach((c) => marker(c, 0x9b59d0, 0.1));
    m.npcs.forEach((c) => marker(c, 0xe0b040, 1.2));
  }

  setPlayer(c: Cell): void {
    const p = cellCenter(c);
    this.player.position.x = p.x;
    this.player.position.z = p.z;
  }

  start(): void {
    const tick = (t: number) => {
      this.raf = requestAnimationFrame(tick);
      // Giới hạn FPS: bỏ khung khi chưa đủ khoảng (dung sai 1 ms cho màn 60/120 Hz).
      const minDt = 1000 / this.cap - 1;
      if (t - this.last < minDt) return;
      this.last = t;
      this.frame();
    };
    this.raf = requestAnimationFrame(tick);
  }

  dispose(): void {
    cancelAnimationFrame(this.raf);
    this.resizeObs.disconnect();
    this.renderer.dispose();
    this.renderer.domElement.remove();
  }

  private frame(): void {
    // Camera HD-2D: nhìn chéo xuống, bám người chơi.
    this.target.copy(this.player.position);
    this.camera.position.set(this.target.x, this.target.y + 9, this.target.z + 13);
    this.camera.lookAt(this.target);
    this.renderer.render(this.scene, this.camera);
    this.frames += 1;
  }

  private resize(): void {
    const w = this.host.clientWidth || 1;
    const h = this.host.clientHeight || 1;
    this.renderer.setSize(w, h, false);
    this.renderer.domElement.style.width = '100%';
    this.renderer.domElement.style.height = '100%';
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
  }
}
