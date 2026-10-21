#!/usr/bin/env python3
"""Build a local, read-only review snapshot; never activates or alters sprites."""
import collections
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / '.ai/plan/phases/P10-pet-model/redraw-kit/manifest.json'
OUT = ROOT / 'apps/game-client/assets/pets/redraws/batches/20261005'


def local_url(path):
    return html.escape(Path(path).resolve().relative_to(OUT).as_posix(), quote=True)


def main():
    jobs = json.loads(MANIFEST.read_text())['jobs']
    originals = OUT / 'gallery-originals'
    originals.mkdir(exist_ok=True)
    counts, rows, cards = collections.Counter(), [], []
    drawn = 0
    for job in jobs:
        folder = ROOT / job['output_dir']
        result_file = folder / 'result.json'
        result = json.loads(result_file.read_text()) if result_file.exists() else {}
        status = result.get('status', 'not_generated')
        review_file = folder / 'independent-review.md'
        review = review_file.read_text() if review_file.exists() else ''
        candidate_hash = result.get('candidate_sha256', '')
        if candidate_hash and candidate_hash in review and any(
            marker in review.lower() for marker in ('needs repair', 'needs changes', 'changes required')
        ):
            status = 'needs_repair'
        counts[status] += 1
        raws = list(folder.glob('attempt-*/raw.png'))
        drawn += bool(raws)
        source = ROOT / job['source_portrait']
        source_bytes = source.read_bytes()
        assert hashlib.sha256(source_bytes).hexdigest() == job['source_portrait_sha256']
        source_copy = originals / (job['species_id'] + '.png')
        if not source_copy.exists():
            with source_copy.open('xb') as handle:
                handle.write(source_bytes)
        assert source_copy.read_bytes() == source_bytes
        preview = ROOT / result['preview_path'] if result.get('preview_path') else None
        thumbnail = preview.parent / 'portrait-preview.png' if preview else None
        images = '<figure><img alt="APK gốc" src="' + local_url(source_copy) + '"><figcaption>APK gốc</figcaption></figure>'
        if thumbnail and thumbnail.exists():
            images += '<figure><img alt="Bản mới" loading="lazy" src="' + local_url(thumbnail) + '"><figcaption>Bản mới</figcaption></figure>'
        else:
            images += '<figure class="pending"><span>Chờ review</span></figure>'
        links = []
        for label, path in [('Xem animation / 20 frame', preview),
                            ('Sheet đang review', ROOT / result['candidate_path'] if result.get('candidate_path') else None),
                            ('Self-review', ROOT / result['self_review_path'] if result.get('self_review_path') else None),
                            ('Review độc lập', review_file if review_file.exists() else None)]:
            if path and path.exists():
                links.append('<a href="' + local_url(path) + '">' + label + '</a>')
        blockers = result.get('blockers', [])
        row = {'species_id': job['species_id'], 'name': job['display_name_vi'],
               'source_species_id': job['source_species_id'], 'status': status,
               'drawn': bool(raws), 'candidate_sha256': candidate_hash,
               'human_approved': result.get('human_approved', False),
               'generation_calls': result.get('generation_calls', len(raws))}
        rows.append(row)
        search = html.escape(' '.join([row['species_id'], row['name'], row['source_species_id']]).lower(), quote=True)
        cards.append('<article data-status="' + html.escape(status) + '" data-search="' + search + '"><h2>' + html.escape(row['name']) + '</h2><p>' + row['species_id'] + ' · ' + html.escape(row['source_species_id']) + '</p><strong>' + status + '</strong><div class="compare">' + images + '</div><nav>' + ' · '.join(links) + '</nav><p class="issues">' + html.escape('; '.join(str(x) for x in blockers)) + '</p></article>')
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    snapshot = {'created_utc': stamp, 'drawn': drawn, 'total': len(jobs), 'counts': dict(counts), 'jobs': rows}
    (OUT / 'gallery-status.json').write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + '\n')
    summary = ' · '.join(str(n) + ' ' + status for status, n in sorted(counts.items()))
    options = ''.join('<option value="' + html.escape(s) + '">' + html.escape(s) + '</option>' for s in sorted(counts))
    page = '''<!doctype html><html lang="vi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Phimond — redraw150</title>
<style>body{font:16px system-ui;margin:24px;background:#20252c;color:#edf2f7}h1{margin-bottom:8px}header{max-width:1100px}input,select{padding:10px;margin:8px 8px 16px 0;font:inherit}#cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}article{background:#303844;border:1px solid #566273;border-radius:8px;padding:16px}h2{font-size:20px;margin:0}p{font-size:14px;overflow-wrap:anywhere}strong{font-size:14px;color:#ffd48a}.compare{display:flex;gap:12px;margin:12px 0}figure{margin:0;flex:1;text-align:center;background:#dfe6de;color:#1c2530;min-height:150px}img{width:130px;height:130px;object-fit:contain;image-rendering:pixelated}figcaption{font-size:13px;padding-bottom:6px}.pending{display:grid;place-items:center}a{color:#9ed6ff}nav{line-height:1.7;font-size:14px}.issues{color:#ffb8b8}[hidden]{display:none!important}</style>
<header><h1>Phimond — redraw150</h1><p>Chỉ dùng APK gốc để giữ nhận dạng và hai anchor Độc Đằng Nữ / Đảo Thiên Đường để giữ style. Bản mới chưa được kích hoạt trong game. ready_for_review là chờ bạn duyệt, không phải đã được chấp nhận.</p><p>SNAPSHOT_SUMMARY</p><p>SNAPSHOT_TIME</p><label>Tìm loài <input id="search" placeholder="Tên hoặc species_ID"></label><label>Trạng thái <select id="status"><option value="">Tất cả</option>STATUS_OPTIONS</select></label><p id="shown"></p></header><main id="cards">CARDS</main>
<script>const cards=[...document.querySelectorAll('article')],search=document.querySelector('#search'),status=document.querySelector('#status');function filter(){let n=0;for(const card of cards){card.hidden=!(card.dataset.search.includes(search.value.toLowerCase())&&(!status.value||card.dataset.status===status.value));n+=!card.hidden}document.querySelector('#shown').textContent=n+' / '+cards.length+' loài'}search.addEventListener('input',filter);status.addEventListener('change',filter);filter();</script></html>'''
    page = page.replace('SNAPSHOT_SUMMARY', str(drawn) + ' /150 loài đã có raw. ' + html.escape(summary)).replace('SNAPSHOT_TIME', 'Cập nhật UTC: ' + stamp).replace('STATUS_OPTIONS', options).replace('CARDS', ''.join(cards))
    (OUT / 'index.html').write_text(page)
    print(json.dumps({'status': 'gallery_exported', 'drawn': drawn, 'total': len(jobs), 'counts': dict(counts), 'index': str(OUT / 'index.html')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
