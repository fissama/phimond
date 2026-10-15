"""Sinh .ai/plan/phases/P12-world/review/review-package.json từ roster Stage 4. Chạy: python3 tools/p12_review/build_package.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PH = ROOT / '.ai/plan/phases/P12-world'
OUT = PH / 'review/review-package.json'
NAMES = {
 'summoning_hall_main_hall': 'Triệu Linh Điện', 'emerald_forest_main_woods': 'Bìa Rừng Lục Bảo',
 'emerald_forest_deep_woods': 'Rừng Sâu Lục Bảo', 'city_square': 'Quảng Trường Thạch Trụ',
 'city_market': 'Thương Phố', 'city_palace_gate': 'Hoàng Môn', 'city_royal_palace': 'Vương Cung',
 'city_activity_hall': 'Vạn Sự Hội Sảnh', 'city_pet_room': 'Phòng thú cưng', 'city_farm': 'Điền Trang Lục Dã',
 'city_deathmatch_arena': 'Huyết Chiến Đài', 'treasure_beach_fishermen_beach': 'Bến Ngư Châu',
 'treasure_beach_east_beach': 'Bờ Đông Ngọc Bích', 'treasure_beach_west_beach': 'Bờ Tây Hoàng Sa',
 'treasure_beach_deep_sea': 'Vực Hải Lam', 'treasure_beach_prosperity_island': 'Đảo Phú Quý',
 'middle_corridor_main_hall': 'Hải Tặc Hào'}
TIER = {'main': 'Chính tuyến', 'free': 'Tự do', 'service': 'Dịch vụ'}
ROLE = {'quest': 'nhiệm vụ', 'guide': 'hướng dẫn', 'heal': 'hồi máu', 'shop': 'cửa hàng', 'learn': 'học kỹ năng',
 'free': 'nhiệm vụ phụ', 'teleport': 'trụ dịch chuyển', 'arena': 'đấu trường', 'quest_board': 'bảng nhiệm vụ',
 'story': 'cốt truyện', 'guild': 'bang hội', 'events': 'hoạt động', 'reward': 'phần thưởng', 'appraise': 'giám định',
 'strengthen': 'cường hóa', 'bless': 'ban phúc', 'breed': 'lai tạo', 'recipe': 'công thức', 'hatch': 'ấp trứng',
 'storage': 'gửi/rút pet'}
roster = json.load(open(PH / 'stage4/P12-S4-npc-roster.json', encoding='utf-8'))
dec = [
 {'id': 'S1-SCOPE', 'category': 'Stage 1 · Phạm vi', 'title': 'Phạm vi khảo sát chi tiết (review_detailed_scope)',
  'summary': '17 map: Triệu Linh Điện, 2 map Emerald, 8 map thành (kể cả Điền Trang và Phòng thú cưng là map riêng từng người chơi), 5 map bãi biển và Hải Tặc Hào.',
  'rationale': 'Bạn đã chốt phạm vi trong hội thoại 2026-10-15; thẻ này ghi nhận chính thức thay cho mục review_detailed_scope còn "unresolved" ở app cũ. Duyệt phạm vi không cấp quyền chạy runtime.',
  'columns': ['Map', 'ID'], 'rows': [[v, k] for k, v in NAMES.items()]},
 {'id': 'S3-CLOSE', 'category': 'Stage 3 · Renderer', 'title': 'Chốt Three.js, bỏ benchmark tiếp',
  'summary': 'Client web dùng Three.js (ADR-0001). Không đo thêm trên iPhone 17 Pro Max / macOS Safari; benchmark Stage 3 đóng.',
  'rationale': 'Theo quyết định của bạn 2026-10-15. Hiệu năng sẽ được kiểm ở milestone M0 của kế hoạch port, không còn là điều kiện đóng P12.',
  'columns': [], 'rows': []}]
by = {}
for n in roster: by.setdefault(n['map_id'], []).append(n)
for mid, name in NAMES.items():
    ns = by.get(mid, [])
    new = sum(1 for n in ns if n['new'])
    dec.append({'id': 'S4-NPC-' + mid, 'category': 'Stage 4 · Roster NPC', 'title': name,
      'summary': f'{len(ns)} NPC' + (f' ({new} mới)' if new else '') + '.',
      'rationale': 'Tên và vai trò là đề xuất thiết kế, không lấy từ tên trong APK. Chuỗi nhiệm vụ chính do phase quest quyết.',
      'columns': ['Tên', 'Hạng', 'Vai trò', 'Nguồn', 'Ghi chú'],
      'rows': [[n['name_vi'], TIER[n['tier']], ', '.join(ROLE.get(r, r) for r in n['roles']),
                'MỚI' if n['new'] else 'vị trí APK', n['note']] for n in ns]})
pkg = {'schema_version': 1, 'phase': 'P12', 'revision': 'P12-owner-review-20261015',
 'title': 'P12 · Duyệt một lần: phạm vi, renderer, roster NPC',
 'status': 'Chờ chủ dự án duyệt', 'summary': f'{len(roster)} NPC trên 17 map.', 'decisions': dec}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('decisions', len(dec), 'npcs', len(roster))
