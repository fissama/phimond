from pathlib import Path
import json, html, shutil
from PIL import Image

ROOT = Path(__file__).resolve().parent
items = [('species_0151', 'Đại Vương Bọ Cạp', 6),
         ('species_0143', 'Thần Đèn', 11)]
content = '''<!doctype html><meta charset="utf-8"><title>Phimond — JAR reference redraw</title>
<style>body{font:16px system-ui;background:#17202e;color:#e9eef7;margin:32px}a{color:#8dccff}img{max-width:100%;image-rendering:pixelated}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(360px,1fr));gap:24px}.card{padding:24px;background:#253247;border-radius:16px}.poses{background:#e2e6ed}iframe{border:0;width:100%;height:850px}small{overflow-wrap:anywhere;color:#aebed1}</style>
<h1>Hai atlas sửa theo mẫu Java</h1><p>Bản mới để duyệt hình ảnh và animation. Chưa đổi atlas được chọn hay runtime.</p>
<p>Bọ Cạp: daddy body tím, mặt nam tính đẹp trai, tóc vuốt gọn; Java dùng cho càng và thân dưới.
Thần Đèn: djinn và mũi đèn đều hướng trái, quai bên phải; khi đi chỉ có chiếc đèn nhảy.</p><div class="cards">'''
for species, name, attempt in items:
    folder = ROOT / species / f'attempt-{attempt:02d}'
    atlas = folder / 'packed.png'
    with Image.open(atlas) as image:
        sheet = Image.new('RGB', (720, 900), '#e2e6ed')
        frames = []
        for i in range(20):
            frame = image.crop((i%4*281, i//4*281, i%4*281+281, i//4*281+281))
            frames.append(frame)
            preview = frame.resize((180, 180), Image.Resampling.NEAREST)
            sheet.paste(preview, (i%4*180, i//4*180), preview)
        sheet.save(folder / 'contact-light.png')
        for row in range(5):
            gif = []
            for frame in frames[row*4:row*4+4]:
                canvas = Image.new('RGBA', (281, 281), '#e2e6ed')
                canvas.alpha_composite(frame); gif.append(canvas.convert('RGB'))
            options = {'loop':0} if row<2 else {}
            gif[0].save(folder/f'row-{row+1}.gif', save_all=True,
                        append_images=gif[1:], duration=180, disposal=2, **options)
    rel = str(folder.relative_to(ROOT))
    result = json.loads((ROOT/species/'result.json').read_text())
    content += f'<div class="card"><h2>{html.escape(name)}</h2><p><a href="{rel}/packed.png">Atlas PNG</a> · <a href="{rel}/preview/preview.html">Xem đủ 5 animation</a></p><small>SHA256 {result["candidate_sha256"]}</small><p><img class="poses" src="{rel}/preview/portrait-preview.png"></p><h3>Di chuyển</h3><img src="{rel}/row-2.gif"><details><summary>20 frame trên nền sáng</summary><img src="{rel}/contact-light.png"></details></div>'
content += '</div><h2>Animation viewer</h2>'
for species, name, attempt in items:
    content += f'<h3>{html.escape(name)}</h3><iframe src="{species}/attempt-{attempt:02d}/preview/preview.html"></iframe>'
(ROOT/'review.html').write_text(content, encoding='utf-8')
print(ROOT/'review.html')
