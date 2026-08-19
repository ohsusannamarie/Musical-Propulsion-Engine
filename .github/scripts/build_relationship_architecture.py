import json, math
from pathlib import Path

ROOT=Path('.')
titles=json.loads((ROOT/'data/titles.json').read_text(encoding='utf-8'))
by_id={x['id']:x for x in titles}
score_keys=['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks','afterglow','replay']

pairs={}
for x in titles:
    for yid in x.get('links',[]):
        if yid not in by_id or yid==x['id']: continue
        a,b=sorted([x['id'],yid]); rec=pairs.setdefault((a,b),{'a':a,'b':b,'a_to_b':False,'b_to_a':False})
        if x['id']==a: rec['a_to_b']=True
        else: rec['b_to_a']=True

def quality_tier(shared_norm,shared_raw,distance,same_format,same_type):
    # Conservative candidate tiers. These describe evidence strength only.
    points=0
    points += min(3,len(shared_norm))
    points += min(2,len(shared_raw))
    points += 1 if same_format else 0
    points += 1 if same_type else 0
    points += 3 if distance<=0.55 else 2 if distance<=0.75 else 1 if distance<=0.95 else 0
    if points>=7: return 'A'
    if points>=5: return 'B'
    if points>=3: return 'C'
    return 'D'

edges=[]
for (a,b),rec in sorted(pairs.items()):
    A,B=by_id[a],by_id[b]
    rawA=A.get('dna',[]); rawB=B.get('dna',[]); normA=A.get('dnaNormalized',rawA); normB=B.get('dnaNormalized',rawB)
    shared_raw=sorted(set(rawA)&set(rawB)); shared_norm=sorted(set(normA)&set(normB))
    distance=round(math.sqrt(sum((A['scores'][k]-B['scores'][k])**2 for k in score_keys)/len(score_keys)),3)
    same_format=A.get('enrichment',{}).get('format')==B.get('enrichment',{}).get('format')
    same_type=A.get('enrichment',{}).get('musicalType')==B.get('enrichment',{}).get('musicalType')
    reciprocal=rec['a_to_b'] and rec['b_to_a']; direction='reciprocal' if reciprocal else 'one-way'
    authored=[f'{a}->{b}',f'{b}->{a}'] if reciprocal else [f'{a}->{b}' if rec['a_to_b'] else f'{b}->{a}']
    signals=[]
    if shared_norm: signals.append('shared-normalized-dna')
    if shared_raw: signals.append('shared-raw-dna')
    if same_format: signals.append('same-format')
    if same_type: signals.append('same-musical-type')
    if distance<=0.75: signals.append('close-score-profile')
    tier=quality_tier(shared_norm,shared_raw,distance,same_format,same_type)
    reciprocal_candidate=(direction=='one-way' and tier in ('A','B'))
    edges.append({'id':f'{a}__{b}','titles':[a,b],'authoredDirection':direction,'authoredLinks':authored,'relationshipClass':'catalog-link','qualityTier':tier,'reciprocalCandidate':reciprocal_candidate,'evidence':{'sharedNormalizedDNA':shared_norm,'sharedRawDNA':shared_raw,'scoreDistance':distance,'sameFormat':same_format,'sameMusicalType':same_type},'signals':signals,'provenance':{'type':'derived-from-authored-links','note':'Direction is preserved from titles.json; evidence and quality tiers are computed review aids, not editorial claims.'}})

summary={'titleCount':len(titles),'edgeCount':len(edges),'reciprocalEdges':sum(e['authoredDirection']=='reciprocal' for e in edges),'oneWayEdges':sum(e['authoredDirection']=='one-way' for e in edges),'edgesWithSharedNormalizedDNA':sum(bool(e['evidence']['sharedNormalizedDNA']) for e in edges),'edgesWithCloseScoreProfile':sum(e['evidence']['scoreDistance']<=0.75 for e in edges),'reciprocalCandidates':sum(e['reciprocalCandidate'] for e in edges),'qualityTiers':{t:sum(e['qualityTier']==t for e in edges) for t in 'ABCD'}}
out={'version':3,'summary':summary,'relationshipSemantics':{'catalog-link':'An explicit title-to-title link authored in titles.json.','reciprocal':'Both titles explicitly link to each other.','one-way':'Only one title explicitly links to the other. This is preserved, not automatically repaired.','evidence':'Computed descriptive signals used to understand why an edge may exist. They are not asserted causal explanations.','qualityTier':'Computed evidence-strength review tier. A/B are strong candidates for human review, not automatic truth.','reciprocalCandidate':'A one-way edge with A/B evidence strength. Candidate status never mutates titles.json automatically.'},'relationships':edges}
(ROOT/'data/relationships.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

lines=['# Relationship Architecture v3','',f"Titles: **{summary['titleCount']}**",f"Canonical edges: **{summary['edgeCount']}**",f"Reciprocal edges: **{summary['reciprocalEdges']}**",f"One-way edges: **{summary['oneWayEdges']}**",f"Strong reciprocal candidates: **{summary['reciprocalCandidates']}**",f"Quality tiers: **A {summary['qualityTiers']['A']} · B {summary['qualityTiers']['B']} · C {summary['qualityTiers']['C']} · D {summary['qualityTiers']['D']}**",'', '## Principle','', 'Direction remains authored data. Quality tiers rank evidence for review and never manufacture reciprocity. This lets recommendation direction remain distinct from simple relatedness.','', '## Strong reciprocal candidates','']
cands=[e for e in edges if e['reciprocalCandidate']]
cands.sort(key=lambda e:('AB'.index(e['qualityTier']),e['evidence']['scoreDistance'],-len(e['evidence']['sharedNormalizedDNA'])))
for e in cands:
    shared=', '.join(e['evidence']['sharedNormalizedDNA']) or 'none'
    lines.append(f"- **Tier {e['qualityTier']}** `{e['authoredLinks'][0]}` | distance {e['evidence']['scoreDistance']} | DNA: {shared} | signals: {', '.join(e['signals']) or 'none'}")
lines += ['', '## Lower-confidence one-way review queue','']
rest=[e for e in edges if e['authoredDirection']=='one-way' and not e['reciprocalCandidate']]
rest.sort(key=lambda e:(e['qualityTier'],e['evidence']['scoreDistance']))
for e in rest[:50]:
    shared=', '.join(e['evidence']['sharedNormalizedDNA']) or 'none'
    lines.append(f"- **Tier {e['qualityTier']}** `{e['authoredLinks'][0]}` | distance {e['evidence']['scoreDistance']} | DNA: {shared}")
(ROOT/'data/RELATIONSHIP_ARCHITECTURE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(summary)
