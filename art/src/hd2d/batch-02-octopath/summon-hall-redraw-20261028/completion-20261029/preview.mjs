import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('/Users/phileanh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/');
const sharp=require('sharp');
const here=path.dirname(new URL(import.meta.url).pathname),root=path.dirname(here);
const placements=[];
const label=(s,x,y)=>placements.push({input:Buffer.from(`<svg width="${Math.max(240,s.length*13)}" height="34"><text x="0" y="24" font-family="monospace" font-size="20" fill="#eee">${s}</text></svg>`),left:x,top:y});
async function put(file,x,y,w,h){placements.push({input:await sharp(path.join(root,file)).resize(w,h,{fit:'fill',kernel:'nearest'}).png().toBuffer(),left:x,top:y});}
label('CITY BACKDROP / 2432 x 486 / 48 colors',18,8);await put('city-backdrop-wide.png',18,46,1216,243);
label('NEAR ROOFS / 2432 x 220 / binary alpha',18,302);await put('city-near-roofs.png',18,340,1216,110);
label('FLOOR B',18,468);await put('stone-floor-b.png',18,506,384,384);
label('WARM LIGHT',430,468);await put('floor-light-1.png',430,548,256,256);
label('RED LIGHT',708,468);await put('floor-light-2.png',708,548,256,256);
label('BLUE LIGHT',986,468);await put('floor-light-3.png',986,548,256,256);
await sharp({create:{width:1252,height:910,channels:4,background:'#303238'}}).composite(placements).png().toFile(path.join(here,'contact-sheet.png'));
const html=`<!doctype html><meta charset="utf-8"><title>Summon hall asset review</title><style>body{background:#24262b;color:#eee;font:16px system-ui;margin:24px}img{image-rendering:pixelated;max-width:100%}a{color:#9dd7ff}section{margin:30px 0}.alpha{background:repeating-conic-gradient(#42464d 0 25%,#31343a 0 50%) 0/20px 20px}p{max-width:1000px}</style><h1>Summon hall — six assets</h1><p>Technical checks pass: exact dimensions, color limits, binary alpha, no magenta. Floor retains a 2–8px reference collar for A/B compatibility; the absolute no-reused-shape condition is not certified. Roof strip has a 1216px internal period. Inspect the repeat previews below before accepting visual joins.</p><section><img src="contact-sheet.png"></section><section><h2>Floor B, repeated 3×3</h2><img src="floor-repeat-3x3.png"></section><section><h2>Original A and new B, mixed 3×3</h2><img src="floor-mixed-3x3.png"></section><section><h2>Near roofs repeated twice</h2><div class="alpha" style="overflow:auto"><img style="max-width:none" src="roofs-repeat-2x.png"></div></section><p><a href="qa.json">QA</a> · <a href="verification.json">Verification</a> · <a href="prompts.json">Prompts</a></p>`;
fs.writeFileSync(path.join(here,'review.html'),html);
