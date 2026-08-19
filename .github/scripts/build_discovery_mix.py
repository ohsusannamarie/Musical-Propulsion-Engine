from pathlib import Path
import re

for filename in ('index.html','app.html'):
    p=Path(filename)
    html=p.read_text(encoding='utf-8')
    html=html.replace('The Musical Propulsion Engine · v2.3.1','The Musical Propulsion Engine · v2.3.2')

    marker='/* v2.3.2 discovery mix */'
    if marker not in html:
        css='''<style>
/* v2.3.2 discovery mix */
.discovery-mix{margin:0 0 16px;border:1px solid #30384b;border-radius:16px;padding:16px;background:radial-gradient(circle at 92% 0%,rgba(173,125,255,.09),transparent 30%),linear-gradient(135deg,rgba(15,24,34,.96),rgba(8,10,16,.98));box-shadow:var(--shadow)}
.discovery-mix-head{display:flex;gap:12px;align-items:end;justify-content:space-between;flex-wrap:wrap;margin-bottom:12px}.discovery-mix-head h3{font-family:Georgia,serif;font-size:24px;font-weight:500;margin:0}.discovery-mix-head p{font-size:10px;color:#9da8b8;margin:3px 0 0;line-height:1.45;max-width:680px}.discovery-mix-anchor{font-size:9px;color:#7f8999}.discovery-mix-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.discovery-pick{border:1px solid #293246;border-radius:12px;overflow:hidden;background:#0d121c;cursor:pointer;transition:.16s ease}.discovery-pick:hover{transform:translateY(-2px);border-color:#536078}.discovery-poster{height:190px;position:relative;overflow:hidden;background:#121827}.discovery-poster img{width:100%;height:100%;object-fit:cover;display:block}.discovery-poster:after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 42%,rgba(7,8,13,.86))}.discovery-rank{position:absolute;z-index:2;left:9px;top:9px}.discovery-score{position:absolute;z-index:2;right:9px;top:9px;width:42px;height:42px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--pink);background:rgba(7,8,13,.82);color:#ff82a7;font-size:10px;font-weight:800}.discovery-title{position:absolute;z-index:2;left:10px;right:10px;bottom:10px;font-family:Georgia,serif;font-size:20px;line-height:1;color:#fff;text-shadow:0 2px 15px #000}.discovery-copy{padding:11px}.discovery-copy p{font-size:9px;color:#aeb8c7;line-height:1.45;margin:0 0 8px}.discovery-gateway{font-size:9px;color:#79e59f;font-weight:750}.discovery-pick.safe .discovery-rank{color:#8ef0ad}.discovery-pick.stretch .discovery-rank{color:#f6c35b}.discovery-pick.wild .discovery-rank{color:#c8a8ff}
@media(max-width:900px){.discovery-mix-grid{grid-template-columns:1fr 1fr}.discovery-pick:last-child{grid-column:1/-1}.discovery-pick:last-child .discovery-poster{height:220px}}
@media(max-width:700px){.discovery-mix{padding:12px}.discovery-mix-grid{grid-template-columns:1fr}.discovery-pick:last-child{grid-column:auto}.discovery-poster,.discovery-pick:last-child .discovery-poster{height:210px}.discovery-mix-head h3{font-size:22px}}
</style>'''
        html=html.replace('</head>',css+'</head>',1)

    if 'id="discoveryMix"' not in html:
        anchor='<section id="discover" class="section active">'
        if anchor not in html:
            raise RuntimeError(f'discover section anchor missing in {filename}')
        html=html.replace(anchor,anchor+'\n<div id="discoveryMix"></div>',1)

    if 'function renderDiscoveryMix()' not in html:
        anchor='function discoveryReason(a,b)'
        pos=html.find(anchor)
        if pos<0:
            raise RuntimeError(f'discoveryReason missing in {filename}')
        end=html.find('\n',html.find('}',pos))+1
        js=r'''
function discoveryMixPicks(){
  const a=byId[selected]||D[0];
  const pool=D.filter(x=>x.id!==a.id&&stat(x)!=='miss'&&stat(x)!=='later');
  const bestFor=(kind)=>pool.filter(x=>discoveryClass(a,x)===kind).sort((x,y)=>discoveryScore(a,y)-discoveryScore(a,x)||personalFit(y)-personalFit(x))[0];
  const used=new Set();
  const picks=[];
  ['safe','stretch','wild'].forEach(kind=>{let x=bestFor(kind);if(!x)x=pool.filter(z=>!used.has(z.id)).sort((u,v)=>discoveryScore(a,v)-discoveryScore(a,u))[0];if(x){used.add(x.id);picks.push({kind,x})}});
  return {a,picks};
}
function renderDiscoveryMix(){
  const host=document.getElementById('discoveryMix');if(!host)return;
  const {a,picks}=discoveryMixPicks();
  const labels={safe:'Safe bet',stretch:'Smart stretch',wild:'Wild card'};
  host.innerHTML=`<div class="discovery-mix"><div class="discovery-mix-head"><div><h3>Your discovery mix</h3><p>Three different bets from the same taste model: one highly trusted match, one adjacent surprise, and one useful leap.</p></div><div class="discovery-mix-anchor">Built from ${a.title}</div></div><div class="discovery-mix-grid">${picks.map(({kind,x})=>`<article class="discovery-pick ${kind}" data-id="${x.id}"><div class="discovery-poster has-media">${posterMarkup(x)}<span class="discovery-rank">${labels[kind]}</span><span class="discovery-score">${discoveryScore(a,x)}%</span><div class="discovery-title">${x.title}</div></div><div class="discovery-copy"><p>${discoveryReason(a,x)}</p><div class="discovery-gateway">Gateway song: ${x.songs?.[0]||'Open profile to explore'}</div></div></article>`).join('')}</div></div>`;
}
'''
        html=html[:end]+js+html[end:]

    if 'renderDiscoveryMix();' not in html:
        pattern=r'function renderAll\(\)\{([^}]*)\}'
        m=re.search(pattern,html)
        if not m:
            raise RuntimeError(f'renderAll missing in {filename}')
        body=m.group(1)
        replacement='function renderAll(){renderDiscoveryMix();'+body+'}'
        html=html[:m.start()]+replacement+html[m.end():]

    required=['v2.3.2 discovery mix','id="discoveryMix"','function renderDiscoveryMix()','function discoveryMixPicks()','Your discovery mix','Safe bet','Smart stretch','Wild card']
    missing=[x for x in required if x not in html]
    if missing:
        raise RuntimeError(f'{filename} missing: '+', '.join(missing))

    p.write_text(html,encoding='utf-8')

print('v2.3.2 Discovery Mix build complete')
