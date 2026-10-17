'use strict';
const $ = id => document.getElementById(id);
const SVGNS = 'http://www.w3.org/2000/svg';
function h(tag, attrs, ...kids) { const e = document.createElement(tag); for (const [k, v] of Object.entries(attrs || {})) { if (k === 'class') e.className = v; else if (k.startsWith('on')) e[k] = v; else if (k === 'text') e.textContent = v; else if (k === 'value') e.value = v; else e.setAttribute(k, v); } for (const c of kids) e.append(c); return e; }
function sv(tag, attrs, ...kids) { const e = document.createElementNS(SVGNS, tag); for (const [k, v] of Object.entries(attrs || {})) { if (k === 'class') e.setAttribute('class', v); else if (k === 'text') e.textContent = v; else e.setAttribute(k, v); } for (const c of kids) e.append(c); return e; }
const S = { filter: 'all', base: { ports: [], links: [] }, maps: [], M: {}, ports: [], links: [], version: 0, hash: '', A: 'city_square', B: 'treasure_beach_east_beach', mode: 'link', view: 'mind', sel: null, dirty: false, baseChanged: false };
const STAT = { pending: 'Chờ', approved: 'Duyệt', changes_requested: 'Cần sửa', rejected: 'Từ chối' };
const P = id => S.ports.find(p => p.id === id);
const baseL = id => S.base.links.find(l => l.id === id);
function diffOf(l) {
  const o = baseL(l.id); if (!o) return ['liên kết mới do bạn tạo'];
  const d = []; if (o.a !== l.a || o.b !== l.b) d.push('đổi đầu nối'); if (o.oneway !== l.oneway) d.push(l.oneway ? 'APK hai chiều → bạn đặt một chiều' : 'APK một chiều → bạn đặt hai chiều'); if ((o.comment || '') !== (l.comment || '')) d.push('có nhận xét mới'); return d;
}
const isNew = l => diffOf(l).length > 0;
const bTitle = id => { const p = P(id) || S.base.ports.find(x => x.id === id); return p ? portTitle(p) : id; };
const goneLinks = () => S.base.links.filter(o => !S.links.some(l => l.id === o.id));
function match(l, f = S.filter) { return f === 'all' || (f === 'approved' && l.status === 'approved') || (f === 'todo' && l.status !== 'approved') || (f === 'pending' && l.status === 'pending') || (f === 'changes' && (l.status === 'changes_requested' || l.status === 'rejected')) || (f === 'edited' && isNew(l)) || (f === 'claude' && !!l.rev); }
function restoreLink(o) {
  for (const id of [o.a, o.b]) if (!P(id)) { const bp = S.base.ports.find(p => p.id === id); if (bp) S.ports.push(JSON.parse(JSON.stringify(bp))); }
  if (P(o.a) && P(o.b)) { S.links.push(JSON.parse(JSON.stringify(o))); S.sel = { type: 'link', id: o.id }; mark(); render(); }
}
const linksOf = m => S.links.filter(l => P(l.a).map === m || P(l.b).map === m);
function err(m) { $('error').hidden = !m; $('error').textContent = m || ''; }
function mark() { S.dirty = true; $('save').disabled = false; $('save-state').textContent = 'Có thay đổi chưa lưu'; stats(); }
function toPx(m, xy) { const b = S.M[m].bounds; return [(xy[0] - b[0]) * 100, (b[3] - xy[1]) * 100]; }
function toWorld(m, px) { const b = S.M[m].bounds; return [+(px[0] / 100 + b[0]).toFixed(2), +(b[3] - px[1] / 100).toFixed(2)]; }
function stats() {
  const c = { pending: 0, approved: 0, changes_requested: 0, rejected: 0 }; S.links.forEach(l => c[l.status]++);
  const flag = S.ports.filter(p => p.flag === 'cần đặt').length;
  const FL = { all: 'Tất cả', approved: 'Đã duyệt', todo: 'Chưa duyệt', pending: 'Chờ', changes: 'Cần sửa', edited: 'Mới sửa', claude: 'Claude sửa' };
  document.querySelectorAll('#filters button').forEach(b => { const f = b.dataset.f, n = S.links.filter(l => match(l, f)).length + (f === 'edited' ? goneLinks().length : 0); b.textContent = `${FL[f]} ${n}`; b.classList.toggle('on', f === S.filter); });
  const np = S.links.filter(l => l.status === 'pending' && match(l)).length; $('approve-all').textContent = `Duyệt ${np} liên kết chờ${S.filter === 'all' ? '' : ' (đang lọc)'}`; $('approve-all').disabled = !np;
  $('stats').textContent = `${S.links.length} liên kết · duyệt ${c.approved} · cần sửa ${c.changes_requested + c.rejected} · chờ ${c.pending} · ${flag} điểm cần đặt` + (S.baseChanged ? ' · dữ liệu gốc đã đổi' : '');
}
function nid(prefix, list) { let n = list.length + 1; while (list.some(x => x.id === prefix + String(n).padStart(3, '0'))) n++; return prefix + String(n).padStart(3, '0'); }
function mapName(m) { return S.M[m] ? S.M[m].name : m; }
function portTitle(p) { return `${mapName(p.map)} · ${p.label}`; }
function openMaps(a, b) { if (a) S.A = a; if (b) S.B = b; setView('split'); }
function setView(v) { S.view = v; $('v-mind').hidden = v !== 'mind'; $('v-split').hidden = v !== 'split'; document.querySelectorAll('#views button').forEach(b => b.classList.toggle('on', b.dataset.v === v)); render(); }
// ---------- mind map ----------
const GORDER = ['Khởi đầu', 'Emerald', 'Thành phố', 'Bãi biển', 'Hải Tặc Hào', 'Sa Mạc', 'Mỏm Đá Gió', 'Đảo Ác Mộng', 'Lăng Mộ', 'Giao Điểm', 'Tinh Không', 'Di Tích Cổ', 'Lâu Đài Ma', 'Cây Thế Giới', 'Tháp Chim', 'Mê Thành'];
function layoutMind() {
  const CW = 236, NW = 108, NH = 26, COLS = 4, colH = [30, 30, 30, 30], pos = {}, boxes = [];
  for (const g of GORDER) {
    const ms = S.maps.filter(m => m.group === g); if (!ms.length) continue;
    const rows = Math.ceil(ms.length / 2), hgt = 28 + rows * 34 + 8;
    const c = colH.indexOf(Math.min(...colH)), x = 16 + c * (CW + 16), y = colH[c];
    boxes.push({ g, x, y, w: CW, h: hgt });
    ms.forEach((m, i) => { pos[m.id] = [x + 8 + (i % 2) * (NW + 8) + NW / 2, y + 28 + Math.floor(i / 2) * 34 + NH / 2]; });
    colH[c] += hgt + 18;
  }
  return { pos, boxes, W: 16 + COLS * (CW + 16), H: Math.max(...colH) + 10, NW, NH };
}
function renderMind() {
  const L = layoutMind(), svg = $('mind'); svg.innerHTML = ''; svg.setAttribute('width', L.W); svg.setAttribute('height', L.H); svg.setAttribute('viewBox', `0 0 ${L.W} ${L.H}`);
  for (const b of L.boxes) { svg.append(sv('rect', { class: 'cl', x: b.x, y: b.y, width: b.w, height: b.h, rx: 8 }), sv('text', { class: 'ct', x: b.x + 10, y: b.y + 18, text: b.g })); }
  const pairs = {};
  const live = new Set();
  for (const l of S.links) {
    if (!match(l)) continue;
    const a = P(l.a).map, b = P(l.b).map; if (a === b) continue; live.add(a); live.add(b);
    const k = [a, b].sort().join('|'); (pairs[k] = pairs[k] || { a: [a, b].sort()[0], b: [a, b].sort()[1], ls: [] }).ls.push(l);
  }
  const g = sv('g'); svg.append(g);
  for (const pr of Object.values(pairs)) {
    const p1 = L.pos[pr.a], p2 = L.pos[pr.b], mx = (p1[0] + p2[0]) / 2, my = (p1[1] + p2[1]) / 2, dx = p2[0] - p1[0], dy = p2[1] - p1[1], n = Math.hypot(dx, dy) || 1;
    const bend = Math.min(60, n * 0.18), cx = mx - dy / n * bend, cy = my + dx / n * bend;
    const st = pr.ls.some(l => l.status === 'changes_requested' || l.status === 'rejected') ? 'changes_requested' : pr.ls.every(l => l.status === 'approved') ? 'approved' : 'pending';
    const pil = pr.ls.every(l => P(l.a).kind === 'pillar');
    const e = sv('path', { class: `me ${st}${pil ? ' pillar' : ''}${pr.ls.some(x => isNew(x) || x.rev) ? ' ed' : ''}`, d: `M${p1[0]},${p1[1]} Q${cx},${cy} ${p2[0]},${p2[1]}`, 'marker-end': '' }, sv('title', { text: pr.ls.map(l => `${portTitle(P(l.a))} ${l.oneway ? '→' : '↔'} ${portTitle(P(l.b))}`).join('\n') }));
    e.onclick = () => { S.sel = { type: 'link', id: pr.ls[0].id }; openMaps(pr.a, pr.b); };
    g.append(e);
    if (pr.ls.every(l => l.oneway)) { const dir = pr.ls.every(l => P(l.a).map === pr.a) ? [pr.a, pr.b] : pr.ls.every(l => P(l.a).map === pr.b) ? [pr.b, pr.a] : null; if (dir) { const q = L.pos[dir[1]], t = 0.86, bx = (1 - t) * (1 - t) * L.pos[dir[0]][0] + 2 * (1 - t) * t * cx + t * t * q[0], by = (1 - t) * (1 - t) * L.pos[dir[0]][1] + 2 * (1 - t) * t * cy + t * t * q[1]; const ang = Math.atan2(q[1] - by, q[0] - bx) * 180 / Math.PI; g.append(sv('path', { d: 'M-6,-4 L4,0 L-6,4 Z', transform: `translate(${bx},${by}) rotate(${ang})`, fill: '#888', 'pointer-events': 'none' })); } }
  }
  const selfs = {};
  for (const l of S.links) { if (!match(l)) continue; const a = P(l.a).map; if (a === P(l.b).map) (selfs[a] = selfs[a] || []).push(l); }
  for (const m of S.maps) {
    const [x, y] = L.pos[m.id], n = sv('g', { class: 'mn' + (S.filter !== 'all' && !live.has(m.id) ? ' dim' : '') + (m.id === S.A ? ' a' : '') + (m.id === S.B ? ' b' : '') }, sv('title', { text: m.name + ' (' + m.id + ')' }), sv('rect', { x: x - L.NW / 2, y: y - L.NH / 2, width: L.NW, height: L.NH, rx: 5 }), sv('text', { x: x - L.NW / 2 + 5, y: y + 4, text: m.name.length > 17 ? m.name.slice(0, 16) + '…' : m.name }));
    n.onclick = ev => { if (ev.shiftKey) S.B = m.id; else S.A = m.id; renderMind(); renderLinks(); };
    n.ondblclick = () => openMaps(m.id, null);
    svg.append(n);
    const sl = selfs[m.id];
    if (sl) {
      const st = sl.some(l => l.status === 'changes_requested' || l.status === 'rejected') ? 'changes_requested' : sl.every(l => l.status === 'approved') ? 'approved' : 'pending';
      const bd = sv('g', { class: `selfb ${st}${sl.some(isNew) ? ' ed' : ''}` }, sv('title', { text: 'Liên kết trong cùng map (qua tầng, nối cửa với cửa):\n' + sl.map(l => `${portTitle(P(l.a))} ${l.oneway ? '→' : '↔'} ${portTitle(P(l.b))}`).join('\n') }), sv('circle', { cx: x + L.NW / 2 - 2, cy: y - L.NH / 2 + 2, r: 9 }), sv('text', { x: x + L.NW / 2 - 2, y: y - L.NH / 2 + 6, 'text-anchor': 'middle', text: '↻' + (sl.length > 1 ? sl.length : '') }));
      bd.onclick = () => { S.sel = { type: 'link', id: sl[0].id }; openMaps(m.id, m.id); };
      svg.append(bd);
    }
  }
}
// ---------- hai bản đồ ----------
function renderPane(w) {
  const el = $('pane-' + w), mid = S[w], m = S.M[mid]; el.innerHTML = '';
  const sel = h('select', { id: 'sel-' + w, 'aria-label': 'Bản đồ ' + w });
  for (const g of GORDER) { const og = h('optgroup', { label: g }); S.maps.filter(x => x.group === g).forEach(x => og.append(h('option', { value: x.id, text: x.name, selected: x.id === mid ? '' : null }))); if (og.children.length) sel.append(og); }
  sel.value = mid; sel.onchange = () => { S[w] = sel.value; render(); };
  const wrap = h('div', { class: 'wrap' }), img = h('img', { src: '/map-images/' + mid + '.png', alt: m.name });
  img.onerror = () => { const nn = h('div', { class: 'none' }, 'Không có ảnh map (' + mid + '.png). Chạy server với --images trỏ tới thư mục map-images.'); nn.style.aspectRatio = m.size[0] + '/' + m.size[1]; img.replaceWith(nn); };
  const ov = sv('svg', { class: 'ov', viewBox: `0 0 ${m.size[0]} ${m.size[1]}`, preserveAspectRatio: 'none' }); ov.dataset.map = mid; ov.dataset.w = w;
  for (const p of S.ports.filter(q => q.map === mid)) {
    const [x, y] = toPx(mid, p.xy), g = sv('g');
    const c = sv('circle', { class: `pt ${p.kind}${S.sel && S.sel.type === 'port' && S.sel.id === p.id ? ' sel' : ''}${p.flag === 'cần đặt' ? ' flag' : ''}`, cx: x, cy: y, r: 36, 'data-port': p.id }, sv('title', { text: p.label + (p.flag ? ' · ' + p.flag : '') }));
    c.onpointerdown = ev => startDrag(ev, p);
    g.append(c, sv('text', { class: 'ptlabel', x: x + 44, y: y + 12, text: p.label.length > 22 ? p.label.slice(0, 21) + '…' : p.label })); ov.append(g);
  }
  ov.onpointerdown = ev => { if (ev.target === ov && S.mode === 'add') addPortAt(ev, ov); };
  wrap.append(img, ov); el.append(sel, wrap);
}
function svgPoint(ov, ev) { const r = ov.getBoundingClientRect(), vb = ov.viewBox.baseVal; return [(ev.clientX - r.left) / r.width * vb.width, (ev.clientY - r.top) / r.height * vb.height]; }
function addPortAt(ev, ov) {
  const mid = ov.dataset.map, id = nid('N:', S.ports), xy = toWorld(mid, svgPoint(ov, ev));
  S.ports.push({ id, map: mid, xy, kind: 'door', label: 'Cổng mới', origin: 'edited', flag: null }); S.sel = { type: 'port', id }; mark(); render();
}
let drag = null;
function startDrag(ev, p) {
  ev.preventDefault(); ev.stopPropagation();
  S.sel = { type: 'port', id: p.id };
  drag = { p, mode: S.mode, moved: false, ov: ev.target.closest('svg') };
  ev.target.setPointerCapture && ev.target.setPointerCapture(ev.pointerId);
  document.onpointermove = onMove; document.onpointerup = onUp; renderInspector();
}
function onMove(ev) {
  if (!drag) return; drag.moved = true;
  if (drag.mode === 'move') { const xy = toWorld(drag.p.map, svgPoint(drag.ov, ev)); drag.p.xy = xy; drag.p.flag = drag.p.flag === 'cần đặt' ? null : drag.p.flag; const c = drag.ov.querySelector(`[data-port="${CSS.escape(drag.p.id)}"]`), px = toPx(drag.p.map, xy); c.setAttribute('cx', px[0]); c.setAttribute('cy', px[1]); drawWires(); return; }
  if (drag.mode === 'link') {
    const w = $('wire'), r = $('split').getBoundingClientRect(), c = document.querySelector(`[data-port="${CSS.escape(drag.p.id)}"]`).getBoundingClientRect();
    let t = w.querySelector('.tmp'); if (!t) { t = sv('line', { class: 'tmp', stroke: '#ffeb3b', 'stroke-width': 3, 'stroke-dasharray': '6 4' }); w.append(t); }
    t.setAttribute('x1', c.left + c.width / 2 - r.left); t.setAttribute('y1', c.top + c.height / 2 - r.top); t.setAttribute('x2', ev.clientX - r.left); t.setAttribute('y2', ev.clientY - r.top);
  }
}
function onUp(ev) {
  document.onpointermove = null; document.onpointerup = null; const d = drag; drag = null; const t = $('wire').querySelector('.tmp'); if (t) t.remove();
  if (!d) return;
  if (d.mode === 'move') { if (d.moved) { d.p.origin = 'edited'; mark(); } render(); return; }
  if (d.mode !== 'link' || !d.moved) { render(); return; }
  const el = document.elementFromPoint(ev.clientX, ev.clientY); const tp = el && el.closest && el.closest('[data-port]');
  if (tp && tp.dataset.port !== d.p.id) { connect(d.p, P(tp.dataset.port)); return; }
  const ov = el && el.closest && el.closest('svg.ov');
  if (ov && ov.dataset.map) {
    const id = nid('N:', S.ports), xy = toWorld(ov.dataset.map, svgPoint(ov, ev));
    S.ports.push({ id, map: ov.dataset.map, xy, kind: 'arrival', label: 'Điểm đến từ ' + mapName(d.p.map), origin: 'edited', flag: null }); connect(d.p, P(id)); return;
  }
  render();
}
function connect(a, b) {
  const dup = S.links.find(l => (l.a === a.id && l.b === b.id) || (l.a === b.id && l.b === a.id));
  if (dup) { S.sel = { type: 'link', id: dup.id }; err('Hai điểm này đã có liên kết.'); render(); return; }
  err('');
  const one = a.kind === 'pillar' || a.kind === 'arrival' || b.kind === 'arrival' || b.kind === 'pillar';
  const l = { id: nid('L', S.links), a: a.id, b: b.id, oneway: one, origin: 'edited', note: 'Tạo trong web review.', door_ids: [], mode: null, status: 'pending', comment: '' };
  S.links.push(l); S.sel = { type: 'link', id: l.id }; mark(); render();
}
function drawWires() {
  const w = $('wire'); w.innerHTML = ''; if (S.view !== 'split') return;
  const r = $('split').getBoundingClientRect(); w.setAttribute('viewBox', `0 0 ${r.width} ${r.height}`);
  const ctr = id => { const c = document.querySelector(`[data-port="${CSS.escape(id)}"]`); if (!c) return null; const b = c.getBoundingClientRect(); return [b.left + b.width / 2 - r.left, b.top + b.height / 2 - r.top]; };
  for (const l of S.links) {
    if (!match(l)) continue;
    const a = ctr(l.a), b = ctr(l.b); if (!a || !b) continue;
    const o = P(l.a).kind === 'pillar' ? ' owner' : '', sel = S.sel && S.sel.type === 'link' && S.sel.id === l.id ? ' sel' : '';
    const dx = b[0] - a[0], dy = b[1] - a[1], n = Math.hypot(dx, dy) || 1, cx = (a[0] + b[0]) / 2 - dy / n * 24, cy = (a[1] + b[1]) / 2 + dx / n * 24;
    const p = sv('path', { class: `wl ${l.status}${o}${sel}${isNew(l) ? ' ed' : ''}`, d: `M${a[0]},${a[1]} Q${cx},${cy} ${b[0]},${b[1]}` }, sv('title', { text: `${portTitle(P(l.a))} ${l.oneway ? '→' : '↔'} ${portTitle(P(l.b))}` }));
    p.onclick = () => { S.sel = { type: 'link', id: l.id }; render(); };
    w.append(p);
    if (l.oneway) { const t = 0.5, bx = (1 - t) * (1 - t) * a[0] + 2 * (1 - t) * t * cx + t * t * b[0], by = (1 - t) * (1 - t) * a[1] + 2 * (1 - t) * t * cy + t * t * b[1], ang = Math.atan2(b[1] - cy, b[0] - cx) * 180 / Math.PI; w.append(sv('path', { d: 'M-8,-6 L6,0 L-8,6 Z', transform: `translate(${bx},${by}) rotate(${ang})`, fill: '#ddd', stroke: '#333', 'stroke-width': 1, 'pointer-events': 'none' })); }
  }
}
function renderLinks() {
  const box = $('links'); box.innerHTML = '';
  const global = S.view === 'mind' && S.filter !== 'all';
  const ls = S.links.filter(l => match(l) && (global || (() => { const a = P(l.a).map, b = P(l.b).map; return a === S.A || a === S.B || b === S.A || b === S.B; })()));
  box.append(h('div', { class: 'flt-head', text: global ? `Mọi map · ${ls.length} liên kết khớp bộ lọc${S.filter === 'edited' ? ` · ${goneLinks().length} đã xóa` : ''}` : `Hai map đang mở · ${ls.length} liên kết${S.filter === 'all' ? '' : ' khớp bộ lọc'}` }));
  if (!ls.length) box.append(h('p', { class: 'muted pad' }, 'Không có liên kết nào khớp.'));
  for (const l of ls) {
    const it = h('div', { class: 'li' + (S.sel && S.sel.type === 'link' && S.sel.id === l.id ? ' sel' : '') }, h('span', { class: 'chip ' + l.status, text: STAT[l.status] }), isNew(l) ? h('span', { class: 'chip ed', text: '✎', title: diffOf(l).join('; ') }) : '', l.rev ? h('span', { class: 'chip cl', text: 'Claude', title: l.reply || '' }) : '', h('span', { class: 't', text: `${mapName(P(l.a).map)} ${l.oneway ? '→' : '↔'} ${mapName(P(l.b).map)}`, title: `${portTitle(P(l.a))} ${l.oneway ? '→' : '↔'} ${portTitle(P(l.b))}` }));
    it.onclick = () => { S.sel = { type: 'link', id: l.id }; const a = P(l.a).map, b = P(l.b).map; if (a !== S.A && a !== S.B && b !== S.A && b !== S.B) { S.A = a; S.B = b; } render(); };
    box.append(it);
  }
  if (S.filter === 'edited') for (const o of goneLinks()) {
    const r = h('button', { class: 'secondary', text: 'Khôi phục' }); r.onclick = () => restoreLink(o);
    box.append(h('div', { class: 'li gone' }, h('span', { class: 'chip', text: 'Đã xóa' }), h('span', { class: 't', text: `${bTitle(o.a)} ${o.oneway ? '→' : '↔'} ${bTitle(o.b)}`, title: `${o.id}: ${o.a} ↔ ${o.b}` }), r));
  }
}
function renderInspector() {
  const box = $('inspector'); box.innerHTML = '';
  if (!S.sel) { box.append(h('p', { class: 'muted' }, 'Chọn một liên kết hoặc một điểm để xem và sửa.')); return; }
  if (S.sel.type === 'link') {
    const l = S.links.find(x => x.id === S.sel.id); if (!l) { S.sel = null; return renderInspector(); }
    const a = P(l.a), b = P(l.b);
    box.append(h('b', { text: `${l.id} · ${l.origin === 'apk' ? 'APK' : l.origin === 'owner' ? 'Quyết định owner' : 'Bạn sửa'}` }), h('p', { text: `${portTitle(a)} ${l.oneway ? '→' : '↔'} ${portTitle(b)}` }), h('p', { class: 'muted', text: l.note || '' }));
    if (l.reply) box.append(h('p', { class: 'reply', text: 'Claude (' + (l.rev || '') + '): ' + l.reply }));
    if (isNew(l)) box.append(h('p', { class: 'diff', text: '✎ Khác bản nháp APK: ' + diffOf(l).join('; ') }));
    const one = h('input', { type: 'checkbox', id: 'i-one' }); one.checked = l.oneway; one.onchange = () => { l.oneway = one.checked; mark(); render(); };
    box.append(h('label', { for: 'i-one' }, one, ' Một chiều (A → B)'));
    const st = h('div', { class: 'row' });
    for (const k of Object.keys(STAT)) { const i = h('input', { type: 'radio', name: 'st', id: 'st-' + k, value: k }); i.checked = l.status === k; i.onchange = () => { l.status = k; mark(); render(); }; st.append(h('label', { for: 'st-' + k, class: 'inl' }, i, ' ' + STAT[k])); }
    const ta = h('textarea', { rows: 3, id: 'i-comment', placeholder: 'Nhận xét', value: l.comment }); ta.oninput = () => { l.comment = ta.value; mark(); };
    const sw = h('button', { class: 'secondary', text: 'Đổi chiều' }); sw.onclick = () => { [l.a, l.b] = [l.b, l.a]; mark(); render(); };
    const op = h('button', { class: 'secondary', text: 'Mở hai map' }); op.onclick = () => { S.A = a.map; S.B = b.map; setView('split'); };
    const del = h('button', { class: 'secondary', text: 'Xóa liên kết' }); let armed = false; del.onclick = () => { if (!armed) { armed = true; del.textContent = 'Bấm lần nữa để xóa'; return; } removeLink(l.id); };
    box.append(st, h('label', { for: 'i-comment', text: 'Nhận xét' }), ta, h('div', { class: 'row' }, sw, op, del));
  } else {
    const p = P(S.sel.id); if (!p) { S.sel = null; return renderInspector(); }
    box.append(h('b', { text: `Điểm ${p.id}` }), h('p', { class: 'muted', text: `${mapName(p.map)} · (${p.xy[0]}, ${p.xy[1]})${p.flag ? ' · ' + p.flag : ''}` }));
    const lab = h('input', { type: 'text', id: 'i-label', value: p.label, class: 'full' }); lab.oninput = () => { p.label = lab.value.slice(0, 200); mark(); };
    const kind = h('select', { id: 'i-kind' }); for (const k of ['door', 'pillar', 'arrival']) kind.append(h('option', { value: k, text: { door: 'Cửa', pillar: 'Trụ', arrival: 'Điểm đến' }[k] })); kind.value = p.kind; kind.onchange = () => { p.kind = kind.value; mark(); render(); };
    const linked = S.links.some(l => l.a === p.id || l.b === p.id), del = h('button', { class: 'secondary', text: linked ? 'Xóa các liên kết trước' : 'Xóa điểm' }); del.disabled = linked; del.onclick = () => { S.ports = S.ports.filter(x => x.id !== p.id); S.sel = null; mark(); render(); };
    box.append(h('label', { for: 'i-label', text: 'Nhãn' }), lab, h('label', { for: 'i-kind', text: 'Loại' }), kind, h('div', { class: 'row' }, del));
  }
}
function removeLink(id) {
  const l = S.links.find(x => x.id === id); S.links = S.links.filter(x => x.id !== id); S.sel = null;
  for (const pid of [l.a, l.b]) { const p = P(pid); if (p && p.kind === 'arrival' && p.origin !== 'apk' && !S.links.some(x => x.a === pid || x.b === pid)) S.ports = S.ports.filter(x => x.id !== pid); }
  mark(); render();
}
function render() {
  if (S.view === 'mind') renderMind(); else { $('pane-B').hidden = S.A === S.B; renderPane('A'); if (S.A !== S.B) renderPane('B'); }
  renderLinks(); renderInspector(); stats();
  requestAnimationFrame(() => { drawWires(); }); setTimeout(drawWires, 300);
}
async function save() {
  err(''); $('save').disabled = true;
  try {
    const r = await fetch('/api/portals', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ version: S.version, graph: { ports: S.ports, links: S.links } }) });
    const j = await r.json(); if (!r.ok) { err(j.error || 'Lỗi lưu'); $('save').disabled = false; return; }
    S.version = j.version; S.dirty = false; $('save-state').textContent = 'Đã lưu ' + new Date(j.updated_at).toLocaleString('vi-VN');
  } catch (e) { err('Không kết nối được server.'); $('save').disabled = false; }
}
$('save').onclick = save;
document.querySelectorAll('#views button').forEach(b => b.onclick = () => setView(b.dataset.v));
document.querySelectorAll('#modes button').forEach(b => b.onclick = () => { S.mode = b.dataset.m; document.querySelectorAll('#modes button').forEach(x => x.classList.toggle('on', x === b)); });
$('approve-all').onclick = () => { S.links.forEach(l => { if (l.status === 'pending' && match(l)) l.status = 'approved'; }); mark(); render(); };
document.querySelectorAll('#filters button').forEach(b => b.onclick = () => { S.filter = b.dataset.f; render(); });
let flagIdx = 0;
$('next-flag').onclick = () => {
  const fl = S.ports.filter(p => p.flag === 'cần đặt'); if (!fl.length) { err('Không còn điểm cần đặt.'); return; } err('');
  const p = fl[flagIdx++ % fl.length]; const l = S.links.find(x => x.a === p.id || x.b === p.id), o = l && P(l.a === p.id ? l.b : l.a);
  S.A = p.map; if (o) S.B = o.map; S.sel = { type: 'port', id: p.id }; setView('split');
};
window.addEventListener('resize', drawWires);
window.onbeforeunload = e => { if (S.dirty) { e.preventDefault(); return ''; } };
fetch('/api/portals').then(r => r.json()).then(j => {
  S.maps = j.maps; S.M = Object.fromEntries(j.maps.map(m => [m.id, m])); S.ports = j.graph.ports; S.links = j.graph.links; S.base = j.baseline || S.base; S.version = j.version; S.hash = j.package_hash; S.baseChanged = j.base_changed;
  $('save-state').textContent = j.updated_at ? 'Đã lưu ' + new Date(j.updated_at).toLocaleString('vi-VN') : 'Chưa lưu'; render();
}).catch(() => err('Không tải được đồ thị. Chạy build_portals.py trước.'));
