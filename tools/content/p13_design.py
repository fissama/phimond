"""P13 authoring + exact arithmetic probes. Never loaded by the game server."""
import collections
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / '.ai/plan/phases/P13-skills'
P11 = ROOT / '.ai/plan/phases/P11-stats/P11-species-catalog.json'
RACES = {'undead':'Vong Linh','plant':'Thực Vật','dragon':'Rồng','demon':'Ác Ma','beast':'Thú','bird':'Chim','insect':'Côn Trùng','spirit':'Linh'}
ELEMENTS = [('fire','Hỏa','#dc6544'),('water','Thủy','#318ac2'),('wind','Phong','#479b87'),('earth','Địa','#aa864a'),('light','Quang','#bd9a24'),('dark','Âm','#8564ad')]
ALL_RACES = list(RACES)
ROLE_NAMES = {'physical_dps':'Vật lý','magic_dps':'Phép','hybrid':'Song công','tank':'Chống chịu','support':'Hỗ trợ','disruptor':'Khống chế'}


def damage(offense, defense, power, element=Fraction(1), crit=Fraction(1)):
    offense, defense = max(Fraction(0), Fraction(str(offense))), max(Fraction(0), Fraction(str(defense)))
    if offense == 0:
        return 0
    x = offense * power * 100 / (100 + defense) * element * crit
    return max(1, x.numerator // x.denominator)


def status_chance(p, sr):
    s = max(Fraction(0), Fraction(str(sr)))
    return p * (1 - Fraction(4, 5) * s / (s + 100))


def inherited_pool(a, b, race, skills):
    return sorted({sid for sid in a + b if race in skills[sid]['inheritance']})


def skill(sid, name, kind, target, mp, cd, level, description, functions, inheritance=None, element='neutral', power=None, effect=None, source_ids=None):
    return {'id':sid,'name':name,'kind':kind,'target':target,'mp':mp,'cooldown':cd,'learn_level':level,
            'element':element,'description':description,'functions':functions,
            'inheritance':ALL_RACES if inheritance is None else inheritance,
            'power':power,'effect':effect,'source_ids':source_ids or [],
            'provenance':'adapted_source' if source_ids else 'phimond_authored',
            'rank_policy':'damage_heal_3_ranks' if kind in ('physical','magic','heal') else 'fixed_rank_1',
            'action_channel':'physical' if kind == 'physical' else ('utility' if sid in ['guard','counter','beast_instinct','resilience','protect','haste','attack_up'] else 'magic')}


def build_skills():
    S=[]
    def add(*a,**kw):S.append(skill(*a,**kw))
    add('strike','Cường kích','physical','enemy_one',8,0,1,'Một địch, 1.20×ATK; không hiệu ứng phụ.',['physical_dps','hybrid'],power='1.20')
    add('sweep','Càn quét','physical','enemy_all',18,1,5,'Mỗi địch 0.75×ATK; tổng 2.25× khi có 3 địch.',['physical_dps','hybrid'],power='0.75',source_ids=['CanQuetNhe','CanQuet','CanQuetCaoCap','CanQuetSieuCap'])
    add('pierce','Xuyên giáp','physical','enemy_one',12,1,10,'1.00×ATK, bỏ qua 30% DEF hiệu lực; không bỏ qua khiên.',['physical_dps','hybrid'],power='1.00',effect={'penetration':0.30})
    add('double','Liên kích','physical','enemy_one',12,1,10,'Hai hit 0.60×ATK; hit/crit riêng; cùng target, không đổi mục tiêu nếu chết.',['physical_dps','hybrid'],power='0.60',effect={'hits':2})
    add('drain','Công kích hút máu','physical','enemy_one',16,2,20,'1.10×ATK; hồi 25% HP thực sự mất của target, sau khiên; không từ overkill.',['physical_dps','hybrid'],power='1.10',source_ids=['CongKichHutMau'])
    add('counter','Phản kích','buff','self',12,2,10,'2 vòng: tối đa 1 phản kích/vòng, 0.50×ATK sau khi sống sót qua đòn trực tiếp; không phản đòn phản kích/DoT.',['tank'],inheritance=['beast','dragon','undead','insect'],source_ids=['PhanKich'])
    source={'fire':'LamNong','water':'BaoTuyet','wind':'ThuatLocXoay','earth':'ThuatNutDat','light':'CuDanhThoiSon','dark':'HuyDiet'}
    for e,n,c in ELEMENTS:
        add('bolt_'+e,'Linh kích '+n,'magic','enemy_one',10,0,1,'1.20×MAG, một địch; bảng hệ theo skill và target.',['magic_dps','hybrid'],element=e,power='1.20')
        add('wave_'+e,{'fire':'Làm nóng','water':'Bão tuyết','wind':'Lốc xoáy','earth':'Nứt đất','light':'Quang minh','dark':'Hủy diệt'}[e],'magic','enemy_all',20,1,5,'Mỗi địch 0.75×MAG; không tự gây control theo tên/element.',['magic_dps','hybrid'],element=e,power='0.75',source_ids=[source[e]+'Nhe',source[e],source[e]+'CaoCap',{'fire':'HoaThieuSieuCap','water':'HanBangSieuCap','wind':'ThanPhongSieuCap','earth':'DaiDiaSieuCap','light':'QuangMinhSieuCap','dark':'HacAmSieuCap'}[e]])
        add('claw_'+e,'Lợi trảo '+n,'physical','enemy_one',10,0,5,'1.10×ATK với element ghi rõ; không STAB.',['physical_dps','hybrid'],element=e,power='1.10')
    add('heal','Trị liệu','heal','ally_one',14,1,1,'Hồi floor(1.50×MAG + 10) HP; self hợp lệ; không hồi sinh.',['support'],source_ids=['TriLieu'])
    add('group_heal','Trị liệu nhóm','heal','ally_all',28,2,20,'Mỗi đồng minh còn sống hồi floor(0.85×MAG + 6); solo chỉ hồi một pet.',['support'],inheritance=['plant','bird','spirit'],source_ids=['TriLieuNhom','TriLieuNhomSieuCap'])
    add('shield','Hộ thuẫn','shield','ally_one',14,2,5,'Khiên floor(1.20×MAG + 0.08×maxHP người thi triển), 2 vòng; cùng loại giữ lượng lớn hơn, không cộng dồn.',['tank','support'])
    add('guard','Giáp hộ thân','buff','self',10,2,1,'DEF +25% trong 2 vòng, một nhóm armor; không nhân vô hạn.',['tank'],source_ids=['ThuatTaoVo'])
    add('protect','Che chở','buff','ally_one',16,2,10,'Cho ally/self DEF +20% trong 2 vòng; thay nhóm armor nếu mạnh hơn, không chuyển sát thương giữa actor.',['tank','support'])
    add('regen','Tái sinh','buff','ally_one',16,3,15,'2 lần cuối vòng kế tiếp, mỗi lần hồi floor(0.60×MAG + 4); paid active, không passive/free heal.',['support','tank'],inheritance=['plant','beast'],source_ids=['TaiSinh'])
    add('haste','Cấp tốc','buff','ally_one',12,2,10,'SPD +20% trong 2 vòng; có hiệu lực từ danh sách hành động vòng sau, không thêm lượt.',['support'],inheritance=['bird','beast'],source_ids=['TangToc'])
    add('beast_instinct','Thú tính','buff','self',12,2,10,'ATK +20% trong 2 vòng, DEF −10% trong cùng thời gian; trả giá bằng chống chịu.',['physical_dps','hybrid'],inheritance=['beast','dragon'],source_ids=['ThuTinh'])
    add('meditate','Suy tưởng','resource','ally_other',12,2,15,'Chuyển 10 MP tới đồng minh khác, hao hụt 2 MP và 1 action; không dùng lên self, không tạo MP.',['support'],inheritance=['spirit','beast'],source_ids=['SuyTuong'])
    add('attack_up','Thiên thần hạ phàm','buff','ally_all',24,3,20,'ATK cả đội +20% trong 2 vòng, nhóm might; solo vẫn buff self.',['support'],source_ids=['ThienThanHaPham'])
    add('magic_up','Tim ác ma','buff','ally_all',24,3,20,'MAG cả đội +20% trong 2 vòng, nhóm intellect.',['support'],source_ids=['TimAcMa'])
    add('magic_focus','Tập trung pháp lực','buff','self',10,2,10,'MAG +20% trong 2 vòng; không hồi MP.',['magic_dps','hybrid'])
    add('resilience','Kiên tâm','buff','self',10,3,10,'SR +25% trong 2 vòng; không miễn nhiễm, không tăng tỉ lệ gây status.',['tank'])
    add('revive','Thuật phục sinh','revive','ally_fainted',35,4,40,'Hồi sinh ally khác đã chết, 25% maxHP, giữ MP hiện tại; tối đa 1 lần/actor/battle, không tự hồi sinh.',['support'],inheritance=[],source_ids=['PhucSinh','TrungSinh'])
    add('sleep','Ngủ say','control','enemy_one',16,3,15,'75% base chance: mất tối đa 1 action; direct hit đánh thức, không bonus damage.',['disruptor'],inheritance=['bird','plant'],effect={'status':'sleep','chance':0.75},source_ids=['NguSay'])
    add('bind','Trói buộc','control','enemy_one',14,2,10,'80% base chance: chặn action vật lý trong 2 vòng; magic/support hợp lệ, basic sẽ bị chặn.',['disruptor'],inheritance=['beast','plant','insect'],effect={'status':'bind','chance':0.80},source_ids=['TroiBuoc'])
    add('silence','Trầm mặc','control','enemy_one',14,2,10,'80% base chance: chặn skill channel magic (gồm heal/shield/control/resource) trong 2 vòng; channel physical/utility và basic vẫn hợp lệ; channel ghi từng skill.',['disruptor'],inheritance=['demon','bird'],effect={'status':'silence','chance':0.80},source_ids=['TramMac'])
    add('blind','Làm mù','debuff','enemy_one',12,2,10,'85% base chance: accuracy −20 điểm phần trăm trong 2 vòng; không làm mọi đòn chắc miss.',['disruptor'],inheritance=['plant','beast','bird'],effect={'status':'blind','chance':0.85},source_ids=['LamMu'])
    add('petrify','Hóa đá','control','enemy_one',20,3,20,'70% base chance: mất tối đa 1 action, DEF +25% khi tồn tại; vẫn nhận damage, không miễn nhiễm toàn phần.',['disruptor'],inheritance=['insect','dragon'],effect={'status':'petrify','chance':0.70},source_ids=['HoaDa'])
    add('confuse','Hỗn loạn','control','enemy_one',18,3,15,'75% base chance: action kế tiếp thành basic vào một địch sống do server RNG chọn; không tấn công phe mình.',['disruptor'],inheritance=['undead','spirit'],effect={'status':'confuse','chance':0.75},source_ids=['HonLoan'])
    add('misfortune','Vận xui','debuff','enemy_one',14,2,15,'80% base chance: lượng HP được hồi −25% trong 2 vòng; có thể giải, không tử hình tức thì.',['disruptor'],inheritance=['spirit','undead','insect'],effect={'status':'misfortune','chance':0.80},source_ids=['VanXui'])
    for sid,name,stat in [('weaken_atk','Suy nhược','atk'),('weaken_mag','Tán linh','mag'),('break_def','Phá giáp','def'),('slow','Trì hoãn','spd')]:
        add(sid,name,'debuff','enemy_one',12,2,10,'85% base chance: '+stat.upper()+' −20% trong 2 vòng; áp dụng pipeline P11.',['disruptor'],effect={'stat':stat,'amount':-0.20,'chance':0.85})
    add('frailty','Sinh lực suy yếu','debuff','enemy_one',14,2,15,'80% base chance: ATK và MAG −10% trong 2 vòng; thích ứng brief max-HP impairment để không tạo free heal/maxHP exploit.',['disruptor'],effect={'status':'frailty','chance':0.80})
    add('poison','Độc châm','physical','enemy_one',14,2,10,'0.80×ATK; sau hit, 70% base chance độc: mỗi tick 0.30×ATK nguồn, 2 tick. Độc đơn thuần không tạo role Disruptor.',['physical_dps','hybrid'],inheritance=['insect','bird','undead'],power='0.80',effect={'status':'poison','chance':0.70})
    add('burn','Hỏa ấn','magic','enemy_one',14,2,10,'0.80×MAG Hỏa; sau hit, 70% base chance cháy: mỗi tick 0.30×MAG nguồn, 2 tick.',['magic_dps','hybrid'],element='fire',power='0.80',effect={'status':'burn','chance':0.70})
    add('cleanse','Thanh tẩy','cleanse','ally_one',16,2,10,'Gỡ 1 trạng thái xấu: control action trước, rồi silence/bind, rồi debuff, rồi DoT; hòa theo thời điểm cũ hơn.',['support'])
    for sid,name,status,src in [('wake','Thức tỉnh','sleep','ThucTinh'),('free','Chúc phúc tự do','bind','ChucPhucTuDo'),('song','Ca hát','silence','CaHat'),('sight','Làm sáng lại','blind','LamSangLai'),('dissolve','Hòa tan','petrify','HoaTan'),('order','Trật tự','confuse','TratTu'),('bless','Ban phước','misfortune','BanPhuoc')]:
        add(sid,name,'cleanse','ally_one',8,1,5,'Gỡ '+status+' cho ally/self; nếu không có status này, target không hợp lệ, không mất MP/action.',['support'],effect={'cleanse':status},source_ids=[src])
    add('dispel','Phá phù','dispel','enemy_one',14,2,15,'Gỡ 1 buff: shield trước, rồi ATK/MAG, armor, SPD/SR; không gây damage; kiểm tra hit, không qua SR.',['disruptor'])
    add('extinguish','Dập lửa','cleanse','ally_one',8,1,5,'Gỡ cháy; thêm khiên floor(0.50×MAG) trong 1 vòng. Target cần có burn.',['support'],element='water')
    add('mana_burn','Thiêu đốt pháp lực','magic','enemy_one',18,2,20,'0.75×MAG damage; target mất tối đa floor(0.20×MAG nguồn) MP, tối đa 10 MP/hit; không chuyển MP về nguồn.',['magic_dps','disruptor','hybrid'],power='0.75',source_ids=['ThieuDotPhapLuc'])
    add('dragon_breath','Uy rồng phả hơi','magic','enemy_one',28,3,40,'1.70×MAG Quang, một địch; signature Thánh Rồng Thái Cổ, không kế thừa.',['magic_dps','hybrid'],inheritance=[],element='light',power='1.70',source_ids=['UyRongPhaHoi'])
    add('death_scythe','Lưỡi hái tử thần','physical','enemy_one',26,3,40,'1.50×ATK Âm + mark nhận hồi phục −25% (70% base chance), 2 vòng; giải được, không instant kill.',['physical_dps'],inheritance=[],element='dark',power='1.50',effect={'status':'misfortune','chance':0.70},source_ids=['LuoiHai'])
    add('love_kiss','Nụ hôn Ái Thần','shield','ally_one',26,3,40,'Khiên floor(1.80×MAG + 0.10×maxHP nguồn), 1 vòng; không miễn nhiễm. Signature Chim Ái Thần, không kế thừa.',['support'],inheritance=[],source_ids=['NuHon'])
    # Owner review v8: authored species-exclusive kits, not recovered APK rules.
    signatures=[
        ('azure_tide','Thanh Long · Triều áp','species_0068','magic','enemy_one',24,30,'water','1.10',{'status':'slow','chance':0.70,'amount':-0.20},['magic_dps','hybrid'],'1.10×MAG Thủy; sau hit, 70% base chance SPD target −20% trong 2 vòng. Giải debuff được; không thêm damage khi dập burn.'),
        ('tiger_gale','Bạch Hổ · Phong trảo','species_0087','physical','enemy_one',24,30,'wind','1.25',{'self_buff':'spd','amount':0.20},['physical_dps'],'1.25×ATK Phong; sau hit thành công, self SPD +20% trong 2 vòng. Không thêm lượt; cùng nhóm haste, có thể dispel.'),
        ('vermilion_ember','Chu Tước · Ly hỏa','species_0105','magic','enemy_one',24,30,'fire','1.10',{'status':'burn','chance':0.70,'tick_power':'0.30'},['magic_dps'],'1.10×MAG Hỏa; sau hit, 70% base chance burn 0.30×MAG nguồn mỗi tick, 2 tick. Water/cleanse dập được, không hồi sinh tự động.'),
        ('turtle_tide','Huyền Vũ · Thủy giáp','species_0139','shield','ally_one',24,30,'water',None,{'cleanse':'burn','shield_mag':'1.20','shield_hp':'0.08'},['tank','support'],'Gỡ burn nếu có rồi tạo khiên floor(1.20×MAG + 8%maxHP nguồn), 2 vòng. Ally/self còn sống hợp lệ dù không có burn; shield giữ strongest, dispel được.'),
        ('empress_eclipse','Nữ Đế · Minh ấn','species_0019','magic','enemy_one',28,40,'dark','1.40',{'status':'misfortune','chance':0.70},['magic_dps','disruptor'],'1.40×MAG Âm; sau hit, 70% base chance giảm HP được hồi 25% trong 2 vòng, cùng misfortune. Cleanse được; không instant kill.'),
        ('giant_bastion','Cự Ma · Địa chấn hộ thể','species_0142','physical','enemy_one',28,40,'earth','1.40',{'self_buff':'def','amount':0.25},['physical_dps','tank'],'1.40×ATK Địa; sau hit thành công, self DEF +25% trong 2 vòng, cùng nhóm armor. Có thể dispel, không bỏ qua DEF target.'),
        ('flower_radiance','Hoa Hương · Quang tịnh','species_0144','heal','ally_one',28,40,'light',None,{'cleanse_one':True,'heal_mag':'1.50','heal_flat':10},['support'],'Gỡ 1 status xấu theo priority cleanse, rồi hồi floor(1.50×MAG + 10) HP. Ally/self sống hợp lệ nếu thiếu HP hoặc có status xấu; không revive, không refill MP.')]
    for sid,name,owner,kind,target,mp,level,element,power,effect,functions,desc in signatures:
        add(sid,name,kind,target,mp,3,level,desc+' Độc quyền '+owner+'; chiếm 1/6 slot, rank1 cố định, không kế thừa.',functions,inheritance=[],element=element,power=power,effect=effect)
        S[-1].update(exclusive_species=owner,rank_policy='fixed_rank_1')
    # Keep APK tier identities as independent selectable skills; never auto-upgrade light.
    source_rows={r['id']:r for r in json.loads((PHASE/'evidence/apk84-skills.json').read_text())['rows']}
    for base in [s for s in list(S) if s['id']=='sweep' or s['id'].startswith('wave_')]:
        source_ids=list(base['source_ids']);physical=base['kind']=='physical'
        powers=['0.45','0.75','1.05','1.35'];costs=[10,18,26,36] if physical else [12,20,28,38]
        for i,(suffix,level,cd) in enumerate([('_light',1,0),('',5,1),('_advanced',20,1),('_super',40,2)]):
            sid=base['id']+suffix;source_id=source_ids[i]
            desc=f"AoE tất cả địch; mỗi target {powers[i]}×{'ATK' if physical else 'MAG'}, hit/crit riêng. Damage thuần, không status. Tier{' nhẹ cho farm ít MP' if i==0 else ' mạnh hơn, trả thêm MP'}; không xóa/thay tier khác."
            row=skill(sid,source_rows[source_id]['name'].strip(),base['kind'],'enemy_all',costs[i],cd,level,desc,base['functions'],inheritance=base['inheritance'],element=base['element'],power=powers[i],source_ids=[source_id])
            row.update(tier_family=base['id'],tier_index=i+1,rank_policy='fixed_rank_1')
            if suffix:S.append(row)
            else:base.clear();base.update(row)
    group=next(s for s in S if s['id']=='group_heal');group['source_ids']=['TriLieuNhom']
    group.update(tier_family='group_heal',tier_index=1,rank_policy='fixed_rank_1')
    add('group_heal_super','Trị liệu nhóm siêu cấp','heal','ally_all',40,3,40,'Mỗi ally sống hồi floor(1.10×MAG+10); heal cả đội, không damage, không revive. Skill riêng, giữ trị liệu nhóm ít MP.',['support'],inheritance=group['inheritance'],effect={'heal_mag':'1.10','heal_flat':10},source_ids=['TriLieuNhomSieuCap'])
    S[-1].update(tier_family='group_heal',tier_index=2,rank_policy='fixed_rank_1')
    for row in S:
        row['target_shape']='aoe' if row['target'] in ['enemy_all','ally_all'] else 'single'
        row['damage_mode']='damage_with_effect' if row['kind'] in ['physical','magic'] and (row['effect'] or row['id']=='drain') else ('damage_only' if row['kind'] in ['physical','magic'] else 'effect_only')
    return S


ROLE_POOLS={'physical_dps':['strike','sweep','pierce'], 'magic_dps':['BOLT','WAVE','magic_focus'], 'hybrid':['strike','BOLT','sweep','WAVE'], 'tank':['guard','shield','protect'], 'support':['heal','shield','cleanse','attack_up'], 'disruptor':['weaken_atk','slow','dispel']}
RACE_POOLS={'undead':['resilience','confuse','order'], 'plant':['regen','blind','sight'], 'dragon':['guard','petrify','dissolve'], 'demon':['beast_instinct','silence','song'], 'beast':['beast_instinct','bind','free'], 'bird':['haste','sleep','wake'], 'insect':['poison','petrify','dissolve'], 'spirit':['magic_focus','misfortune','bless']}
# Explicit named accents, not random/modulo assignment. These preserve source/P11 briefs.
ACCENTS={
'0001':['poison'],'0002':['heal'],'0003':['counter'],'0004':['misfortune'],'0005':['resilience'],'0006':['drain'],
'0007':['claw_fire'],'0008':['heal'],'0009':['double'],'0010':['counter'],'0011':['counter','drain'],'0012':['weaken_mag'],'0013':['cleanse'],'0014':['magic_up'],'0015':['dissolve','death_scythe'],'0016':['confuse'],'0017':['claw_water'],'0018':['protect'],'0019':['silence'],'0020':['counter'],
'0021':['counter'],'0022':['group_heal'],'0023':['sleep'],'0024':['wave_earth'],'0025':['wave_water'],'0026':['counter'],'0027':['weaken_atk'],'0028':['group_heal'],'0029':['heal'],'0030':['bind'],'0031':['double'],'0032':['counter'],'0033':['break_def'],'0034':['bind'],'0035':['group_heal'],'0036':['double'],'0037':['bind','bolt_earth'],'0038':['group_heal','guard'],
'0039':['claw_wind'],'0040':['burn'],'0041':['shield'],'0042':['heal'],'0043':['weaken_atk'],'0044':['break_def'],'0045':['bolt_earth'],'0046':['magic_focus'],'0047':['attack_up'],'0048':['wave_wind'],'0049':['weaken_mag'],'0050':['silence'],'0051':['drain'],'0052':['dragon_breath','protect'],
'0053':['burn'],'0054':['heal'],'0055':['heal'],'0056':['counter'],'0057':['double'],'0058':['pierce'],'0059':['counter'],'0060':['counter'],'0061':['mana_burn'],'0062':['weaken_atk'],'0063':['counter'],'0064':['bind','weaken_atk'],'0065':['magic_focus'],'0066':['weaken_mag'],'0067':['counter'],'0068':['wave_water'],'0069':['protect'],
'0070':['double'],'0071':['claw_fire'],'0072':['bind'],'0073':['protect'],'0074':['drain'],'0075':['guard'],'0076':['pierce','counter'],'0077':['haste'],'0078':['group_heal'],'0079':['blind'],'0080':['counter'],'0081':['attack_up'],'0082':['sweep'],'0083':['meditate','magic_up'],'0084':['bind'],'0085':['blind'],'0086':['wave_light'],'0087':['double'],'0088':['claw_fire','drain'],
'0089':['heal'],'0090':['confuse'],'0091':['double'],'0092':['sweep'],'0093':['heal'],'0094':['wave_wind'],'0095':['pierce'],'0096':['mana_burn'],'0097':['slow'],'0098':['haste'],'0099':['resilience'],'0100':['poison'],'0101':['slow'],'0102':['burn'],'0103':['sleep','slow'],'0104':['song'],'0105':['heal'],'0106':['slow'],'0107':['pierce','claw_wind'],
'0108':['double'],'0109':['wave_earth'],'0110':['counter'],'0111':['guard'],'0112':['pierce'],'0113':['bolt_earth'],'0114':['counter'],'0115':['frailty'],'0116':['poison'],'0117':['guard'],'0118':['group_heal'],'0119':['strike','bolt_water'],'0120':['bless','protect'],'0121':['frailty'],'0122':['misfortune'],'0123':['petrify'],'0124':['counter'],'0125':['wave_light'],'0126':['group_heal','bind'],
'0127':['heal'],'0128':['wave_wind'],'0129':['counter'],'0130':['resilience'],'0131':['mana_burn'],'0132':['heal'],'0133':['drain'],'0134':['weaken_atk'],'0135':['guard'],'0136':['bind'],'0137':['misfortune'],'0138':['weaken_mag'],'0139':['protect'],'0140':['double'],'0141':['magic_up'],'0142':['counter'],'0143':['shield','magic_up'],
'0144':['group_heal'],'0145':['group_heal','protect'],'0146':['mana_burn','heal'],'0147':['counter'],'0148':['protect'],'0149':['claw_light'],'0150':['protect','heal'],'0151':['bind'],'0152':['group_heal','love_kiss']}


def build_species(skills, records=None, species_accents=None):
    records=json.loads(P11.read_text())['records'] if records is None else records
    accents=ACCENTS if species_accents is None else species_accents
    rows=[]
    for sid,r in records.items():
        element=r['element_id']; roles=r['role_ids']; pool=[]
        for role in roles:
            for x in ROLE_POOLS[role]:pool.append({'BOLT':'bolt_'+element,'WAVE':'wave_'+element}.get(x,x))
        pool+=RACE_POOLS[r['race_id']]
        pool+=accents[sid[-4:]]
        exclusive=[s['id'] for s in skills if s.get('exclusive_species')==sid]
        pool+=exclusive
        if r['primary_role'] in ['physical_dps','hybrid']:pool.append('claw_'+element)
        if 'support' in roles and r['star']>=3:pool.append('group_heal')
        if 'support' in roles and r['star']>=4 and r['race_id'] in ['plant','bird','spirit']:pool.append('revive')
        families={s['tier_family'] for s in skills if s.get('tier_family')}
        expanded=[]
        for x in pool:
            expanded.extend([s['id'] for s in sorted(skills,key=lambda s:s.get('tier_index',0)) if s.get('tier_family')==x] if x in families else [x])
        pool=expanded
        pool=list(dict.fromkeys(pool))
        # Build is a demonstrator chosen by Primary -> Secondary -> explicit accent.
        # Native pool remains content, not automatic learned skills.
        priority=exclusive+accents[sid[-4:]]+(['claw_'+element] if roles[0] in ['physical_dps','hybrid'] else [])+ROLE_POOLS[roles[0]]
        if len(roles)>1:priority+=ROLE_POOLS[roles[1]][:2]
        priority+=RACE_POOLS[r['race_id']]+pool
        build=[]
        for x in priority:
            x={'BOLT':'bolt_'+element,'WAVE':'wave_'+element}.get(x,x)
            # Illustrative farm kit may carry light and regular simultaneously.
            if x in families and x+'_light' in pool and x+'_light' not in build:
                build.append(x+'_light')
                if len(build)==6:break
            if x in pool and x not in build:build.append(x)
            if len(build)==6:break
        rows.append({'id':sid,'name':r['name_vi'],'race':r['race_id'],'race_name':RACES[r['race_id']],'star':r['star'],
                     'class':r['species_class'],'element':element,'roles':roles,'role_names':[ROLE_NAMES[x] for x in roles],
                     'native_skills':pool,'sample_build':build,'rationale':r['rationale'],
                     'native_brief':r['p13_native_pool_contract'],'source_description':r['source_description_vi'],
                     'provenance':'phimond_authored_pending_owner_acceptance',
                     'source_identity':r['source_identity'],'base_stats':r['base_stats'],'growth_baseline':r['growth_baseline']})
    return rows


def decision(i,title,summary,rationale,alternatives,acceptance,impact,category='Luật chiến đấu',evidence=None):
    return {'id':f'P13-D{i:02d}','category':category,'title':title,'summary':summary,'rationale':rationale,
            'alternatives':alternatives,'acceptance':acceptance,'impact':impact,'evidence':evidence or ['P13-R01–R06','P11 F04'],
            'authority':'candidate_pending_owner_acceptance'}


def build_decisions():
    return [
    decision(1,'Giữ skill nhẹ và tier gốc APK','7 chuỗi AoE giữ4 skill riêng Nhẹ/Thường/Cao cấp/Siêu cấp, đúng tên và ID nguồn. Trị liệu nhóm/siêu cấp cũng riêng. Tier không gộp rank; học tier mạnh vẫn giữ tier nhẹ.','Owner yêu cầu farm ítMP. Source target/channel/name có chứng cứ; Mana/Dame raw chưa hiểu encoding, numbers Phimond riêng. APK3.2/8.4 vẫn đối chiếu13conflicts.',['Gộp thành rank: mất rõ lựa chọn farm, v3 thay phương án này.','Copy sốraw: chưa chứng minh encoding/server.'],['60sourceIDs đều mapping;28AoE source tier có28candidateIDs riêng.','Tier cao không xóa/thay/khóa tier thấp.'],'Runtime thuộc P02; tên source, số authored.',category='Phạm vi & nguồn'),
    decision(2,'Giữ 6 slot: đủ vai trò, còn đánh đổi','6 current skill + basic riêng, signature cũng chiếm1 slot. Native/Inherited là pool lựa chọn, không phải tất cả đều phải mang vào trận; newborn0, re-hatch giữ skill/rank.','Review owner: 4 slot dễ bó hẹp pet hai role; 6 chứa 2 hướng damage + phòng thủ + hồi/cleanse + control + signature. 8 slot dễ mang quá nhiều đáp án, tăng pool truyền current và UI. Basic0MP riêng giúp kit không cần tốn slot cho fallback. Đây là lập luận thiết kế, chưa phải playtest.',['4 slot: pet hybrid/support dễ phải bỏ secondary role.','6 slot: đề xuất giữ P10 D35, kit6 phải có lựa chọn bỏ bớt.','8 slot: cân nhắc chỉ khi P02/P07 chứng minh6 thiếu; cần mở lại P10/lifecycle/UI.'],['0/6 vẫn basic được; rank không chiếm thêm slot.','Học khi6/6 cần replacement + xác nhận; không slot7 riêng cho Special.','P02/P07 so kit4/6/8 cùng pool/MP/stats/AI, đo role coverage, skill usage, thời lượng trận, control pressure; owner duyệt trước thay limit.'],'P03/P16 giữ6; P02/P07 chứng minh bằng trận thật. Xem P13-owner-feedback-v2.md.',category='Học & kế thừa'),
    decision(3,'Học tier riêng, giữ skill farm ítMP','Common strike/heal/guard. AoE APK và2groupheal tier cố địnhrank1, học từngID, mang nhẹ+mạnh chiếm2slot. 7signature mới cố địnhrank1. Damage/heal khác rank1–3: power/heal×1.15/1.30,MPceil×1.20/1.40, effects/CD không đổi; rank2Lvmax(20,base+15),rank3max(40,base+30). Giá học20+10×level;upgrade2/3=3×/6×base;relearn20%base.','Tier là skillID riêng; rank là upgrade cùngID. Không auto-upgrade nhẹ, không nhânrank AoE tier. Giá học vẫn ứng viên P19.',['Auto thay nhẹ bằng mạnh: mất farm option.','Mang cả4tier chiếm4/6slot.'],['Native/inherit/current lưu từngtierID; học tier cao không consume tier thấp.','Full6/6 thay đúng skill đã chọn, không thay cảfamily.','Tier MP/CD cố định, không có rank2/3 cho cácfamily này.'],'P03/P16 snapshots; P19 pacing.',category='Học & kế thừa'),
    decision(4,'Eligibility và độc quyền từng species','Native được học theo species pool. Inheritance chỉ Race whitelist mỗi skill; khác Element không loại. Revive/dragon_breath/death_scythe/love_kiss không truyền. 7 signature mới có exclusive_species, chỉ loài đó được học; inheritance rỗng, không vào common hoặc pool loài khác.','Giữ bản sắc và lựa chọn donor. No RNG chọn skill, chỉ current skills truyền. Độc quyền gắn species ID, không dùng Race/Star làm quyền chung. Signature dùng active cost, rank1 cố định.',['Mọi skill truyền: homogenization.','Cấm khác Element: trái P10.','Slot7 hoặc passive miễn phí cho Special: bỏ qua tradeoff6slot.'],['Union→dedupe→filter deterministic;7 signature luôn bị lọc khỏi inheritance.','Giữ inherited pool qua hoàn nguyên; quên current không xóa pool.','Species thay đổi không được auto cấp/giữ quyền signature của species cũ; P16 kiểm tra ownership trước giao dịch.'],'P16 snapshots/migration version; P03 trước-sau. 7 signature là Phimond-authored, không claim source mechanics.',category='Học & kế thừa'),
    decision(5,'Ma trận 6 Element','Hỏa>Phong>Địa>Thủy>Hỏa: thuận1.25×, nghịch0.80×; Quang/Âm khắc nhau1.25×; còn lại1×. Basic và neutral1×.','Thay chart cực đoan bằng chênh lệch vừa; không miễn nhiễm damage theo Element/Race.',['2×/0.5×: counter dễ áp đảo level.','Chart damage0: nhiều dead match.'],['36 ô đủ; chart không đi từ Race.','Skill khác Element vẫn dùng bình thường.'],'Numeric candidate; P02/P07 balance phải đo.',category='Hệ & phối hợp'),
    decision(6,'Damage vật lý/phép','Base=offense×power×100/(100+DEF); nhân chart, crit; floor một lần. Offense0→0, offense>0 damage tối thiểu1. Physical ATK; magic MAG; basic neutral1.00×ATK.','Một DEF P11; tránh phép subtraction khiến low level hoàn toàn vô dụng.',['ATK−DEF dễ hard wall.','Tách MDEF trái P11.'],['ATK100,DEF50,power1.2: thuận100; nghịch64.','HP loss dùng min(damage,currentHP), không overkill.'],'P02 exact rational + replay.',category='Công thức & tài nguyên'),
    decision(7,'Đơn thể/AoE; damage và hiệu ứng','Mỗi skill có single/AoE và damage thuần/damage+effect/effect khôngdamage. AoE4tier power mỗi target .45/.75/1.05/1.35;physicalMP10/18/26/36,magicMP12/20/28/38;learnLv1/5/20/40;CD0/1/1/2. Hit95%,blind−20pp clamp50–95;crit5%×1.50 cho directdamage.','Power đã là mỗi target, không nhân thêm .75. Poison/burn códamage+effect; sleep/bind/debuff/cleanse khôngdamage. Hit/crit/status riêng mỗi target; DoT/heal/control khôngcrit.',['Chỉ dùng tier mạnh dễ overkill và haoMP.','AoE không đồng nghĩa damage: heal/buff cảđội cũng AoE.'],['Web card và filter có target shape/effect mode.','Offense100,DEF50 neutral khôngcrit: mỗi target30/50/70/90, đủ3hit tổng90/150/210/270.','Farm3quái25HP: nhẹ/mạnh đều đủkill nếuhit, nhẹ tiết kiệmMP.','Dead targets không nhận hit/proc, AoEheal chỉ ally sống.'],'Numbers Phimond; P02/P07 đo balance.',category='Công thức & tài nguyên'),
    decision(8,'MP, cooldown và action','MP cost trả một lần khi action hợp lệ bắt đầu; miss vẫn tốn. CD C: cast vòngR dùng lại từR+C+1. Một actor1 action/vòng; CD không thêm action. Không passive regen/end-battle refill.','Tuân MP P11. Dùng skill retained Lv1 theo MP thực, không khóa level lần nữa.',['Cost%maxMP khiến cùng skill đổi giá theo pet.','CD theo giây tạo race/disconnect issue.'],['Không đủ MP: auto fallback basic.','Invalid request không mất MP/action; retry không trừ hai lần.'],'P19 items có account cooldown riêng.',category='Công thức & tài nguyên'),
    decision(9,'Vòng, SPD và replay','Đầu vòng chốt list actor sống theo SPD P11, random rank battle khi hòa. Không resort giữa vòng. Dead trước action bị bỏ; revive lên action vòng sau.','P11 SPD không tự thêm lượt. Chọn vòng rõ để buff/control đo được.',['Gauge continuous làm thay đổi P11 và khó replay.'],['Haste cast giữa vòng chỉ đổi order vòng sau.','Reconnect trả snapshot/event cursor, không reroll rank.'],'P02 scheduling; P07 command deadline30s, timeout auto.',category='Luật chiến đấu'),
    decision(10,'Status, SR và duration','p_final=p_base×(1−0.8×SR/(SR+100));1 draw/status sau hit. Base chances ghi từng skill. Buff/debuff2 vòng castR hết cuốiR+2; DoT/regen tickR+1,R+2, không tick ngay.','Kháng status không xóa direct damage. DoT snapshot offense; DEF/chart target lúc tick, không crit.',['Hai roll proc/resist làm lệch chance.'],['p75%,SR100→45%.','SR không giảm damage/tick/duration; cleanse remove được.'],'P02 event order/disconnect tests.',category='Trạng thái & counterplay'),
    decision(11,'Control và chống khóa liên tục','Sleep/petrify/confuse tối đa1 action; không stack với nhau. Khi trigger, expire hoặc cleanse: control grace đến cuối vòng kế tiếp, không nhận3 status đó. Bind/silence2 vòng nhưng không chặn mọi action cùng lúc: status đến sau bị reject khi trạng thái kia còn hoạt động.','Solo1v3 cần đường thoát. NPC trainer không cứu pet đang sleep trong combat. Basic còn dùng được khi silence; bind cho phép magic/support.',['3 vòng hard lock hoặc instant death làm mất counterplay.'],['Sleep bị direct damage đánh thức, không double damage.','Petrify vẫn nhận damage, chỉ DEF+25%.','Confuse basic random địch sống, không friendly fire.'],'P07 kiểm chứng control pressure3v3.',category='Trạng thái & counterplay'),
    decision(12,'Stack, DoT và pipeline','Cùng status giữ potency lớn hơn, refresh có trần2 vòng kể từ lần apply mới; tối đa poison+burn,1 stack/type. Buff cùng stat giữ strongest positive; debuff strongest negative; khác nhóm cộng theo P11. Battle percent stat clamp tổng−50%..+50%.','No multiplicative infinite stack; reapply vẫn tiêuMP/action/CD, grace chặn hard lock. Không buff maxHP trong v1.',['DoT stacking theo từng caster snowball3v3.'],['Gear/buff không vào inheritance.','Counter tối đa1/vòng, không reaction cascade.'],'P14 phối hợp item/equipment effect budgets.',category='Trạng thái & counterplay'),
    decision(13,'Triệt tiêu và tăng cường','Cleanse chuyên biệt MP8/CD1; genericMP16/CD2 gỡ1 status theo priority. Water hit thành công dập burn trên target (sau damage, trước status mới); mọi rank như nhau. Không phản ứng dây chuyền/free damage. Buff ATK/MAG/SPD hỗ trợ đồng đội theo role.','Giải trạng thái là lựa chọn rõ; source7 cleanse được giữ tên. Counter chart, synergy buff và cleanse là3 trục riêng.',['Mọi nước auto freeze: tên không là luật.','Element reaction cascade khó budget.'],['Dispel gỡbuff không quaSR nhưng kiểm tra hit.','Cleanse target không có trạng thái phù hợp không mất cost.'],'P02 single/group; P07 multi-owner.',category='Hệ & phối hợp'),
    decision(14,'Shield, hồi phục và revive','Heal1.50×MAG+10; group thường0.85×MAG+6/28MP/CD2; group siêu cấp1.10×MAG+10/40MP/CD3 mỗi ally sống, họcLv40, riêngID/rank1. Shield1.20×MAG+8%maxHP nguồn,2 vòng; shield cùng loại giữ lớn hơn, không stack. Revive35MP/CD4 họcLv40:25%HP, không refillMP,1 lần/actor/battle, không self.','P11 không tự heal. Source passive rebirth/regeneration thành paid active; kiss thành shield thay immunity.',['Passive proc20% nguồn mở heal/MP miễn phí.','Full revive liên tục tạo stall.'],['Heal không hồi sinh.','Shield nhận trướcHP, drain tính HP mất.','Ally-fainted không hợp lệ trong PvE solo1pet.'],'P07 revive; P02 announce unavailability.',category='Công thức & tài nguyên'),
    decision(15,'152 pools + 7 signature Special4★/5★','Giữ Race/Element/Star/roles P11. Special4: Thanh Long–Triều áp(Thủy/slow), Bạch Hổ–Phong trảo(Phong/selfhaste), Chu Tước–Ly hỏa(Hỏa/burn), Huyền Vũ–Thủy giáp(Thủy/shield+gỡburn). Special5: Nữ Đế–Minh ấn(Âm/antiheal), Cự Ma–Địa chấn hộ thể(Địa/selfarmor), Hoa Hương–Quang tịnh(Quang/heal+cleanse). Mỗi signature1/6slot, rank1, CD3;4★ họcLv30/24MP;5★ Lv40/28MP. Pool mở đủtier nhẹ→siêu cấp theo damage channel. Mỗi Race có≥2 primaryphysical và≥2 primarymagic; web có số lượng, ví dụ và gaps theoStar, không claim mỗiStar đều đủ.','Giá trị Special đến từ nén hai công dụng phù hợp role vào1action có cost/CD, không tăng stats P11 hay tự thắng. Hiệu ứng tận dụng status/buff hiện có; Element chart chỉ tăng damage, không khuếch đại heal/shield/status. Đây là đề xuất authored sau owner review, không recovered source.',['Ép mọi loài cùng số skill không có lợi gameplay.','Cấp mọi17Special signature ngay: chưa có yêu cầu, mở rộng balance trước playtest.'],['152 IDs đủ, role/reference hợp lệ;27 loài cùng stats khác pool.','7 signature chỉ xuất hiện ở7 species sở hữu, đủ6Element, cả4★/5★; sample build vẫn≤6.','MP/CD/counterplay rõ; buffs không stack loại cũ, không control mới/instant kill.','P02/P07 so Special có/không signature và Normal cùng level/grade; không chứng nhận balance từ static checks.'],'Candidate cần owner duyệt D15 lại; P02/P07 kit review, Special operation gates P16/P20 giữ nguyên.',category='Nội dung loài'),
    decision(16,'Quái, auto và targeting','Quái dùng native subset theo level: mỗi lượt lọc skill hợp lệ, priority control chưa có→heal ally<40%→AoE>=2địch→buff chưa có→single; tie pool order. Tier auto theo thứ tự người chơi chọn trong6skill, không tự ưu tiên tier mạnh. Farm kit nên đặt nhẹ trước mạnh; burst kit đổi thứ tự trước trận; quái tie pool order nhẹ trước mạnh. Pet mặc định heal ally/self<40% → cleanse cần thiết → control chưa có/grace-free → buff chưa có → AoE>=2 → single → basic.','Không quái tự có mọi skill; không macro nâng cao. Target enemy_single mặc địnhHP thấp nhất, hòa stableID; ally heal%HP thấp nhất.','Manual commands valid server-authoritative; pet auto luôn có fallback.'.split('|'),['PvE solo1pet vs3quái, party3người×1pet, PvP3pet/bên.','Một mode khóa target phải báo rõ; không mất MP khi invalid.'],'P02 PvE implementation; P07 arena formation separate.',category='Luật chiến đấu'),
    decision(17,'Save, event và retry contract','Version p13-candidate-v1; learning intent idempotency key + expected pet revision; costs+replace atomic. Battle events có instance/source/target/skill/rank/sequence/hit/crit/status outcomes; client trình bày kết quả server.','Inherited skills rank reset1 lúc học con; preserved current giữ rank. Migration legacy14→152 cần mapping rõ, không guess.',['Không auto migrate vì source catalog đủ.'],['Retry/reconnect không double-charge/replay.','Snapshot không lộ seed/RNG/hidden appraisal.'],'P02/P03/P16 migration và atomic integration.',category='Tích hợp & nghiệm thu'),
    decision(18,'Exit gate và giới hạn cân bằng','Candidate cần owner acceptance qua web; arithmetic/catalog checks chỉ chứng minh consistency. P02/P07 đo trận thật, P15/P19 đo chi phí học và retraining; không claim50CCU/balance.','Handoff chỉ tạo sau owner acceptance, đính exact candidate hash và unresolved dispositions.',['Đóng phase vì có152pools không chứng minh value.'],['Có examples damage, neutral, counter, synergy, cleanse,0skills.','Feedback được lưu theo hash; owner có thể từ chối từng nhóm.'],'Design ready for review, closure pending.',category='Tích hợp & nghiệm thu')]


def build_scenarios():
    entries=[
    ('0 skill vẫn chơi','PvE 1v3','Pet mới nở có 0/6 skill, MP50.','Bắt đầu auto combat.','Basic trung tính, 0MP hoạt động; không cấp skill ngầm.','P02 live'),
    ('Counter từ skill, không Race','PvE 1v3','Pet Chim dùng skill Hỏa vào target Phong.','Hit thành công.','Damage nhân1.25 theo Element; không STAB/Race bonus.','Arithmetic + P02'),
    ('Neutral damage','PvE 1v3','Basic ATK100, target DEF50.','Hit không crit.','Damage floor66; Element của pet không đổi basic.','Arithmetic + P02'),
    ('SR kháng status giữ damage','PvE 1v3','Hỏa ấn hit thành công, target SR100.','Status draw thất bại.','Direct damage vẫn có; target không nhận burn/tick.','P02 seeded replay'),
    ('Học khi đầy','Ngoài trận','Pet6/6, đủ gold, expectedRevision đúng.','Chọn replacement rồi retry cùng intent.','Vẫn6/6, chỉ trả phí một lần; skill đã quên không truyền nữa.','P03/P19 integration'),
    ('Kế thừa khác Element','Dung hợp','Cha đã học bolt_fire; con Thủy với Race hợp lệ.','Union/dedupe/filter skills của bố mẹ.','Fire nằm inherited pool; current0; level chỉ xét lúc học.','Static + P16'),
    ('Signature không truyền','Dung hợp','Cha đã học dragon_breath.','Con được tạo dưới dạng Egg.','Không vào inherited pool bất kể Race/Element con.','Static + P16'),
    ('Hoàn nguyên giữ rank','Lifecycle','PetLv40 có skill rank3 đã học.','Pet → Egg → nở lại Lv1.','Current skill/rank giữ nguyên; đủ MP thì dùng, không khóa level lại.','P16/P02'),
    ('MP retained ở Lv1','PvE 1v3','Lv1 maxMP50, wave_super retained cần38MP.','Một cast hợp lệ rồi thử cast thứ hai sauCD.','Còn12MP; super lần hai không hợp lệ, có thể chọn wave_light12MP đã học hoặc basic.','Arithmetic + P02'),
    ('AoE vào 3 địch','PvE 1v3','MAG100, ba địch DEF50, Element trung tính.','Cast wave với20MP.','Mỗi hit không crit gây50; tổng150 nếu đủ3hit; chỉ trả20MP.','Arithmetic + P02'),
    ('Buff phối hợp','Party 3×1','Support cast attack_up; teammate dùng physical.','Teammate thực hiện action.','ATK+20% theo pipeline P11; không thêm action.','P07 integration'),
    ('Cleanse cứu ally','Party 3×1','Ally sleep; người giải còn action/MP.','Cast wake trước slot action của ally.','Sleep gỡ, thêm grace; ally được act nếu còn slot; cost8MP.','P07 integration'),
    ('Control không chain','PvP 3v3','Petrify làm mất action trong vòngR.','Enemy cast sleep/confuse trong thời gian grace.','Hard control bị từ chối đến cuốiR+1.','P07 replay + playtest'),
    ('Bind/silence counterplay','PvE 1v3','Target đang bị bind.','Enemy thử apply silence.','Silence không vào; channel magic/utility vẫn có đường hành động.','P02/P07'),
    ('Triệt tiêu cháy','PvE 1v3','Enemy đang burn còn hai tick.','Water hit thành công.','Direct damage xong rồi burn bị gỡ; không có tick burn tương lai.','P02'),
    ('DoT và reapply','PvP 3v3','Hai caster apply poison với potency khác nhau.','Apply cùng loại status.','Giữ strongest một stack; tick cuốiR+1/R+2, không crit.','P07'),
    ('Shield và drain','PvE 1v3','Damage100, shield80, target còn10HP.','Drain hit thành công.','HP thực mất10; drain hồi floor2HP, không hồi25.','Arithmetic + P02'),
    ('SPD không resort','Party 3×1','Danh sách action vòngR đã chốt.','Haste tăng SPD giữa vòngR.','OrderR giữ nguyên; R+1 sort lại theo P11.','P02/P07 replay'),
    ('Revive bị giới hạn','PvP 3v3','Ally chết, chưa từng được revive trong battle này.','Revive thành công.','25%HP, giữ MP, act từR+1; revive lần hai của actor đó bị từ chối.','P07'),
    ('RNG và reconnect','PvE 1v3','Action đã processed, dedupe receipt còn lưu.','Disconnect → retry → reconnect.','Không trừ MP/damage/reward lần hai, không reroll RNG hoặc rank.','P02 integration'),
    ('Native role viability','Catalog','152 records P11v2 đã cố định.','Validate từng native pool.','Support có ally function; Disruptor không chỉ DoT; Hybrid có hai damage channels; cùng stats khác kit.','Static; combat value P02/P07'),
    ('Cost và retraining payoff','Progression','Con dung hợp luyện Lv1→Lv40 rồi học lại kit.','Đo số trận, EXP, gold và thời gian lấy lại vai trò.','Owner review time-to-useful; static formulas không tự chứng nhận balance.','P15/P19'),
    ('SR và immunity rõ ràng','PvP 3v3','Target SR rất cao hoặc đang control grace.','Apply status xấu.','SR không tự miễn nhiễm; grace chỉ chặn ba hard controls, không chặn burn/debuff.','P07'),
    ('Stale review','Web nghiệm thu','Tab hoặc candidate hash đã cũ.','Lưu phản hồi hoặc gửi kết luận.','HTTP409; không ghi đè phản hồi/phiên bản mới.','Automated local server'),
    ('Signature đúng species, đúng slot','Catalog/lifecycle','Special4★/5★ sở hữu signature, current6/6.','Học signature hoặc thử học trên loài khác.','Chủ sở hữu chọn replacement; loài khác bị từ chối, không slot7; rank1.','Static + P03/P16'),
    ('Signature không rò qua inheritance','Dung hợp','Cha mẹ có7 signature Special mới đã học.','Union/dedupe/filter theo Race con.','Cả7 không vào inherited pool, kể cả con cùng species; newborn không tự cấp.','Static + P16'),
    ('Signature buff cần hit','PvE/PvP','Bạch Hổ/Cự Ma đủMP, action hợp lệ.','Signature miss hoặc hit thành công.','Miss vẫn trảMP nhưng không selfbuff; hit có selfbuff strongest, không thêm action.','P02/P07'),
    ('Quang tịnh cleanse trước heal','Party','Ally có misfortune và thiếuHP.','Hoa Hương dùng Quang tịnh.','Cleanse theo priority rồi heal; nếu misfortune đã gỡ, heal không bị giảm; cost28/CD3 một lần.','P07'),
    ('Nhẹ tiết kiệm khi farm','PvE','ATK100,3quái25HP/DEF50, neutral,50MP.','Hit Càn quét nhẹ hoặc siêu cấp, khôngcrit.','Cảhai đủkill nếu3hit;nhẹ30damage/target và10MP,siêu90/target và36MP. Không chứng nhận clear speed cómiss/CD.','Arithmetic + P02'),
    ('Học tier cao vẫn giữ nhẹ','Trainer','Pet đã học Càn quét nhẹ, cònslot vàđủgold.','Học Càn quét siêu cấp.','HaiIDcurrent riêng,2slot;Nhẹ khôngxóa, MP10/36 cố định; khôngupgrade cảfamily.','Static + P03/P16'),
    ('Effect không damage','PvP','Sleep single, attack_up allyall, burn single.','Resolve action theo target.','Sleep/attack_up khôngdamage;burn códirectdamage khi procstatusfail. AoE không tự códamage.','Static classification + P07'),
    ('Race và gaps từngStar','Catalog','Frozen152species và8Race.','Đếm primarydamage riêng, kiểmtraNative single/lightAoE.','MỗiRace≥2physical và≥2magic;Hybrid riêng. GapsNormalStar côngkhai, không đổiP11stats/roles.','Static')]
    return [{'id':f'P13-A{i:02d}','title':t,'mode':m,'given':g,'when':w,'then':n,'verification':v} for i,(t,m,g,w,n,v) in enumerate(entries,1)]


def validate(p):
    errors=[]; by={s['id']:s for s in p['skills']}; species=p['species']
    frozen=json.loads(P11.read_text())['records']
    if len(by)!=len(p['skills']):errors.append('duplicate skill IDs')
    if {s['id'] for s in species}!=set(frozen):errors.append('152 frozen species IDs mismatch')
    for s in species:
        for k,old in [('race','race_id'),('star','star'),('element','element_id'),('roles','role_ids')]:
            if s[k]!=frozen[s['id']][old]:errors.append(s['id']+' changed '+k)
        refs=s['native_skills']; functions=set()
        for sid in refs:
            if sid not in by:errors.append(s['id']+' missing '+sid)
            else:functions.update(by[sid]['functions'])
        for role in s['roles']:
            if role not in functions:errors.append(s['id']+' missing role '+role)
        kinds={by[x]['kind'] for x in refs if x in by}
        if 'hybrid' in s['roles'] and not {'physical','magic'} <= kinds:errors.append(s['id']+' hybrid lacks two channels')
        if 'disruptor' in s['roles'] and not kinds & {'control','debuff','dispel'}:errors.append(s['id']+' disruptor lacks impairment')
        if 'support' in s['roles'] and not any(by[x]['target'].startswith('ally') for x in refs if x in by):errors.append(s['id']+' support lacks ally target')
        if len(set(s['sample_build']))!=len(s['sample_build']) or len(s['sample_build'])>6 or not set(s['sample_build'])<=set(refs):errors.append(s['id']+' invalid build')
    groups=collections.defaultdict(list)
    for s in species:groups[json.dumps([s['base_stats'],s['growth_baseline']],sort_keys=True)].append(s)
    for group in groups.values():
        if len(group)>1:
            pools=[tuple(sorted(s['native_skills'])) for s in group]
            if len(set(pools))!=len(pools):errors.append('duplicate-stat pool identical: '+','.join(s['id'] for s in group))
            builds=[tuple(sorted(s['sample_build'])) for s in group]
            if len(set(builds))!=len(builds):errors.append('duplicate-stat sample build identical: '+','.join(s['id'] for s in group))
    for s in p['skills']:
        if s['mp']<0 or s['cooldown']<0 or not set(s['inheritance'])<=set(RACES):errors.append('invalid skill '+s['id'])
        if s.get('exclusive_species'):
            owners=[r for r in species if s['id'] in r['native_skills']]
            if len(owners)!=1 or owners[0]['id']!=s['exclusive_species']:errors.append('exclusive pool violation '+s['id'])
            elif owners[0]['class']!='special' or owners[0]['star'] not in (4,5) or owners[0]['element']!=s['element']:errors.append('exclusive identity violation '+s['id'])
            if s['inheritance'] or s['rank_policy']!='fixed_rank_1':errors.append('exclusive transmission/rank violation '+s['id'])
    for race in RACES:
        for role,kind in [('physical_dps','physical'),('magic_dps','magic')]:
            candidates=[s for s in species if s['race']==race and s['roles'][0]==role]
            if len(candidates)<2:errors.append('race damage coverage '+race+' '+role)
            for pet in candidates:
                rows=[by[x] for x in pet['native_skills'] if x in by and by[x]['kind']==kind]
                if not any(x['target']=='enemy_one' for x in rows) or not any(x['target']=='enemy_all' and x.get('tier_index')==1 for x in rows):errors.append('race damage coverage kit '+pet['id'])
    families=collections.defaultdict(list)
    for s in p['skills']:
        if s.get('tier_family'):families[s['tier_family']].append(s)
    for family,rows in families.items():
        rows.sort(key=lambda s:s['tier_index'])
        if len(rows)!=(2 if family=='group_heal' else 4) or any(s['rank_policy']!='fixed_rank_1' for s in rows):errors.append('invalid tier family '+family)
        if family!='group_heal' and any(rows[i]['mp']>=rows[i+1]['mp'] or Fraction(rows[i]['power'])>=Fraction(rows[i+1]['power']) for i in range(len(rows)-1)):errors.append('tier budget not increasing '+family)
    if len(p['chart'])!=6 or any(len(r)!=6 for r in p['chart'].values()):errors.append('chart incomplete')
    source=json.loads((PHASE/'evidence/apk84-skills.json').read_text())
    source_ids={r['id'] for r in source['rows']}
    mapped={sid for sk in p['skills'] for sid in sk['source_ids']}
    if mapped!=source_ids:errors.append('source mapping differs from60-record catalog')
    return errors


def build_package():
    chart={e:{t:1 for t,n,c in ELEMENTS} for e,n,c in ELEMENTS}
    for e,t in [('fire','wind'),('wind','earth'),('earth','water'),('water','fire')]:chart[e][t]=1.25;chart[t][e]=0.8
    chart['light']['dark']=chart['dark']['light']=1.25
    skills=build_skills()
    p={'schema_version':1,'phase':'P13','revision':'P13-candidate-v3-20261013','title':'Skill, hệ & bản sắc linh thú',
       'status':'Chờ chủ dự án nghiệm thu — design candidate, chưa runtime',
       'summary':'Bản v3: giữ skill APK Nhẹ/Thường/Cao cấp/Siêu cấp riêng để farm ít MP; làm rõ đơn thể/AoE và damage/hiệu ứng; kiểm tra cả8 Race có pet vật lý lẫn phép. 7 signature Special mới giữ nguyên.',
       'baseline':{'p11_catalog_version':json.loads(P11.read_text())['catalog_version'],'p11_sha256':hashlib.sha256(P11.read_bytes()).hexdigest(),'master_sha256':hashlib.sha256((ROOT/'.ai/plan/PHIMOND_MASTER_SPEC.md').read_bytes()).hexdigest()},
       'decisions':build_decisions(),'elements':[{'id':e,'name':n,'color':c} for e,n,c in ELEMENTS], 'chart':chart,
       'skills':skills,'species':build_species(skills),'scenarios':build_scenarios(),
       'sources':[{'id':'owner-v3','title':'Phản hồi tier/farm/target/Race → v3','path':'P13-owner-feedback-v3.md','note':'Tách28tier AoE và2groupheal; cheap farm option; rõ target/effect; frozen Race coverage.'},
                  {'id':'owner-v2','title':'Phản hồi owner → bản v2','path':'P13-owner-feedback-v2.md','note':'6-slot review +7 exclusive Special signatures. Historical revision; v3 giữ7signature nguyên vẹn.'},
                  {'id':'master','title':'Master P13-R01–R06','path':'.ai/plan/PHIMOND_MASTER_SPEC.md','note':'Accepted product scope; P13 design gate, P02/P07 runtime.'},
                  {'id':'p10','title':'P10 D35–D38','path':'.ai/plan/phases/P10-pet-model/P10-design-decisions.md','note':'6 skills, native/inherited/current, eligibility, hatch/re-hatch.'},
                  {'id':'p11','title':'P11 final + catalog v2','path':'.ai/plan/phases/P11-stats/P11-final-spec.md','note':'Stats, MP, SR and SPD authoritative interfaces.'},
                  {'id':'apk84','title':'APK8.4 — 60 skill records','path':'evidence/apk84-skills.json','note':'Observed serialized client data; original server mechanics unresolved.'},
                  {'id':'apk32','title':'APK3.2 — 60 skill records','path':'evidence/apk32-skills.json','note':'13 requirement-record differences against8.4.'},
                  {'id':'jar','title':'JAR Pokezoo1.00','path':'P13-source-audit.md','note':'Client strings: Race signatures, trainer/forget/AoE. Not server formula proof.'}],
       'checks':[], 'limitations':['Chưa đo balance với combat authoritative1v3/3v3.','Giá học/MP/control là proposed Phimond numbers, owner có thể yêu cầu sửa.','Chưa triển khai runtime/migration; không chứng nhận50CCU.','Plant/Insect briefs dùng skill paid active; quái không tự có mọi skill.']}
    p['race_coverage']=[]
    for race,name in RACES.items():
        rows=[s for s in p['species'] if s['race']==race]
        physical=[s for s in rows if s['roles'][0]=='physical_dps'];magic=[s for s in rows if s['roles'][0]=='magic_dps']
        gaps=[]
        for star in range(1,6):
            normal=[s for s in rows if s['star']==star and s['class']=='normal']
            channels={k for s in normal for k in s['roles']}
            if not ('physical_dps' in channels or 'hybrid' in channels):gaps.append(f'{star}★ thiếu role vật lý')
            if not ('magic_dps' in channels or 'hybrid' in channels):gaps.append(f'{star}★ thiếu role phép')
        p['race_coverage'].append({'race':race,'name':name,'total':len(rows),'primary_physical':len(physical),'primary_magic':len(magic),'primary_hybrid':sum(s['roles'][0]=='hybrid' for s in rows),'physical_examples':[s['name']+' ('+s['id']+')' for s in physical[:2]],'magic_examples':[s['name']+' ('+s['id']+')' for s in magic[:2]],'normal_star_gaps':gaps})
    return p


def main():
    p=build_package();errors=validate(p)
    if errors:raise SystemExit('\n'.join(errors))
    minimum=min(len(s['native_skills']) for s in p['species']);maximum=max(len(s['native_skills']) for s in p['species'])
    p['checks']=[{'name':'152 IDs + roles + references','status':'PASS','detail':'152 pools; 6-slot builds; frozen identity/Element/roles P11.'},
                 {'name':'28 separate APK AoE tiers +2 groupheal','status':'PASS','detail':'Power/MP tăng theo tier; light giữ được; fixedrank1; family pools đủtiers.'},
                 {'name':'8 Race vật lý và phép','status':'PASS','detail':'Mỗi Race≥2 primaryphysical +≥2 primarymagic; single vàlightAoE đúngchannel. Star gaps công khai, không sửa P11.'},
                 {'name':'7 exclusive Special signatures','status':'PASS','detail':'4 species4★ +3 species5★, đủ6Element; unique owner, no inheritance;1/6slot, fixedrank1.'},
                 {'name':'27 species cùng vector','status':'PASS','detail':'Mỗi pair/group cùng base/growth có native pool khác nhau.'},
                 {'name':'60 source IDs','status':'PASS','detail':'Mọi source skill/tier có mapping rõ sang candidate; không sao chép số gốc chưa hiểu encoding.'},
                 {'name':'Ma trận hệ','status':'PASS','detail':'36 ô; neutral/basic1×; không STAB.'},
                 {'name':'Pool size','status':'INFO','detail':f'{minimum}–{maximum} skills/species; không quota bằng nhau.'},
                 {'name':'Combat balance','status':'PENDING','detail':'P02/P07 live integration và playtest.'},
                 {'name':'Owner acceptance','status':'PENDING','detail':'Gửi kết luận trên web; agent không tự duyệt.'}]
    PHASE.mkdir(parents=True,exist_ok=True)
    (PHASE/'review-package.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
    (PHASE/'P13-skill-catalog.json').write_text(json.dumps({'version':p['revision'],'status':'candidate_pending_owner_acceptance','skills':p['skills']},ensure_ascii=False,indent=2)+'\n')
    (PHASE/'P13-species-pools.json').write_text(json.dumps({'version':p['revision'],'p11_baseline':p['baseline'],'status':'candidate_pending_owner_acceptance','species':p['species']},ensure_ascii=False,indent=2)+'\n')
    md=['# P13 — Skill pet/quái và tương tác giữa các hệ','', '**Status: CANDIDATE — owner acceptance pending.** Date: 2026-10-13. Runtime chưa kích hoạt.', '', '## Outcome',p['summary'],'','## Authority','P10/P11 accepted decisions giữ nguyên. Các P13-D dưới đây là đề xuất do agent lựa chọn theo quyền owner giao; chưa phải owner approval. Source facts xem P13-source-audit.md. Handoff/closure sau nghiệm thu.', '', '## Traceability','P13-R01/R01a/R01b: D02–D04,D15,D16. R02: D05–D14. R03: D09,D14,D16. R04: D04,D17. R05: D10–D14,D18. R06: D04,D15 và 152 native pools.', '', '## Decisions']
    for x in p['decisions']:
        md += ['', '### '+x['id']+' — '+x['title'],x['summary'],'','Rationale: '+x['rationale'],'','Acceptance:',*['- '+a for a in x['acceptance']],'','Downstream: '+x['impact']]
    md += ['','## Content artifacts','- P13-skill-catalog.json: all concrete skills, functions, power/effects, cost, CD, learn gate, inheritance whitelist and source mapping.','- P13-species-pools.json: 152 explicit species pools + illustrative builds of up to6 skills; builds assume required learning levels and paid learning.','- review-package.json: exact candidate shown in web, combining decisions/catalog/chart/scenarios/evidence.','- P13-behavior-contract.md: timing, transaction, input/result and error semantics.','','## Phase gate','Candidate prepared and statically checked. Owner acceptance PENDING. P02/P07 live, balance and save migration remain separate release blockers. Numeric consistency is not measured kit balance. No handoff/closure yet.']
    (PHASE/'P13-final-spec.md').write_text('\n'.join(md)+'\n')
    print(json.dumps({'skills':len(p['skills']),'species':len(p['species']),'decisions':len(p['decisions']),'scenarios':len(p['scenarios']),'pool_range':[minimum,maximum],'errors':errors}))

if __name__=='__main__':main()
