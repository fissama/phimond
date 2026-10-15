import { tn } from '../i18n';
// Thông điệp tiếng Việt cho lỗi và sự kiện, port nguyên văn từ client Godot (PhimondClient.gd).
const FRIENDLY: Record<string, string> = {
  'insufficient gold': 'Không đủ vàng.',
  'finish your battle first': 'Hãy hoàn thành trận đấu trước.',
  'use a portal at the map edge': 'Bạn đã đến rìa bản đồ. Hãy tìm cổng dịch chuyển.',
  'NPC is not nearby': 'Hãy đến gần nhân vật để trò chuyện.',
  'no nearby portal': 'Không có cổng dịch chuyển ở gần.',
  'wild beast is not nearby': 'Hãy đến gần linh thú để bắt đầu trận đấu.',
  'heal your active beast before battle': 'Linh thú đã kiệt sức. Hãy hồi phục trước khi chiến đấu.',
  'slow down': 'Thao tác quá nhanh. Vui lòng chờ một chút.',
  'quest is not ready for reward': 'Nhiệm vụ chưa hoàn thành.',
  'already appraised': 'Thú cưng đã được giám định.',
  'switch active pet before releasing': 'Hãy đổi thú cưng xuất chiến trước khi thả.',
};
export const GENERIC_ERROR = 'Chưa thể thực hiện thao tác này. Hãy kiểm tra điều kiện và thử lại.';
export const friendlyError = (message: string): string => FRIENDLY[message] ?? GENERIC_ERROR;

export function httpFailureText(status: number, timedOut: boolean, kind: 'login' | 'register' | 'other' = 'other'): string {
  if (timedOut) return 'Máy chủ phản hồi quá lâu. Vui lòng thử lại.';
  if (status === 401) return 'Tên đăng nhập hoặc mật khẩu không đúng.';
  if (status === 409) return 'Tên đăng nhập đã được sử dụng.';
  // Server thật trả 400 cho mọi lỗi đăng nhập/đăng ký; đăng nhập sai nên báo đúng nguyên nhân.
  if (status === 400) return kind === 'login' ? 'Tên đăng nhập hoặc mật khẩu không đúng.' : 'Thông tin đăng ký chưa hợp lệ hoặc tên đã được dùng (tên 3–24 ký tự a–z, 0–9, _; mật khẩu 10–72 ký tự).';
  return 'Không thể kết nối máy chủ. Vui lòng thử lại.';
}

const LABELS: Record<string, string> = {
  npc_dialogue: 'Mỗi linh thú mang câu chuyện của những thế hệ tổ tiên.',
  pet_appraise: 'Đã giám định tiềm năng thú cưng.',
  pet_activate: 'Đã đổi thú cưng xuất chiến.',
  pet_learn: 'Thú cưng đã học kỹ năng.',
  pet_release: 'Đã thả thú cưng; phả hệ vẫn được lưu giữ.',
  pet_strengthen: 'Đã cường hóa thú cưng.',
  recipe_learn: 'Đã học công thức lai tạo.',
  pet_heal: 'Các thú cưng đã được hồi phục.',
  item_gain: 'Đã nhận vật phẩm.',
  currency_spend: 'Đã thanh toán vàng.',
  currency_gain: 'Đã nhận phần thưởng.',
  pet_breed: 'Lai tạo thành công; tổ tiên được lưu trong phả hệ.',
  item_spend: 'Đã sử dụng vật phẩm.',
  battle_start: 'Trận đấu bắt đầu!',
  battle_flee: 'Đã rút lui khỏi trận đấu.',
  action_blocked: 'Không thể thực hiện hành động này.',
  pet_capture: 'Đã bắt thú cưng! Hãy đến người giám định.',
  capture_failed: 'Thú cưng đã thoát khỏi phong ấn.',
  defend: 'Đang phòng thủ.',
  status_fatal: 'Thú cưng gục ngã do hiệu ứng bất lợi.',
  status_expired: 'Hiệu ứng đã kết thúc.',
  battle_win: 'Chiến thắng!',
  battle_loss: 'Thất bại. Hãy hồi phục và thử lại.',
  skill_cast: 'Đã thi triển kỹ năng.',
  miss: 'Đòn đánh trượt mục tiêu.',
  status_cleansed: 'Đã giải trừ hiệu ứng bất lợi.',
  status_resisted: 'Đã kháng hiệu ứng.',
  status_applied: 'Mục tiêu chịu hiệu ứng bất lợi.',
  buff_applied: 'Đã nhận hiệu ứng hỗ trợ.',
};

export function eventMessage(ev: { type: string; message?: string; amount?: number }): string {
  const message = tn(ev.message ?? '');
  switch (ev.type) {
    case 'map_enter':
      return `Đã đến ${message}.`;
    case 'quest_accept':
      return `Đã nhận nhiệm vụ: ${message}`;
    case 'quest_complete':
      return `Hoàn thành nhiệm vụ: ${message}`;
    case 'damage':
      return `Mục tiêu nhận ${Math.trunc(ev.amount ?? 0)} sát thương.`;
    case 'heal':
      return `Hồi phục ${Math.trunc(ev.amount ?? 0)} sinh lực.`;
    default:
      return LABELS[ev.type] ?? '';
  }
}
