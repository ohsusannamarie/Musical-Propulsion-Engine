import json, math
from pathlib import Path
P=Path('.')
titles=json.loads((P/'data/titles.json').read_text())
by={x['id']:x for x in titles}
keys=['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks','afterglow','replay']

def classify(a,b):
 d={k:round(b['scores'][k]-a['scores'][k],3) for k in keys}
 dist=round(math.sqrt(sum((a['scores'][k]-b['scores'][k])**2 for k in keys)/len(keys)),3)
 na=set(a.get('dnaNormalized',a.get('dna',[]))); nb=set(b.get('dnaNormalized',b.get('dna',[])))
 raw=set(a.get('dna',[]))&set(b.get('dna',[])); norm=sorted(na&nb)
 cand=[]
 if dist<=.60:cand.append(('safe-next-step',4,'close score profile'))
 if d['comfort']>=.65 and d['emotion']<=.45:cand.append(('lower-friction',3,'higher comfort'))
 if d['maximalism']>=.65 or (d['propulsion']>=.55 and d['movement']>=.45):cand.append(('higher-intensity',3,'more propulsion or maximalism'))
 if d['emotion']>=.65:cand.append(('more-emotional',3,'higher emotional intensity'))
 if norm and dist<=.95:cand.append(('adjacent-style',3,'shared musical DNA'))
 if d['belt']>=.65:cand.append(('more-belt-forward',2,'more belt potential'))
 if d['movement']>=.65:cand.append(('more-movement-driven',2,'more movement energy'))
 if d['narrative']>=.65:cand.append(('more-narrative-driven',2,'more narrative emphasis'))
 if d['hooks']>=.65:cand.append(('hookier',2,'more hook density'))
 if dist>=1.35 and norm:cand.append(('wild-card-bridge',1,'shared DNA with wider profile distance'))
 if not cand:return 'catalog-authored',[], 'low','no dominant computed route',dist,d,norm,sorted(raw)
 cand.sort(key=lambda x:-x[1]); pri=cand[0]
 tags=[]
 for x in cand:
  if x[0] not in tags:tags.append(x[0])
 conf='high' if pri[1]>=4 else 'medium' if pri[1]>=2 else 'low'
 return pri[0],tags,conf,pri[2],dist,d,norm,sorted(raw)

rows=[]
for a in titles:
 for bid in a.get('links',[]):
  if bid not in by or bid==a['id']:continue
  b=by[bid]; pri,tags,conf,why,dist,d,norm,raw=classify(a,b)
  rows.append({'id':a['id']+'->'+b['id'],'source':a['id'],'target':b['id'],'primaryRoute':pri,'routeTags':tags,'confidence':conf,'computedRationale':why,'scoreDistance':dist,'scoreDeltas':d,'sharedNormalizedDNA':norm,'sharedRawDNA':raw,'provenance':{'type':'derived-from-authored-direction','note':'Direction comes from titles.json; route labels are computed review aids.'}})
routes=['safe-next-step','adjacent-style','higher-intensity','lower-friction','more-emotional','more-belt-forward','more-movement-driven','more-narrative-driven','hookier','wild-card-bridge','catalog-authored']
summary={'titleCount':len(titles),'directionCount':len(rows),'routeCounts':{k:sum(x['primaryRoute']==k for x in rows) for k in routes},'confidenceCounts':{k:sum(x['confidence']==k for x in rows) for k in ['high','medium','low']}}
out={'version':1,'summary':summary,'directions':rows}
(P/'data/recommendation-directions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
lines=['# Recommendation Direction Architecture v1','',f"Titles: **{len(titles)}**",f"Authored directions: **{len(rows)}**",'', '## Principle','', 'Relatedness and recommendation direction are separate layers. Route labels describe the computed move from source to target and remain review aids.','', '## Primary route distribution','']
for k,v in summary['routeCounts'].items():lines.append(f'- **{k}**: {v}')
lines+=['','## High-confidence examples','']
for r in sorted([x for x in rows if x['confidence']=='high'],key=lambda x:(x['primaryRoute'],x['scoreDistance']))[:60]:lines.append(f"- `{r['source']} -> {r['target']}` | **{r['primaryRoute']}** | distance {r['scoreDistance']}")
lines+=['','## Low-confidence review queue','']
for r in sorted([x for x in rows if x['confidence']=='low'],key=lambda x:x['scoreDistance'])[:60]:lines.append(f"- `{r['source']} -> {r['target']}` | {r['primaryRoute']} | distance {r['scoreDistance']}")
(P/'data/RECOMMENDATION_DIRECTIONS.md').write_text('\n'.join(lines)+'\n')
print(summary)
