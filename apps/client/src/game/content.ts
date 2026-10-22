import type { BattleEvent, Catalog, MapDef, Npc } from '@phimond/protocol';
import { Grid } from '../world/grid.ts';

/** Tên tiếng Việt cho nội dung server còn tên tiếng Anh (loài, vật phẩm, kỹ năng, trạng thái, công thức). */
type Dict = Record<string, Record<string, string | { name: string; description?: string }>>;
let dict: Dict = {};
const reverse = new Map<string, string>();

export async function loadDictionary(): Promise<void> {
  try {
    const r = await fetch(`${import.meta.env.BASE_URL}i18n/vi.json`);
    if (r.ok) dict = (await r.json()) as Dict;
  } catch {
    dict = {};
  }
}

function tr(kind: string, id: string, fallback: string): string {
  const t = dict[kind]?.[id];
  if (!t) return fallback;
  return typeof t === 'string' ? t : t.name;
}

/** Catalog đã gắn tên tiếng Việt và lưới đi được của từng map. */
export class Content {
  readonly grids = new Map<string, Grid>();

  constructor(readonly cat: Catalog) {
    for (const kind of ['species', 'items', 'skills', 'statuses', 'recipes'] as const) {
      const src = cat[kind] as Record<string, { name: string }>;
      for (const [id, v] of Object.entries(src)) {
        const vi = tr(kind, id, v.name);
        reverse.set(v.name, vi);
        v.name = vi;
      }
    }
    for (const m of Object.values(cat.maps)) {
      if (m.walk) this.grids.set(m.id, Grid.parse(m.walk, m.width, m.height || m.width));
    }
  }

  map(id: string): MapDef | undefined {
    return this.cat.maps[id];
  }
  grid(id: string): Grid | undefined {
    return this.grids.get(id);
  }
  npcsOn(mapId: string): Npc[] {
    return Object.values(this.cat.npcs).filter((n) => n.map_id === mapId);
  }
  speciesName(id: string): string {
    return this.cat.species[id]?.name ?? id;
  }
  itemName(id: string): string {
    return this.cat.items[id]?.name ?? id;
  }
  skillName(id: string): string {
    return this.cat.skills[id]?.name ?? id;
  }
  mapName(id: string): string {
    return this.cat.maps[id]?.name ?? MAP_NAMES[id] ?? id;
  }
}

/** Đổi tên gốc (tiếng Anh) server ghi trong tên pet/sự kiện sang tiếng Việt. */
export function viName(name: string): string {
  return reverse.get(name) ?? name;
}

/** Tên map chưa mở (đích bị khóa) để hiển thị. */
export const MAP_NAMES: Record<string, string> = {
  city_market: 'Thương Phố',
  city_royal_palace: 'Vương Cung',
  city_farm: 'Điền Trang Lục Dã',
  treasure_beach_east_shore: 'Bờ Đông Ngọc Bích',
};

export const STARTERS: Record<string, { name: string; blurb: string }> = {
  tien_chuong: { name: 'Tiên Chưởng', blurb: 'Hệ Quang, thiên về phép: đòn Quang Ba mạnh, sau này học được hồi máu.' },
  sa_hat: { name: 'Sa Hạt', blurb: 'Hệ Thổ, thiên về đánh: chắc chắn, dễ chơi nhất cho người mới.' },
  xich_ung: { name: 'Xích Ưng', blurb: 'Hệ Vô, nhanh nhẹn và trâu bò: thường ra đòn trước.' },
};

export const ELEMENT_VI: Record<string, string> = { earth: 'Thổ', water: 'Thủy', wind: 'Phong', fire: 'Hỏa', neutral: 'Vô', light: 'Quang', dark: 'Ám' };
export const RACE_VI: Record<string, string> = { plant: 'Thực vật', insect: 'Côn trùng', beast: 'Thú', undead: 'Bất tử', dragon: 'Rồng', fish: 'Thủy tộc', bird: 'Phi cầm', demon: 'Ma' };
export const ITEM_DESC: Record<string, string> = {
  capture_seal: 'Dùng trong trận để bắt linh thú hoang. Quái càng yếu máu càng dễ bắt.',
  potion: 'Hồi 35 HP cho linh thú. Dùng được trong và ngoài trận.',
  ether: 'Hồi 20 MP cho linh thú. Dùng được trong và ngoài trận.',
  synthesis_soul: 'Nguyên liệu tổng hợp thế hệ mới ở Điền Trang (mở ở bản sau).',
  blessing_leaf: 'Nguyên liệu cường hóa linh thú (mở ở bản sau).',
};

export const ROLE_LABEL: Record<string, string> = {
  heal: 'Hồi phục',
  shop: 'Cửa hàng',
  learn: 'Học kỹ năng',
  quest: 'Nhiệm vụ',
  teleport: 'Dịch chuyển',
  guild: 'Bang hội',
  exchange: 'Sàn giao dịch',
  warehouse: 'Kho đồ',
  mailbox: 'Hòm thư',
  arena_info: 'Huyết Chiến Đài',
};
/** Chức năng có NPC nhưng chưa có ở server 1.0.0 (nợ N01/N04): báo "chưa mở". */
export const ROLE_NOT_OPEN = new Set(['guild', 'exchange', 'warehouse', 'mailbox', 'arena_info']);

const num = (s: string, i = 0) => Number((s.match(/\d+/g) ?? [])[i] ?? 0);

/** Thông điệp sự kiện tiếng Việt cho log/trận đấu. `unitName` tra tên theo id đơn vị trận. */
export function eventText(e: BattleEvent, unitName: (id?: string) => string = () => ''): string {
  const a = unitName(e.actor_id);
  const t = unitName(e.target_id);
  switch (e.type) {
    case 'battle_start':
      return `Gặp ${viName(e.message.replace(/^Encountered /, ''))}!`;
    case 'skill_cast':
      return `${a} dùng ${viName(e.message.split(' used ')[1] ?? '')}`;
    case 'damage':
      return `${t} mất ${e.amount ?? 0} HP`;
    case 'heal':
      return `${t} hồi ${e.amount ?? 0} HP`;
    case 'miss':
      return `${a} đánh trượt`;
    case 'status_applied':
      return `${t} bị hiệu ứng ${viName(e.message.split(' by ')[1] ?? '')}`;
    case 'status_resisted':
      return `${t} kháng được hiệu ứng`;
    case 'status_cleansed':
      return 'Hiệu ứng được gỡ bỏ';
    case 'status_expired':
      return 'Một hiệu ứng đã hết';
    case 'status_fatal':
      return 'Hiệu ứng chí mạng phát tác';
    case 'buff_applied':
      return `${t || 'Linh thú'} được cường hóa`;
    case 'defend':
      return `${viName(e.message.replace(/ braces for impact$/, ''))} phòng thủ`;
    case 'action_blocked':
      return 'Không thể hành động lượt này';
    case 'item_spend':
      return e.message.includes('binding seal') ? 'Dùng một Phù Phong Ấn' : `Dùng ${viName(e.message.replace(/^Used /, ''))}`;
    case 'pet_capture':
      return `Bắt được ${viName(e.message.split(' joined')[0] ?? '')}!`;
    case 'capture_failed':
      return 'Thú hoang đã thoát ra';
    case 'battle_win':
      return 'Chiến thắng!';
    case 'battle_loss':
      return 'Thất bại…';
    case 'battle_flee':
      return 'Đã chạy thoát';
    case 'battle_capture':
      return 'Trận đấu kết thúc';
    case 'battle_draw':
      return 'Hòa — hết lượt';
    case 'currency_gain':
      return /Earned/.test(e.message) ? `Nhận ${num(e.message)} vàng và ${num(e.message, 1)} EXP` : `Nhận ${num(e.message)} vàng`;
    case 'currency_spend':
      return /Spent/.test(e.message) ? `Tiêu ${num(e.message)} vàng` : 'Đã trả phí';
    case 'item_gain':
      return /Quest supplies/.test(e.message) ? 'Nhận vật phẩm thưởng' : `Nhận ${viName(e.message.replace(/ ×\d+$/, ''))} ×${num(e.message)}`;
    case 'pet_heal':
      return 'Linh thú đã hồi phục';
    case 'pet_learn':
      return `Học được ${viName(e.message.split(' learned ')[1] ?? '')}`;
    case 'pet_activate':
      return `${viName(e.message.replace(/ is following you$/, ''))} đi theo bạn`;
    case 'pet_appraise':
      return 'Đã giám định tiềm năng';
    case 'quest_accept':
      return `Nhận nhiệm vụ: ${e.message}`;
    case 'quest_complete':
      return `Hoàn thành: ${e.message}`;
    case 'starter_chosen':
      return `${viName(e.message.replace(/ đã chọn bạn$/, ''))} đã chọn bạn!`;
    case 'map_enter':
      return `Đến ${e.message}`;
    case 'level_up':
      return e.message;
    default:
      return e.message;
  }
}
