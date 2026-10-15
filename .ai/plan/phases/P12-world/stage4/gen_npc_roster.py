#!/usr/bin/env python3
"""Sinh roster NPC đề xuất (P12 Stage 4). Chạy trong thư mục stage4: python3 -I gen_npc_roster.py
Đọc apk-extract/npcs.json (vị trí NPC gốc APK 3.2); dữ liệu thiết kế nằm trong roster_data.py."""
import json, collections, sys
sys.path.insert(0, ".")
from roster_data import M, R
from roster_outer import M2, R2
M = {**M, **M2}; R = list(R) + list(R2)
SRC = {(r['map'][0], r['name']): r for r in json.load(open('apk-extract/npcs.json', encoding='utf-8'))}
out=[]; used=set()
for m,i,name,tier,roles,so,note in R:
    mid=M[m]; r=None
    if so:
        r=SRC.get((mid,so)); assert r,(mid,so); used.add((mid,so))
    out.append(dict(id=i,map_id=mid,name_vi=name,tier=tier,roles=roles,source_object=so,
        apk_xy=r['xy'] if r else None,apk_sprite=r['sprite'] if r else None,new=so is None,note=note))
unused=[k for k in SRC if k not in used and k[0]!='summoning_hall_main_hall' and k!=('city_farm','Npc')]  # nông trại chỉ còn 1 NPC (Oren)  # 3 biến thể ẩn còn lại của người hướng dẫn
assert not unused, unused
json.dump(out,open('P12-S4-npc-roster.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
by=collections.OrderedDict((v,[]) for v in M.values())
for o in out: by[o['map_id']].append(o)
n_src=sum(1 for o in out if not o['new']); n_new=len(out)-n_src
L=['# P12 Stage 4 — Roster NPC đề xuất (nháp, chờ owner duyệt)\n',
f'{len(out)-1} NPC + 1 hòm thư (vật thể) trong 75 map (17 map phạm vi + 58 map của 11 vùng mở rộng 2026-10-15): {n_src} gắn vào vị trí NPC gốc APK 3.2 (44 slot, chỉ 17 map đầu), {n_new} MỚI (cần đặt vị trí khi vẽ HD-2D). Sinh bằng `gen_npc_roster.py`; tên không dùng tên NPC trong APK.\n',
'**Lưu ý:** tên object trong APK (`thaythuoc`, `TTTD`, `guild`…) là tên prefab, chưa đủ tin cậy để suy vai trò; vai trò ở đây là **thiết kế đề xuất**, chỉ dùng vị trí gốc làm sườn. Tọa độ APK chỉ là bản phác, bản vẽ HD-2D sẽ đặt lại.\n',
'Hạng: **main** = chuỗi nhiệm vụ chính (P04 onboarding; P17 viết truyện sau), **free** = NPC tự do/nhiệm vụ phụ (P18), **service** = dịch vụ.\n',
'## Ma trận phủ theo map\n','| Map | main | free | heal | learn | shop | khác |','|---|---|---|---|---|---|---|']
for mid,os_ in by.items():
    c=collections.Counter()
    for o in os_:
        if o['tier']=='main': c['main']+=1
        if o['tier']=='free' or 'free' in o['roles']: c['free']+=1
        for k in('heal','learn','shop'):
            if k in o['roles']: c[k]+=1
    other=sorted({r for o in os_ for r in o['roles']}-{'quest','heal','learn','shop','free'})
    f=lambda k: c[k] or '—'
    L.append(f"| `{mid}` | {f('main')} | {f('free')} | {f('heal')} | {f('learn')} | {f('shop')} | {', '.join(other) or '—'} |")
for mid,os_ in by.items():
    L+=[f'\n## {mid} ({len(os_)})\n','| Tên | Hạng | Vai trò | Vị trí APK (x,y) | Nguồn | Ghi chú |','|---|---|---|---|---|---|']
    for o in os_:
        xy=', '.join(str(v) for v in o['apk_xy']) if o['apk_xy'] else 'MỚI: chưa đặt'
        L.append(f"| **{o['name_vi']}** (`{o['id']}`) | {o['tier']} | {', '.join(o['roles'])} | {xy} | {o['source_object'] or '—'} | {o['note']} |")
L+=['\n## Phạm vi roster\n',
'Tài liệu này **chỉ soạn NPC** (tên, hạng, vai trò dịch vụ, vị trí sườn). Hạng `main` chỉ đánh dấu NPC dự kiến tham gia tuyến chính; **chuỗi nhiệm vụ chính, thứ tự và nội dung do phase quest quyết (P04/P17)**, không quyết ở P12. Runtime hiện có 4 nhiệm vụ và 5 NPC, roster này không đổi runtime.\n',
'## Quyết định owner\n- Kỹ năng: mỗi điểm dạy là một thầy chung cho mọi race; bậc kỹ năng từng thầy do P13 quyết.\n- Nông trại và Phòng thú cưng là map riêng của từng người chơi (không dùng chung). Nông trại chỉ có Oren (gửi/rút pet); giám định, cường hóa, lai tạo, ấp và dịch vụ pet khác ở Phòng thú cưng, ấp trứng cũng ở đó.\n']
open('P12-S4-npc-roster.md','w',encoding='utf-8').write('\n'.join(L)+'\n')
print(len(out),'NPC;',n_new,'mới')
