import * as THREE from 'three';
import { loadJson, loadTexture, assetUrl } from './assets.ts';
import { AtlasSprite, type AtlasSpec } from './actors.ts';
import type { SharedUniforms } from './sceneBuilder.ts';

interface SpeciesArt { file: string; small: string; feet: number[][]; width: number[][]; height: number[][]; portrait: [number, number, number]; footPad: number; bodyH: number; bodyW: number }
interface PetManifest { cell: number; cols: number; rows: number; rowNames: string[]; species: Record<string, SpeciesArt>; legacy: Record<string, { species: string; artPending: boolean }> }
interface ActorManifest { player: { file: string; cols: number; rows: number; cell: number; idle: [number, number]; run: [number, number]; fps: number }; npcs: Record<string, { file: string; w: number; h: number; bbox: [number, number, number, number] }> }

export const PET_ROWS = { idle: 0, move: 1, attack: 2, cast: 3, down: 4 } as const;
export type PetRow = keyof typeof PET_ROWS;

let petMan: Promise<PetManifest> | null = null;
let actMan: Promise<ActorManifest> | null = null;
export const petManifest = (): Promise<PetManifest> => (petMan ??= loadJson<PetManifest>('assets/pets/manifest.json'));
export const actorManifest = (): Promise<ActorManifest> => (actMan ??= loadJson<ActorManifest>('assets/actors/manifest.json'));

/** Loài server -> atlas hiển thị. Loài lạ dùng ô dự phòng đầu tiên (không bao giờ vỡ UI). */
export async function resolveSpecies(speciesId: string): Promise<{ id: string; art: SpeciesArt; pending: boolean }> {
  const m = await petManifest();
  const hit = m.legacy[speciesId] ?? (m.species[speciesId] ? { species: speciesId, artPending: false } : undefined);
  const sid = hit?.species ?? Object.keys(m.species)[0]!;
  return { id: sid, art: m.species[sid]!, pending: hit?.artPending ?? true };
}

/** Kiểu CSS cắt chân dung vuông từ atlas (UI: danh sách pet, thanh trạng thái). Đồng bộ sau khi manifest đã nạp. */
export function portraitStyle(m: PetManifest, speciesId: string, size: number): Record<string, string> {
  const hit = m.legacy[speciesId] ?? (m.species[speciesId] ? { species: speciesId, artPending: false } : undefined);
  const art = m.species[hit?.species ?? Object.keys(m.species)[0]!]!;
  const [x, y, side] = art.portrait; const k = size / side;
  return {
    width: `${size}px`, height: `${size}px`, imageRendering: 'pixelated', backgroundRepeat: 'no-repeat',
    backgroundImage: `url(${assetUrl('assets/pets/' + art.small)})`,
    backgroundSize: `${m.cell * m.cols * k}px ${m.cell * m.rows * k}px`,
    backgroundPosition: `${-x * k}px ${-y * k}px`,
  };
}

export async function createPetSprite(speciesId: string, targetBodyH: number, U: SharedUniforms, small = false): Promise<{ sprite: AtlasSprite; pending: boolean }> {
  const m = await petManifest(); const r = await resolveSpecies(speciesId);
  const tex = await loadTexture(`assets/pets/${small ? r.art.small : r.art.file}`, { mip: true, aniso: 2 });
  const full = m.cell * m.cols; // 1124 ở bản đầy đủ
  const k = small ? 0.5 : 1;
  const upp = targetBodyH / (r.art.bodyH * k);
  const spec: AtlasSpec = { texture: tex, cols: m.cols, rows: m.rows, cellPx: [m.cell * k, m.cell * k], unitsPerPx: upp, footPadPx: r.art.footPad * k, shadowW: Math.min(r.art.bodyW * k * upp * 0.8, 2.2) };
  void full;
  return { sprite: new AtlasSprite(spec, U, r.art.bodyH * k), pending: r.pending };
}

export async function createPlayerSprite(U: SharedUniforms): Promise<AtlasSprite> {
  const a = await actorManifest();
  const tex = await loadTexture(`assets/actors/${a.player.file}`, { mip: false });
  return new AtlasSprite({ texture: tex, cols: a.player.cols, rows: a.player.rows, cellPx: [a.player.cell, a.player.cell], unitsPerPx: 0.0265, footPadPx: 0, shadowW: 0.85 }, U, 58);
}

export async function createNpcSprite(npcId: string, U: SharedUniforms): Promise<AtlasSprite> {
  const a = await actorManifest();
  const n = a.npcs[npcId] ?? a.npcs.trainer!;
  const tex = await loadTexture(`assets/actors/${n.file}`, { mip: false });
  return new AtlasSprite({ texture: tex, cols: 1, rows: 1, cellPx: [n.w, n.h], unitsPerPx: 0.026, footPadPx: n.h - n.bbox[3], shadowW: 0.9 }, U, n.bbox[3] - n.bbox[1]);
}
export type { THREE };
