# batch-13-release

Cắt từ `../p01-release-art-20261022/sources` (GPT vẽ) bằng `tools/p01/cut_release_art.py`. Chỉ tách nền, đưa vào ô, căn chân/thân, giảm màu; không sửa hình. Mọi asset `approved=false` cho tới khi duyệt trong cảnh thật.

- `player-male/run.png`, `run-down.png`, `player-female/run.png`: dải 6 khung 192×192.
- `path-fringe-*`, `path-cap-*`: mảnh chuyển đất↔cỏ.
- `forest-*`: viền rừng theo lớp.

Nạp vào client: `python3 tools/p01/sync_client_assets.py --merge`.
