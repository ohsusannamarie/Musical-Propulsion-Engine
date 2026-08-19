from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

html = html.replace('The Musical Propulsion Engine · v2.2.5', 'The Musical Propulsion Engine · v2.2.6')
html = html.replace('V2.2.5 · THE RABBIT HOLE', 'V2.2.6 · THE RABBIT HOLE')

marker = '/* v2.2.6 explain my match */'
if marker not in html:
    css = '''<style>
/* v2.2.6 explain my match */
.match-explain{margin-top:6px;padding:7px 9px;border-radius:8px;background:rgba(84,217,255,.055);border:1px solid rgba(84,217,255,.13);font-size:9px;line-height:1.45;color:#aeb8c7}
.match-explain b{color:#72dfff;text-transform:uppercase;letter-spacing:.05em;font-size:8px}
.match-explain strong{color:#f5f0e8;font-weight:750}
.match-explain .friction{color:#dba5b6}
.match-explain .confidence{color:#f6c35b}
@media(max-width:700px){.match-explain{font-size:9px;padding:8px 9px}}
</style>'''
    html = html.replace('</head>', css + '</head>', 1)

map_marker = '/* v2.2.6 connection map detail */'
if map_marker not in html:
    css = '''<style>
/* v2.2.6 connection map detail */
.graph-wrap{height:auto;min-height:0;overflow:visible;padding:10px;background:radial-gradient(circle at 50% 38%,rgba(84,217,255,.07),transparent 34%),#080b11}
.graph-stage{height:500px;position:relative;overflow:hidden;border-radius:10px}
.graph-stage svg{width:100%;height:100%;display:block}
.graph-node text{font-size:13px;pointer-events:none}
.graph-node circle{transition:.18s ease;cursor:pointer}
.graph-node:hover circle,.graph-node.focused circle{fill:#21172a;stroke:#54d9ff;stroke-width:3}
.graph-node.focused text{font-weight:800}
.graph-explain-panel{margin-top:10px;padding:16px;border:1px solid rgba(84,217,255,.19);border-radius:12px;background:linear-gradient(135deg,rgba(84,217,255,.065),rgba(255,95,143,.045));color:#bdc6d3}
.graph-explain-panel h3{font-family:Georgia,serif;font-weight:500;font-size:22px;line-height:1.08;color:#f6f1e8;margin:5px 0 8px}
.graph-explain-panel p{font-size:11px;line-height:1.5;margin:0 0 7px;color:#b8c1cf}
.graph-explain-panel .shared-dna strong{color:#f6c35b}
.graph-open{margin-top:10px;border:1px solid #39445b;background:#111724;color:#f6f1e8;border-radius:8px;padding:9px 11px;font-size:10px;cursor:pointer}
.graph-hint{font-size:9px;color:#7f8999;margin:0 0 4px}
@media(max-width:700px){
  .graph-wrap{padding:6px}
  .graph-stage{height:370px}
  .graph-node text{font-size:14px}
  .graph-explain-panel{padding:13px;margin-top:6px}
  .graph-explain-panel h3{font-size:20px}
}
</style>'''
    html = html.replace('</head>', css + '</head>', 1)

anchor = 'function tasteEvidenceCount(){'
if 'function explainMatch(' not in html:
    pos = html.find(anchor)
    if pos < 0:
        raise RuntimeError('Could not locate taste model helpers')
    end = html.find('\n', html.find('}', pos)) + 1
    helpers = r'''
function explainMatch(x,base){
  const w=tasteWeights();
  const ranked=tasteMetrics.map(k=>({k,impact:(x.scores[k]||0)*w[k],score:x.scores[k]||0,weight:w[k]})).sort((a,b)=>b.impact-a.impact);
  const strong=ranked.filter(v=>v.score>=4 && v.weight>=1.02).slice(0,2);
  const fallback=ranked.slice(0,2);
  const wins=(strong.length?strong:fallback).map(v=>metricLabel(v.k));
  const friction=[...ranked].reverse().find(v=>v.score<=3 && v.weight>=1.05);
  const evidence=tasteEvidenceCount();
  const confidence=evidence>=5?'High':evidence>=2?'Growing':'Early';
  const learned=evidence?`${evidence} explicit calibration${evidence===1?'':'s'} + library reactions`:'your library reactions';
  return {wins,friction:friction?metricLabel(friction.k):'',confidence,learned,score:base};
}
function matchExplanationMarkup(x,base){
  const e=explainMatch(x,base);
  return `<div class="match-explain"><b>Why this for you</b><br><strong>${e.wins.join(' + ')}</strong> align with what your taste model currently values.${e.friction?` <span class="friction">Possible friction: ${e.friction}.</span>`:''}<br><span class="confidence">${e.confidence} confidence</span> · Learned from ${e.learned}.</div>`;
}
'''
    html = html[:end] + helpers + html[end:]

# Recommendation-list explanations.
old = '<small class="shared-reason"><b>the bridge →</b> ${rabbitBridge(x,r,\'all\')}</small>'
new = '<small class="shared-reason"><b>the bridge →</b> ${rabbitBridge(x,r,\'all\')}</small>${matchExplanationMarkup(r,sim(x,r))}'
if old in html:
    html = html.replace(old, new, 1)
elif 'matchExplanationMarkup(r,sim(x,r))' not in html:
    raise RuntimeError('Could not attach explanations to Connections')

# Turn the Connection Map into an inspectable relationship view.
old_graph = '''function renderGraph(){const x=byId[selected], rel=(x.links||[]).map(id=>byId[id]).filter(Boolean).slice(0,8); const W=1000,H=600,cx=500,cy=300,R=210;let lines='',nodes='';rel.forEach((r,i)=>{const a=(Math.PI*2*i/rel.length)-Math.PI/2;const px=cx+Math.cos(a)*R,py=cy+Math.sin(a)*R;lines+=`<line class="graph-line ${sim(x,r)>87?'hot':''}" x1="${cx}" y1="${cy}" x2="${px}" y2="${py}"/>`;nodes+=`<g class="graph-node" data-id="${r.id}"><circle cx="${px}" cy="${py}" r="54"/><text x="${px}" y="${py-4}" text-anchor="middle">${r.title.length>20?r.title.slice(0,18)+'…':r.title}</text><text x="${px}" y="${py+15}" text-anchor="middle" style="fill:#ff7fa5">${sim(x,r)}%</text></g>`});nodes+=`<g class="graph-node center"><circle cx="${cx}" cy="${cy}" r="72"/><text x="${cx}" y="${cy-3}" text-anchor="middle" style="font-size:13px">${x.title.length>22?x.title.slice(0,21)+'…':x.title}</text><text x="${cx}" y="${cy+19}" text-anchor="middle" style="fill:#ffc4d5">SELECTED</text></g>`;document.getElementById('graph').innerHTML=`<svg viewBox="0 0 ${W} ${H}">${lines}${nodes}</svg>`}'''
new_graph = r'''let graphFocus=null;
function renderGraph(){
  const x=byId[selected],rel=(x.links||[]).map(id=>byId[id]).filter(Boolean).slice(0,8);
  if(!rel.length){document.getElementById('graph').innerHTML='<div class="empty">No mapped connections yet.</div>';return}
  if(!graphFocus||!rel.some(r=>r.id===graphFocus))graphFocus=rel[0].id;
  const focus=byId[graphFocus];
  const W=700,H=500,cx=350,cy=245,R=168;
  let lines='',nodes='';
  rel.forEach((r,i)=>{
    const a=(Math.PI*2*i/rel.length)-Math.PI/2,px=cx+Math.cos(a)*R,py=cy+Math.sin(a)*R;
    lines+=`<line class="graph-line ${sim(x,r)>87?'hot':''}" x1="${cx}" y1="${cy}" x2="${px}" y2="${py}"/>`;
    nodes+=`<g class="graph-node ${r.id===graphFocus?'focused':''}" data-connection-id="${r.id}"><circle cx="${px}" cy="${py}" r="59"/><text x="${px}" y="${py-5}" text-anchor="middle">${r.title.length>18?r.title.slice(0,17)+'…':r.title}</text><text x="${px}" y="${py+17}" text-anchor="middle" style="fill:#ff7fa5;font-weight:800">${sim(x,r)}%</text></g>`;
  });
  nodes+=`<g class="graph-node center"><circle cx="${cx}" cy="${cy}" r="77"/><text x="${cx}" y="${cy-4}" text-anchor="middle" style="font-size:14px">${x.title.length>20?x.title.slice(0,19)+'…':x.title}</text><text x="${cx}" y="${cy+20}" text-anchor="middle" style="fill:#ffc4d5;font-size:11px">ANCHOR</text></g>`;
  const sharedDna=x.dna.filter(v=>focus.dna.includes(v));
  const sharedVibe=x.vibe.filter(v=>focus.vibe.includes(v));
  const bridge=rabbitBridge(x,focus,'all');
  const detail=`<div class="graph-explain-panel"><div class="graph-hint">Tap another node to inspect a different relationship.</div><span class="learn-badge">🕸 WHY THIS CONNECTS</span><h3>${focus.title} ↔ ${x.title}</h3><p class="shared-dna"><strong>The bridge:</strong> ${bridge}</p>${sharedDna.length?`<p><strong>Shared musical DNA:</strong> ${sharedDna.join(' · ')}</p>`:''}${sharedVibe.length?`<p><strong>Shared vibe:</strong> ${sharedVibe.join(' · ')}</p>`:''}${matchExplanationMarkup(focus,sim(x,focus))}<button class="graph-open" type="button" data-id="${focus.id}">Open ${focus.title} profile →</button></div>`;
  document.getElementById('graph').innerHTML=`<div class="graph-stage"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Connection map for ${x.title}">${lines}${nodes}</svg></div>${detail}`;
}'''
if 'let graphFocus=null;' not in html:
    if old_graph not in html:
        raise RuntimeError('Could not locate current Connection Map renderer')
    html = html.replace(old_graph, new_graph, 1)

# Node taps should inspect the relationship, not immediately navigate away.
if "const graphNode=e.target.closest('[data-connection-id]')" not in html:
    click_anchor = "const nav=e.target.closest('[data-section]');"
    click_upgrade = "const graphNode=e.target.closest('[data-connection-id]');if(graphNode){graphFocus=graphNode.dataset.connectionId;renderGraph();return}const nav=e.target.closest('[data-section]');"
    if click_anchor not in html:
        raise RuntimeError('Could not locate click dispatcher for Connection Map')
    html = html.replace(click_anchor, click_upgrade, 1)

required=[
    'v2.2.6 explain my match',
    'function explainMatch(',
    'function matchExplanationMarkup(',
    'Why this for you',
    'matchExplanationMarkup(r,sim(x,r))',
    'The Musical Propulsion Engine · v2.2.6',
    'v2.2.6 connection map detail',
    'let graphFocus=null;',
    'data-connection-id',
    'graph-explain-panel',
    'WHY THIS CONNECTS'
]
missing=[x for x in required if x not in html]
if missing:
    raise RuntimeError('Missing v2.2.6 markers: '+', '.join(missing))

p.write_text(html,encoding='utf-8')
Path('app.html').write_text(html,encoding='utf-8')
print('v2.2.6 Connection Map explanation build complete')
