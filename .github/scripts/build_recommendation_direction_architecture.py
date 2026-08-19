import json, math
from pathlib import Path
P=Path('.')
titles=json.loads((P/'data/titles.json').read_text())
by={x['id']:x for x in titles}
keys=['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks','afterglow','replay']

ROUTES=['safe-next-step','adjacent-style','higher-intensity','lower-friction','more-emotional','more-belt-forward','more-movement-driven','more-narrative-driven','hookier','wild-card-bridge','catalog-authored']

# v2: rank routes by evidence strength instead of insertion order. Broad routes such as
# higher-intensity and lower-friction require composite evidence, while specific routes
# can win when one dimension is the clearest directional change.
def classify(a,b):
    d={k:round(b['scores'][k]-a['scores'][k],3) for k in keys}
    dist=round(math.sqrt(sum((a['scores'][k]-b['scores'][k])**2 for k in keys)/len(keys)),3)
    na=set(a.get('dnaNormalized',a.get('dna',[]))); nb=set(b.get('dnaNormalized',b.get('dna',[])))
    raw=sorted(set(a.get('dna',[]))&set(b.get('dna',[]))); norm=sorted(na&nb)
    evidence=[]

    def add(route,strength,why):
        if strength>0:evidence.append({'route':route,'strength':round(strength,3),'why':why})

    # Similarity is strongest only when genuinely close. Shared DNA raises confidence.
    if dist<=0.58:
        add('safe-next-step',1.30+(0.58-dist)*1.8+(0.12 if norm else 0),'close overall profile')

    # Style adjacency requires both shared DNA and reasonably close behavior.
    if norm and dist<=1.00:
        add('adjacent-style',0.78+min(.30,.07*len(norm))+(1.00-dist)*.35,'shared musical DNA with compatible profile')

    # Lower friction should mean materially easier/safer, not merely more comfortable.
    friction_gain=d['comfort'] - .45*max(0,d['emotion']) - .35*max(0,d['maximalism'])
    if d['comfort']>=.75 and friction_gain>=.55:
        add('lower-friction',0.68+min(.85,friction_gain*.42),'higher comfort without a matching rise in emotional or maximalist load')

    # Broad intensity now requires a composite upward move. Maximalism alone cannot win.
    intensity_components=[d['propulsion'],d['movement'],d['maximalism']]
    positive=[x for x in intensity_components if x>0]
    intensity=sum(max(0,x) for x in intensity_components)/3
    if intensity>=.55 and len([x for x in intensity_components if x>=.40])>=2:
        add('higher-intensity',0.62+min(.90,intensity*.48),'combined rise in propulsion, movement, and/or maximalism')

    # Specific directional moves get magnitude-sensitive strength and can outrank broad labels.
    specs=[
        ('more-emotional','emotion',.72,'higher emotional intensity'),
        ('more-belt-forward','belt',.72,'more belt potential'),
        ('more-movement-driven','movement',.72,'more movement energy'),
        ('more-narrative-driven','narrative',.72,'more narrative emphasis'),
        ('hookier','hooks',.72,'more hook density')]
    for route,key,threshold,why in specs:
        if d[key]>=threshold:
            add(route,0.70+min(1.05,(d[key]-threshold)*.52+d[key]*.18),why)

    # Wild cards require a true profile jump plus some connective tissue.
    if dist>=1.35 and norm:
        add('wild-card-bridge',0.58+min(.45,(dist-1.35)*.3)+min(.18,.06*len(norm)),'shared DNA across a deliberately wider profile jump')

    if not evidence:
        return 'catalog-authored',[], 'low','no dominant computed route',dist,d,norm,raw,0,[]

    # Route-specific tie preference: specific moves > adjacency > broad intensity/friction when strengths are nearly equal.
    tie_order={'safe-next-step':0,'more-emotional':1,'more-belt-forward':2,'more-movement-driven':3,'more-narrative-driven':4,'hookier':5,'adjacent-style':6,'lower-friction':7,'higher-intensity':8,'wild-card-bridge':9}
    evidence.sort(key=lambda x:(-x['strength'],tie_order.get(x['route'],99)))
    pri=evidence[0]
    tags=[x['route'] for x in evidence]
    margin=pri['strength']-(evidence[1]['strength'] if len(evidence)>1 else 0)
    if pri['route']=='safe-next-step' and pri['strength']>=1.24:
        conf='high'
    elif pri['strength']>=1.12 and margin>=.16:
        conf='high'
    elif pri['strength']>=.82:
        conf='medium'
    else:
        conf='low'
    return pri['route'],tags,conf,pri['why'],dist,d,norm,raw,pri['strength'],evidence

rows=[]
for a in titles:
    for bid in a.get('links',[]):
        if bid not in by or bid==a['id']:continue
        b=by[bid]
        pri,tags,conf,why,dist,d,norm,raw,strength,evidence=classify(a,b)
        rows.append({'id':a['id']+'->'+b['id'],'source':a['id'],'target':b['id'],'primaryRoute':pri,'routeTags':tags,'confidence':conf,'computedRationale':why,'primaryStrength':strength,'routeEvidence':evidence,'scoreDistance':dist,'scoreDeltas':d,'sharedNormalizedDNA':norm,'sharedRawDNA':raw,'provenance':{'type':'derived-from-authored-direction','note':'Direction comes from titles.json; v2 route labels are calibrated computed review aids, not editorial truth.'}})

summary={'titleCount':len(titles),'directionCount':len(rows),'routeCounts':{k:sum(x['primaryRoute']==k for x in rows) for k in ROUTES},'confidenceCounts':{k:sum(x['confidence']==k for x in rows) for k in ['high','medium','low']}}
out={'version':2,'summary':summary,'heuristicPolicy':{
    'principle':'Primary routes are selected by evidence strength, not rule order.',
    'higher-intensity':'Requires a composite rise across at least two of propulsion, movement, and maximalism.',
    'lower-friction':'Requires comfort gain that is not cancelled by rising emotion or maximalism.',
    'specific-routes':'Emotion, belt, movement, narrative, and hooks compete by magnitude and may outrank broad routes.',
    'confidence':'Uses evidence strength and winning margin, rather than route category alone.'
},'directions':rows}
(P/'data/recommendation-directions.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
lines=['# Recommendation Direction Architecture v2','',f"Titles: **{len(titles)}**",f"Authored directions: **{len(rows)}**",'', '## Principle','', 'Relatedness and recommendation direction remain separate layers. v2 chooses the primary route by evidence strength rather than classifier rule order.','', '## Primary route distribution','']
for k,v in summary['routeCounts'].items():lines.append(f'- **{k}**: {v}')
lines+=['','## Confidence distribution','']
for k,v in summary['confidenceCounts'].items():lines.append(f'- **{k}**: {v}')
lines+=['','## High-confidence examples','']
for r in sorted([x for x in rows if x['confidence']=='high'],key=lambda x:(x['primaryRoute'],-x['primaryStrength']))[:60]:lines.append(f"- `{r['source']} -> {r['target']}` | **{r['primaryRoute']}** | strength {r['primaryStrength']} | distance {r['scoreDistance']}")
lines+=['','## Low-confidence review queue','']
for r in sorted([x for x in rows if x['confidence']=='low'],key=lambda x:(-x['primaryStrength'],x['scoreDistance']))[:60]:lines.append(f"- `{r['source']} -> {r['target']}` | {r['primaryRoute']} | strength {r['primaryStrength']} | distance {r['scoreDistance']}")
(P/'data/RECOMMENDATION_DIRECTIONS.md').write_text('\n'.join(lines)+'\n')
print(summary)
