import json
from pathlib import Path

path = Path('data/titles.json')
data = json.loads(path.read_text(encoding='utf-8'))
by_id = {x['id']: x for x in data}

profiles = {
  'moulin': {
    'format':'film','musicalType':'jukebox','vocalStyle':['theatrical pop','power belt','ensemble','romantic ballad'],
    'lyricalDensity':3,'musicDrivenPercent':88,'catharsis':5,'rewatchability':5,'familiarityAdvantage':4,
    'bestMood':['maximalist','romantic','cathartic','belt-along','need to feel everything'],
    'friction':['deliberately overwhelming visual style','tragic ending'],
    'gatewaySongs':[
      {'song':'El Tango de Roxanne','purpose':'maximum emotional escalation'},
      {'song':'Come What May','purpose':'romantic belt instinct'},
      {'song':'Elephant Love Medley','purpose':'jukebox transformation proof'}],
    'notes':'Primary reference title for emotional maximalism. Familiar songs are not decoration here; they are reorganized into narrative propulsion.',
  },
  'hamilton': {
    'format':'stage-capture','musicalType':'filmed-stage','vocalStyle':['rap','hip-hop','R&B','ensemble belt','rapid-fire patter'],
    'lyricalDensity':5,'musicDrivenPercent':98,'catharsis':5,'rewatchability':5,'familiarityAdvantage':2,
    'bestMood':['locked in','lyric hungry','cathartic','high attention','narrative propulsion'],
    'friction':['very high lyrical density','caption dependence can increase cognitive load'],
    'gatewaySongs':[
      {'song':'Wait for It','purpose':'emotional architecture + belt payoff'},
      {'song':'Satisfied','purpose':'lyrical density + narrative integration'},
      {'song':'Yorktown','purpose':'maximum propulsion'}],
    'notes':'Important counterexample to the idea that familiarity is required for singability. Momentum and emotional legibility can overcome extreme lyrical density.',
  },
  'inside': {
    'format':'other','musicalType':'original','vocalStyle':['synth-pop','comedy patter','intimate vocal','electronic ballad'],
    'lyricalDensity':5,'musicDrivenPercent':92,'catharsis':5,'rewatchability':5,'familiarityAdvantage':2,
    'bestMood':['existential','darkly funny','hyperfocused','cathartic','want to be intellectually moved'],
    'friction':['existential material can intensify a low mood','claustrophobic by design'],
    'gatewaySongs':[
      {'song':'All Eyes on Me','purpose':'full-body catharsis'},
      {'song':'Welcome to the Internet','purpose':'hook density + escalation'},
      {'song':'That Funny Feeling','purpose':'quiet emotional aftershock'}],
    'notes':'A key proof that “musical propulsion” can come from conceptual construction and escalation, not traditional movie-musical form.',
  },
  'ticktick': {
    'format':'film','musicalType':'adaptation','vocalStyle':['contemporary musical theater','rock belt','piano-driven','ensemble'],
    'lyricalDensity':4,'musicDrivenPercent':82,'catharsis':5,'rewatchability':5,'familiarityAdvantage':2,
    'bestMood':['creative urgency','career feelings','need to belt','cathartic','ambitious'],
    'friction':['career anxiety themes can hit personally','grief and mortality undercurrent'],
    'gatewaySongs':[
      {'song':'30/90','purpose':'instant propulsion fingerprint'},
      {'song':'Come to Your Senses','purpose':'belt payoff'},
      {'song':'Louder Than Words','purpose':'emotional thesis + ensemble release'}],
    'notes':'Turns time pressure itself into rhythm. Strong fit when urgency, creative identity, and emotional release need to arrive together.',
  },
  'moana': {
    'format':'animated','musicalType':'original','vocalStyle':['contemporary musical theater','pop belt','character song','ensemble'],
    'lyricalDensity':3,'musicDrivenPercent':72,'catharsis':4.8,'rewatchability':5,'familiarityAdvantage':2,
    'bestMood':['comfort','yearning','reset','sing-along','warm propulsion'],
    'friction':['lower maximalism than the most explosive titles'],
    'gatewaySongs':[
      {'song':'How Far I’ll Go','purpose':'yearning + belt instinct'},
      {'song':'I Am Moana','purpose':'identity catharsis'},
      {'song':'Shiny','purpose':'playful contrast + hook density'}],
    'notes':'Core comfort anchor. Useful because it proves comfort and propulsion are not opposites.',
  },
  'heights': {
    'format':'film','musicalType':'adaptation','vocalStyle':['hip-hop','Latin pop','ensemble belt','rap','contemporary musical theater'],
    'lyricalDensity':4,'musicDrivenPercent':84,'catharsis':4.7,'rewatchability':4.7,'familiarityAdvantage':2,
    'bestMood':['summer energy','communal','movement','yearning','big ensemble'],
    'friction':['long runtime','some quieter narrative stretches'],
    'gatewaySongs':[
      {'song':'96,000','purpose':'maximum ensemble propulsion'},
      {'song':'Breathe','purpose':'yearning + emotional amplitude'},
      {'song':'Carnaval del Barrio','purpose':'communal release'}],
    'notes':'Strong bridge between Hamilton-style lyrical momentum and warmer neighborhood-scale musical storytelling.',
  },
  'greatest': {
    'format':'film','musicalType':'original','vocalStyle':['pop belt','power ballad','ensemble anthem','duet'],
    'lyricalDensity':3,'musicDrivenPercent':76,'catharsis':4.7,'rewatchability':5,'familiarityAdvantage':2,
    'bestMood':['anthem hungry','upbeat','need to move','belt-along','glossy maximalism'],
    'friction':['narrative is less sophisticated than the soundtrack','subtlety is not the point'],
    'gatewaySongs':[
      {'song':'From Now On','purpose':'build-and-release propulsion'},
      {'song':'This Is Me','purpose':'anthemic belt payoff'},
      {'song':'The Other Side','purpose':'rhythmic chemistry + movement'}],
    'notes':'Excellent calibration title for separating musical payoff from plot quality. The soundtrack itself carries extraordinary propulsion.',
  },
  'wicked': {
    'format':'film','musicalType':'adaptation','vocalStyle':['Broadway belt','legit musical theater','ensemble','power ballad'],
    'lyricalDensity':4,'musicDrivenPercent':78,'catharsis':5,'rewatchability':4.8,'familiarityAdvantage':3,
    'bestMood':['belt-along','yearning','defiant','spectacle','emotional payoff'],
    'friction':['long runtime','slower dramatic passages between major numbers'],
    'gatewaySongs':[
      {'song':'Defying Gravity','purpose':'maximum belt + catharsis'},
      {'song':'What Is This Feeling?','purpose':'hook density + comic propulsion'},
      {'song':'The Wizard and I','purpose':'yearning + narrative promise'}],
    'notes':'High-value reference for belt instinct and maximal emotional payoff, while still carrying substantial narrative integration.',
  },
  'across': {
    'format':'film','musicalType':'jukebox','vocalStyle':['rock','psychedelic pop','ensemble','intimate ballad','theatrical cover'],
    'lyricalDensity':3,'musicDrivenPercent':90,'catharsis':4.8,'rewatchability':5,'familiarityAdvantage':4,
    'bestMood':['immersive','dreamy','romantic','belt-along','visual music'],
    'friction':['dreamlike passages slow conventional narrative momentum'],
    'gatewaySongs':[
      {'song':'I Want to Hold Your Hand','purpose':'recontextualization proof'},
      {'song':'Happiness Is a Warm Gun','purpose':'maximalist theatrical transformation'},
      {'song':'All You Need Is Love','purpose':'collective catharsis'}],
    'notes':'A major jukebox reference because familiar music is emotionally reattached to new narrative contexts rather than merely performed.',
  },
  'walkline': {
    'format':'biopic','musicalType':'biographical','vocalStyle':['country','rockabilly','live-performance vocal','duet'],
    'lyricalDensity':2,'musicDrivenPercent':54,'catharsis':4.2,'rewatchability':4.8,'familiarityAdvantage':3,
    'bestMood':['music-biopic','rootsy','romantic tension','performance energy','story first'],
    'friction':['less wall-to-wall musical than traditional musicals','relationship dysfunction is central'],
    'gatewaySongs':[
      {'song':'Jackson','purpose':'chemistry + rhythmic lift'},
      {'song':'Cocaine Blues','purpose':'live-performance propulsion'},
      {'song':'Ring of Fire','purpose':'emotional familiarity anchor'}],
    'notes':'Critical musical-adjacent reference. Demonstrates that performance scenes can provide propulsion even when the film itself is not structurally a musical.',
  },
  'kpop': {
    'format':'animated','musicalType':'original','vocalStyle':['K-pop','pop belt','ensemble','rap','power vocal'],
    'lyricalDensity':4,'musicDrivenPercent':74,'catharsis':4.8,'rewatchability':5,'familiarityAdvantage':1,
    'bestMood':['high energy','hook hungry','movement','belt-along','colorful maximalism'],
    'friction':['hyper-polished pop style may be too glossy for some moods'],
    'gatewaySongs':[
      {'song':'Golden','purpose':'instant hook + belt payoff'},
      {'song':'How It’s Done','purpose':'kinetic group propulsion'},
      {'song':'What It Sounds Like','purpose':'emotional climax'}],
    'notes':'Strong evidence that immediate singability can emerge from hook density and emotional clarity without prior familiarity.',
  },
  'hairspray': {
    'format':'film','musicalType':'adaptation','vocalStyle':['60s pop','soul','Broadway belt','ensemble','gospel-influenced'],
    'lyricalDensity':3,'musicDrivenPercent':82,'catharsis':4.6,'rewatchability':5,'familiarityAdvantage':2,
    'bestMood':['joyful','body movement','communal','bright','belt-along'],
    'friction':['deliberately broad comedy','retro pastiche style'],
    'gatewaySongs':[
      {'song':'Good Morning Baltimore','purpose':'instant tone + propulsion'},
      {'song':'You Can’t Stop the Beat','purpose':'maximum movement + finale release'},
      {'song':'I Know Where I’ve Been','purpose':'emotional amplitude + soul belt'}],
    'notes':'One of the clearest joy-propulsion titles in the catalog. Especially valuable for body movement, communal lift, and replay value.',
  }
}

for tid, enrichment in profiles.items():
    if tid not in by_id:
        raise RuntimeError(f'Missing title id: {tid}')
    enrichment = dict(enrichment)
    enrichment['provenance'] = [
        {'type':'editorial-analysis','source':'Musical Propulsion Engine core enrichment batch v1','scope':'interpretive scoring and fit analysis'}
    ]
    by_id[tid]['enrichment'] = enrichment

path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(f'Enriched {len(profiles)} core titles.')
