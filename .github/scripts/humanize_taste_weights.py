from pathlib import Path

for filename in ('index.html', 'app.html'):
    p = Path(filename)
    html = p.read_text(encoding='utf-8')

    if 'function tasteStrengthLabel(' not in html:
        anchor = "function tasteProfileData(){"
        helper = "function tasteStrengthLabel(w){return w>=1.65?'VERY STRONG':w>=1.40?'STRONG':w>=1.15?'MEANINGFUL':w>=.90?'SUPPORTING':'LOW SIGNAL'}\n"
        if anchor not in html:
            raise RuntimeError(f'Could not locate tasteProfileData in {filename}')
        html = html.replace(anchor, helper + anchor, 1)

    old = "<div class=\"taste-metric-head\"><b>${m.label}</b><span>${m.weight.toFixed(2)}×</span></div><div class=\"taste-meter\"><i style=\"width:${m.pct}%\"></i></div><p>${tasteSourceLine(m)}</p>"
    new = "<div class=\"taste-metric-head\"><b>${m.label}</b><span>${tasteStrengthLabel(m.weight)}</span></div><div class=\"taste-meter\"><i style=\"width:${m.pct}%\"></i></div><p><strong>${m.weight.toFixed(2)}× recommendation weighting</strong> · ${tasteSourceLine(m)}</p>"
    if old in html:
        html = html.replace(old, new, 1)
    elif 'recommendation weighting</strong>' not in html:
        raise RuntimeError(f'Could not locate taste metric markup in {filename}')

    p.write_text(html, encoding='utf-8')
