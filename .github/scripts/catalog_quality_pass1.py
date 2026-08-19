import json
from pathlib import Path

p = Path('data/titles.json')
data = json.loads(p.read_text(encoding='utf-8'))
by_id = {x['id']: x for x in data}

# 1) Repair known broken relationship IDs from the 81-title health audit.
repairs = {
    ('legallyblonde', 'meanGirls'): 'meangirls',
    ('velvetgoldmine', 'purpleRain'): 'purplerain',
    ('onceisland', 'comeFromAway'): 'comefromaway',
}
for (src, bad), good in repairs.items():
    x = by_id[src]
    x['links'] = [good if v == bad else v for v in x.get('links', [])]

# 2) Add a normalized DNA layer without destroying the expressive/raw DNA tags.
# Raw `dna` remains editorial texture used by the UI. `dnaNormalized` gives the
# recommendation/data layer stable parent concepts for coverage analysis.
parent_map = {
    '60s Pop':'Pop','70s Rock':'Rock','80s New Wave':'New Wave','ABBA':'Pop',
    'Acoustic':'Folk','Acoustic Pop':'Pop','Ballad':'Ballad','Blues':'Blues',
    'Burlesque':'Cabaret','Caribbean Influence':'World/Regional','Celtic':'Folk',
    'Chamber Pop':'Pop','Children’s Chorus':'Musical Theater','Christmas':'Holiday',
    'Classic Hollywood Musical':'Golden Age','Classic Musical':'Golden Age',
    'Classic Rock':'Rock','Colombian Influence':'World/Regional','Coming-of-Age':'Narrative Theme',
    'Concept Album':'Rock Opera','Contemporary Pop Musical':'Pop','Counterculture':'Rock',
    'Country':'Country','Dark Comedy':'Comedy','Disco':'Disco','Doo-wop':'R&B',
    'Drag':'Performance','Electronic':'Electronic','Electropop':'Electronic','Elton John':'Pop',
    'Fantasy Musical':'Musical Theater','Folk Rock':'Rock','Golden Age Revival':'Golden Age',
    'Goth':'Rock','Hair Metal':'Rock','Holiday':'Holiday','Horror':'Genre Hybrid',
    'Indie Folk':'Folk','Indie Rock':'Rock','Industrial':'Electronic','Jazz':'Jazz',
    'Jukebox':'Jukebox','Latin':'Latin','Musical Theater':'Musical Theater',
    'Contemporary Musical Theater':'Musical Theater','New Wave':'New Wave','Orchestral':'Orchestral',
    'Polynesian Influence':'World/Regional','Pop':'Pop','Pop Rock':'Rock','Power Ballad':'Ballad',
    'Punk':'Rock','R&B':'R&B','Rap':'Hip-hop','Rock':'Rock','Rock and Roll':'Rock',
    'Rock Opera':'Rock Opera','Salsa':'Latin','Singer-Songwriter':'Singer-Songwriter',
    'Synth-pop':'Electronic','Vaudeville':'Cabaret','Broadway':'Musical Theater',
    'A cappella':'Vocal Performance','Animation':'Animation','Comedy':'Comedy',
    'Dance':'Dance','Family':'Family','Folk':'Folk','Gospel':'Gospel','Hip-hop':'Hip-hop',
    'Experimental':'Experimental','Cabaret':'Cabaret','Glam Rock':'Rock','Music Drama':'Music Drama',
    'Queer Cinema':'Queer','Stage Rock':'Rock','Disney':'Musical Theater'
}

for x in data:
    raw = x.get('dna', [])
    normalized = []
    for tag in raw:
        parent = parent_map.get(tag, tag)
        if parent not in normalized:
            normalized.append(parent)
    x['dnaNormalized'] = normalized

# Hard integrity checks.
ids = set(by_id)
assert len(ids) == len(data)
for x in data:
    broken = [v for v in x.get('links', []) if v not in ids]
    assert not broken, (x['id'], broken)
    assert x.get('dnaNormalized'), x['id']

p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

# Separate taxonomy contract for future expansion/research tooling.
taxonomy = {
    'version': 1,
    'purpose': 'Preserve expressive DNA tags while providing stable parent concepts for analysis and recommendation logic.',
    'parentMap': parent_map,
    'rules': [
        'Do not delete raw dna tags solely to improve counts.',
        'Use dnaNormalized for broad coverage and model features.',
        'A title may have multiple normalized DNA parents.',
        'New raw tags should receive a parent when they are too specific to stand alone analytically.'
    ]
}
Path('data/dna-taxonomy.json').write_text(json.dumps(taxonomy, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Quality pass 1 complete: {len(data)} titles, 3 broken links repaired, normalized DNA added.')
