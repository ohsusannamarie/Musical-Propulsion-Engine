import json, pathlib

ROOT=pathlib.Path('.')
TITLES=ROOT/'data/titles.json'
POSTERS=ROOT/'assets/posters'
OUT=ROOT/'data/media-manifest.json'
REPORT=ROOT/'data/MEDIA_RECOVERY.md'

titles=json.loads(TITLES.read_text(encoding='utf-8'))
valid_ext={'.jpg','.jpeg','.png','.webp','.gif','.avif'}
local={}
if POSTERS.exists():
    for f in POSTERS.iterdir():
        if f.is_file() and f.suffix.lower() in valid_ext:
            local[f.stem]=f

entries={}
counts={'bundled':0,'remote':0,'fallback':0,'missing':0}
queue=[]
for x in titles:
    tid=x['id']
    entry={'title':x['title'],'status':None,'poster':None,'provenance':None}
    f=local.get(tid)
    if f:
        entry.update(status='bundled',poster='./'+f.as_posix(),provenance={'type':'repository-asset','path':f.as_posix()})
    elif x.get('poster'):
        entry.update(status='remote',poster=x['poster'],provenance={'type':'title-record','field':'poster'})
    elif x.get('posterFallback'):
        entry.update(status='fallback',poster=x['posterFallback'],provenance={'type':'title-record','field':'posterFallback'})
    else:
        entry.update(status='missing',poster=None,provenance={'type':'none'})
        queue.append({'id':tid,'title':x['title'],'year':x.get('year'),'status':'needs-source'})
    counts[entry['status']]+=1
    entries[tid]=entry

manifest={'version':1,'catalogSize':len(titles),'counts':counts,'entries':entries,'recoveryQueue':queue}
OUT.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

pct=lambda n: round(n/len(titles)*100,1) if titles else 0
lines=[
'# Media Recovery Status','',
f'- Catalog titles: **{len(titles)}**',
f'- Bundled: **{counts["bundled"]}** ({pct(counts["bundled"])}%)',
f'- Remote: **{counts["remote"]}** ({pct(counts["remote"])}%)',
f'- Fallback: **{counts["fallback"]}** ({pct(counts["fallback"])}%)',
f'- Missing: **{counts["missing"]}** ({pct(counts["missing"])}%)','',
'## Recovery queue',''
]
lines += [f'- `{q["id"]}` — {q["title"]} ({q.get("year") or "year unknown"})' for q in queue]
lines += ['', '## Policy', '', 'Poster state is explicit and durable: `bundled`, `remote`, `fallback`, or `missing`. CI never downloads remote art as a prerequisite for deployment. Recovery happens separately, then the manifest is rebuilt.']
REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')

assert len(entries)==len(titles)
assert sum(counts.values())==len(titles)
print('media manifest',counts)
