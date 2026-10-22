import type { Character } from '@phimond/protocol';
import type { Content } from './content.ts';

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
  const quests = Object.values(content.cat.quests) as { id: string; name: string; count?: number }[];
  const active = quests.map((q) => ({ q, s: ch.quests[q.id] })).filter((x) => x.s && !x.s.claimed);
  const ready = active.find((x) => x.s!.progress >= (x.q.count ?? 1));
  if (ready) return { title: ready.q.name, detail: 'Hoàn thành — quay lại báo cáo' };
  if (active[0]) return { title: active[0].q.name, detail: `Tiến độ ${active[0].s!.progress}/${active[0].q.count ?? 1}` };
  const started = quests.some((q) => ch.quests[q.id]);
  return started
    ? { title: 'Khám phá Đợt A', detail: 'Ghé Quảng Trường Thạch Trụ để mở đường tới nơi mới' }
    : { title: 'Nhận nhiệm vụ đầu tiên', detail: 'Hỏi Kiểm Lâm Lio ở Bìa Rừng Lục Bảo' };
}
