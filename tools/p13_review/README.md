# P13 local acceptance tool

```sh
rtk proxy python3 tools/p13_review/server.py --port 8133
rtk proxy python3 -m unittest discover -s tools/p13_review -p 'test_*.py'
```

Python stdlib; no installation/build. Loopback only. Defaults: candidate
`.ai/plan/phases/P13-skills/review-package.json`, responses
`.ai/plan/phases/P13-skills/review/responses/<sha256>.json`.

GET `/api/review` returns package, its exact byte hash and feedback. POST
`/api/feedback` takes package_hash, version, all decisions `{status,comment}`,
notes and verdict. Optimistic version checks and atomic file replace protect
stale tabs. Non-draft edits first save draft; prior submitted verdict retained
in history. Approval requires all decision cards approved. Hash changes preserve
old file and start a new review; never silently transfer human approval.

GET `/api/document?name=...` serves only explicitly whitelisted P13 Markdown.
No arbitrary filesystem/DB/game API access. Host/Origin/body/IDs/status validated;
HTML content escaped; same-origin CSP. Tests use temporary fixture/storage only.
Client exports JSON with package hash and an explicit unsaved_changes marker.

Authoring: `rtk proxy python3 tools/content/p13_design.py`. Source audit uses
existing UnityPy env: `rtk proxy tools/.cache/asset-venv/bin/python tools/content/p13_source_audit.py`.
