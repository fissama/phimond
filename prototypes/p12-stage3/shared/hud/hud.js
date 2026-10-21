// Phimond HUD (2D, giữ nguyên bố cục classic_hud.gd + sprite HUD trích từ APK).
// Dùng chung cho Three.js và Godot Web: engine chỉ vẽ thế giới; HUD là lớp DOM phía trên.
// API: window.PhimondHUD { vec, onConfirm, onBack, sys(msg), log(ch,msg), setState(o), setDebug(t), on(name,fn), shiftFrac }
(() => {
  const BASE = new URL('.', document.currentScript.src).href;
  const Q = new URLSearchParams(location.search);
  if (Q.get('hud') === '0') { window.PhimondHUD = { vec: { x: 0, z: 0 }, sys() {}, sysq() {}, setResult() {}, setFps() {}, setTier() {}, setBenchBusy() {}, log() {}, setState() {}, setDebug() {}, on() {}, shiftFrac: 0, off: true }; return; }
  // bắt lỗi trang/engine để hiện trong tab Hệ thống (giúp chẩn đoán trên thiết bị không có devtools)
  const errQ = []; let errSink = (t) => errQ.push(t); let errN = 0;
  const pushErr = (t) => { if (errN++ < 40) errSink('[lỗi] ' + String(t).slice(0, 220)); };
  addEventListener('error', (e) => pushErr((e.message || 'error') + (e.filename ? ' @' + e.filename.split('/').slice(-2).join('/') + ':' + e.lineno : '')));
  addEventListener('unhandledrejection', (e) => pushErr('promise: ' + ((e.reason && e.reason.message) || e.reason)));
  for (const k of ['error', 'warn']) { const o = console[k].bind(console); console[k] = (...a) => { o(...a); try { const t = a.map((x) => (x && x.message) || String(x)).join(' '); if (k === 'error' || /shader|webgl|glsl|context/i.test(t)) pushErr((k === 'warn' ? 'warn: ' : '') + t); } catch (e) { } }; }
  const start = () => {
  const A = (n) => `${BASE}${n}.png`;
  const REF_H = 640, STRIP = 186, LEFT_W = 245, RIGHT_W = 197;
  const CHANNELS = [
    { id: 'all', label: 'Chung', color: '#123548' },
    { id: 'sys', label: 'Hệ thống', color: '#0e3a66' },
    { id: 'pm', label: 'Riêng', color: '#8a1f7a' },
    { id: 'party', label: 'Đội', color: '#17652a' },
    { id: 'world', label: 'Thế giới', color: '#a24a00' },
    { id: 'guild', label: 'Hội', color: '#5b2aa8' },
  ];
  const tag = { sys: 'Hệ thống', pm: 'Riêng', party: 'Đội', world: 'Thế giới', guild: 'Hội' };
  const css = `
  #phud{position:fixed;inset:0;pointer-events:none;z-index:50;font-family:"Be Vietnam Pro",system-ui,-apple-system,"Segoe UI",Arial,sans-serif;color:#fff0bb;-webkit-user-select:none;user-select:none;touch-action:none}
  #phud *{box-sizing:border-box}
  #phud .px{image-rendering:pixelated;position:absolute;pointer-events:none;background-repeat:no-repeat;background-size:100% 100%}
  #phud .hit{position:absolute;pointer-events:auto;cursor:pointer;background:none;border:0;padding:0;margin:0;-webkit-tap-highlight-color:transparent;touch-action:none}
  #phud .hit:active .px{filter:brightness(1.25)}
  #phud .t{position:absolute;white-space:nowrap;text-shadow:-1px 0 #142535,1px 0 #142535,0 -1px #142535,0 1px #142535;pointer-events:none;line-height:1.1}
  #phud .tab{position:absolute;pointer-events:auto;cursor:pointer;display:flex;align-items:center;justify-content:center;color:#e9f3ff;font-weight:600;text-shadow:0 1px 0 #061a2e;border:0;padding:0;background:none;touch-action:none}
  #phud .tab .px{z-index:0;filter:saturate(.8) brightness(.8)}
  #phud .tab.on .px{filter:none}
  #phud .tab.on{color:#ffe28a}
  #phud .tab span{position:relative;z-index:1}
  #phud .tab i{position:absolute;right:2px;top:1px;width:7px;height:7px;border-radius:50%;background:#ff4b3a;z-index:2;display:none}
  #phud .tab.unread i{display:block}
  #phud #log{position:absolute;overflow-y:auto;overflow-x:hidden;pointer-events:auto;font-weight:500;line-height:1.25;scrollbar-width:none;touch-action:pan-y}
  #phud #log::-webkit-scrollbar{display:none}
  #phud #log div{margin:0 0 1px 0;word-break:break-word;text-shadow:0 0 2px rgba(255,255,255,.8)}
  #phud #toast{position:absolute;left:50%;top:22%;transform:translateX(-50%);background:rgba(5,15,18,.7);color:#fff0bb;padding:5px 12px;border-radius:7px;opacity:0;transition:opacity .25s;white-space:nowrap;text-shadow:0 1px 0 #000}
  #phud #menu{position:absolute;display:none;pointer-events:auto;background:rgba(7,48,84,.92);border:2px solid #c9a25a;border-radius:8px;padding:8px}
  #phud #menu.open{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
  #phud #menu button{position:relative;background:none;border:0;color:#fff0bb;font:inherit;display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;text-shadow:-1px 0 #142535,1px 0 #142535,0 -1px #142535,0 1px #142535;touch-action:none}
  #phud #menu button:active{filter:brightness(1.3)}
  #phud #dev{max-height:70%;overflow:auto;position:absolute;display:none;pointer-events:auto;background:rgba(7,48,84,.95);border:2px solid #c9a25a;border-radius:8px;padding:10px;font:12px/1.4 ui-monospace,Menlo,monospace;color:#e8f3ee;min-width:230px}
  #phud #dev.open{display:block}
  #phud #dev b{display:block;margin-bottom:6px;color:#ffe28a;font-family:inherit}
  #phud #dev .row{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:6px}
  #phud #dev button,#phud #dev select{font:12px ui-monospace,Menlo,monospace;padding:6px 8px;border-radius:6px;border:1px solid #4d8a78;background:#143b33;color:#e8f3ee;touch-action:none}
  #phud #dev pre{margin:0;white-space:pre;font:inherit;color:#bfe3d6}`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const root = document.createElement('div'); root.id = 'phud'; document.body.appendChild(root);
  const H = { vec: { x: 0, z: 0 }, shiftFrac: 0, handlers: {}, state: {}, tab: 'all', msgs: [], unread: {} };
  const emit = (n, a) => { (H.handlers[n] || []).forEach((f) => { try { f(a); } catch (e) { console.error(e); } }); };
  H.on = (n, f) => { (H.handlers[n] = H.handlers[n] || []).push(f); };
  const els = [];
  function px(img, cls = '') { const e = document.createElement('div'); e.className = 'px ' + cls; if (img) e.style.backgroundImage = `url(${A(img)})`; return e; }
  function add(parent, e, place) { parent.appendChild(e); if (place) els.push([e, place]); return e; }
  function txt(parent, text, size, place, color, align) { const e = document.createElement('div'); e.className = 't'; e.textContent = text; e.dataset.fs = size; if (color) e.style.color = color; if (align) e.style.textAlign = align; add(parent, e, place); e._fs = size; return e; }
  function hit(parent, place, onDown, onUp, label) { const b = document.createElement('button'); b.className = 'hit'; b.setAttribute('aria-label', label || ''); if (onDown) b.addEventListener('pointerdown', (ev) => { ev.preventDefault(); b.setPointerCapture(ev.pointerId); onDown(ev); }); if (onUp) { b.addEventListener('pointerup', onUp); b.addEventListener('pointercancel', onUp); } add(parent, b, place); return b; }
  // place: (s, W, Hh) => [x,y,w,h] px
  const L = (x, y, w, h) => (s) => [x * s, y * s, w * s, h * s];                       // neo góc trên-trái, theo tọa độ 960x640
  const R = (mx, y, w, h) => (s, W) => [W - (mx + w) * s, y * s, w * s, h * s];       // neo phải
  const B = (x, y, w, h) => (s, W, Hh) => [x * s, Hh - (STRIP - y) * s, w * s, h * s];  // neo đáy-trái (y tính trong dải 186)
  const BR = (mx, y, w, h) => (s, W, Hh) => [W - (mx + w) * s, Hh - (STRIP - y) * s, w * s, h * s];
  const CHAT = (x, y, wTrim, h) => (s, W, Hh) => [(LEFT_W + x) * s, Hh - (STRIP - y) * s, W - (LEFT_W + RIGHT_W) * s - wTrim * s, h * s];

  // ----- dải dưới -----
  add(root, px('panel_controls'), B(0, 0, LEFT_W, STRIP));
  add(root, px('frame_chat'), CHAT(0, 0, 0, STRIP));
  add(root, px('panel_controls'), BR(0, 0, RIGHT_W, STRIP));
  add(root, px('dpad'), B(31, 7, 184, 178));
  // d-pad: 4 hướng theo vị trí chạm + nút giữa = menu
  const dirs = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
  const dpad = hit(root, B(31, 7, 184, 178), null, null, 'D-pad');
  let dpadId = null;
  function dpadMove(ev) {
    const r = dpad.getBoundingClientRect(); const cx = r.left + r.width / 2, cy = r.top + r.height / 2; const dx = ev.clientX - cx, dy = ev.clientY - cy; const m = Math.hypot(dx, dy);
    if (m < r.width * 0.17) { H.vec = { x: 0, z: 0 }; return; }
    const v = Math.abs(dx) > Math.abs(dy) ? { x: Math.sign(dx), z: 0 } : { x: 0, z: Math.sign(dy) }; H.vec = v; emit('input', v);
  }
  dpad.addEventListener('pointerdown', (ev) => { ev.preventDefault(); dpadId = ev.pointerId; dpad.setPointerCapture(ev.pointerId); const r = dpad.getBoundingClientRect(); if (Math.hypot(ev.clientX - (r.left + r.width / 2), ev.clientY - (r.top + r.height / 2)) < r.width * 0.17) { toggleMenu(); return; } dpadMove(ev); pushMove(); });
  dpad.addEventListener('pointermove', (ev) => { if (ev.pointerId === dpadId) { dpadMove(ev); pushMove(); } });
  const dpadEnd = (ev) => { if (ev.pointerId === dpadId) { dpadId = null; H.vec = { x: 0, z: 0 }; pushMove(); } };
  dpad.addEventListener('pointerup', dpadEnd); dpad.addEventListener('pointercancel', dpadEnd);
  function pushMove() { try { window.__godot && window.__godot.move && window.__godot.move(H.vec.x, H.vec.z); } catch (e) { } }

  // chat: 6 tab + log
  const tabEls = {};
  CHANNELS.forEach((c, i) => {
    const b = document.createElement('button'); b.className = 'tab'; b.dataset.id = c.id; b.dataset.i = i;
    b.appendChild(px('tab_menu')); const sp = document.createElement('span'); sp.textContent = c.label; b.appendChild(sp); b.appendChild(document.createElement('i'));
    b.addEventListener('pointerdown', (ev) => { ev.preventDefault(); setTab(c.id); });
    root.appendChild(b); tabEls[c.id] = b; b._fs = 12;
  });
  const logEl = document.createElement('div'); logEl.id = 'log'; root.appendChild(logEl);
  function render() {
    logEl.innerHTML = '';
    const list = H.msgs.filter((m) => H.tab === 'all' || m.ch === H.tab).slice(-60);
    if (!list.length) { const d = document.createElement('div'); d.textContent = 'Chưa có tin nhắn.'; d.style.color = '#4a6a80'; logEl.appendChild(d); }
    for (const m of list) { const d = document.createElement('div'); const c = CHANNELS.find((x) => x.id === m.ch); d.style.color = c ? c.color : '#123548'; d.textContent = (tag[m.ch] ? `[${tag[m.ch]}] ` : '') + m.text; logEl.appendChild(d); }
    logEl.scrollTop = logEl.scrollHeight;
    for (const id in tabEls) { tabEls[id].classList.toggle('on', id === H.tab); tabEls[id].classList.toggle('unread', !!H.unread[id] && id !== H.tab); }
  }
  function setTab(id) { H.tab = id; H.unread[id] = 0; render(); }
  H.log = (ch, text) => { H.msgs.push({ ch, text }); if (H.msgs.length > 300) H.msgs.shift(); if (ch !== H.tab && H.tab !== 'all') H.unread[ch] = 1; render(); };
  H.sysq = (text) => { H.log('sys', text); };
  H.sys = (text) => { H.log('sys', text); showToast(text); };
  let toastT = 0; const toastEl = document.createElement('div'); toastEl.id = 'toast'; root.appendChild(toastEl);
  function showToast(t) { toastEl.textContent = t; toastEl.style.opacity = 1; clearTimeout(toastT); toastT = setTimeout(() => (toastEl.style.opacity = 0), 1600); }

  // Chọn / Trở về
  function btn(id, label, place, ev) {
    add(root, px(id, 'contain'), place);
    const e = root.lastChild; e.style.backgroundSize = 'contain'; e.style.backgroundPosition = 'center';
    const h = hit(root, place, () => emit(ev), null, label); txt(root, label, 16, place, '#ffffff', 'center').style.display = 'flex';
    const t = root.lastChild; t.style.alignItems = 'center'; t.style.justifyContent = 'center';
  }
  btn('button_confirm', 'Chọn', BR(22, 12, 157, 78), 'confirm');
  btn('button_back', 'Trở về', BR(22, 94, 157, 78), 'back');

  // ----- góc trên trái: nhân vật + pet -----
  add(root, px('frame_bars'), L(48, 31, 187, 55));
  const hpFill = add(root, px('bar_hp'), L(71, 40, 142, 11));
  const mpFill = add(root, px('bar_mp'), L(92, 57, 138, 10));
  add(root, px('frame_portrait'), L(6, 5, 93, 88));
  const petImg = px(null); petImg.style.backgroundSize = '400% 500%'; petImg.style.backgroundPosition = '0 0'; add(root, petImg, L(16, 14, 37, 41));
  const plImg = px(null); plImg.style.backgroundSize = '600% 200%'; plImg.style.backgroundPosition = '0 0'; add(root, plImg, L(47, 40, 33, 41));
  const nameT = txt(root, 'Phimond · Lv.1', 16, L(68, 7, 204, 24));
  const hpT = txt(root, '', 11, L(114, 36, 110, 20), '#fff', 'left');
  const mpT = txt(root, '', 11, L(114, 53, 110, 20), '#fff', 'left');
  const petT = txt(root, '', 12, L(56, 88, 200, 18), '#bff4ff');
  const pet = hit(root, L(8, 98, 56, 58), () => H.sys('Linh thú (mẫu: chưa nối menu thật)'), null, 'Linh thú'); pet.appendChild(px('button_pet')); pet.lastChild.style.cssText += ';inset:0;background-size:contain;background-position:center';
  const qst = hit(root, L(8, 163, 56, 58), () => H.sys('Nhiệm vụ (mẫu: chưa nối menu thật)'), null, 'Nhiệm vụ'); qst.appendChild(px('button_quest')); qst.lastChild.style.cssText += ';inset:0;background-size:contain;background-position:center';

  // ----- góc trên phải: tên map, tiền, menu -----
  const titleT = txt(root, 'Rừng Ngọc', 18, R(11, 9, 280, 27), '#fff0bb', 'right');
  const metaT = txt(root, '', 12, R(11, 38, 280, 22), '#fff0bb', 'right');
  const menuBtn = hit(root, R(12, 69, 54, 55), () => toggleMenu(), null, 'Menu'); menuBtn.appendChild(px('button_settings')); menuBtn.lastChild.style.cssText += ';inset:0;background-size:contain;background-position:center';
  const menuEl = document.createElement('div'); menuEl.id = 'menu'; root.appendChild(menuEl);
  // điều hướng giữa các trang đo (cùng thư mục cha): ../three/ <-> ../godot/ , ../index.html
  const here = location.pathname.includes('/godot/') ? 'godot' : 'three';
  const keep = location.search || '';
  const otherUrl = new URL(`../${here === 'godot' ? 'three' : 'godot'}/index.html${keep}`, location.href).href;
  const homeUrl = new URL('../index.html', location.href).href;
  const go = (u) => { H.sys('Đang chuyển trang…'); setTimeout(() => { location.href = u; }, 50); };
  H.otherName = here === 'godot' ? 'Three.js' : 'Godot';
  const ITEMS = [['button_pet', 'Linh thú'], ['button_inventory', 'Vật phẩm'], ['button_quest', 'Nhiệm vụ'], ['button_shop', 'Cửa hàng'], ['button_guild', 'Hội'], ['button_settings', 'Cài đặt'], ['button_round', 'Đổi engine'], ['button_side', 'Trang chọn']];
  for (const [img, label] of ITEMS) {
    const b = document.createElement('button'); const i = document.createElement('div'); i.className = 'px'; i.style.cssText = `position:relative;width:calc(var(--s)*52px);height:calc(var(--s)*52px);background-image:url(${A(img)});background-size:contain;background-position:center;background-repeat:no-repeat;image-rendering:pixelated`;
    const t = document.createElement('span'); t.textContent = label; t.style.fontSize = 'calc(var(--s)*12px)'; b.append(i, t);
    b.addEventListener('pointerdown', (ev) => { ev.preventDefault(); if (label === 'Cài đặt') { devEl.classList.toggle('open'); } else if (label === 'Đổi engine') { go(otherUrl); } else if (label === 'Trang chọn') { go(homeUrl); } else H.sys(label + ' (mẫu: chưa nối menu thật)'); menuEl.classList.remove('open'); });
    menuEl.appendChild(b);
  }
  function toggleMenu() { menuEl.classList.toggle('open'); }

  // ----- bảng dev -----
  const devEl = document.createElement('div'); devEl.id = 'dev';
  devEl.innerHTML = '<b>Cài đặt · đo hiệu năng (dev)</b><div class="row"><select id="d-tier"><option>low</option><option>medium</option><option selected>high</option></select><button id="d-pillar">Trụ → Rừng sâu</button></div><div class="row"><button id="d-bench">Chạy bench 60s</button><button id="d-save">Xuất JSON</button></div><div class="row"><button id="d-other"></button><button id="d-home">Trang chọn</button></div><pre id="d-txt"></pre><b style="margin-top:8px">Kết quả (JSON)</b><textarea id="d-res" readonly rows="4" style="width:100%;font:11px ui-monospace,Menlo,monospace;background:#0b2238;color:#bfe3d6;border:1px solid #4d8a78;border-radius:6px" placeholder="Chạy bench hoặc bấm Xuất JSON"></textarea><div class="row" style="margin-top:6px"><button id="d-copy">Sao chép JSON</button></div>';
  root.appendChild(devEl);
  devEl.querySelector('#d-tier').addEventListener('change', (e) => emit('tier', e.target.value));
  devEl.querySelector('#d-pillar').addEventListener('click', () => emit('pillar'));
  devEl.querySelector('#d-bench').addEventListener('click', () => emit('bench'));
  devEl.querySelector('#d-save').addEventListener('click', () => emit('save'));
  devEl.querySelector('#d-other').textContent = 'Mở bản ' + H.otherName; devEl.querySelector('#d-other').addEventListener('click', () => go(otherUrl)); devEl.querySelector('#d-home').addEventListener('click', () => go(homeUrl));
  const dTxt = devEl.querySelector('#d-txt'); const dRes = devEl.querySelector('#d-res');
  H.setResult = (t) => { dRes.value = t; };
  devEl.querySelector('#d-copy').addEventListener('click', () => { dRes.select(); try { navigator.clipboard.writeText(dRes.value).catch(() => {}); } catch (e) { } try { document.execCommand('copy'); } catch (e) { } });
  H.setDebug = (t) => { dTxt.textContent = t; };
  H.setTier = (t) => { devEl.querySelector('#d-tier').value = t; };
  H.setBenchBusy = (b) => { devEl.querySelector('#d-bench').disabled = b; };
  // góc trên giữa: chỉ báo FPS gọn khi bảng dev đóng
  const fpsT = txt(root, '', 11, (s, W) => [W / 2 - 150 * s, 2 * s, 300 * s, 16 * s], '#d8ffe9', 'center'); fpsT.style.opacity = '.85';
  H.setFps = (t) => { fpsT.textContent = t; };

  // ----- trạng thái -----
  H.setState = (o) => {
    Object.assign(H.state, o); const s = H.state;
    nameT.textContent = `${s.name || 'Phimond'} · Lv.${s.level || 1}`;
    if (s.pet) {
      const p = s.pet; petT.textContent = `${p.name} · Lv.${p.level}`;
      hpFill._r = Math.max(0, Math.min(1, p.hp / p.maxHp)); mpFill._r = Math.max(0, Math.min(1, p.mp / p.maxMp)); applyBars();
      hpT.textContent = `${p.hp} / ${p.maxHp}`; mpT.textContent = `${p.mp} / ${p.maxMp}`;
      if (p.img) petImg.style.backgroundImage = `url(${p.img})`;
    }
    if (s.playerImg) plImg.style.backgroundImage = `url(${s.playerImg})`;
    if (s.map) titleT.textContent = s.map;
    metaT.textContent = `${s.gold ?? 0} vàng   ·   ${s.crystals ?? 0} pha lê`;
  };

  hpFill._r = 1; mpFill._r = 1; hpFill._w = 142; mpFill._w = 138;
  function applyBars() { const s = parseFloat(root.style.getPropertyValue('--s')) || 1; hpFill.style.width = hpFill._w * s * hpFill._r + 'px'; mpFill.style.width = mpFill._w * s * mpFill._r + 'px'; }
  // ----- bố cục -----
  function layout() {
    const W = innerWidth, Hh = innerHeight; const s = Math.max(0.5, Math.min(1.6, Hh / REF_H));
    root.style.setProperty('--s', s);
    for (const [e, pl] of els) { const [x, y, w, h] = pl(s, W, Hh); const st = e.style; st.left = x + 'px'; st.top = y + 'px'; st.width = w + 'px'; st.height = h + 'px'; if (e._fs) st.fontSize = e._fs * s + 'px'; }
    applyBars();
    // chat: tab + log
    const cx = LEFT_W * s, cw = W - (LEFT_W + RIGHT_W) * s, top = Hh - STRIP * s, tabH = 24 * s, gap = 2 * s;
    const tw = (cw - 14 * s - gap * 5) / 6;
    CHANNELS.forEach((c, i) => { const b = tabEls[c.id]; b.style.left = cx + 7 * s + i * (tw + gap) + 'px'; b.style.top = top + 4 * s + 'px'; b.style.width = tw + 'px'; b.style.height = tabH + 'px'; b.style.fontSize = Math.max(9, 12 * s) + 'px'; b.querySelector('.px').style.cssText += ';inset:0;width:100%;height:100%'; });
    logEl.style.left = cx + 8 * s + 'px'; logEl.style.top = top + 32 * s + 'px'; logEl.style.width = cw - 16 * s + 'px'; logEl.style.height = (STRIP - 38) * s + 'px'; logEl.style.fontSize = Math.max(10, 13 * s) + 'px';
    menuEl.style.right = 12 * s + 'px'; menuEl.style.top = 128 * s + 'px'; menuEl.style.fontSize = 12 * s + 'px';
    devEl.style.right = 80 * s + 'px'; devEl.style.top = 70 * s + 'px';
    H.shiftFrac = (STRIP * s) / Hh; window.__hudShiftFrac = H.shiftFrac; emit('layout', { s, W, H: Hh, shift: H.shiftFrac });
  }
  addEventListener('resize', layout);
  // bàn phím
  addEventListener('keydown', (e) => { if (e.key === 'Escape') { if (devEl.classList.contains('open') || menuEl.classList.contains('open')) { devEl.classList.remove('open'); menuEl.classList.remove('open'); emit('back'); } else toggleMenu(); } else if (e.key === ' ' || e.key === 'Enter' || e.key.toLowerCase() === 'e') emit('confirm'); });
  H.on('back', () => { menuEl.classList.remove('open'); devEl.classList.remove('open'); });
  H.on('confirm', () => { /* tương tác: engine có thể ghi đè */ });
  window.PhimondHUD = H;
  errSink = (t) => H.log('sys', t); errQ.splice(0).forEach((t) => H.log('sys', t));
  // dữ liệu mẫu (có thể tắt bằng chatdemo=0)
  H.log('sys', 'Chào mừng đến Phimond');
  H.log('sys', 'Mũi tên / WASD: di chuyển · E: tương tác · Esc: menu');
  if (Q.get('chatdemo') !== '0') {
    H.log('world', 'Aria: Ai đổi Linh Tiên Hoa Hương không? (tin mẫu)');
    H.log('party', 'Bo: Đi Rừng sâu nhé (tin mẫu)');
    H.log('guild', 'Hội trưởng: 20h họp hội (tin mẫu)');
    H.log('pm', 'Elin: Nhận nhiệm vụ rồi chọn pet nhé (tin mẫu)');
  }
  layout();
  };
  if (!document.body) addEventListener('DOMContentLoaded', start); else start();
})();
