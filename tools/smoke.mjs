// Real HTTP/WebSocket contract smoke. Creates two isolated test accounts.
// Run: node tools/smoke.mjs. Tokens/passwords are never printed.
import assert from 'node:assert/strict';
import { randomBytes } from 'node:crypto';
const base=process.env.GAME_API_URL||'http://127.0.0.1:8090';
const credentials=()=>({username:'smoke_'+randomBytes(6).toString('hex'),password:randomBytes(20).toString('hex')});
async function api(path,method='GET',data,token){const r=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})},body:data?JSON.stringify(data):undefined});return [r.status,await r.json()];}
const aCred=credentials(),bCred=credentials();let a,b,socket;
try{
 let code;[code,a]=await api('/api/register','POST',aCred);assert.equal(code,200);[code,b]=await api('/api/register','POST',bCred);assert.equal(code,200);
 const [_,character]=await api('/api/character','GET',undefined,a.token);
 assert.equal((await api('/api/lineage/'+character.pets[0].id,'GET',undefined,b.token))[0],404);
 socket=new WebSocket(base.replace('http','ws')+'/ws');await new Promise((resolve,reject)=>{socket.onopen=resolve;socket.onerror=reject});
 const waiting=new Map();socket.onmessage=event=>{const m=JSON.parse(event.data);waiting.get(m.request_id)?.(m);waiting.delete(m.request_id)};
 let sequence=0;const send=(op,data={},id='smoke-'+(++sequence))=>new Promise((resolve,reject)=>{const timer=setTimeout(()=>{waiting.delete(id);reject(Error('timeout '+op))},20000);waiting.set(id,m=>{clearTimeout(timer);resolve(m)});socket.send(JSON.stringify({op,request_id:id,data}))});
 let m=await send('auth.session',{token:a.token});assert.equal(m.op,'state');
 m=await send('shop.buy',{item_id:'potion',quantity:1},'dedup-shop');assert.equal(m.op,'state');const gold=m.data.character.gold;const qty=m.data.character.inventory.potion;
 m=await send('shop.buy',{item_id:'potion',quantity:1},'dedup-shop');assert.equal(m.data.character.gold,gold);assert.equal(m.data.character.inventory.potion,qty);
 m=await send('world.move',{direction:'left',damage:999});assert.equal(m.op,'error');assert.match(m.data.message,/invalid intent/);
 const before=m=await send('character.get');m=await send('world.move',{direction:'left'});assert.equal(m.data.character.x,before.data.character.x-1);
 const restored=(await api('/api/character','GET',undefined,a.token))[1];assert.equal(restored.x,m.data.character.x);
 await api('/api/logout','POST',{},a.token);assert.equal((await api('/api/character','GET',undefined,a.token))[0],401);
 console.log('PASS: auth, foreign lineage isolation, real WebSocket, deduped inventory/gold, forged result rejection, persisted movement, logout.');
}finally{socket?.close();if(a?.token)await api('/api/logout','POST',{},a.token);if(b?.token)await api('/api/logout','POST',{},b.token)}
