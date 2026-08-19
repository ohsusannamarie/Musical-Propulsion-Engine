import json, mimetypes, pathlib, time, urllib.parse, urllib.request

ROOT=pathlib.Path('.')
POSTERS=ROOT/'assets'/'posters'
POSTERS.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'data'/'media-manifest.json'

pages={
 'spirited':'Spirited_(film)',
 'matilda':'Matilda_the_Musical_(film)',
 'prom':'The_Prom_(film)',
 'cyrano':'Cyrano_(film)',
 'wonka':'Wonka_(film)',
 'meangirls':'Mean_Girls_(2024_film)',
 'rockofages':'Rock_of_Ages_(2012_film)',
 'purplerain':'Purple_Rain_(film)',
 'hair':'Hair_(film)',
 'tommy':'Tommy_(1975_film)',
 'blinded':'Blinded_by_the_Light_(2019_film)',
 'yesterday':'Yesterday_(2019_film)',
 'chicago':'Chicago_(2002_film)',
 'mammamia':'Mamma_Mia!_(film)',
 'soundmusic':'The_Sound_of_Music_(film)'
}

headers={'User-Agent':'MusicalPropulsionEngine/2.3 media recovery (https://github.com/ohsusannamarie/Musical-Propulsion-Engine)'}

def get(url,retries=4):
    last=None
    for attempt in range(retries):
        try:
            req=urllib.request.Request(url,headers=headers)
            with urllib.request.urlopen(req,timeout=30) as r:
                return r.read(),r.headers.get_content_type()
        except Exception as e:
            last=e
            time.sleep(2+attempt*3)
    raise last

manifest=json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {'version':1,'entries':{}}
entries=manifest.setdefault('entries',{})
recovered=[]; failed=[]

for key,page in pages.items():
    try:
        summary='https://en.wikipedia.org/api/rest_v1/page/summary/'+urllib.parse.quote(page,safe='()!,_')
        raw,_=get(summary)
        js=json.loads(raw.decode('utf-8'))
        src=(js.get('originalimage') or js.get('thumbnail') or {}).get('source')
        if not src: raise RuntimeError('no image in page summary')
        img,ctype=get(src)
        if not ctype.startswith('image/') or len(img)<3000:
            raise RuntimeError(f'bad image response: {ctype}, {len(img)} bytes')
        ext={'image/jpeg':'.jpg','image/png':'.png','image/webp':'.webp'}.get(ctype)
        if not ext:
            ext=mimetypes.guess_extension(ctype) or '.jpg'
        dest=POSTERS/(key+ext)
        dest.write_bytes(img)
        entries[key]['status']='bundled'
        entries[key]['poster']='./assets/posters/'+dest.name
        entries[key]['provenance']={'type':'wikipedia-rest-summary','page':page,'source':src}
        recovered.append(key)
        print('RECOVERED',key,'->',dest,len(img))
    except Exception as e:
        failed.append({'id':key,'error':str(e)})
        print('FAILED',key,e)
    time.sleep(1.25)

counts={'bundled':0,'remote':0,'fallback':0,'missing':0}
for e in entries.values():
    counts[e.get('status','missing')]=counts.get(e.get('status','missing'),0)+1
manifest['counts']=counts
manifest['catalogSize']=len(entries)
manifest['recoveryQueue']=[{'id':k,'title':v.get('title'),'status':'needs-source'} for k,v in entries.items() if v.get('status')=='missing']
manifest['lastRecovery']={'batch':1,'attempted':len(pages),'recovered':recovered,'failed':failed}
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

# Keep app posterSources synchronized with bundled assets from the manifest.
poster_sources={k:v['poster'] for k,v in entries.items() if v.get('status')=='bundled' and v.get('poster')}
for fn in ('index.html','app.html'):
    p=ROOT/fn
    if not p.exists(): continue
    txt=p.read_text(encoding='utf-8')
    import re
    new='const posterSources='+json.dumps(poster_sources,separators=(',',':'))+';'
    txt,n=re.subn(r'const posterSources=\{.*?\};',new,txt,count=1,flags=re.S)
    if n!=1: raise RuntimeError(f'Could not update posterSources in {fn}')
    p.write_text(txt,encoding='utf-8')

print('Recovered',len(recovered),'of',len(pages),'batch 1 titles; remaining missing',counts.get('missing',0))
