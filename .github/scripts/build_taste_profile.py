from pathlib import Path

p = Path('index.html')
html = p.read_text(encoding='utf-8')

# Version bump without disturbing previous feature markers.
html = html.replace('The Musical Propulsion Engine · v2.2.6', 'The Musical Propulsion Engine · v2.3.0')
html = html.replace('<div class="brand"><small>THE · V2.2</small>', '<div class="brand"><small>THE · V2.3</small>')
html = html.replace('V2.2.6 · THE RABBIT HOLE', 'V2.3.0 · THE RABBIT HOLE')

marker = '/* v2.3.0 taste intelligence */'
if marker not in html:
    css = '''<style>
/* v2.3.0 taste intelligence */
.taste-shell{border:1px solid #343d50;border-radius:20px;padding:22px;background:radial-gradient(circle at 90% 4%,rgba(84,217,255,.12),transparent 28%),radial-gradient(circle at 6% 95%,rgba(255,95,143,.10),transparent 30%),linear-gradient(145deg,#0b111b,#090b12 62%,#120c17);box-shadow:var(--shadow)}
.taste-hero{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(230px,.6fr);gap:18px;align-items:start;padding-bottom:18px;border-bottom:1px solid var(--line)}
.taste-kicker{font-size:10px;letter-spacing:.15em;color:var(--gold);font-weight:850}.taste-hero h2{font-family:Georgia,serif;font-size:36px;font-weight:500;line-height:1.02;margin:5px 0 8px}.taste-hero h2 em{color:#ff83aa}.taste-hero p{color:#adb7c7;font-size:12px;line-height:1.6;max-width:760px;margin:0}
.taste-confidence{border:1px solid rgba(84,217,255,.22);border-radius:13px;padding:13px;background:rgba(84,217,255,.045)}.taste-confidence span{font-size:9px;letter-spacing:.08em;text-transform:uppercase;color:#8fdfff;font-weight:800}.taste-confidence b{display:block;font-family:Georgia,serif;font-size:26px;color:#f6f1e8;margin:3px 0}.taste-confidence small{display:block;color:#96a2b4;font-size:9px;line-height:1.45}
.taste-summary{margin:16px 0 12px;padding:14px 15px;border:1px solid rgba(246,195,91,.19);border-radius:12px;background:rgba(246,195,91,.045);font-size:11px;line-height:1.55;color:#cdd4df}.taste-summary strong{color:#ffe08c}
.taste-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.taste-metric{border:1px solid #293246;border-radius:12px;padding:12px;background:linear-gradient(160deg,#101622,#0b0f17)}.taste-metric-head{display:flex;justify-content:space-between;gap:10px;align-items:baseline}.taste-metric-head b{font-size:11px;color:#f4f0e9}.taste-metric-head span{font-size:10px;color:#ff86aa;font-weight:800}.taste-meter{height:7px;background:#1c2330;border-radius:99px;overflow:hidden;margin:9px 0 8px}.taste-meter i{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,var(--cyan),var(--pink),var(--gold))}.taste-metric p{font-size:9px;line-height:1.45;color:#9ca7b7;margin:0}.taste-metric p strong{color:#d9dee8}
.taste-lower{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}.taste-card{border:1px solid #293246;border-radius:13px;padding:14px;background:#0d121c}.taste-card h3{font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:#71ddff;margin:0 0 10px}.taste-card p{font-size:10px;line-height:1.5;color:#aeb8c7;margin:0 0 8px}.taste-evidence-row{padding:8px 0;border-bottom:1px solid rgba(255,255,255,.055)}.taste-evidence-row:last-child{border-bottom:0}.taste-evidence-row b{display:block;font-size:10px;color:#f4f0e9}.taste-evidence-row span{display:block;font-size:9px;color:#8f9bac;margin-top:3px;line-height:1.4}.taste-exception{padding:9px 10px;border-radius:9px;background:rgba(255,95,143,.055);border:1px solid rgba(255,95,143,.12);margin:7px 0;font-size:9px;line-height:1.45;color:#b9c2d0}.taste-exception strong{color:#ff9ab7}.taste-history-note{margin-top:12px;padding:10px 11px;border-radius:9px;background:rgba(114,224,155,.045);border:1px solid rgba(114,224,155,.14);font-size:9px;color:#a9c9b5;line-height:1.5}.taste-history-note strong{color:#79e59f}
@media(max-width:900px){.taste-hero{grid-template-columns:1fr}.taste-lower{grid-template-columns:1fr}}
@media(max-width:700px){.taste-shell{padding:15px;border-radius:15px}.taste-hero h2{font-size:29px}.taste-grid{grid-template-columns:1fr}.taste-confidence{padding:11px}.taste-metric{padding:11px}.taste-lower{gap:10px}.taste-card{padding:12px}}
</style>'''
    html = html.replace('</head>', css + '</head>', 1)

# Add a dedicated My Taste navigation item.
nav_anchor = '<button data-section="library"><span class="ico">🎞️</span><span>YOUR LIBRARY<small>Your history & statuses</small></span></button>'
nav_item = '<button data-section="taste"><span class="ico">🧬</span><span>MY TASTE<small>What the engine has learned</small></span></button>\n      ' + nav_anchor
if 'data-section="taste"' not in html:
    if nav_anchor not in html:
        raise RuntimeError('Could not locate library nav item')
    html = html.replace(nav_anchor, nav_item, 1)

# Give the existing sidebar profile a live target while preserving its static fallback.
html = html.replace('<div class="profile-mini">', '<div class="profile-mini" id="profileMini">', 1)

# Add the Taste Intelligence section before the library.
section_anchor = '    <section id="library" class="section">'
if '<section id="taste" class="section">' not in html:
    if section_anchor not in html:
        raise RuntimeError('Could not locate library section')
    taste_section = '''    <section id="taste" class="section">
      <div class="taste-shell">
        <div class="taste-hero">
          <div><div class="taste-kicker">V2.3 · TASTE INTELLIGENCE</div><h2>This is what the engine thinks <em>moves you.</em></h2><p>Your profile is inferred from library reactions plus every More of This / Less of This calibration. Nothing here is a permanent label. It is the engine showing its work.</p></div>
          <div class="taste-confidence" id="tasteConfidence"></div>
        </div>
        <div class="taste-summary" id="tasteSummary"></div>
        <div class="taste-grid" id="tasteMetricsGrid"></div>
        <div class="taste-lower">
          <div class="taste-card"><h3>What taught the engine</h3><div id="tasteEvidence"></div></div>
          <div class="taste-card"><h3>Exceptions & context</h3><div id="tasteExceptions"></div><div class="taste-history-note" id="tasteHistory"></div></div>
        </div>
      </div>
    </section>

'''
    html = html.replace(section_anchor, taste_section + section_anchor, 1)

# Add profile intelligence helpers immediately after tasteEvidenceCount().
helper_anchor = "function tasteEvidenceCount(){return Object.keys(tasteFeedback).filter(id=>{const f=feedbackFor(id);return f.more.length||f.less.length}).length}"
if 'function tasteProfileData()' not in html:
    if helper_anchor not in html:
        raise RuntimeError('Could not locate taste evidence helper')
    helpers = r'''
let tasteHistory=[]; try{tasteHistory=JSON.parse(localStorage.getItem('mpe-taste-history-v1')||'[]')}catch(e){tasteHistory=[]}
function saveTasteHistory(){try{localStorage.setItem('mpe-taste-history-v1',JSON.stringify(tasteHistory.slice(-60)))}catch(e){}}
function tasteReactionCount(){return D.filter(x=>['moved','liked','miss','revisit'].includes(stat(x))).length}
function tasteConfidenceInfo(){const explicit=tasteEvidenceCount(),reactions=tasteReactionCount(),evidence=explicit*2+Math.min(reactions,12);return evidence>=16?{label:'High confidence',detail:'The model has multiple explicit calibrations plus a meaningful reaction history.'}:evidence>=8?{label:'Growing confidence',detail:'Patterns are emerging, but a few more explicit calibrations will sharpen the edges.'}:{label:'Early model',detail:'The engine has useful signals, but it is still learning what is essential versus merely correlated.'}}
function metricExplicitTitles(k,dir){return Object.keys(tasteFeedback).filter(id=>feedbackFor(id)[dir].includes(k)).map(id=>byId[id]).filter(Boolean)}
function metricStatusTitles(k){return D.filter(x=>stat(x)==='moved'&&x.scores[k]>=4.7).sort((a,b)=>b.scores[k]-a.scores[k])}
function tasteProfileData(){const w=tasteWeights();return tasteMetrics.map(k=>{const more=metricExplicitTitles(k,'more'),less=metricExplicitTitles(k,'less'),status=metricStatusTitles(k);const pct=Math.max(4,Math.min(100,Math.round((w[k]-.58)/(1.75-.58)*100)));return {k,label:metricLabel(k),weight:w[k],pct,more,less,status}}).sort((a,b)=>b.weight-a.weight)}
function tasteSourceLine(m){const explicit=m.more.length?`Explicitly reinforced by ${m.more.slice(0,2).map(x=>x.title).join(' + ')}`:'';const moved=m.status.length?`Strong in ${m.status.slice(0,2).map(x=>x.title).join(' + ')}`:'';const less=m.less.length?`Dialed down by ${m.less.slice(0,2).map(x=>x.title).join(' + ')}`:'';return [explicit,moved,less].filter(Boolean).join(' · ')||'Inferred mostly from your broader library pattern.'}
function tasteExceptions(){const data=tasteProfileData(),out=[];data.slice(0,4).forEach(m=>{const exception=D.filter(x=>stat(x)==='moved'&&x.scores[m.k]<=3.8).sort((a,b)=>a.scores[m.k]-b.scores[m.k])[0];if(exception)out.push(`<div class="taste-exception"><strong>${m.label} usually matters, but it is not a rule.</strong> ${exception.title} still moved you at ${exception.scores[m.k].toFixed(1)}/5, so the engine should not treat this dimension as mandatory.</div>`)});const context=D.find(x=>stat(x)==='later'&&tasteMetrics.some(k=>x.scores[k]>=4.7));if(context)out.push(`<div class="taste-exception"><strong>Context can override fit.</strong> ${context.title} scores strongly on several dimensions but is marked Not right now. The engine preserves that boundary instead of learning “dislike.”</div>`);return out.slice(0,3)}
function recordTasteSnapshot(reason){const weights=tasteWeights(),stamp={t:Date.now(),reason,weights};const last=tasteHistory[tasteHistory.length-1];if(last&&tasteMetrics.every(k=>Math.abs((last.weights?.[k]||0)-weights[k])<.001))return;tasteHistory.push(stamp);saveTasteHistory()}
function ensureTasteBaseline(){if(!tasteHistory.length){tasteHistory=[{t:Date.now(),reason:'baseline',weights:tasteWeights()}];saveTasteHistory()}}
function tasteHistoryText(){if(tasteHistory.length<2)return '<strong>Learning history starts here.</strong> Future calibration changes will be saved on this device so the profile can show how your taste model evolves.';const first=tasteHistory[0].weights||{},now=tasteWeights();const changes=tasteMetrics.map(k=>({k,d:(now[k]||1)-(first[k]||1)})).sort((a,b)=>Math.abs(b.d)-Math.abs(a.d)).filter(x=>Math.abs(x.d)>=.03).slice(0,2);return changes.length?`<strong>${tasteHistory.length} taste snapshots saved.</strong> Biggest movement since baseline: ${changes.map(x=>`${metricLabel(x.k)} ${x.d>0?'↑':'↓'} ${Math.abs(x.d).toFixed(2)}`).join(' · ')}.`:`<strong>${tasteHistory.length} taste snapshots saved.</strong> Your profile has been relatively stable since the baseline.`}
function renderTasteProfile(){
  const shell=document.getElementById('tasteMetricsGrid');if(!shell)return;
  const data=tasteProfileData(),top=data.slice(0,3),conf=tasteConfidenceInfo();
  document.getElementById('tasteConfidence').innerHTML=`<span>Model confidence</span><b>${conf.label}</b><small>${tasteEvidenceCount()} explicitly calibrated title${tasteEvidenceCount()===1?'':'s'} · ${tasteReactionCount()} reaction signals<br>${conf.detail}</small>`;
  document.getElementById('tasteSummary').innerHTML=`Right now the engine sees <strong>${top.map(x=>x.label).join(' + ')}</strong> as your strongest propulsion signals. That does not mean every favorite must max them out. Exceptions are part of the model, not errors in it.`;
  shell.innerHTML=data.map(m=>`<div class="taste-metric"><div class="taste-metric-head"><b>${m.label}</b><span>${m.weight.toFixed(2)}×</span></div><div class="taste-meter"><i style="width:${m.pct}%"></i></div><p>${tasteSourceLine(m)}</p></div>`).join('');
  document.getElementById('tasteEvidence').innerHTML=top.map(m=>`<div class="taste-evidence-row"><b>${m.label}</b><span>${tasteSourceLine(m)}</span></div>`).join('')+`<div class="taste-evidence-row"><b>Evidence mix</b><span>Explicit calibrations carry the most weight. Moved Me, Liked, Revisit, and Didn’t Ignite contribute softer signals. Not right now remains contextual rather than negative.</span></div>`;
  const exceptions=tasteExceptions();document.getElementById('tasteExceptions').innerHTML=exceptions.length?exceptions.join(''):'<p>No strong exception pattern yet. The engine needs a little more contradictory evidence before it can distinguish a true requirement from a frequent companion.</p>';
  document.getElementById('tasteHistory').innerHTML=tasteHistoryText();
  const mini=document.getElementById('profileMini');if(mini)mini.innerHTML=`<h3>Live Taste Profile</h3><p>${conf.label}. ${tasteEvidenceCount()} title${tasteEvidenceCount()===1?'':'s'} explicitly calibrated.</p>${data.slice(0,4).map(m=>`<span style="font-size:9px;color:#e7eaf0">${m.label}</span><div class="bar"><i style="width:${m.pct}%"></i></div>`).join('')}`;
}
'''
    html = html.replace(helper_anchor, helper_anchor + helpers, 1)

# Keep the profile live whenever calibration or status feedback changes.
html = html.replace("tasteFeedback[id]=f;saveTasteFeedback();renderAll();return", "tasteFeedback[id]=f;saveTasteFeedback();recordTasteSnapshot('calibration');renderAll();return")
html = html.replace("delete tasteFeedback[reset.dataset.tasteReset];saveTasteFeedback();renderAll();return", "delete tasteFeedback[reset.dataset.tasteReset];saveTasteFeedback();recordTasteSnapshot('reset');renderAll();return")

old_render_all = 'function renderAll(){renderRabbit();renderModes();renderFeature();renderConnections();renderTabs();renderCards();renderLibrary();renderGraph();renderTonight();}'
new_render_all = 'function renderAll(){renderRabbit();renderModes();renderFeature();renderConnections();renderTabs();renderCards();renderLibrary();renderGraph();renderTonight();renderTasteProfile();}'
if old_render_all in html:
    html = html.replace(old_render_all, new_render_all, 1)
elif 'renderTasteProfile();}' not in html:
    raise RuntimeError('Could not upgrade renderAll for Taste Profile')

status_old = "renderCards();renderConnections();renderRabbit();renderTonight();if(e.target.dataset.statusId===selected)renderFeature();"
status_new = "recordTasteSnapshot('status');renderCards();renderConnections();renderRabbit();renderTonight();renderTasteProfile();if(e.target.dataset.statusId===selected)renderFeature();"
if status_old in html:
    html = html.replace(status_old, status_new, 1)
elif "recordTasteSnapshot('status')" not in html:
    raise RuntimeError('Could not connect status changes to Taste Profile')

html = html.replace("renderAll(); document.documentElement.classList.add('js-ok');", "ensureTasteBaseline();renderAll(); document.documentElement.classList.add('js-ok');", 1)

required = [
    'The Musical Propulsion Engine · v2.3.0',
    'data-section="taste"',
    '<section id="taste" class="section">',
    'function tasteProfileData()',
    'function renderTasteProfile()',
    'function recordTasteSnapshot(reason)',
    'mpe-taste-history-v1',
    'What taught the engine',
    'Exceptions & context',
    'renderTasteProfile();',
]
missing = [x for x in required if x not in html]
if missing:
    raise RuntimeError('Missing v2.3.0 Taste Profile markers: ' + ', '.join(missing))

p.write_text(html, encoding='utf-8')
Path('app.html').write_text(html, encoding='utf-8')
print('v2.3.0 Taste Intelligence build complete')
