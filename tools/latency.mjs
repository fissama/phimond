// HTTP/WS latency against the running server. Isolated disposable account; no secrets printed.
import {randomBytes} from 'node:crypto';
import assert from 'node:assert/strict';
const base=process.env.GAME_API_URL || 'http://127.0.0.1:8090';
const count=Number(process.env.LATENCY_SAMPLES || 20);
const samples={};
async function measure(name,fn){const start=performance.now();const result=await fn();(samples[name]??=[]).push(performance.now()-start);return result;}
let token,ws;
async function api(path,method='GET',data){const res=await fetch(base+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})},body:data?JSON.stringify(data):undefined});assert.equal(res.status,200,`${path}: ${res.status}`);return res.json();}
try {
 const auth=await measure('register',()=>api('/api/register','POST',{username:'lat_'+randomBytes(7).toString('hex'),password:randomBytes(20).toString('hex')}));token=auth.token;
 for(let i=0;i<5;i++)await measure('http_character',()=>api('/api/character'));
 ws=new WebSocket(base.replace('http','ws')+'/ws');await new Promise((resolve,reject)=>{ws.onopen=resolve;ws.onerror=reject});
 let seq=0;const waiting=new Map();ws.onmessage=ev=>{const m=JSON.parse(ev.data);waiting.get(m.request_id)?.(m);waiting.delete(m.request_id)};
 function send(op,data={}){const id='lat-'+(++seq);return new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('timeout '+op)),30000);waiting.set(id,m=>{clearTimeout(timer);assert.equal(m.op,'state',JSON.stringify(m));resolve(m)});ws.send(JSON.stringify({op,request_id:id,data}))})}
 await measure('ws_auth',()=>send('auth.session',{token}));
 for(let i=0;i<count;i++){await measure('ws_move',()=>send('world.move',{direction:i%2?'left':'right'}));await new Promise(r=>setTimeout(r,100));}
 await measure('ws_durable',()=>send('shop.buy',{item_id:'potion',quantity:1}));
 if(process.env.LATENCY_BATTLE==='1'){
 let m=await send('character.get');while(m.data.character.x<37)m=await send('world.move',{direction:'right'});
 await measure('ws_portal',()=>send('world.portal',{portal_id:'forest_gate'}));
 m=await measure('ws_encounter',()=>send('world.encounter'));
 for(let turn=0;turn<5&&m.data.character.battle;turn++){const battle=m.data.character.battle;m=await measure('ws_battle_action',()=>send('battle.action',{battle_id:battle.id,turn:battle.turn,choice:'defend'}));}
 }
 await measure('logout',()=>api('/api/logout','POST',{}));token=undefined;
 for(const [name,values] of Object.entries(samples)){values.sort((a,b)=>a-b);console.log(JSON.stringify({name,n:values.length,p50_ms:+values[Math.floor(values.length*.5)].toFixed(2),p95_ms:+values[Math.min(values.length-1,Math.floor(values.length*.95))].toFixed(2),max_ms:+values.at(-1).toFixed(2)}))}
} finally {ws?.close();if(token)await api('/api/logout','POST',{}).catch(()=>{});}
