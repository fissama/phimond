// Deterministic conformance of image_gen artwork; no procedural replacement art.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire('/Users/phileanh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/');
const sharp=require('sharp');
const {PNG}=require('pngjs');
const here=path.dirname(new URL(import.meta.url).pathname), root=path.dirname(here);
const files=JSON.parse(fs.readFileSync(path.join(here,'sources.json')));
const read=p=>PNG.sync.read(fs.readFileSync(p));
const write=(p,im)=>fs.writeFileSync(p,PNG.sync.write(im));
const empty=(w,h)=>new PNG({width:w,height:h});
const pix=(a,x,y)=>(y*a.width+x)*4;
function copyPixel(a,x,y,b,u,v){a.data.set(b.data.subarray(pix(b,u,v),pix(b,u,v)+4),pix(a,x,y));}
async function resize(im,w,h){return PNG.sync.read(await sharp(PNG.sync.write(im)).resize(w,h,{fit:'fill',kernel:'nearest'}).png().toBuffer());}
function crop(im,x,y,w,h){let out=empty(w,h);for(let v=0;v<h;v++)for(let u=0;u<w;u++)copyPixel(out,u,v,im,x+u,y+v);return out;}
function binary(im,threshold=128){for(let i=0;i<im.data.length;i+=4){if(im.data[i+3]<threshold){im.data.fill(0,i,i+4);}else im.data[i+3]=255;}return im;}
function quantize(im,limit){
 const hist=new Map();let transparent=false;for(let i=0;i<im.data.length;i+=4){if(!im.data[i+3]){transparent=true;continue;}let key=im.data[i]*65536+im.data[i+1]*256+im.data[i+2];hist.set(key,(hist.get(key)||0)+1);}
 const count=limit-(transparent?1:0);if(hist.size<=count)return im;
 const entries=[...hist].map(([k,n])=>({c:[k>>16,(k>>8)&255,k&255],n,key:k}));
 const describe=a=>{const lo=[255,255,255],hi=[0,0,0];let n=0;for(const p of a){n+=p.n;for(let k=0;k<3;k++){lo[k]=Math.min(lo[k],p.c[k]);hi[k]=Math.max(hi[k],p.c[k]);}}const range=hi.map((v,k)=>v-lo[k]);return {a,n,range,score:Math.max(...range)*Math.sqrt(n)};};
 const boxes=[describe(entries)];while(boxes.length<count){let bi=-1,best=-1;for(let i=0;i<boxes.length;i++)if(boxes[i].a.length>1&&boxes[i].score>best){best=boxes[i].score;bi=i;}if(bi<0)break;const box=boxes.splice(bi,1)[0],channel=box.range.indexOf(Math.max(...box.range));box.a.sort((a,b)=>a.c[channel]-b.c[channel]);let total=0,j=0;while(j<box.a.length-1&&total<box.n/2)total+=box.a[j++].n;boxes.push(describe(box.a.slice(0,j)),describe(box.a.slice(j)));}
 const colors=boxes.map(b=>{let c=[0,0,0];for(const p of b.a)for(let k=0;k<3;k++)c[k]+=p.c[k]*p.n;return c.map(v=>Math.round(v/b.n));});
 const table=new Map();for(const p of entries){let best=Infinity,chosen;for(const c of colors){let d=0;for(let k=0;k<3;k++)d+=(c[k]-p.c[k])**2;if(d<best){best=d;chosen=c;}}table.set(p.key,chosen);}
 for(let i=0;i<im.data.length;i+=4)if(im.data[i+3])im.data.set(table.get(im.data[i]*65536+im.data[i+1]*256+im.data[i+2]),i);return im;
}
async function save(im,name,colors){const p=path.join(root,name+'.png');write(p,quantize(im,colors));return read(p);}
function palette(im){const p=new Map();for(let i=0;i<im.data.length;i+=4)if(im.data[i+3]){const c=[...im.data.subarray(i,i+3)];p.set(c.join(','),c);}return [...p.values()];}
function mapPalette(im,colors){for(let i=0;i<im.data.length;i+=4){if(!im.data[i+3])continue;let best=Infinity,c0;for(const c of colors){let d=0;for(let k=0;k<3;k++)d+=(c[k]-im.data[i+k])**2;if(d<best){best=d;c0=c;}}im.data.set(c0,i);}return im;}
// Minimum-error cut keeps a narrow reference collar, preserving A/B boundary compatibility.
function collar(dst,ref,side){const n=512,min=2,max=8,W=max-min+1;let prev=new Float64Array(W),back=new Int16Array(n*W);
 const coords=(t,s)=>side===0?[s,t]:side===1?[n-1-s,t]:side===2?[t,s]:[t,n-1-s];
 for(let t=0;t<n;t++){const cur=new Float64Array(W);for(let q=0;q<W;q++){let [x,y]=coords(t,min+q),i=pix(dst,x,y),cost=0;for(let k=0;k<3;k++)cost+=(dst.data[i+k]-ref.data[i+k])**2;let b=q,val=t?prev[q]:0;if(t)for(let j=Math.max(0,q-1);j<=Math.min(W-1,q+1);j++)if(prev[j]<val){val=prev[j];b=j;}cur[q]=cost+val+q*.2;back[t*W+q]=b;}prev=cur;}
 let q=prev.indexOf(Math.min(...prev));for(let t=n-1;t>=0;t--){for(let s=0;s<=min+q;s++){let [x,y]=coords(t,s);copyPixel(dst,x,y,ref,x,y);}q=back[t*W+q];}}
const manifest={route:'host_image',tool:'image_gen.imagegen',model:'tool default',estimateUsd:null,assets:[],processing:[],warnings:[]};
for(const [name,src] of Object.entries(files)){fs.copyFileSync(src,path.join(here,'raw',name+'.png'));}
const ref=read(path.join(root,'scene-edges/stone-floor/final.png'));
let floor=await resize(read(files['stone-floor-b']),512,512);
const refPal=palette(ref);mapPalette(floor,refPal);
for(let s=0;s<4;s++)collar(floor,ref,s);
floor=await save(floor,'stone-floor-b',48);
manifest.processing.push('Floor: nearest resize, reference palette, minimum-error cuts to retain a 2–8px compatibility collar. Interior uses generated artwork.');
manifest.warnings.push('WARN floor-zero-reuse: NOT fully satisfied/certified. Floor retains 2–8px reference boundary fragments for A/B compatibility; every brick/crack being wholly different is not guaranteed. Files: stone-floor-b.png and completion-20261029/floor-mixed-3x3.png.');
let city=read(files['city-backdrop-wide']);
// Remove generator-added bottom white margin and excess upper sky; retain central spire.
city=crop(city,0,264,city.width,500);
city=await resize(city,2432,486);
for(let i=0;i<city.data.length;i+=4){let r=city.data[i],g=city.data[i+1],b=city.data[i+2];if(r<45&&g<145&&b>180){city.data[i]=33;city.data[i+1]=112;city.data[i+2]=234;}city.data[i+3]=255;}
city=await save(city,'city-backdrop-wide',48);
manifest.processing.push('City: crop excess sky and bottom white margin, nearest resize, flatten saturated blue sky, quantize without dithering.');
let roof=read(files['city-near-roofs']);
roof=binary(crop(roof,0,459,roof.width,252),180);
// Fit each generated city strip to half the requested panorama width, retaining scale.
roof=await resize(roof,1280,220);
// Overlap the end into the beginning with a per-row minimum-error graph cut.
const period=1216,overlap=64;
let roofTile=crop(roof,0,0,period,220);
let previous=new Float64Array(overlap),back=new Int16Array(220*overlap);
for(let y=0;y<220;y++){let cur=new Float64Array(overlap);for(let x=0;x<overlap;x++){let a=pix(roof,x,y),b=pix(roof,period+x,y),cost=0;for(let k=0;k<4;k++)cost+=(roof.data[a+k]-roof.data[b+k])**2;let q=x,val=y?previous[x]:0;if(y)for(let j=Math.max(0,x-1);j<=Math.min(overlap-1,x+1);j++)if(previous[j]<val){val=previous[j];q=j;}cur[x]=cost+val;back[y*overlap+x]=q;}previous=cur;}
let cut=previous.indexOf(Math.min(...previous));for(let y=219;y>=0;y--){for(let x=0;x<=cut;x++)copyPixel(roofTile,x,y,roof,period+x,y);cut=back[y*overlap+cut];}
// The opaque architectural baseline stays flat; remove residual alpha fringe at base.
for(let x=0;x<period;x++){let srcY=219;while(srcY>180&&!roofTile.data[pix(roofTile,x,srcY)+3])srcY--;for(let y=srcY+1;y<220;y++)copyPixel(roofTile,x,y,roofTile,x,srcY);}
roof=empty(2432,220);for(let y=0;y<220;y++)for(let x=0;x<2432;x++)copyPixel(roof,x,y,roofTile,x%period,y);
roof=await save(binary(roof),'city-near-roofs',48);
manifest.processing.push('Roofs: crop transparent padding, threshold alpha, nearest sizing, 64px minimum-error overlap to form a 1216px period repeated twice, opaque flat baseline, 48-color export.');
for(let v=1;v<=3;v++){const name='floor-light-'+v;if(!files[name])continue;let im=await resize(read(files[name]),256,256);
 // Convert the generator alpha falloff to binary ordered coverage (4x4 Bayer).
 const bayer=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]];
 for(let y=0;y<256;y++)for(let x=0;x<256;x++){let i=pix(im,x,y),a=im.data[i+3];if(a>(bayer[y%4][x%4]+.5)*16){im.data[i+3]=255;}else im.data.fill(0,i,i+4);}
 // Match the requested dominant color family, retaining each generated pane pattern.
 for(let i=0;i<im.data.length;i+=4){if(!im.data[i+3])continue;let r=im.data[i],g=im.data[i+1],b=im.data[i+2];if(v===1&&b>r*1.1){im.data[i]=255;im.data[i+1]=Math.min(255,190+Math.round(g*.22));im.data[i+2]=Math.min(235,130+Math.round(b*.35));}else if(v===1&&r>g*1.25&&b>g*1.05){im.data[i]=255;im.data[i+1]=Math.min(250,150+Math.round(g*.45));im.data[i+2]=Math.min(215,80+Math.round(b*.45));}else if(v===3&&r>b*1.2){im.data[i]=Math.min(220,Math.round(r*.68));im.data[i+1]=Math.max(170,g);im.data[i+2]=255;}}
 if(v===2)for(let i=0;i<im.data.length;i+=4){if(!im.data[i+3])continue;let r=im.data[i],g=im.data[i+1],b=im.data[i+2];if(b>r*1.08){im.data[i]=255;im.data[i+1]=Math.min(220,65+Math.round(g*.60));im.data[i+2]=Math.min(245,100+Math.round(b*.55));}else if(r>b*1.2&&g>b*1.15){im.data[i]=255;im.data[i+1]=Math.min(230,100+Math.round(g*.45));im.data[i+2]=Math.min(230,115+Math.round(b*.5));}}
 im=await save(im,name,32);
 manifest.processing.push(name+': nearest resize, ordered binary alpha coverage, max 32 colors without color dithering.');}
function audit(name,expected,limit,opaque){const im=read(path.join(root,name+'.png'));let colors=new Set(),alphas=new Set(),magenta=0;for(let i=0;i<im.data.length;i+=4){alphas.add(im.data[i+3]);if(im.data[i+3]){colors.add([...im.data.subarray(i,i+3)].join(','));if(im.data[i]>225&&im.data[i+1]<40&&im.data[i+2]>225)magenta++;}}const sizeOk=im.width===expected[0]&&im.height===expected[1],alphaOk=[...alphas].every(a=>a===255||(!opaque&&a===0));return {name,size:[im.width,im.height],colors:colors.size,alpha:[...alphas].sort((a,b)=>a-b),magentaPixels:magenta,pass:sizeOk&&colors.size<=limit&&alphaOk&&magenta===0};}
const specs=[['stone-floor-b',[512,512],48,true],['city-backdrop-wide',[2432,486],48,true],['city-near-roofs',[2432,220],48,false],...[1,2,3].filter(v=>files['floor-light-'+v]).map(v=>['floor-light-'+v,[256,256],32,false])];
manifest.assets=specs.map(s=>audit(...s));
function repeat(im,nx,ny){let out=empty(im.width*nx,im.height*ny);for(let y=0;y<out.height;y++)for(let x=0;x<out.width;x++)copyPixel(out,x,y,im,x%im.width,y%im.height);return out;}
write(path.join(here,'floor-repeat-3x3.png'),repeat(floor,3,3));
let mixed=empty(1536,1536);for(let y=0;y<1536;y++)for(let x=0;x<1536;x++)copyPixel(mixed,x,y,((x/512|0)+(y/512|0))%2?floor:ref,x%512,y%512);
write(path.join(here,'floor-mixed-3x3.png'),mixed);
write(path.join(here,'roofs-repeat-2x.png'),repeat(roof,2,1));
fs.writeFileSync(path.join(here,'qa.json'),JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify(manifest.assets));
