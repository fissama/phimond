#!/usr/bin/env python3
"""Cắt godot/index.wasm thành các mảnh <=10MB (Artifact giới hạn 16MB/file); index.html nạp lại qua wasm-parts.json."""
import json,sys,os
d=sys.argv[1] if len(sys.argv)>1 else 'godot'
b=open(os.path.join(d,'index.wasm'),'rb').read(); n=10*1024*1024; parts=[]
for i in range(0,len(b),n):
    name=f'wasm-part-{i//n}.wasm'; open(os.path.join(d,name),'wb').write(b[i:i+n]); parts.append(name)
json.dump({'parts':parts,'size':len(b)},open(os.path.join(d,'wasm-parts.json'),'w')); print(parts)

import shutil
if os.path.exists(os.path.join(d,'index.pck')): shutil.copy(os.path.join(d,'index.pck'),os.path.join(d,'index-pck.wasm'))
