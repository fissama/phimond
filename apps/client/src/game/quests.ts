import type { Character } from '@phimond/protocol';
import type { Content } from './content.ts';

export interface QuestDef {
  id: string;
  name: string;
  description?: string;
  kind: string;
  target?: string;
  count?: number;
  gold?: number;
  xp?: number;
  items?: Record<string, number>;
  requires?: string;
  giver?: string;
}
export interface QuestView {
  q: QuestDef;
  s?: { progress: number; claimed: boolean };
  ready: boolean;
  /** Chưa nhận và đã đủ điều kiện (xong nhiệm vụ trước). */
  available: boolean;
}

/** Trạng thái chuỗi nhiệm vụ theo thứ tự dữ liệu (server kiểm lại requires/giver khi nhận). */
export function questViews(ch: Character, content: Content): QuestView[] {
  const quests = Object.values(content.cat.quests) as unknown as QuestDef[];
  return quests.map((q) => {
    const s = ch.quests[q.id] as QuestView['s'];
    const prevDone = !q.requires || !!ch.quests[q.requires]?.claimed;
    return { q, s, ready: !!s && !s.claimed && s.progress >= (q.count ?? 1), available: !s && prevDone };
  });
}

export function npcLabel(content: Content, id?: string): string {
  if (!id) return '';
  const n = content.cat.npcs[id] as { name?: string; map_id?: string } | undefined;
  if (!n) return id;
  return `${n.name ?? id}${n.map_id ? ` (${content.mapName(n.map_id)})` : ''}`;
}

/** Câu hướng dẫn cụ thể cho nhiệm vụ đang làm. */
export function questHint(v: QuestView, content: Content): string {
  const { q, s } = v;
  const n = q.count ?? 1;
  const prog = `${Math.min(s?.progress ?? 0, n)}/${n}`;
  switch (q.kind) {
    case 'battle_win':
      return `Thắng trận${q.target ? ` với ${content.speciesName(q.target)}` : ''} · ${prog}`;
    case 'pet_capture':
      return `Bắt linh thú: làm yếu rồi dùng Phù Phong Ấn · ${prog}`;
    case 'talk_npc':
      return `Nói chuyện với ${npcLabel(content, q.target)}`;
    case 'reach_map':
      return `Đi tới ${content.mapName(q.target ?? '')}`;
    default:
      return `Tiến độ ${prog}`;
  }
}
