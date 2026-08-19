import json
from pathlib import Path

ROOT=Path('.')
p=ROOT/'data/titles.json'
titles=json.loads(p.read_text(encoding='utf-8'))
by_id={x['id']:x for x in titles}

# Human-curated relatedness promotions. These are deliberately conservative:
# each pair is considered genuinely useful in both directions as a RELATED TITLE,
# even if future recommendation direction may differ.
promotions={
 ('tickstage','waitress'):'contemporary singer-songwriter stage storytelling',
 ('frozen','moana'):'modern Disney musical anchors with major pop/Broadway hooks',
 ('meangirls','prom'):'contemporary comedy-pop adaptations with ensemble dance energy',
 ('legallyblonde','newsies'):'high-propulsion dance-forward Broadway captures',
 ('frozen','tangled'):'closely related modern Disney musical language and comfort appeal',
 ('billyelliot','newsies'):'dance-driven stage storytelling with youth and class stakes',
 ('cabaret','chicago'):'jazz/cabaret lineage, theatrical cynicism, and Fosse-adjacent language',
 ('lalaland','once'):'intimate music-centered romance with melancholy creative ambition',
 ('legallyblonde','hairspray'):'bright pop-Broadway propulsion, comedy, dance, and cathartic belt energy',
 ('hedwigstage','hedwig'):'same underlying musical work across stage and film forms',
 ('jcs','rent'):'rock-driven sung theatrical storytelling with high emotional intensity',
 ('pitchperfect','mammamia'):'familiar-pop communal sing-along energy and high replay value',
 ('frozen','encanto'):'modern Disney ensemble musicals with family-centered emotional architecture',
 ('grease','mammamia'):'familiar-pop sing-along comfort and communal performance energy',
 ('rent','hedwig'):'queer rock musical lineage, direct emotional expression, and cult identity',
 ('cyrano','lastfive'):'romantic yearning carried by contemporary musical storytelling',
 ('meangirls','jamie'):'contemporary pop musical theater centered on identity and social belonging',
 ('onceisland','comefromaway'):'ensemble-led communal storytelling with folk/rhythmic foundations',
 ('reefer','rocky'):'cult camp rock musicals built around maximal commitment and satire',
 ('tangled','moana'):'Disney yearning/adventure musicals with strong pop/Broadway songwriting',
 ('rockyhorrorlive','rocky'):'same core work across original and remake/performance interpretation',
 ('mammamia','moulin'):'jukebox spectacle, romance, maximalism, and familiar-pop propulsion',
 ('rockofages','across'):'rock jukebox musicals using familiar songs as narrative architecture',
 ('yesterday','across'):'Beatles-centered music storytelling from contrasting narrative forms',
 ('legallyblonde','meangirls'):'female-led contemporary comedy musicals with pop score and dance propulsion',
 ('cyrano','phantom'):'orchestral romantic maximalism, yearning, and theatrical melodrama'
}

missing=[]
for a,b in promotions:
    if a not in by_id or b not in by_id: missing.append((a,b))
assert not missing,missing

added=[]
for (a,b),reason in promotions.items():
    A,B=by_id[a],by_id[b]
    A.setdefault('links',[]); B.setdefault('links',[])
    changed=False
    if b not in A['links']:
        A['links'].append(b); changed=True
    if a not in B['links']:
        B['links'].append(a); changed=True
    if changed: added.append({'titles':[a,b],'reason':reason})

# Stable link ordering keeps diffs deterministic.
for x in titles:
    x['links']=sorted(dict.fromkeys(x.get('links',[])))

p.write_text(json.dumps(titles,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
curation={
 'version':1,
 'policy':'Curated promotions convert selected high-confidence one-way relatedness edges into reciprocal relatedness. This does not assert equal recommendation direction.',
 'promotionCount':len(promotions),
 'changedCount':len(added),
 'promotions':[{'titles':list(pair),'reason':reason} for pair,reason in promotions.items()]
}
(ROOT/'data/relationship-curation.json').write_text(json.dumps(curation,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('curated',len(promotions),'pairs; changed',len(added))
