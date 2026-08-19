import json, mimetypes, pathlib, re, time, urllib.parse, urllib.request

ROOT=pathlib.Path('.')
POSTERS=ROOT/'assets'/'posters'
POSTERS.mkdir(parents=True,exist_ok=True)
MANIFEST=ROOT/'data'/'media-manifest.json'

pages={
 'newsies':'Newsies_(musical)',
 'comefromaway':'Come_from_Away_(film)',
 'shrek':'Shrek_the_Musical',
 'grease':'Grease_(film)',
 'burlesque':'Burlesque_(2010_American_film)',
 'pitchperfect':'Pitch_Perfect',
 'coco':'Coco_(2017_film)',
 'princessfrog':'The_Princess_and_the_Frog',
 'tangled':'Tangled',
 'frozen':'Frozen_(2013_film)',
 'waitress':'Waitress:_The_Musical',
 'legallyblonde':'Legally_Blonde_(musical)',
 'falsettos':'Falsettos',
 'marypoppins':'Mary_Poppins_Returns',
 'starsborn':'A_Star_Is_Born_(2018_film)'
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

manifest=json.loads(MANIFEST.read_text())
entries=manifest['entries']
before_missing=sum(1 for e in entries.values() if e.get('status')=='missing')
recovered=[]; failed=[]; skipped=[]

for key,page in pages.items():
    if entries.get(key,{}).get('status')=='bundled':
        skipped.append(key)
        continue
    try:
        summary='https://en.wikipedia.org/api/rest_v1/page/summary/'+urllib.parse.quote(page,safe='()!,:,_')
        raw,_=get(summary)
        js=json.loads(raw.decode('utf-8'))
        src=(js.get('originalimage') or js.get('thumbnail') or {}).get('source')
        if not src:
            raise RuntimeError('no image in page summary')
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
        failed.append({'id':key,'page':page,'error':str(e)})
        print('FAILED',key,e)
    time.sleep(1.25)

counts={'bundled':0,'remote':0,'fallback':0,'missing':0}
for e in entries.values():
    status=e.get('status','missing')
    counts[status]=counts.get(status,0)+1
manifest['counts']=counts
manifest['catalogSize']=len(entries)
manifest['recoveryQueue']=[{'id':k,'title':v.get('title'),'status':'needs-source'} for k,v in entries.items() if v.get('status')=='missing']
manifest['lastRecovery']={'batch':2,'attempted':len(pages)-len(skipped),'recovered':recovered,'failed':failed,'skipped':skipped,'beforeMissing':before_missing,'afterMissing':counts['missing']}
MANIFEST.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')

poster_sources={k:v['poster'] for k,v in entries.items() if v.get('status')=='bundled' and v.get('poster')}
for fn in ('index.html','app.html'):
    p=ROOT/fn
    if not p.exists():
        continue
    txt=p.read_text(encoding='utf-8')
    new='const posterSources='+json.dumps(poster_sources,separators=(',',':'))+';'
    txt,n=re.subn(r'const posterSources=\{.*?\};',new,txt,count=1,flags=re.S)
    if n!=1:
        raise RuntimeError(f'Could not update posterSources in {fn}')
    p.write_text(txt,encoding='utf-8')

print('Recovered',len(recovered),'of',len(pages)-len(skipped),'attempted batch 2 titles; remaining missing',counts['missing'])
