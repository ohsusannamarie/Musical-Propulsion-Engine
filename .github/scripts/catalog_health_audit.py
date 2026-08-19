import json, math, statistics
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path('.')
TITLES=ROOT/'data/titles.json'
POSTERS=ROOT/'assets/posters'
OUT_JSON=ROOT/'data/catalog-health.json'
OUT_MD=ROOT/'data/CATALOG_HEALTH.md'

data=json.loads(TITLES.read_text(encoding='utf-8'))
by_id={x['id']:x for x in data}
ids=set(by_id)

# Core structural checks
orphans=[]; weak_links=[]; broken_links=[]; inbound=Counter(); degree={}
for x in data:
    links=[y for y in x.get('links',[]) if y!=x['id']]
    valid=[y for y in links if y in ids]
    bad=[y for y in links if y not in ids]
    broken_links.extend((x['id'],y) for y in bad)
    degree[x['id']]=len(set(valid))
    for y in set(valid): inbound[y]+=1
    if not valid: orphans.append(x['id'])
    if len(set(valid))<3: weak_links.append(x['id'])

one_way=[]
for a in data:
    for b in a.get('links',[]):
        if b in by_id and a['id'] not in by_id[b].get('links',[]):
            one_way.append((a['id'],b))

# Taxonomy coverage
DNA=Counter(); VIBE=Counter(); FORMAT=Counter(); TYPE=Counter(); STATUS=Counter()
for x in data:
    DNA.update(x.get('dna',[])); VIBE.update(x.get('vibe',[])); STATUS[x.get('status','unknown')]+=1
    e=x.get('enrichment',{})
    FORMAT[e.get('format') or 'missing']+=1
    TYPE[e.get('musicalType') or 'missing']+=1

# Enrichment completeness
required=['format','musicalType','vocalStyle','lyricalDensity','musicDrivenPercent','catharsis','rewatchability','familiarityAdvantage','bestMood','friction','gatewaySongs','notes','provenance']
missing_fields=defaultdict(list)
for x in data:
    e=x.get('enrichment',{})
    for k in required:
        v=e.get(k)
        if v is None or v==[] or v=='': missing_fields[k].append(x['id'])

# Score distributions
score_keys=['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks','afterglow','replay']
score_stats={}
for k in score_keys:
    vals=[float(x['scores'][k]) for x in data if k in x.get('scores',{})]
    score_stats[k]={
        'mean': round(statistics.mean(vals),2),
        'median': round(statistics.median(vals),2),
        'stdev': round(statistics.pstdev(vals),2),
        'min': min(vals),'max': max(vals),
        'high_4_5_plus': sum(v>=4.5 for v in vals),
        'low_3_or_less': sum(v<=3 for v in vals),
    }

# Duplicate-ish conceptual coverage: exact normalized DNA signatures
sig=defaultdict(list)
for x in data:
    key=tuple(sorted(s.strip().lower() for s in x.get('dna',[])))
    sig[key].append(x['id'])
duplicate_dna_groups=[v for v in sig.values() if len(v)>=3]

# Poster/media gaps
poster_ids=set()
if POSTERS.exists():
    for p in POSTERS.iterdir():
        if p.is_file(): poster_ids.add(p.stem)
poster_gaps=sorted(ids-poster_ids)

# Gateway coverage and thin records
no_gateway=[]; thin_gateway=[]
for x in data:
    g=x.get('enrichment',{}).get('gatewaySongs') or []
    if not g:no_gateway.append(x['id'])
    elif len(g)<2:thin_gateway.append(x['id'])

# Connectivity ranking
hubs=sorted(((k,degree.get(k,0)+inbound.get(k,0)) for k in ids), key=lambda z:z[1], reverse=True)

# Coverage-gap heuristics
under_dna=[{'tag':k,'count':v} for k,v in sorted(DNA.items(), key=lambda kv:(kv[1],kv[0])) if v<=2]
over_dna=[{'tag':k,'count':v} for k,v in DNA.most_common(12)]
under_vibe=[{'tag':k,'count':v} for k,v in sorted(VIBE.items(), key=lambda kv:(kv[1],kv[0])) if v<=2]

# Health score intentionally simple and inspectable
penalty=0
penalty += len(orphans)*4
penalty += len(weak_links)*1.25
penalty += len(broken_links)*3
penalty += len(poster_gaps)*0.5
penalty += sum(len(v) for v in missing_fields.values())*0.08
penalty += len(no_gateway)*0.75
health=max(0,round(100-penalty,1))

report={
 'catalogSize':len(data),
 'healthScore':health,
 'connectivity':{
   'orphans':orphans,'weakUnder3Links':weak_links,'brokenLinks':[{'from':a,'to':b} for a,b in broken_links],
   'oneWayLinksCount':len(one_way),'oneWayExamples':[{'from':a,'to':b} for a,b in one_way[:30]],
   'topHubs':[{'id':k,'combinedDegree':v} for k,v in hubs[:15]]
 },
 'coverage':{
   'formats':dict(FORMAT),'musicalTypes':dict(TYPE),'statuses':dict(STATUS),
   'topDNA':over_dna,'underrepresentedDNA':under_dna[:40],
   'underrepresentedVibes':under_vibe[:40],
   'duplicateDNAGroups':duplicate_dna_groups
 },
 'enrichment':{
   'missingFields':dict(missing_fields),'noGatewaySongs':no_gateway,'thinGatewaySongs':thin_gateway
 },
 'scores':score_stats,
 'media':{'posterGapCount':len(poster_gaps),'posterGaps':poster_gaps},
 'recommendationReadiness':{
   'note':'Proxy audit only. Safe Bet / Smart Stretch / Wild Card diversity depends on live user taste weights in localStorage and cannot be fully evaluated in CI.',
   'candidateConcerns':[
      'High score means cluster tightly around 4.5 to 5.0 on several dimensions, which can compress ranking separation.' if any(v['stdev']<0.65 for v in score_stats.values()) else 'Score spread is generally healthy.',
      f'{len(weak_links)} titles have fewer than three explicit links.',
      f'{len(poster_gaps)} titles lack bundled poster assets.'
   ]
 }
}
OUT_JSON.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

lines=[]
lines += ['# Catalog Health Audit','',f'**Catalog size:** {len(data)} titles  ',f'**Health score:** {health}/100','']
lines += ['## Highest-priority fixes','']
priorities=[]
if broken_links: priorities.append(f'Fix {len(broken_links)} broken relationship links.')
if orphans: priorities.append(f'Connect {len(orphans)} orphan titles: '+', '.join(orphans[:12]))
if weak_links: priorities.append(f'Strengthen {len(weak_links)} titles with fewer than 3 valid links.')
if poster_gaps: priorities.append(f'Add bundled poster/media assets for {len(poster_gaps)} titles.')
missing_total=sum(len(v) for v in missing_fields.values())
if missing_total: priorities.append(f'Fill {missing_total} missing enrichment-field values across the catalog.')
if no_gateway: priorities.append(f'Add gateway songs for {len(no_gateway)} titles.')
if not priorities: priorities=['No critical structural problems detected.']
for i,p in enumerate(priorities,1): lines.append(f'{i}. {p}')
lines += ['','## Connectivity','',f'- Orphans: **{len(orphans)}**',f'- Under 3 explicit links: **{len(weak_links)}**',f'- Broken links: **{len(broken_links)}**',f'- One-way relationship links: **{len(one_way)}**','']
lines += ['### Top hubs','']
for k,v in hubs[:10]: lines.append(f'- **{by_id[k]["title"]}**: {v} combined inbound + outbound links')
lines += ['','## Coverage','',f'- Formats: `{dict(FORMAT)}`',f'- Musical types: `{dict(TYPE)}`','']
lines += ['### Most common DNA','']
for x in over_dna[:10]: lines.append(f'- {x["tag"]}: {x["count"]}')
lines += ['','### Underrepresented DNA candidates','']
for x in under_dna[:20]: lines.append(f'- {x["tag"]}: {x["count"]}')
lines += ['','## Score spread','']
for k,v in score_stats.items(): lines.append(f'- **{k}**: mean {v["mean"]}, stdev {v["stdev"]}, range {v["min"]} to {v["max"]}')
lines += ['','## Media','',f'- Poster gaps: **{len(poster_gaps)}**']
if poster_gaps: lines.append('- Missing: '+', '.join(poster_gaps[:40]))
lines += ['','## What this audit cannot know','', 'The CI audit cannot reproduce Susanna’s live Safe Bet / Smart Stretch / Wild Card mix because taste-feedback weights are stored locally in the browser. This report therefore audits catalog readiness, not personalized ranking outcomes.']
OUT_MD.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'titles':len(data),'health':health,'orphans':len(orphans),'weakLinks':len(weak_links),'brokenLinks':len(broken_links),'posterGaps':len(poster_gaps),'missingFields':missing_total},indent=2))
