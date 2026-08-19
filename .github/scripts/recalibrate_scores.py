import json, math, statistics
from pathlib import Path

p=Path('data/titles.json')
data=json.loads(p.read_text())
if len(data)<81:
    raise SystemExit(f'REFUSING SCORE CALIBRATION ON PARTIAL CATALOG: {len(data)} titles')

dims=['propulsion','belt','movement','emotion','comfort','maximalism','narrative','hooks','afterglow','replay']

# Preserve the hand-authored/editorial scores permanently. Re-running this script is idempotent.
for x in data:
    if 'scoresRaw' not in x:
        x['scoresRaw']={k:float(x['scores'][k]) for k in dims}

# Percentile calibration keeps ordering intact while giving the engine actual separation.
# We intentionally target 2.0–5.0 rather than 1.0–5.0 because this catalog is curated:
# even its weak examples generally have some musical value.
def percentile_map(values):
    n=len(values)
    ordered=sorted((v,i) for i,v in enumerate(values))
    out=[None]*n
    i=0
    while i<n:
        j=i+1
        while j<n and ordered[j][0]==ordered[i][0]:
            j+=1
        # average rank for ties, zero based
        avg_rank=(i+(j-1))/2
        pct=avg_rank/(n-1) if n>1 else .5
        # Smooth S curve: stronger discrimination near the crowded middle, gentle at extremes.
        curved=0.5+0.5*math.tanh((pct-0.5)*2.25)/math.tanh(1.125)
        score=2.0+3.0*curved
        for k in range(i,j):
            out[ordered[k][1]]=round(score,2)
        i=j
    return out

before={}
after={}
for dim in dims:
    vals=[float(x['scoresRaw'][dim]) for x in data]
    mapped=percentile_map(vals)
    for x,v in zip(data,mapped):
        x['scores'][dim]=v
    before[dim]={
        'mean':round(statistics.mean(vals),2),
        'median':round(statistics.median(vals),2),
        'stdev':round(statistics.pstdev(vals),2),
        'min':min(vals),'max':max(vals),
        'high_4_5_plus':sum(v>=4.5 for v in vals)
    }
    after[dim]={
        'mean':round(statistics.mean(mapped),2),
        'median':round(statistics.median(mapped),2),
        'stdev':round(statistics.pstdev(mapped),2),
        'min':min(mapped),'max':max(mapped),
        'high_4_5_plus':sum(v>=4.5 for v in mapped)
    }

for x in data:
    x['scoreCalibration']={
        'version':'1.0',
        'method':'catalog-percentile-s-curve',
        'rawField':'scoresRaw',
        'note':'Calibrated scores preserve editorial rank order while increasing separation across the curated catalog.'
    }

p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
report={'catalogSize':len(data),'method':'catalog-percentile-s-curve','range':[2.0,5.0],'before':before,'after':after}
Path('data/score-calibration.json').write_text(json.dumps(report,indent=2)+'\n')

md=['# Score Calibration Report','',f'Catalog: **{len(data)} titles**','', 'Editorial scores are preserved in `scoresRaw`. The live `scores` field is now percentile-calibrated so recommendation math has more separation while preserving within-dimension ordering.','', '| Dimension | Raw mean | Calibrated mean | Raw stdev | Calibrated stdev | Raw ≥4.5 | Calibrated ≥4.5 |','|---|---:|---:|---:|---:|---:|---:|']
for d in dims:
    md.append(f"| {d} | {before[d]['mean']} | {after[d]['mean']} | {before[d]['stdev']} | {after[d]['stdev']} | {before[d]['high_4_5_plus']} | {after[d]['high_4_5_plus']} |")
Path('data/SCORE_CALIBRATION.md').write_text('\n'.join(md)+'\n')
print('Calibrated',len(data),'titles')
for d in dims:
    print(d,'stdev',before[d]['stdev'],'->',after[d]['stdev'],'high>=4.5',before[d]['high_4_5_plus'],'->',after[d]['high_4_5_plus'])
