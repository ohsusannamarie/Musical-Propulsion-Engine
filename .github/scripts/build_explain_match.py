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

# Connections recommendation rows: add causal explanation under the existing bridge copy.
old = '<small><b style="color:var(--cyan)">the bridge →</b> ${bridge(x,y)}</small>'
new = '<small><b style="color:var(--cyan)">the bridge →</b> ${bridge(x,y)}</small>${matchExplanationMarkup(y,sim(x,y))}'
if old in html:
    html = html.replace(old, new)
elif 'matchExplanationMarkup(y,sim(x,y))' not in html:
    raise RuntimeError('Could not attach explanations to Connections')

# Rabbit Hole cards have their own recommendation renderer. Attach an explanation wherever the match score badge is built.
rabbit_needles = [
    '<span class="rabbit-match">${r.match}%</span>',
    '<div class="rabbit-match">${r.match}%</div>',
    '<span class="match">${r.match}%</span>'
]
attached = False
for needle in rabbit_needles:
    if needle in html:
        html = html.replace(needle, needle + '${matchExplanationMarkup(r.x||r.item||r,r.match)}')
        attached = True
        break
# Do not fail if the Rabbit Hole markup uses a different badge shape. Connections remains fully explainable.

required=['v2.2.6 explain my match','function explainMatch(','function matchExplanationMarkup(','Why this for you','The Musical Propulsion Engine · v2.2.6']
missing=[x for x in required if x not in html]
if missing:
    raise RuntimeError('Missing v2.2.6 markers: '+', '.join(missing))

p.write_text(html,encoding='utf-8')
Path('app.html').write_text(html,encoding='utf-8')
print('v2.2.6 explainable match build complete')
