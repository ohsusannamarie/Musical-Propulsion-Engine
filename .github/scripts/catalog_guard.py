import json, subprocess, sys
from pathlib import Path
p=Path('data/titles.json')
cur=json.loads(p.read_text())
cur_count=len(cur)
prev_count=None
try:
    prev=subprocess.check_output(['git','show','HEAD:data/titles.json'],text=True)
    prev_count=len(json.loads(prev))
except Exception:
    pass
if prev_count is not None and cur_count < prev_count:
    raise SystemExit(f'REFUSING CATALOG REGRESSION: {prev_count} -> {cur_count}')
ids=[x.get('id') for x in cur]
if len(ids)!=len(set(ids)):
    raise SystemExit('REFUSING CATALOG WRITE: duplicate ids detected')
print(f'Catalog guard passed: {prev_count if prev_count is not None else "n/a"} -> {cur_count}')
