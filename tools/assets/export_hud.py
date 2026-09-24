"""Export reviewed HUD Sprite slices from the user's 3.2 APK; no generated artwork."""
import hashlib
import json
import shutil
import zipfile
from pathlib import Path
import UnityPy

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path('/Users/phileanh/Downloads/Spirit Beast World 3.2.apk')
CACHE = ROOT / 'tools/.cache/reference/apk-3.2'
OUT = ROOT / 'apps/game-client/assets/reference/hud'
# Alias -> serialized Sprite name. Repeated aliases intentionally retain a single source.
NAMES = {
    'row_menu': 'tableitem_0', 'row_selected': 'tableitem1_0', 'tab_menu': 'tab',
    'button_accept': 'DongY', 'button_cancel': 'Huy 1', 'panel_menu': 'UI_0', 'dpad': 'UIall_10', 'button_round': 'UIall_15', 'button_round_red': 'UIall_20',
    'bar_hp': 'UIall_8', 'bar_mp': 'UIall_1', 'bar_xp': 'UIall_7', 'bar_green': 'UIall_16',
    'frame_bars': 'UIall_4', 'frame_portrait': 'UIall_14',
    'frame_chat': 'chatbg_0', 'panel_controls': 'UIall_2', 'panel_ornate': 'UIall_9',
    'button_confirm': 'UIall_3', 'button_back': 'UIall_3', 'button_menu': 'UIall_21',
    'button_side': 'UIall_5', 'button_orb': 'UIall_12', 'frame_small': 'UIall_13',
    'slot': 'UIall_19', 'slot_light': 'UIall_18', 'ornament_corner': 'UIall_0',
    'battle_actions': 'battlebg_0', 'icon_attack': 'Attack_0', 'icon_magic': 'Magic_0',
    'icon_inventory': 'Iventory_0', 'icon_auto': 'Auto_0', 'icon_run': 'Run_0',
    'button_inventory': 'item', 'button_pet': 'pet', 'button_settings': 'CaiDat',
    'button_quest': 'NV', 'button_shop': 'shop', 'button_guild': 'Bang',
    'icon_chat': 'chat', 'selection': 'Select_0', 'arrow_up': 'dir_arrow0_0',
    'battle_win': 'bwin', 'battle_loss': 'blost',
}
manifest = json.loads((CACHE / 'manifest.json').read_text())
assets = {a['name']: a for a in manifest['assets'] if a['type'] == 'Sprite'}
selected = {(assets[n]['file'], assets[n]['id']) for n in NAMES.values()}
with zipfile.ZipFile(SOURCE) as archive:
    bundle = next(n for n in archive.namelist() if n.endswith('data.unity3d'))
    env = UnityPy.load(archive.read(bundle))
metadata = {}
for obj in env.objects:
    key = (obj.assets_file.name, obj.path_id)
    if key not in selected:
        continue
    tree = obj.read_typetree()
    metadata[key] = {
        'sprite_rect_bottom_left': tree['m_Rect'],
        'sprite_border': tree['m_Border'],
        'sprite_pivot': tree['m_Pivot'],
        'texture_pointer': tree['m_RD']['texture'],
    }
OUT.mkdir(parents=True, exist_ok=True)
result = {'source': manifest['source'], 'source_sha256': manifest['sha256'],
          'method': 'UnityPy Sprite.image; original Sprite polygon/alpha and slice; byte-for-byte copied from extracted PNGs',
          'notes': ['button_confirm and button_back share unlabeled oval Sprite. Render labels separately.',
                    'frame_chat is a 10x85 cyan background strip to stretch horizontally, not a complete ornamental frame.',
                    'APK3.2 D-pad and silver bar chrome differ from the older reference video.'], 'assets': {}}
for alias, name in NAMES.items():
    entry = assets[name]
    dest = OUT / (alias + '.png')
    shutil.copyfile(CACHE / entry['path'], dest)
    result['assets'][alias] = {
        'path': 'res://assets/reference/hud/' + dest.name,
        'width': entry['width'], 'height': entry['height'],
        'source_sprite': name, 'source_file': entry['file'], 'source_id': entry['id'],
        'extracted_path': entry['path'],
        'png_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        **metadata[(entry['file'], entry['id'])],
    }
(OUT / 'hud.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(f'Exported {len(result["assets"])} reviewed Sprite aliases to {OUT}')
