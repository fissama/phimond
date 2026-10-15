"""Sinh .ai/plan/phases/P12-world/review/review-package.json từ roster Stage 4. Chạy: python3 tools/p12_review/build_package.py"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PH = ROOT / '.ai/plan/phases/P12-world'
sys.path.insert(0, str(PH / 'stage4'))
from roster_outer import NAME as ONAME, REGIONS
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
 'storage': 'gửi/rút pet', 'exchange': 'sàn giao dịch', 'warehouse': 'kho đồ', 'mailbox': 'hòm thư', 'smith': 'rèn trang bị'}
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
dec.append({'id': 'S1-SCOPE-EXT', 'category': 'Stage 1 · Phạm vi', 'title': 'Mở rộng: 58 map của 11 vùng ngoài 17 map',
  'summary': 'Sa Mạc, Mỏm Đá Gió, Đảo Ác Mộng, Lăng Mộ, Giao Điểm và 6 vùng cao Lv40+ (Tinh Không, Di Tích Cổ, Lâu Đài Ma, Cây Thế Giới, Tháp Chim, Mê Thành). Chỉ phần NPC; portal, cấp và vùng an toàn đã có ở thiết kế.',
  'rationale': 'Owner yêu cầu 2026-10-15. Các map này vẫn ngoài phạm vi ma trận portal chi tiết; roster dùng số slot NPC trong APK 3.2, chưa có vị trí.',
  'columns': ['Vùng', 'Map'], 'rows': [[r, ', '.join(ONAME[m] for m in ms)] for _, r, ms in REGIONS]})
for mid, name in NAMES.items():
    ns = by.get(mid, [])
    new = sum(1 for n in ns if n['new'])
    dec.append({'id': 'S4-NPC-' + mid, 'category': 'Stage 4 · Roster NPC', 'title': name,
      'summary': f'{len(ns)} NPC' + (f' ({new} mới)' if new else '') + '.',
      'rationale': 'Tên và vai trò là đề xuất thiết kế, không lấy từ tên trong APK. Chuỗi nhiệm vụ chính do phase quest quyết.',
      'columns': ['Tên', 'Hạng', 'Vai trò', 'Nguồn', 'Ghi chú'],
      'rows': [[n['name_vi'], TIER[n['tier']], ', '.join(ROLE.get(r, r) for r in n['roles']),
                'MỚI' if n['new'] else 'vị trí APK', n['note']] for n in ns]})
for key, rname, ms in REGIONS:
    ns = [n for m in ms for n in by.get(m, [])]
    rows = [[ONAME[n['map_id']], n['name_vi'], TIER[n['tier']], ', '.join(ROLE.get(r, r) for r in n['roles']), n['note'].replace('MỚI (vị trí chưa trích từ APK). ', '')] for n in ns]
    nomap = [ONAME[m] for m in ms if not by.get(m)]
    dec.append({'id': 'S4-NPC-REG-' + key, 'category': 'Stage 4 · Roster NPC (vùng ngoài)', 'title': rname,
      'summary': f'{len(ns)} NPC trên {len(ms)} map.' + (f' Không có NPC: {", ".join(nomap)}.' if nomap else ''),
      'rationale': 'Hub an toàn có hồi máu/cửa hàng/kỹ năng; map quái chỉ NPC nhiệm vụ phụ. Tên là đề xuất, không lấy từ APK.',
      'columns': ['Map', 'Tên', 'Hạng', 'Vai trò', 'Ghi chú'], 'rows': rows})
pkg = {'schema_version': 1, 'phase': 'P12', 'revision': 'P12-owner-review-20261015',
 'title': 'P12 · Duyệt một lần: phạm vi, renderer, roster NPC',
 'status': 'Chờ chủ dự án duyệt', 'summary': f'{len(roster)} mục (106 NPC + 1 hòm thư) trên 75 map.', 'decisions': dec}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('decisions', len(dec), 'npcs', len(roster))
