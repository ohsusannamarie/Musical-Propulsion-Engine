import json, pathlib, urllib.parse, urllib.request

ROOT=pathlib.Path('.')
manifest_path=ROOT/'data/media-manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
before=manifest['counts']['missing']
TARGETS={
'repo':'Repo!_The_Genetic_Opera','velvetgoldmine':'Velvet_Goldmine','priscilla':'The_Adventures_of_Priscilla,_Queen_of_the_Desert','annaapocalypse':'Anna_and_the_Apocalypse','dancerinthedark':'Dancer_in_the_Dark','hedwigstage':'Hedwig_and_the_Angry_Inch_(musical)','batboy':'Bat_Boy:_The_Musical','reefer':'Reefer_Madness_(2005_film)','singininrain':'Singin%27_in_the_Rain','cabaret':'Cabaret_(1972_film)','rockyhorrorlive':'The_Rocky_Horror_Picture_Show:_Let%27s_Do_the_Time_Warp_Again','billyelliot':'Billy_Elliot_the_Musical_Live','tickstage':'Tick,_Tick..._Boom!_(musical)','onceisland':'Once_on_This_Island','shocktreatment':'Shock_Treatment_(1981_film)'}
out=ROOT/'assets/posters'; out.mkdir(parents=True,exist_ok=True)
headers={'User-Agent':'MusicalPropulsionEngine/3.0 (github.com/ohsusannamarie/Musical-Propulsion-Engine)'}
recovered=[]; failed=[]
def fetch_json(url):
 req=urllib.request.Request(url,headers=headers)
 with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read().decode())
def fetch_bytes(url):
 req=urllib.request.Request(url,headers=headers)
 with urllib.request.urlopen(req,timeout=30) as r:return r.read(),r.headers.get_content_type()
for id,slug in TARGETS.items():
 if manifest['entries'].get(id,{}).get('status')=='bundled':continue
 try:
  summary=fetch_json('https://en.wikipedia.org/api/rest_v1/page/summary/'+slug)
  src=((summary.get('originalimage') or summary.get('thumbnail') or {}).get('source'))
  if not src:raise RuntimeError('no summary image')
  body,ctype=fetch_bytes(src)
  if not ctype.startswith('image/') or len(body)<3000:raise RuntimeError(f'bad image {ctype} {len(body)}')
  ext={ 'image/png':'.png','image/webp':'.webp','image/gif':'.gif'}.get(ctype,'.jpg')
  dest=out/(id+ext); dest.write_bytes(body); recovered.append(id)
 except Exception as e: failed.append([id,str(e)])
print('recovered',recovered); print('failed',failed)
# Regenerate manifest from repository assets, preserving deterministic status semantics.
titles=json.loads((ROOT/'data/titles.json').read_text(encoding='utf-8'))
exts=['.jpg','.jpeg','.png','.webp','.gif']
entries={}; queue=[]; bundled=0
for x in titles:
 found=None
 for ext in exts:
  q=out/(x['id']+ext)
  if q.exists():found='./assets/posters/'+q.name;break
 if found:
  bundled+=1; entries[x['id']]={'title':x['title'],'status':'bundled','poster':found,'provenance':{'type':'repository-asset','path':found[2:]}}
 else:
  entries[x['id']]={'title':x['title'],'status':'missing','poster':None,'provenance':{'type':'none'}}; queue.append({'id':x['id'],'title':x['title'],'year':x.get('year'),'status':'needs-source'})
new={'version':1,'catalogSize':len(titles),'counts':{'bundled':bundled,'remote':0,'fallback':0,'missing':len(queue)},'entries':entries,'recoveryQueue':queue}
manifest_path.write_text(json.dumps(new,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
# Update local poster map in both app surfaces if present.
for fname in ['index.html','app.html']:
 p=ROOT/fname
 if not p.exists():continue
 text=p.read_text(encoding='utf-8')
 import re
 local={k:v['poster'] for k,v in entries.items() if v['status']=='bundled'}
 replacement='const posterSources='+json.dumps(local,separators=(',',':'),ensure_ascii=False)+';'
 text,n=re.subn(r'const posterSources=\{.*?\};',replacement,text,count=1,flags=re.S)
 if n:p.write_text(text,encoding='utf-8')
print(f'missing {before} -> {len(queue)}; bundled {bundled}/{len(titles)}')
