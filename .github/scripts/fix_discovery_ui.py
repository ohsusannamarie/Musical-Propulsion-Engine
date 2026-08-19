from pathlib import Path

for filename in ('index.html','app.html'):
    p=Path(filename)
    html=p.read_text(encoding='utf-8')

    double='${matchExplanationMarkup(r,sim(x,r))}${matchExplanationMarkup(r,sim(x,r))}'
    single='${matchExplanationMarkup(r,sim(x,r))}'
    discovery='${matchExplanationMarkup(r,sim(x,r))}<div class="discovery-lens"><span class="discovery-pill ${discoveryClass(x,r)}">${discoveryLabel(x,r)}</span></div><div class="discovery-explain">${discoveryReason(x,r)}</div>'

    if double in html:
        html=html.replace(double,discovery)
    elif discovery not in html:
        if single not in html:
            raise RuntimeError(f'Could not locate recommendation explanation markup in {filename}')
        html=html.replace(single,discovery,1)

    # Clean up any accidental repeated explanatory panels left by older builders.
    while '${matchExplanationMarkup(r,sim(x,r))}${matchExplanationMarkup(r,sim(x,r))}' in html:
        html=html.replace('${matchExplanationMarkup(r,sim(x,r))}${matchExplanationMarkup(r,sim(x,r))}',single)

    # Verify discovery intelligence itself exists before writing.
    required=['function discoveryClass(','function discoveryLabel(','function discoveryReason(','discovery-pill']
    missing=[x for x in required if x not in html]
    if missing:
        raise RuntimeError(f'Missing discovery intelligence in {filename}: {missing}')

    p.write_text(html,encoding='utf-8')

print('Discovery UI repaired: duplicate Why This For You removed and recommendation classes surfaced.')
