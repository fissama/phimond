import test from 'node:test';
import assert from 'node:assert/strict';
import {ProtocolClient, LoadReport, readConfig} from './load_gameplay.mjs';

class Socket extends EventTarget {
 sent=[];
 send(raw){this.sent.push(JSON.parse(raw));}
 reply(data){this.dispatchEvent(new MessageEvent('message',{data:JSON.stringify(data)}));}
 close(){this.dispatchEvent(new Event('close'));}
}

test('request IDs isolated, ack correlated, malformed state never passes',async()=>{
 const a=new Socket(), b=new Socket();
 const x=new ProtocolClient(a,30), y=new ProtocolClient(b,30);
 const first=x.send('world.move',{direction:'left'}), second=y.send('world.move',{direction:'right'});
 assert.notEqual(a.sent[0].request_id,b.sent[0].request_id);
 a.reply({op:'state',request_id:a.sent[0].request_id,sequence:1,data:{character:{id:'a'}}});
 b.reply({op:'state',request_id:b.sent[0].request_id,sequence:1,data:{character:null}});
 assert.equal((await first).data.character.id,'a');
 await assert.rejects(second,/malformed/);
 assert.equal(y.pending.size,0);
});
test('timeout and disconnect reject pending and never replay mutation',async()=>{
 const a=new Socket(), x=new ProtocolClient(a,10);
 await assert.rejects(x.send('pet.activate',{pet_id:'p'}),/timeout/);
 assert.equal(x.pending.size,0);
 const waiting=x.send('shop.buy',{item_id:'potion',quantity:1});
 a.close(); await assert.rejects(waiting,/disconnected/);
 assert.equal(a.sent.length,2); assert.equal(x.pending.size,0);
});
test('server rejection is separated from timeout/internal errors',async()=>{
 const a=new Socket(), x=new ProtocolClient(a,30);
 const waiting=x.send('shop.buy',{});
 a.reply({op:'error',request_id:a.sent[0].request_id,data:{message:'insufficient gold'}});
 await assert.rejects(waiting,e=>e.code==='rejected');
});
test('empty samples, missing/stalled users and failures cannot yield a passing report',()=>{
 const r=new LoadReport(2,0);
 let result=r.summary(1000);
 assert.equal(result.passed,false); assert.equal(result.operations['world.move'],undefined);
 r.record(0,'world.move',10,1000); r.record(1,'pet.activate',50,1000);
 result=r.summary(2000); assert.equal(result.passed,true);
 assert.equal(result.operations['world.move'].p95_ms,10);
 assert.equal(r.summary(32000).passed,false);
 r.failure(0,'battle.action','timeout'); assert.equal(r.summary(2000).passed,false);
});
test('load config refuses mutation by default and validates bounds before registration',()=>{
 assert.throws(()=>readConfig({}),/LOAD_ALLOW_MUTATION/);
 assert.throws(()=>readConfig({LOAD_ALLOW_MUTATION:'1',LOAD_USERS:'0'}),/LOAD_USERS/);
 assert.throws(()=>readConfig({LOAD_ALLOW_MUTATION:'1',LOAD_PROFILE:'hot-map'}),/profile/);
 assert.equal(readConfig({LOAD_ALLOW_MUTATION:'1',LOAD_USERS:'10',LOAD_SECONDS:'120'}).users,10);
});
test('completed slow workload must not be reported as meeting performance budget',()=>{
 const r=new LoadReport(1,0);r.record(0,'battle.action',900,1000);
 const result=r.summary(2000);
 assert.equal(result.workload_completed,true);
 assert.equal(result.performance_budget_met,false);
 assert.equal(result.passed,false);
});
test('recovered stalls, including the initial gap, remain failures',()=>{
 for(const initial of [false,true]){
  const r=new LoadReport(1,0);
  if(!initial)r.record(0,'world.move',10,1000);
  r.record(0,'world.move',10,40000);
  assert.equal(r.summary(41000).workload_completed,false);
  assert.ok(r.summary(41000).users[0].max_gap_ms>=39000);
 }
});
