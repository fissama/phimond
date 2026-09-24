// Opt-in, public-protocol load. No seed changes, admin APIs, automatic retries
// or secrets in reports. Independent-account capacity is not shared-world CCU.
import {randomBytes, randomUUID} from 'node:crypto';
import {readFile, writeFile} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
import {cpus, platform, arch} from 'node:os';

const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
const fault=(code,message=code)=>Object.assign(new Error(message),{code});

export function assessBudget(operations){
 return Object.keys(operations).length>0&&Object.values(operations).every(s=>s.n>0&&s.p95_ms<=250&&s.p99_ms<=400);
}

export class ProtocolClient {
 constructor(socket, timeout=15000){
  this.socket=socket; this.timeout=timeout; this.pending=new Map(); this.prefix=randomUUID(); this.counter=0;
  socket.addEventListener('message',ev=>{
   let m; try {m=JSON.parse(ev.data);} catch {return;}
   const p=this.pending.get(m.request_id); if(!p)return;
   clearTimeout(p.timer); this.pending.delete(m.request_id);
   if(m.op==='error') {p.reject(fault('rejected')); return;}
   if(m.op!=='state'||!Number.isInteger(m.sequence)||m.sequence<0||!m.data?.character||Array.isArray(m.data.character)||typeof m.data.character!=='object'){
    p.reject(fault('malformed')); return;
   }
   p.resolve(m);
  });
  const abort=()=>{for(const p of this.pending.values()){clearTimeout(p.timer);p.reject(fault('disconnected'));}this.pending.clear();};
  socket.addEventListener('close',abort); socket.addEventListener('error',abort);
 }
 send(op,data={}){
  const request_id=`${this.prefix}-${++this.counter}`;
  return new Promise((resolve,reject)=>{
   const timer=setTimeout(()=>{this.pending.delete(request_id);reject(fault('timeout'));},this.timeout);
   this.pending.set(request_id,{resolve,reject,timer});
   try {this.socket.send(JSON.stringify({op,request_id,data}));}
   catch {clearTimeout(timer);this.pending.delete(request_id);reject(fault('disconnected'));}
  });
 }
}

export class LoadReport {
 constructor(users,started=performance.now()){
  this.users=Array.from({length:users},()=>({actions:0,last:null,errors:0,max_gap_ms:0}));
  this.started=started; this.operations={}; this.failures=[];
 }
 record(user,op,ms,now=performance.now()){
  const u=this.users[user];u.max_gap_ms=Math.max(u.max_gap_ms,now-(u.last??this.started));u.actions++;u.last=now;
  const stat=this.operations[op]??={count:0,total_ms:0,max_ms:0,buckets:new Uint32Array(10002)};
  stat.count++;stat.total_ms+=ms;stat.max_ms=Math.max(stat.max_ms,ms);
  stat.buckets[Math.min(10001,Math.ceil(ms))]++;
 }
 failure(user,op,code){
  this.users[user].errors++;
  if(this.failures.length<100)this.failures.push({user,op,code});
 }
 summary(now=performance.now()){
  const percentile=(s,p)=>{let n=0;for(let i=0;i<s.buckets.length;i++){n+=s.buckets[i];if(n>=Math.ceil(s.count*p))return i===10001?s.max_ms:i;}return null;};
  const operations={};
  for(const [op,s] of Object.entries(this.operations))operations[op]={n:s.count,p50_ms:percentile(s,.5),p95_ms:percentile(s,.95),p99_ms:percentile(s,.99),max_ms:s.max_ms};
  const elapsed=Math.max(1,now-this.started),actions=this.users.reduce((sum,u)=>sum+u.actions,0);
  const workload_completed=this.users.every(u=>u.actions>0&&u.errors===0&&u.last!==null&&Math.max(u.max_gap_ms,now-u.last)<=30000);
  const performance_budget_met=assessBudget(operations);
  return {passed:workload_completed&&performance_budget_met,workload_completed,performance_budget_met,
   configured_users:this.users.length,active_users:this.users.filter(u=>u.actions>0&&u.last!==null&&now-u.last<=30000).length,
   elapsed_ms:elapsed,actions,actions_per_second:actions/(elapsed/1000),users:this.users,operations,failures:this.failures,
   measurement:'client send to authoritative acknowledgement; includes network and persistence',
   capacity_certified:false,limitations:['No shared-world presence/fan-out yet','No renderer/FPS measurement in protocol bots','Provisioning and travel warmup excluded']};
 }
}

export function readConfig(env=process.env){
 if(env.LOAD_ALLOW_MUTATION!=='1')throw Error('Set LOAD_ALLOW_MUTATION=1 on the dedicated test instance');
 const integer=(key,def,min,max)=>{const n=Number(env[key]??def);if(!Number.isInteger(n)||n<min||n>max)throw Error(`Invalid ${key}`);return n;};
 const profile=env.LOAD_PROFILE||'mixed';if(!['mixed','world','battle','pet'].includes(profile))throw Error('Unsupported profile; hot-map requires P06 presence');
 const base=new URL(env.GAME_API_URL||'http://127.0.0.1:8091');
 if(!['http:','https:'].includes(base.protocol)||base.username||base.password||base.search||base.hash)throw Error('Invalid GAME_API_URL');
 const run=env.LOAD_RUN_ID||`p00-${Date.now()}`;if(!/^[a-zA-Z0-9_-]{1,40}$/.test(run))throw Error('Invalid LOAD_RUN_ID');
 return {base:base.href.replace(/\/$/,''),users:integer('LOAD_USERS',1,1,75),seconds:integer('LOAD_SECONDS',120,1,7200),cadence:integer('LOAD_CADENCE_MS',500,200,5000),profile,run,
  reconnect:env.LOAD_RECONNECT==='1', output:env.LOAD_OUTPUT||`/tmp/${run}.json`};
}

async function api(base,path,body,token){
 const r=await fetch(base+path,{method:'POST',signal:AbortSignal.timeout(20000),headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},body:JSON.stringify(body)});
 if(!r.ok)throw fault(`http_${r.status}`);return r.json();
}
async function connect(base,token){
 const socket=new WebSocket(base.replace(/^http/,'ws')+'/ws');
 await new Promise((resolve,reject)=>{
  const timer=setTimeout(()=>{socket.close();reject(fault('connect_timeout'));},15000);
  socket.addEventListener('open',()=>{clearTimeout(timer);resolve();},{once:true});
  socket.addEventListener('error',()=>{clearTimeout(timer);reject(fault('connect_error'));},{once:true});
 });
 const protocol=new ProtocolClient(socket);
 try {const response=await protocol.send('auth.session',{token});return {socket,protocol,state:response.data.character};}
 catch(e){socket.close();throw e;}
}
function chooseProfile(cfg,index){
 if(cfg.profile!=='mixed')return cfg.profile;
 const ratio=index/cfg.users;return ratio<.4?'world':ratio<.8?'battle':'pet';
}
async function prepare(bot,cfg){
 if(bot.profile!=='battle')return;
 const send=async(op,data)=>{bot.state=(await bot.protocol.send(op,data)).data.character;await sleep(cfg.cadence);};
 while(bot.state.x<37)await send('world.move',{direction:'right'});
 await send('world.portal',{portal_id:'forest_gate'});
 while(bot.state.x<6)await send('world.move',{direction:'right'});
}
function nextAction(bot){
 const s=bot.state,pet=s.pets.find(p=>p.id===s.active_pet_id);
 if(bot.profile==='world')return ['world.move',{direction:s.x<=6?'right':'left'}];
 if(bot.profile==='pet'){
  if(!s.quests?.first_steps)return ['quest.accept',{quest_id:'first_steps'}];
  if(bot.actions%20===0&&s.gold>=10)return ['shop.buy',{item_id:'potion',quantity:1}];
  return ['pet.activate',{pet_id:s.active_pet_id}];
 }
 if(s.battle){
  const unit=s.battle.units.find(u=>u.side==='player');
  const usePotion=unit.hp<unit.max_hp*.4&&(s.inventory.potion||0)>0;
  return ['battle.action',{battle_id:s.battle.id,turn:s.battle.turn,choice:usePotion?'item':'attack',...(usePotion?{item_id:'potion'}:{})}];
 }
 if(pet.hp<pet.max_hp*.65)return ['pet.heal',{}];
 return ['world.encounter',{}];
}

export async function runLoad(cfg){
 const bots=[],manifest=[],report=new LoadReport(cfg.users);
 let summary;
 try {
  for(let i=0;i<cfg.users;i++){
   const username=`p00_${randomBytes(7).toString('hex')}`;
   const auth=await api(cfg.base,'/api/register',{username,password:randomBytes(24).toString('hex')});
   const bot={...await connect(cfg.base,auth.token),token:auth.token,profile:chooseProfile(cfg,i),actions:0};
   bots.push(bot);manifest.push({id:bot.state.id,username,profile:bot.profile});
   // Recoverable manifest contains IDs only, never credentials.
   await writeFile(cfg.output+'.accounts.json',JSON.stringify({run:cfg.run,accounts:manifest},null,2),{mode:0o600});
   if(i+1<cfg.users)await sleep(3200); // respect 20 registrations/minute/IP
  }
  await Promise.all(bots.map(bot=>prepare(bot,cfg)));
  report.started=performance.now();const deadline=report.started+cfg.seconds*1000;
  await Promise.all(bots.map(async(bot,i)=>{
   let reconnected=false;
   while(performance.now()<deadline){
    let op='reconnect';
    try {
     if(cfg.reconnect&&!reconnected&&i<Math.ceil(cfg.users*.2)&&performance.now()>report.started+cfg.seconds*500){
      bot.socket.close();Object.assign(bot,await connect(cfg.base,bot.token));reconnected=true;
     }
     const data=nextAction(bot);op=data[0];const started=performance.now();
     bot.state=(await bot.protocol.send(op,data[1])).data.character;bot.actions++;
     report.record(i,op,performance.now()-started);
    } catch(e){report.failure(i,op,e.code||'worker_error');return;}
    await sleep(cfg.cadence);
   }
  }));
  summary=report.summary();
 } catch(e){
  report.failure(Math.min(bots.length,cfg.users-1),'provision_or_prepare',e.code||'setup_error');
  summary=report.summary();
 } finally {
  await Promise.allSettled(bots.map(async b=>{b.socket.close();await api(cfg.base,'/api/logout',{},b.token);}));
 }
 const result={...summary,run:cfg.run,config:{users:cfg.users,seconds:cfg.seconds,cadence_ms:cfg.cadence,profile:cfg.profile,reconnect:cfg.reconnect},generator:{node:process.version,platform:platform(),arch:arch(),cpus:cpus().length},accounts:manifest};
 await writeFile(cfg.output,JSON.stringify(result,null,2),{mode:0o600});
 return result;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 try {
  if(process.argv[2]==='--assess'){
   const path=process.argv[3];if(!path)throw Error('Expected existing report path');
   const original=JSON.parse(await readFile(path,'utf8'));
   const assessment={source:path,performance_budget_met:assessBudget(original.operations),ack_budget_ms:{p95:250,p99:400},capacity_certified:false,
    note:'Assessment of recorded samples only; original workload report preserved, not a new run',operations:original.operations};
   await writeFile(path+'.assessment.json',JSON.stringify(assessment,null,2),{mode:0o600});
   console.log(JSON.stringify(assessment));if(!assessment.performance_budget_met)process.exitCode=1;
  }else{
   const cfg=readConfig();const result=await runLoad(cfg);console.log(JSON.stringify({report:cfg.output,passed:result.passed,workload_completed:result.workload_completed,performance_budget_met:result.performance_budget_met,active:result.active_users,operations:result.operations}));if(!result.passed)process.exitCode=1;
  }
 }
 catch(e){console.error(e.code||e.message);process.exitCode=1;}
}
