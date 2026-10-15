#!/usr/bin/env python3
"""Sinh public/assets/i18n/vi.json: tên hiển thị tiếng Việt cho catalog của server.
Loài: lấy `display_name.vi` từ P10 (data/p10/species.json) qua legacy-species-map.json (nguồn sự thật).
Bốn loài tiến hóa (grove_guardian, tide_sentinel, moon_warden, dawn_sovereign) dùng chung atlas P10 với loài khác
nên có tên riêng do Phimond đặt (không có trong P10) — cần chủ dự án duyệt."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
p10 = json.load(open(os.path.join(ROOT, 'data/p10/species.json')))['records']
smap = json.load(open(os.path.join(os.path.dirname(__file__), 'legacy-species-map.json')))
OWN = {'grove_guardian': 'Hộ Vệ Lùm Cây', 'tide_sentinel': 'Thủy Vệ Triều Dâng', 'moon_warden': 'Nguyệt Thủ', 'dawn_sovereign': 'Hoàng Đế Bình Minh'}
species = {}
for k, v in smap.items():
    if k.startswith('_'): continue
    species[k] = OWN.get(k) or p10[v['species']]['display_name']['vi']
D = {
 'species': species,
 'maps': {'severa': 'Quảng Trường Thạch Trụ', 'forest': 'Bìa Rừng Lục Bảo', 'beach': 'Bến Ngư Châu', 'ranch': 'Điền Trang Lục Dã', 'arena': 'Huyết Chiến Đài'},
 'npcs': {'trainer': 'Huấn Luyện Viên Elin', 'ranch_keeper': 'Quản Trang Oren', 'arena_master': 'Đài Chủ Vale', 'forest_guide': 'Kiểm Lâm Lio', 'beach_guide': 'Hoa Tiêu Nia'},
 'items': {'capture_seal': 'Phù Phong Ấn', 'potion': 'Thuốc Rễ Dại', 'ether': 'Sương Tinh Tú', 'synthesis_soul': 'Hồn Hợp Thành', 'blessing_leaf': 'Lá Chúc Phúc'},
 'skills': {'attack': 'Đòn Đánh', 'earth_strike': 'Địa Chấn', 'petrify': 'Hóa Đá', 'cleanse_doom': 'Giải Tử Chú', 'insect_boon': 'Phúc Trùng', 'water_strike': 'Thủy Chấn', 'doom': 'Tử Chú', 'cleanse_sleep': 'Giải Ngủ', 'spirit_boon': 'Phúc Linh', 'wind_strike': 'Phong Chấn', 'sleep': 'Ngủ', 'cleanse_silence': 'Giải Câm Lặng', 'bird_boon': 'Phúc Điểu', 'fire_strike': 'Hỏa Chấn', 'silence': 'Câm Lặng', 'cleanse_bind': 'Giải Trói', 'demon_boon': 'Phúc Ma', 'neutral_strike': 'Vô Chấn', 'bind': 'Trói Buộc', 'beast_boon': 'Phúc Thú', 'light_strike': 'Quang Chấn', 'blind': 'Mù Lòa', 'cleanse_confusion': 'Giải Hỗn Loạn', 'plant_boon': 'Phúc Thảo', 'dark_strike': 'Ám Chấn', 'confusion': 'Hỗn Loạn', 'cleanse_petrify': 'Giải Hóa Đá', 'undead_boon': 'Phúc Vong', 'mend': 'Ánh Sáng Chữa Lành'},
 'statuses': {'petrify': 'Hóa Đá', 'doom': 'Tử Chú', 'sleep': 'Ngủ', 'silence': 'Câm Lặng', 'bind': 'Trói Buộc', 'blind': 'Mù Lòa', 'confusion': 'Hỗn Loạn'},
 'quests': {
  'first_steps': {'name': 'Bước vào màu xanh', 'description': 'Đến Bìa Rừng Lục Bảo rồi nói chuyện với người dẫn đường.'},
  'first_capture': {'name': 'Mối giao ước đầu tiên', 'description': 'Làm yếu và bắt một linh thú hoang dã.'},
  'field_training': {'name': 'Học từ hoang dã', 'description': 'Thắng ba trận chiến với linh thú hoang dã.'},
  'next_generation': {'name': 'Gốc rễ và cành nhánh', 'description': 'Hợp thành một thế hệ mới tại điền trang.'}},
 'recipes': {'snail_refinement': 'Tinh luyện Ốc Sên Rêu', 'grove_guardian': 'Hợp thành Hộ Vệ Lùm Cây', 'guardian_refinement': 'Tinh luyện Hộ Vệ Lùm Cây', 'tide_sentinel': 'Hợp thành Thủy Vệ Triều Dâng', 'moon_warden': 'Hợp thành Nguyệt Thủ', 'dawn_sovereign': 'Hợp thành Hoàng Đế Bình Minh'},
}
out = os.path.join(ROOT, 'apps/game-web/public/assets/i18n'); os.makedirs(out, exist_ok=True)
json.dump(D, open(os.path.join(out, 'vi.json'), 'w'), ensure_ascii=False, indent=1)
print('ok', {k: len(v) for k, v in D.items()})
