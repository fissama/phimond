// Godot can exit zero after a script parse/assertion error. Check diagnostics,
// a positive completion marker and a timeout, not just process status.
import {spawnSync} from 'node:child_process';
import {resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(fileURLToPath(new URL('..',import.meta.url)));
const godot=process.env.GODOT_BIN || resolve(root,'apps/game-client/.tools/Godot.app/Contents/MacOS/Godot');
for(const script of ['client_protocol_check','world_room_check','contact_check','reference_menus_check','battle_presentation_check']){
 const r=spawnSync(godot,['--headless','--path',resolve(root,'apps/game-client'),'--script',`res://scripts/${script}.gd`],{encoding:'utf8',timeout:60000});
 const output=(r.stdout||'')+(r.stderr||'');
 const marker = script === 'reference_menus_check' ? 'REFERENCE_MENUS_CHECK:' : 'PASS:';
 if(r.error || r.status!==0 || /(?:SCRIPT ERROR|^ERROR:)/m.test(output) || !output.includes(marker)){
  process.stderr.write(output); console.error(`FAIL ${script}: ${r.error?.message || r.status}`); process.exit(1);
 }
 console.log(`${script}: ${output.split('\n').find(line=>line.startsWith(marker))}`);
}
