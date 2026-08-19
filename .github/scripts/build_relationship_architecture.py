import json, math
from pathlib import Path

ROOT=Path('.')
titles=json.loads((ROOT/'data/titles.json').read_text(encoding='utf-8'))
by_id={x['id']:x for x in titles}
score_keys=['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks','afterglow','replay']

# Preserve authored directionality. Build one canonical edge per pair, then annotate
# whether the authored link is reciprocal or one-way. Do not invent reciprocity.
pairs={}
for x in titles:
    for yid in x.get('links',[]):
        if yid not in by_id or yid==x['id']:
            continue
        a,b=sorted([x['id'],yid])
        key=(a,b)
        rec=pairs.setdefault(key,{'a':a,'b':b,'a_to_b':False,'b_to_a':False})
        if x['id']==a: rec['a_to_b']=True
        else: rec['b_to_a']=True

edges=[]
for (a,b),rec in sorted(pairs.items()):
    A,B=by_id[a],by_id[b]
    rawA=A.get('dna',[]); rawB=B.get('dna',[])
    normA=A.get('dnaNormalized',rawA); normB=B.get('dnaNormalized',rawB)
    shared_raw=sorted(set(rawA)&set(rawB))
    shared_norm=sorted(set(normA)&set(normB))
    d=0
    for k in score_keys:
        d+=(A['scores'][k]-B['scores'][k])**2
    distance=round(math.sqrt(d/len(score_keys)),3)
    reciprocal=rec['a_to_b'] and rec['b_to_a']
    if reciprocal:
        direction='reciprocal'
        authored=[f'{a}->{b}',f'{b}->{a}']
    else:
        direction='one-way'
        authored=[f'{a}->{b}' if rec['a_to_b'] else f'{b}->{a}']
    evidence=[]
    if shared_norm: evidence.append('shared-normalized-dna')
    if shared_raw: evidence.append('shared-raw-dna')
    if A.get('enrichment',{}).get('format')==B.get('enrichment',{}).get('format'): evidence.append('same-format')
    if A.get('enrichment',{}).get('musicalType')==B.get('enrichment',{}).get('musicalType'): evidence.append('same-musical-type')
    if distance<=0.75: evidence.append('close-score-profile')
    edges.append({
        'id':f'{a}__{b}',
        'titles':[a,b],
        'authoredDirection':direction,
        'authoredLinks':authored,
        'relationshipClass':'catalog-link',
        'evidence':{
            'sharedNormalizedDNA':shared_norm,
            'sharedRawDNA':shared_raw,
            'scoreDistance':distance,
            'sameFormat':A.get('enrichment',{}).get('format')==B.get('enrichment',{}).get('format'),
            'sameMusicalType':A.get('enrichment',{}).get('musicalType')==B.get('enrichment',{}).get('musicalType')
        },
        'signals':evidence,
        'provenance':{'type':'derived-from-authored-links','note':'Direction is preserved from titles.json; evidence fields are computed, not editorial claims.'}
    })

summary={
    'titleCount':len(titles),
    'edgeCount':len(edges),
    'reciprocalEdges':sum(e['authoredDirection']=='reciprocal' for e in edges),
    'oneWayEdges':sum(e['authoredDirection']=='one-way' for e in edges),
    'edgesWithSharedNormalizedDNA':sum(bool(e['evidence']['sharedNormalizedDNA']) for e in edges),
    'edgesWithCloseScoreProfile':sum(e['evidence']['scoreDistance']<=0.75 for e in edges)
}
out={'version':2,'summary':summary,'relationshipSemantics':{
    'catalog-link':'An explicit title-to-title link authored in titles.json.',
    'reciprocal':'Both titles explicitly link to each other.',
    'one-way':'Only one title explicitly links to the other. This is preserved, not automatically repaired.',
    'evidence':'Computed descriptive signals used to understand why an edge may exist. They are not asserted causal explanations.'
},'relationships':edges}
(ROOT/'data/relationships.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Human-readable architecture report.
lines=['# Relationship Architecture v2','',f"Titles: **{summary['titleCount']}**",f"Canonical edges: **{summary['edgeCount']}**",f"Reciprocal edges: **{summary['reciprocalEdges']}**",f"One-way edges: **{summary['oneWayEdges']}**",'', '## Principle','', 'This pass does not force symmetry. It separates authored direction from computed evidence so future recommendation direction can be modeled independently from simple relatedness.','', '## Highest-priority one-way edges for editorial review','']
one=[e for e in edges if e['authoredDirection']=='one-way']
one.sort(key=lambda e:(e['evidence']['scoreDistance'], -len(e['evidence']['sharedNormalizedDNA'])))
for e in one[:40]:
    A,B=e['titles']; route=e['authoredLinks'][0]
    shared=', '.join(e['evidence']['sharedNormalizedDNA']) or 'none'
    lines.append(f"- `{route}` | score distance {e['evidence']['scoreDistance']} | shared normalized DNA: {shared}")
(ROOT/'data/RELATIONSHIP_ARCHITECTURE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(summary)
