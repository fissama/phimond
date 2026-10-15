// Trang xem cảnh độc lập (dev): ?map=forest&x=0.5&q=high  — dùng để chụp ảnh kiểm tra nghệ thuật/hiệu năng.
import { Engine } from '../render/engine.ts';

const Q = new URLSearchParams(location.search);
const engine = new Engine(document.getElementById('c') as HTMLCanvasElement, document.getElementById('host')!);
(window as unknown as { engine: Engine }).engine = engine;
const id = Q.get('map') ?? 'forest';
void engine.loadMap(id).then((rt) => {
  const w = rt.data.walk; const fx = Number(Q.get('x') ?? 0.5);
  const x = w.x0 + (w.x1 - w.x0) * fx; const z = (w.z0 + w.z1) / 2;
  engine.onFrame(() => { engine.U.uCamX.value = x; engine.placeCamera(x, z); });
  engine.start();
  (window as unknown as { ready: boolean }).ready = true;
});
