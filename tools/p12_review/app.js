'use strict';
const $=id=>document.getElementById(id);
const LAB={pending:'Chờ',approved:'Duyệt',changes_requested:'Cần sửa',rejected:'Từ chối'};
let pkg,hash,fb,dirty=false,busy=false;
function el(t,props,...kids){const e=document.createElement(t);if(props)Object.assign(e,props);for(const k of kids)e.append(k);return e}
function err(m){$('error').hidden=!m;$('error').textContent=m||''}
function mark(){dirty=true;$('save').disabled=false;$('save-state').textContent='Có thay đổi chưa lưu';progress()}
function progress(){const v=Object.values(fb.decisions);const a=v.filter(x=>x.status==='approved').length;$('progress').textContent=`Đã duyệt ${a}/${v.length} nhóm`;
 const k=document.querySelectorAll('nav button[data-id]');k.forEach(b=>{const s=fb.decisions[b.dataset.id].status;b.lastChild.textContent=s==='approved'?'✓':s==='pending'?'':'!'})}
function card(d){
  const c=el('article',{className:'card',id:'c-'+d.id});
  c.append(el('div',{className:'cat'},d.category),el('h3',null,d.title),el('p',null,d.summary));
  if(d.columns&&d.columns.length){const t=el('table'),h=el('tr');d.columns.forEach(x=>h.append(el('th',null,x)));t.append(h);
    d.rows.forEach(r=>{const tr=el('tr');r.forEach(x=>tr.append(el('td',null,String(x))));t.append(tr)});c.append(t)}
  c.append(el('p',{className:'muted'},d.rationale));
  const st=el('div',{className:'st'});
  for(const s of Object.keys(LAB)){const i=el('input',{type:'radio',name:'s-'+d.id,value:s,checked:fb.decisions[d.id].status===s});
    const l=el('label',null,i,LAB[s]);if(i.checked)l.className='on';
    i.onchange=()=>{fb.decisions[d.id].status=s;st.querySelectorAll('label').forEach(x=>x.className='');l.className='on';mark()};st.append(l)}
  const ta=el('textarea',{rows:2,placeholder:'Góp ý (tùy chọn)',value:fb.decisions[d.id].comment});
  ta.oninput=()=>{fb.decisions[d.id].comment=ta.value;mark()};c.append(st,ta);return c}
function render(){
  $('title').textContent=pkg.title;$('intro').textContent=pkg.summary+' — '+pkg.status;
  const nav=$('nav'),cont=$('content');let last='';
  pkg.decisions.forEach(d=>{if(d.category!==last){nav.append(el('div',{className:'cat'},d.category));last=d.category}
    const b=el('button',{type:'button'},el('span',null,d.title),el('b'));b.dataset.id=d.id;b.onclick=()=>$('c-'+d.id).scrollIntoView({behavior:'smooth'});nav.append(b);cont.append(card(d))});
  $('notes').value=fb.notes;$('verdict').value=fb.verdict;$('hash').textContent='Gói '+hash.slice(0,12);progress();
  $('save-state').textContent=fb.updated_at?'Đã lưu '+new Date(fb.updated_at).toLocaleString('vi-VN'):'Chưa lưu'}
async function save(verdict){
  if(busy)return;busy=true;err('');
  try{const r=await fetch('/api/feedback',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({package_hash:hash,version:fb.version,decisions:fb.decisions,notes:$('notes').value,verdict})});
    const j=await r.json();if(!r.ok){err(j.error||'Lỗi lưu');return}
    fb=j.feedback;dirty=false;$('save').disabled=true;$('verdict').value=fb.verdict;$('save-state').textContent='Đã lưu '+new Date(fb.updated_at).toLocaleString('vi-VN')}
  catch(e){err('Không kết nối được server.')}finally{busy=false}}
$('save').onclick=()=>save('draft');
$('submit').onclick=()=>save($('verdict').value);
$('notes').oninput=mark;
$('approve-all').onclick=()=>{for(const [id,x] of Object.entries(fb.decisions))if(x.status==='pending'){x.status='approved'}
  document.querySelectorAll('.card').forEach(c=>{const id=c.id.slice(2);c.querySelectorAll('label').forEach(l=>{const i=l.firstChild;i.checked=i.value===fb.decisions[id].status;l.className=i.checked?'on':''})});mark()};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify({package_hash:hash,unsaved_changes:dirty,feedback:fb},null,2)],{type:'application/json'});
  const a=el('a',{href:URL.createObjectURL(blob),download:'p12-review.json'});a.click()};
window.onbeforeunload=e=>{if(dirty){e.preventDefault();return ''}};
fetch('/api/review').then(r=>r.json()).then(j=>{pkg=j.package;hash=j.package_hash;fb=j.feedback;render()}).catch(()=>err('Không tải được gói duyệt.'));
