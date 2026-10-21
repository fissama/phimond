"""Feedback roundtrip uses temporary data; never alters owner reviews."""
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from PIL import Image
import p10_review_server as review
from p10_review_server import ReviewServer


def effective_fixture():
    frozen = review.read_json(review.ROOT/'data/p10/species.json')['records']
    records = dict(frozen)
    for i in range(153,161):
        records[f'species_{i:04}'] = dict(display_name={'vi': f'Thiết kế mới {i}'},
                                        race_id='dragon', star=5,
                                        species_class='special' if i>=159 else 'normal',
                                        provenance={'namespace':'phimond_authored'})
    return records


class ReviewRoundtrip(unittest.TestCase):
    def setUp(self):
        # Registry/art generation can run independently; exercise160 using its
        # agreed schema without depending on partially generated disk contents.
        actual_read = review.read_json
        records = effective_fixture()
        def read(path, default=None):
            if path == review.ROOT/'data/p10/species_effective.json':
                return {'records': records}
            if path.parent.parent == review.EXTENSION and path.name == 'result.json':
                return {}
            return actual_read(path, default)
        self.reader = patch.object(review, 'read_json', side_effect=read)
        self.reader.start()
        self.addCleanup(self.reader.stop)

    def test_catalog_save_reload_version_and_asset_guard(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'reviews.json'
            server = ReviewServer(('127.0.0.1', 0), path)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            base = f'http://127.0.0.1:{server.server_port}'
            try:
                def get(route):
                    with urlopen(base + route) as response:
                        return json.load(response)

                def post(data):
                    request = Request(base + '/api/reviews', json.dumps(data).encode(),
                                      {'Content-Type': 'application/json'})
                    with urlopen(request) as response:
                        return json.load(response)

                catalog = get('/api/species')['species']
                self.assertEqual(len(catalog), 160)
                self.assertEqual(get('/api/species')['total'],160)
                self.assertEqual(get('/healthz')['species'],160)
                self.assertEqual(len({pet['id'] for pet in catalog}), 160)
                self.assertTrue(all(len(pet['bounds']) == 20 for pet in catalog[:152]))
                self.assertTrue(all(pet['owner_done'] and pet['previously_approved'] for pet in catalog[:152]))
                authored=catalog[152:]
                self.assertEqual(len(authored),8)
                self.assertTrue(all(pet['original'] is None and pet['provenance']=='Phimond-authored' for pet in authored))
                self.assertTrue(all(pet['atlas'] is None and pet['sha256'] is None for pet in authored))
                self.assertTrue(all(not pet['previously_approved'] and not pet['owner_done'] and not pet['runtime_activated'] for pet in authored))
                with self.assertRaises(HTTPError) as missing_candidate:
                    post(dict(species_id=authored[0]['id'],sha256=None,approved=True))
                self.assertEqual(missing_candidate.exception.code,409)
                pet = catalog[0]
                record = dict(species_id=pet['id'], sha256=pet['sha256'],
                              approved=True, comment='Kiểm tra tiếng Việt: chân, mặt.',
                              animation='move')
                self.assertTrue(post(record)['saved'])
                record['approved'] = False
                record['comment'] = 'Cần sửa Cast.'
                post(record)
                persisted = get('/api/reviews')['reviews'][pet['id']][pet['sha256']]
                self.assertFalse(persisted['approved'])
                self.assertEqual(persisted['comment'], record['comment'])
                self.assertEqual(json.loads(path.read_text())['reviews'][pet['id']][pet['sha256']], persisted)
                with self.assertRaises(HTTPError) as wrong_version:
                    post(dict(record, sha256='old-atlas'))
                self.assertEqual(wrong_version.exception.code, 409)
                with self.assertRaises(HTTPError) as traversal:
                    get('/assets/../../../../.env')
                self.assertEqual(traversal.exception.code, 404)
                with urlopen(base + pet['atlas']) as response:
                    self.assertEqual(response.headers['Content-Type'], 'image/png')
                # New server instance reads feedback already stored on disk.
                restarted = ReviewServer(('127.0.0.1', 0), path)
                self.assertEqual(restarted.reviews()['reviews'][pet['id']][pet['sha256']], persisted)
                restarted.server_close()
            finally:
                server.shutdown()
                server.server_close()
                worker.join()

    def test_authored_candidate_hash_without_source_or_approval(self):
        sid='species_0153'
        rec=effective_fixture()[sid]
        with tempfile.TemporaryDirectory(dir=review.PETS/'redraws') as directory:
            atlas=Path(directory)/'packed.png'
            image=Image.new('RGBA',(1124,1405))
            for row in range(5):
                for col in range(4):
                    image.putpixel((col*281+140,row*281+210),(100,150,70,255))
            image.save(atlas)
            sha=review.hashlib.sha256(atlas.read_bytes()).hexdigest()
            result={'candidate_path':str(atlas),'candidate_sha256':sha,'human_approved':True,
                    'visual_notes':['Skill effect needs readability review','Check weapon consistency']}
            with patch.object(review,'read_json',return_value=result):
                candidate=review.authored_review_row(sid,rec)
                self.assertEqual(candidate['sha256'],sha)
                self.assertEqual(len(candidate['bounds']),20)
                self.assertIsNone(candidate['original'])
                self.assertFalse(candidate['previously_approved'])
                self.assertFalse(candidate['runtime_activated'])
                self.assertEqual(candidate['revision_note'],
                                 'Skill effect needs readability review · Check weapon consistency')
                result['visual_notes']='Pixel style needs owner review'
                self.assertEqual(review.authored_review_row(sid,rec)['revision_note'],
                                 'Pixel style needs owner review')
                result['candidate_sha256']='old-atlas'
                with self.assertRaisesRegex(ValueError,'hash mismatch'):
                    review.authored_review_row(sid,rec)

    def test_browser_contract_for_one_shots_and_explicit_game_scales(self):
        page=review.PAGE.read_text()
        self.assertIn("row<2&&$('loop').checked",page)
        for size in ('64','96','192'):
            self.assertIn(f'<option value="{size}">',page)
        self.assertIn('Phimond-authored',page)
        self.assertIn('species.length',page)


if __name__ == '__main__':
    unittest.main()
