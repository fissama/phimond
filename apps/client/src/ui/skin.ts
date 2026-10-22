/**
 * Giao diện dùng bộ UI HD-2D đã duyệt (art-src batch 06 HUD, 07 trận, 08 menu, 09 icon, 10 logo/tải).
 * Ảnh nằm ở public/ui (sinh bằng tools/p01/sync_client_assets.py). CSS được sinh lúc chạy để đường dẫn
 * đúng với BASE_URL ở cả bản dev và bản build.
 */
export const uiUrl = (id: string) => `${import.meta.env.BASE_URL}ui/${id}.png`;

type Slice = [number, number, number, number]; // trái, trên, phải, dưới (theo manifest)

/** border-image 9-slice; `k` = tỷ lệ hiển thị so với px gốc. */
function nine(id: string, s: Slice, k: number, fill = true): string {
  const [l, t, r, b] = s;
  const w = (n: number) => `${Math.round(n * k)}px`;
  return `border-style:solid;border-width:${w(t)} ${w(r)} ${w(b)} ${w(l)};border-image:url(${uiUrl(id)}) ${t} ${r} ${b} ${l} ${fill ? 'fill' : ''} / ${w(t)} ${w(r)} ${w(b)} ${w(l)} stretch;image-rendering:pixelated;background:none;`;
}
const sprite = (id: string) => `background:url(${uiUrl(id)}) center/100% 100% no-repeat;image-rendering:pixelated;border:0;`;

const PANELS: Record<string, [string, Slice, number, string]> = {
  // lớp CSS: [ảnh, slice, tỷ lệ, màu chữ]
  dialogue: ['dialogue-panel', [222, 87, 222, 87], 0.22, 'var(--text)'],
  large: ['panel-large', [64, 64, 64, 64], 0.42, 'var(--text)'],
  small: ['panel-small', [64, 64, 64, 64], 0.36, 'var(--text)'],
  settings: ['settings-panel', [64, 64, 64, 64], 0.42, 'var(--text)'],
  shop: ['npc-shop-panel', [80, 80, 80, 80], 0.4, '#fbe9c8'],
  quest: ['quest-log-panel', [90, 80, 90, 80], 0.4, '#3a2a14'],
  bag: ['inventory-panel', [64, 64, 64, 64], 0.42, '#fbe9c8'],
  pets: ['pet-management-panel', [80, 80, 80, 80], 0.4, '#eaf6e4'],
  learn: ['skill-learning-panel', [90, 80, 90, 80], 0.4, '#3a2a14'],
  confirm: ['confirmation-panel', [64, 64, 64, 64], 0.42, 'var(--text)'],
};

export function installSkin(): void {
  if (document.getElementById('phimond-skin')) return;
  const css: string[] = [];
  for (const [cls, [id, s, k, color]] of Object.entries(PANELS)) {
    css.push(`.skin-${cls}{${nine(id, s, k)}color:${color};}`);
    if (color !== 'var(--text)') css.push(`.skin-${cls} .muted{color:${color};opacity:.72}.skin-${cls} h2{color:${color}}`);
  }
  css.push(
    // Nút
    `.btn{${nine('button-secondary-normal', [75, 42, 75, 42], 0.3)}padding:0 6px;min-height:36px;color:#f4ecd6;text-shadow:0 1px 1px #000;}`,
    `.btn:active:not(:disabled),.btn.on{${nine('button-secondary-pressed', [75, 42, 75, 42], 0.3)}}`,
    `.btn:disabled{${nine('button-secondary-disabled', [75, 42, 75, 42], 0.3)}opacity:1;color:#9a9a9a;}`,
    `.btn.primary{${nine('button-primary-normal', [75, 42, 75, 42], 0.3)}color:#fff6e0;font-weight:700;}`,
    `.btn.primary:active:not(:disabled){${nine('button-primary-pressed', [75, 42, 75, 42], 0.3)}}`,
    `.btn.primary:disabled{${nine('button-primary-disabled', [75, 42, 75, 42], 0.3)}}`,
    `.btn.danger{${nine('button-primary-normal', [75, 42, 75, 42], 0.3)}}`,
    `.btn.small{min-height:30px;font-size:13px;}`,
    `.btn-close{${sprite('button-close')}width:40px;height:40px;flex:none;}`,
    `.btn-close:active{transform:scale(.94)}`,
    // Hàng danh sách, tab
    `.dialog .item{${nine('row-normal', [120, 35, 120, 35], 0.22)}padding:0 2px;min-height:44px;}`,
    `.skin-quest .item,.skin-learn .item{border-image-source:url(${uiUrl('row-selected')});color:#3a2a14}`,
    `.tab{${sprite('tab-normal')}min-width:96px;height:38px;padding:0 10px;color:#f1ead6;font-size:14px;}`,
    `.tab.on{${sprite('tab-selected')}color:#2a1d08;font-weight:700;}`,
    // HUD
    `.hud-map{${nine('map-name-panel', [120, 49, 120, 49], 0.24)}padding:0 6px;}`,
    `.hud-status .ring{${sprite('frame-portrait')}width:68px;height:68px;display:grid;place-items:center;flex:none;position:relative;}`,
    `.hud-status .ring .portrait{width:46px;height:46px;border-radius:50%;border:0;}`,
    `.hud-status .badge{${sprite('badge-level')}position:absolute;left:-6px;bottom:-6px;width:30px;height:30px;display:grid;place-items:center;font-size:11px;font-weight:800;color:#fff3cf;text-shadow:0 1px 1px #000;}`,
    `.hud-status .plate{${nine('hud-underlay', [40, 20, 40, 20], 0.5)}padding:2px 6px;}`,
    `.uibar{position:relative;height:13px;width:132px;${sprite('bar-track')}}`,
    `.uibar>i{position:absolute;left:0;top:0;bottom:0;background-size:132px 100%;background-repeat:no-repeat;image-rendering:pixelated;transition:width .3s;}`,
    `.uibar.hp>i{background-image:url(${uiUrl('hp-fill')})}.uibar.mp>i{background-image:url(${uiUrl('mp-fill')})}.uibar.xp>i{background-image:url(${uiUrl('xp-fill')})}`,
    `.coin{${sprite('currency-gold')}display:inline-block;width:16px;height:16px;vertical-align:-3px;margin-right:3px;}`,
    `.hud-menu .rbtn{${sprite('button-round')}width:58px;height:58px;display:grid;place-items:center;position:relative;}`,
    `.hud-menu .rbtn.pet{${sprite('button-pet')}}.hud-menu .rbtn.bag{${sprite('menu-inventory')}}.hud-menu .rbtn.quest{${sprite('menu-quest')}}.hud-menu .rbtn.settings{${sprite('menu-settings')}}`,
    `.hud-menu .rbtn:active{transform:scale(.94)}`,
    `.hud-menu .rbtn span{position:absolute;bottom:-14px;left:50%;transform:translateX(-50%);font-size:11px;font-weight:700;white-space:nowrap;color:#fff3cf;text-shadow:0 1px 2px #000,0 0 3px #000;}`,
    `.dpad{${sprite('dpad-base')}}`,
    `.dpad button{${sprite('dpad-up-normal')}border-radius:50%;color:transparent;}`,
    ...(['up', 'down', 'left', 'right'] as const).map(
      (d) => `.dpad button.${d}{background-image:url(${uiUrl(`dpad-${d}-normal`)})}.dpad button.${d}.on{background-image:url(${uiUrl(`dpad-${d}-pressed`)})}`,
    ),
    `.dpad .center{${sprite('dpad-center')}position:absolute;left:52px;top:52px;width:46px;height:46px;pointer-events:none;}`,
    `.round{border:0;color:#fff3cf;text-shadow:0 1px 2px #000;font-weight:800;}`,
    `.round.a{${sprite('confirm-normal')}width:96px;height:90px;}.round.a:active{${sprite('confirm-pressed')}}`,
    `.round.b{${sprite('back-normal')}width:78px;height:72px;font-size:13px;}.round.b:active{${sprite('back-pressed')}}`,
    `.chat .tabs button{${sprite('chat-tab-normal')}color:#e9e1c8;padding:2px 8px;min-width:58px;}`,
    `.chat .tabs button.on{${sprite('chat-tab-selected')}color:#fff;}`,
    `.toast{${nine('toast-panel', [84, 51, 84, 51], 0.26)}padding:0 8px;}`,
    `.hud-net{${nine('notification-banner', [236, 40, 236, 40], 0.18)}padding:0 8px;}`,
    // Trận đấu
    `.battle .card{${nine('battle_nameplate', [72, 72, 72, 60], 0.3)}padding:0 4px;}`,
    `.battle .cmds{${nine('battle_actions', [192, 72, 192, 72], 0.18)}padding:2px;}`,
    `.bbtn{${sprite('battle_button_normal')}width:64px;height:60px;display:grid;place-items:center;position:relative;color:#fff;}`,
    `.bbtn:active:not(:disabled){${sprite('battle_button_pressed')}}.bbtn:disabled{${sprite('battle_button_locked')}opacity:1;}`,
    `.bbtn img{width:34px;height:34px;image-rendering:pixelated;}.bbtn:disabled img{filter:grayscale(1) brightness(.6)}`,
    `.bbtn span{position:absolute;bottom:-15px;font-size:11px;font-weight:700;white-space:nowrap;text-shadow:0 1px 2px #000;}`,
    `.banner{width:min(420px,80vw);aspect-ratio:600/180;image-rendering:pixelated;display:grid;place-items:center;}`,
    `.dmg{display:inline-flex;align-items:center;height:44px;}.dmg img{height:44px;image-rendering:pixelated;margin:0 -8px}`,
    `.dmg.heal img{filter:sepia(1) hue-rotate(70deg) saturate(3)}.dmg.hurt img{filter:sepia(1) hue-rotate(-30deg) saturate(4) brightness(1.1)}`,
    // Đăng nhập, tải
    `.login-box{${nine('dialogue-panel', [222, 87, 222, 87], 0.22)}}`,
    `.input{${nine('text-input', [132, 34, 132, 34], 0.3)}color:#f4ecd6;font-size:16px;padding:0 6px;min-height:40px;}`,
    `.loadbar{${nine('loading-bar-frame', [48, 48, 48, 48], 0.25)}width:min(360px,70vw);height:28px;}`,
    `.icon{width:28px;height:28px;image-rendering:pixelated;flex:none;}`,
  );
  const el = document.createElement('style');
  el.id = 'phimond-skin';
  el.textContent = css.join('\n');
  document.head.appendChild(el);
}

/** Ảnh số sát thương (font batch 07). */
export function damageGlyphs(text: string): string[] {
  const map: Record<string, string> = { '+': 'damage_plus', '-': 'damage_minus' };
  return [...text].map((ch) => uiUrl(map[ch] ?? (/\d/.test(ch) ? `damage_${ch}` : 'damage_miss')));
}

/** Icon cho vật phẩm/kỹ năng/trạng thái/NPC theo id (batch 09); null nếu không có. */
const known = new Set<string>();
export async function loadUiManifest(): Promise<void> {
  try {
    const r = await fetch(`${import.meta.env.BASE_URL}ui/ui.json`);
    if (r.ok) Object.keys((await r.json()) as Record<string, unknown>).forEach((k) => known.add(k));
  } catch {
    /* thiếu manifest: chỉ mất icon */
  }
}
export function iconFor(id: string): string | null {
  return known.has(id) ? uiUrl(id) : null;
}
