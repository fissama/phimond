import type { Character } from '@phimond/protocol';
import type { Content } from './content.ts';
import { npcLabel, questHint, questViews } from './quests.ts';

/**
 * Mục tiêu hiện tại hiện ở HUD (đánh giá G2: người mới không biết làm gì). Suy ra từ trạng thái nhân vật,
 * không lưu riêng nên không lệch với server.
 */
export function currentGoal(ch: Character, content: Content): { title: string; detail: string } | null {
  if (ch.battle) return null;
  const hasPet = ch.pets.some((p) => !p.retired);
  if (!hasPet) {
    return {
      title: 'Chọn linh thú đầu tiên',
      detail: ch.map_id.includes('summoning_hall') ? 'Đi tới một bệ đá rồi bấm Chọn' : 'Về Triệu Linh Điện để chọn bệ đá',
    };
  }
  const views = questViews(ch, content);
  const ready = views.find((v) => v.ready);
  if (ready) return { title: ready.q.name, detail: 'Xong — báo cáo ở NPC nhiệm vụ gần nhất để nhận thưởng' };
  const active = views.find((v) => v.s && !v.s.claimed);
  if (active) return { title: active.q.name, detail: questHint(active, content) };
  const next = views.find((v) => v.available && v.q.kind !== 'pet_breed');
  if (next) return { title: next.q.name, detail: `Nhận nhiệm vụ: gặp ${npcLabel(content, next.q.giver) || 'NPC nhiệm vụ'}` };
  return { title: 'Hoàn thành Đợt A', detail: 'Luyện linh thú, bắt thêm bạn mới — Điền Trang mở ở bản sau' };
}
